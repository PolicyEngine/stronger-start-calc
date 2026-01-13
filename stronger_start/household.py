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
            # Phases in from $0 to $2,500, reaching $375
            change = income * 0.15
        elif income <= 22667:
            # Maximum benefit of $375 between $2,500 and $22,667
            change = 375
        elif income <= 25167:
            # Phases out from $22,667 to $25,167 at 15% rate
            # change = 375 - (income - 22667) * 0.15
            change = 375 - (income - 22667) * 0.15
        else:
            # Above $25,167, no benefit
            change = 0

        net_income_changes.append(change)

    return employment_income_values, net_income_changes
