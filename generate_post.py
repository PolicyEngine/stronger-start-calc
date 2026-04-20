"""Generate blog post assets for Stronger Start for Working Families Act analysis."""

import os
from pathlib import Path

from stronger_start import (
    create_net_income_change_chart,
    create_baseline_reform_comparison_chart,
    create_winners_by_decile_chart,
    create_avg_benefit_by_decile_chart,
)

# Output directories
OUTPUT_DIR = Path("output")
CHARTS_DIR = OUTPUT_DIR / "charts"

# Base URL for GitHub Pages
BASE_URL = "https://policyengine.github.io/stronger-start-calc"

# HTML template for standalone chart files
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | PolicyEngine</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="theme-color" content="#319795">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="PolicyEngine">
    <meta property="og:image" content="https://policyengine.org/images/logos/policyengine/profile/PNG/policyengine-logo-teal.png">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="https://policyengine.org/images/logos/policyengine/profile/PNG/policyengine-logo-teal.png">

    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "{title}",
        "description": "{description}",
        "url": "{canonical_url}",
        "creator": {{
            "@type": "Organization",
            "name": "PolicyEngine",
            "url": "https://policyengine.org"
        }},
        "license": "https://opensource.org/licenses/MIT",
        "keywords": ["Child Tax Credit", "Stronger Start", "Working Families Act", "tax policy", "policy analysis"]
    }}
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-2YHG89FY0N"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-2YHG89FY0N', {{ tool_name: 'stronger-start-calc' }});
    </script>
    <script>
    (function() {{
      var TOOL_NAME = 'stronger-start-calc';
      if (typeof window === 'undefined' || !window.gtag) return;

      var scrollFired = {{}};
      window.addEventListener('scroll', function() {{
        var docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight <= 0) return;
        var pct = Math.floor((window.scrollY / docHeight) * 100);
        [25, 50, 75, 100].forEach(function(m) {{
          if (pct >= m && !scrollFired[m]) {{
            scrollFired[m] = true;
            window.gtag('event', 'scroll_depth', {{ percent: m, tool_name: TOOL_NAME }});
          }}
        }});
      }}, {{ passive: true }});

      [30, 60, 120, 300].forEach(function(sec) {{
        setTimeout(function() {{
          if (document.visibilityState !== 'hidden') {{
            window.gtag('event', 'time_on_tool', {{ seconds: sec, tool_name: TOOL_NAME }});
          }}
        }}, sec * 1000);
      }});

      document.addEventListener('click', function(e) {{
        var link = e.target && e.target.closest ? e.target.closest('a') : null;
        if (!link || !link.href) return;
        try {{
          var url = new URL(link.href, window.location.origin);
          if (url.hostname && url.hostname !== window.location.hostname) {{
            window.gtag('event', 'outbound_click', {{
              url: link.href,
              target_hostname: url.hostname,
              tool_name: TOOL_NAME
            }});
          }}
        }} catch (err) {{}}
      }});
    }})();
    </script>
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
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}
    </style>
</head>
<body>
    <main>
        <article>
            <h1 class="sr-only">{title}</h1>
            <div id="chart" role="img" aria-label="{title}"></div>
            <noscript>
                <p>This interactive chart requires JavaScript to display. It shows: {description}</p>
            </noscript>
        </article>
    </main>
    <script>
        var figure = {figure_json};
        Plotly.newPlot('chart', figure.data, figure.layout, {{responsive: true}});
    </script>
</body>
</html>
"""


def generate_chart_html(fig, title: str, filename: str, description: str) -> None:
    """Generate standalone HTML file for a Plotly chart."""
    canonical_url = f"{BASE_URL}/{filename}"
    html_content = HTML_TEMPLATE.format(
        title=title,
        description=description,
        canonical_url=canonical_url,
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
    print("Creating baseline vs reform comparison chart...")
    fig1 = create_baseline_reform_comparison_chart()
    generate_chart_html(
        fig1,
        "Baseline vs Reform - Stronger Start for Working Families Act",
        "baseline-reform-comparison.html",
        "Comparison of the refundable Child Tax Credit phase-in under current law versus the Stronger Start for Working Families Act reform, which eliminates the $2,500 earnings requirement.",
    )

    print("Creating net income change chart...")
    fig2 = create_net_income_change_chart()
    generate_chart_html(
        fig2,
        "Net Income Change - Stronger Start for Working Families Act",
        "net-income-change.html",
        "Chart showing the change in net income by employment income under the Stronger Start for Working Families Act for households with 1, 2, or 3 children.",
    )

    print("Creating winners by decile chart...")
    fig3 = create_winners_by_decile_chart()
    generate_chart_html(
        fig3,
        "Winners by Income Decile - Stronger Start for Working Families Act",
        "winners-by-decile.html",
        "Breakdown of winners and losers by income decile under the Stronger Start for Working Families Act. About 3.4% of Americans benefit, concentrated in the lowest income deciles.",
    )

    print("Creating average benefit by decile chart...")
    fig4 = create_avg_benefit_by_decile_chart()
    generate_chart_html(
        fig4,
        "Average Benefit by Income Decile - Stronger Start for Working Families Act",
        "avg-benefit-by-decile.html",
        "Average household benefit of the Stronger Start for Working Families Act by income decile. Lower-income deciles receive the largest benefits, up to $11 per household on average.",
    )

    print()
    print("Done! Charts generated in output/charts/")
    print()
    print("Chart URLs after deployment:")
    print(
        "  https://policyengine.github.io/stronger-start-calc/baseline-reform-comparison.html"
    )
    print("  https://policyengine.github.io/stronger-start-calc/net-income-change.html")
    print("  https://policyengine.github.io/stronger-start-calc/winners-by-decile.html")
    print(
        "  https://policyengine.github.io/stronger-start-calc/avg-benefit-by-decile.html"
    )


if __name__ == "__main__":
    main()
