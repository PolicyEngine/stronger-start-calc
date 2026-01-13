"""Generate blog post assets for Stronger Start for Working Families Act analysis."""

import os
from pathlib import Path

from stronger_start import (
    create_net_income_change_chart,
    create_winners_by_decile_chart,
    create_avg_benefit_by_decile_chart,
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
    """Generate all chart files."""
    # Create output directories
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating charts for Stronger Start for Working Families Act...")
    print()

    # Generate each chart
    print("Creating net income change chart...")
    fig1 = create_net_income_change_chart()
    generate_chart_html(
        fig1,
        "Net Income Change - Stronger Start for Working Families Act",
        "net-income-change.html",
    )

    print("Creating winners by decile chart...")
    fig2 = create_winners_by_decile_chart()
    generate_chart_html(
        fig2,
        "Winners by Income Decile - Stronger Start for Working Families Act",
        "winners-by-decile.html",
    )

    print("Creating average benefit by decile chart...")
    fig3 = create_avg_benefit_by_decile_chart()
    generate_chart_html(
        fig3,
        "Average Benefit by Income Decile - Stronger Start for Working Families Act",
        "avg-benefit-by-decile.html",
    )

    print()
    print("Done! Charts generated in output/charts/")
    print()
    print("Chart URLs after deployment:")
    print("  https://policyengine.github.io/stronger-start-calc/net-income-change.html")
    print("  https://policyengine.github.io/stronger-start-calc/winners-by-decile.html")
    print("  https://policyengine.github.io/stronger-start-calc/avg-benefit-by-decile.html")


if __name__ == "__main__":
    main()
