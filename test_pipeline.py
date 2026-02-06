import sys
import os
import pandas as pd
from src.pipeline.pipeline import run_mock_classification

# Create mock data
data = pd.DataFrame([
    {"feature1": 0.5, "feature2": 10},
    {"feature1": 0.1, "feature2": 90},
    {"feature1": 0.9, "feature2": 50}
])

print("Running mock test...")
results = run_mock_classification(data)
print("Test Results:")
print(results)

if len(results) == 3:
    print("SUCCESS: Got 3 mock predictions")
else:
    print("FAILURE: Incorrect number of results")
