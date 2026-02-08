"""
Main entry point for LinkedIn Automation Bot
Runs on GitHub Actions or locally
"""

import os
import sys
import datetime
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main function that runs the LinkedIn automation"""
    print("="*60)
    print("[BOT] LinkedIn Automation Bot")
    print(f"[INFO] Started at: {datetime.datetime.now()}")
    print("="*60)
    
    # Load environment variables
    load_dotenv()
    
    # Check for required environment variables
    required_vars = ['LINKEDIN_ACCESS_TOKEN', 'LINKEDIN_PERSON_URN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"[MISSING] Environment variables: {missing_vars}")
        print("Please set these in GitHub Secrets or .env file")
        return 1
    
    try:
        # Import and run LinkedIn poster
        from notifications.linkedin_poster import LinkedInThoughtLeaderPoster
        
        # Create pipeline results
        pipeline_results = {
            "project_name": "MLOps Pipeline with LinkedIn Automation",
            "status": "SUCCESS",
            "execution_time": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "key_achievement": "Automated LinkedIn posts via GitHub Actions",
            "technologies": ["Python", "GitHub Actions", "LinkedIn API", "Gemini AI"],
            "time_saved": "24/7 automation without manual intervention"
        }
        
        # Initialize and run
        poster = LinkedInThoughtLeaderPoster()
        
        print("\n[INFO] Validating credentials...")
        if poster.validate_credentials():
            print("[OK] Credentials validated successfully!")
            
            # Check if it's posting time (9 AM UTC)
            current_hour = datetime.datetime.utcnow().hour
            current_minute = datetime.datetime.utcnow().minute
            
            # Post only at 9:00 AM UTC (2:30 PM IST)
            # OR if TEST_POSTING is true (for manual triggers or testing)
            force_post = os.getenv('TEST_POSTING', 'false').lower() == 'true'
            
            if force_post or (current_hour == 9 and current_minute <= 5):
                if force_post:
                     print("[WARN] FORCE POSTING enabled")
                else:
                     print("[INFO] It's posting time! (9 AM UTC / 2:30 PM IST)")
                     
                print("[INFO] Generating thought leadership content...")
                
                result = poster.automated_thought_leadership_post(pipeline_results)
                
                if result.get('success'):
                    print("[OK] LinkedIn post published successfully!")
                    if 'post_url' in result:
                        print(f"[LINK] Post URL: {result['post_url']}")
                    
                    # Log engagement predictions
                    if 'engagement_prediction' in result:
                        pred = result['engagement_prediction']
                        print(f"\n[STATS] Engagement Predictions:")
                        print(f"   - Impressions: {pred.get('predicted_impressions', 0):,}")
                        print(f"   - Likes: {pred.get('predicted_likes', 0)}")
                        print(f"   - Comments: {pred.get('predicted_comments', 0)}")
                else:
                    print(f"[ERROR] Failed to publish: {result.get('error', 'Unknown error')}")
            else:
                print(f"[INFO] Not posting time yet (Current: {current_hour}:{current_minute} UTC)")
                print("Next post at: 9:00 AM UTC (2:30 PM IST)")
                print("\n[OK] Bot is running correctly. Will post at scheduled time.")
        else:
            print("[ERROR] Credentials validation failed")
            print("Please check your LinkedIn credentials in GitHub Secrets")
            return 1
            
    except ImportError as e:
         print(f"[ERROR] Could not import 'src.notifications.linkedin_poster': {e}")
         import traceback
         traceback.print_exc()
         return 1
    except Exception as e:
        print(f"[ERROR] Occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "="*60)
    print("[OK] Bot execution completed successfully!")
    print("="*60)
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
