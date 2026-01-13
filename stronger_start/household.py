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

    Phase-out ranges vary by number of children:
    - 1 child: $11,333 to $13,833
    - 2 children: $22,667 to $25,167
    - 3 children: $34,000 to $36,500

    Args:
        filing_status: "single" or "joint" (doesn't affect the benefit calculation)
        num_children: Number of children (1-3)
        min_income: Minimum employment income to calculate
        max_income: Maximum employment income to calculate
        step: Income increment step size

    Returns:
        Tuple of (employment_income_values, net_income_changes)
    """
    employment_income_values = list(range(min_income, max_income + 1, step))
    net_income_changes = []

    # Calculate phase-out range based on number of children
    # Max refundable CTC is $1,700 per child
    # Reform reaches max at: ($1,700 * num_children) / 0.15
    # Baseline reaches max at: reform_max + $2,500
    max_refundable_per_child = 1700
    phase_in_rate = 0.15
    baseline_threshold = 2500
    max_benefit = baseline_threshold * phase_in_rate  # $375

    reform_reaches_max = (max_refundable_per_child * num_children) / phase_in_rate
    baseline_reaches_max = reform_reaches_max + baseline_threshold

    for income in employment_income_values:
        if income == 0:
            # No earnings = no refundable CTC under either baseline or reform
            change = 0
        elif income <= baseline_threshold:
            # Reform gives 15% of income from first dollar
            # Baseline gives 0 for income <= $2,500
            # Phases in from $0 to $2,500, reaching $375
            change = income * phase_in_rate
        elif income <= reform_reaches_max:
            # Maximum benefit of $375 between $2,500 and when reform reaches max
            change = max_benefit
        elif income <= baseline_reaches_max:
            # Phases out as baseline catches up to reform
            # change = $375 - (income - reform_reaches_max) * 0.15
            change = max_benefit - (income - reform_reaches_max) * phase_in_rate
        else:
            # Above baseline_reaches_max, no benefit (both give full refundable credit)
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
