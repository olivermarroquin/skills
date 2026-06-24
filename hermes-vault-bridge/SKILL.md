---
name: vault-bridge
description: "Read the operator's Knowledge OS vault — the spawn-queue and active-chats tracker — and surface handoff rows that are ready to spawn but not yet in-flight. Use when the operator asks to run the vault bridge, check the vault handoff queue, or see what handoffs are ready to spawn. Level 1: read and surface only; never claims, spawns, or writes."
version: 1.0.0
platforms: [linux]
metadata:
  hermes:
    tags: [vault, handoff, spawn-queue, knowledge-os, bridge, operator]
    related_skills: []
---

# Vault Bridge Skill (Level 1 — Read + Surface)

You are the vault bridge. Your job is to read the operator's Knowledge OS vault
(synced to this box via git), find handoff rows that are ready to spawn but not
yet in-flight, and surface them via Telegram. You do NOT take action on them.

## How to run

Execute the bridge script. It auto-detects its environment:

```bash
python3 ~/.hermes/skills/vault-bridge/bridge.py
```

The script auto-detects the vault path and mode at startup:

1. `VAULT_BRIDGE_BASE` env var if set (explicit override), else
2. `/workspace/vault-second-brain` if it exists (container — sandbox mode), else
3. `/home/hermes/hermes-data/vault/second-brain` (host — host mode)

Mode is tied to the detected path:
- **sandbox** (container): read-only, no git pull (host cron syncs; deploy key
  not available per I23). Freshness = `.git/FETCH_HEAD` mtime, 7h threshold.
- **host**: git pull on stale. Freshness = commit age, 15min threshold.

Override with `VAULT_BRIDGE_BASE` and `VAULT_BRIDGE_MODE` env vars if needed.

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

5. **Read referenced handoff files** — for context on each queued row.

6. **Read event log** — last ~50 rows of `_meta/_event-log.md` for freshness.

7. **Output** — a formatted message listing ready rows (or "no new rows").

## What you do with the output

Send the script's stdout output verbatim as a Telegram message to the operator.
Relay the ENTIRE stdout block — it starts with 🔵 and contains the row list.
Do not summarize, paraphrase, or omit any part of it.

The action log (every file read, every operation) is written to
`/tmp/hermes-vault-bridge.log` — NOT to stderr or stdout. You do not need
to read or relay the log file. It exists for operator debugging only.

If the script exits with a stale-vault message, send that message instead.

## What you must NOT do

- Do NOT write any files (no outbox, no claim ledger, no status updates)
- Do NOT take autonomous action on any rows (no claiming, no spawning)
- Do NOT read files outside the script's built-in allowlist
- Do NOT modify the vault clone in any way (git pull is the only git operation)

These capabilities ship in future waves. This is Level 1: read and surface only.

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
| 0 | Success — message printed to stdout |
| 1 | Error — could not read required files |
| 2 | Stale vault — git pull failed, no data read |

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

### 2. Mount the vault clone into the container

Hermes runs skills inside a rootless-Docker sandbox. The vault clone lives on
the host at `/home/hermes/hermes-data/vault/second-brain/` but is NOT mounted
by default. The deploy key (`~/.ssh/hermes-vault-deploy-key`) must NOT be
mounted (I23 — keep secrets out of the container).

The container's workspace bind mount (`…/sandboxes/docker/default/workspace`
→ `/workspace`) inherits host bind mounts placed under the workspace source
directory. Use a systemd `.mount` unit to make it durable and ordered before
Hermes starts.

**Step 1 — Create the mount point:**
```bash
mkdir -p /home/hermes/.hermes/sandboxes/docker/default/workspace/vault-second-brain
```

**Step 2 — Create the systemd mount unit:**

Generate the correct unit filename on the box (don't hand-write it):
```bash
UNIT_NAME=$(systemd-escape -p --suffix=mount /home/hermes/.hermes/sandboxes/docker/default/workspace/vault-second-brain)
echo "Unit filename: $UNIT_NAME"
```

Then create the unit file:
```bash
cat > /etc/systemd/system/home-hermes-\\x2ehermes-sandboxes-docker-default-workspace-vault\\x2dsecond\\x2dbrain.mount << 'EOF'
[Unit]
Description=Vault clone bind mount for Hermes bridge skill
Before=hermes.service
After=local-fs.target

[Mount]
What=/home/hermes/hermes-data/vault/second-brain
Where=/home/hermes/.hermes/sandboxes/docker/default/workspace/vault-second-brain
Type=none
Options=bind,ro

[Install]
WantedBy=multi-user.target
EOF
```

**Step 3 — Enable and start:**
```bash
systemctl daemon-reload
systemctl enable --now home-hermes-\\x2ehermes-sandboxes-docker-default-workspace-vault\\x2dsecond\\x2dbrain.mount
```

**Step 4 — Verify:**
```bash
mount | grep vault-second-brain
ls /home/hermes/.hermes/sandboxes/docker/default/workspace/vault-second-brain/_meta/handoffs/_spawn-queue.md
```

In-container path: `/workspace/vault-second-brain`
Set `VAULT_BRIDGE_BASE=/workspace/vault-second-brain` in the run command.

**Note:** The container must be rebuilt after the mount is in place (Hermes
auto-rebuilds after ~5 min idle per `lifetime_seconds`, or force with
`docker rm` on the sandbox container). The deploy key stays on the host only
— never mounted into the container (I23).

### 3. Restart and verify

```bash
systemctl restart hermes
```

Verify the skill is discoverable by sending "run the vault bridge" via
Telegram. Live skill discovery does not depend on `.skills_prompt_snapshot.json`
(that file is a stale dump, not the live source).

## Troubleshooting

- **"Vault sync stale"** — the git pull failed. Check network connectivity
  and the deploy key at `~/.ssh/hermes-vault-deploy-key`.
- **"could not read spawn queue"** — the vault clone may be missing or
  corrupted. Check `/home/hermes/hermes-data/vault/second-brain/` exists.
- **Empty results** — all queued rows may already be in-flight. Check the
  active chats tracker.
- **Skill not in prompt snapshot** — the skill was placed but not registered.
  Restart Hermes (`systemctl restart hermes`). If still missing, investigate
  the local skill discovery mechanism.
