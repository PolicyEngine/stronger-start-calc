"""Dynamic chart generation functions using PolicyEngine microsimulation.

These charts use live microsimulation data rather than hardcoded values.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..household import calculate_net_income_changes, calculate_baseline_reform_comparison

# PolicyEngine app-v2 color palette
BLACK = "#000000"
PRIMARY_500 = "#319795"  # Main teal brand color
PRIMARY_700 = "#285E61"  # Dark teal for gains >5%
PRIMARY_ALPHA_60 = "rgba(49, 151, 149, 0.6)"  # Teal with 60% opacity
GRAY_200 = "#E5E7EB"  # No change
GRAY_400 = "#9CA3AF"  # Loss <5%
GRAY_600 = "#4B5563"  # Loss >5%

# Additional colors for multi-scenario charts
TEAL_LIGHT = "rgba(49, 151, 149, 0.4)"  # Lighter teal for 1 child
TEAL_MEDIUM = "rgba(49, 151, 149, 0.7)"  # Medium teal for 2 children
TEAL_DARK = "#285E61"  # Dark teal for 3 children

# Chart watermark configuration
WATERMARK_CONFIG = {
    "source": "https://policyengine.github.io/utah-sb60-calc/assets/teal-square-transparent.png",
    "xref": "paper",
    "yref": "paper",
    "sizex": 0.07,
    "sizey": 0.07,
    "xanchor": "right",
    "yanchor": "bottom",
}


def create_dynamic_winners_by_decile_chart(microsim_data: dict) -> go.Figure:
    """
    Create Winners/Losers by decile chart using microsimulation data.

    Args:
        microsim_data: Dictionary from calculate_decile_impacts() containing
            decile_outcomes and all_outcomes

    Returns:
        Plotly figure object
    """
    decile_outcomes = microsim_data["decile_outcomes"]
    all_outcomes = microsim_data["all_outcomes"]

    labels_deciles = [str(i) for i in range(1, 11)]

    df_deciles = pd.DataFrame(
        {
            "Income decile": labels_deciles,
            "Gain more than 5%": decile_outcomes["gain_more_than_5pct"],
            "Gain less than 5%": decile_outcomes["gain_less_than_5pct"],
            "No change": decile_outcomes["no_change"],
            "Lose less than 5%": decile_outcomes["loss_less_than_5pct"],
            "Lose more than 5%": decile_outcomes["loss_more_than_5pct"],
        }
    )

    df_all = pd.DataFrame(
        {
            "Income decile": ["All"],
            "Gain more than 5%": [all_outcomes["gain_more_than_5pct"]],
            "Gain less than 5%": [all_outcomes["gain_less_than_5pct"]],
            "No change": [all_outcomes["no_change"]],
            "Lose less than 5%": [all_outcomes["loss_less_than_5pct"]],
            "Lose more than 5%": [all_outcomes["loss_more_than_5pct"]],
        }
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.1, 0.9],
    )

    # Colors
    COLOR_GAIN_MORE = PRIMARY_700
    COLOR_GAIN_LESS = PRIMARY_ALPHA_60
    COLOR_NO_CHANGE = GRAY_200
    COLOR_LOSS_LESS = GRAY_400
    COLOR_LOSS_MORE = GRAY_600

    # Add traces for "All" category - first row
    _add_stacked_bar_traces(
        fig,
        df_all,
        COLOR_GAIN_MORE,
        COLOR_GAIN_LESS,
        COLOR_NO_CHANGE,
        COLOR_LOSS_LESS,
        COLOR_LOSS_MORE,
        row=1,
        show_legend=True,
    )

    # Add traces for deciles - second row
    _add_stacked_bar_traces(
        fig,
        df_deciles,
        COLOR_GAIN_MORE,
        COLOR_GAIN_LESS,
        COLOR_NO_CHANGE,
        COLOR_LOSS_LESS,
        COLOR_LOSS_MORE,
        row=2,
        show_legend=False,
    )

    fig.update_layout(
        barmode="stack",
        title=dict(
            text="Figure 3: Winners of Stronger Start for Working Families Act by income decile",
            x=0,
        ),
        font=dict(family="Roboto Serif"),
        xaxis=dict(
            title=dict(text=""),
            ticksuffix="%",
            range=[0, 100],
            showgrid=False,
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis2=dict(
            title=dict(text="Population share"),
            ticksuffix="%",
            range=[0, 100],
            fixedrange=True,
        ),
        yaxis=dict(
            title=dict(text=""),
            tickvals=["All"],
        ),
        yaxis2=dict(
            title=dict(text="Income decile"),
            automargin=True,
        ),
        legend=dict(
            title=dict(text=""),
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(size=10),
        ),
        font_color=BLACK,
        margin={"l": 60, "r": 60, "b": 100, "t": 120, "pad": 4},
        height=580,
        width=800,
        uniformtext=dict(
            mode="hide",
            minsize=8,
        ),
        images=[
            {
                **WATERMARK_CONFIG,
                "sizex": 0.09,
                "sizey": 0.09,
                "x": 1.05,
                "y": -0.20,
            }
        ],
    )

    return fig


def _add_stacked_bar_traces(
    fig: go.Figure,
    df: pd.DataFrame,
    color_gain_more: str,
    color_gain_less: str,
    color_no_change: str,
    color_loss_less: str,
    color_loss_more: str,
    row: int,
    show_legend: bool,
) -> None:
    """Add stacked bar traces to a figure."""
    categories = [
        ("Gain more than 5%", "Gain >5%", color_gain_more, None),
        ("Gain less than 5%", "Gain <5%", color_gain_less, BLACK),
        ("No change", "No change", color_no_change, BLACK),
        ("Lose less than 5%", "Loss <5%", color_loss_less, None),
        ("Lose more than 5%", "Loss >5%", color_loss_more, None),
    ]

    for col_name, legend_name, color, text_color in categories:
        text_kwargs = {}
        if text_color:
            text_kwargs["textfont"] = dict(color=text_color)

        fig.add_trace(
            go.Bar(
                y=df["Income decile"],
                x=df[col_name],
                name=legend_name,
                orientation="h",
                marker_color=color,
                text=[f"{x:.0f}%" if x > 0 else "" for x in df[col_name]],
                textposition="inside",
                textangle=0,
                legendgroup=col_name.lower().replace(" ", "_"),
                showlegend=show_legend,
                hovertemplate="%{x:.1f}%<extra></extra>",
                **text_kwargs,
            ),
            row=row,
            col=1,
        )


def create_dynamic_avg_benefit_by_decile_chart(microsim_data: dict) -> go.Figure:
    """
    Create average benefit by decile chart using microsimulation data.

    Args:
        microsim_data: Dictionary from calculate_decile_impacts() containing
            avg_impact_by_decile

    Returns:
        Plotly figure object
    """
    avg_impact = microsim_data["avg_impact_by_decile"]

    df = pd.DataFrame(
        {
            "Income decile": list(range(1, 11)),
            "Average impact": avg_impact,
        }
    )

    dollar_text = [f"${int(x)}" for x in avg_impact]

    fig = (
        px.bar(
            df,
            x="Income decile",
            y="Average impact",
            text=dollar_text,
            color_discrete_sequence=[PRIMARY_500],
            title="Figure 3: Average benefit of Stronger Start for Working Families Act by income decile",
        )
        .update_layout(
            font=dict(family="Roboto Serif"),
            xaxis=dict(
                title=dict(text="Income decile"),
                tickvals=list(range(1, 11)),
                fixedrange=True,
            ),
            yaxis=dict(
                title=dict(text="Absolute change in household income"),
                tickformat=",",
                tickprefix="$",
                fixedrange=True,
            ),
            showlegend=False,
            font_color=BLACK,
            margin={"l": 60, "r": 60, "b": 80, "t": 80, "pad": 4},
            images=[
                {
                    **WATERMARK_CONFIG,
                    "x": 1.05,
                    "y": -0.18,
                }
            ],
        )
        .update_traces(
            hovertemplate="Income decile: %{x}<br>Average impact: $%{y:,.0f}<extra></extra>"
        )
    )

    return fig


def create_dynamic_net_income_change_chart() -> go.Figure:
    """
    Create net income change chart showing all 3 child scenarios simultaneously.

    This redesigned chart shows 1, 2, and 3 children scenarios as separate lines
    without a dropdown menu, making it easier to compare scenarios.

    Returns:
        Plotly figure object
    """
    fig = go.Figure()

    # Line styles for each scenario
    line_configs = [
        {"num_children": 1, "color": TEAL_LIGHT, "dash": "dot", "name": "1 child"},
        {"num_children": 2, "color": PRIMARY_500, "dash": "solid", "name": "2 children"},
        {"num_children": 3, "color": TEAL_DARK, "dash": "dash", "name": "3 children"},
    ]

    for config in line_configs:
        employment_incomes, net_income_changes = calculate_net_income_changes(
            filing_status="single", num_children=config["num_children"]
        )

        fig.add_trace(
            go.Scatter(
                x=employment_incomes,
                y=net_income_changes,
                name=config["name"],
                mode="lines",
                line=dict(color=config["color"], width=3, dash=config["dash"]),
                hovertemplate=(
                    f"{config['name']}<br>"
                    "Employment income: $%{x:,}<br>"
                    "Change in net income: $%{y:.2f}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title="Figure 2: Change in net income from the Stronger Start for Working Families Act",
        font=dict(family="Roboto Serif", color=BLACK),
        xaxis=dict(
            title=dict(text="Employment income"),
            tickformat=",",
            tickprefix="$",
            fixedrange=True,
        ),
        yaxis=dict(
            title=dict(text="Change in net income"),
            tickformat=",",
            tickprefix="$",
            fixedrange=True,
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            entrywidth=100,
            entrywidthmode="pixels",
        ),
        font_color=BLACK,
        margin={"l": 60, "r": 60, "b": 120, "t": 80, "pad": 4},
        images=[
            {
                **WATERMARK_CONFIG,
                "x": 1.05,
                "y": -0.22,
            }
        ],
    )

    return fig


def create_dynamic_baseline_reform_chart() -> go.Figure:
    """
    Create baseline vs reform refundable CTC comparison chart.

    This chart shows the phase-in of the refundable CTC under current law
    (dashed line) vs the reform (solid line).

    Returns:
        Plotly figure object
    """
    employment_incomes, baseline_credits, reform_credits = (
        calculate_baseline_reform_comparison()
    )

    fig = go.Figure()

    # Baseline trace (dashed gray)
    fig.add_trace(
        go.Scatter(
            x=employment_incomes,
            y=baseline_credits,
            name="Current law",
            mode="lines",
            line=dict(color=GRAY_600, width=3, dash="dash"),
            hovertemplate="Employment income: $%{x:,}<br>Refundable CTC: $%{y:,.0f}<extra></extra>",
        )
    )

    # Reform trace (solid teal)
    fig.add_trace(
        go.Scatter(
            x=employment_incomes,
            y=reform_credits,
            name="Stronger Start reform",
            mode="lines",
            line=dict(color=PRIMARY_500, width=3),
            hovertemplate="Employment income: $%{x:,}<br>Refundable CTC: $%{y:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title="Figure 1: Refundable Child Tax Credit phase-in: Current law vs. reform",
        font=dict(family="Roboto Serif", color=BLACK),
        xaxis=dict(
            title=dict(text="Employment income"),
            tickformat=",",
            tickprefix="$",
            fixedrange=True,
        ),
        yaxis=dict(
            title=dict(text="Refundable Child Tax Credit"),
            tickformat=",",
            tickprefix="$",
            fixedrange=True,
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            entrywidth=150,
            entrywidthmode="pixels",
        ),
        font_color=BLACK,
        margin={"l": 60, "r": 60, "b": 120, "t": 80, "pad": 4},
        images=[
            {
                **WATERMARK_CONFIG,
                "x": 1.05,
                "y": -0.22,
            }
        ],
    )

    return fig
