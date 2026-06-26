#!/usr/bin/env python3
"""
Hermes Vault Bridge — Level 1 (Read + Surface + Write-Back to Outbox)

Wave 2: Reads the vault's spawn-queue and active-chats tracker, cross-references
to find ready-but-not-in-flight rows, and outputs a formatted Telegram
surface message.

Wave 3: Writes claim ledger, status digest, event-log entries, and action log
to the Hermes outbox (operator-reviewed merge). Telegram alerts for write-back.

Hard-coded read allowlist (D-B):
  1. _meta/handoffs/_spawn-queue.md
  2. _meta/handoffs/_active-chats-tracker.md
  3. Referenced handoff files (from spawn-queue rows)
  4. _meta/_event-log.md (last ~50 rows)

Write-back boundary (D-C / Level 1):
  - Writes ONLY to the outbox directory (hermes-outbox/)
  - NEVER writes to the live vault clone
  - NEVER does git push
  - Outbox = air-gap; operator reviews + merges

AC-5:  Every file read is logged to the action log file.
AC-6:  Freshness gate — checks git recency; sandbox uses FETCH_HEAD mtime.
AC-7:  Outbox populated with correct structure (claim ledger, status, event log, action log).
AC-8:  Claim ledger prevents duplicate surfaces (idempotent SHA-256 hashing).
AC-9:  Attribution markers on all Hermes-authored content.
AC-10: Action log records every operation (sync, read, surface, write-back).
AC-15: Level 1 only — no autonomous claiming or action on rows.

Environment variables:
  VAULT_BRIDGE_BASE  — vault clone path (auto-detected)
  VAULT_BRIDGE_MODE  — "sandbox" (default) or "host"
  VAULT_BRIDGE_OUTBOX — outbox path (auto-detected)
"""

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --- Constants ---

_CONTAINER_VAULT = Path("/workspace/vault-second-brain")
_HOST_VAULT = Path("/home/hermes/hermes-data/vault/second-brain")

_CONTAINER_OUTBOX = Path("/workspace/hermes-outbox")
_HOST_OUTBOX = Path("/home/hermes/hermes-data/hermes-outbox")


def _detect_vault_base() -> tuple[Path, str]:
    """Auto-detect vault path and bridge mode.

    Resolution order:
      1. VAULT_BRIDGE_BASE env var (explicit override)
      2. /workspace/vault-second-brain (container/sandbox — read-only mount)
      3. /home/hermes/hermes-data/vault/second-brain (host — has deploy key)

    Mode is tied to detection unless VAULT_BRIDGE_MODE is explicitly set:
      - Container path -> sandbox (no git pull)
      - Host path -> host (git pull on stale)
    """
    explicit_base = os.environ.get("VAULT_BRIDGE_BASE")
    explicit_mode = os.environ.get("VAULT_BRIDGE_MODE")

    if explicit_base:
        base = Path(explicit_base)
        mode = explicit_mode or ("sandbox" if base == _CONTAINER_VAULT else "host")
        return base, mode

    if _CONTAINER_VAULT.is_dir():
        return _CONTAINER_VAULT, explicit_mode or "sandbox"

    if _HOST_VAULT.is_dir():
        return _HOST_VAULT, explicit_mode or "host"

    # Neither found — default to container path (will fail with clear error)
    return _CONTAINER_VAULT, explicit_mode or "sandbox"


def _detect_outbox_path() -> Path:
    """Auto-detect outbox path.

    Resolution order:
      1. VAULT_BRIDGE_OUTBOX env var (explicit override)
      2. /workspace/hermes-outbox (container — writable mount)
      3. /home/hermes/hermes-data/hermes-outbox (host)
    """
    explicit = os.environ.get("VAULT_BRIDGE_OUTBOX")
    if explicit:
        return Path(explicit)

    if _CONTAINER_OUTBOX.is_dir():
        return _CONTAINER_OUTBOX

    if _HOST_OUTBOX.is_dir():
        return _HOST_OUTBOX

    # Default to container path (will fail with clear error on write)
    return _CONTAINER_OUTBOX


