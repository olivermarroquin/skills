# Phase 3 Wave 1 — Operator Steps

All commands run on the box via SSH as root (or sudo where noted).
One command per line. Paste-safe — no backslash continuations.

---

## Step 1: Set Telegram home channel (AC-1)

In your Telegram DM with @HermesOliverProdBot, type:

```
/sethome
```

The bot will reply with the chat name and chat_id confirming the home channel is set.

**Verify it persisted to .env:**

```
sudo -u hermes grep TELEGRAM_HOME_CHANNEL /home/hermes/.hermes/.env
```

Expected: `TELEGRAM_HOME_CHANNEL=<your-chat-id>` (and optionally `TELEGRAM_HOME_CHANNEL_THREAD_ID`).

---

## Step 2: Check existing Hermes crons (AC-3 prep)

```
sudo -u hermes /home/hermes/.local/bin/hermes cron list
```

Paste the output back. I need to see:
- Whether the vault-bridge is scheduled as a Hermes cron
- What `deliver:` is set to on each cron

If the vault-bridge cron exists but doesn't deliver to Telegram, we'll update it.
If no crons exist, we'll create a test cron to verify AC-3.

---

## Step 3: Place boot-health-check hook (AC-2, AC-4, AC-5)

```
sudo -u hermes mkdir -p /home/hermes/.hermes/hooks/boot-health-check
```

Then copy the two files from this directory to the box. You can use scp or paste:

**HOOK.yaml:**
```
sudo -u hermes tee /home/hermes/.hermes/hooks/boot-health-check/HOOK.yaml << 'HOOKEOF'
name: boot-health-check
description: >-
  Gateway startup health check (boot.md pattern). Inspects cron failures,
  vault-sync freshness (FETCH_HEAD mtime > 7h = stale), and systemd service
  health (hermes + hermes-dashboard). Posts a Telegram summary on issues found;
  silent on all-clear.
events:
  - gateway:startup
HOOKEOF
```

**handler.py:**
```
sudo -u hermes tee /home/hermes/.hermes/hooks/boot-health-check/handler.py << 'PYEOF'
"""
boot-health-check hook — gateway:startup event handler.

Runs three health checks on every gateway start:
  1. Cron status   — scans recent cron output for failures.
  2. Vault-sync    — checks FETCH_HEAD mtime; stale if >7h since last fetch.
  3. Service health — checks hermes + hermes-dashboard systemd units.

Posts a Telegram summary ONLY when issues are found. Silent on all-clear.

No secrets in this file. Bot token and home channel are read from env at
runtime (TELEGRAM_BOT_TOKEN, TELEGRAM_HOME_CHANNEL).
"""

import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# --- Configuration -----------------------------------------------------------

HERMES_HOME = Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")))
VAULT_SYNC_PATH = Path(
    os.environ.get(
        "VAULT_SYNC_PATH",
        os.path.expanduser("~/hermes-data/vault/second-brain"),
    )
)
FETCH_HEAD_STALE_HOURS = 7
CRON_OUTPUT_DIR = HERMES_HOME / "cron" / "output"
SYSTEMD_UNITS = ["hermes", "hermes-dashboard"]


# --- Health checks -----------------------------------------------------------


def _check_cron_failures() -> Optional[str]:
    """Scan recent cron output directories for failures."""
    if not CRON_OUTPUT_DIR.exists():
        return None

    failures = []
    for job_dir in CRON_OUTPUT_DIR.iterdir():
        if not job_dir.is_dir():
            continue
        runs = sorted(
            [d for d in job_dir.iterdir() if d.is_dir()],
            key=lambda d: d.name,
            reverse=True,
        )
        if not runs:
            continue
        latest = runs[0]
        result_file = latest / "result.json"
        error_file = latest / "error.txt"
        if error_file.exists():
            error_text = error_file.read_text(encoding="utf-8").strip()[:200]
            failures.append(f"  • {job_dir.name}: {error_text}")
        elif result_file.exists():
            import json

            try:
                result = json.loads(result_file.read_text(encoding="utf-8"))
                status = result.get("status", "").lower()
                if status in ("failed", "error", "timeout"):
                    msg = result.get("error", result.get("message", status))
                    failures.append(f"  • {job_dir.name}: {str(msg)[:200]}")
            except (json.JSONDecodeError, OSError):
                pass

    if failures:
        return "🔴 Cron failures detected:\n" + "\n".join(failures)
    return None


def _check_vault_sync_freshness() -> Optional[str]:
    """Check FETCH_HEAD mtime to determine if vault sync is stale.

    Uses FETCH_HEAD mtime (not commit date) because commit date measures
    vault activity, not sync health — a quiet weekend with no commits
    would false-alarm on commit-date freshness.
    """
    fetch_head = VAULT_SYNC_PATH / ".git" / "FETCH_HEAD"
    if not fetch_head.exists():
        git_path = VAULT_SYNC_PATH / ".git"
        if git_path.is_file():
            git_dir_line = git_path.read_text(encoding="utf-8").strip()
            if git_dir_line.startswith("gitdir:"):
                real_git = Path(git_dir_line.split(":", 1)[1].strip())
                if not real_git.is_absolute():
                    real_git = VAULT_SYNC_PATH / real_git
                fetch_head = real_git / "FETCH_HEAD"

    if not fetch_head.exists():
        return "🟡 Vault sync: FETCH_HEAD not found — sync may not be configured."

    mtime = fetch_head.stat().st_mtime
    age_hours = (time.time() - mtime) / 3600

    if age_hours > FETCH_HEAD_STALE_HOURS:
        return (
            f"🟡 Vault sync stale: last fetch was {age_hours:.1f}h ago "
            f"(threshold: {FETCH_HEAD_STALE_HOURS}h)."
        )
    return None


def _check_service_health() -> Optional[str]:
    """Check hermes + hermes-dashboard systemd units are active."""
    issues = []
    for unit in SYSTEMD_UNITS:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", unit],
                capture_output=True,
                text=True,
                timeout=5,
            )
            status = result.stdout.strip()
            if status != "active":
                issues.append(f"  • {unit}: {status}")
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            issues.append(f"  • {unit}: check failed ({e})")

    if issues:
        return "🔴 Service health issues:\n" + "\n".join(issues)
    return None


# --- Telegram delivery -------------------------------------------------------


def _send_telegram(message: str) -> None:
    """Send a message to the Telegram home channel via Bot API."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_HOME_CHANNEL")

    if not bot_token or not chat_id:
        logger.warning(
            "boot-health-check: cannot send Telegram — "
            "TELEGRAM_BOT_TOKEN or TELEGRAM_HOME_CHANNEL not set."
        )
        return

    thread_id = os.environ.get("TELEGRAM_HOME_CHANNEL_THREAD_ID")

    import urllib.request
    import urllib.parse
    import json as _json

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    if thread_id:
        payload["message_thread_id"] = int(thread_id)

    data = _json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                logger.warning(
                    "boot-health-check: Telegram API returned %s", resp.status
                )
    except Exception as e:
        logger.warning("boot-health-check: Telegram send failed: %s", e)


# --- Main handler ------------------------------------------------------------


def handle(event_type: str, context: dict) -> None:
    """Gateway startup hook handler.

    Runs all health checks. If any issues found, posts a summary to Telegram.
    Silent on all-clear (no noise).
    """
    issues = []

    cron_check = _check_cron_failures()
    if cron_check:
        issues.append(cron_check)

    sync_check = _check_vault_sync_freshness()
    if sync_check:
        issues.append(sync_check)

    svc_check = _check_service_health()
    if svc_check:
        issues.append(svc_check)

    if not issues:
        logger.info("boot-health-check: all clear — no issues found.")
        return

    platforms = context.get("platforms", [])
    header = (
        f"⚡ *Boot Health Check*\n"
        f"Platforms: {', '.join(platforms) if platforms else 'unknown'}\n"
        f"{'─' * 30}"
    )
    body = "\n\n".join(issues)
    message = f"{header}\n\n{body}"

    _send_telegram(message)
    logger.warning("boot-health-check: %d issue(s) found and reported.", len(issues))
PYEOF
```

