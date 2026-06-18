import json
from pathlib import Path
from collections import Counter

import pandas as pd
import streamlit as st


# ==================================================
# PROJECT PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "collected_documents.jsonl"
CLEAN_FILE = PROJECT_ROOT / "data" / "processed" / "clean_documents.jsonl"
STRATEGIC_EVIDENCE_FILE = PROJECT_ROOT / "data" / "intelligence" / "strategic_evidence.json"
CEO_BRIEFING_FILE = PROJECT_ROOT / "data" / "intelligence" / "ceo_briefing.json"


# ==================================================
# BASIC LOADERS
# ==================================================

def load_json(path):
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_jsonl(path):
    if not path.exists():
        return []

    records = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return records


def safe_get(data, key, default=""):
    if not isinstance(data, dict):
        return default

    return data.get(key, default)


def make_dataframe(records):
    if not records:
        return pd.DataFrame()

    return pd.DataFrame(records)


# ==================================================
# DASHBOARD HELPERS
# ==================================================

def get_categories(strategic_evidence):
    if not strategic_evidence:
        return {}

    return strategic_evidence.get("categories", {})


def count_evidence_items(categories):
    total = 0

    for items in categories.values():
        total += len(items)

    return total


def flatten_evidence(categories):
    rows = []

    for category, items in categories.items():
        for item in items:
            rows.append({
                "category": category,
                "title": item.get("title", ""),
                "source": item.get("source", ""),
                "publisher": item.get("publisher", ""),
                "score": item.get("score", 0),
                "url": item.get("url", ""),
                "evidence_text": item.get("evidence_text", "")
            })

    return rows


def deduplicate_sources(sources):
    unique_sources = []
    seen_keys = set()

    for source in sources:
        url = str(source.get("url", "")).strip().lower()
        title = str(source.get("title", "")).strip().lower()

        key = url if url else title

        if not key:
            key = source.get("source_id", "")

        if key in seen_keys:
            continue

        seen_keys.add(key)
        unique_sources.append(source)

    return unique_sources


def display_file_status(label, path):
    if path.exists():
        st.sidebar.success(f"{label}: Found")
    else:
        st.sidebar.error(f"{label}: Missing")


def display_category_section(title, items):
    st.subheader(title)

    if not items:
        st.warning("No data available for this section.")
        return

    for index, item in enumerate(items, start=1):
        item_title = item.get("title", "Untitled")
        source = item.get("source", "")
        publisher = item.get("publisher", "")
        score = item.get("score", "")
        evidence_text = item.get("evidence_text", "")
        url = item.get("url", "")

        with st.expander(f"{index}. {item_title}"):
            col1, col2, col3 = st.columns(3)

            col1.metric("Source", source if source else "Unknown")
            col2.metric("Publisher", publisher if publisher else "Unknown")
            col3.metric("Score", score if score != "" else "N/A")

            st.markdown("**Evidence Text**")
            st.write(evidence_text if evidence_text else "No evidence text available.")

            if url:
                st.markdown(f"[Open Source]({url})")


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI CEO Agent Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# LOAD DATA
# ==================================================

raw_documents = load_jsonl(RAW_FILE)
clean_documents = load_jsonl(CLEAN_FILE)
strategic_evidence = load_json(STRATEGIC_EVIDENCE_FILE)
ceo_briefing = load_json(CEO_BRIEFING_FILE)

categories = get_categories(strategic_evidence)
evidence_rows = flatten_evidence(categories)

raw_df = make_dataframe(raw_documents)
clean_df = make_dataframe(clean_documents)
evidence_df = make_dataframe(evidence_rows)

sources_used = []

if ceo_briefing:
    sources_used = ceo_briefing.get("sources_used", [])

unique_sources = deduplicate_sources(sources_used)
sources_df = make_dataframe(unique_sources)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("AI CEO Agent")
st.sidebar.markdown("NVIDIA Strategic Intelligence Dashboard")

st.sidebar.divider()

display_file_status("Raw Documents", RAW_FILE)
display_file_status("Clean Documents", CLEAN_FILE)
display_file_status("Strategic Evidence", STRATEGIC_EVIDENCE_FILE)
display_file_status("CEO Briefing", CEO_BRIEFING_FILE)

st.sidebar.divider()

st.sidebar.markdown("### Data Files")
st.sidebar.code(
    f"""
Raw: {RAW_FILE}
Clean: {CLEAN_FILE}
Evidence: {STRATEGIC_EVIDENCE_FILE}
Briefing: {CEO_BRIEFING_FILE}
"""
)


# ==================================================
# MAIN HEADER
# ==================================================

st.title("📊 AI CEO Agent Dashboard")

company_name = "NVIDIA"

if ceo_briefing:
    company_name = ceo_briefing.get("company", "NVIDIA")

st.markdown(f"### Company: **{company_name}**")

if ceo_briefing:
    st.caption(f"Generated at: {ceo_briefing.get('generated_at', 'Unknown')}")


# ==================================================
# TOP METRICS
# ==================================================

st.divider()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Raw Documents", len(raw_documents))
col2.metric("Clean Documents", len(clean_documents))
col3.metric("Evidence Items", count_evidence_items(categories))
col4.metric("Evidence Categories", len(categories))
col5.metric("Unique Sources", len(unique_sources))


# ==================================================
# TABS
# ==================================================

tab_overview, tab_market, tab_opportunities, tab_risks, tab_competitors, tab_trends, tab_briefing, tab_sources = st.tabs([
    "Company Overview",
    "Market Intelligence",
    "Opportunity Monitor",
    "Risk Monitor",
    "Competitor Activity",
    "Emerging Trends",
    "CEO Briefing",
    "Sources Used"
])


