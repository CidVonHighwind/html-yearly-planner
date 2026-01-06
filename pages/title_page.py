"""
Title page generator
"""


def generate_title_page(year: int) -> str:
    """Generate HTML for title page"""
    return f"""
    <!-- Title Page -->
    <div class="page">
        <div class="title-page">
            <h1>{year}</h1>
            <h2>PLANNER</h2>
        </div>
    </div>
"""
