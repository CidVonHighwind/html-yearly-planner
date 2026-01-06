from generate_pdf import generate_planner_pdf

if __name__ == "__main__":
    for year in range(2026, 2031):
        print(f"=== Generating {year} ===")
        generate_planner_pdf(year)
