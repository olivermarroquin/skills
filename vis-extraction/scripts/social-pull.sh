#!/usr/bin/env bash
# social-pull.sh — download + transcribe short-form social video (FB/IG/TikTok reels)
#
# Usage:
#   ./social-pull.sh <reel-url> [output-dir] [--cookies <cookie-file>] [--model <whisper-model>]
#
# Examples:
#   ./social-pull.sh https://www.facebook.com/reel/123456789
#   ./social-pull.sh https://www.instagram.com/reel/ABC123/
#   ./social-pull.sh https://www.tiktok.com/@user/video/123456789
#   ./social-pull.sh https://www.facebook.com/reel/123 ./cache --cookies ~/cookies-fb.txt
#   ./social-pull.sh https://www.facebook.com/reel/123 ./cache --model medium
#
# Output: a markdown file in the cache dir (default: ./cache/) with format:
#   transcript-YYYY-MM-DD-HHMMSS-<slug>.md
#
# Architecture:
#   1. yt-dlp downloads the video (or just audio where supported)
#   2. ffmpeg extracts audio as WAV (16kHz mono — Whisper's preferred input)
#   3. Whisper transcribes locally (model: base by default, configurable)
#   4. Output formatted as the same markdown transcript shape transcript-pull.sh produces
#
# Cookie handling:
#   - Facebook: many reels are public but some require auth. Export cookies via
#     browser extension (e.g., "Get cookies.txt LOCALLY") to a Netscape-format file.
#     Pass with --cookies <path>. If yt-dlp fails without cookies, the script will
#     suggest the flag.
#   - Instagram: almost always requires cookies for yt-dlp. Same export method.
#   - TikTok: usually public. Cookies only needed for age-gated/region-locked content.
#
# Requirements: yt-dlp, ffmpeg, Python 3.12 with openai-whisper

set -euo pipefail

# ---------- Configuration ----------

PYTHON_BIN="/opt/homebrew/bin/python3.12"
WHISPER_MODEL="base"
COOKIE_FILE=""

# ---------- Argument handling ----------

