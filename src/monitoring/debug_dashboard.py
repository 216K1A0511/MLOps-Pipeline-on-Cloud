import os
import re
from datetime import datetime

LOG_DIR = "logs"
REPORT_DIR = "reports"
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MLOps Debug Dashboard</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; }}
        .error {{ color: red; font-weight: bold; }}
        .success {{ color: green; font-weight: bold; }}
        .log-entry {{ margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
    </style>
</head>
<body>
    <h1>MLOps Pipeline Debug Dashboard</h1>
    <p>Last Updated: {timestamp}</p>
    <h2>Recent Activity</h2>
    <div id="logs">
        {log_content}
    </div>
</body>
</html>
"""

def generate_dashboard():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
    
    logs = []
    if os.path.exists(LOG_DIR):
        for filename in os.listdir(LOG_DIR):
            if filename.endswith(".log"):
                with open(os.path.join(LOG_DIR, filename), "r") as f:
                    logs.append(f.read())
    
    # Mocking some log content if empty for demonstration
    if not logs:
        logs = ["[INFO] Pipeline started", "[INFO] Loading data...", "[SUCCESS] API Connection Verified", "[INFO] Task completed"]

    log_html = ""
    for entry in logs:
        color_class = "error" if "ERROR" in entry else "success" if "SUCCESS" in entry else ""
        log_html += f'<div class="log-entry {color_class}">{entry}</div>'

    dashboard_path = os.path.join(REPORT_DIR, "debug_dashboard.html")
    with open(dashboard_path, "w") as f:
        f.write(HTML_TEMPLATE.format(timestamp=datetime.now(), log_content=log_html))
    
    print(f"Dashboard generated: {dashboard_path}")

if __name__ == "__main__":
    generate_dashboard()
