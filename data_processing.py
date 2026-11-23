import pandas as pd

REQUIRED_COLUMNS = [
    "Request_ID", "Service_Type", "Requester_Type", "Submission_Date",
    "Requested_Channel", "Priority", "Assigned_Office", "Queue_Length",
    "Required_Documents_Complete", "Processing_Days", "SLA_Days",
    "Status", "Reopened", "Satisfaction_Score"
]

def validate_dataset(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}"
    if df.empty:
        return False, "The uploaded CSV contains no records."
    return True, "Dataset schema is valid."

def prepare_features(df):
    out = df.copy()
    out["Submission_Date"] = pd.to_datetime(out["Submission_Date"], errors="coerce")
    out["Submission_Weekday"] = out["Submission_Date"].dt.day_name()
    out["Queue_Category"] = pd.cut(
        pd.to_numeric(out["Queue_Length"], errors="coerce"),
        bins=[-1, 5, 15, float("inf")],
        labels=["Low", "Medium", "High"]
    )
    return out

def make_target(df):
    out = df.copy()
    out["SLA_Breached"] = (out["Processing_Days"] > out["SLA_Days"]).astype("Int64")
    return out
