"""Statewide impact data for Stronger Start for Working Families Act.

Data sourced from PolicyEngine simulation:
https://app.policyengine.org/us/report-output/sur-mk5steto8pe9
"""

# Income deciles (1-10)
DECILES = list(range(1, 11))

# Percentage of population by outcome category for each decile
# Benefits concentrated in lower income deciles where families
# have earnings but don't maximize the refundable CTC
GAIN_MORE_THAN_5PCT = [0.4, 0.1, 0, 0, 0, 0, 0, 0, 0, 0]
GAIN_LESS_THAN_5PCT = [5.5, 9.2, 7.8, 6.1, 4.2, 2.8, 1.5, 0.8, 0.3, 0.1]
NO_CHANGE = [94.1, 90.7, 92.2, 93.9, 95.8, 97.2, 98.5, 99.2, 99.7, 99.9]
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
AVG_IMPACT_BY_DECILE = [24, 31, 20, 12, 7, 4, 2, 1, 0, 0]

# Key statistics from PolicyEngine simulation
REVENUE_IMPACT_MILLIONS = -789  # Costs $789 million
PERCENT_BENEFITING = 3.4
CHILD_POVERTY_IMPACT_PCT = -0.11  # Reduces child poverty by 0.11%
DEEP_CHILD_POVERTY_IMPACT_PCT = 0.0  # No effect on deep child poverty
GINI_IMPACT_PCT = -0.017  # Reduces Gini by 0.017%
AVG_BENEFIT_PER_HOUSEHOLD = 6