**Verify ownership:**
```
ls -la /home/hermes/.hermes/hooks/boot-health-check/
```

Expected: both files owned by `hermes:hermes`.

---

## Step 4: Restart gateway to trigger boot hook (AC-2 verification)

```
sudo systemctl stop hermes
```
```
sudo systemctl start hermes
```

(Separate commands — sudoers is exact-match, combined `stop hermes hermes-dashboard` is NOT allowlisted.)

**Check Telegram:** If all healthy → silence (no message). If any issue → you'll get a health summary in the home channel DM.

**Check logs for hook loading:**
```
sudo journalctl -u hermes --since "1 min ago" --no-pager | grep -i hook
```

Expected: `[hooks] Loaded hook 'boot-health-check' for events: ['gateway:startup']`

---

## Step 5: Test cron delivery to Telegram (AC-3 verification)

First, check what crons exist:
```
sudo -u hermes /home/hermes/.local/bin/hermes cron list
```

To test delivery, create a one-shot test cron that delivers to Telegram:
```
sudo -u hermes /home/hermes/.local/bin/hermes cron add --name test-telegram-delivery --schedule "in 1 minute" --deliver telegram --prompt "Say: Telegram delivery test successful. Then output [DONE]."
```

(If the `--schedule "in 1 minute"` syntax isn't supported, use a near-future time or run the vault-bridge manually and check Telegram.)

**Check Telegram:** The test cron result should land in your home channel DM within ~1 minute.

After verification, remove the test cron:
```
sudo -u hermes /home/hermes/.local/bin/hermes cron remove test-telegram-delivery
```

---

## Step 6: Verification summary (paste back)

Please paste back the output of each of these for AC evidence:

```
sudo -u hermes grep TELEGRAM_HOME_CHANNEL /home/hermes/.hermes/.env
```
```
ls -la /home/hermes/.hermes/hooks/boot-health-check/
```
```
sudo journalctl -u hermes --since "5 min ago" --no-pager | grep -i hook
```
```
sudo -u hermes /home/hermes/.local/bin/hermes cron list
```

And confirm:
- [ ] AC-1: `/sethome` reply received + env var persisted
- [ ] AC-2: Gateway restarted → hook loaded (journal line) → Telegram received health check OR silence on all-clear
- [ ] AC-3: Test cron output landed in Telegram home channel
- [ ] AC-4: All 3 health checks present in handler.py (cron failures, FETCH_HEAD freshness, systemd units)
- [ ] AC-5: `ls -la` shows hermes:hermes ownership on hook files

---

## Rollback (if needed)

```
sudo -u hermes rm -rf /home/hermes/.hermes/hooks/boot-health-check/
```
```
sudo systemctl stop hermes
```
```
sudo systemctl start hermes
```

To revert the home channel:
```
sudo -u hermes sed -i '/TELEGRAM_HOME_CHANNEL/d' /home/hermes/.hermes/.env
```
```
sudo systemctl stop hermes
```
```
sudo systemctl start hermes
```
