from flask import Blueprint, render_template
import pandas as pd

main = Blueprint("main", __name__)

@main.route("/")
def index():
    df = pd.read_csv("logs_dataset/logs_summary.csv")
    grouped_logs = {}

    for _, row in df.iterrows():
        pod = row["pod_name"]
        full_log = row["full_log_snippet"]
        
        # Handle NaN or missing values
        if pd.isna(full_log):
            full_log = ""

        log_entry = {
            "timestamp": row["timestamp"],
            "error_lines": row["error_lines"],
            "full_log_snippet": full_log
        }
        if pod not in grouped_logs:
            grouped_logs[pod] = []
        grouped_logs[pod].append(log_entry)

    return render_template("index.html", grouped_logs=grouped_logs)