VAULT_BASE, BRIDGE_MODE = _detect_vault_base()
VAULT_BASE_RESOLVED = VAULT_BASE.resolve()
OUTBOX_BASE = _detect_outbox_path()
STALENESS_THRESHOLD_MINUTES = 15  # host mode: commit-age threshold for pull
SYNC_STALENESS_THRESHOLD_MINUTES = 420  # sandbox mode: 7h (6h cron + 1h buffer)

# Action log goes to a file (not stderr) so Hermes's terminal tool returns
# ONLY stdout (the Telegram message) to the model. AC-5 compliance preserved.
ACTION_LOG_PATH = Path(os.environ.get(
    "VAULT_BRIDGE_LOG",
    "/tmp/hermes-vault-bridge.log",
))

# Session / chat ID for attribution
BRIDGE_CHAT_ID = os.environ.get("VAULT_BRIDGE_CHAT_ID", "hermes-bridge-auto")

# D-B allowlist — only these paths (relative to VAULT_BASE) may be read
ALLOWLIST_PREFIXES = [
    "_meta/handoffs/_spawn-queue.md",
    "_meta/handoffs/_active-chats-tracker.md",
    "_meta/handoffs/",  # for referenced handoff files
    "_meta/_event-log.md",
]

# In-memory action log entries (flushed at end)
action_log: list[dict] = []


# --- Action Logging (D-N) ---

def log_action(action: str, target: str, result: str = "ok"):
    """Log an operation to the in-memory action log.

    Format per D-N: {"ts", "action", "target", "result", "chat_id"}
    """
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "target": target,
        "result": result,
        "chat_id": BRIDGE_CHAT_ID,
    }
    action_log.append(entry)


def flush_action_log():
    """Write the action log to ACTION_LOG_PATH and both D-N destinations.

    1. /tmp log file (operator debugging — always attempted)
    2. Outbox mirror: hermes-outbox/_hermes-bridge-actions.jsonl (append)
    3. Box-side primary: hermes-outbox/_hermes-bridge-actions.jsonl IS the
       primary when mounted (operator can symlink from expected host path)

    Keeps stdout clean for the Telegram message.
    """
    # Write to /tmp debug log (overwrite per run)
    try:
        with open(ACTION_LOG_PATH, "w", encoding="utf-8") as f:
            for entry in action_log:
                f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    # Append to outbox action log (persistent, append-only — D-N)
    outbox_action_log = OUTBOX_BASE / "_hermes-bridge-actions.jsonl"
    try:
        with open(outbox_action_log, "a", encoding="utf-8") as f:
            for entry in action_log:
                f.write(json.dumps(entry) + "\n")
    except OSError:
        # Outbox not writable — log but don't crash (surface message is primary)
        pass


def log_read(filepath: str):
    """Log a file read (AC-5 compliance)."""
    log_action("read", filepath)


def log_skip(filepath: str, reason: str):
    """Log a skipped read attempt."""
    log_action("read-blocked", filepath, result=reason)


# --- Read Allowlist (D-B) ---

def is_allowlisted(rel_path: str) -> bool:
    """Check if a relative path falls within the D-B read allowlist."""
    for prefix in ALLOWLIST_PREFIXES:
        if prefix.endswith("/"):
            if rel_path.startswith(prefix):
                return True
        else:
            if rel_path == prefix:
                return True
    return False


def safe_read(rel_path: str) -> str | None:
    """Read a file only if it's within the D-B allowlist.

    Returns file content or None if blocked/missing.
    """
    normalized = os.path.normpath(rel_path)
    if ".." in Path(normalized).parts:
        log_skip(rel_path, "path traversal rejected")
        return None
    rel_path = normalized

    if not is_allowlisted(rel_path):
        log_skip(rel_path, "outside D-B allowlist")
        return None

    full_path = VAULT_BASE / rel_path
    try:
        resolved = full_path.resolve()
        if not str(resolved).startswith(str(VAULT_BASE_RESOLVED)):
            log_skip(rel_path, "symlink escape outside vault base")
            return None
    except OSError:
        log_skip(rel_path, "path resolution failed")
        return None

    if not full_path.is_file():
        log_skip(rel_path, "file not found")
        return None

    log_read(rel_path)
    return full_path.read_text(encoding="utf-8")


