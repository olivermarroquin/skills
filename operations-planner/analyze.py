#!/usr/bin/env python3
"""
operations-planner analyze.py — the chief-of-operations brain.

Walks the handoff tree, builds the reverse-dependency graph, computes
gate-opening leverage scores, and emits an operations_plan JSON + human-readable
summary.

Composition contract (honest scoping):
- Reimplements weighted-sum scoring inline (prioritization skill is markdown spec,
  not a callable module). Profile shape matches references/operations-planner-profile.md.
- Reads edit-zone conflict tables from cluster _README.md files (pre-authored human
  judgments). Does NOT reimplement vault-orchestrator's severity-scoring algorithm.
- Reimplements the blocker-cleared check (set-membership test on depends_on vs done
  column). Does NOT reimplement multi-chat-coordination's six-factor evaluation.

Usage:
    python3 analyze.py [--handoffs-dir PATH] [--output-dir PATH] [--verbose]
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# YAML parsing — use PyYAML if available, else a minimal regex parser
# ---------------------------------------------------------------------------

try:
    import yaml
    def parse_frontmatter(text: str) -> dict | None:
        m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
        if not m:
            return None
        try:
            return yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            return None
except ImportError:
    def parse_frontmatter(text: str) -> dict | None:
        m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
        if not m:
            return None
        fm = {}
        for line in m.group(1).split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            colon = line.find(':')
            if colon == -1:
                continue
            key = line[:colon].strip()
            val = line[colon+1:].strip().strip("'\"")
            # Handle YAML lists: [a, b, c]
            if val.startswith('[') and val.endswith(']'):
                val = [v.strip().strip("'\"") for v in val[1:-1].split(',') if v.strip()]
            fm[key] = val
        return fm


# ---------------------------------------------------------------------------
# Status normalization
# ---------------------------------------------------------------------------

STATUS_TO_COLUMN = {
    'consumed':          'done',
    'shipped':           'done',
    'complete':          'done',
    'promoted':          'done',
    'locked':            'done',
    'staging-complete':  'done',
    'cancelled':         'done',
    'superseded':        'done',
    'phase-1-consumed':  'done',
    'open':              'in_flight',
    'submitted':         'in_flight',
    'active-with-wf4':   'in_flight',
    'queued':            'queued',
    'draft':             'queued',
    'draft-for-build':   'queued',
    'stub':              'queued',
    'ready':             'next',
    'ready-to-spawn':    'next',
}

# 'active' is context-dependent — resolved via tracker cross-reference


def normalize_status(raw_status: str, tracker_state: dict, file_stem: str) -> str:
    """Normalize a raw status string to a canonical column.

    Tracker state OVERRIDES frontmatter for non-done statuses — handoff
    frontmatter often says 'queued' or 'active' even when the tracker has
    moved the row to Active/in-flight or Ready-to-spawn. The tracker is
    the canonical runtime state; frontmatter is the authored state.
    """
    # Tracker override: if the tracker has an opinion, it wins for non-done statuses
    tracker_col = tracker_state.get(file_stem)
    if tracker_col:
        return tracker_col

    raw = raw_status.lower().strip()
    if raw in STATUS_TO_COLUMN:
        return STATUS_TO_COLUMN[raw]
    if raw == 'active':
        return 'in_flight'  # active = work is live; default to in_flight
    return '__unmapped__'


# ---------------------------------------------------------------------------
# Tag extraction — extract [TAG] identifiers from handoff titles/tags
# ---------------------------------------------------------------------------

TAG_BRACKET_PATTERN = re.compile(r'\[([A-Z]{1,5}-?\d{1,3}[A-Za-z]?)\]')
# Also match "DA1:", "RQ2:", "WF-7:" etc. without brackets in titles
TAG_COLON_PATTERN = re.compile(r'(?:^|—\s*)([A-Z]{1,5}-?\d{1,3}[A-Za-z]?)\s*[:—]')

def extract_tag(fm: dict, body: str, filename: str) -> str | None:
    """Extract a tag like [OP-1], [MI-3], DA1 from the handoff."""
    # Try tags list first
    tags = fm.get('tags', [])
    if isinstance(tags, list):
        tag_from_list = extract_tag_from_tags_list(tags)
        if tag_from_list:
            return tag_from_list
    # Try H1 title — bracket form first
    for line in body.split('\n')[:10]:
        if line.startswith('# '):
            m = TAG_BRACKET_PATTERN.search(line)
            if m:
                return m.group(1)
            # Try colon form: "DA1:" or "— DA1:"
            m = TAG_COLON_PATTERN.search(line)
            if m:
                return m.group(1)
    # Try filename
    m = TAG_BRACKET_PATTERN.search(filename)
    if m:
        return m.group(1)
    return None


def extract_tag_from_tags_list(tags: list) -> str | None:
    """Look for tag IDs like op-1, mi-3, da1, rgh-6 in the tags list."""
    tag_id_pattern = re.compile(r'^([a-z]{1,5}-?\d{1,3}[a-z]?)$', re.IGNORECASE)
    for t in tags:
        if isinstance(t, str) and tag_id_pattern.match(t):
            return t.upper()
    return None


# ---------------------------------------------------------------------------
# Effort parsing
# ---------------------------------------------------------------------------

EFFORT_PATTERN = re.compile(r'~?(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(?:h|hours?)?', re.IGNORECASE)
EFFORT_SINGLE = re.compile(r'~?(\d+(?:\.\d+)?)\s*(?:h|hours?)', re.IGNORECASE)

def parse_effort(body: str, fm: dict) -> float:
    """Extract estimated effort hours (midpoint). Default 4.0."""
    # Check body for "Estimated effort" or "Operator-time" sections
    for line in body.split('\n'):
        if any(k in line.lower() for k in ['estimated effort', 'operator-time', 'estimated build time']):
            m = EFFORT_PATTERN.search(line)
            if m:
                return (float(m.group(1)) + float(m.group(2))) / 2.0
            m = EFFORT_SINGLE.search(line)
            if m:
                return float(m.group(1))
    return 4.0  # default median


# ---------------------------------------------------------------------------
# Dependency resolution
# ---------------------------------------------------------------------------

def build_dependency_slug_index(all_nodes: dict) -> dict:
    """Build a lookup from various slug forms to canonical node IDs."""
    index = {}
    for node_id, node in all_nodes.items():
        stem = node['file_stem']
        index[stem] = node_id
        index[stem + '.md'] = node_id
        # Short forms: strip 'handoff-YYYY-MM-DD-' prefix
        short = re.sub(r'^handoff-\d{4}-\d{2}-\d{2}-', '', stem)
        index[short] = node_id
        # Phase forms: 'phase-N-slug'
        if stem.startswith('phase-'):
            index[stem] = node_id
        # Tag-based: if node has a tag like OP-1, index by that too
        if node.get('tag'):
            index[node['tag'].lower()] = node_id
            index[node['tag']] = node_id
        # Program-based short refs: e.g., "wf7-data-model-spec" for WF7
        program = node.get('program', '')
        if program:
            # Create slug from tag + key words in the short form
            tag = node.get('tag', '')
            if tag:
                index[tag.lower() + '-' + short.split('-', 1)[-1] if '-' in short else short] = node_id
    return index


def resolve_dependency(dep_ref: str, slug_index: dict) -> str | None:
    """Resolve a depends-on reference to a canonical node ID."""
    dep_ref = dep_ref.strip().strip("'\"")
    # Strip parenthetical annotations like "(already cleared 2026-06-01)"
    dep_ref = re.sub(r'\s*\(.*?\)\s*$', '', dep_ref).strip()
    # Strip .md extension for matching
    bare = dep_ref.replace('.md', '')
    # Try exact match
    if dep_ref in slug_index:
        return slug_index[dep_ref]
    if bare in slug_index:
        return slug_index[bare]
    # Try lowercase
    if dep_ref.lower() in slug_index:
        return slug_index[dep_ref.lower()]
    if bare.lower() in slug_index:
        return slug_index[bare.lower()]
    # Try partial match — find keys that end with the reference
    for key, node_id in slug_index.items():
        if key.endswith(bare) or key.endswith(bare.lower()):
            return node_id
    # Try substring containment — the ref is a short slug that appears inside a key
    bare_lower = bare.lower()
    if bare_lower != 'none':  # skip literal "none"
        for key, node_id in slug_index.items():
            if bare_lower in key.lower() and len(bare_lower) > 5:
                return node_id
    return None


# ---------------------------------------------------------------------------
# Leverage scoring — the net-new computation
# ---------------------------------------------------------------------------

def compute_leverage_scores(nodes: dict, reverse_graph: dict) -> dict:
    """
    Compute gate-opening leverage for each node.

    leverage_score = sum(1 / (1 + depth)) for each transitive downstream node.
    Depth 0 = direct unblock (weight 1.0), depth 1 = weight 0.5, etc.
    """
    scores = {}
    for node_id in nodes:
        score = _traverse_downstream(node_id, reverse_graph, set(), 0)
        scores[node_id] = round(score, 3)
    return scores


def _traverse_downstream(node_id: str, reverse_graph: dict, visited: set, depth: int) -> float:
    """BFS/DFS downstream traversal with depth decay."""
    total = 0.0
    for child_id in reverse_graph.get(node_id, []):
        if child_id in visited:
            continue
        visited.add(child_id)
        total += 1.0 / (1.0 + depth)
        total += _traverse_downstream(child_id, reverse_graph, visited, depth + 1)
    return total


# ---------------------------------------------------------------------------
# Cycle detection
# ---------------------------------------------------------------------------

def detect_cycles(forward_graph: dict) -> list:
    """Detect cycles via DFS. Returns list of cycle paths."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    cycles = []
    path = []

    def dfs(node):
        color[node] = GRAY
        path.append(node)
        for neighbor in forward_graph.get(node, []):
            if color[neighbor] == GRAY:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
            elif color[neighbor] == WHITE:
                dfs(neighbor)
        path.pop()
        color[node] = BLACK

    all_nodes = set(forward_graph.keys())
    for vals in forward_graph.values():
        all_nodes.update(vals)
    for node in all_nodes:
        if color[node] == WHITE:
            dfs(node)

    return cycles


