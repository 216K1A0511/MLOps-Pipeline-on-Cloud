import os
import argparse
import yaml
import google.generativeai as genai
from prefect import flow, task

def load_config(config_path="configs/gemini_config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

@task
def load_data(path):
    print(f"Loading data from: {path}")
    # Simulate data loading
    return "Data Loaded"

@task
def run_classification(config):
    print("Initializing Gemini model...")
    
    # Security: Prioritize Environment Variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = config['gemini']['api_key']
        print("Warning: Using API key from config file (Not recommended for production)")
    else:
        print("Success: Using API key from Environment Variable")
    
    genai.configure(api_key=api_key)
    
    model_name = config['gemini'].get('model_name', 'gemini-1.5-flash')
    model = genai.GenerativeModel(model_name)
    
    print(f"Running classification with {model_name}...")
    try:
        response = model.generate_content("Classify this sentiment: 'I love building MLOps pipelines!'")
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@flow(name="Gemini MLOps Pipeline")
def main_pipeline(data_path="synthetic", task_type="classification"):
    print(f"Starting {task_type} task...")
    
    # Load Configuration
    try:
        config = load_config()
    except FileNotFoundError:
        print("Config file not found, using defaults")
        config = {'gemini': {'api_key': '', 'model_name': 'gemini-1.5-flash'}}

    data = load_data(data_path)
    result = run_classification(config)
    print(f"Pipeline Result: {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", default="synthetic")
    parser.add_argument("--task-type", default="classification")
    args = parser.parse_args()
    
    main_pipeline(data_path=args.data_path, task_type=args.task_type)