# --- Freshness Gate (D-L) ---

def check_freshness() -> bool:
    """Check vault freshness. Return False if data is too stale to read.

    Sandbox mode: checks .git/FETCH_HEAD mtime (updated by every fetch/pull,
    even with no new commits). Threshold: 7h (6h cron + 1h buffer).
    Host mode: checks commit age, pulls if stale.
    """
    log_action("freshness-check", f"starting (mode={BRIDGE_MODE})")

    if BRIDGE_MODE == "sandbox":
        return _check_freshness_sandbox()
    else:
        return _check_freshness_host()


def _check_freshness_sandbox() -> bool:
    """Sandbox mode: check sync recency via .git/FETCH_HEAD mtime."""
    try:
        fetch_head = VAULT_BASE / ".git" / "FETCH_HEAD"
        if not fetch_head.is_file():
            fallback = VAULT_BASE / ".git" / "HEAD"
            if not fallback.is_file():
                log_action(
                    "freshness-check",
                    "no .git/FETCH_HEAD or .git/HEAD — vault clone missing?",
                    result="error",
                )
                return False
            target = fallback
            signal_name = ".git/HEAD mtime (fallback)"
        else:
            target = fetch_head
            signal_name = ".git/FETCH_HEAD mtime"

        mtime = datetime.fromtimestamp(target.stat().st_mtime, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        age_minutes = (now - mtime).total_seconds() / 60

        log_action(
            "freshness-check",
            f"{signal_name}: {mtime.isoformat()}, age {age_minutes:.0f}min "
            f"(threshold {SYNC_STALENESS_THRESHOLD_MINUTES}min)",
        )

        if age_minutes <= SYNC_STALENESS_THRESHOLD_MINUTES:
            log_action("freshness-check", "fresh (sandbox)", result="ok")
            return True

        log_action(
            "freshness-check",
            f"stale ({age_minutes:.0f}min > {SYNC_STALENESS_THRESHOLD_MINUTES}min) "
            f"— sandbox mode, host cron may have missed",
            result="stale",
        )
        return False

    except Exception as e:
        log_action("freshness-check", f"sandbox check failed: {e}", result="error")
        return False


def _check_freshness_host() -> bool:
    """Host mode: check commit age, pull if stale."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci"],
            cwd=VAULT_BASE,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            log_action("freshness-check", "git log failed", result="error")
            return False

        last_commit_str = result.stdout.strip()
        if not last_commit_str:
            log_action("freshness-check", "empty git log output", result="error")
            return False

        last_commit_dt = _parse_git_date(last_commit_str)
        now = datetime.now(timezone.utc)
        age_minutes = (now - last_commit_dt).total_seconds() / 60

        log_action(
            "freshness-check",
            f"last commit {last_commit_str}, age {age_minutes:.1f}min",
        )

        if age_minutes <= STALENESS_THRESHOLD_MINUTES:
            log_action("freshness-check", "fresh (host)", result="ok")
            return True

        log_action("freshness-pull", "vault stale, pulling")
        pull_result = subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=VAULT_BASE,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if pull_result.returncode != 0:
            log_action(
                "freshness-pull",
                f"pull failed: {pull_result.stderr.strip()}",
                result="error",
            )
            return False

        log_action("freshness-pull", "pull succeeded", result="ok")
        return True

    except subprocess.TimeoutExpired:
        log_action("freshness-check", "timeout", result="error")
        return False
    except Exception as e:
        log_action("freshness-check", f"host check failed: {e}", result="error")
        return False


def _parse_git_date(date_str: str) -> datetime:
    """Parse git's default date format: '2026-06-22 19:31:00 -0400'."""
    parts = date_str.rsplit(" ", 1)
    if len(parts) == 2:
        dt_part, tz_part = parts
        dt = datetime.strptime(dt_part, "%Y-%m-%d %H:%M:%S")
        tz_sign = 1 if tz_part[0] == "+" else -1
        tz_hours = int(tz_part[1:3])
        tz_mins = int(tz_part[3:5])
        tz_offset = timedelta(hours=tz_hours, minutes=tz_mins) * tz_sign
        dt = dt.replace(tzinfo=timezone(tz_offset))
        return dt.astimezone(timezone.utc)
    dt = datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S")
    return dt.replace(tzinfo=timezone.utc)


# --- Claim Ledger (D-L) ---

def _row_id(handoff_file: str, chat_name: str) -> str:
    """Compute a deterministic row ID from handoff file + chat name.

    SHA-256 of the concatenation ensures idempotency (AC-8).
    """
    payload = f"{handoff_file}::{chat_name}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def load_claim_ledger() -> set[str]:
    """Load existing row IDs from the claim ledger (idempotency check)."""
    ledger_path = OUTBOX_BASE / "_meta" / "handoffs" / "_hermes-claimed.jsonl"
    claimed: set[str] = set()
    try:
        if ledger_path.is_file():
            for line in ledger_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    claimed.add(entry.get("row_id", ""))
                except json.JSONDecodeError:
                    continue
    except OSError:
        log_action("claim-ledger", "could not read claim ledger", result="warning")
    return claimed


def append_claim(row_id: str, summary: str):
    """Append a surfaced-row entry to the claim ledger."""
    ledger_path = OUTBOX_BASE / "_meta" / "handoffs" / "_hermes-claimed.jsonl"
    entry = {
        "row_id": row_id,
        "action": "surfaced",
        "ts": datetime.now(timezone.utc).isoformat(),
        "chat_id": BRIDGE_CHAT_ID,
        "summary": summary,
    }
    try:
        with open(ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        log_action("write-back", f"claim ledger: {row_id}", result="ok")
    except OSError as e:
        log_action("write-back", f"claim ledger write failed: {e}", result="error")


# --- Status Digest (D-M) ---

def write_status_digest(
    surfaced_count: int,
    skipped_count: int,
    active_count: int,
    sync_status: str,
):
    """Write a status digest to the outbox (D-M).

    Every line has attribution: | by: hermes | chat-id: <id> | ts: <ISO> |
    """
    ts = datetime.now(timezone.utc).isoformat()
    attr = f"| by: hermes | chat-id: {BRIDGE_CHAT_ID} | ts: {ts} |"

    digest_path = OUTBOX_BASE / "_meta" / "handoffs" / "_hermes-status.md"
    content = (
        f"# Hermes Bridge Status Digest {attr}\n"
        f"\n"
        f"**Timestamp:** {ts} {attr}\n"
        f"**Sync status:** {sync_status} {attr}\n"
        f"**Rows surfaced this run:** {surfaced_count} {attr}\n"
        f"**Rows skipped (already claimed):** {skipped_count} {attr}\n"
        f"**Active chats in tracker:** {active_count} {attr}\n"
    )
    try:
        with open(digest_path, "w", encoding="utf-8") as f:
            f.write(content)
        log_action("write-back", "status digest written", result="ok")
    except OSError as e:
        log_action("write-back", f"status digest write failed: {e}", result="error")


# --- Event Log Entries (D-M) ---

def append_event_log_entry(event_type: str, description: str):
    """Append an event to the Hermes event log in the outbox.

    Format mirrors the vault _event-log.md shape (D-M).
    Attribution on every line (AC-9).
    """
    ts = datetime.now(timezone.utc).isoformat()
    event_log_path = OUTBOX_BASE / "_meta" / "_event-log-hermes.md"

    # Initialize with header if file is empty/new
    header = ""
    try:
        if not event_log_path.is_file() or event_log_path.stat().st_size == 0:
            header = (
                "# Hermes Bridge Event Log\n\n"
                "| Timestamp | Files touched | Event type | Chat ID | Description |\n"
                "|---|---|---|---|---|\n"
            )
    except OSError:
        header = (
            "# Hermes Bridge Event Log\n\n"
            "| Timestamp | Files touched | Event type | Chat ID | Description |\n"
            "|---|---|---|---|---|\n"
        )

    row = (
        f"| {ts} | outbox: claim+status+event | {event_type} "
        f"| {BRIDGE_CHAT_ID} | {description} "
        f"(by: hermes, chat-id: {BRIDGE_CHAT_ID}, ts: {ts}) |\n"
    )

    try:
        with open(event_log_path, "a", encoding="utf-8") as f:
            if header:
                f.write(header)
            f.write(row)
        log_action("write-back", f"event log: {event_type}", result="ok")
    except OSError as e:
        log_action("write-back", f"event log write failed: {e}", result="error")


# --- Parsers ---

def _protect_inner_pipes(line: str) -> str:
    """Replace pipe characters inside [[ ]] and < > with a placeholder."""
    result = []
    depth_bracket = 0
    depth_angle = 0
    i = 0
    while i < len(line):
        ch = line[i]
        if line[i:i+2] == "[[":
            depth_bracket += 1
            result.append("[[")
            i += 2
            continue
        elif line[i:i+2] == "]]":
            depth_bracket = max(0, depth_bracket - 1)
            result.append("]]")
            i += 2
            continue
        elif ch == "<" and depth_bracket == 0:
            depth_angle += 1
        elif ch == ">" and depth_angle > 0:
            depth_angle -= 1

        if ch == "|" and (depth_bracket > 0 or depth_angle > 0):
            result.append("\x00")
        else:
            result.append(ch)
        i += 1
    return "".join(result)


def _split_table_row(line: str) -> list[str]:
    """Split a markdown table row on pipes, respecting wikilinks and HTML."""
    protected = _protect_inner_pipes(line)
    cells = [c.strip().replace("\x00", "|") for c in protected.split("|")]
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def parse_spawn_queue(content: str) -> list[dict]:
    """Parse the Queued section of _spawn-queue.md.

    Returns list of dicts with keys: number, chat_name, handoff_pointer,
    substrate_rec, estimated_time, conflicts, prompt_snippet.
    """
    rows = []

    queued_match = re.search(
        r"## 🔵 Queued \(ready to spawn\)\s*\n",
        content,
    )
    if not queued_match:
        log_action("parse", "spawn-queue: no Queued section found", result="warning")
        return rows

    section_start = queued_match.end()
    next_section = re.search(r"\n## ", content[section_start:])
    if next_section:
        section_text = content[section_start : section_start + next_section.start()]
    else:
        section_text = content[section_start:]

    lines = section_text.split("\n")
    in_table = False
    header_seen = False

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table:
                break
            continue

        cells = _split_table_row(stripped)

        if not header_seen:
            header_seen = True
            continue

        if re.match(r"^[-|:\s]+$", stripped):
            in_table = True
            continue

        if not in_table:
            continue

        if len(cells) < 6:
            continue

        row = {
            "number": cells[0].strip(),
            "chat_name": cells[1].strip(),
            "handoff_pointer": cells[2].strip(),
            "substrate_rec": cells[3].strip(),
            "estimated_time": cells[4].strip(),
            "conflicts": cells[5].strip(),
        }
        rows.append(row)

    log_action("parse", f"spawn-queue: {len(rows)} queued rows found")
    return rows


def parse_active_chats(content: str) -> list[str]:
    """Parse the Active section of _active-chats-tracker.md.

    Returns a list of chat names currently in-flight.
    """
    active_names = []

    active_match = re.search(
        r"## 🟡 Active / in-flight chats\s*\n",
        content,
    )
    if not active_match:
        log_action("parse", "tracker: no Active section found", result="warning")
        return active_names

    section_start = active_match.end()
    next_section = re.search(r"\n## ", content[section_start:])
    if next_section:
        section_text = content[section_start : section_start + next_section.start()]
    else:
        section_text = content[section_start:]

    lines = section_text.split("\n")
    in_table = False
    header_seen = False

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table:
                break
            continue

        cells = _split_table_row(stripped)

        if not header_seen:
            header_seen = True
            continue

        if re.match(r"^[-|:\s]+$", stripped):
            in_table = True
            continue

        if not in_table:
            continue

        if len(cells) >= 2:
            chat_name = cells[1].strip()
            active_names.append(chat_name)

    log_action("parse", f"tracker: {len(active_names)} active chats found")
    return active_names


def extract_handoff_path(pointer_cell: str) -> str | None:
    r"""Extract a relative file path from a handoff pointer cell.

    Handles both plain and Obsidian-escaped wikilinks:
      '[[path|display]]' and '[[path\|display]]' (table-escaped pipe)
    """
    m = re.search(r"\[\[(.+?)(?:\\?\|[^\]]+)?\]\]", pointer_cell)
    if not m:
        return None
    raw_path = m.group(1).rstrip("\\")
    if ".." in Path(raw_path).parts or raw_path.startswith("/"):
        return None
    rel_path = f"_meta/handoffs/{raw_path}"
    if not rel_path.endswith(".md"):
        rel_path += ".md"
    return rel_path


def get_event_log_tail(n_lines: int = 50) -> str:
    """Read the last ~N lines of _event-log.md."""
    content = safe_read("_meta/_event-log.md")
    if not content:
        return "(event log not readable)"
    lines = content.strip().split("\n")
    tail = lines[-n_lines:] if len(lines) > n_lines else lines
    return "\n".join(tail)


# --- Cross-reference ---

def find_ready_rows(
    queued_rows: list[dict],
    active_names: list[str],
) -> list[dict]:
    """Filter queued rows to those not already in-flight.

    Compares by extracting the [TAG] bracket from chat names.
    """
    active_tags = set()
    for name in active_names:
        tag_match = re.search(r"\[([^\]]+)\]", name)
        if tag_match:
            active_tags.add(tag_match.group(1).upper())

    ready = []
    for row in queued_rows:
        tag_match = re.search(r"\[([^\]]+)\]", row["chat_name"])
        if tag_match:
            row_tag = tag_match.group(1).upper()
            if row_tag in active_tags:
                log_action(
                    "cross-ref",
                    f"skipping [{row_tag}] — already in-flight",
                )
                continue
        ready.append(row)

    log_action("cross-ref", f"{len(ready)} ready rows after filtering")
    return ready


# --- Output Formatting ---

def format_telegram_message(
    ready_rows: list[dict],
    skipped_count: int,
    active_count: int,
) -> str:
    """Format the Telegram surface message."""
    if not ready_rows and skipped_count == 0:
        return (
            "\U0001f535 Bridge: no new rows ready for harness.\n"
            f"({active_count} chats currently in-flight)"
        )

    lines = []
    if ready_rows:
        lines.append(
            f"\U0001f535 Bridge found {len(ready_rows)} queued row(s):"
        )
        for row in ready_rows:
            conflicts = row.get("conflicts", "none")
            conflict_flag = " \u26a0\ufe0f" if "blocked" in conflicts.lower() else ""
            lines.append(
                f"  \u2022 #{row['number']} {row['chat_name']}"
                f" ({row['estimated_time']}){conflict_flag}"
            )
    else:
        lines.append(
            "\U0001f535 Bridge: no new rows (all already surfaced)."
        )

    if skipped_count > 0:
        lines.append(f"({skipped_count} rows skipped — already in claim ledger)")

    lines.append(f"\n({active_count} chats in-flight)")

    # Write-back confirmation (D-N Telegram alert)
    lines.append(
        f"\nBridge wrote status digest + {len(ready_rows)} claim entries to outbox"
    )

    return "\n".join(lines)


# --- Main ---

def main():
    """Bridge skill main entry point."""
    log_action(
        "bridge-start",
        f"Level 1 read+surface+write-back run — "
        f"vault={VAULT_BASE}, mode={BRIDGE_MODE}, outbox={OUTBOX_BASE}",
    )

    # Step 1: Freshness gate (D-L / AC-6)
    if not check_freshness():
        stale_msg = "\u26a0\ufe0f Vault sync stale \u2014 skipping this run"
        print(stale_msg)
        log_action("bridge-abort", "freshness gate failed", result="stale")
        flush_action_log()
        sys.exit(2)

    log_action("sync", "vault fresh", result="ok")

    # Step 2: Read spawn queue (D-B item 1)
    sq_content = safe_read("_meta/handoffs/_spawn-queue.md")
    if not sq_content:
        print("\u26a0\ufe0f Bridge: could not read spawn queue")
        log_action("bridge-abort", "spawn queue unreadable", result="error")
        flush_action_log()
        sys.exit(1)

    queued_rows = parse_spawn_queue(sq_content)

    # Step 3: Read active chats tracker (D-B item 2)
    tracker_content = safe_read("_meta/handoffs/_active-chats-tracker.md")
    if not tracker_content:
        print("\u26a0\ufe0f Bridge: could not read active chats tracker")
        log_action("bridge-abort", "tracker unreadable", result="error")
        flush_action_log()
        sys.exit(1)

    active_names = parse_active_chats(tracker_content)

    # Step 4: Read referenced handoff files for context (D-B item 3)
    for row in queued_rows:
        handoff_path = extract_handoff_path(row.get("handoff_pointer", ""))
        if handoff_path:
            safe_read(handoff_path)

    # Step 5: Read event log tail (D-B item 4)
    get_event_log_tail(50)
    log_action("read", "event log tail (~50 lines)")

    # Step 6: Cross-reference — find ready rows
    ready_rows = find_ready_rows(queued_rows, active_names)

    # Step 7: Claim ledger check (D-L / AC-8 — idempotency)
    claimed_ids = load_claim_ledger()
    new_rows = []
    skipped_count = 0

    for row in ready_rows:
        handoff_pointer = row.get("handoff_pointer", "")
        chat_name = row.get("chat_name", "")
        rid = _row_id(handoff_pointer, chat_name)
        if rid in claimed_ids:
            log_action(
                "claim-check",
                f"skipping #{row['number']} {chat_name} — already claimed ({rid})",
            )
            skipped_count += 1
        else:
            row["_row_id"] = rid
            new_rows.append(row)

    log_action(
        "claim-check",
        f"{len(new_rows)} new, {skipped_count} already claimed",
    )

    # Step 8: Write claims for newly surfaced rows (D-L)
    for row in new_rows:
        summary = f"#{row['number']} {row['chat_name']} ({row['estimated_time']})"
        append_claim(row["_row_id"], summary)

    # Step 9: Write status digest (D-M)
    write_status_digest(
        surfaced_count=len(new_rows),
        skipped_count=skipped_count,
        active_count=len(active_names),
        sync_status="fresh",
    )

    # Step 10: Write event log entry (D-M)
    if new_rows:
        row_nums = ", ".join(f"#{r['number']}" for r in new_rows)
        append_event_log_entry(
            "surface",
            f"Surfaced {len(new_rows)} rows: {row_nums}",
        )
    else:
        append_event_log_entry(
            "surface",
            f"No new rows (0 surfaced, {skipped_count} already claimed)",
        )

    # Step 11: Format and output (stdout — Telegram message)
    message = format_telegram_message(new_rows, skipped_count, len(active_names))
    print(message)

    log_action("surface", f"Telegram message: {len(new_rows)} rows surfaced")

    log_action(
        "bridge-complete",
        f"{len(new_rows)} surfaced, {skipped_count} skipped, "
        f"{len(active_names)} active",
    )
    log_action("write-back", "outbox write-back complete", result="ok")

    # Flush action log last (D-N)
    flush_action_log()


if __name__ == "__main__":
    main()