# ---------------------------------------------------------------------------
# Critical path — longest dependency chain
# ---------------------------------------------------------------------------

def compute_critical_path(forward_graph: dict, nodes: dict) -> list:
    """Find the longest dependency chain by node count."""
    memo = {}

    def longest_from(node_id):
        if node_id in memo:
            return memo[node_id]
        deps = forward_graph.get(node_id, [])
        if not deps:
            memo[node_id] = [node_id]
            return memo[node_id]
        best = []
        for dep in deps:
            chain = longest_from(dep)
            if len(chain) > len(best):
                best = chain
        memo[node_id] = best + [node_id]
        return memo[node_id]

    longest = []
    for node_id in nodes:
        chain = longest_from(node_id)
        if len(chain) > len(longest):
            longest = chain
    return longest


# ---------------------------------------------------------------------------
# Edit-zone conflict parsing from cluster _README.md files
# ---------------------------------------------------------------------------

def parse_edit_zone_tables(handoffs_dir: Path) -> dict:
    """
    Read edit-zone conflict tables from cluster _README.md files.
    Returns {(node_a, node_b): severity} pairs.
    """
    conflicts = {}
    for readme_path in handoffs_dir.glob('*/_README.md'):
        try:
            text = readme_path.read_text(encoding='utf-8')
        except Exception:
            continue
        # Find the edit-zone conflicts table
        in_table = False
        for line in text.split('\n'):
            if '## Edit-zone conflicts' in line or '## Edit-zone' in line:
                in_table = True
                continue
            if in_table and line.startswith('## '):
                break
            if in_table and '|' in line and '---' not in line and 'Pair' not in line:
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if len(cells) >= 3:
                    pair_text = cells[0]
                    severity = cells[2].lower() if len(cells) > 2 else 'unknown'
                    # Extract tag pairs like [OP-1] ↔ [OP-2]
                    tags = TAG_BRACKET_PATTERN.findall(pair_text)
                    if len(tags) >= 2:
                        conflicts[(tags[0], tags[1])] = severity
    return conflicts


