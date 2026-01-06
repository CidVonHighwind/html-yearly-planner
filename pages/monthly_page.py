"""
Monthly page generator with daily blocks and notes section
"""

import calendar
import datetime
from constants import MONTH_NAMES, WEEKDAY_NAMES, MONTHLY_NOTES_LINES


def generate_monthly_page(year: int, month_num: int) -> str:
    """Generate HTML for a single month page with daily blocks and notes"""
    month_name = MONTH_NAMES[month_num - 1]
    cal = calendar.monthcalendar(year, month_num)

    # Build header row with weekday names (no WEEK header)
    header_html = '<tr class="header-row"><th class="week-header"></th>'
    for day_name in WEEKDAY_NAMES:
        header_html += f'<th class="weekday-header">{day_name}</th>'
    header_html += "</tr>"

    # Build the table rows
    rows_html = []
    for week_idx, week in enumerate(cal):
        # Calculate ISO week number using the first valid day in the week
        first_day = next((d for d in week if d != 0), None)
        if first_day:
            week_date = datetime.date(year, month_num, first_day)
            iso_week_num = week_date.isocalendar()[1]
        else:
            iso_week_num = week_idx + 1

        cells = [
            f'<td class="week-number"><div class="week-text"><a href="#week-{iso_week_num}">WEEK {iso_week_num}</a></div></td>'
        ]

        for day in week:
            if day == 0:
                cells.append('<td class="day-cell empty"></td>')
            else:
                cells.append(
                    f'<td class="day-cell"><span class="day-number">{day}</span></td>'
                )
        rows_html.append(f'<tr class="data-row">{"".join(cells)}</tr>')

    # Create notes section as a table with lines (similar to weekly pages)
    notes_rows = []
    for i in range(MONTHLY_NOTES_LINES):
        notes_rows.append(
            '<tr class="notes-line-row"><td class="notes-line-cell"></td></tr>'
        )

    notes_table = f"""
            <table class="notes-table">
                <tbody>
{''.join(notes_rows)}
                </tbody>
            </table>"""

    return f"""
    <!-- Monthly Page: {month_name} -->
    <div class="page">
        <div class="monthly-page" id="month-{month_num}">
            <div class="year-link"><a href="#year-overview">{year}</a></div>
            <h2 class="month-title">{month_name}</h2>
            
            <table class="days-grid">
{header_html}
{''.join(rows_html)}
            </table>
            
            <div class="notes-section">
{notes_table}
            </div>
        </div>
    </div>
    """


def generate_all_monthly_pages(year: int) -> list[str]:
    """Generate all 12 monthly pages"""
    pages = []
    for month_num in range(1, 13):
        pages.append(generate_monthly_page(year, month_num))
    return pages
