from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=api_key)

print("Listing models...")
try:
    for m in client.models.list(config={'page_size': 100}):
        print(f"Model: {m.name}")
        # print(dir(m)) # Uncomment if needed for debugging
        # if 'generateContent' in m.supported_generation_methods:
        #    print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
