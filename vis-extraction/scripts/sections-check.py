#!/usr/bin/env python3
"""
sections-check.py — VIS required-sections enforcement (T1 + T2, Phase 8)

Checks that a source note contains all sections required by extraction-prompt v3.7.
Implements three modes:
  --structure   (default): section headers present + at least one entry per required section
  --content              : structure check + stub detection on action sections
  --stubs-only           : stub detection only, skip structure check (T4b calibration)

Manifest is derived from extraction-prompt v3.7 explicit mandates:
  short:          ## Operator follow-ups  (Step 4: "ALWAYS present for social reels")
  standard:       ## Suggested judgments  (Phase 3, always generated)
                  ## Related notes        (Phase 7: "Every source note must link to")
                  ## Second-squeeze delta (Phase 4b: "MANDATORY, capped")
  prompt-library: ## Prompt library (from source)  (Phase 3: "mandatory when present")

NOT in manifest (conditional / inclusion-gated):
  ## Structured action items — inclusion gate: only when items meet all 4 criteria
  ## Verbatim prompt library — only when demonstrated prompts present (use prompt-library type)

Named-specific detection (stub check):
  An action entry is a "named specific" (not a stub) if it contains:
    1. A backtick-wrapped token  (e.g., `yt-dlp`, `coverage-diff.py`)
    2. A URL                     (e.g., https://grokbot.so)
    3. A token from the note's own ## Tools mentioned table (exact lowercase match)
  Single capitalized words are NOT used for named-specific detection — they are too
  unreliable (sentence-initial words, formatting artifacts, common verbs all capitalize).
  For a named target that is a capitalized proper noun, wrap it in backticks or list it
  in ## Tools mentioned. This is the Gate 2 sharpening: "named specific must NOT rely on
  capitalization to recognize a real target."

Usage:
  python3 sections-check.py <note-file> --type short|standard|prompt-library [--content]
                                                                               [--stubs-only]
                                                                               [--selftest]
                                                                               [--manifest]

Exit codes:
  0  — all checks pass
  1  — section missing or empty (structure failure)
  2  — stub entry detected in action section (content failure)

Manifest version: 1.0 (derived from extraction-prompt v3.7)
Built: 2026-11-23 (VIS-P8 value hardening)
"""

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Manifest — derived from extraction-prompt v3.7 explicit mandates
# ---------------------------------------------------------------------------

MANIFEST = {
    "short": {
        "description": "Short-form video note (social reels, Shorts, TikToks)",
        "required": ["## Operator follow-ups"],
        "action_sections": ["## Operator follow-ups"],
        "source": "extraction-prompt v3.7, §short-form Step 4: 'ALWAYS present for social reels'",
    },
    "standard": {
        "description": "Standard source note (long-form video, article, course)",
        "required": [
            "## Suggested judgments",
            "## Related notes",
            "## Second-squeeze delta",
        ],
        "action_sections": ["## Structured action items"],  # checked IF present
        "source": (
            "extraction-prompt v3.7: "
            "§Suggested judgments (Phase 3, always generated), "
            "§Related notes (Phase 7: 'Every source note must link to'), "
            "§Second-squeeze delta (Phase 4b: 'MANDATORY, capped')"
        ),
    },
    "prompt-library": {
        "description": "Note where transcript contains demonstrated AI prompts",
        "required": ["## Prompt library (from source)"],
        "action_sections": [],
        "source": "extraction-prompt v3.7, §Verbatim prompt library (Phase 3): 'mandatory when present'",
    },
}

# ---------------------------------------------------------------------------
# Stub detection — conservative (misses a stub rather than false-parks real entry)
# ---------------------------------------------------------------------------

# Phrases that signal a generic/stub entry when NO named-specific is also present.
# Two-condition rule: stub phrase + no named specific → FAIL.
# If no stub phrase but also no named specific → PASS (conservative).
STUB_PHRASES = [
    r"\blook\s+into\b",
    r"\bfollow\s+up\s+on\b",
    r"\bresearch\s+further\b",
    r"\binvestigate\s+the\b",
    r"\bcheck\s+on\s+the\b",
    r"\btest\s+the\s+approach\b",
    r"\btest\s+the\s+method\b",
    r"\breview\s+the\s+(?:tools?|claims?|approach|methods?)\b",
    r"\btools?\s+mentioned\b",
    r"\bapproach\s+described\b",
    r"\bthe\s+tools?\b",           # "look into the tools" (bare generic)
    r"\bthe\s+claims?\b",          # "look into the claims"
    r"\bthis\s+approach\b",
    r"\bexplore\s+this\b",
    r"\blook\s+at\s+this\b",
    r"\bgeneral\s+curiosity\b",
]

STUB_RE = re.compile("|".join(STUB_PHRASES), re.IGNORECASE)

