from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import query
import time

class MLMonitoring:
    def __init__(self, project_id):
        self.client = monitoring_v3.MetricServiceClient()
        self.project = project_id
    
    def create_uptime_check(self, endpoint_url, check_name):
        """Create uptime check for model endpoint"""
        uptime_client = monitoring_v3.UptimeCheckServiceClient()
        
        config = monitoring_v3.UptimeCheckConfig(
            display_name=check_name,
            monitored_resource={
                "type": "uptime_url",
                "labels": {
                    "host": endpoint_url.replace("https://", "")
                }
            },
            http_check={
                "path": "/health",
                "port": 443,
                "use_ssl": True
            },
            timeout={"seconds": 10},
            period={"seconds": 60}
        )
        
        return uptime_client.create_uptime_check_config(
            parent=f"projects/{self.project}",
            uptime_check_config=config
        )
    
    def create_alert_policy(self, metric_name, threshold):
        """Create alert policy for model metrics"""
        alert_client = monitoring_v3.AlertPolicyServiceClient()
        
        condition = monitoring_v3.AlertPolicy.Condition(
            display_name="High Prediction Latency",
            condition_threshold={
                "filter": f'metric.type="{metric_name}"',
                "comparison": "COMPARISON_GT",
                "threshold_value": threshold,
                "duration": {"seconds": 300},
                "trigger": {"count": 1}
            }
        )
        
        policy = monitoring_v3.AlertPolicy(
            display_name="Model Performance Alert",
            conditions=[condition],
            combiner="OR",
            notification_channels=["projects/{project}/notificationChannels/..."],
            enabled=True
        )
        
        return alert_client.create_alert_policy(
            name=f"projects/{self.project}",
            alert_policy=policy
        )
    
    def log_prediction_metrics(self, latency, success_rate, model_version):
        """Log custom metrics for predictions"""
        series = monitoring_v3.TimeSeries()
        series.metric.type = "custom.googleapis.com/prediction/latency"
        series.resource.type = "global"
        
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        
        point = monitoring_v3.Point({
            "interval": {
                "end_time": {"seconds": seconds, "nanos": nanos}
            },
            "value": {"double_value": latency}
        })
        series.points = [point]
        
        self.client.create_time_series(
            name=f"projects/{self.project}",
            time_series=[series]
        )