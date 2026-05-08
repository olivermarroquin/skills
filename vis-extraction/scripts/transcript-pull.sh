#!/usr/bin/env bash
# transcript-pull.sh — fetch and clean transcript/text from a URL or local file
#
# Usage:
#   ./transcript-pull.sh <url-or-path> [output-dir]
#
# Examples:
#   ./transcript-pull.sh https://www.youtube.com/watch?v=ABC123
#   ./transcript-pull.sh https://example.com/blog/article
#   ./transcript-pull.sh /path/to/transcript.txt
#
# Output: a markdown file in the cache dir (default: ./cache/) with format:
#   transcript-YYYY-MM-DD-HHMMSS-<slug>.md
#
# Architecture: separates fetch from extract.
#   - YouTube path:  yt-dlp pulls captions
#   - Article path:  curl fetches with browser-like headers, then trafilatura extracts
#   - File path:     reads local file, strips noise from VTT/SRT
#
# Why curl-then-extract for articles: trafilatura's default fetcher is blocked by
# many sites (Medium, Cloudflare-protected pages, etc). curl with a real user-agent
# is accepted by most. Trafilatura then handles the messy HTML → clean markdown step,
# which is what it's actually best at.

set -euo pipefail

# ---------- Configuration ----------

# The Python interpreter that has trafilatura installed.
# Adjust this path if your environment is different.
PYTHON_BIN="/opt/homebrew/bin/python3.12"

# ---------- Argument handling ----------