# ---------------------------------------------------------------------------
# Parallel group computation
# ---------------------------------------------------------------------------

def compute_parallel_groups(ready_nodes: list, edit_zone_conflicts: dict) -> list:
    """
    Group ready nodes into parallel-safe sets.
    Two nodes are parallel-safe if they have no serial-required edit-zone conflict.
    """
    # Build adjacency for serial conflicts
    serial_pairs = set()
    for (a, b), severity in edit_zone_conflicts.items():
        if 'serial' in severity:
            serial_pairs.add((a, b))
            serial_pairs.add((b, a))

    groups = []
    assigned = set()

    for node in ready_nodes:
        tag = node.get('tag', '')
        if tag in assigned:
            continue
        group = [node]
        assigned.add(tag)
        for other in ready_nodes:
            other_tag = other.get('tag', '')
            if other_tag in assigned:
                continue
            # Check if other conflicts with any node already in the group
            conflicts = False
            for g in group:
                g_tag = g.get('tag', '')
                if (g_tag, other_tag) in serial_pairs or (other_tag, g_tag) in serial_pairs:
                    conflicts = True
                    break
            if not conflicts:
                group.append(other)
                assigned.add(other_tag)
        groups.append(group)

    return groups


# ---------------------------------------------------------------------------
# Weighted-sum scoring (reimplements prioritization inline)
# ---------------------------------------------------------------------------

WEIGHTS = {
    'gate_opening_leverage': 0.40,
    'effort_hours':          0.20,
    'reuse_multiplier':      0.15,
    'operator_priority':     0.25,
}

def estimate_reuse(node: dict) -> int:
    """Heuristic: 1-5 reuse multiplier from tags and body signals."""
    tags = node.get('tags', [])
    if not isinstance(tags, list):
        tags = []
    tag_set = set(t.lower() for t in tags if isinstance(t, str))

    score = 1
    if any(k in tag_set for k in ['engine', 'skill-build', 'agnostic', 'reusable', 'infrastructure']):
        score += 2
    if any(k in tag_set for k in ['compose-dont-duplicate', 'cross-project']):
        score += 1
    if 'client-work' in tag_set or node.get('client'):
        score = max(score, 2)  # client work has some reuse across clients
    return min(score, 5)


