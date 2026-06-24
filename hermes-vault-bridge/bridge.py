#!/usr/bin/env python3
"""
Hermes Vault Bridge — Level 1 (Read + Surface)

Reads the vault's spawn-queue and active-chats tracker, cross-references
to find ready-but-not-in-flight rows, and outputs a formatted Telegram
surface message.

Hard-coded read allowlist (D-B):
  1. _meta/handoffs/_spawn-queue.md
  2. _meta/handoffs/_active-chats-tracker.md
  3. Referenced handoff files (from spawn-queue rows)
  4. _meta/_event-log.md (last ~50 rows)

AC-5: Every file read is logged to stderr.
AC-6: Freshness gate — checks git recency; in sandbox mode (default when
      VAULT_BRIDGE_MODE=sandbox), checks commit age only — host cron handles
      git pull. In host mode, pulls if stale.
AC-15: Level 1 only — no writes, no claims, no autonomous action.

Environment variables:
  VAULT_BRIDGE_BASE  — vault clone path (default: /home/hermes/hermes-data/vault/second-brain)
  VAULT_BRIDGE_MODE  — "sandbox" (default) or "host"
    sandbox: read-only, no git pull (host cron syncs; deploy key not available)
    host: git pull --ff-only on stale (for direct host-side runs)
"""

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


def _detect_vault_base() -> tuple[Path, str]:
    """Auto-detect vault path and bridge mode.

    Resolution order:
      1. VAULT_BRIDGE_BASE env var (explicit override)
      2. /workspace/vault-second-brain (container/sandbox — read-only mount)
      3. /home/hermes/hermes-data/vault/second-brain (host — has deploy key)

    Mode is tied to detection unless VAULT_BRIDGE_MODE is explicitly set:
      - Container path → sandbox (no git pull)
      - Host path → host (git pull on stale)
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


VAULT_BASE, BRIDGE_MODE = _detect_vault_base()
VAULT_BASE_RESOLVED = VAULT_BASE.resolve()
STALENESS_THRESHOLD_MINUTES = 15  # host mode: commit-age threshold for pull
SYNC_STALENESS_THRESHOLD_MINUTES = 420  # sandbox mode: 7h (6h cron + 1h buffer)

# Action log goes to a file (not stderr) so Hermes's terminal tool returns
# ONLY stdout (the Telegram message) to the model. AC-5 compliance preserved.
ACTION_LOG_PATH = Path(os.environ.get(
    "VAULT_BRIDGE_LOG",
    "/tmp/hermes-vault-bridge.log",
))

# D-B allowlist — only these paths (relative to VAULT_BASE) may be read
ALLOWLIST_PREFIXES = [
    "_meta/handoffs/_spawn-queue.md",
    "_meta/handoffs/_active-chats-tracker.md",
    "_meta/handoffs/",  # for referenced handoff files
    "_meta/_event-log.md",
]

# Action log entries (written to stdout as JSON lines)
action_log = []


def log_action(operation: str, detail: str, result: str = "ok"):
    """Log an operation to the in-memory action log."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "operation": operation,
        "detail": detail,
        "result": result,
    }
    action_log.append(entry)


def flush_action_log():
    """Write the action log to ACTION_LOG_PATH (not stderr).

    Keeps stdout clean for the Telegram message so Hermes's terminal tool
    returns only the surface message to the model.
    """
    try:
        with open(ACTION_LOG_PATH, "w", encoding="utf-8") as f:
            for entry in action_log:
                f.write(json.dumps(entry) + "\n")
    except OSError:
        # If log file is unwritable (e.g. read-only fs), silently skip —
        # the Telegram surface message is the primary deliverable.
        pass


def log_read(filepath: str):
    """Log a file read (AC-5 compliance). Written to log file, not stderr."""
    log_action("read", filepath)


def log_skip(filepath: str, reason: str):
    """Log a skipped read attempt. Written to log file, not stderr."""
    log_action("read-blocked", filepath, result=reason)


def is_allowlisted(rel_path: str) -> bool:
    """Check if a relative path falls within the D-B read allowlist."""
    for prefix in ALLOWLIST_PREFIXES:
        if prefix.endswith("/"):
            # Directory prefix — path must start with it
            if rel_path.startswith(prefix):
                return True
        else:
            # Exact file match
            if rel_path == prefix:
                return True
    return False


