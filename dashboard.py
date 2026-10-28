# dashboard.py
import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="AI Security Proxy Dashboard", layout="wide")

st.title("🛡️ AI Agent Security Observatory")
st.markdown("Real-time monitoring of AI Tool Calls and Prompt Injection attempts.")

LOG_FILE = "attack_logs.json"

# Load logs
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
else:
    logs = []

# Metrics
total_requests = len(logs)
blocked_requests = sum(1 for log in logs if log["status"] == "BLOCKED")
allowed_requests = total_requests - blocked_requests

col1, col2, col3 = st.columns(3)
col1.metric("Total Requests", total_requests)
col2.metric("🛑 Blocked Attacks", blocked_requests, delta_color="inverse")
col3.metric("✅ Allowed Queries", allowed_requests)

st.divider()

# Display Logs as a Table
if logs:
    st.subheader("📜 Recent Activity Log")
    df = pd.DataFrame(logs)
    
    # Color code the status
    def color_status(val):
        color = 'red' if val == 'BLOCKED' else 'green'
        return f'color: {color}; font-weight: bold'

    styled_df = df.style.applymap(color_status, subset=['status'])
    st.dataframe(styled_df, use_container_width=True)
else:
    st.info("No activity recorded yet. Run the AI Agent to generate traffic!")

# Auto-refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()