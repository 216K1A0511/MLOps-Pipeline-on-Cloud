import os
import argparse
from prefect import flow, task

@task
def load_data(path):
    print(f"Loading data from: {path}")
    return "Data Loaded"

@task
def run_classification():
    print("Running Gemini-powered classification...")
    return "Classification Complete"

@flow(name="Gemini MLOps Pipeline")
def main_pipeline(data_path="synthetic", task_type="classification"):
    print(f"Starting {task_type} task...")
    data = load_data(data_path)
    result = run_classification()
    print(f"Pipeline Result: {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", default="synthetic")
    parser.add_argument("--task-type", default="classification")
    args = parser.parse_args()
    
    main_pipeline(data_path=args.data_path, task_type=args.task_type)