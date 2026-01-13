"""Household impact calculations for Stronger Start for Working Families Act."""


def calculate_net_income_changes(
    min_income: int = 0,
    max_income: int = 50000,
    step: int = 100,
) -> tuple[list[int], list[float]]:
    """
    Calculate change in net income for a single parent with two children.

    The reform eliminates the $2,500 earnings threshold for the refundable
    portion of the Child Tax Credit. The benefit is 15% of the eliminated
    threshold range, maxing out at $375 (15% * $2,500).

    Args:
        min_income: Minimum employment income to calculate
        max_income: Maximum employment income to calculate
        step: Income increment step size

    Returns:
        Tuple of (employment_income_values, net_income_changes)
    """
    employment_income_values = list(range(min_income, max_income + 1, step))
    net_income_changes = []

    for income in employment_income_values:
        if income == 0:
            # No earnings = no refundable CTC under either baseline or reform
            change = 0
        elif income <= 2500:
            # Reform gives 15% of income from first dollar
            # Baseline gives 15% of (income - 2500) = 0 for income <= 2500
            change = income * 0.15
        else:
            # Both give 15% * (income - threshold)
            # Difference is 15% * 2500 = $375
            change = 375

        net_income_changes.append(change)

    return employment_income_values, net_income_changes
