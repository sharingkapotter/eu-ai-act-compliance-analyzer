import json
import pandas as pd

def load_gap_analysis():
    """Load the gap analysis data from JSON file"""
    with open("data/gap_analysis.json", "r") as f:
        return json.load(f)

def load_requirements():
    """Load the EU AI Act requirements from JSON file"""
    with open("data/requirements.json", "r") as f:
        return json.load(f)

def get_compliance_dataframe():
    """Convert gap analysis JSON into a pandas DataFrame for easy manipulation"""
    data = load_gap_analysis()
    scores = data["compliance_scores"]
    
    df = pd.DataFrame([{
        "req_id": item["req_id"],
        "title": item["title"],
        "category": item["category"],
        "article": item["article"],
        "score": item["score"],
        "status": item["status"],
        "severity": item["severity"],
        "gap_description": item["gap_description"],
        "findings_count": len(item["findings"]),
        "evidence_count": len(item["evidence_available"])
    } for item in scores])
    
    return df

def get_summary_stats():
    """Return high-level summary statistics"""
    data = load_gap_analysis()
    summary = data["summary"]
    metadata = data["assessment_metadata"]
    return summary, metadata

def get_severity_color(severity):
    """Map severity levels to colors for the dashboard"""
    colors = {
        "Critical": "#FF4444",
        "High": "#FF8C00",
        "Medium": "#FFD700",
        "Low": "#32CD32"
    }
    return colors.get(severity, "#808080")

def get_status_color(status):
    """Map compliance status to colors"""
    colors = {
        "Compliant": "#32CD32",
        "Partial": "#FF8C00",
        "Non-Compliant": "#FF4444"
    }
    return colors.get(status, "#808080")

def calculate_category_scores():
    """Calculate average compliance score per category"""
    df = get_compliance_dataframe()
    category_scores = df.groupby("category")["score"].mean().reset_index()
    category_scores.columns = ["category", "avg_score"]
    category_scores["avg_score"] = category_scores["avg_score"].round(1)
    return category_scores

def get_critical_gaps():
    """Return only the critical gaps for priority highlighting"""
    df = get_compliance_dataframe()
    return df[df["severity"] == "Critical"].sort_values("score")

def get_findings_detail():
    """Return full findings detail for each requirement"""
    data = load_gap_analysis()
    return data["compliance_scores"]