# Named-specific detectors — conservative, reliable, no capitalization heuristics
BACKTICK_RE = re.compile(r"`[^`]+`")
URL_RE = re.compile(r"https?://\S+")


def has_named_specific(text: str, tools_mentioned: list[str]) -> bool:
    """
    Return True if text contains a named specific that makes it non-stub.

    Checks (in order):
    1. Backtick-wrapped token — e.g., `yt-dlp`, `coverage-diff.py`
    2. URL — e.g., https://grokbot.so
    3. Exact token from the note's own Tools mentioned table (lowercase match)

    Capitalized proper nouns are intentionally excluded: single capitalized words
    are unreliable (sentence-initial, formatting artifacts, common verbs). For a
    named target that is a proper noun, wrap it in backticks or list it in
    ## Tools mentioned. See Gate 2 sharpening note in module docstring.
    """
    # 1. Backtick-wrapped token
    if BACKTICK_RE.search(text):
        return True
    # 2. URL
    if URL_RE.search(text):
        return True
    # 3. Exact token match against note's own Tools-mentioned entries
    text_lower = text.lower()
    for tool in tools_mentioned:
        t = tool.strip().lower()
        if t and len(t) > 2 and t in text_lower:
            return True
    return False


def is_stub_entry(text: str, tools_mentioned: list[str]) -> bool:
    """
    Return True if the entry is a stub.
    Stub = no named specific AND at least one stub phrase.
    Conservative: entries with neither named specific nor stub phrase → PASS.
    """
    if has_named_specific(text, tools_mentioned):
        return False
    return bool(STUB_RE.search(text))


# ---------------------------------------------------------------------------
# Note parsing helpers
# ---------------------------------------------------------------------------

def parse_sections(content: str) -> dict[str, str]:
    """Parse a markdown note into {header: body_text} mapping."""
    sections = {}
    current_header = None
    current_lines = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_header is not None:
                sections[current_header] = "\n".join(current_lines)
            current_header = line.strip()
            current_lines = []
        elif current_header is not None:
            current_lines.append(line)

    if current_header is not None:
        sections[current_header] = "\n".join(current_lines)

    return sections


