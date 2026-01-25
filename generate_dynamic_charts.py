"""Generate dynamic charts for Stronger Start for Working Families Act analysis.

This script generates charts using live PolicyEngine-US microsimulation data
rather than hardcoded values from statewide.py.
"""

from pathlib import Path

from stronger_start.dynamic_charts import (
    calculate_decile_impacts,
    create_dynamic_winners_by_decile_chart,
    create_dynamic_avg_benefit_by_decile_chart,
    create_dynamic_net_income_change_chart,
    create_dynamic_baseline_reform_chart,
)

# Output directories
OUTPUT_DIR = Path("output")
CHARTS_DIR = OUTPUT_DIR / "charts"

# HTML template for standalone chart files
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Roboto Serif', serif;
        }}
        #chart {{
            width: 100%;
            height: 100vh;
        }}
    </style>
</head>
<body>
    <div id="chart"></div>
    <script>
        var figure = {figure_json};
        Plotly.newPlot('chart', figure.data, figure.layout, {{responsive: true}});
    </script>
</body>
</html>
"""


def generate_chart_html(fig, title: str, filename: str) -> None:
    """Generate standalone HTML file for a Plotly chart."""
    html_content = HTML_TEMPLATE.format(
        title=title,
        figure_json=fig.to_json(),
    )

    filepath = CHARTS_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated: {filepath}")


def main():
    """Generate all dynamic chart files."""
    # Create output directories
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Generating DYNAMIC charts for Stronger Start for Working Families Act")
    print("Using PolicyEngine-US microsimulation")
    print("=" * 60)
    print()

    # Step 1: Run microsimulation to get decile data
    print("Step 1: Running microsimulation...")
    microsim_data = calculate_decile_impacts()
    print("Microsimulation complete.")
    print()

    # Step 2: Generate charts
    print("Step 2: Generating charts...")
    print()

    # Chart 1: Baseline vs Reform comparison
    print("Creating dynamic baseline vs reform comparison chart...")
    fig1 = create_dynamic_baseline_reform_chart()
    generate_chart_html(
        fig1,
        "Baseline vs Reform (Dynamic) - Stronger Start for Working Families Act",
        "dynamic-baseline-reform-comparison.html",
    )

    # Chart 2: Net income change (redesigned with 3 scenarios)
    print("Creating dynamic net income change chart (3 scenarios)...")
    fig2 = create_dynamic_net_income_change_chart()
    generate_chart_html(
        fig2,
        "Net Income Change (Dynamic) - Stronger Start for Working Families Act",
        "dynamic-net-income-change.html",
    )

    # Chart 3: Winners/Losers by decile
    print("Creating dynamic winners by decile chart...")
    fig3 = create_dynamic_winners_by_decile_chart(microsim_data)
    generate_chart_html(
        fig3,
        "Winners by Income Decile (Dynamic) - Stronger Start for Working Families Act",
        "dynamic-winners-by-decile.html",
    )

    # Chart 4: Average benefit by decile
    print("Creating dynamic average benefit by decile chart...")
    fig4 = create_dynamic_avg_benefit_by_decile_chart(microsim_data)
    generate_chart_html(
        fig4,
        "Average Benefit by Income Decile (Dynamic) - Stronger Start for Working Families Act",
        "dynamic-avg-benefit-by-decile.html",
    )

    print()
    print("=" * 60)
    print("Done! Dynamic charts generated in output/charts/")
    print("=" * 60)
    print()
    print("Dynamic chart URLs after deployment:")
    print("  https://policyengine.github.io/stronger-start-calc/dynamic-baseline-reform-comparison.html")
    print("  https://policyengine.github.io/stronger-start-calc/dynamic-net-income-change.html")
    print("  https://policyengine.github.io/stronger-start-calc/dynamic-winners-by-decile.html")
    print("  https://policyengine.github.io/stronger-start-calc/dynamic-avg-benefit-by-decile.html")


if __name__ == "__main__":
    main()
