import pandas as pd
import plotly.express as px

def service_volume_chart(df):
    counts = df["Service_Type"].value_counts().rename_axis("Service Type").reset_index(name="Requests")
    return px.bar(counts, x="Service Type", y="Requests", title="Requests by Service Type", color="Requests")

def status_chart(df):
    counts = df["Status"].value_counts().rename_axis("Status").reset_index(name="Requests")
    return px.pie(counts, names="Status", values="Requests", title="Request Status Distribution", hole=0.45)

def queue_chart(df):
    return px.histogram(df, x="Queue_Length", color="Priority", title="Queue Length by Priority", nbins=15)

def office_breach_chart(df):
    done = df[(df["Status"] == "Completed") & df["Processing_Days"].notna() & df["SLA_Days"].notna()].copy()
    if done.empty:
        return None
    done["SLA_Breached"] = (done["Processing_Days"] > done["SLA_Days"]).astype(int)
    rates = (done.groupby("Assigned_Office")["SLA_Breached"].mean() * 100).reset_index(name="Breach Rate (%)")
    return px.bar(rates.sort_values("Breach Rate (%)", ascending=False), x="Assigned_Office", y="Breach Rate (%)", title="Observed SLA Breach Rate by Office")
