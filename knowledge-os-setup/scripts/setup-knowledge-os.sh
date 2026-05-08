#!/usr/bin/env bash
# Knowledge OS — vault scaffold installer
# Creates the directory structure, copies templates and seed notes, prepares the vault for Obsidian.
#
# Usage: ./setup-knowledge-os.sh <workspace-path> <skill-assets-path>
# Example: ./setup-knowledge-os.sh /Users/oliver/workspace /path/to/skill/assets
#
# Idempotent: safe to re-run. Will not overwrite existing files.

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <workspace-path> <skill-assets-path>"
  echo "  workspace-path: e.g. /Users/oliver/workspace"
  echo "  skill-assets-path: path to the skill's assets/ folder"
  exit 1
fi

WORKSPACE="$1"
ASSETS="$2"
VAULT="$WORKSPACE/second-brain"

if [ ! -d "$WORKSPACE" ]; then
  echo "ERROR: workspace path does not exist: $WORKSPACE"
  exit 1
fi

if [ ! -d "$ASSETS" ]; then
  echo "ERROR: skill assets path does not exist: $ASSETS"
  exit 1
fi

echo "→ Installing Knowledge OS into: $VAULT"
echo ""

# ---------- 1. Create vault directory structure ----------
echo "[1/6] Creating folder structure..."

# Top-level
for d in 00_inbox 01_ai-operating-system 02_core 03_domains 04_projects 05_shared-intelligence 99_archive _meta; do
  mkdir -p "$VAULT/$d"
done

# Inbox
for d in captures sources-pending decisions-pending; do
  mkdir -p "$VAULT/00_inbox/$d"
done

# Core
for d in thinking strategy abstractions principles; do
  mkdir -p "$VAULT/02_core/$d"
done

# Domains
for domain in automation-systems app-building video-intelligence content-systems client-services; do
  for sub in concepts artifacts execution validation insights; do
    mkdir -p "$VAULT/03_domains/$domain/$sub"
  done
done

# Projects
mkdir -p "$VAULT/04_projects/personal"
for d in _active _private _archive; do
  mkdir -p "$VAULT/04_projects/clients/$d"
done

# Shared intelligence
for d in patterns lessons blueprints tools workflows systems; do
  mkdir -p "$VAULT/05_shared-intelligence/$d"
done

# Meta
for d in templates scripts MOCs dashboards; do
  mkdir -p "$VAULT/_meta/$d"
done
for d in kos vis project; do
  mkdir -p "$VAULT/_meta/templates/$d"
done

echo "  ✓ folder structure created"

# ---------- 2. Copy templates ----------
echo "[2/6] Installing templates..."

copy_if_missing() {
  local src="$1"
  local dest="$2"
  if [ ! -f "$dest" ]; then
    cp "$src" "$dest"
    echo "  + $(basename "$dest")"
  else
    echo "  · $(basename "$dest") already exists, skipping"
  fi
}

for f in "$ASSETS/templates/kos"/*.md; do
  copy_if_missing "$f" "$VAULT/_meta/templates/kos/$(basename "$f")"
done

for f in "$ASSETS/templates/vis"/*.md; do
  copy_if_missing "$f" "$VAULT/_meta/templates/vis/$(basename "$f")"
done

for f in "$ASSETS/templates/project"/*.md; do
  copy_if_missing "$f" "$VAULT/_meta/templates/project/$(basename "$f")"
done

# ---------- 3. Install seed notes ----------
echo "[3/6] Installing seed notes (home, MOCs, workflows, conventions)..."

copy_if_missing "$ASSETS/seed-notes/_HOME.md" "$VAULT/_HOME.md"
copy_if_missing "$ASSETS/seed-notes/conventions.md" "$VAULT/_meta/conventions.md"
copy_if_missing "$ASSETS/seed-notes/obsidian-setup.md" "$VAULT/_meta/obsidian-setup.md"
copy_if_missing "$ASSETS/seed-notes/MOC-video-intelligence.md" "$VAULT/_meta/MOCs/MOC-video-intelligence.md"
copy_if_missing "$ASSETS/seed-notes/MOC-shared-intelligence.md" "$VAULT/_meta/MOCs/MOC-shared-intelligence.md"
copy_if_missing "$ASSETS/seed-notes/workflow-knowledge-promotion.md" "$VAULT/05_shared-intelligence/workflows/workflow-knowledge-promotion.md"
copy_if_missing "$ASSETS/seed-notes/workflow-video-extraction.md" "$VAULT/05_shared-intelligence/workflows/workflow-video-extraction.md"

# ---------- 4. Install sample notes (only if vault is empty otherwise) ----------
echo "[4/6] Installing sample notes for dashboard verification..."

copy_if_missing "$ASSETS/seed-notes/source-example-onboarding-agent.md" "$VAULT/03_domains/video-intelligence/insights/source-example-onboarding-agent.md"
copy_if_missing "$ASSETS/seed-notes/tactic-schema-first-agent-design.md" "$VAULT/03_domains/app-building/insights/tactic-schema-first-agent-design.md"
copy_if_missing "$ASSETS/seed-notes/opportunity-onboarding-agent-productized-service.md" "$VAULT/00_inbox/decisions-pending/opportunity-onboarding-agent-productized-service.md"

# ---------- 5. Migrate existing files (if any) ----------
echo "[5/6] Checking for existing AI OS files to relocate..."

# Move existing top-level docs into 01_ai-operating-system if they're loose
EXISTING="$WORKSPACE/second-brain/01_ai-operating-system"
if [ -d "$EXISTING" ]; then
  echo "  · existing 01_ai-operating-system folder detected — leaving in place"
else
  echo "  · no existing AI OS folder — fresh install"
fi

# ---------- 6. .obsidian config hint ----------
echo "[6/6] Creating .obsidian placeholder hint..."

if [ ! -d "$VAULT/.obsidian" ]; then
  mkdir -p "$VAULT/.obsidian"
  cat > "$VAULT/.obsidian/README.md" << 'EOF'
This folder will be populated by Obsidian when the vault is opened for the first time.

After opening:
1. Install the four required plugins (Templater, Dataview, QuickAdd, Omnisearch)
2. Configure them per ../_meta/obsidian-setup.md
3. Open _HOME.md and verify all dashboard queries render

If queries don't render, check that Dataview is enabled and that JavaScript queries are turned on in Dataview settings.
EOF
fi

echo ""
echo "✅ Knowledge OS installed at: $VAULT"
echo ""
echo "Next steps:"
echo "  1. Open Obsidian"
echo "  2. 'Open folder as vault' → select $VAULT"
echo "  3. Install plugins: Templater, Dataview, QuickAdd, Omnisearch"
echo "  4. Follow setup guide at $VAULT/_meta/obsidian-setup.md"
echo "  5. Open _HOME.md to verify the dashboard renders"
echo ""