if [ $# -lt 1 ]; then
  cat <<EOF
Usage: $0 <url-or-path> [output-dir]

Inputs supported:
  - YouTube URL (https://www.youtube.com/watch?v=... or youtu.be/...)
  - Article/blog URL (any http/https URL pointing to readable content)
  - Local file path (.txt, .md, .vtt, .srt)

Default output dir: ./cache/

Requires: yt-dlp (for YouTube), curl + trafilatura (for articles).
Install with:
  brew install yt-dlp
  $PYTHON_BIN -m pip install trafilatura --break-system-packages
EOF
  exit 1
fi

INPUT="$1"
OUTPUT_DIR="${2:-./cache}"

# ---------- Helpers ----------

slugify() {
  echo "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g' \
    | sed -E 's/^-+|-+$//g' \
    | cut -c1-60
}

timestamp() { date +"%Y-%m-%d-%H%M%S"; }

require_tool() {
  if ! command -v "$1" &>/dev/null; then
    echo "ERROR: required tool '$1' not found." >&2
    echo "Install with: brew install $1" >&2
    exit 2
  fi
}

# ---------- Detect input type ----------

INPUT_TYPE=""

if [[ "$INPUT" =~ ^https?:// ]]; then
  if [[ "$INPUT" =~ (youtube\.com|youtu\.be) ]]; then
    INPUT_TYPE="youtube"
  else
    INPUT_TYPE="article"
  fi
elif [ -f "$INPUT" ]; then
  INPUT_TYPE="file"
else
  echo "ERROR: input not recognized as URL or existing file: $INPUT" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
TS=$(timestamp)

# ---------- YouTube path ----------

handle_youtube() {
  require_tool yt-dlp

  echo "→ Detected YouTube URL"
  echo "→ Fetching metadata..."

  local metadata_json
  metadata_json=$(yt-dlp --dump-json --no-warnings --skip-download "$INPUT" 2>/dev/null) || {
    echo "ERROR: yt-dlp failed to fetch metadata. Video may be private/removed/region-locked." >&2
    exit 3
  }

  local title uploader duration_seconds upload_date video_id
  title=$(echo "$metadata_json" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('title','unknown'))")
  uploader=$(echo "$metadata_json" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('uploader','unknown'))")
  duration_seconds=$(echo "$metadata_json" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('duration',0))")
  upload_date=$(echo "$metadata_json" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('upload_date','unknown'))")
  video_id=$(echo "$metadata_json" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('id','unknown'))")

  local duration_fmt
  if [ "$duration_seconds" -ge 3600 ]; then
    duration_fmt=$(printf "%d:%02d:%02d" $((duration_seconds/3600)) $((duration_seconds%3600/60)) $((duration_seconds%60)))
  else
    duration_fmt=$(printf "%d:%02d" $((duration_seconds/60)) $((duration_seconds%60)))
  fi

  local upload_date_fmt="unknown"
  if [ ${#upload_date} -eq 8 ]; then
    upload_date_fmt="${upload_date:0:4}-${upload_date:4:2}-${upload_date:6:2}"
  fi

  local slug
  slug=$(slugify "$uploader-$title")
  local outfile="$OUTPUT_DIR/transcript-$TS-$slug.md"

  echo "→ Title: $title"
  echo "→ Uploader: $uploader"
  echo "→ Duration: $duration_fmt"
  echo "→ Pulling captions..."

  local tmpdir
  tmpdir=$(mktemp -d)
  local cap_status="none"

  yt-dlp --write-subs --sub-langs "en.*,en-orig" --skip-download \
         --no-warnings --convert-subs vtt \
         -o "$tmpdir/%(id)s.%(ext)s" "$INPUT" >/dev/null 2>&1 || true

  # Check if a .vtt file actually appeared. yt-dlp returns 0 even when there
  # are no subs to download, so we must verify by file existence not exit code.
  if find "$tmpdir" -name "*.vtt" -type f | grep -q .; then
    cap_status="manual"
  fi

  if [ "$cap_status" = "none" ]; then
    yt-dlp --write-auto-subs --sub-langs "en.*,en-orig" --skip-download \
           --no-warnings --convert-subs vtt \
           -o "$tmpdir/%(id)s.%(ext)s" "$INPUT" >/dev/null 2>&1 || true
    if find "$tmpdir" -name "*.vtt" -type f | grep -q .; then
      cap_status="auto"
    fi
  fi

  local vtt_file
  vtt_file=$(find "$tmpdir" -name "*.vtt" | head -1)

  if [ -z "$vtt_file" ] || [ ! -f "$vtt_file" ]; then
    echo "WARNING: no captions available for this video." >&2
    echo "→ Producing metadata-only output (no transcript body)."
    cap_status="unavailable"
  fi

  {
    echo "---"
    echo "source-type: youtube"
    echo "url: $INPUT"
    echo "video-id: $video_id"
    echo "title: \"${title//\"/\\\"}\""
    echo "uploader: \"${uploader//\"/\\\"}\""
    echo "duration: $duration_fmt"
    echo "upload-date: $upload_date_fmt"
    echo "captions: $cap_status"
    echo "fetched: $(date +%Y-%m-%dT%H:%M:%S%z)"
    echo "---"
    echo ""
    echo "# $title"
    echo ""
    echo "**Channel:** $uploader  "
    echo "**Published:** $upload_date_fmt  "
    echo "**Duration:** $duration_fmt  "
    echo "**URL:** $INPUT"
    echo ""
    echo "---"
    echo ""

    if [ "$cap_status" = "unavailable" ]; then
      echo "## Note"
      echo ""
      echo "No captions were available for this video. Manual transcription or"
      echo "alternative source needed for content extraction."
    else
      echo "## Transcript ($cap_status captions)"
      echo ""
      grep -v -E '^WEBVTT|^Kind:|^Language:|^[0-9]{2}:[0-9]{2}:[0-9]{2}|^$|<[0-9:.]+>' "$vtt_file" \
        | sed -E 's/<[^>]+>//g' \
        | awk 'NF && $0 != prev { print; prev=$0 }'
    fi
  } > "$outfile"

  rm -rf "$tmpdir"

  echo "→ Wrote: $outfile"
  echo "→ Caption status: $cap_status"
  echo "$outfile"
}

# ---------- Article path ----------

handle_article() {
  require_tool curl

  if ! "$PYTHON_BIN" -c "import trafilatura" 2>/dev/null; then
    echo "ERROR: Python module 'trafilatura' not found in $PYTHON_BIN." >&2
    echo "Install with: $PYTHON_BIN -m pip install trafilatura --break-system-packages" >&2
    exit 2
  fi

  echo "→ Detected article URL"
  echo "→ Fetching with browser-like headers..."

  # Resolve script directory to find extract-article.py companion
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  local extractor="$script_dir/extract-article.py"

  if [ ! -f "$extractor" ]; then
    echo "ERROR: extract-article.py not found at $extractor" >&2
    echo "(It should sit next to transcript-pull.sh.)" >&2
    exit 5
  fi

  # Fetch HTML via curl with a real browser user-agent and accept headers.
  # Most anti-bot measures (Medium, Cloudflare basic, etc) accept this.
  local tmphtml
  tmphtml=$(mktemp -t article-XXXXXX.html)

  if ! curl -sSL --compressed \
       -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
       -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
       -H "Accept-Language: en-US,en;q=0.9" \
       -H "Accept-Encoding: gzip, deflate, br" \
       --max-time 30 \
       -o "$tmphtml" \
       "$INPUT"; then
    echo "ERROR: curl failed to fetch URL." >&2
    rm -f "$tmphtml"
    exit 4
  fi

  local html_size
  html_size=$(wc -c < "$tmphtml" | tr -d ' ')
  echo "→ Fetched ${html_size} bytes; extracting content..."

  if [ "$html_size" -lt 500 ]; then
    echo "WARNING: response is suspiciously small ($html_size bytes). Site may be blocking us." >&2
  fi

  local extracted
  extracted=$("$PYTHON_BIN" "$extractor" < "$tmphtml")

  if [ -z "$extracted" ]; then
    echo "ERROR: extraction returned empty. Site content may not be extractable." >&2
    rm -f "$tmphtml"
    exit 4
  fi

  local title author article_date body
  title=$(echo "$extracted" | sed -n 's/^TITLE:://p' | head -1)
  author=$(echo "$extracted" | sed -n 's/^AUTHOR:://p' | head -1)
  article_date=$(echo "$extracted" | sed -n 's/^DATE:://p' | head -1)
  body=$(echo "$extracted" | awk '/^BODY_START::$/{flag=1; next} flag')

  [ -z "$title" ] && title="untitled"
  [ -z "$author" ] && author="unknown"
  [ -z "$article_date" ] && article_date="unknown"

  local body_length
  body_length=$(echo "$body" | wc -c | tr -d ' ')

  if [ "$body_length" -lt 200 ]; then
    echo "WARNING: extracted body is very short ($body_length chars). Content may be paywalled or anti-scraped." >&2
  fi

  local slug
  slug=$(slugify "$author-$title")
  local outfile="$OUTPUT_DIR/transcript-$TS-$slug.md"

  echo "→ Title: $title"
  echo "→ Author: $author"

  {
    echo "---"
    echo "source-type: article"
    echo "url: $INPUT"
    echo "title: \"${title//\"/\\\"}\""
    echo "author: \"${author//\"/\\\"}\""
    echo "article-date: $article_date"
    echo "fetched: $(date +%Y-%m-%dT%H:%M:%S%z)"
    echo "---"
    echo ""
    echo "# $title"
    echo ""
    echo "**Author:** $author  "
    echo "**Published:** $article_date  "
    echo "**URL:** $INPUT"
    echo ""
    echo "---"
    echo ""
    echo "$body"
  } > "$outfile"

  rm -f "$tmphtml"

  echo "→ Wrote: $outfile"
  echo "$outfile"
}

# ---------- Local file path ----------

handle_file() {
  echo "→ Detected local file"

  local title
  title=$(basename "$INPUT" | sed -E 's/\.[^.]+$//')
  local slug
  slug=$(slugify "$title")
  local outfile="$OUTPUT_DIR/transcript-$TS-$slug.md"

  local ext="${INPUT##*.}"
  local body=""

  case "$ext" in
    txt|md)
      body=$(cat "$INPUT")
      ;;
    vtt|srt)
      body=$(grep -v -E '^WEBVTT|^Kind:|^Language:|^[0-9]+$|^[0-9]{2}:[0-9]{2}:[0-9]{2}|^$|<[0-9:.]+>' "$INPUT" \
             | sed -E 's/<[^>]+>//g' \
             | awk 'NF && $0 != prev { print; prev=$0 }')
      ;;
    *)
      echo "WARNING: unrecognized extension '$ext'; treating as plain text." >&2
      body=$(cat "$INPUT")
      ;;
  esac

  {
    echo "---"
    echo "source-type: local-file"
    echo "source-path: $INPUT"
    echo "title: \"$title\""
    echo "fetched: $(date +%Y-%m-%dT%H:%M:%S%z)"
    echo "---"
    echo ""
    echo "# $title"
    echo ""
    echo "**Source file:** \`$INPUT\`"
    echo ""
    echo "---"
    echo ""
    echo "$body"
  } > "$outfile"

  echo "→ Wrote: $outfile"
  echo "$outfile"
}

# ---------- Dispatch ----------

case "$INPUT_TYPE" in
  youtube)  handle_youtube ;;
  article)  handle_article ;;
  file)     handle_file ;;
esac
