"""Household impact calculations for Stronger Start for Working Families Act."""


def calculate_net_income_changes(
    filing_status: str = "single",
    num_children: int = 2,
    min_income: int = 0,
    max_income: int = 50000,
    step: int = 100,
) -> tuple[list[int], list[float]]:
    """
    Calculate change in net income for different household types.

    The reform eliminates the $2,500 earnings threshold for the refundable
    portion of the Child Tax Credit. The benefit is 15% of the eliminated
    threshold range, maxing out at $375 (15% * $2,500).

    Args:
        filing_status: "single" or "joint" (doesn't affect the benefit calculation)
        num_children: Number of children (1-3) (doesn't affect max $375 benefit)
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


def calculate_baseline_reform_comparison(
    min_income: int = 0,
    max_income: int = 20000,
    step: int = 100,
) -> tuple[list[int], list[float], list[float]]:
    """
    Calculate refundable CTC for baseline and reform scenarios.

    The refundable CTC phases in at 15% of earnings above a threshold:
    - Baseline: $2,500 threshold
    - Reform: $0 threshold
    Maximum refundable amount is $1,700 in 2026.

    This calculation is the same for all filing statuses and numbers of children.

    Args:
        min_income: Minimum employment income to calculate
        max_income: Maximum employment income to calculate
        step: Income increment step size

    Returns:
        Tuple of (employment_income_values, baseline_credits, reform_credits)
    """
    employment_income_values = list(range(min_income, max_income + 1, step))
    baseline_credits = []
    reform_credits = []

    PHASE_IN_RATE = 0.15
    MAX_REFUNDABLE = 1700
    BASELINE_THRESHOLD = 2500
    REFORM_THRESHOLD = 0

    for income in employment_income_values:
        # Baseline: phases in from $2,500
        if income <= BASELINE_THRESHOLD:
            baseline_credit = 0
        else:
            baseline_credit = min(
                (income - BASELINE_THRESHOLD) * PHASE_IN_RATE, MAX_REFUNDABLE
            )

        # Reform: phases in from $0
        reform_credit = min(income * PHASE_IN_RATE, MAX_REFUNDABLE)

        baseline_credits.append(baseline_credit)
        reform_credits.append(reform_credit)

    return employment_income_values, baseline_credits, reform_credits
