---
name: vault-bridge
description: "Read the operator's Knowledge OS vault — the spawn-queue and active-chats tracker — surface handoff rows that are ready to spawn but not yet in-flight, and write claim ledger + status digest + event log + action log to the Hermes outbox. Use when the operator asks to run the vault bridge, check the vault handoff queue, or see what handoffs are ready to spawn. Level 1: read, surface, and write to outbox only; never claims, spawns, writes to the live vault, or does git push."
version: 2.0.0
platforms: [linux]
metadata:
  hermes:
    tags: [vault, handoff, spawn-queue, knowledge-os, bridge, operator, outbox, claim-ledger, observability]
    related_skills: []
---

# Vault Bridge Skill (Level 1 — Read + Surface + Outbox Write-Back)

You are the vault bridge. Your job is to read the operator's Knowledge OS vault
(synced to this box via git), find handoff rows that are ready to spawn but not
yet in-flight, surface them via Telegram, and write observability data to the
Hermes outbox (claim ledger, status digest, event log, action log).

You do NOT take autonomous action on the rows. You do NOT write to the live
vault clone. You do NOT do git push. The outbox is the air-gap — the operator
reviews and merges.

## How to run

Execute the bridge script. It auto-detects its environment:

```bash
python3 ~/.hermes/skills/vault-bridge/bridge.py
```

The script auto-detects the vault path, outbox path, and mode at startup:

**Vault path:**
1. `VAULT_BRIDGE_BASE` env var if set (explicit override), else
2. `/workspace/vault-second-brain` if it exists (container — sandbox mode), else
3. `/home/hermes/hermes-data/vault/second-brain` (host — host mode)

**Outbox path:**
1. `VAULT_BRIDGE_OUTBOX` env var if set (explicit override), else
2. `/workspace/hermes-outbox` if it exists (container — writable mount), else
3. `/home/hermes/hermes-data/hermes-outbox` (host)

Mode is tied to the detected vault path:
- **sandbox** (container): read-only vault, no git pull (host cron syncs; deploy
  key not available per I23). Freshness = `.git/FETCH_HEAD` mtime, 7h threshold.
- **host**: git pull on stale. Freshness = commit age, 15min threshold.

## What happens

The script will:

1. **Freshness gate** — check if the vault clone is fresh.
   - **Sandbox mode** (default): checks `.git/FETCH_HEAD` mtime (updated by
     every fetch/pull, even with no new commits). Threshold: 7 hours (aligned
     with the 6h host cron + 1h buffer). No git pull — host cron handles sync.
   - **Host mode**: checks last commit age (<15min). Pulls if stale.
   If stale in either mode, outputs "Vault sync stale — skipping this run"
   and exits (code 2). Do NOT read stale data.

2. **Read the handoff queue** — parse `_meta/handoffs/_spawn-queue.md` for rows
   in the "Queued (ready to spawn)" section.

3. **Read the active tracker** — parse `_meta/handoffs/_active-chats-tracker.md`
   for chats currently in-flight.

4. **Cross-reference** — filter out queued rows that are already in-flight.

5. **Claim ledger check** — load `hermes-outbox/_meta/handoffs/_hermes-claimed.jsonl`
   and skip rows already surfaced (idempotency — AC-8).

6. **Read referenced handoff files** — for context on each queued row.

7. **Read event log** — last ~50 rows of `_meta/_event-log.md` for freshness.

8. **Write to outbox** (all writes go to hermes-outbox/, never the vault):
   - Append new claims to `_meta/handoffs/_hermes-claimed.jsonl` (D-L)
   - Write status digest to `_meta/handoffs/_hermes-status.md` (D-M)
   - Append event to `_meta/_event-log-hermes.md` (D-M)
   - Append action log entries to `_hermes-bridge-actions.jsonl` (D-N)

9. **Output** — a formatted message listing ready rows (or "no new rows") +
   write-back confirmation.

## What you do with the output

Send the script's stdout output verbatim as a Telegram message to the operator.
Relay the ENTIRE stdout block — it starts with a blue circle and contains the
row list + write-back confirmation. Do not summarize, paraphrase, or omit any
part of it.

The action log (every file read, every operation) is written to
`/tmp/hermes-vault-bridge.log` — NOT to stderr or stdout. You do not need
to read or relay the log file. It exists for operator debugging only.

If the script exits with a stale-vault message, send that message instead.

## What you must NOT do

- Do NOT take autonomous action on any rows (no claiming, no spawning)
- Do NOT read files outside the script's built-in allowlist
- Do NOT write to the live vault clone in any way
- Do NOT do git push

The outbox is the air-gap. The operator reviews and merges outbox content into
the live vault on the Mac side.