def extract_tools_mentioned(sections: dict[str, str]) -> list[str]:
    """
    Extract tool names from ## Tools mentioned section.
    Table format: | Tool | Verified URL | Pricing |
    Returns list of tool name strings (column 1 of data rows).
    """
    tools = []
    body = sections.get("## Tools mentioned", "")
    for line in body.splitlines():
        if line.startswith("|") and not line.startswith("| ---") and not line.startswith("| Tool"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if parts and parts[0] and parts[0] not in ("Tool", "---"):
                tools.append(parts[0])
    return tools


def extract_action_entries(section_body: str) -> list[str]:
    """
    Extract individual action entries from an action section body.
    Handles:
    - Numbered list items: "1. **Title** — description"
    - Bullet items: "- **Title** — description"
    - **What:** / **Why:** style entries
    Returns each entry as a single string (title + description concatenated).
    """
    entries = []
    lines = section_body.splitlines()
    current_entry = []

    for line in lines:
        stripped = line.strip()
        # New list item starts with number+dot, dash, or asterisk
        is_new_item = bool(re.match(r"^(\d+\.\s+|-\s+|\*\s+)", stripped))
        # Also treat **What:** style as new item
        is_what_item = stripped.startswith("**What:**") or stripped.startswith("- **What:**")

        if (is_new_item or is_what_item) and stripped:
            if current_entry:
                entries.append(" ".join(current_entry))
            current_entry = [stripped]
        elif stripped.startswith("**Why:**") or stripped.startswith("- **Why:**"):
            current_entry.append(stripped)
        elif stripped and current_entry:
            # Continuation line
            current_entry.append(stripped)

    if current_entry:
        entries.append(" ".join(current_entry))

    return [e for e in entries if e.strip()]


def section_has_content(body: str) -> bool:
    """Return True if section body has at least one non-blank, non-comment line."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("<!--") and not stripped.startswith("*("):
            return True
    return False


# ---------------------------------------------------------------------------
# Main check functions
# ---------------------------------------------------------------------------

def check_structure(
    note_file: Path,
    note_type: str,
    sections: dict[str, str],
) -> tuple[bool, str]:
    """
    T1 — Structure check: required headers present + each has at least one content line.
    Returns (passed, message).
    """
    spec = MANIFEST[note_type]
    for required_header in spec["required"]:
        if required_header not in sections:
            return (
                False,
                f"PARK — {note_type} note missing required section: {required_header}\n"
                f"Source mandate: {spec['source']}",
            )
        if not section_has_content(sections[required_header]):
            return (
                False,
                f"PARK — {note_type} note has empty required section: {required_header}\n"
                f"The section header is present but contains no content.",
            )
    return True, "PASS — all required sections present and non-empty"


def check_stubs(
    note_file: Path,
    sections: dict[str, str],
    tools_mentioned: list[str],
) -> tuple[bool, str]:
    """
    T2 (stub check only) — no structure prerequisite.
    Checks action sections for stub entries if those sections are present.
    Used for --stubs-only mode (T4b calibration: test stub detection on released notes
    without failing on structure gaps that predate Phase 8 enforcement).
    Returns (passed, message).
    """
    action_sections_to_check = []
    if "## Operator follow-ups" in sections:
        action_sections_to_check.append("## Operator follow-ups")
    if "## Structured action items" in sections:
        action_sections_to_check.append("## Structured action items")

    if not action_sections_to_check:
        return True, "PASS (stubs-only) — no action sections present to check"

    for section_header in action_sections_to_check:
        body = sections.get(section_header, "")
        entries = extract_action_entries(body)

        if not entries:
            return (
                False,
                f"PARK (stubs-only) — {section_header}: section present but no parseable entries.\n"
                f"At minimum one substantive entry is required.",
            )

        for i, entry_text in enumerate(entries, 1):
            if is_stub_entry(entry_text, tools_mentioned):
                return (
                    False,
                    f"PARK (stubs-only) — {section_header}: entry {i} appears to be a stub "
                    f"(no named specific + generic verb pattern detected).\n"
                    f"Entry: {entry_text[:120]}\n"
                    f"Rewrite to name a specific tool (backtick-wrap lowercase tools), URL, "
                    f"or list it in ## Tools mentioned, then state a concrete reason.",
                )

    return True, "PASS (stubs-only) — action entries present and non-stub"


def check_content(
    note_file: Path,
    note_type: str,
    sections: dict[str, str],
    tools_mentioned: list[str],
) -> tuple[bool, str]:
    """
    T1 + T2 combined — structure check first, then stub detection on action sections.
    Returns (passed, message).
    """
    # Structure must pass first
    ok, msg = check_structure(note_file, note_type, sections)
    if not ok:
        return ok, msg

    # Stub detection on action sections
    ok, msg = check_stubs(note_file, sections, tools_mentioned)
    if not ok:
        # Recode exit message to remove "(stubs-only)" qualifier
        return False, msg.replace(" (stubs-only)", "")

    return True, "PASS — all required sections present, action entries non-stub"


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

SELFTEST_CASES = [
    # (description, note_type, mode, sections_dict, tools, expected_pass)
    (
        "short — Operator follow-ups present, real entry",
        "short", "content",
        {
            "## Operator follow-ups": (
                "1. **Hunt down the actual viral X prompt** — Search X for the circulating "
                "two-page GTA6 prompt; if found, extract verbatim into the prompt library."
            )
        },
        [],
        True,
    ),
    (
        "short — Operator follow-ups missing",
        "short", "structure",
        {"## Suggested judgments": "Some content"},
        [],
        False,
    ),
    (
        "short — Operator follow-ups present, stub entry (no named specific, stub phrase)",
        "short", "content",
        {
            "## Operator follow-ups": (
                "1. **What:** Look into the tools mentioned. **Why:** Claims may be worth investigating."
            )
        },
        [],
        False,
    ),
    (
        "short — stub with backtick tool — should PASS",
        "short", "content",
        {
            "## Operator follow-ups": (
                "1. **Test `yt-dlp` on the pipeline** — verify the tool handles the edge case described."
            )
        },
        [],
        True,
    ),
    (
        "short — stub with Tools-mentioned lowercase tool — should PASS",
        "short", "content",
        {
            "## Operator follow-ups": (
                "1. **Look into grokbot for the content pipeline** — worth evaluating for this use case."
            )
        },
        ["grokbot"],  # from Tools mentioned section
        True,
    ),
    (
        "short — Operator follow-ups present, empty section",
        "short", "content",
        {"## Operator follow-ups": ""},
        [],
        False,
    ),
    (
        "standard — all required sections present",
        "standard", "structure",
        {
            "## Suggested judgments": "- **Suggested tier:** 2",
            "## Related notes": "[[some-parent-moc]] · [[peer-note]]",
            "## Second-squeeze delta": "| Pass | Angles | Items | Corrections |\n| 1 | inventory | N/A | — |",
        },
        [],
        True,
    ),
    (
        "standard — Related notes missing",
        "standard", "structure",
        {
            "## Suggested judgments": "- **Suggested tier:** 2",
            "## Second-squeeze delta": "| Pass | Angles | Items | Corrections |",
        },
        [],
        False,
    ),
    (
        "standard — Second-squeeze delta missing",
        "standard", "structure",
        {
            "## Suggested judgments": "- **Suggested tier:** 2",
            "## Related notes": "[[some-moc]]",
        },
        [],
        False,
    ),
    (
        "prompt-library — Prompt library section present",
        "prompt-library", "structure",
        {
            "## Prompt library (from source)": (
                "1. **CEO-persona prompt** — 'You are the CEO...' — timestamp 2:14"
            )
        },
        [],
        True,
    ),
    (
        "prompt-library — Prompt library section missing",
        "prompt-library", "structure",
        {"## Suggested judgments": "- **Suggested tier:** 2"},
        [],
        False,
    ),
]


def run_selftest() -> None:
    """Run built-in test cases and report results."""
    print("Running sections-check.py self-test...")
    passed = 0
    failed = 0

    for desc, note_type, mode, sections, tools, expected_pass in SELFTEST_CASES:
        if mode == "structure":
            ok, msg = check_structure(Path("test.md"), note_type, sections)
        else:
            ok, msg = check_content(Path("test.md"), note_type, sections, tools)

        result = "PASS" if ok == expected_pass else "FAIL"
        status_icon = "✓" if ok == expected_pass else "✗"
        print(f"  {status_icon} [{result}] {desc}")
        if ok != expected_pass:
            print(f"       Expected: {'pass' if expected_pass else 'fail'}, Got: {'pass' if ok else 'fail'}")
            print(f"       Message: {msg}")
            failed += 1
        else:
            passed += 1

    print(f"\nResults: {passed} passed, {failed} failed out of {len(SELFTEST_CASES)} cases")
    if failed:
        sys.exit(1)
    else:
        print("All self-test cases passed.")
        sys.exit(0)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="VIS required-sections enforcement (extraction-prompt v3.7 mandates)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Note types and their required sections:
  short          ## Operator follow-ups
  standard       ## Suggested judgments, ## Related notes, ## Second-squeeze delta
  prompt-library ## Prompt library (from source)

Modes:
  --structure  (default) Section headers present + non-empty
  --content              Structure check + stub detection on action sections

Exit codes: 0=PASS, 1=structure failure, 2=content (stub) failure
""",
    )
    parser.add_argument("note_file", nargs="?", help="Path to the source note .md file")
    parser.add_argument(
        "--type",
        choices=list(MANIFEST.keys()),
        required=False,
        help="Note type (required unless --selftest)",
    )
    parser.add_argument(
        "--content",
        action="store_true",
        default=False,
        help="Enable content (stub-detection) check in addition to structure check",
    )
    parser.add_argument(
        "--stubs-only",
        action="store_true",
        default=False,
        dest="stubs_only",
        help=(
            "Stub detection only — skip structure check. "
            "Use for T4b calibration: verifies stub heuristics don't false-park "
            "real entries in pre-Phase-8 notes that may lack new required sections."
        ),
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        default=False,
        help="Run built-in test cases and exit",
    )
    parser.add_argument(
        "--manifest",
        action="store_true",
        default=False,
        help="Print the full sections manifest and exit",
    )

    args = parser.parse_args()

    if args.selftest:
        run_selftest()
        return

    if args.manifest:
        print("sections-check.py — Required Sections Manifest")
        print("Source: extraction-prompt v3.7 explicit mandates\n")
        for note_type, spec in MANIFEST.items():
            print(f"Note type: {note_type}")
            print(f"  Description: {spec['description']}")
            print(f"  Required sections:")
            for s in spec["required"]:
                print(f"    {s}")
            print(f"  Source: {spec['source']}")
            print()
        print("NOT in manifest (conditional):")
        print("  ## Structured action items — inclusion gate (only when items meet all 4 criteria)")
        print("  ## Verbatim prompt library — use note type 'prompt-library' instead")
        return

    if args.stubs_only:
        # --stubs-only does not require --type
        if not args.note_file:
            parser.error("note_file is required with --stubs-only")
    elif not args.note_file or not args.type:
        parser.error("note_file and --type are required (or use --selftest, --manifest, or --stubs-only)")

    note_file = Path(args.note_file)
    if not note_file.exists():
        print(f"ERROR: Note file not found: {note_file}", file=sys.stderr)
        sys.exit(1)

    content = note_file.read_text(encoding="utf-8")
    sections = parse_sections(content)
    tools_mentioned = extract_tools_mentioned(sections)

    if args.stubs_only:
        ok, msg = check_stubs(note_file, sections, tools_mentioned)
        exit_code = 0 if ok else 2
    elif args.content:
        ok, msg = check_content(note_file, args.type, sections, tools_mentioned)
        exit_code = 0 if ok else 2
    else:
        ok, msg = check_structure(note_file, args.type, sections)
        exit_code = 0 if ok else 1

    print(msg)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