# ==================================================
# TAB 1: COMPANY OVERVIEW
# ==================================================

with tab_overview:
    st.header("Company Overview")

    if ceo_briefing:
        st.markdown("### CEO Question")
        st.info(ceo_briefing.get("question", "No CEO question found."))

    st.markdown("### Data Pipeline Status")

    pipeline_data = {
        "Stage": [
            "Raw Data Collection",
            "Document Cleaning",
            "Strategic Evidence Generation",
            "CEO Briefing Generation"
        ],
        "Output File": [
            str(RAW_FILE.relative_to(PROJECT_ROOT)),
            str(CLEAN_FILE.relative_to(PROJECT_ROOT)),
            str(STRATEGIC_EVIDENCE_FILE.relative_to(PROJECT_ROOT)),
            str(CEO_BRIEFING_FILE.relative_to(PROJECT_ROOT))
        ],
        "Status": [
            "Available" if RAW_FILE.exists() else "Missing",
            "Available" if CLEAN_FILE.exists() else "Missing",
            "Available" if STRATEGIC_EVIDENCE_FILE.exists() else "Missing",
            "Available" if CEO_BRIEFING_FILE.exists() else "Missing"
        ]
    }

    st.dataframe(pd.DataFrame(pipeline_data), use_container_width=True)

    st.markdown("### Evidence Category Counts")

    if categories:
        category_counts = {
            "Category": [],
            "Count": []
        }

        for category, items in categories.items():
            category_counts["Category"].append(category)
            category_counts["Count"].append(len(items))

        category_df = pd.DataFrame(category_counts)

        st.bar_chart(
            category_df.set_index("Category")
        )

        st.dataframe(category_df, use_container_width=True)
    else:
        st.warning("No strategic evidence categories found.")


# ==================================================
# TAB 2: MARKET INTELLIGENCE
# ==================================================

with tab_market:
    st.header("Market Intelligence")

    if evidence_df.empty:
        st.warning("No evidence data available.")
    else:
        st.markdown("### Top Evidence by Score")

        if "score" in evidence_df.columns:
            evidence_df["score_numeric"] = pd.to_numeric(
                evidence_df["score"],
                errors="coerce"
            ).fillna(0)

            top_evidence_df = evidence_df.sort_values(
                by="score_numeric",
                ascending=False
            ).head(10)

            st.dataframe(
                top_evidence_df[[
                    "category",
                    "title",
                    "source",
                    "publisher",
                    "score",
                    "url"
                ]],
                use_container_width=True
            )
        else:
            st.dataframe(evidence_df, use_container_width=True)

        st.markdown("### Source Distribution")

        if "source" in evidence_df.columns:
            source_counts = evidence_df["source"].fillna("Unknown").value_counts()
            st.bar_chart(source_counts)


# ==================================================
# TAB 3: OPPORTUNITY MONITOR
# ==================================================

with tab_opportunities:
    opportunity_items = []

    for key in categories.keys():
        if "opportun" in key.lower():
            opportunity_items = categories.get(key, [])
            break

    display_category_section("Opportunity Monitor", opportunity_items)


# ==================================================
# TAB 4: RISK MONITOR
# ==================================================

with tab_risks:
    risk_items = []

    for key in categories.keys():
        if "risk" in key.lower():
            risk_items = categories.get(key, [])
            break

    display_category_section("Risk Monitor", risk_items)


# ==================================================
# TAB 5: COMPETITOR ACTIVITY
# ==================================================

with tab_competitors:
    competitor_items = []

    for key in categories.keys():
        if "competitor" in key.lower():
            competitor_items = categories.get(key, [])
            break

    display_category_section("Competitor Activity", competitor_items)


# ==================================================
# TAB 6: EMERGING TRENDS
# ==================================================

with tab_trends:
    trend_items = []

    for key in categories.keys():
        if "trend" in key.lower() or "emerging" in key.lower():
            trend_items = categories.get(key, [])
            break

    display_category_section("Emerging Trends", trend_items)


# ==================================================
# TAB 7: CEO BRIEFING
# ==================================================

with tab_briefing:
    st.header("CEO Briefing")

    if not ceo_briefing:
        st.warning("CEO briefing file not found. Run the AI CEO agent first.")
        st.code("python -m agents.ai_ceo_agent")
    else:
        answer = ceo_briefing.get("answer", "")

        if answer:
            st.markdown(answer)
        else:
            st.warning("CEO briefing answer is empty.")

        st.download_button(
            label="Download CEO Briefing JSON",
            data=json.dumps(ceo_briefing, indent=4, ensure_ascii=False),
            file_name="ceo_briefing.json",
            mime="application/json"
        )


# ==================================================
# TAB 8: SOURCES USED
# ==================================================

with tab_sources:
    st.header("Sources Used")

    if sources_df.empty:
        st.warning("No sources available.")
    else:
        st.markdown("### Unique Sources")

        display_columns = []

        for column in ["source_id", "type", "category", "title", "source", "publisher", "score", "url"]:
            if column in sources_df.columns:
                display_columns.append(column)

        st.dataframe(
            sources_df[display_columns],
            use_container_width=True
        )

        st.markdown("### Source Type Count")

        if "type" in sources_df.columns:
            type_counts = sources_df["type"].fillna("Unknown").value_counts()
            st.bar_chart(type_counts)

        st.markdown("### Source Publisher Count")

        if "publisher" in sources_df.columns:
            publisher_counts = sources_df["publisher"].fillna("Unknown").value_counts().head(10)
            st.bar_chart(publisher_counts)