def safe_read(rel_path: str) -> str | None:
    """Read a file only if it's within the D-B allowlist.

    Returns file content or None if blocked/missing.
    """
    # Normalize and reject path traversal BEFORE allowlist check
    normalized = os.path.normpath(rel_path)
    if ".." in Path(normalized).parts:
        log_skip(rel_path, "path traversal rejected")
        return None
    rel_path = normalized

    if not is_allowlisted(rel_path):
        log_skip(rel_path, "outside D-B allowlist")
        return None

    full_path = VAULT_BASE / rel_path
    # Resolve to catch symlink escapes
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

    In sandbox mode (default): checks .git/FETCH_HEAD mtime — this file is
    updated on every git fetch/pull, even when there are no new commits.
    Threshold = SYNC_STALENESS_THRESHOLD_MINUTES (7h, aligned with 6h cron).
    No git pull (container has no deploy key per I23).

    In host mode: checks commit age, pulls if stale, fails if pull fails.
    Threshold = STALENESS_THRESHOLD_MINUTES (15min).
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
            # FETCH_HEAD missing — vault may never have been fetched/pulled.
            # Fall back to .git/HEAD mtime as a last resort.
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

        # Stale — attempt pull
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
    # Strip the timezone offset and parse separately
    parts = date_str.rsplit(" ", 1)
    if len(parts) == 2:
        dt_part, tz_part = parts
        # Parse the datetime part
        dt = datetime.strptime(dt_part, "%Y-%m-%d %H:%M:%S")
        # Parse timezone offset
        tz_sign = 1 if tz_part[0] == "+" else -1
        tz_hours = int(tz_part[1:3])
        tz_mins = int(tz_part[3:5])
        tz_offset = timedelta(hours=tz_hours, minutes=tz_mins) * tz_sign
        dt = dt.replace(tzinfo=timezone(tz_offset))
        return dt.astimezone(timezone.utc)
    # Fallback — treat as UTC
    dt = datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S")
    return dt.replace(tzinfo=timezone.utc)


# --- Parsers ---

def _protect_inner_pipes(line: str) -> str:
    """Replace pipe characters inside [[ ]] and < > with a placeholder.

    Markdown table rows use | as delimiter, but wikilinks ([[path|display]])
    and HTML tags (<details>...<summary>...</summary>...</details>) can
    contain literal pipes. We temporarily replace them so split("|") works.
    """
    result = []
    depth_bracket = 0  # inside [[ ]]
    depth_angle = 0    # inside < >
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
            result.append("\x00")  # placeholder
        else:
            result.append(ch)
        i += 1
    return "".join(result)


