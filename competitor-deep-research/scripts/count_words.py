#!/usr/bin/env python3
"""
Count words in a fetched competitor page.

Usage:
    # From a file:
    python count_words.py <path-to-fetched-page.md>

    # From stdin (e.g., piping WebFetch markdown output):
    cat fetched-page.md | python count_words.py

    # Multiple files:
    python count_words.py page1.md page2.md page3.md

Output:
    JSON with word count, line count, and section breakdown by H1/H2/H3 headings.

Purpose:
    Used by the competitor-deep-research skill to get hard word counts on fetched
    competitor pages, replacing the "estimate from reading" approach. The synthesis's
    quantitative claims about content depth are sharper when grounded in actual counts.
"""

import json
import re
import sys
from pathlib import Path


def count_words_in_text(text: str) -> dict:
    """Count words and break down by heading section."""
    # Strip code blocks (don't count code as prose)
    text_no_code = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Strip inline code
    text_no_code = re.sub(r'`[^`]+`', '', text_no_code)
    # Strip markdown link syntax but keep link text
    text_no_links = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text_no_code)
    # Strip image syntax
    text_no_images = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', text_no_links)
    # Strip HTML tags
    text_no_html = re.sub(r'<[^>]+>', '', text_no_images)

    words = re.findall(r'\b\w+\b', text_no_html)
    total_word_count = len(words)

    # Section breakdown — split on H1/H2/H3
    sections = []
    current_section = {'heading': '(intro)', 'level': 0, 'words': 0}

    for line in text_no_html.split('\n'):
        heading_match = re.match(r'^(#{1,3})\s+(.+)$', line)
        if heading_match:
            # Save the previous section
            if current_section['words'] > 0:
                sections.append(current_section)
            current_section = {
                'heading': heading_match.group(2).strip(),
                'level': len(heading_match.group(1)),
                'words': 0,
            }
        else:
            line_words = len(re.findall(r'\b\w+\b', line))
            current_section['words'] += line_words

    # Don't forget the last section
    if current_section['words'] > 0:
        sections.append(current_section)

    return {
        'total_words': total_word_count,
        'total_lines': len(text.split('\n')),
        'sections': sections,
    }


def main():
    if len(sys.argv) == 1 and sys.stdin.isatty():
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    results = {}

    if len(sys.argv) > 1:
        # Read from files
        for filepath in sys.argv[1:]:
            path = Path(filepath)
            if not path.exists():
                print(f"Error: file not found: {filepath}", file=sys.stderr)
                continue
            text = path.read_text(encoding='utf-8')
            results[str(path)] = count_words_in_text(text)
    else:
        # Read from stdin
        text = sys.stdin.read()
        results['<stdin>'] = count_words_in_text(text)

    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
