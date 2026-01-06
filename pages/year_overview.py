"""
Year overview page generator
"""

import calendar
import datetime
from constants import MONTH_NAMES, WEEKDAY_ABBR


def generate_year_overview(year: int) -> str:
    """Generate HTML for year-at-a-glance page"""
    calendar_html = _generate_year_calendar_html(year)

    return f"""
    <!-- Year at a Glance -->
    <div class="page">
        <div class="year-overview" id="year-overview">
            <div class="months-grid">
{calendar_html}
            </div>
        </div>
    </div>
"""


def _generate_year_calendar_html(year: int) -> str:
    """Generate HTML for all 12 month calendars"""
    months_html = []

    for month_num in range(1, 13):
        cal = calendar.monthcalendar(year, month_num)
        month_name = MONTH_NAMES[month_num - 1]

        # Build calendar HTML
        month_html = f'<div class="month-box">\n'
        month_html += f'  <h3><a href="#month-{month_num}">{month_name}</a></h3>\n'
        month_html += f'  <div class="calendar">\n'

        # Weekday headers with week column
        month_html += '    <div class="calendar-header">\n'
        month_html += '      <div class="week-col">W</div>\n'
        for day in WEEKDAY_ABBR:
            month_html += f"      <div>{day}</div>\n"
        month_html += "    </div>\n"

        # Calendar days with week numbers
        month_html += '    <div class="calendar-days">\n'
        first_day_of_month = cal[0]
        first_day_num = next((d for d in first_day_of_month if d != 0), 1)
        first_date = datetime.date(year, month_num, first_day_num)

        for week_idx, week in enumerate(cal):
            # Calculate week number
            if week[0] != 0:
                week_date = datetime.date(year, month_num, week[0])
            else:
                first_valid = next((d for d in week if d != 0), None)
                if first_valid:
                    week_date = datetime.date(year, month_num, first_valid)
                else:
                    week_date = first_date
            week_num = week_date.isocalendar()[1]

            month_html += '      <div class="calendar-week-row">\n'
            month_html += f'        <div class="week-num"><a href="#week-{week_num}">{week_num}</a></div>\n'
            for day in week:
                if day == 0:
                    month_html += '        <div class="day empty"></div>\n'
                else:
                    month_html += f'        <div class="day">{day}</div>\n'
            month_html += "      </div>\n"
        month_html += "    </div>\n"
        month_html += "  </div>\n"
        month_html += "</div>\n"

        months_html.append(month_html)

    return "\n".join(months_html)