def _split_table_row(line: str) -> list[str]:
    """Split a markdown table row on pipes, respecting wikilinks and HTML."""
    protected = _protect_inner_pipes(line)
    cells = [c.strip().replace("\x00", "|") for c in protected.split("|")]
    # Remove empty first/last cells from leading/trailing |
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

    # Find the "Queued (ready to spawn)" section
    queued_match = re.search(
        r"## 🔵 Queued \(ready to spawn\)\s*\n",
        content,
    )
    if not queued_match:
        log_action("parse", "spawn-queue: no Queued section found", result="warning")
        return rows

    # Extract from the queued section start to the next ## heading
    section_start = queued_match.end()
    next_section = re.search(r"\n## ", content[section_start:])
    if next_section:
        section_text = content[section_start : section_start + next_section.start()]
    else:
        section_text = content[section_start:]

    # Find the table — look for header row then separator then data rows
    # Header: | # | Chat name | Handoff pointer | Substrate rec | ...
    # Separator: |---|---|---|---|...
    # Data: | 5 | [WF-7] ... | ... |
    lines = section_text.split("\n")
    in_table = False
    header_seen = False

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table:
                break  # End of table
            continue

        cells = _split_table_row(stripped)

        if not header_seen:
            # First | row = header
            header_seen = True
            continue

        if re.match(r"^[-|:\s]+$", stripped):
            # Separator row
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

    # Find the Active section
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

    # Find the table rows (| Started | Chat name | ...)
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

    Examples:
      '[[website-factory/handoff-...\|WF-7 handoff]]' -> '_meta/handoffs/website-factory/handoff-...'
      '[[handoff-...|handoff]]' -> '_meta/handoffs/handoff-...'
    """
    # Match wikilink: [[path\|display]] or [[path|display]] or [[path]]
    # The \| form is Obsidian's escape for pipes inside table cells
    m = re.search(r"\[\[(.+?)(?:\\?\|[^\]]+)?\]\]", pointer_cell)
    if not m:
        return None
    raw_path = m.group(1).rstrip("\\")  # Strip trailing backslash if present
    # Reject path traversal and absolute paths
    if ".." in Path(raw_path).parts or raw_path.startswith("/"):
        return None
    # Handoff pointers are relative to _meta/handoffs/
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
    # Extract tags from active chat names for matching
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
    active_count: int,
    event_log_summary: str,
) -> str:
    """Format the Telegram surface message."""
    if not ready_rows:
        return (
            "🔵 Bridge: no new rows ready for harness.\n"
            f"({active_count} chats currently in-flight)"
        )

    lines = [f"🔵 Bridge found {len(ready_rows)} queued row(s):"]
    for row in ready_rows:
        conflicts = row.get("conflicts", "none")
        conflict_flag = " ⚠️" if "blocked" in conflicts.lower() else ""
        lines.append(
            f"  • #{row['number']} {row['chat_name']}"
            f" ({row['estimated_time']}){conflict_flag}"
        )

    lines.append(f"\n({active_count} chats in-flight)")
    return "\n".join(lines)


# --- Main ---

def main():
    """Bridge skill main entry point."""
    log_action(
        "bridge-start",
        f"Level 1 read+surface run — vault={VAULT_BASE}, mode={BRIDGE_MODE}",
    )

    # Step 1: Freshness gate (D-L / AC-6)
    if not check_freshness():
        stale_msg = "⚠️ Vault sync stale — skipping this run"
        print(stale_msg)
        log_action("bridge-abort", "freshness gate failed", result="stale")
        flush_action_log()
        # Exit code 2 = stale vault (distinguishable from 0=success, 1=error)
        sys.exit(2)

    # Step 2: Read spawn queue (D-B item 1)
    sq_content = safe_read("_meta/handoffs/_spawn-queue.md")
    if not sq_content:
        print("⚠️ Bridge: could not read spawn queue")
        log_action("bridge-abort", "spawn queue unreadable", result="error")
        flush_action_log()
        sys.exit(1)

    queued_rows = parse_spawn_queue(sq_content)

    # Step 3: Read active chats tracker (D-B item 2)
    tracker_content = safe_read("_meta/handoffs/_active-chats-tracker.md")
    if not tracker_content:
        print("⚠️ Bridge: could not read active chats tracker")
        log_action("bridge-abort", "tracker unreadable", result="error")
        flush_action_log()
        sys.exit(1)

    active_names = parse_active_chats(tracker_content)

    # Step 4: Read referenced handoff files for context (D-B item 3)
    for row in queued_rows:
        handoff_path = extract_handoff_path(row.get("handoff_pointer", ""))
        if handoff_path:
            handoff_content = safe_read(handoff_path)
            if handoff_content:
                # Extract the one-line description from frontmatter or first paragraph
                # Just note we read it — the summary comes from the spawn-queue row
                pass

    # Step 5: Read event log tail (D-B item 4)
    event_tail = get_event_log_tail(50)
    log_action("event-log", f"read last ~50 lines")

    # Step 6: Cross-reference — find ready rows
    ready_rows = find_ready_rows(queued_rows, active_names)

    # Step 7: Format and output
    message = format_telegram_message(ready_rows, len(active_names), event_tail)
    print(message)

    log_action("bridge-complete", f"{len(ready_rows)} ready, {len(active_names)} active")

    # Write action log to file (AC-5 + D-N) — NOT stderr, so Hermes's
    # terminal tool returns only the clean stdout message to the model.
    flush_action_log()


if __name__ == "__main__":
    main()
