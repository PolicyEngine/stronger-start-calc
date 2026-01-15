"""Calculate 10-year budget impact by running simulation for each year."""

from policyengine_us import Microsimulation

from .reform import stronger_start_reform


def calculate_yearly_cost(year: int) -> float:
    """Calculate the cost for a specific year using microsimulation."""
    print(f"  Simulating {year}...", end=" ", flush=True)

    baseline = Microsimulation()
    reform = Microsimulation(reform=stronger_start_reform)

    baseline_revenue = baseline.calculate("income_tax", period=year)
    reform_revenue = reform.calculate("income_tax", period=year)

    baseline_total = baseline_revenue.sum()
    reform_total = reform_revenue.sum()

    cost_millions = -(reform_total - baseline_total) / 1e6
    print(f"${cost_millions:,.0f}M")

    return cost_millions


def main():
    """Run simulation for each year 2026-2035 and calculate total."""
    print("=" * 60)
    print("Stronger Start for Working Families Act")
    print("10-Year Budget Impact (2026-2035)")
    print("Using enhanced_cps simulation for each year")
    print("=" * 60)
    print()

    years = list(range(2026, 2036))
    yearly_costs = []

    print("Calculating costs by year:")
    for year in years:
        cost = calculate_yearly_cost(year)
        yearly_costs.append(cost)

    print()
    print("-" * 60)
    print("Results:")
    print("-" * 60)
    print()
    print("| Year | Cost ($ millions) |")
    print("|------|-------------------|")

    cumulative = 0
    for year, cost in zip(years, yearly_costs):
        cumulative += cost
        print(f"| {year} | {cost:,.0f} |")

    print()
    print(f"Total 10-Year Cost: ${cumulative / 1000:.2f} billion")
    print("-" * 60)


if __name__ == "__main__":
    main()
