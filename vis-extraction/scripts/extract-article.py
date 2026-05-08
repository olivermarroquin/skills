#!/usr/bin/env python3
# extract-article.py — extract title, author, date, and clean markdown body from HTML
#
# Reads HTML from stdin, writes structured output to stdout in the format:
#
#   TITLE::<title>
#   AUTHOR::<author>
#   DATE::<date>
#   BODY_START::
#   <markdown body>
#
# Designed to be called by transcript-pull.sh after curl fetches the HTML.

import sys
import trafilatura

html = sys.stdin.read()

if not html or len(html) < 100:
    # Empty or absurdly small response — nothing to extract.
    sys.exit(4)

result = trafilatura.extract(
    html,
    output_format="markdown",
    with_metadata=True,
    include_comments=False,
    include_tables=True,
    include_links=False,
    favor_recall=False,
)

meta = trafilatura.extract_metadata(html)

if meta is None:
    print("TITLE::untitled")
    print("AUTHOR::unknown")
    print("DATE::unknown")
else:
    title = (meta.title or "untitled").strip()
    author = (meta.author or "unknown").strip() if meta.author else "unknown"
    date = (meta.date or "unknown").strip() if meta.date else "unknown"
    print(f"TITLE::{title}")
    print(f"AUTHOR::{author}")
    print(f"DATE::{date}")

print("BODY_START::")
print(result or "")
