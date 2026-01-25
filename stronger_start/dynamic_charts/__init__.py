"""Dynamic charts module using PolicyEngine microsimulation.

This module generates charts using live microsimulation data from PolicyEngine-US
rather than hardcoded values.
"""

from .microsim import calculate_decile_impacts
from .charts import (
    create_dynamic_winners_by_decile_chart,
    create_dynamic_avg_benefit_by_decile_chart,
    create_dynamic_net_income_change_chart,
    create_dynamic_baseline_reform_chart,
)

__all__ = [
    "calculate_decile_impacts",
    "create_dynamic_winners_by_decile_chart",
    "create_dynamic_avg_benefit_by_decile_chart",
    "create_dynamic_net_income_change_chart",
    "create_dynamic_baseline_reform_chart",
]