## Invocation

The operator will ask to "run the vault bridge", "check the vault handoff queue",
or "see what handoffs are ready to spawn". These are your trigger phrases.

Avoid interpreting bare "spawn queue" or "check queue" as this skill — those
phrases collide with Hermes's built-in process/cron-queue commands. Respond to
vault-specific phrasing only.

## Cron usage

This skill can be registered as a cron job for periodic checks (e.g., every 6h):

```
run the vault bridge
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Success — message printed to stdout, outbox updated |
| 1 | Error — could not read required files |
| 2 | Stale vault — git pull failed, no data read, no outbox writes |

## Installation

### 1. Place skill files

```bash
# As root on the box:
cp -r /tmp/vault-bridge/ /home/hermes/.hermes/skills/vault-bridge/
chown -R operator:hermes /home/hermes/.hermes/skills/vault-bridge/
chmod 755 /home/hermes/.hermes/skills/vault-bridge/
chmod 644 /home/hermes/.hermes/skills/vault-bridge/SKILL.md
chmod 755 /home/hermes/.hermes/skills/vault-bridge/bridge.py
```

### 2. Mount the vault clone into the container (read-only)

Already done in Wave 2. The vault clone is mounted read-only at
`/workspace/vault-second-brain` via a systemd `.mount` unit.

### 3. Mount the outbox into the container (read-write)

The outbox lives on the host at `/home/hermes/hermes-data/hermes-outbox/` but
is NOT mounted by default. It must be writable from inside the container.

**Step 1 — Create the mount point:**
```bash
mkdir -p /home/hermes/.hermes/sandboxes/docker/default/workspace/hermes-outbox
```

**Step 2 — Create the systemd mount unit:**

Generate the correct unit filename on the box (don't hand-write it):
```bash
UNIT_NAME=$(systemd-escape -p --suffix=mount /home/hermes/.hermes/sandboxes/docker/default/workspace/hermes-outbox)
echo "Unit filename: $UNIT_NAME"
```

Then create the unit file (use the generated filename):
```bash
cat > "/etc/systemd/system/${UNIT_NAME}" << 'EOF'
[Unit]
Description=Outbox bind mount for Hermes bridge skill (rw)
Before=hermes.service
After=local-fs.target

[Mount]
What=/home/hermes/hermes-data/hermes-outbox
Where=/home/hermes/.hermes/sandboxes/docker/default/workspace/hermes-outbox
Type=none
Options=bind

[Install]
WantedBy=multi-user.target
EOF
```

**Step 3 — Enable and start:**
```bash
systemctl daemon-reload
systemctl enable --now "${UNIT_NAME}"
```

**Step 4 — Verify:**
```bash
mount | grep hermes-outbox
ls /home/hermes/.hermes/sandboxes/docker/default/workspace/hermes-outbox/_meta/handoffs/_hermes-claimed.jsonl
```

In-container path: `/workspace/hermes-outbox`

**Note:** The container must be rebuilt after the mount is in place (Hermes
auto-rebuilds after ~5 min idle per `lifetime_seconds`, or force with
`docker rm` on the sandbox container). The outbox mount is read-write;
the vault mount remains read-only; the deploy key stays on the host only (I23).

### 4. Create symlink for box-side action log path (optional)

The action log primary copy lives inside the outbox at
`hermes-outbox/_hermes-bridge-actions.jsonl`. If you want the expected host
path to work too:

```bash
sudo -u hermes ln -sf /home/hermes/hermes-data/hermes-outbox/_hermes-bridge-actions.jsonl /home/hermes/hermes-data/hermes-bridge-actions.jsonl
```

### 5. Restart and verify

```bash
# Force container rebuild to pick up the new mount:
docker rm -f $(docker ps -q --filter name=hermes) 2>/dev/null || true
systemctl restart hermes
```

Verify the skill is discoverable by sending "run the vault bridge" via
Telegram. The output should now include a write-back confirmation line.

## Troubleshooting

- **"Vault sync stale"** — the git pull failed. Check network connectivity
  and the deploy key at `~/.ssh/hermes-vault-deploy-key`.
- **"could not read spawn queue"** — the vault clone may be missing or
  corrupted. Check `/home/hermes/hermes-data/vault/second-brain/` exists.
- **Empty results** — all queued rows may already be in-flight or claimed.
  Check the claim ledger: `cat hermes-outbox/_meta/handoffs/_hermes-claimed.jsonl`
- **Outbox write failures** — check the outbox mount is active:
  `mount | grep hermes-outbox`. Check permissions on hermes-outbox/.
- **Skill not in prompt snapshot** — restart Hermes. If still missing,
  investigate the local skill discovery mechanism.
