"""Statewide impact data for Stronger Start for Working Families Act.

Data sourced from PolicyEngine simulation:
https://app.policyengine.org/us/report-output/sur-mk5steto8pe9
"""

# Income deciles (1-10)
DECILES = list(range(1, 11))

# Percentage of population by outcome category for each decile
# Benefits concentrated in lower income deciles where families
# have earnings but don't maximize the refundable CTC
GAIN_MORE_THAN_5PCT = [1.4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
GAIN_LESS_THAN_5PCT = [6.8, 7.9, 14, 10.5, 7.9, 4.4, 1.8, 1.7, 0.6, 2.2]
NO_CHANGE = [91.8, 92.1, 86, 89.5, 92.1, 95.6, 98.2, 98.3, 99.4, 97.8]
LOSS_LESS_THAN_5PCT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
LOSS_MORE_THAN_5PCT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Overall population totals
ALL_GAIN_MORE_THAN_5PCT = 0.1
ALL_GAIN_LESS_THAN_5PCT = 5.8
ALL_NO_CHANGE = 94.1
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
