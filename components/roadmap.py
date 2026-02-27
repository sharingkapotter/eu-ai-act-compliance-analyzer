import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def load_roadmap():
    """Load the roadmap data from JSON file"""
    with open("data/roadmap.json", "r") as f:
        return json.load(f)

def get_phase_color(priority):
    """Map priority levels to colors"""
    colors = {
        "Critical": "#FF4444",
        "High": "#FF8C00",
        "Medium": "#4169E1",
        "Low": "#32CD32"
    }
    return colors.get(priority, "#808080")

def get_effort_icon(effort):
    """Map effort levels to emoji indicators"""
    icons = {
        "Low": "🟢 Low",
        "Medium": "🟡 Medium",
        "High": "🔴 High"
    }
    return icons.get(effort, effort)

def create_gantt_chart():
    """Create a Gantt chart of the remediation roadmap"""
    data = load_roadmap()
    
    tasks = []
    for phase in data["phases"]:
        phase_num = phase["phase_number"]
        for task in phase["tasks"]:
            tasks.append({
                "Task": task["title"],
                "Phase": f"Phase {phase_num}: {phase['title']}",
                "Start": f"2026-0{max(1, (phase_num-1)*3+1):02d}-01",
                "Finish": f"2026-{min(12, phase_num*3):02d}-28",
                "Priority": task["priority"],
                "Owner": task["owner"],
                "Effort": task["effort"],
                "req_id": task["req_id"]
            })

    df = pd.DataFrame(tasks)
    df["Start"] = pd.to_datetime(df["Start"])
    df["Finish"] = pd.to_datetime(df["Finish"])

    color_map = {
        "Critical": "#FF4444",
        "High": "#FF8C00",
        "Medium": "#4169E1",
        "Low": "#32CD32"
    }

    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Priority",
        color_discrete_map=color_map,
        hover_data=["Phase", "Owner", "Effort", "req_id"],
        title="Remediation Roadmap - 12 Month Plan"
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title="Priority",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_score_progression_chart():
    """Create a line chart showing projected compliance score improvement"""
    data = load_roadmap()
    
    phases = [
        {"phase": "Current State", "score": 32.5, "month": "Feb 2026"},
        {"phase": "After Phase 1", "score": 50, "month": "Apr 2026"},
        {"phase": "After Phase 2", "score": 65, "month": "Jul 2026"},
        {"phase": "After Phase 3", "score": 80, "month": "Oct 2026"},
        {"phase": "After Phase 4", "score": 95, "month": "Feb 2027"},
    ]

    df = pd.DataFrame(phases)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["month"],
        y=df["score"],
        mode="lines+markers+text",
        text=[f"{s}%" for s in df["score"]],
        textposition="top center",
        line=dict(color="#FF8C00", width=3),
        marker=dict(size=12, color="#FF8C00"),
        name="Projected Score"
    ))

    fig.add_hline(
        y=70,
        line_dash="dash",
        line_color="green",
        annotation_text="Minimum Acceptable (70%)",
        annotation_position="right"
    )

    fig.add_hrect(
        y0=0, y1=40,
        fillcolor="red", opacity=0.1,
        annotation_text="Non-Compliant Zone"
    )
    fig.add_hrect(
        y0=40, y1=70,
        fillcolor="orange", opacity=0.1,
        annotation_text="Partial Zone"
    )
    fig.add_hrect(
        y0=70, y1=100,
        fillcolor="green", opacity=0.1,
        annotation_text="Compliant Zone"
    )

    fig.update_layout(
        title="Projected Compliance Score Progression",
        xaxis_title="Timeline",
        yaxis_title="Compliance Score (%)",
        yaxis=dict(range=[0, 110]),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def get_phase_summary():
    """Return phase summary for display cards"""
    data = load_roadmap()
    return data["phases"]

def get_all_tasks_dataframe():
    """Return all tasks as a flat DataFrame"""
    data = load_roadmap()
    tasks = []
    for phase in data["phases"]:
        for task in phase["tasks"]:
            tasks.append({
                "Phase": f"Phase {phase['phase_number']}",
                "Task ID": task["id"],
                "Req ID": task["req_id"],
                "Title": task["title"],
                "Effort": get_effort_icon(task["effort"]),
                "Duration": f"{task['duration_weeks']} weeks",
                "Owner": task["owner"],
                "Priority": task["priority"],
                "Deliverable": task["deliverable"]
            })
    return pd.DataFrame(tasks)