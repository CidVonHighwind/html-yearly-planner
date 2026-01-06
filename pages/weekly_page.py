"""
Weekly page generator with daily sections
"""

import datetime
import calendar
from constants import WEEKDAY_NAMES, WEEKLY_LINES_PER_DAY


def generate_weekly_page(year: int, week_num: int) -> str:
    """Generate HTML for a single week page with sections for each day"""
    # Get the date range for this ISO week
    jan4 = datetime.date(year, 1, 4)
    week_one_start = jan4 - datetime.timedelta(days=jan4.weekday())
    week_start = week_one_start + datetime.timedelta(weeks=week_num - 1)

    # Build table rows - 6 rows per day, 42 rows total
    rows_html = []

    for day_offset in range(7):
        current_date = week_start + datetime.timedelta(days=day_offset)
        day_name = WEEKDAY_NAMES[day_offset]
        day_number = current_date.day

        # First row of each day has the label
        rows_html.append(
            f"""
        <tr class="week-line-row">
            <td class="week-day-cell week-day-first">
                <div class="week-day-label-row">
                    <span class="week-day-name-left">{day_name}</span>
                    <span class="week-day-num-right">{day_number}</span>
                </div>
            </td>
            <td class="week-spacer-cell"></td>
            <td class="week-notes-cell week-notes-first"></td>
        </tr>"""
        )

        # Remaining rows for that day are empty
        for _ in range(WEEKLY_LINES_PER_DAY - 1):
            rows_html.append(
                """
        <tr class="week-line-row">
            <td class="week-day-cell"></td>
            <td class="week-spacer-cell"></td>
            <td class="week-notes-cell"></td>
        </tr>"""
            )

    # Format week date range (Windows compatible)
    week_end = week_start + datetime.timedelta(days=6)
    start_str = week_start.strftime("%B %d").replace(" 0", " ")
    end_str = week_end.strftime("%B %d, %Y").replace(" 0", " ")

    # Create linked month names
    start_month = week_start.month
    end_month = week_end.month
    start_month_name = week_start.strftime("%B")
    end_month_name = week_end.strftime("%B")

    # Build date range with linked month names
    if start_month == end_month:
        # Same month: "February 9 - 15, 2026"
        date_range = f'<a href="#month-{start_month}">{start_month_name}</a> {week_start.day} - {week_end.day}, {year}'
    else:
        # Different months: "February 24 - March 2, 2026"
        date_range = f'<a href="#month-{start_month}">{start_month_name}</a> {week_start.day} - <a href="#month-{end_month}">{end_month_name}</a> {week_end.day}, {year}'

    return f"""
    <!-- Weekly Page: Week {week_num} -->
    <div class="page">
        <div class="weekly-page" id="week-{week_num}">
            <div class="week-header-section">
                <div class="year-link"><a href="#year-overview">{year}</a></div>
                <h2 class="week-title">WEEK {week_num}</h2>
                <div class="week-date-range">{date_range}</div>
            </div>
            
            <table class="week-table">
                <colgroup>
                    <col style="width: 49%;">
                    <col style="width: 2%;">
                    <col style="width: 49%;">
                </colgroup>
                <tbody>
{''.join(rows_html)}
                </tbody>
            </table>
        </div>
    </div>
    """


def generate_all_weekly_pages(year: int) -> list[str]:
    """Generate all weekly pages for the year"""
    pages = []

    # Calculate number of weeks in the year
    jan4 = datetime.date(year, 1, 4)
    dec28 = datetime.date(year, 12, 28)
    last_week = dec28.isocalendar()[1]

    for week_num in range(1, last_week + 1):
        pages.append(generate_weekly_page(year, week_num))

    return pages