def estimate_operator_priority(node: dict) -> int:
    """Heuristic: 1-5 from priority field and program signals."""
    priority = node.get('priority', '')
    if isinstance(priority, str):
        priority = priority.lower()
    if priority == 'high':
        return 4
    if priority == 'critical':
        return 5
    if priority == 'medium' or priority == 'med':
        return 3
    if priority == 'low':
        return 2
    return 2  # default: no strong signal


def weighted_sum_score(leverage: float, effort: float, reuse: int, priority: int,
                       all_leverages: list, all_efforts: list) -> float:
    """Compute weighted sum with min-max normalization."""
    def normalize(val, vals, lower_is_better=False):
        mn, mx = min(vals), max(vals)
        if mx == mn:
            return 0.5
        normed = (val - mn) / (mx - mn)
        return 1.0 - normed if lower_is_better else normed

    norm_leverage = normalize(leverage, all_leverages)
    norm_effort = normalize(effort, all_efforts, lower_is_better=True)
    norm_reuse = normalize(reuse, [1, 5])
    norm_priority = normalize(priority, [1, 5])

    return round(
        WEIGHTS['gate_opening_leverage'] * norm_leverage +
        WEIGHTS['effort_hours'] * norm_effort +
        WEIGHTS['reuse_multiplier'] * norm_reuse +
        WEIGHTS['operator_priority'] * norm_priority,
        3
    )


# ---------------------------------------------------------------------------
# Tracker cross-reference — determine which handoffs are in which section
# ---------------------------------------------------------------------------

def parse_tracker_state(handoffs_dir: Path) -> dict:
    """
    Parse _active-chats-tracker.md AND _recently-closed.md to determine which
    handoffs are in_flight vs next vs queued vs done. Returns {file_stem: column}.

    _recently-closed.md holds rows that shipped — these map to 'done'.
    Without this, handoffs with status: active whose tracker row moved to
    _recently-closed would fall through to 'queued' (false ready_now).
    """
    state = {}

    # Parse _recently-closed.md first — all wikilinks there map to 'done'
    closed_path = handoffs_dir / '_recently-closed.md'
    if closed_path.exists():
        try:
            closed_text = closed_path.read_text(encoding='utf-8')
            for m in re.finditer(r'\[\[([^\]]+?)\]\]', closed_text):
                raw = m.group(1)
                ref = re.split(r'\\?\|', raw)[0].strip()
                stem = ref.split('/')[-1].replace('.md', '')
                if stem and not stem.startswith('_'):
                    state[stem] = 'done'
        except Exception:
            pass

    # Parse the main tracker
    tracker_path = handoffs_dir / '_active-chats-tracker.md'
    if not tracker_path.exists():
        return state

    try:
        text = tracker_path.read_text(encoding='utf-8')
    except Exception:
        return state

    current_section = None
    section_map = {
        'active / in-flight': 'in_flight',
        'in-flight chats': 'in_flight',
        'ready to spawn': 'next',
        'queued — tier 2': 'queued',
        'queued — tier 3': 'queued',
    }

    for line in text.split('\n'):
        lower = line.lower().strip()
        # Detect section headers
        if lower.startswith('## ') or lower.startswith('> [!'):
            for key, col in section_map.items():
                if key in lower:
                    current_section = col
                    break

        # Extract handoff references from table rows
        if current_section and '[[' in line:
            # Find wikilink targets — handle both [[target|label]] and [[target\|label]]
            for m in re.finditer(r'\[\[([^\]]+?)\]\]', line):
                raw = m.group(1)
                # Split on | or \| to get just the target
                ref = re.split(r'\\?\|', raw)[0].strip()
                # Normalize: strip path prefix, get stem
                stem = ref.split('/')[-1].replace('.md', '')
                state[stem] = current_section

    return state


# ---------------------------------------------------------------------------
# Main: walk tree, build graph, compute plan
# ---------------------------------------------------------------------------

