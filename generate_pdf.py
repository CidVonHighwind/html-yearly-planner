"""
Generate PDF planner from HTML using Playwright
"""

import os
import shutil
from datetime import datetime
from typing import Optional
from playwright.sync_api import sync_playwright

import config
from pages.title_page import generate_title_page
from pages.year_overview import generate_year_overview
from pages.monthly_page import generate_all_monthly_pages
from pages.weekly_page import generate_all_weekly_pages


def generate_html(year: int) -> str:
    """Generate complete HTML by combining all pages"""
    # Collect all page content
    pages = []
    pages.append(generate_title_page(year))
    pages.append(generate_year_overview(year))

    # Add all monthly pages
    pages.extend(generate_all_monthly_pages(year))

    # Add all weekly pages
    pages.extend(generate_all_weekly_pages(year))

    # Combine into full HTML document with external CSS
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{year} Planner</title>
    <link rel="stylesheet" href="planner_styles.css">
</head>
<body>
{''.join(pages)}
</body>
</html>"""

    return html_content


def generate_planner_pdf(year: Optional[int] = None) -> None:
    """Generate HTML and convert to PDF using Playwright"""
    if year is None:
        year = config.DEFAULT_YEAR

    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = config.get_output_paths(year, script_dir)
    html_path = paths["html"]
    pdf_path = paths["pdf"]

    # Create output directory if it doesn't exist
    os.makedirs(paths["output_dir"], exist_ok=True)

    # Copy CSS file to output directory
    css_source = paths["css"]
    css_dest = os.path.join(paths["output_dir"], "planner_styles.css")
    shutil.copy2(css_source, css_dest)

    # Delete old PDF if it exists
    if os.path.exists(pdf_path):
        print(f"Deleting old PDF: {pdf_path}")
        os.remove(pdf_path)

    print(f"Generating HTML for year {year}...")
    html_content = generate_html(year)

    # Save generated HTML
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✓ HTML saved to: {html_path}")

    # return

    print(f"Generating PDF with Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the HTML file
        page.goto(f"file:///{html_path.replace(chr(92), '/')}")

        # Generate PDF with exact page settings matching CSS (1404 x 1872 pixels)
        page.pdf(path=pdf_path, **config.PDF_SETTINGS)

        browser.close()

    print(f"✓ PDF generated successfully!")
    print(f"  Output: {pdf_path}")

    # Get file size and modification time
    size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    mod_time = datetime.fromtimestamp(os.path.getmtime(pdf_path))
    print(f"  Size: {size_mb:.2f} MB")
    print(f"  Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    generate_planner_pdf()
