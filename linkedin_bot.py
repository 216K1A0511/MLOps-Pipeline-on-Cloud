
import os
import time
import json
import random
from datetime import datetime
from dotenv import load_dotenv

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import content generator
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from notifications.linkedin_poster import LinkedInThoughtLeaderPoster

# Load environment variables
load_dotenv()

def setup_driver():
    """Configure and return a headless Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    # Initialize driver (Selenium 4 manages drivers automatically)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_linkedin(driver, username, password):
    """Login to LinkedIn"""
    print("[INFO] Logging into LinkedIn...")
    driver.get("https://www.linkedin.com/login")
    
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = driver.find_element(By.ID, "password")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        
        # Wait for home page or feed
        WebDriverWait(driver, 20).until(
            EC.url_contains("feed")
        )
        print("[SUCCESS] Logged in successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        driver.save_screenshot("linkedin_posts/login_error.png")
        return False

def post_content(driver, content):
    """Post content to LinkedIn"""
    print("[INFO] Navigating to create post...")
    try:
        # Click "Start a post" button
        # Determining exact selector can be tricky as LinkedIn changes classes.
        # We'll try a few common strategies.
        
        # Strategy 1: Navigate directly to feed (already there) and click the button
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-box-feed-entry__trigger')]"))
        )
        post_button.click()
        
        # Wait for modal
        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ql-editor"))
        )
        
        # Type content
        print("[INFO] Typing content...")
        editor.send_keys(content)
        time.sleep(2) # Wait for preview/rendering
        
        # Click Post
        print("[INFO] Clicking Post button...")
        submit_button = driver.find_element(By.CSS_SELECTOR, ".share-actions__primary-action")
        submit_button.click()
        
        # Wait for post to appear or modal to close
        time.sleep(5)
        print("[SUCCESS] Post submitted!") 
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to post: {e}")
        driver.save_screenshot("linkedin_posts/posting_error.png")
        return False

def main():
    print("="*60)
    print("LinkedIn Selenium Automation Bot")
    print("="*60)
    
    # Ensure artifact directory exists
    os.makedirs("linkedin_posts", exist_ok=True)
    
    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not username or not password:
        print("[ERROR] LINKEDIN_USERNAME or LINKEDIN_PASSWORD not set.")
        return
    
    # Generate Content
    poster = LinkedInThoughtLeaderPoster()
    pipeline_results = {
        "project_name": "MLOps Pipeline",
        "status": "SUCCESS",
        "timestamp": datetime.now().isoformat()
    }
    
    print("[INFO] Generating content using Gemini...")
    content = poster.generate_thought_leadership_content(pipeline_results)
    
    if not content:
        print("[ERROR] Failed to generate content.")
        return

    print("\n[GENERATED CONTENT]:")
    print("-" * 20)
    try:
        print(content)
    except:
        print(content.encode('utf-8'))
    print("-" * 20)
    
    # Save content to file for artifact
    with open("linkedin_posts/post_content.txt", "w", encoding="utf-8") as f:
        f.write(content)

    # Initialize Driver
    driver = setup_driver()
    
    try:
        if login_linkedin(driver, username, password):
            if post_content(driver, content):
                # Take success screenshot
                driver.save_screenshot("linkedin_posts/success_post.png")
                print("[INFO] Screenshot saved to linkedin_posts/success_post.png")
            else:
                 print("[WARN] Posting failed, check screenshots.")
        else:
            print("[ERROR] Could not login.")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