def walk_handoff_tree(handoffs_dir: Path, tracker_state: dict, verbose: bool = False):
    """Walk the handoff tree and build handoff_node objects."""
    nodes = {}
    unmapped_statuses = []

    for md_path in sorted(handoffs_dir.rglob('*.md')):
        # Skip underscore-prefixed files (_README, _active-chats-tracker, etc.)
        if md_path.name.startswith('_'):
            continue
        # Skip non-handoff reference/prototype/execution-log/strategic files
        if any(md_path.name.startswith(p) for p in ['prototype-', 'reference-', 'spec-', 'sop-']):
            continue

        try:
            text = md_path.read_text(encoding='utf-8')
        except Exception:
            continue

        fm = parse_frontmatter(text)
        if not fm:
            continue

        # Only process type: handoff
        if fm.get('type') != 'handoff':
            continue

        file_stem = md_path.stem
        rel_path = str(md_path.relative_to(handoffs_dir))

        # Determine cluster from parent dir
        parent = md_path.parent
        if parent == handoffs_dir:
            cluster = '_root'
        else:
            cluster = parent.name

        # Extract tag ID
        body = text.split('---', 2)[-1] if text.count('---') >= 2 else text
        tag = extract_tag(fm, body, md_path.name)
        # Fallback: check tags list for tag IDs
        if not tag:
            tags_list = fm.get('tags', [])
            if isinstance(tags_list, list):
                tag = extract_tag_from_tags_list(tags_list)

        # Parse depends-on
        depends_on_raw = fm.get('depends-on', [])
        if isinstance(depends_on_raw, str):
            depends_on_raw = [d.strip() for d in depends_on_raw.split(',') if d.strip()]
        elif not isinstance(depends_on_raw, list):
            depends_on_raw = []

        # Normalize status
        raw_status = str(fm.get('status', 'queued')).lower().strip()
        column = normalize_status(raw_status, tracker_state, file_stem)
        if column == '__unmapped__':
            unmapped_statuses.append({'file': rel_path, 'status': raw_status})
            column = 'queued'  # safe default

        # Extract effort
        effort = parse_effort(body, fm)

        # Build node
        node_id = file_stem
        title = ''
        for line in body.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()
                break
        if not title:
            title = file_stem

        # Make display_id unique and human-readable
        if tag:
            # Prefix generic PHASE-N with cluster to disambiguate
            display_id = f"{cluster}/{tag}" if tag.startswith('PHASE-') and cluster != '_root' else tag
        else:
            # No tag — use a shortened file stem (strip handoff-YYYY-MM-DD- prefix)
            display_id = re.sub(r'^handoff-\d{4}-\d{2}-\d{2}-', '', file_stem)

        nodes[node_id] = {
            'id': display_id,
            'file_stem': file_stem,
            'rel_path': rel_path,
            'cluster': cluster,
            'title': title,
            'status_raw': raw_status,
            'column': column,
            'depends_on_raw': depends_on_raw,
            'depends_on': [],       # resolved in next pass
            'unblocks': [],         # populated by graph inversion
            'tag': tag,
            'substrate': fm.get('substrate', fm.get('preferred-substrate', 'unknown')),
            'effort_hours': effort,
            'tags': fm.get('tags', []),
            'priority': fm.get('priority', ''),
            'client': fm.get('client', ''),
            'program': fm.get('program', ''),
        }

        if verbose:
            print(f"  [{tag or '???'}] {file_stem} → {column} (deps: {depends_on_raw})")

    # Post-walk fixup: scan _recently-closed.md for wikilink references to
    # handoff files and override matching nodes to 'done'. This catches
    # handoffs whose tracker row moved to _recently-closed but whose
    # frontmatter still says 'active'.
    closed_path = handoffs_dir / '_recently-closed.md'
    if closed_path.exists():
        try:
            closed_text = closed_path.read_text(encoding='utf-8')

            # Collect wikilink stems from _recently-closed — these are reliable
            closed_stems = set()
            for m in re.finditer(r'\[\[([^\]]+?)\]\]', closed_text):
                raw = m.group(1)
                ref = re.split(r'\\?\|', raw)[0].strip()
                stem = ref.split('/')[-1].replace('.md', '')
                if stem and not stem.startswith('_'):
                    closed_stems.add(stem)

            # Also collect bracket tags, but only match nodes whose extracted
            # tag is an exact match (non-generic tags like DA5, not PHASE-1)
            closed_tags = set(TAG_BRACKET_PATTERN.findall(closed_text))

            for node_id, node in nodes.items():
                if node['column'] == 'done':
                    continue
                # Match by wikilink stem (highest confidence)
                if node['file_stem'] in closed_stems:
                    if verbose:
                        print(f"  ★ Overriding [{node.get('tag') or node_id}] → done (wikilink in _recently-closed)")
                    node['column'] = 'done'
                    continue
                # Match by exact tag, but ONLY for non-generic tags
                # (skip PHASE-N, WAVE-N, CORE-30 etc. which collide across clusters)
                tag = node['tag']
                if tag and tag in closed_tags:
                    if not re.match(r'^(PHASE|WAVE|CORE|SPLIT|TIER|LEVEL)-', tag):
                        if verbose:
                            print(f"  ★ Overriding [{tag}] → done (tag in _recently-closed)")
                        node['column'] = 'done'
        except Exception:
            pass

    return nodes, unmapped_statuses


