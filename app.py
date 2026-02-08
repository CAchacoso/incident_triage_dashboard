import streamlit as st
from src.data_loader import load_incident_data
from src.metrics import (
    calculate_kpis,
    incidents_by_service,
    aging_open_incidents,
    mttr_by_service
)
from src.charts import (
    incidents_over_time,
    severity_distribution,
    incidents_by_service_chart,
    mttr_by_service_chart
)

# ------------------------------
# PAGE SETUP
# ------------------------------
st.set_page_config(
    page_title="Incident & Triage Dashboard",
    layout="wide"
)
st.title("🚨 Incident & Triage Analytics Dashboard")

# ------------------------------
# LOAD DATA
# ------------------------------
df = load_incident_data("data/incidents.csv")

# ------------------------------
# SIDEBAR FILTERS
# ------------------------------
selected_service = st.sidebar.multiselect(
    "Filter by Service", options=df["service"].unique(), default=df["service"].unique()
)

selected_severity = st.sidebar.multiselect(
    "Filter by Severity", options=df["severity"].unique(), default=df["severity"].unique()
)

selected_status = st.sidebar.multiselect(
    "Filter by Status", options=df["status"].unique(), default=df["status"].unique()
)

# Apply filters
filtered_df = df[
    (df["service"].isin(selected_service)) &
    (df["severity"].isin(selected_severity)) &
    (df["status"].isin(selected_status))
]

# ------------------------------
# SIDEBAR NAVIGATION
# ------------------------------
page = st.sidebar.radio(
    "Go to",
    ["KPIs & Data", "Trends & Severity", "Service & Aging Analysis"]
)

# ------------------------------
# PAGE: KPIs & Data
# ------------------------------
if page == "KPIs & Data":
    st.subheader("📊 Key Incident Metrics")
    kpis = calculate_kpis(filtered_df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Incidents", kpis["Total Incidents"])
    col2.metric("Open Incidents", kpis["Open Incidents"])
    col3.metric("Closed Incidents", kpis["Closed Incidents"])
    col4.metric("MTTR (days)", kpis["MTTR (days)"])

    st.subheader("Incident Data")
    st.dataframe(filtered_df)

# ------------------------------
# PAGE: Trends & Severity
# ------------------------------
elif page == "Trends & Severity":
    st.subheader("📈 Incident Trends Over Time")
    trend_fig = incidents_over_time(filtered_df)
    st.plotly_chart(trend_fig, use_container_width=True)

    st.subheader("🔥 Incident Severity Distribution")
    severity_fig = severity_distribution(filtered_df)
    st.plotly_chart(severity_fig, use_container_width=True)

# ------------------------------
# PAGE: Service & Aging Analysis
# -----------------------
