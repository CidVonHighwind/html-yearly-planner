"""
Generate sample images for README from the planner HTML
"""

import os
from typing import Optional
from playwright.sync_api import sync_playwright

import config
from pages.title_page import generate_title_page
from pages.year_overview import generate_year_overview
from pages.monthly_page import generate_monthly_page
from pages.weekly_page import generate_weekly_page


def generate_sample_html(page_content: str, page_name: str) -> str:
    """Generate a single-page HTML file for screenshot"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_name}</title>
    <link rel="stylesheet" href="planner_styles.css">
</head>
<body>
{page_content}
</body>
</html>"""


def generate_sample_images(year: Optional[int] = None) -> None:
    """Generate sample images for each page type"""
    if year is None:
        year = config.DEFAULT_YEAR

    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")

    # Create images directory if it doesn't exist
    os.makedirs(images_dir, exist_ok=True)

    # Define pages to capture
    pages_to_capture = [
        ("title_page", generate_title_page(year)),
        ("year_overview", generate_year_overview(year)),
        ("monthly_page", generate_monthly_page(year, 1)),  # January
        ("weekly_page", generate_weekly_page(year, 1)),  # Week 1
    ]

    print(f"Generating sample images for year {year}...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for page_name, page_content in pages_to_capture:
            # Create temporary HTML file
            html_content = generate_sample_html(page_content, page_name)
            temp_html = os.path.join(script_dir, f"temp_{page_name}.html")

            with open(temp_html, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Load and screenshot
            page.goto(f"file:///{temp_html.replace(chr(92), '/')}")
            page.set_viewport_size({"width": 595, "height": 795})  # 6.2x8.3in at 96dpi

            output_path = os.path.join(images_dir, f"{page_name}.png")
            page.screenshot(path=output_path, full_page=True)
            print(f"✓ Generated: {page_name}.png")

            # Clean up temp file
            os.remove(temp_html)

        browser.close()

    print(f"\n✓ All sample images generated in: {images_dir}")


if __name__ == "__main__":
    generate_sample_images()
