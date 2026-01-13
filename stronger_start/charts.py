"""Chart generation functions for Stronger Start for Working Families Act analysis."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .household import calculate_net_income_changes, calculate_baseline_reform_comparison
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
)

# PolicyEngine app-v2 color palette - matching WinnersLosersIncomeDecileSubPage.tsx
BLACK = "#000000"

# Primary teal colors
PRIMARY_500 = "#319795"  # colors.primary[500] - main brand color
PRIMARY_700 = "#285E61"  # colors.primary[700] - dark teal for gains >5%
PRIMARY_ALPHA_60 = "rgba(49, 151, 149, 0.6)"  # colors.primary.alpha[60] - teal with 60% opacity

# Gray scale
GRAY_200 = "#E5E7EB"  # colors.gray[200] - no change
GRAY_400 = "#9CA3AF"  # colors.gray[400] - loss <5%
GRAY_600 = "#4B5563"  # colors.gray[600] - loss >5%

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


def create_net_income_change_chart() -> go.Figure:
    """Create net income change chart with filing status and children options."""
    # Generate data for all scenarios
    scenarios = []
    for filing_status in ["single", "joint"]:
        for num_children in [1, 2, 3]:
            employment_incomes, net_income_changes = calculate_net_income_changes(
                filing_status=filing_status, num_children=num_children
            )
            scenarios.append(
                {
                    "filing_status": filing_status,
                    "num_children": num_children,
                    "employment_incomes": employment_incomes,
                    "net_income_changes": net_income_changes,
                }
            )

    # Create figure
    fig = go.Figure()

    # Add trace for each scenario
    for i, scenario in enumerate(scenarios):
        visible = i == 0  # Only first scenario visible initially

        fig.add_trace(
            go.Scatter(
                x=scenario["employment_incomes"],
                y=scenario["net_income_changes"],
                name="Benefit",
                mode="lines",
                line=dict(color=PRIMARY_500, width=3),
                visible=visible,
                hovertemplate="Employment income: $%{x:,}<br>Change in net income: $%{y:.2f}<extra></extra>",
            )
        )

    # Create buttons for scenario selection
    buttons = []
    for i, scenario in enumerate(scenarios):
        filing_label = "Single" if scenario["filing_status"] == "single" else "Joint"
        label = f"{filing_label}, {scenario['num_children']} child{'ren' if scenario['num_children'] > 1 else ''}"

        # Create visibility list: show the trace for this scenario
        visibility = [False] * len(scenarios)
        visibility[i] = True

        buttons.append(
            dict(
                label=label,
                method="update",
                args=[
                    {"visible": visibility},
                    {"title": f"Benefit from Stronger Start Working Families Act<br><sub>{label}</sub>"},
                ],
            )
        )

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.15,
                yanchor="top",
                bgcolor="#FFFFFF",
                bordercolor=GRAY_400,
                borderwidth=1,
            )
        ],
        title="Benefit from Stronger Start Working Families Act<br><sub>Single, 1 child</sub>",
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
        showlegend=False,
        font_color=BLACK,
        margin={"l": 60, "r": 60, "b": 100, "t": 140, "pad": 4},
        images=[
            {
                **WATERMARK_CONFIG,
                "x": 1.05,
                "y": -0.22,
            }
        ],
    )

    return fig


def create_baseline_reform_comparison_chart() -> go.Figure:
    """Create simple baseline vs reform refundable CTC comparison chart."""
    employment_incomes, baseline_credits, reform_credits = calculate_baseline_reform_comparison()

    # Create figure with both traces
    fig = go.Figure()

    # Baseline trace
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

    # Reform trace
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
        title="Refundable Child Tax Credit phase-in: Current law vs. Stronger Start for Working Families Act reform",
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
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
        ),
        font_color=BLACK,
        margin={"l": 60, "r": 60, "b": 100, "t": 80, "pad": 4},
        images=[
            {
                **WATERMARK_CONFIG,
                "x": 1.05,
                "y": -0.22,
            }
        ],
    )

    return fig


def create_winners_by_decile_chart() -> go.Figure:
    """
    Create Figure 2: Winners of Stronger Start for Working Families Act by income decile.

    Returns:
        Plotly figure object
    """
    labels_deciles = [f"{i}" for i in DECILES]

    df_deciles = pd.DataFrame(
        {
            "Income decile": labels_deciles,
            "Gain more than 5%": GAIN_MORE_THAN_5PCT,
            "Gain less than 5%": GAIN_LESS_THAN_5PCT,
            "No change": NO_CHANGE,
            "Lose less than 5%": LOSS_LESS_THAN_5PCT,
            "Lose more than 5%": LOSS_MORE_THAN_5PCT,
        }
    )

    df_all = pd.DataFrame(
        {
            "Income decile": ["All"],
            "Gain more than 5%": [ALL_GAIN_MORE_THAN_5PCT],
            "Gain less than 5%": [ALL_GAIN_LESS_THAN_5PCT],
            "No change": [ALL_NO_CHANGE],
            "Lose less than 5%": [ALL_LOSS_LESS_THAN_5PCT],
            "Lose more than 5%": [ALL_LOSS_MORE_THAN_5PCT],
        }
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.1, 0.9],
    )

    # Colors matching app-v2 WinnersLosersIncomeDecileSubPage.tsx
    COLOR_GAIN_MORE = PRIMARY_700  # Dark teal (#285E61)
    COLOR_GAIN_LESS = PRIMARY_ALPHA_60  # Teal with 60% opacity (#31979599)
    COLOR_NO_CHANGE = GRAY_200  # Light gray
    COLOR_LOSS_LESS = GRAY_400  # Medium gray
    COLOR_LOSS_MORE = GRAY_600  # Dark gray

    # Add traces for "All" category - first row
    _add_stacked_bar_traces(
        fig, df_all, COLOR_GAIN_MORE, COLOR_GAIN_LESS,
        COLOR_NO_CHANGE, COLOR_LOSS_LESS, COLOR_LOSS_MORE,
        row=1, show_legend=True
    )

    # Add traces for deciles - second row
    _add_stacked_bar_traces(
        fig, df_deciles, COLOR_GAIN_MORE, COLOR_GAIN_LESS,
        COLOR_NO_CHANGE, COLOR_LOSS_LESS, COLOR_LOSS_MORE,
        row=2, show_legend=False
    )

    fig.update_layout(
        barmode="stack",
        title=dict(text="Figure 2: Winners of Stronger Start for Working Families Act by income decile", x=0),
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
    # Categories with shortened legend labels
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


def create_avg_benefit_by_decile_chart() -> go.Figure:
    """
    Create Figure 3: Average benefit of Stronger Start for Working Families Act by income decile.

    Returns:
        Plotly figure object
    """
    df = pd.DataFrame(
        {
            "Income decile": DECILES,
            "Average impact": AVG_IMPACT_BY_DECILE,
        }
    )

    dollar_text = [f"${x}" for x in AVG_IMPACT_BY_DECILE]

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
