from google import genai
import pandas as pd
import numpy as np
import json
from datetime import datetime
import os
import time
from dotenv import load_dotenv

# Load env variables including API key
load_dotenv()

class MinimalMLPipeline:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not found. Ensure .env is loaded or 'GEMINI_API_KEY' is set.")
        
        # Initialize the new SDK client
        self.client = genai.Client(api_key=self.api_key) 
    
    def run(self, data_path=None):
        print("[START] Starting Minimal MLOps Pipeline")
        
        # 1. Prepare data
        if data_path and os.path.exists(data_path):
            data = pd.read_csv(data_path)
        else:
            data = self.generate_sample_data()
        
        # 2. Create prompt template
        prompt = self.create_prompt_template(data)
        
        # 3. Train (few-shot learning)
        results = self.few_shot_learning(data, prompt)
        
        # 4. Save results
        self.save_results(results)
        
        print("[SUCCESS] Pipeline completed successfully!")
        return results
    
    def generate_sample_data(self):
        """Generate synthetic classification data"""
        np.random.seed(42)
        n_samples = 5
        return pd.DataFrame({
            'feature1': np.random.rand(n_samples),
            'feature2': np.random.randint(0, 100, n_samples),
            'feature3': np.random.choice(['A', 'B', 'C'], n_samples),
            'label': np.random.choice(['Positive', 'Negative'], n_samples)
        })
    
    def create_prompt_template(self, data):
        """Create optimized prompt"""
        categories = data['label'].unique().tolist()
        
        prompt = f"""You are a classification model. Given features, predict label.

Available categories: {categories}

Example format:
Feature1: 0.5, Feature2: 75, Feature3: A → Positive
Feature1: 0.2, Feature2: 30, Feature3: C → Negative

Now classify:
{{features}}

Return only the predicted label."""
        
        return prompt
    
    def few_shot_learning(self, data, prompt_template):
        """Simple few-shot learning with retry logic"""
        results = []
        
        # Limit to 5 for quick local verification/demo
        for i, row in data.head(5).iterrows(): 
            features = f"Feature1: {row['feature1']}, Feature2: {row['feature2']}, Feature3: {row['feature3']}"
            prompt = prompt_template.format(features=features)
            
            predicted = "ERROR"
            max_retries = 3
            base_delay = 5
            
            for attempt in range(max_retries):
                try:
                    response = self.client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt
                    )
                    predicted = response.text.strip()
                    print(f"Row {i}: Success")
                    time.sleep(1) # Flash is faster, can reduce delay
                    break
                except Exception as e:
                    if "429" in str(e) or "Quota" in str(e) or "429" in str(e): # Handle both SDK error types
                        delay = base_delay * (2 ** attempt)
                        print(f"Row {i}: Quota exceeded. Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        print(f"Prediction failed for row {i}: {e}")
                        break
            else:
                 print(f"Row {i}: Failed after retries")

            actual = row['label']
            
            results.append({
                'features': features,
                'predicted': predicted,
                'actual': actual,
                'correct': predicted == actual
            })
        
        # Avoid division by zero
        if not results:
            accuracy = 0.0
        else:
            accuracy = sum(r['correct'] for r in results) / len(results)
        
        return {
            'accuracy': accuracy,
            'predictions': results,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_results(self, results):
        """Save pipeline results"""
        os.makedirs('reports', exist_ok=True)
        filename = f"reports/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[SAVED] Results saved to {filename}")

if __name__ == "__main__":
    try:
        pipeline = MinimalMLPipeline()
        results = pipeline.run()
        print(f"[METRICS] Accuracy: {results['accuracy']:.2%}")
    except Exception as e:
        print(f"[ERROR] Pipeline Failed: {e}")
