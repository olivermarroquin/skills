"""Generate Keelworks LLC invoice PDF.

Usage:
  python3 generate_invoice.py \\
    --client-name "Ahmad Shaban" \\
    --client-business "EV Electric Services" \\
    --client-location "Fairfax, Virginia" \\
    --client-website "evelectric.pro" \\
    --invoice-number "EVE-001" \\
    --amount "700.00" \\
    --issued-date "May 13, 2026" \\
    --due-line "On or before May 20, 2026"

See SKILL.md in this directory for full documentation.

This script uses ReportLab to produce a branded one-page PDF invoice with:
- Keelworks wordmark in the header (with teal ".ai" accent if used)
- Client identity block
- Engagement subtitle (two configurable lines)
- Action-verb scope items list (7 default items, overridable)
- Payment box with Zelle details
- Footer with invoice metadata

The script prints a content-gap diagnostic at the end so callers can verify the
output before sending.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, black, white
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("ERROR: reportlab is not installed. Install with:")
    print("  pip install --user --break-system-packages reportlab")
    sys.exit(1)


# Brand palette
KEELWORKS_TEAL = HexColor("#2BB3A3")
KEELWORKS_INK = HexColor("#1A2332")
KEELWORKS_MUTED = HexColor("#6B7785")
KEELWORKS_LIGHT = HexColor("#F5F7FA")


DEFAULT_SCOPE_ITEMS = [
    "Initiate site audit and competitive analysis",
    "Build out and optimize your Google Business Profile",
    "Architect and develop Core 30 service + city pages",
    "Deploy technical SEO foundations (schema, performance, fixes)",
    "Launch local community signal outreach (Chamber, sponsorships, directories)",
    "Integrate call tracking and source attribution",
    "Additional services discussed during our call",
]


DEFAULT_PAYMENT_LINE = "Zelle / 240-204-3885 / Oliver Marroquin"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a Keelworks LLC invoice PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Client identity
    parser.add_argument("--client-name", required=True, help='e.g. "Ahmad Shaban"')
    parser.add_argument("--client-business", required=True, help='e.g. "EV Electric Services"')
    parser.add_argument("--client-location", required=True, help='e.g. "Fairfax, Virginia"')
    parser.add_argument("--client-website", required=True, help='e.g. "evelectric.pro"')

    # Invoice identity
    parser.add_argument("--invoice-number", required=True, help='e.g. "EVE-001"')
    parser.add_argument("--amount", required=True, help='e.g. "700.00" (no $ sign)')
    parser.add_argument("--issued-date", required=True, help='e.g. "May 13, 2026"')
    parser.add_argument(
        "--due-line",
        required=True,
        help='e.g. "On or before May 20, 2026" or "$250 around May 14 · $250 around May 16"',
    )

    # Optional: reference suffix shown below Invoice #
    parser.add_argument(
        "--reference-suffix",
        default=None,
        help='e.g. "EV Electric" — appears under "Invoice #"',
    )

    # Optional: payment method note shown next to payment box
    parser.add_argument(
        "--payment-method-note",
        default="Fast, free, instant",
        help='e.g. "Fast, free, instant" or "$250 + $250 split"',
    )

    # Engagement subtitle (two lines)
    parser.add_argument(
        "--engagement-subtitle-line-1",
        default=None,
        help='e.g. "Beginning the work needed to grow EV Electric\'s organic visibility"',
    )
    parser.add_argument(
        "--engagement-subtitle-line-2",
        default=None,
        help='e.g. "across Google, Google Maps, and AI search."',
    )

    # Next steps (two lines)
    parser.add_argument("--next-steps-line-1", default=None)
    parser.add_argument("--next-steps-line-2", default=None)

    # Scope items override
    parser.add_argument(
        "--scope-items",
        nargs="+",
        default=None,
        help="Override default scope items. Pass each as a separate argument.",
    )

    # Payment line override
    parser.add_argument(
        "--payment-line",
        default=DEFAULT_PAYMENT_LINE,
        help=f'Payment instruction line. Default: "{DEFAULT_PAYMENT_LINE}"',
    )

    # Output path
    parser.add_argument(
        "--output-path",
        default=None,
        help='Defaults to ~/workspace/repos/keelworks/ops/invoices/invoice-<lowercase-invoice-number>-keelworks.pdf',
    )

    return parser.parse_args()


def resolve_output_path(args):
    if args.output_path:
        return Path(args.output_path).expanduser()
    default_dir = Path.home() / "workspace" / "repos" / "keelworks" / "ops" / "invoices"
    default_dir.mkdir(parents=True, exist_ok=True)
    filename = f"invoice-{args.invoice_number.lower()}-keelworks.pdf"
    return default_dir / filename


def draw_wordmark(c, x, y):
    """Draw 'keelworks.ai' wordmark with teal .ai accent at (x, y)."""
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(KEELWORKS_INK)
    c.drawString(x, y, "keelworks")
    keelworks_width = c.stringWidth("keelworks", "Helvetica-Bold", 20)
    c.setFillColor(KEELWORKS_TEAL)
    c.drawString(x + keelworks_width, y, ".ai")


def draw_header(c, args, page_width, page_height):
    """Draw header band: wordmark + invoice number on right."""
    header_y = page_height - 0.75 * inch
    draw_wordmark(c, 0.6 * inch, header_y)

    # Invoice metadata block (right side)
    c.setFont("Helvetica", 9)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawRightString(page_width - 0.6 * inch, header_y + 8, "INVOICE")
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(KEELWORKS_INK)
    c.drawRightString(page_width - 0.6 * inch, header_y - 10, f"#{args.invoice_number}")

    if args.reference_suffix:
        c.setFont("Helvetica", 9)
        c.setFillColor(KEELWORKS_MUTED)
        c.drawRightString(page_width - 0.6 * inch, header_y - 24, args.reference_suffix)

    # Horizontal rule below header
    c.setStrokeColor(KEELWORKS_LIGHT)
    c.setLineWidth(1)
    c.line(0.6 * inch, header_y - 38, page_width - 0.6 * inch, header_y - 38)


def draw_client_block(c, args, page_width, page_height):
    """Draw client identity block."""
    y = page_height - 1.65 * inch

    c.setFont("Helvetica", 9)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawString(0.6 * inch, y, "BILL TO")
    y -= 14

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(KEELWORKS_INK)
    c.drawString(0.6 * inch, y, args.client_name)
    y -= 14

    c.setFont("Helvetica", 11)
    c.setFillColor(KEELWORKS_INK)
    c.drawString(0.6 * inch, y, args.client_business)
    y -= 13

    c.setFont("Helvetica", 10)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawString(0.6 * inch, y, args.client_location)
    y -= 13
    c.drawString(0.6 * inch, y, args.client_website)

    # Invoice date block on right
    right_y = page_height - 1.65 * inch
    c.setFont("Helvetica", 9)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawRightString(page_width - 0.6 * inch, right_y, "ISSUED")
    c.setFont("Helvetica", 11)
    c.setFillColor(KEELWORKS_INK)
    c.drawRightString(page_width - 0.6 * inch, right_y - 14, args.issued_date)

    c.setFont("Helvetica", 9)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawRightString(page_width - 0.6 * inch, right_y - 32, "DUE")
    c.setFont("Helvetica", 11)
    c.setFillColor(KEELWORKS_INK)
    c.drawRightString(page_width - 0.6 * inch, right_y - 46, args.due_line)


def draw_engagement_subtitle(c, args, page_width, page_height):
    """Draw the two-line engagement subtitle below the client block."""
    if not args.engagement_subtitle_line_1 and not args.engagement_subtitle_line_2:
        return page_height - 2.85 * inch  # no subtitle drawn

    y = page_height - 2.85 * inch
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(KEELWORKS_INK)
    if args.engagement_subtitle_line_1:
        c.drawString(0.6 * inch, y, args.engagement_subtitle_line_1)
        y -= 14
    if args.engagement_subtitle_line_2:
        c.drawString(0.6 * inch, y, args.engagement_subtitle_line_2)
        y -= 14
    return y - 6


def draw_scope_items(c, args, top_y, page_width):
    """Draw the action-verb scope items list."""
    items = args.scope_items if args.scope_items else DEFAULT_SCOPE_ITEMS

    y = top_y
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawString(0.6 * inch, y, "SCOPE OF WORK")
    y -= 18

    c.setFont("Helvetica", 10.5)
    c.setFillColor(KEELWORKS_INK)
    for item in items:
        # Small teal bullet
        c.setFillColor(KEELWORKS_TEAL)
        c.circle(0.7 * inch, y + 3, 2, fill=1, stroke=0)
        # Item text
        c.setFillColor(KEELWORKS_INK)
        c.drawString(0.85 * inch, y, item)
        y -= 17
    return y - 10


def draw_payment_box(c, args, top_y, page_width):
    """Draw payment box with amount + payment line."""
    box_top = top_y
    box_height = 1.0 * inch
    box_left = 0.6 * inch
    box_right = page_width - 0.6 * inch
    box_bottom = box_top - box_height

    # Background
    c.setFillColor(KEELWORKS_LIGHT)
    c.rect(box_left, box_bottom, box_right - box_left, box_height, fill=1, stroke=0)

    # Amount label
    c.setFont("Helvetica", 9)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawString(box_left + 0.2 * inch, box_top - 18, "AMOUNT DUE")

    # Amount value
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(KEELWORKS_INK)
    c.drawString(box_left + 0.2 * inch, box_top - 44, f"${args.amount}")

    # Payment-method note
    if args.payment_method_note:
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(KEELWORKS_MUTED)
        c.drawString(box_left + 0.2 * inch, box_top - 60, args.payment_method_note)

    # Payment line (right side)
    c.setFont("Helvetica", 9)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawRightString(box_right - 0.2 * inch, box_top - 18, "SEND TO")
    c.setFont("Helvetica", 11)
    c.setFillColor(KEELWORKS_INK)
    c.drawRightString(box_right - 0.2 * inch, box_top - 34, args.payment_line)
    c.setFont("Helvetica", 9)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawRightString(
        box_right - 0.2 * inch,
        box_top - 50,
        f"Reference: {args.invoice_number}",
    )

    return box_bottom - 12


def draw_next_steps(c, args, top_y, page_width):
    """Draw optional next-steps lines under payment box."""
    if not args.next_steps_line_1 and not args.next_steps_line_2:
        return top_y

    y = top_y
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawString(0.6 * inch, y, "NEXT")
    y -= 16

    c.setFont("Helvetica", 10)
    c.setFillColor(KEELWORKS_INK)
    if args.next_steps_line_1:
        c.drawString(0.6 * inch, y, args.next_steps_line_1)
        y -= 14
    if args.next_steps_line_2:
        c.drawString(0.6 * inch, y, args.next_steps_line_2)
        y -= 14
    return y


def draw_footer(c, page_width):
    """Draw footer with company line."""
    c.setStrokeColor(KEELWORKS_LIGHT)
    c.setLineWidth(1)
    c.line(0.6 * inch, 0.6 * inch + 24, page_width - 0.6 * inch, 0.6 * inch + 24)

    c.setFont("Helvetica", 8)
    c.setFillColor(KEELWORKS_MUTED)
    c.drawString(0.6 * inch, 0.6 * inch + 8, "Keelworks LLC")
    c.drawRightString(
        page_width - 0.6 * inch,
        0.6 * inch + 8,
        "Thank you for the trust.",
    )


def print_diagnostic(args, output_path):
    """Print content-gap diagnostic so callers can verify before sending."""
    print("\n=== Invoice generated ===")
    print(f"  File:        {output_path}")
    try:
        size_kb = output_path.stat().st_size / 1024
        print(f"  Size:        {size_kb:.1f} KB")
    except FileNotFoundError:
        print(f"  Size:        (file not found — generation failed?)")

    print("\n=== Content gap check ===")
    gaps = []
    if not args.engagement_subtitle_line_1:
        gaps.append("engagement-subtitle-line-1 missing — invoice will have no engagement framing")
    if not args.next_steps_line_1:
        gaps.append("next-steps-line-1 missing — invoice will have no 'what's next' line")
    if not args.reference_suffix:
        gaps.append("reference-suffix missing — only invoice number shown in header")

    if gaps:
        for g in gaps:
            print(f"  ⚠  {g}")
    else:
        print("  ✓  No content gaps detected.")

    print()


def generate_invoice(args):
    output_path = resolve_output_path(args)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    page_width, page_height = LETTER
    c = canvas.Canvas(str(output_path), pagesize=LETTER)

    draw_header(c, args, page_width, page_height)
    draw_client_block(c, args, page_width, page_height)
    after_subtitle_y = draw_engagement_subtitle(c, args, page_width, page_height)
    after_scope_y = draw_scope_items(c, args, after_subtitle_y, page_width)
    after_payment_y = draw_payment_box(c, args, after_scope_y, page_width)
    draw_next_steps(c, args, after_payment_y, page_width)
    draw_footer(c, page_width)

    c.showPage()
    c.save()

    print_diagnostic(args, output_path)
    return output_path


def main():
    args = parse_args()
    output_path = generate_invoice(args)
    return 0 if output_path.exists() else 1


if __name__ == "__main__":
    sys.exit(main())
