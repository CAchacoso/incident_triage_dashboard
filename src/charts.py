import plotly.express as px
import pandas as pd

def incidents_over_time(df: pd.DataFrame):
    daily = (
        df.groupby(df["created_at"].dt.date)
        .size()
        .reset_index(name="incident_count")
    )

    fig = px.line(
        daily,
        x="created_at",
        y="incident_count",
        title="Incidents Over Time",
        markers=True
    )
    return fig


def severity_distribution(df: pd.DataFrame):
    severity_counts = (
        df["severity"]
        .value_counts()
        .reset_index()
    )
    severity_counts.columns = ["severity", "count"]

    fig = px.bar(
        severity_counts,
        x="severity",
        y="count",
        title="Incident Severity Distribution"
    )
    return fig

def incidents_by_service_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="service",
        y="incident_count",
        title="Incidents by Service"
    )
    return fig

def mttr_by_service_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="service",
        y="mttr_days",
        title="Mean Time to Resolve (MTTR) by Service",
        color="mttr_days",
        color_continuous_scale="Reds"
    )
    return fig
