import pandas as pd

def calculate_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    open_incidents = df[df["status"] == "Open"].shape[0]
    closed_incidents = df[df["status"] == "Closed"].shape[0]

    resolved = df.dropna(subset=["resolved_at"]).copy()
    resolved["resolution_time"] = (
        resolved["resolved_at"] - resolved["created_at"]
    ).dt.days

    mttr = round(resolved["resolution_time"].mean(), 2) if not resolved.empty else 0

    return {
        "Total Incidents": total,
        "Open Incidents": open_incidents,
        "Closed Incidents": closed_incidents,
        "MTTR (days)": mttr
    }

def incidents_by_service(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("service").size().reset_index(name="incident_count")

def aging_open_incidents(df: pd.DataFrame, days_threshold=3) -> pd.DataFrame:
    today = pd.Timestamp.today()
    df_open = df[df["status"] == "Open"].copy()
    df_open["days_open"] = (today - df_open["created_at"]).dt.days
    return df_open[df_open["days_open"] >= days_threshold]

def mttr_by_service(df: pd.DataFrame) -> pd.DataFrame:
    resolved = df.dropna(subset=["resolved_at"]).copy()
    resolved["resolution_time"] = (resolved["resolved_at"] - resolved["created_at"]).dt.days
    return resolved.groupby("service")["resolution_time"].mean().reset_index(name="mttr_days")
