import json
import glob
import pandas as pd
from datetime import datetime
import os

# Collect all reports
reports = []
report_files = glob.glob("reports/*.json")
for report_file in report_files:
    try:
        with open(report_file, 'r') as f:
            data = json.load(f)
            data['file'] = report_file
            
            # Normalize structure if minimal_pipeline format differs from full pipeline
            if 'accuracy' in data:
                data['metrics'] = {'accuracy': data['accuracy']}
                
            reports.append(data)
    except:
        continue

if reports:
    # Create DataFrame
    df_data = []
    for r in reports:
        entry = {
            'timestamp': r.get('timestamp'),
            'accuracy': r.get('metrics', {}).get('accuracy', 0),
            'deployed': r.get('deployment_ready', False),
            'samples': 0 # Default
        }
        # Try to find samples count if available
        if 'predictions' in r:
            entry['samples'] = len(r['predictions'])
            
        df_data.append(entry)

    df = pd.DataFrame(df_data)
    
    # Sort by timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    print("PERFORMANCE TREND ANALYSIS")
    print("=" * 50)
    print(f"Total Runs: {len(df)}")
    if not df.empty:
        print(f"Latest Accuracy: {df.iloc[-1]['accuracy']:.3f}")
        print(f"Best Accuracy: {df['accuracy'].max():.3f}")
        print(f"Average Accuracy: {df['accuracy'].mean():.3f}")
        print(f"Deployed Models: {df['deployed'].sum()}")
        
        # Show trend
        if len(df) > 1:
            print("\nTrend Analysis:")
            improvement = df.iloc[-1]['accuracy'] - df.iloc[0]['accuracy']
            print(f"Overall Improvement: {improvement:+.3f}")
            
            if improvement > 0:
                print("[GOOD] Model performance is improving!")
            elif improvement < 0:
                print("[WARN] Model performance may be degrading")
            else:
                print("[INFO] Model performance is stable")
else:
    print("No reports found. Run the pipeline first.")

print("\nTo improve performance:")
print("1. Add more training data")
print("2. Experiment with prompt engineering")
print("3. Adjust Gemini model parameters (temperature, max_tokens)")
