import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from components.risk_scorer import (
    get_compliance_dataframe,
    get_severity_color,
    get_status_color,
    calculate_category_scores
)

def create_compliance_gauge(overall_score):
    """Create a gauge chart showing overall compliance score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=overall_score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Overall Compliance Score", "font": {"size": 20}},
        delta={"reference": 100, "increasing": {"color": "red"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": "#FF8C00"},
            "steps": [
                {"range": [0, 40], "color": "#FFE5E5"},
                {"range": [40, 70], "color": "#FFF3E0"},
                {"range": [70, 100], "color": "#E8F5E9"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 70
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_requirements_heatmap():
    """Create a heatmap of compliance scores per requirement"""
    df = get_compliance_dataframe()
    
    colors = []
    for score in df["score"]:
        if score >= 70:
            colors.append("#32CD32")
        elif score >= 40:
            colors.append("#FF8C00")
        else:
            colors.append("#FF4444")

    fig = go.Figure(go.Bar(
        x=df["score"],
        y=df["req_id"],
        orientation="h",
        marker_color=colors,
        text=[f"{s}% - {st}" for s, st in zip(df["score"], df["status"])],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{customdata}<br>Score: %{x}%<extra></extra>",
        customdata=df["title"]
    ))

    fig.update_layout(
        title="Compliance Score by Requirement",
        xaxis_title="Compliance Score (%)",
        yaxis_title="Requirement",
        xaxis=dict(range=[0, 120]),
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_category_radar():
    """Create a radar chart showing compliance by category"""
    category_scores = calculate_category_scores()
    
    categories = category_scores["category"].tolist()
    scores = category_scores["avg_score"].tolist()
    
    # Close the radar chart loop
    categories.append(categories[0])
    scores.append(scores[0])

    fig = go.Figure(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill="toself",
        fillcolor="rgba(255, 140, 0, 0.2)",
        line=dict(color="#FF8C00", width=2),
        name="Current Compliance"
    ))

    fig.add_trace(go.Scatterpolar(
        r=[100] * len(categories),
        theta=categories,
        fill="toself",
        fillcolor="rgba(50, 205, 50, 0.1)",
        line=dict(color="#32CD32", width=1, dash="dash"),
        name="Target (100%)"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        title="Compliance by Category",
        showlegend=True,
        height=450,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def create_severity_donut():
    """Create a donut chart of gap severity distribution"""
    df = get_compliance_dataframe()
    severity_counts = df["severity"].value_counts()

    colors = [get_severity_color(s) for s in severity_counts.index]

    fig = go.Figure(go.Pie(
        labels=severity_counts.index,
        values=severity_counts.values,
        hole=0.5,
        marker=dict(colors=colors),
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"
    ))

    fig.update_layout(
        title="Gap Severity Distribution",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def create_status_summary_table():
    """Create a styled summary table of all requirements"""
    df = get_compliance_dataframe()

    display_df = df[[
        "req_id", "article", "title", "category",
        "score", "status", "severity"
    ]].copy()

    display_df.columns = [
        "ID", "Article", "Requirement", "Category",
        "Score (%)", "Status", "Severity"
    ]

    return display_df