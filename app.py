import streamlit as st
import pandas as pd
import json
from components.risk_scorer import (
    get_compliance_dataframe,
    get_summary_stats,
    get_critical_gaps,
    get_findings_detail
)
from components.gap_analysis import (
    create_compliance_gauge,
    create_requirements_heatmap,
    create_category_radar,
    create_severity_donut,
    create_status_summary_table
)
from components.roadmap import (
    create_gantt_chart,
    create_score_progression_chart,
    get_phase_summary,
    get_all_tasks_dataframe,
    get_effort_icon
)

# ── Page Configuration ──────────────────────────────────────────────
st.set_page_config(
    page_title="EU AI Act Compliance Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A5F;
        padding-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #FF8C00;
    }
    .critical-badge {
        background-color: #FF4444;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    .high-badge {
        background-color: #FF8C00;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    .section-divider {
        border-top: 2px solid #e0e0e0;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg", width=80)
    st.markdown("## ⚖️ EU AI Act Analyzer")
    st.markdown("**System Under Review:**")
    st.info("🤖 Resume Screening Tool\n\nVendor: HireAI Corp\n\nClassification: **High-Risk**\n\nAnnex III Category")
    
    st.markdown("---")
    page = st.radio(
        "Navigate to:",
        [
            "📊 Executive Summary",
            "🔍 Gap Analysis",
            "🗺️ Remediation Roadmap",
            "📋 Detailed Findings"
        ]
    )
    
    st.markdown("---")
    st.markdown("**Assessment Date:** Feb 27, 2026")
    st.markdown("**Next Review:** Aug 27, 2026")
    st.markdown("**Assessor:** AI Governance Analyst")
    st.markdown("---")
    st.caption("Built for EU AI Act Compliance · Portfolio Project")

# ── Load Data ────────────────────────────────────────────────────────
summary, metadata = get_summary_stats()
df = get_compliance_dataframe()
critical_gaps = get_critical_gaps()

# ════════════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════════════════════
if page == "📊 Executive Summary":
    st.markdown('<p class="main-header">⚖️ EU AI Act Compliance Analyzer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Resume Screening Tool · Regulatory Gap Analysis & Remediation Roadmap</p>', unsafe_allow_html=True)

    # Top KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Overall Score", f"{summary['overall_score']}%", delta="-67.5% to target")
    with col2:
        st.metric("Compliant", summary["compliant"], delta=None)
    with col3:
        st.metric("Partial", summary["partial"], delta=None)
    with col4:
        st.metric("Non-Compliant", summary["non_compliant"], delta=None)
    with col5:
        st.metric("Critical Gaps", summary["critical_gaps"], delta=None)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Gauge + Donut
    col1, col2 = st.columns(2)
    with col1:
        fig_gauge = create_compliance_gauge(summary["overall_score"])
        st.plotly_chart(fig_gauge, use_container_width=True)
    with col2:
        fig_donut = create_severity_donut()
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Critical Gaps Alert Box
    st.markdown("### 🚨 Critical Gaps Requiring Immediate Action")
    for _, row in critical_gaps.iterrows():
        with st.expander(f"❌ {row['req_id']} — {row['title']} | Score: {row['score']}%"):
            st.markdown(f"**Article:** {row['article']}")
            st.markdown(f"**Category:** {row['category']}")
            st.markdown(f"**Gap Description:** {row['gap_description']}")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Legal exposure warning
    st.error("""
    ⚠️ **Legal Exposure Warning**
    
    This system is currently operating as a High-Risk AI system under EU AI Act Annex III 
    without meeting mandatory compliance requirements. Continued operation without remediation 
    may result in fines of up to **€30 million or 6% of global annual turnover**, whichever is higher.
    Immediate action is recommended.
    """)

# ════════════════════════════════════════════════════════════════════
# PAGE 2: GAP ANALYSIS
# ════════════════════════════════════════════════════════════════════
elif page == "🔍 Gap Analysis":
    st.markdown("## 🔍 Compliance Gap Analysis")
    st.markdown("Detailed assessment of each EU AI Act requirement against current system state.")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Bar chart
    fig_bar = create_requirements_heatmap()
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Radar chart
    fig_radar = create_category_radar()
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Summary table
    st.markdown("### 📋 Requirements Summary Table")
    display_df = create_status_summary_table()

    def color_status(val):
        if val == "Non-Compliant":
            return "background-color: #FFE5E5; color: #CC0000; font-weight: bold"
        elif val == "Partial":
            return "background-color: #FFF3E0; color: #CC6600; font-weight: bold"
        elif val == "Compliant":
            return "background-color: #E8F5E9; color: #006600; font-weight: bold"
        return ""

    def color_severity(val):
        if val == "Critical":
            return "background-color: #FFE5E5; color: #CC0000; font-weight: bold"
        elif val == "High":
            return "background-color: #FFF3E0; color: #CC6600; font-weight: bold"
        return ""

    styled_df = display_df.style.applymap(color_status, subset=["Status"]).applymap(color_severity, subset=["Severity"])
    st.dataframe(styled_df, use_container_width=True, height=400)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Filter by category
    st.markdown("### 🔎 Filter by Category")
    categories = ["All"] + df["category"].unique().tolist()
    selected_category = st.selectbox("Select Category", categories)

    filtered_df = df if selected_category == "All" else df[df["category"] == selected_category]
    st.dataframe(filtered_df[["req_id", "title", "score", "status", "severity", "gap_description"]], use_container_width=True)

# ════════════════════════════════════════════════════════════════════
# PAGE 3: REMEDIATION ROADMAP
# ════════════════════════════════════════════════════════════════════
elif page == "🗺️ Remediation Roadmap":
    st.markdown("## 🗺️ Remediation Roadmap")
    st.markdown("12-month plan to achieve EU AI Act compliance for the Resume Screening Tool.")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Score progression
    fig_progression = create_score_progression_chart()
    st.plotly_chart(fig_progression, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Gantt chart
    fig_gantt = create_gantt_chart()
    st.plotly_chart(fig_gantt, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Phase cards
    st.markdown("### 📦 Phase Breakdown")
    phases = get_phase_summary()

    for phase in phases:
        color = {"Critical": "🔴", "High": "🟠", "Medium": "🔵"}.get(phase["priority"], "⚪")
        with st.expander(f"{color} Phase {phase['phase_number']}: {phase['title']} | {phase['duration']} | {phase['estimated_cost']}"):
            st.markdown(f"**Goal:** {phase['description']}")
            st.markdown(f"**Target Score:** {phase['target_score_improvement']}")
            st.markdown("**Tasks:**")
            for task in phase["tasks"]:
                st.markdown(f"- **{task['id']}** — {task['title']} *(Owner: {task['owner']}, {task['duration_weeks']} weeks)*")
                st.markdown(f"  - 📄 Deliverable: {task['deliverable']}")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Full task table
    st.markdown("### 📊 All Tasks Overview")
    tasks_df = get_all_tasks_dataframe()
    st.dataframe(tasks_df, use_container_width=True, height=400)

# ════════════════════════════════════════════════════════════════════
# PAGE 4: DETAILED FINDINGS
# ════════════════════════════════════════════════════════════════════
elif page == "📋 Detailed Findings":
    st.markdown("## 📋 Detailed Findings by Requirement")
    st.markdown("Deep dive into each EU AI Act requirement, findings, and available evidence.")

    findings = get_findings_detail()

    # Filter controls
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Non-Compliant", "Partial", "Compliant"])
    with col2:
        severity_filter = st.selectbox("Filter by Severity", ["All", "Critical", "High", "Medium", "Low"])

    filtered_findings = findings
    if status_filter != "All":
        filtered_findings = [f for f in filtered_findings if f["status"] == status_filter]
    if severity_filter != "All":
        filtered_findings = [f for f in filtered_findings if f["severity"] == severity_filter]

    st.markdown(f"**Showing {len(filtered_findings)} of {len(findings)} requirements**")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    for item in filtered_findings:
        status_emoji = {"Compliant": "✅", "Partial": "⚠️", "Non-Compliant": "❌"}.get(item["status"], "❓")
        severity_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(item["severity"], "⚪")

        with st.expander(f"{status_emoji} {item['req_id']} — {item['title']} | Score: {item['score']}% | {severity_emoji} {item['severity']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Compliance Score", f"{item['score']}%")
            with col2:
                st.metric("Status", item["status"])
            with col3:
                st.metric("Severity", item["severity"])

            st.markdown(f"**Article:** {item['article']}")
            st.markdown(f"**Category:** {item['category']}")
            st.markdown(f"**Gap Description:** {item['gap_description']}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🔍 Findings:**")
                for finding in item["findings"]:
                    st.markdown(f"- {finding}")
            with col2:
                st.markdown("**📁 Evidence Available:**")
                if item["evidence_available"]:
                    for evidence in item["evidence_available"]:
                        st.markdown(f"- ✅ {evidence}")
                else:
                    st.markdown("- ❌ No evidence available")