import pandas as pd

def load_incident_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["resolved_at"] = pd.to_datetime(df["resolved_at"])
    return df
