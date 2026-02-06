import sys
print(f"Python: {sys.executable}")
print(f"Path: {sys.path}")

try:
    import google
    print(f"Google: {google}")
    print(f"Google Path: {google.__path__}")
except ImportError as e:
    print(f"Failed to import google: {e}")

try:
    import google.genai
    print(f"Google GenAI: {google.genai}")
except ImportError as e:
    print(f"Failed to import google.genai: {e}")

try:
    from google import genai
    print(f"From Google Import GenAI: {genai}")
except ImportError as e:
    print(f"Failed from google import genai: {e}")