show_usage() {
  cat <<EOF
Usage: $0 <reel-url> [output-dir] [--cookies <cookie-file>] [--model <whisper-model>]

Platforms supported:
  - Facebook Reels (https://www.facebook.com/reel/... or /watch/...)
  - Instagram Reels (https://www.instagram.com/reel/...)
  - TikTok (https://www.tiktok.com/@user/video/...)
  - YouTube Shorts (https://www.youtube.com/shorts/...)

Options:
  --cookies <file>   Netscape-format cookie file for authenticated downloads
  --model <name>     Whisper model: tiny, base (default), small, medium, large

Default output dir: ./cache/

Requires: yt-dlp, ffmpeg, python3.12 with openai-whisper
EOF
  exit 1
}

if [ $# -lt 1 ]; then
  show_usage
fi

INPUT="$1"
shift

OUTPUT_DIR="./cache"

# Parse remaining args
while [ $# -gt 0 ]; do
  case "$1" in
    --cookies)
      COOKIE_FILE="$2"
      shift 2
      ;;
    --model)
      WHISPER_MODEL="$2"
      shift 2
      ;;
    -h|--help)
      show_usage
      ;;
    *)
      # First non-flag arg after URL is output dir
      if [ -z "${OUTPUT_DIR_SET:-}" ]; then
        OUTPUT_DIR="$1"
        OUTPUT_DIR_SET=1
      fi
      shift
      ;;
  esac
done

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

cleanup() {
  [ -n "${TMPDIR_WORK:-}" ] && rm -rf "$TMPDIR_WORK"
}
trap cleanup EXIT

# ---------- Preflight ----------

require_tool yt-dlp
require_tool ffmpeg

if ! "$PYTHON_BIN" -c "import whisper" 2>/dev/null; then
  echo "ERROR: openai-whisper not installed in $PYTHON_BIN." >&2
  echo "Install with: $PYTHON_BIN -m pip install openai-whisper --break-system-packages" >&2
  exit 2
fi

# ---------- Detect platform ----------

PLATFORM=""
if [[ "$INPUT" =~ facebook\.com|fb\.watch ]]; then
  PLATFORM="facebook"
elif [[ "$INPUT" =~ instagram\.com ]]; then
  PLATFORM="instagram"
elif [[ "$INPUT" =~ tiktok\.com ]]; then
  PLATFORM="tiktok"
elif [[ "$INPUT" =~ youtube\.com/shorts|youtu\.be ]]; then
  PLATFORM="youtube-shorts"
else
  echo "WARNING: URL pattern not recognized as a known social platform. Attempting download anyway." >&2
  PLATFORM="unknown"
fi

echo "→ Platform: $PLATFORM"
echo "→ URL: $INPUT"
echo "→ Whisper model: $WHISPER_MODEL"

mkdir -p "$OUTPUT_DIR"
TMPDIR_WORK=$(mktemp -d)
TS=$(timestamp)

# ---------- Step 1: Download video ----------

echo "→ Downloading video..."

YT_DLP_ARGS=(
  --no-warnings
  --no-playlist
  -f "bestaudio/best"
  -o "$TMPDIR_WORK/video.%(ext)s"
)

if [ -n "$COOKIE_FILE" ]; then
  if [ ! -f "$COOKIE_FILE" ]; then
    echo "ERROR: cookie file not found: $COOKIE_FILE" >&2
    exit 3
  fi
  YT_DLP_ARGS+=(--cookies "$COOKIE_FILE")
  echo "→ Using cookies from: $COOKIE_FILE"
fi

# Attempt download
if ! yt-dlp "${YT_DLP_ARGS[@]}" "$INPUT" 2>"$TMPDIR_WORK/ytdlp-err.log"; then
  echo "ERROR: yt-dlp download failed." >&2
  cat "$TMPDIR_WORK/ytdlp-err.log" >&2
  if [ -z "$COOKIE_FILE" ] && [[ "$PLATFORM" =~ facebook|instagram ]]; then
    echo "" >&2
    echo "HINT: This $PLATFORM content may require authentication." >&2
    echo "Export your browser cookies to a Netscape-format file and retry with:" >&2
    echo "  $0 '$INPUT' '$OUTPUT_DIR' --cookies ~/cookies-${PLATFORM}.txt" >&2
  fi
  exit 3
fi

# Find the downloaded file
DOWNLOADED=$(find "$TMPDIR_WORK" -name "video.*" -type f | head -1)
if [ -z "$DOWNLOADED" ] || [ ! -f "$DOWNLOADED" ]; then
  echo "ERROR: download succeeded but no output file found." >&2
  exit 3
fi

echo "→ Downloaded: $(basename "$DOWNLOADED") ($(du -h "$DOWNLOADED" | cut -f1))"

# ---------- Step 2: Extract metadata via yt-dlp ----------

echo "→ Fetching metadata..."

METADATA_JSON=$(yt-dlp --dump-json --no-warnings --skip-download \
  ${COOKIE_FILE:+--cookies "$COOKIE_FILE"} \
  "$INPUT" 2>/dev/null) || METADATA_JSON="{}"

TITLE=$( echo "$METADATA_JSON" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('title','untitled'))" 2>/dev/null || echo "untitled")
UPLOADER=$(echo "$METADATA_JSON" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('uploader','unknown') or d.get('channel','unknown'))" 2>/dev/null || echo "unknown")
DURATION=$(echo "$METADATA_JSON" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('duration',0))" 2>/dev/null || echo "0")
UPLOAD_DATE=$(echo "$METADATA_JSON" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('upload_date','unknown'))" 2>/dev/null || echo "unknown")
VIDEO_ID=$(echo "$METADATA_JSON" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print(d.get('id','unknown'))" 2>/dev/null || echo "unknown")
DESCRIPTION=$(echo "$METADATA_JSON" | "$PYTHON_BIN" -c "import sys,json;d=json.load(sys.stdin);print((d.get('description','') or '')[:500])" 2>/dev/null || echo "")

# Format duration
if [ "$DURATION" -ge 3600 ] 2>/dev/null; then
  DURATION_FMT=$(printf "%d:%02d:%02d" $((DURATION/3600)) $((DURATION%3600/60)) $((DURATION%60)))
elif [ "$DURATION" -gt 0 ] 2>/dev/null; then
  DURATION_FMT=$(printf "%d:%02d" $((DURATION/60)) $((DURATION%60)))
else
  DURATION_FMT="unknown"
fi

# Format upload date
UPLOAD_DATE_FMT="unknown"
if [ ${#UPLOAD_DATE} -eq 8 ] 2>/dev/null; then
  UPLOAD_DATE_FMT="${UPLOAD_DATE:0:4}-${UPLOAD_DATE:4:2}-${UPLOAD_DATE:6:2}"
fi

echo "→ Title: $TITLE"
echo "→ Creator: $UPLOADER"
echo "→ Duration: $DURATION_FMT"

# ---------- Step 3: Extract audio ----------

echo "→ Extracting audio (16kHz mono WAV)..."

AUDIO_WAV="$TMPDIR_WORK/audio.wav"
if ! ffmpeg -i "$DOWNLOADED" -ar 16000 -ac 1 -f wav "$AUDIO_WAV" -y -loglevel error 2>&1; then
  echo "ERROR: ffmpeg audio extraction failed." >&2
  exit 4
fi

AUDIO_DURATION=$(ffmpeg -i "$AUDIO_WAV" 2>&1 | grep Duration | sed -E 's/.*Duration: ([0-9:.]+).*/\1/' || echo "unknown")
echo "→ Audio extracted: $AUDIO_DURATION"

# ---------- Step 4: Whisper transcription ----------

echo "→ Transcribing with Whisper ($WHISPER_MODEL model)..."

TRANSCRIPT_TXT="$TMPDIR_WORK/transcript.txt"

"$PYTHON_BIN" -c "
import whisper
import sys

model = whisper.load_model('$WHISPER_MODEL')
result = model.transcribe('$AUDIO_WAV', language='en', fp16=False)

with open('$TRANSCRIPT_TXT', 'w') as f:
    f.write(result['text'].strip())

# Also write segments for potential timestamp use
with open('$TMPDIR_WORK/segments.txt', 'w') as f:
    for seg in result['segments']:
        start = seg['start']
        end = seg['end']
        text = seg['text'].strip()
        f.write(f'[{start:.1f}s - {end:.1f}s] {text}\n')

print(f'Transcription complete: {len(result[\"text\"].split())} words, {len(result[\"segments\"])} segments')
" 2>&1

if [ ! -f "$TRANSCRIPT_TXT" ] || [ ! -s "$TRANSCRIPT_TXT" ]; then
  echo "ERROR: Whisper transcription produced no output." >&2
  exit 5
fi

TRANSCRIPT=$(cat "$TRANSCRIPT_TXT")
WORD_COUNT=$(echo "$TRANSCRIPT" | wc -w | tr -d ' ')
echo "→ Transcript: $WORD_COUNT words"

# ---------- Step 5: Write output ----------

SLUG=$(slugify "$UPLOADER-$TITLE")
OUTFILE="$OUTPUT_DIR/transcript-$TS-$SLUG.md"

{
  echo "---"
  echo "source-type: social-reel"
  echo "platform: $PLATFORM"
  echo "url: $INPUT"
  echo "video-id: $VIDEO_ID"
  echo "title: \"${TITLE//\"/\\\"}\""
  echo "uploader: \"${UPLOADER//\"/\\\"}\""
  echo "duration: $DURATION_FMT"
  echo "upload-date: $UPLOAD_DATE_FMT"
  echo "transcription: whisper-$WHISPER_MODEL"
  echo "word-count: $WORD_COUNT"
  echo "fetched: $(date +%Y-%m-%dT%H:%M:%S%z)"
  echo "---"
  echo ""
  echo "# $TITLE"
  echo ""
  echo "**Creator:** $UPLOADER  "
  echo "**Platform:** $PLATFORM  "
  echo "**Published:** $UPLOAD_DATE_FMT  "
  echo "**Duration:** $DURATION_FMT  "
  echo "**URL:** $INPUT"
  echo ""
  if [ -n "$DESCRIPTION" ]; then
    echo "**Description:** $DESCRIPTION"
    echo ""
  fi
  echo "---"
  echo ""
  echo "## Transcript (Whisper $WHISPER_MODEL)"
  echo ""
  echo "$TRANSCRIPT"
  echo ""
  echo "---"
  echo ""
  echo "## Timestamped Segments"
  echo ""
  cat "$TMPDIR_WORK/segments.txt"
} > "$OUTFILE"

echo ""
echo "→ Wrote: $OUTFILE"
echo "→ Platform: $PLATFORM | Duration: $DURATION_FMT | Words: $WORD_COUNT"
echo "→ Ready for VIS extraction (Phases 1-7 run unchanged on this transcript)"
echo "$OUTFILE"
