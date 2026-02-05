import functions_framework
from google.cloud import storage, pubsub_v1
import json

@functions_framework.cloud_event
def trigger_retraining(cloud_event):
    """Cloud Function triggered by new data in GCS"""
    data = cloud_event.data
    
    bucket_name = data['bucket']
    file_name = data['name']
    
    # Check if it's training data
    if 'training_data' in file_name and file_name.endswith('.csv'):
        print(f"New training data detected: {file_name}")
        
        # Publish message to Pub/Sub
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(
            'your-project-id', 'retraining-trigger'
        )
        
        message = {
            'bucket': bucket_name,
            'file': file_name,
            'timestamp': data['timeCreated']
        }
        
        publisher.publish(
            topic_path,
            json.dumps(message).encode('utf-8')
        )
        
        print("Retraining triggered via Pub/Sub")
    
    return 'OK', 200