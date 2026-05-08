#!/usr/bin/env bash
# Initialize a project vault: creates .kos/ inside a repo and symlinks it into second-brain.
#
# Usage: ./init-project-vault.sh <repo-path> <project-area> <vault-root> <skill-assets-path> [fork-from]
#   repo-path:        e.g. /Users/oliver/workspace/repos/resume-saas
#   project-area:     personal | clients | clients-private
#   vault-root:       e.g. /Users/oliver/workspace/second-brain
#   skill-assets-path: path to skill assets/ folder
#   fork-from:        optional. Name of a prior project to copy specs/ and lessons/ from.
#                     If omitted and stdin is a terminal, you'll be prompted.
#                     scopes/ and execution-logs/ are deliberately not copied.
#
# Idempotent. Safe to re-run.

set -euo pipefail

if [ $# -lt 4 ]; then
  echo "Usage: $0 <repo-path> <project-area> <vault-root> <skill-assets-path> [fork-from]"
  echo "  project-area:  personal | clients | clients-private"
  echo "  fork-from:     optional. Name of a prior project to copy specs/ and lessons/ from."
  exit 1
fi

REPO="$1"
AREA="$2"
VAULT="$3"
ASSETS="$4"
FORK_FROM="${5:-}"

if [ ! -d "$REPO" ]; then
  echo "ERROR: repo path does not exist: $REPO"
  exit 1
fi

if [ "$AREA" != "personal" ] && [ "$AREA" != "clients" ] && [ "$AREA" != "clients-private" ]; then
  echo "ERROR: project-area must be 'personal', 'clients', or 'clients-private'"
  exit 1
fi

# Interactive prompt for fork-from if not supplied and stdin is a TTY
if [ -z "$FORK_FROM" ] && [ -t 0 ]; then
  read -r -p "Fork specs/ and lessons/ from a prior project? (project name, or Enter to skip): " FORK_FROM
fi

PROJECT_NAME=$(basename "$REPO")
KOS_DIR="$REPO/.kos"

# Self-fork check
if [ -n "$FORK_FROM" ] && [ "$FORK_FROM" = "$PROJECT_NAME" ]; then
  echo "ERROR: cannot fork-from self ($PROJECT_NAME)"
  exit 1
fi

echo "→ Initializing project vault for: $PROJECT_NAME"

# Create .kos/ structure in repo
echo "[1/4] Creating .kos/ structure..."
TODAY=$(date +%Y-%m-%d)
for d in specs scopes execution-logs lessons; do
  mkdir -p "$KOS_DIR/$d"
done

# Install README and vault-config from templates if they don't exist
if [ ! -f "$KOS_DIR/README.md" ]; then
  cp "$ASSETS/templates/project/template-project-readme.md" "$KOS_DIR/README.md"
  # Substitute Templater placeholders + populate project-name field at copy time.
  # Avoids depending on Obsidian Templater, which can contaminate when multiple
  # files land in the vault simultaneously via symlinks (tp.file.folder() races).
  sed \
    -e "s|<% tp\\.file\\.folder() %>|$PROJECT_NAME|g" \
    -e "s|<% tp\\.date\\.now(\"YYYY-MM-DD\") %>|$TODAY|g" \
    -e "s|^project-name: \"\"$|project-name: $PROJECT_NAME|" \
    "$KOS_DIR/README.md" > "$KOS_DIR/README.md.tmp"
  mv "$KOS_DIR/README.md.tmp" "$KOS_DIR/README.md"
  echo "  + README.md (from template, placeholders substituted)"
else
  echo "  · README.md exists, skipping"
fi

if [ ! -f "$KOS_DIR/.vault-config.md" ]; then
  cp "$ASSETS/templates/project/template-vault-config.md" "$KOS_DIR/.vault-config.md"
  # Substitute Templater date placeholder + fill [name] manual placeholder.
  sed \
    -e "s|<% tp\\.date\\.now(\"YYYY-MM-DD\") %>|$TODAY|g" \
    -e "s|^\\[name\\]$|$PROJECT_NAME|" \
    "$KOS_DIR/.vault-config.md" > "$KOS_DIR/.vault-config.md.tmp"
  mv "$KOS_DIR/.vault-config.md.tmp" "$KOS_DIR/.vault-config.md"
  echo "  + .vault-config.md (from template, placeholders substituted)"
else
  echo "  · .vault-config.md exists, skipping"
fi

# Defensive: warn if any Templater placeholders survived substitution.
# Future template additions that introduce new <% ... %> tags should fail here
# rather than silently propagating contamination.
for f in "$KOS_DIR/README.md" "$KOS_DIR/.vault-config.md"; do
  if [ -f "$f" ] && grep -q '<%[^%]*%>' "$f" 2>/dev/null; then
    echo "  ! WARNING: unsubstituted Templater placeholders remain in $(basename "$f"):"
    grep -n '<%[^%]*%>' "$f" | sed 's/^/      /'
  fi
done

# Optional fork-from: copy specs/ and lessons/ from a prior project
echo "[2/4] Fork-from..."
if [ -z "$FORK_FROM" ] || [ "$FORK_FROM" = "no" ] || [ "$FORK_FROM" = "none" ]; then
  echo "  · no fork-from specified, skipping"
else
  echo "  Looking for prior project: $FORK_FROM"

  SOURCE_KOS=""
  for candidate in "$VAULT/04_projects/personal/$FORK_FROM" \
                   "$VAULT/04_projects/clients/_active/$FORK_FROM" \
                   "$VAULT/04_projects/clients/_private/$FORK_FROM"; do
    if [ -d "$candidate" ]; then
      # Resolve symlinks to physical path (handles both symlinked .kos/ and direct dirs)
      SOURCE_KOS=$(cd "$candidate" && pwd -P)
      echo "  Found at: $candidate → $SOURCE_KOS"
      break
    fi
  done

  if [ -z "$SOURCE_KOS" ]; then
    echo "  ! WARNING: prior project '$FORK_FROM' not found in vault. Skipping fork-from."
    echo "    Searched: 04_projects/{personal,clients/_active,clients/_private}/$FORK_FROM"
    echo "    Continuing without fork. You can manually copy files later."
  else
    # Copy specs/
    if [ -d "$SOURCE_KOS/specs" ] && [ -n "$(ls -A "$SOURCE_KOS/specs" 2>/dev/null)" ]; then
      cp -R "$SOURCE_KOS/specs/." "$KOS_DIR/specs/"
      COUNT=$(find "$SOURCE_KOS/specs" -maxdepth 1 -type f | wc -l | tr -d ' ')
      echo "  + Copied $COUNT file(s) from specs/"
    else
      echo "  · source specs/ is empty or missing, nothing to copy"
    fi

    # Copy lessons/
    if [ -d "$SOURCE_KOS/lessons" ] && [ -n "$(ls -A "$SOURCE_KOS/lessons" 2>/dev/null)" ]; then
      cp -R "$SOURCE_KOS/lessons/." "$KOS_DIR/lessons/"
      COUNT=$(find "$SOURCE_KOS/lessons" -maxdepth 1 -type f | wc -l | tr -d ' ')
      echo "  + Copied $COUNT file(s) from lessons/"
    else
      echo "  · source lessons/ is empty or missing, nothing to copy"
    fi

    echo "  Review and edit/delete copied files as appropriate. Files were copied (not symlinked)."
  fi
fi

# Create symlink in second-brain
echo "[3/4] Creating symlink in second-brain..."

if [ "$AREA" = "personal" ]; then
  LINK_DIR="$VAULT/04_projects/personal"
elif [ "$AREA" = "clients" ]; then
  LINK_DIR="$VAULT/04_projects/clients/_active"
else  # clients-private
  LINK_DIR="$VAULT/04_projects/clients/_private"
fi

LINK_PATH="$LINK_DIR/$PROJECT_NAME"

# Compute relative symlink target so the link is portable across mount points
# (e.g. host /Users/oliver/workspace/ vs Cowork sandbox /sessions/.../mnt/workspace/).
# Assumes repos/ and second-brain/ are siblings under the same workspace root.
#   personal:         <vault>/04_projects/personal/<name>          → ../../../repos/<name>/.kos
#   clients/_active:  <vault>/04_projects/clients/_active/<name>   → ../../../../repos/<name>/.kos
#   clients/_private: same as _active (one extra level deeper than personal)
if [ "$AREA" = "personal" ]; then
  REL_TARGET="../../../repos/$PROJECT_NAME/.kos"
else
  REL_TARGET="../../../../repos/$PROJECT_NAME/.kos"
fi

if [ -L "$LINK_PATH" ]; then
  echo "  · symlink exists, skipping: $LINK_PATH"
elif [ -e "$LINK_PATH" ]; then
  echo "  ! WARNING: $LINK_PATH exists but is not a symlink. Aborting."
  exit 1
else
  ln -s "$REL_TARGET" "$LINK_PATH"
  echo "  + symlink: $LINK_PATH → $REL_TARGET"
fi

echo "[4/4] Done."
echo ""
echo "✅ Project vault initialized for: $PROJECT_NAME"
echo "  - Repo .kos/: $KOS_DIR"
echo "  - Vault link: $LINK_PATH"
echo ""
echo "Next steps:"
echo "  1. Edit $KOS_DIR/README.md to fill in project details"
echo "  2. Edit $KOS_DIR/.vault-config.md to set agent context"
echo "  3. Open the project in Obsidian under 04_projects/"
echo ""
