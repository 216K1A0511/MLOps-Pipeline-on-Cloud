import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print("TESTING MLOPS PIPELINE COMPONENTS")
print("=" * 50)

# 1. Check environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print(f"1. Environment: {'[OK]' if GEMINI_API_KEY else '[FAIL]'}")
if GEMINI_API_KEY:
    print(f"   API Key present (length: {len(GEMINI_API_KEY)})")

# 2. Check imports
print("\n2. Module Imports:")
modules = [
    ('google.generativeai', 'genai'),
    ('pandas', 'pd'),
    ('numpy', 'np'),
    ('fastapi', 'FastAPI')
]

for module, alias in modules:
    try:
        exec(f"import {module} as {alias}")
        print(f"   [OK] {module}")
    except ImportError as e:
        print(f"   [FAIL] {module}: {e}")

# 3. Check directory structure
print("\n3. Directory Structure:")
required_dirs = ['data', 'models', 'logs', 'reports', 'configs', 'src']
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f"   [OK] {dir_name}/")
    else:
        print(f"   [MISSING] {dir_name}/")

# 4. Generate mini report
print("\n4. Generating Test Report:")
test_report = {
    "test_timestamp": datetime.now().isoformat(),
    "components_tested": ["environment", "imports", "directories"],
    "status": "PASS" if GEMINI_API_KEY else "PARTIAL"
}

# Save report
os.makedirs('reports', exist_ok=True)
report_path = 'reports/test_report.json'
with open(report_path, 'w') as f:
    json.dump(test_report, f, indent=2)
    
print(f"   [OK] Report saved to: {report_path}")
print("\n" + "=" * 50)
print("Pipeline Test Complete!")