def build_graph(nodes: dict, verbose: bool = False):
    """Resolve dependencies and build forward + reverse graphs."""
    slug_index = build_dependency_slug_index(nodes)
    forward_graph = defaultdict(list)  # node → its dependencies
    reverse_graph = defaultdict(list)  # node → what it unblocks
    unresolved_deps = []

    for node_id, node in nodes.items():
        resolved = []
        for dep_ref in node['depends_on_raw']:
            target = resolve_dependency(dep_ref, slug_index)
            if target:
                resolved.append(target)
                forward_graph[node_id].append(target)
                reverse_graph[target].append(node_id)
            else:
                unresolved_deps.append({
                    'node': node_id,
                    'tag': node.get('tag'),
                    'unresolved_ref': dep_ref,
                })
                if verbose:
                    print(f"  ⚠ Unresolved dep: {node_id} → {dep_ref}")
        node['depends_on'] = resolved

    return dict(forward_graph), dict(reverse_graph), unresolved_deps


def generate_plan(nodes: dict, forward_graph: dict, reverse_graph: dict,
                  leverage_scores: dict, edit_zone_conflicts: dict,
                  unmapped_statuses: list, unresolved_deps: list,
                  cycles: list, critical_path: list) -> dict:
    """Generate the operations_plan object per the data contract."""

    # Populate unblocks on each node
    for node_id, node in nodes.items():
        node['unblocks'] = reverse_graph.get(node_id, [])
        node['leverage_score'] = leverage_scores.get(node_id, 0.0)

    # Classify nodes
    ready_now = []
    waiting_on = {}
    in_flight = []
    done_nodes = []

    for node_id, node in nodes.items():
        col = node['column']
        if col == 'done':
            done_nodes.append(node_id)
            continue
        if col == 'in_flight':
            in_flight.append(node_id)
            continue

        # Check if all dependencies are done
        deps = node['depends_on']
        if not deps:
            # No dependencies — ready if not done/in_flight
            ready_now.append(node)
        else:
            all_done = all(
                nodes.get(d, {}).get('column') == 'done'
                for d in deps
            )
            if all_done:
                ready_now.append(node)
            else:
                blockers = [
                    d for d in deps
                    if nodes.get(d, {}).get('column') != 'done'
                ]
                blocker_labels = []
                for b in blockers:
                    bn = nodes.get(b, {})
                    tag = bn.get('tag', b)
                    col = bn.get('column', 'unknown')
                    blocker_labels.append(f"{tag} ({col})")
                waiting_on[node_id] = blocker_labels

    # Score ready nodes
    all_leverages = [n['leverage_score'] for n in ready_now] or [0]
    all_efforts = [n['effort_hours'] for n in ready_now] or [4]

    for node in ready_now:
        node['reuse_multiplier'] = estimate_reuse(node)
        node['operator_priority_score'] = estimate_operator_priority(node)
        node['weighted_score'] = weighted_sum_score(
            node['leverage_score'], node['effort_hours'],
            node['reuse_multiplier'], node['operator_priority_score'],
            all_leverages, all_efforts,
        )

    # Sort by weighted score descending
    ready_now.sort(key=lambda n: n['weighted_score'], reverse=True)

    # Compute parallel groups from ready nodes
    parallel_sets = compute_parallel_groups(ready_now, edit_zone_conflicts)

    # Session budget
    total_hours = sum(n['effort_hours'] for n in ready_now)
    fatigue_flag = total_hours > 40  # more than a full week of queued work

    # Build ordered_ready_to_spawn
    ordered = []
    for rank, node in enumerate(ready_now, 1):
        ordered.append({
            'rank': rank,
            'id': node['id'],
            'tag': node.get('tag'),
            'title': node['title'],
            'cluster': node['cluster'],
            'leverage_score': node['leverage_score'],
            'effort_hours': node['effort_hours'],
            'weighted_score': node['weighted_score'],
            'unblocks': [nodes.get(u, {}).get('id', u) for u in node['unblocks']],
            'substrate': node['substrate'],
            'scores': {
                'gate_opening_leverage': node['leverage_score'],
                'effort_hours': node['effort_hours'],
                'reuse_multiplier': node['reuse_multiplier'],
                'operator_priority': node['operator_priority_score'],
            },
        })

    # Build cluster summary — ★ next-up per cluster
    cluster_stars = {}
    for node in ready_now:
        c = node['cluster']
        if c not in cluster_stars:
            cluster_stars[c] = {
                'id': node['id'],
                'tag': node.get('tag'),
                'title': node['title'],
                'leverage_score': node['leverage_score'],
                'weighted_score': node['weighted_score'],
            }

    # Waiting_on formatted
    waiting_formatted = {}
    for node_id, blockers in waiting_on.items():
        node = nodes[node_id]
        waiting_formatted[node.get('tag') or node_id] = {
            'title': node['title'],
            'blocked_by': blockers,
        }

    plan = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'summary': {
            'total_handoffs': len(nodes),
            'done': len(done_nodes),
            'in_flight': len(in_flight),
            'ready_now': len(ready_now),
            'waiting_on': len(waiting_on),
            'clusters': len(set(n['cluster'] for n in nodes.values())),
        },
        'ready_now': [n['id'] for n in ready_now],
        'ordered_ready_to_spawn': ordered,
        'parallel_sets': [
            [{'id': n['id'], 'tag': n.get('tag')} for n in group]
            for group in parallel_sets
        ],
        'waiting_on': waiting_formatted,
        'critical_path': [nodes.get(n, {}).get('id', n) for n in critical_path],
        'critical_path_length': len(critical_path),
        'session_budget_hours': round(total_hours, 1),
        'fatigue_flag': fatigue_flag,
        'cluster_next_up': cluster_stars,
        'in_flight': [
            {'id': nodes[n]['id'], 'tag': nodes[n].get('tag') or nodes[n]['id'], 'title': nodes[n]['title']}
            for n in in_flight if n in nodes
        ],
        'cycles': [list(c) for c in cycles] if cycles else [],
        'unmapped_statuses': unmapped_statuses,
        'unresolved_dependencies': unresolved_deps,
    }

    return plan


