"""Stronger Start for Working Families Act analysis package."""

from .reform import stronger_start_reform
from .household import calculate_net_income_changes
from .statewide import (
    DECILES,
    GAIN_MORE_THAN_5PCT,
    GAIN_LESS_THAN_5PCT,
    NO_CHANGE,
    LOSS_LESS_THAN_5PCT,
    LOSS_MORE_THAN_5PCT,
    ALL_GAIN_MORE_THAN_5PCT,
    ALL_GAIN_LESS_THAN_5PCT,
    ALL_NO_CHANGE,
    ALL_LOSS_LESS_THAN_5PCT,
    ALL_LOSS_MORE_THAN_5PCT,
    AVG_IMPACT_BY_DECILE,
    REVENUE_IMPACT_MILLIONS,
    PERCENT_BENEFITING,
    CHILD_POVERTY_IMPACT_PCT,
    DEEP_CHILD_POVERTY_IMPACT_PCT,
    GINI_IMPACT_PCT,
    AVG_BENEFIT_PER_HOUSEHOLD,
)
from .charts import (
    create_net_income_change_chart,
    create_baseline_reform_comparison_chart,
    create_winners_by_decile_chart,
    create_avg_benefit_by_decile_chart,
)
from .ten_year_impact import (
    calculate_ten_year_impact,
    format_impact_table,
    YearlyImpact,
)
from .dynamic_charts import (
    calculate_decile_impacts,
    create_dynamic_winners_by_decile_chart,
    create_dynamic_avg_benefit_by_decile_chart,
    create_dynamic_net_income_change_chart,
    create_dynamic_baseline_reform_chart,
)

__all__ = [
    "stronger_start_reform",
    "calculate_net_income_changes",
    "DECILES",
    "GAIN_MORE_THAN_5PCT",
    "GAIN_LESS_THAN_5PCT",
    "NO_CHANGE",
    "LOSS_LESS_THAN_5PCT",
    "LOSS_MORE_THAN_5PCT",
    "ALL_GAIN_MORE_THAN_5PCT",
    "ALL_GAIN_LESS_THAN_5PCT",
    "ALL_NO_CHANGE",
    "ALL_LOSS_LESS_THAN_5PCT",
    "ALL_LOSS_MORE_THAN_5PCT",
    "AVG_IMPACT_BY_DECILE",
    "REVENUE_IMPACT_MILLIONS",
    "PERCENT_BENEFITING",
    "CHILD_POVERTY_IMPACT_PCT",
    "DEEP_CHILD_POVERTY_IMPACT_PCT",
    "GINI_IMPACT_PCT",
    "AVG_BENEFIT_PER_HOUSEHOLD",
    "create_net_income_change_chart",
    "create_baseline_reform_comparison_chart",
    "create_winners_by_decile_chart",
    "create_avg_benefit_by_decile_chart",
    "calculate_ten_year_impact",
    "format_impact_table",
    "YearlyImpact",
    # Dynamic charts (microsimulation-based)
    "calculate_decile_impacts",
    "create_dynamic_winners_by_decile_chart",
    "create_dynamic_avg_benefit_by_decile_chart",
    "create_dynamic_net_income_change_chart",
    "create_dynamic_baseline_reform_chart",
]
