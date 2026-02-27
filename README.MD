# ⚖️ EU AI Act Compliance Analyzer

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red.svg)
![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-2024-003399.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An interactive web dashboard for analyzing AI systems against **EU AI Act** regulatory requirements. This tool performs automated compliance gap analysis, risk scoring, and generates a prioritized remediation roadmap.

Built as a portfolio project demonstrating **AI Governance**, **Regulatory Compliance**, and **Risk Management** skills.

---

## 🎯 Project Overview

This tool analyzes a **Resume Screening Tool** (classified as High-Risk under EU AI Act Annex III) against all mandatory compliance requirements. It identifies gaps, scores compliance levels, and produces a 12-month remediation roadmap.

### Why This Matters
The EU AI Act (effective August 2024) is the world's first comprehensive AI regulation. High-risk AI systems — including those used in employment decisions — must meet strict requirements or face fines of up to **€30 million or 6% of global annual turnover**.

---

## ✨ Features

- 📊 **Executive Summary Dashboard** — KPI metrics, compliance gauge, severity distribution
- 🔍 **Gap Analysis** — Requirement-by-requirement scoring with radar and bar charts
- 🗺️ **Remediation Roadmap** — 12-month Gantt chart with prioritized tasks and cost estimates
- 📋 **Detailed Findings** — Filterable deep-dive into each requirement with evidence tracking
- 🎨 **Interactive Visualizations** — Built with Plotly for professional, interactive charts
- 🔎 **Filter & Search** — Filter by category, status, and severity across all views

---

## 🏗️ Project Structure
```
eu-ai-act-compliance-analyzer/
│
├── app.py                      # Main Streamlit dashboard
├── data/
│   ├── requirements.json       # EU AI Act requirements database (10 articles)
│   ├── gap_analysis.json       # Compliance scores & gap findings
│   └── roadmap.json            # 16-task remediation roadmap
├── components/
│   ├── risk_scorer.py          # Risk scoring engine & data loading
│   ├── gap_analysis.py         # Chart generation for gap analysis
│   └── roadmap.py              # Roadmap charts & Gantt generation
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/eu-ai-act-compliance-analyzer.git
cd eu-ai-act-compliance-analyzer

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## 📋 EU AI Act Requirements Covered

| Article | Requirement | Category |
|---------|-------------|----------|
| Article 9 | Risk Management System | Risk Management |
| Article 10 | Data and Data Governance | Data Governance |
| Article 11 | Technical Documentation | Documentation |
| Article 12 | Record-Keeping and Logging | Audit & Logging |
| Article 13 | Transparency and Information Provision | Transparency |
| Article 14 | Human Oversight | Human Oversight |
| Article 15 | Accuracy, Robustness and Cybersecurity | Technical Robustness |
| Article 16 | Obligations of Providers | Governance |
| Article 29 | Obligations of Deployers | Governance |
| Article 72 | Post-Market Monitoring | Monitoring |

---

## 📊 Sample Assessment Results

| Metric | Value |
|--------|-------|
| Overall Compliance Score | 32.5% |
| Compliant Requirements | 0 / 10 |
| Partial Requirements | 3 / 10 |
| Non-Compliant Requirements | 7 / 10 |
| Critical Gaps | 6 |
| Projected Score (12 months) | 95% |

---

## 🗺️ Remediation Roadmap Summary

| Phase | Timeline | Focus | Cost Estimate |
|-------|----------|-------|---------------|
| Phase 1 | Month 1-2 | Emergency Controls & Quick Wins | $25K - $40K |
| Phase 2 | Month 3-5 | Data Governance & Documentation | $60K - $90K |
| Phase 3 | Month 6-8 | Technical Controls & Robustness | $80K - $120K |
| Phase 4 | Month 9-12 | Governance, Registration & Monitoring | $120K - $170K |

---

## 🧠 Key Concepts Demonstrated

- **EU AI Act** — Risk classification, Annex III high-risk categories, compliance obligations
- **AI Risk Management** — Gap analysis methodology, severity scoring, remediation prioritization
- **Data Governance** — Bias detection, data lineage, demographic representation
- **AI Transparency** — Explainability requirements, candidate disclosure obligations
- **Human Oversight** — Override mechanisms, escalation procedures, staff training
- **Post-Market Monitoring** — Bias drift detection, performance monitoring, incident reporting

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Streamlit | Interactive web dashboard |
| Plotly | Interactive charts and visualizations |
| Pandas | Data manipulation |
| JSON | Structured compliance data storage |

---

## 👤 About

Built by **[Your Name]** as part of an AI Governance & Risk portfolio.

- 🔗 LinkedIn: [your-linkedin]
- 📧 Email: [your-email]
- 20 years of SDET experience transitioning into **AI Governance, Risk & Security**

---

## 📄 License

MIT License — feel free to fork and adapt for your own compliance use cases.

---

## ⚠️ Disclaimer

This tool is for educational and portfolio demonstration purposes. It does not constitute legal advice. Always consult qualified legal counsel for actual EU AI Act compliance assessments.

Build with Claude AI
