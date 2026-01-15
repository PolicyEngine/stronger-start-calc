"""Run PolicyEngine microsimulation to calculate budget impact.

Uses enhanced_cps dataset (the default) for estimates.
"""

from policyengine_us import Microsimulation

from .reform import stronger_start_reform


def calculate_budget_impact(year: int = 2026) -> dict:
    """
    Calculate the budget impact of the Stronger Start reform using microsimulation.

    Args:
        year: The tax year to simulate

    Returns:
        Dictionary with budget impact metrics
    """
    print(f"Running baseline simulation for {year}...")
    baseline = Microsimulation()
    dataset_name = baseline.dataset.name

    print(f"Using dataset: {dataset_name}")
    print(f"Running reform simulation for {year}...")
    reform = Microsimulation(reform=stronger_start_reform)

    # Calculate federal income tax revenue at tax_unit level
    baseline_revenue = baseline.calculate("income_tax", period=year)
    reform_revenue = reform.calculate("income_tax", period=year)

    # Get tax unit weights
    baseline_weights = baseline.calculate("tax_unit_weight", period=year)

    # MicroSeries.sum() gives weighted sum, .values.sum() gives unweighted
    # Use weighted sum for totals
    baseline_total = baseline_revenue.sum()  # Weighted sum
    reform_total = reform_revenue.sum()  # Weighted sum

    # Revenue impact (negative = cost to government)
    revenue_impact = reform_total - baseline_total

    # Calculate number of beneficiaries (at tax_unit level)
    baseline_ctc = baseline.calculate("refundable_ctc", period=year)
    reform_ctc = reform.calculate("refundable_ctc", period=year)

    benefit_amount = reform_ctc.values - baseline_ctc.values
    # Count beneficiaries using weights
    beneficiaries = (baseline_weights.values[benefit_amount > 0]).sum()
    total_tax_units = baseline_weights.values.sum()
    pct_benefiting = (beneficiaries / total_tax_units) * 100

    return {
        "year": year,
        "dataset": dataset_name,
        "baseline_revenue_billions": baseline_total / 1e9,
        "reform_revenue_billions": reform_total / 1e9,
        "revenue_impact_millions": revenue_impact / 1e6,
        "cost_millions": -revenue_impact / 1e6,  # Cost is negative of revenue impact
        "benefiting_tax_units": beneficiaries,
        "total_tax_units": total_tax_units,
        "pct_benefiting": pct_benefiting,
    }


def main():
    """Run the simulation and print results."""
    print("=" * 60)
    print("Stronger Start for Working Families Act")
    print("Budget Impact Simulation (enhanced_cps)")
    print("=" * 60)
    print()

    results = calculate_budget_impact()

    print()
    print("-" * 60)
    print("Results:")
    print("-" * 60)
    print(f"Year: {results['year']}")
    print(f"Dataset: {results['dataset']}")
    print()
    print(f"Baseline Federal Revenue: ${results['baseline_revenue_billions']:.2f} billion")
    print(f"Reform Federal Revenue: ${results['reform_revenue_billions']:.2f} billion")
    print()
    print(f"Revenue Impact: ${results['revenue_impact_millions']:.1f} million")
    print(f"Cost to Government: ${results['cost_millions']:.1f} million")
    print()
    print(f"Benefiting Tax Units: {results['benefiting_tax_units']:,.0f}")
    print(f"Percent of Tax Units Benefiting: {results['pct_benefiting']:.2f}%")
    print()
    print("-" * 60)
    print("To update ten_year_impact.py, use:")
    print(f"  base_year_cost_millions = {results['cost_millions']:.0f}")
    print("-" * 60)


if __name__ == "__main__":
    main()
