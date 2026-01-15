"""Calculate 10-year budget impact for Stronger Start for Working Families Act.

This module estimates the federal revenue impact from 2026 to 2035.
"""

from dataclasses import dataclass


@dataclass
class YearlyImpact:
    """Impact data for a single year."""
    year: int
    cost_millions: float
    cumulative_cost_millions: float


def calculate_ten_year_impact(
    base_year_cost_millions: float = 1593,
    start_year: int = 2026,
    end_year: int = 2035,
    annual_growth_rate: float = 0.02,
) -> tuple[list[YearlyImpact], float]:
    """
    Calculate the 10-year budget impact of the Stronger Start for Working Families Act.

    The reform eliminates the $2,500 earnings threshold for the refundable CTC.
    We project costs forward assuming modest annual growth due to:
    - Population growth
    - Wage growth (more families reaching benefit levels)
    - Inflation adjustments to CTC parameters

    Args:
        base_year_cost_millions: Cost in the first year (2026), default $789 million
        start_year: First year of the budget window
        end_year: Last year of the budget window
        annual_growth_rate: Annual growth rate for cost projections (default 2%)

    Returns:
        Tuple of (list of YearlyImpact objects, total 10-year cost in millions)
    """
    yearly_impacts = []
    cumulative_cost = 0

    for i, year in enumerate(range(start_year, end_year + 1)):
        # Apply growth rate for years after the base year
        year_cost = base_year_cost_millions * ((1 + annual_growth_rate) ** i)
        cumulative_cost += year_cost

        yearly_impacts.append(
            YearlyImpact(
                year=year,
                cost_millions=round(year_cost, 1),
                cumulative_cost_millions=round(cumulative_cost, 1),
            )
        )

    return yearly_impacts, round(cumulative_cost, 1)


def format_impact_table(yearly_impacts: list[YearlyImpact]) -> str:
    """Format yearly impacts as a markdown table."""
    lines = [
        "| Year | Annual Cost ($ millions) | Cumulative Cost ($ millions) |",
        "|------|--------------------------|------------------------------|",
    ]

    for impact in yearly_impacts:
        lines.append(
            f"| {impact.year} | {impact.cost_millions:,.1f} | {impact.cumulative_cost_millions:,.1f} |"
        )

    return "\n".join(lines)


def main():
    """Print the 10-year impact analysis."""
    print("=" * 60)
    print("Stronger Start for Working Families Act")
    print("10-Year Budget Impact (2026-2035)")
    print("=" * 60)
    print()

    yearly_impacts, total_cost = calculate_ten_year_impact()

    print(format_impact_table(yearly_impacts))
    print()
    print(f"Total 10-Year Cost: ${total_cost / 1000:.2f} billion")
    print()
    print("Notes:")
    print("- Base year (2026) cost: $1,593 million from PolicyEngine simulation (enhanced_cps)")
    print("- Annual growth rate: 2% (accounts for population and wage growth)")
    print("- Assumes no changes to CTC parameters or eligibility rules")
    print()

    # Also calculate with different growth assumptions
    print("-" * 60)
    print("Sensitivity Analysis:")
    print("-" * 60)

    for rate_name, rate in [("0% growth", 0.0), ("2% growth", 0.02), ("3% growth", 0.03)]:
        _, total = calculate_ten_year_impact(annual_growth_rate=rate)
        print(f"  {rate_name}: ${total / 1000:.2f} billion over 10 years")


if __name__ == "__main__":
    main()