def render_markdown(plan: dict, nodes: dict) -> str:
    """Render a human-readable summary of the operations plan."""
    lines = [
        '---',
        'type: report',
        'status: draft',
        f'created: {datetime.now().strftime("%Y-%m-%d")}',
        f'updated: {datetime.now().strftime("%Y-%m-%d")}',
        'tags: [operations-planner, operations-plan, leverage, report]',
        '---',
        '',
        '# Operations plan',
        '',
        f'Generated: {plan["generated_at"]}',
        '',
        '## Summary',
        '',
        f'| Metric | Count |',
        f'|---|---|',
        f'| Total handoffs | {plan["summary"]["total_handoffs"]} |',
        f'| Done | {plan["summary"]["done"]} |',
        f'| In flight | {plan["summary"]["in_flight"]} |',
        f'| Ready now | {plan["summary"]["ready_now"]} |',
        f'| Waiting on blockers | {plan["summary"]["waiting_on"]} |',
        f'| Clusters | {plan["summary"]["clusters"]} |',
        '',
        f'**Session budget:** {plan["session_budget_hours"]}h across all ready items',
        f'**Fatigue flag:** {"⚠️ YES — exceeds 40h" if plan["fatigue_flag"] else "No"}',
        f'**Critical path length:** {plan["critical_path_length"]} nodes',
        '',
    ]

    # Currently in flight
    if plan['in_flight']:
        lines.append('## Currently in flight')
        lines.append('')
        for item in plan['in_flight']:
            lines.append(f'- **[{item.get("tag", "?")}]** {item["title"]}')
        lines.append('')

    # Ordered ready to spawn
    lines.append('## Ordered ready to spawn (by weighted leverage)')
    lines.append('')
    lines.append('| Rank | Tag | Title | Cluster | Leverage | Effort | Weighted | Unblocks |')
    lines.append('|---|---|---|---|---|---|---|---|')
    for item in plan['ordered_ready_to_spawn']:
        tag = item.get('tag') or item.get('id', '?')
        unblocks = ', '.join(str(u) for u in item['unblocks']) if item['unblocks'] else '—'
        lines.append(
            f'| {item["rank"]} | [{tag}] | {item["title"][:60]} | {item["cluster"]} '
            f'| {item["leverage_score"]:.2f} | {item["effort_hours"]:.1f}h '
            f'| {item["weighted_score"]:.3f} | {unblocks} |'
        )
    lines.append('')

    # ★ Next-up per cluster
    lines.append('## ★ Next-up per cluster')
    lines.append('')
    for cluster, star in sorted(plan['cluster_next_up'].items()):
        tag = star.get('tag') or star.get('id', '?')
        lines.append(f'- **{cluster}**: [{tag}] {star["title"][:50]} (leverage {star["leverage_score"]:.2f})')
    lines.append('')

    # Critical path
    if plan['critical_path']:
        lines.append('## Critical path (longest dependency chain)')
        lines.append('')
        lines.append(' → '.join(str(n) for n in plan['critical_path']))
        lines.append('')

    # Parallel sets
    if plan['parallel_sets']:
        lines.append('## Parallel-safe sets')
        lines.append('')
        for i, group in enumerate(plan['parallel_sets'], 1):
            tags = ', '.join(f'[{n.get("tag", n["id"])}]' for n in group)
            lines.append(f'- Set {i}: {tags}')
        lines.append('')

    # Waiting on
    if plan['waiting_on']:
        lines.append('## Waiting on (blocked)')
        lines.append('')
        for tag, info in sorted(plan['waiting_on'].items(), key=lambda x: str(x[0] or '')):
            blockers = ', '.join(info['blocked_by'])
            lines.append(f'- **[{tag}]** {info["title"][:50]} — blocked by: {blockers}')
        lines.append('')

    # Warnings
    if plan['cycles']:
        lines.append('## ⚠️ Cycles detected')
        lines.append('')
        for cycle in plan['cycles']:
            lines.append(f'- {" → ".join(cycle)}')
        lines.append('')

    if plan['unmapped_statuses']:
        lines.append('## ⚠️ Unmapped statuses')
        lines.append('')
        for item in plan['unmapped_statuses']:
            lines.append(f'- `{item["file"]}`: status `{item["status"]}`')
        lines.append('')

    if plan['unresolved_dependencies']:
        lines.append('## ⚠️ Unresolved dependencies')
        lines.append('')
        for item in plan['unresolved_dependencies']:
            lines.append(f'- `{item["node"]}` [{item.get("tag", "?")}] → `{item["unresolved_ref"]}`')
        lines.append('')

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Operations planner — reverse-dependency leverage scorer')
    parser.add_argument('--handoffs-dir', type=str,
                        default=os.path.expanduser('~/workspace/second-brain/_meta/handoffs'),
                        help='Path to the handoffs directory')
    parser.add_argument('--output-dir', type=str,
                        default=os.path.expanduser('~/workspace/skills/operations-planner/runs'),
                        help='Path to write output files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    handoffs_dir = Path(args.handoffs_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Operations planner — analyzing {handoffs_dir}")
    print()

    # Step 1: Parse tracker state for 'active' status resolution
    print("Step 1: Parsing tracker state...")
    tracker_state = parse_tracker_state(handoffs_dir)
    if args.verbose:
        print(f"  Tracker entries: {len(tracker_state)}")

    # Step 2: Walk handoff tree
    print("Step 2: Walking handoff tree...")
    nodes, unmapped_statuses = walk_handoff_tree(handoffs_dir, tracker_state, verbose=args.verbose)
    print(f"  Found {len(nodes)} handoff files")
    if unmapped_statuses:
        print(f"  ⚠ {len(unmapped_statuses)} unmapped statuses")

    # Step 3: Build dependency graph
    print("Step 3: Building dependency graph...")
    forward_graph, reverse_graph, unresolved_deps = build_graph(nodes, verbose=args.verbose)
    dep_count = sum(len(v) for v in forward_graph.values())
    print(f"  {dep_count} dependency edges, {len(unresolved_deps)} unresolved")

    # Step 4: Detect cycles
    print("Step 4: Checking for cycles...")
    cycles = detect_cycles(forward_graph)
    if cycles:
        print(f"  ⚠ {len(cycles)} cycle(s) detected!")
    else:
        print("  No cycles.")

    # Step 5: Compute leverage scores
    print("Step 5: Computing leverage scores...")
    leverage_scores = compute_leverage_scores(nodes, reverse_graph)

    # Step 6: Compute critical path
    print("Step 6: Computing critical path...")
    critical_path = compute_critical_path(forward_graph, nodes)
    print(f"  Critical path length: {len(critical_path)} nodes")

    # Step 7: Parse edit-zone conflicts
    print("Step 7: Parsing edit-zone conflicts...")
    edit_zone_conflicts = parse_edit_zone_tables(handoffs_dir)
    print(f"  {len(edit_zone_conflicts)} conflict pairs found")

    # Step 8: Generate the plan
    print("Step 8: Generating operations plan...")
    plan = generate_plan(
        nodes, forward_graph, reverse_graph, leverage_scores,
        edit_zone_conflicts, unmapped_statuses, unresolved_deps,
        cycles, critical_path,
    )

    # Step 9: Write outputs
    today = datetime.now().strftime('%Y-%m-%d')
    json_path = output_dir / f'op-plan-{today}.json'
    md_path = output_dir / f'op-plan-{today}.md'

    with open(json_path, 'w') as f:
        json.dump(plan, f, indent=2, default=str)
    print(f"\n  JSON: {json_path}")

    md_content = render_markdown(plan, nodes)
    with open(md_path, 'w') as f:
        f.write(md_content)
    print(f"  Markdown: {md_path}")

    # Print top-5 summary
    print("\n" + "=" * 60)
    print("TOP 5 BY WEIGHTED LEVERAGE SCORE")
    print("=" * 60)
    for item in plan['ordered_ready_to_spawn'][:5]:
        tag = item.get('tag') or item.get('id', '?')
        unblocks = ', '.join(str(u) for u in item['unblocks']) if item['unblocks'] else 'none'
        print(f"  #{item['rank']}  [{tag}]  leverage={item['leverage_score']:.2f}  "
              f"weighted={item['weighted_score']:.3f}  effort={item['effort_hours']:.1f}h")
        print(f"       {item['title'][:70]}")
        print(f"       unblocks: {unblocks}")
        print()

    print(f"Ready now: {plan['summary']['ready_now']} | "
          f"Waiting: {plan['summary']['waiting_on']} | "
          f"In flight: {plan['summary']['in_flight']} | "
          f"Done: {plan['summary']['done']}")


if __name__ == '__main__':
    main()
