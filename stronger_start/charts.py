"""Chart generation functions for Stronger Start for Working Families Act analysis."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .household import calculate_net_income_changes
from . import statewide

# PolicyEngine color palette
TEAL_PRIMARY = "#39C6C0"
TEAL_LIGHT = "#D8F2F1"
TEAL_DARK = "#2A9D97"
BLACK = "#000000"
DARK_GRAY = "#616161"
MEDIUM_GRAY = "#BDBDBD"
LIGHT_GRAY = "#F2F2F2"
WHITE = "#FFFFFF"

# Chart configuration
WATERMARK_URL = "https://raw.githubusercontent.com/PolicyEngine/policyengine-app-v2/main/app/public/assets/logos/policyengine/teal-square.png"


def create_net_income_change_chart() -> go.Figure:
    """Create Figure 1: Change in net income for a single parent with two children."""
    employment_income_values, net_income_changes = calculate_net_income_changes()

    df = pd.DataFrame(
        {
            "Employment Income": employment_income_values,
            "Change in net income": net_income_changes,
        }
    )

    fig = px.line(
        df,
        x="Employment Income",
        y="Change in net income",
        color_discrete_sequence=[TEAL_PRIMARY],
    )

    fig.update_layout(
        title=dict(
            text="Figure 1: Change in net income for a single parent with two children",
            font=dict(size=16),
        ),
        font=dict(family="Roboto Serif", color=BLACK),
        xaxis=dict(
            title="Employment income ($)",
            tickformat=",",
            fixedrange=True,
        ),
        yaxis=dict(
            title="Change in net income ($)",
            tickformat=",",
            fixedrange=True,
            range=[0, 400],
        ),
        margin=dict(l=60, r=60, b=120, t=80),
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        images=[
            dict(
                source=WATERMARK_URL,
                x=1,
                y=-0.18,
                xref="paper",
                yref="paper",
                sizex=0.1,
                sizey=0.1,
                xanchor="right",
                yanchor="bottom",
            )
        ],
        annotations=[
            dict(
                x=1,
                y=-0.22,
                xref="paper",
                yref="paper",
                text="Source: PolicyEngine",
                showarrow=False,
                font=dict(family="Roboto Serif", size=10, color=DARK_GRAY),
                xanchor="right",
            )
        ],
    )

    fig.update_traces(
        hovertemplate="Employment income: $%{x:,}<br>Change in net income: $%{y:.2f}<extra></extra>",
        line=dict(width=3),
    )

    return fig


def _add_stacked_bar_traces(
    fig: go.Figure,
    df: pd.DataFrame,
    row: int,
    show_legend: bool = False,
) -> None:
    """Add stacked bar traces to a subplot."""
    categories = [
        ("Gain more than 5%", TEAL_PRIMARY),
        ("Gain less than 5%", TEAL_LIGHT),
        ("No change", LIGHT_GRAY),
        ("Loss less than 5%", MEDIUM_GRAY),
        ("Loss more than 5%", DARK_GRAY),
    ]

    for name, color in categories:
        values = df[name].tolist()
        fig.add_trace(
            go.Bar(
                y=df["Income decile"],
                x=values,
                name=name,
                orientation="h",
                marker_color=color,
                text=[f"{x:.0f}%" if x > 3 else "" for x in values],
                textposition="inside",
                textfont=dict(color=BLACK if color == LIGHT_GRAY else WHITE),
                legendgroup=name,
                showlegend=show_legend,
                hovertemplate=f"{name}: %{{x:.1f}}%<extra></extra>",
            ),
            row=row,
            col=1,
        )


def create_winners_by_decile_chart() -> go.Figure:
    """Create Figure 2: Winners by income decile."""
    # Create DataFrames
    df_all = pd.DataFrame(
        {
            "Income decile": ["All"],
            "Gain more than 5%": [statewide.ALL_GAIN_MORE_THAN_5PCT],
            "Gain less than 5%": [statewide.ALL_GAIN_LESS_THAN_5PCT],
            "No change": [statewide.ALL_NO_CHANGE],
            "Loss less than 5%": [statewide.ALL_LOSS_LESS_THAN_5PCT],
            "Loss more than 5%": [statewide.ALL_LOSS_MORE_THAN_5PCT],
        }
    )

    df_deciles = pd.DataFrame(
        {
            "Income decile": [str(d) for d in statewide.DECILES],
            "Gain more than 5%": statewide.GAIN_MORE_THAN_5PCT,
            "Gain less than 5%": statewide.GAIN_LESS_THAN_5PCT,
            "No change": statewide.NO_CHANGE,
            "Loss less than 5%": statewide.LOSS_LESS_THAN_5PCT,
            "Loss more than 5%": statewide.LOSS_MORE_THAN_5PCT,
        }
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.1, 0.9],
    )

    _add_stacked_bar_traces(fig, df_all, row=1, show_legend=True)
    _add_stacked_bar_traces(fig, df_deciles, row=2, show_legend=False)

    fig.update_layout(
        barmode="stack",
        title=dict(
            text="Figure 2: Winners of the Stronger Start for Working Families Act by income decile",
            font=dict(size=16),
        ),
        font=dict(family="Roboto Serif", color=BLACK),
        xaxis=dict(ticksuffix="%", range=[0, 100], fixedrange=True),
        xaxis2=dict(
            title="Population share",
            ticksuffix="%",
            range=[0, 100],
            fixedrange=True,
        ),
        yaxis=dict(fixedrange=True),
        yaxis2=dict(title="Income decile", fixedrange=True),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            traceorder="normal",
        ),
        margin=dict(l=60, r=60, b=150, t=80),
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        height=600,
        images=[
            dict(
                source=WATERMARK_URL,
                x=1,
                y=-0.32,
                xref="paper",
                yref="paper",
                sizex=0.08,
                sizey=0.08,
                xanchor="right",
                yanchor="bottom",
            )
        ],
        annotations=[
            dict(
                x=1,
                y=-0.35,
                xref="paper",
                yref="paper",
                text="Source: PolicyEngine",
                showarrow=False,
                font=dict(family="Roboto Serif", size=10, color=DARK_GRAY),
                xanchor="right",
            )
        ],
    )

    return fig


def create_avg_benefit_by_decile_chart() -> go.Figure:
    """Create Figure 3: Average benefit by income decile."""
    df = pd.DataFrame(
        {
            "Income decile": statewide.DECILES,
            "Average impact": statewide.AVG_IMPACT_BY_DECILE,
        }
    )

    fig = px.bar(
        df,
        x="Income decile",
        y="Average impact",
        text=[f"${x}" for x in statewide.AVG_IMPACT_BY_DECILE],
        color_discrete_sequence=[TEAL_PRIMARY],
    )

    fig.update_layout(
        title=dict(
            text="Figure 3: Average benefit of the Stronger Start for Working Families Act by income decile",
            font=dict(size=16),
        ),
        font=dict(family="Roboto Serif", color=BLACK),
        xaxis=dict(
            title="Income decile",
            tickvals=list(range(1, 11)),
            fixedrange=True,
        ),
        yaxis=dict(
            title="Average impact ($)",
            tickformat=",",
            fixedrange=True,
        ),
        showlegend=False,
        margin=dict(l=60, r=60, b=120, t=80),
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        images=[
            dict(
                source=WATERMARK_URL,
                x=1,
                y=-0.18,
                xref="paper",
                yref="paper",
                sizex=0.1,
                sizey=0.1,
                xanchor="right",
                yanchor="bottom",
            )
        ],
        annotations=[
            dict(
                x=1,
                y=-0.22,
                xref="paper",
                yref="paper",
                text="Source: PolicyEngine",
                showarrow=False,
                font=dict(family="Roboto Serif", size=10, color=DARK_GRAY),
                xanchor="right",
            )
        ],
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="Income decile: %{x}<br>Average impact: $%{y:,.0f}<extra></extra>",
    )

    return fig
