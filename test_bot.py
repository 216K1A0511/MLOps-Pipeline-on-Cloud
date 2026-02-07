"""
Test script for LinkedIn Bot (run locally)
"""

import os
import sys
from dotenv import load_dotenv

def test_locally():
    """Test the bot locally without posting to LinkedIn"""
    print("Testing LinkedIn Bot Locally")
    print("="*40)
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Create .env file with:")
        print("LINKEDIN_ACCESS_TOKEN=your_token")
        print("LINKEDIN_PERSON_URN=your_urn")
        print("GEMINI_API_KEY=your_key")
        return
    
    # Check required variables
    required = ['LINKEDIN_ACCESS_TOKEN', 'LINKEDIN_PERSON_URN']
    for var in required:
        if not os.getenv(var):
            print(f"[MISSING]: {var}")
    
    # Test imports
    try:
        sys.path.append('src')
        try:
             from notifications.linkedin_poster import LinkedInThoughtLeaderPoster
             print("[OK] All imports successful")
        except ImportError as e:
             print(f"[ERROR] Import failed: {e}")
             return

        
        # Test credential validation
        print("\n[INFO] Validating credentials...")
        poster = LinkedInThoughtLeaderPoster()
        if poster.validate_credentials():
            print("[OK] LinkedIn credentials validated")
        else:
            print("[ERROR] LinkedIn credentials invalid (Expected if tokens are empty)")
            
        # Test content generation
        print("\n[INFO] Testing content generation...")
        test_results = {
            "project_name": "Test Pipeline",
            "status": "SUCCESS",
            "key_achievement": "Testing content generation"
        }
        
        try:
            content = poster.generate_thought_leadership_content(test_results)
            if content:
                print(f"[OK] Content generated ({len(content)} characters)")
                print(f"\n[INFO] Sample (first 200 chars):")
                print("-" * 40)
                try:
                    safe_content = content[:200].encode('cp1252', errors='ignore').decode('cp1252')
                    print(safe_content + "...")
                except:
                    print(content[:200].encode('utf-8'))
                print("-" * 40)
            else:
                 print("[WARN] Content generation returned empty result (check API key)")
        except Exception as e:
             print(f"[ERROR] Content generation failed: {e}")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_locally()
