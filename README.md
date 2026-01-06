# Yearly Planner Generator

Generate a printable PDF planner optimized for Kindle Scribe (6.2 x 8.3 inches) with yearly overview, monthly pages, and weekly spreads.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Generate planner:
```bash
python generate_pdf.py
```

The PDF will be created as `2026_planner.pdf` in the project directory.

## Configuration

Edit `config.py` to customize:
- `DEFAULT_YEAR` - Year to generate (default: 2026)
- `PAGE_WIDTH` / `PAGE_HEIGHT` - Page dimensions
- `MONTHLY_NOTES_LINES` / `WEEKLY_LINES_PER_DAY` - Layout options in `constants.py`

## Page Types

### Title Page
Clean cover page with the year and "PLANNER" text.

![Title Page](images/title_page.png)

### Year Overview
12-month calendar grid with clickable links to monthly and weekly pages. Shows week numbers.

![Year Overview](images/year_overview.png)

### Monthly Pages
Full month calendar with large daily blocks for notes and a lined notes section at the bottom.

![Monthly Page](images/monthly_page.png)

### Weekly Pages
7-day spread with 6 lines per day for detailed planning. Each day shows date and weekday name.

![Weekly Page](images/weekly_page.png)

## Features

- **Hyperlinked navigation** - Click dates to jump between pages
- **ISO week numbers** - Consistent week numbering throughout
- **Kindle Scribe optimized** - Perfect dimensions for digital annotation
- **Clean design** - Minimal, professional styling
