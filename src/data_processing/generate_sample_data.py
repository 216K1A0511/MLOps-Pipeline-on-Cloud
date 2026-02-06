import pandas as pd
import numpy as np
import os

def generate_data():
    # Ensure directory exists
    os.makedirs('data/raw', exist_ok=True)

    np.random.seed(42)
    n_samples = 5
    data = {
        'feature1': np.random.rand(n_samples),
        'feature2': np.random.randint(0, 100, n_samples),
        'feature3': np.random.choice(['A', 'B', 'C'], n_samples),
        'label': np.random.choice(['Positive', 'Negative'], n_samples)
    }
    pd.DataFrame(data).to_csv('data/raw/sample_data.csv', index=False)
    print(f'Generated {n_samples} samples in data/raw/sample_data.csv')

if __name__ == "__main__":
    generate_data()
