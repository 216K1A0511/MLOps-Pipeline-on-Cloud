import os
import argparse
import yaml
import pandas as pd
import time
from google import genai
from prefect import flow, task

def load_config(config_path="configs/gemini_config.yaml"):
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}

@task
def load_data(path):
    print(f"Loading data from: {path}")
    if os.path.exists(path):
        return pd.read_csv(path)
    print("Warning: Data file not found, using empty DataFrame")
    return pd.DataFrame()

def run_mock_classification(data):
    """Mock classification for testing without API"""
    import random
    
    results = []
    mock_responses = ["positive", "negative", "neutral", "mixed", "uncertain"]
    
    print("Starting mock classification...")
    for i, row in data.iterrows():
        # Simulate processing time
        time.sleep(0.1)
        result = random.choice(mock_responses)
        results.append(result)
        print(f"Sample {i}: Mock classification: {result}")
    
    return results

@task
def run_classification(config, data, use_mock=False):
    print("Initializing Gemini model...")
    
    if use_mock:
        print("Using mock classification (no API calls)")
        return run_mock_classification(data)

    results = []
    
    # Security: Prioritize Environment Variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = config.get('gemini', {}).get('api_key')
        if not api_key:
             return "Error: Missing API Key"
    
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return f"Error initializing client: {e}"
    
    model_name = config.get('gemini', {}).get('model_name', 'gemini-2.0-flash')
    print(f"Running classification with {model_name}...")
    
    # Process only 5 samples for Free Tier (Real API)
    subset = data.head(5)
    
    for i, row in subset.iterrows():
        feature_text = f"Feature1: {row.get('feature1', 0)}, Feature2: {row.get('feature2', 0)}"
        prompt = f"Classify this sentiment based on features: '{feature_text}'"
        
        prediction = "ERROR"
        max_retries = 3
        base_delay = 5
        
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                prediction = response.text.strip()
                print(f"Sample {i}: Success")
                # Free Tier Rate Limiting - Critical for Quota Management
                time.sleep(4) 
                break
            except Exception as e:
                is_quota = "429" in str(e) or "Quota" in str(e)
                if is_quota:
                    delay = base_delay * (2 ** attempt)
                    print(f"Sample {i}: Quota exceeded. Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    print(f"Sample {i}: Error: {e}")
                    break
        
        results.append(prediction)
    
    return results

@flow(name="Gemini MLOps Pipeline")
def main_pipeline(data_path="synthetic", task_type="classification", use_mock=False):
    print(f"Starting {task_type} task...")
    print(f"Mock Mode: {use_mock}")
    
    # Load Configuration
    config = load_config()
    if not config:
         config = {'gemini': {'api_key': '', 'model_name': 'gemini-2.0-flash'}}

    data = load_data(data_path)
    if not data.empty:
        results = run_classification(config, data, use_mock=use_mock)
        print(f"Pipeline Results: {results}")
        
        # Save results
        os.makedirs("reports", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        pd.DataFrame({'prediction': results}).to_csv(f"reports/results_{timestamp}.csv")
        print(f"Saved to reports/results_{timestamp}.csv")
    else:
        print("No data to process.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", default="data/raw/sample_data.csv")
    parser.add_argument("--task-type", default="classification")
    parser.add_argument("--run-id", default="default_run", help="Execution identifier")
    parser.add_argument("--use-mock", action="store_true", help="Use mock mode without API calls")
    args = parser.parse_args()
    
    main_pipeline(data_path=args.data_path, task_type=args.task_type, use_mock=args.use_mock)