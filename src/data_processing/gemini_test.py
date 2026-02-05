import os
import google.generativeai as genai
from prefect import flow, task

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@task
def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

@flow(log_prints=True)
def test_gemini_pipeline():
    result = ask_gemini("Explain MLOps in one sentence for a Cloud Engineer.")
    print(f"Gemini says: {result}")

if __name__ == "__main__":
    test_gemini_pipeline()