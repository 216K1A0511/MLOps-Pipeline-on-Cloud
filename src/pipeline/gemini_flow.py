from prefect import flow, task
import time

@task
def get_raw_data():
    print("Fetching data from Gemini API...")
    return {"status": "success", "data": [10, 20, 30]}

@task
def process_data(data):
    print("Processing AI data for MLOps...")
    return [x * 2 for x in data["data"]]

@flow(log_prints=True)
def gemini_mlops_pipeline():
    raw = get_raw_data()
    processed = process_data(raw)
    print(f"Pipeline Complete! Results: {processed}")

if __name__ == "__main__":
    gemini_mlops_pipeline()