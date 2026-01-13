"""Statewide impact data for Stronger Start for Working Families Act.

Data sourced from PolicyEngine simulation:
https://app.policyengine.org/us/report-output/sur-mk5steto8pe9
"""

# Income deciles (1-10)
DECILES = list(range(1, 11))

# Percentage of population by outcome category for each decile
# Benefits concentrated in lower income deciles where families
# have earnings but don't maximize the refundable CTC
GAIN_MORE_THAN_5PCT = [0.7, 0, 0, 0, 0, 0, 0, 0, 0, 0]
GAIN_LESS_THAN_5PCT = [4.7, 5.7, 7.7, 5.1, 3.5, 3.2, 1.7, 1.1, 0.6, 0.3]
NO_CHANGE = [94.6, 94.3, 92.3, 94.9, 96.5, 96.8, 98.3, 98.9, 99.4, 99.7]
LOSS_LESS_THAN_5PCT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
LOSS_MORE_THAN_5PCT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Overall population totals
ALL_GAIN_MORE_THAN_5PCT = 0.1
ALL_GAIN_LESS_THAN_5PCT = 3.3
ALL_NO_CHANGE = 96.6
ALL_LOSS_LESS_THAN_5PCT = 0
ALL_LOSS_MORE_THAN_5PCT = 0

# Average impact by decile (in dollars)
# Higher benefits in lower deciles where the reform has most effect
AVG_IMPACT_BY_DECILE = [8, 9, 11, 8, 6, 5, 3, 2, 1, 1]

# Key statistics from PolicyEngine simulation
REVENUE_IMPACT_MILLIONS = -789  # Costs $789 million
PERCENT_BENEFITING = 3.4
CHILD_POVERTY_IMPACT_PCT = -0.11  # Reduces child poverty by 0.11%
DEEP_CHILD_POVERTY_IMPACT_PCT = 0.0  # No effect on deep child poverty
GINI_IMPACT_PCT = -0.017  # Reduces Gini by 0.017%
AVG_BENEFIT_PER_HOUSEHOLD = 6
