import pandas as pd
import plotly.express as px
import streamlit as st

def render_dashboard(df, predictions):
    total = len(df)
    completed = int((df["Status"] == "Completed").sum())
    pending = int((df["Status"] == "Pending").sum())
    cancelled = int((df["Status"] == "Cancelled").sum())
    st.subheader("Service Operations Overview")
    a,b,c,d = st.columns(4)
    a.metric("Total Requests", f"{total:,}")
    b.metric("Completed", f"{completed:,}")
    c.metric("Pending", f"{pending:,}")
    d.metric("Cancelled", f"{cancelled:,}")

    completed_df = df[(df["Status"] == "Completed") & df["Processing_Days"].notna() & df["SLA_Days"].notna()]
    if len(completed_df):
        actual_rate = (completed_df["Processing_Days"] > completed_df["SLA_Days"]).mean() * 100
        st.metric("Observed SLA Breach Rate (completed only)", f"{actual_rate:.1f}%")
    else:
        st.info("No completed requests with processing and SLA values are available.")

    st.markdown("#### Predictive review queue")
    queue = predictions.copy()
    if "Breach_Probability" in queue.columns:
        queue["Risk Level"] = queue["Breach_Probability"].apply(lambda p: "High" if p >= .70 else ("Review" if p >= .50 else "Low"))
        flagged = queue[queue["Breach_Probability"] >= .50].sort_values("Breach_Probability", ascending=False)
        st.caption("Risk groups are advisory probability bands: High ≥70%, Review 50–69%, Low <50%.")
        st.metric("Requests recommended for human review", len(flagged))
        cols = [c for c in ["Request_ID","Service_Type","Assigned_Office","Priority","Queue_Length","Required_Documents_Complete","SLA_Days","Risk Level","Breach_Probability","Status"] if c in flagged.columns]
        st.dataframe(flagged[cols].style.format({"Breach_Probability":"{:.1%}"}), use_container_width=True, hide_index=True)
        if not flagged.empty:
            st.plotly_chart(px.histogram(queue, x="Risk Level", color="Risk Level", title="Predicted Risk Group Distribution"), use_container_width=True)
    else:
        st.warning("The loaded model does not provide probability estimates. Review predictions by class only.")

    st.info("Human review is required. A predicted breach is a triage signal, not a decision to deny or delay student services.")
