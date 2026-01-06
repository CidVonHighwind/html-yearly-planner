"""
Configuration settings for the planner PDF generator
"""

import os
from typing import Optional

# Year to generate
DEFAULT_YEAR = 2026

# Page dimensions for Kindle Scribe (6.2 x 8.3 inches)
PAGE_WIDTH = "6.2in"
PAGE_HEIGHT = "8.3in"

# PDF generation settings
PDF_SETTINGS = {
    "width": PAGE_WIDTH,
    "height": PAGE_HEIGHT,
    "margin": {
        "top": "0px",
        "right": "0px",
        "bottom": "0px",
        "left": "0px",
    },
    "print_background": True,
}


# File paths
def get_output_paths(year: int, script_dir: Optional[str] = None) -> dict[str, str]:
    """Get output paths for HTML and PDF files"""
    if script_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.join(script_dir, "output")

    return {
        "html": os.path.join(output_dir, "planner_generated.html"),
        "pdf": os.path.join(output_dir, f"{year}.pdf"),
        "css": os.path.join(script_dir, "planner_styles.css"),
        "output_dir": output_dir,
    }
