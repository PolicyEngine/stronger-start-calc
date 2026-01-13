"""Stronger Start for Working Families Act reform definition."""

from policyengine_core.reforms import Reform

# Define the reform: eliminate the $2,500 earnings threshold for refundable CTC
stronger_start_reform = Reform.from_dict(
    {"gov.irs.credits.ctc.refundable.phase_in.threshold": {"2026-01-01.2100-12-31": 0}},
    country_id="us",
)
