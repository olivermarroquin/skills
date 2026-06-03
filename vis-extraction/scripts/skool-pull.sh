#!/usr/bin/env bash
# skool-pull.sh — download a Skool NATIVE-hosted video from a signed HLS (.m3u8) URL.
#
# STATUS: v0.1 — standalone test harness. NOT yet wired into the VIS skill.
#         Run this on your Mac (host), where yt-dlp + ffmpeg are installed.
#         The Cowork sandbox cannot run this (no yt-dlp, and YouTube/Skool CDNs
#         block cloud IPs). This is the host-side companion for testing what's
#         possible before we formalize the Skool branch (see Handoff A).
#
# WHY THIS EXISTS:
#   Skool serves native video over HLS (.m3u8) behind SHORT-LIVED SIGNED TOKENS.
#   yt-dlp has NO site-specific Skool extractor, so it cannot go from a Skool
#   lesson page URL to the stream on its own. You must hand it the real .m3u8 URL.
#
# HOW TO GET THE .m3u8 URL (manual, ~20 seconds):
#   1. Open the Skool lesson in Chrome while logged in.
#   2. Open DevTools (Cmd+Opt+I) -> Network tab -> filter box: type  m3u8
#   3. Press play on the video. A request to stream.video.skool.com/...m3u8?token=...
#      appears. Right-click it -> Copy -> Copy link address.
#   4. Paste that as the first argument here (in quotes — it's very long).
#
#   The token EXPIRES (minutes to hours). If you get HTTP 403, grab a fresh URL.
#
# USAGE:
#   ./skool-pull.sh "<m3u8-url-with-token>" [output-dir] [output-name]
#
# EXAMPLES:
#   ./skool-pull.sh "https://stream.video.skool.com/abc...m3u8?token=eyJ..."
#   ./skool-pull.sh "https://stream.video.skool.com/abc...m3u8?token=eyJ..." ~/Desktop "lesson-01-intro"
#
# OUTPUT:
#   An .mp4 in the output dir (default ./skool-downloads/), faststart-remuxed.
#
# NEXT STEP FOR VIS:
#   This script gives you the VIDEO file. To get it into the vault you still need
#   TEXT. Options:
#     - If captions exist, this script tries to grab + embed them (--subs).
#     - Otherwise transcribe locally:  whisper "<file>.mp4" --model small --output_format txt
#       then feed the .txt to VIS as a local-file input.
#
# REQUIRES (host): yt-dlp, ffmpeg.  Optional: aria2c (faster fragment download).
#   brew install yt-dlp ffmpeg aria2

set -euo pipefail

# ---------- args ----------
if [ $# -lt 1 ]; then
  sed -n '2,40p' "$0"   # print the header help
  exit 1
fi

M3U8_URL="$1"
OUTPUT_DIR="${2:-./skool-downloads}"
OUTPUT_NAME="${3:-}"          # optional; if empty we use the video's own title
WANT_SUBS="${SKOOL_SUBS:-0}"  # set SKOOL_SUBS=1 to attempt caption download

# ---------- sanity checks ----------
if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "ERROR: yt-dlp not found. Install: brew install yt-dlp" >&2; exit 2
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ERROR: ffmpeg not found. Install: brew install ffmpeg" >&2; exit 2
fi
if [[ "$M3U8_URL" != *m3u8* ]]; then
  echo "WARNING: that URL doesn't contain 'm3u8'. Skool may have switched this" >&2
  echo "         community to fragmented webm segments — see Handoff A, 'known drift'." >&2
fi

mkdir -p "$OUTPUT_DIR"

# Decide output template. A short -o name avoids the macOS 'File name too long'
# error caused by yt-dlp trying to name the file after the giant token string.
if [ -n "$OUTPUT_NAME" ]; then
  OUT_TEMPLATE="$OUTPUT_DIR/${OUTPUT_NAME}.%(ext)s"
else
  OUT_TEMPLATE="$OUTPUT_DIR/%(title).180B.%(ext)s"
fi

# Common flags. Skool's CDN requires a skool.com referer + origin.
COMMON_FLAGS=(
  -N 16                                  # 16 parallel fragment downloads
  -f best
  --hls-prefer-native
  --referer "https://www.skool.com"
  --add-header "Origin: https://www.skool.com"
  --add-header "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  --remux-video mp4
  --merge-output-format mp4
  --postprocessor-args "ffmpeg:-movflags +faststart"
  -o "$OUT_TEMPLATE"
)

if [ "$WANT_SUBS" = "1" ]; then
  COMMON_FLAGS+=( --write-subs --embed-subs --sub-langs "en.*" )
fi

echo "==> Downloading Skool native video"
echo "    out dir : $OUTPUT_DIR"
echo "    name    : ${OUTPUT_NAME:-<from video title>}"
echo "    subs    : $([ "$WANT_SUBS" = 1 ] && echo on || echo off  '(set SKOOL_SUBS=1 to enable)')"
echo

# ---------- attempt 1: native HLS downloader ----------
if yt-dlp "${COMMON_FLAGS[@]}" "$M3U8_URL"; then
  echo "==> Done (native HLS)."
  exit 0
fi

echo "==> Native downloader failed; retrying with extra retries..." >&2
if yt-dlp "${COMMON_FLAGS[@]}" --retries 20 --fragment-retries 100 "$M3U8_URL"; then
  echo "==> Done (with retries)."
  exit 0
fi

# ---------- attempt 2: aria2c fallback (if available) ----------
if command -v aria2c >/dev/null 2>&1; then
  echo "==> Retrying via aria2c external downloader..." >&2
  if yt-dlp \
      -f best \
      --downloader aria2c \
      --downloader-args "aria2c:-x 16 -s 16 -k 1M --max-tries=0 --retry-wait=5" \
      --referer "https://www.skool.com" \
      --add-header "Origin: https://www.skool.com" \
      --add-header "User-Agent: Mozilla/5.0" \
      --remux-video mp4 --merge-output-format mp4 \
      --postprocessor-args "ffmpeg:-movflags +faststart" \
      -o "${OUTPUT_DIR}/${OUTPUT_NAME:-skool_video}.mp4" \
      "$M3U8_URL"; then
    echo "==> Done (aria2c)."
    exit 0
  fi
fi

echo >&2
echo "ERROR: all download attempts failed." >&2
echo "Most likely causes:" >&2
echo "  - Token expired (HTTP 403). Grab a FRESH .m3u8 URL from DevTools and rerun." >&2
echo "  - Skool switched this community to fragmented webm (no single m3u8)." >&2
echo "    In that case use the browser-extension fallback noted in Handoff A." >&2
exit 4
