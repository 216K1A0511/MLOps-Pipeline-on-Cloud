"""
Helper script to get LinkedIn OAuth Access Token
"""

import requests
import secrets
import string
import webbrowser
import time
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = 'https://www.google.com'  # Standard redirect for testing
SCOPE = 'w_member_social'  # Permission to post

def generate_random_state(length=16):
    """Generate a random state string for CSRF protection"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_authorization_code():
    """Step 1: Get Authorization Code"""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Error: Missing CLIENT_ID or CLIENT_SECRET in .env file.")
        print("Please add them to your .env file first.")
        return None

    state = generate_random_state()
    
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': SCOPE
    }
    
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
    
    print("\n" + "="*60)
    print("🔐 LinkedIn Authentication Step 1")
    print("="*60)
    print("To get your access token, we need to authorize this app.")
    print("\n1. I will open the LinkedIn authorization page for you.")
    print("2. Login and click 'Allow'.")
    print("3. You will be redirected to Google.")
    print("4. Copy the FULL URL from your browser's address bar.")
    print("5. Paste it back here.")
    
    input("\nPress Enter to open the browser...")
    webbrowser.open(auth_url)
    
    redirect_response = input("\n🔗 Paste the full redirected URL here: ").strip()
    
    # Extract code from URL
    try:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(redirect_response)
        params = parse_qs(parsed.query)
        
        if 'error' in params:
            print(f"❌ Authorization Error: {params['error'][0]}")
            return None
            
        if 'code' not in params:
            print("❌ Error: Could not find authorization code in the URL.")
            return None
            
        return params['code'][0]
        
    except Exception as e:
        print(f"❌ Error parsing URL: {e}")
        return None

def get_access_token(auth_code):
    """Step 2: Exchange Code for Access Token"""
    if not auth_code:
        return None
        
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    print("\n⏳ Exchanging code for access token...")
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access_token')
            expires_in = data.get('expires_in')
            
            print("\n" + "="*60)
            print("✅ SUCCESS! Access Token Generated")
            print("="*60)
            print(f"\nAccess Token: {access_token}")
            print(f"Expires in: {expires_in} seconds ({expires_in/86400:.1f} days)")
            print("\n📋 Next Steps:")
            print("1. Copy the Access Token above.")
            print("2. Paste it into your .env file as LINKEDIN_ACCESS_TOKEN.")
            
            return access_token
        else:
            print(f"❌ Error getting token: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def get_person_urn(access_token):
    """Step 3: Get Person URN (User ID)"""
    if not access_token:
        return
        
    url = "https://api.linkedin.com/v2/userinfo"
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    print("\n🔍 Fetching your LinkedIn Profile ID (URN)...")
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            urn = data.get('sub') # In v2/userinfo, 'sub' is the ID
            
            print(f"\n✅ Found Person URN: {urn}")
            print("\n📋 Add this to your .env file as LINKEDIN_PERSON_URN.")
            print(f"LINKEDIN_PERSON_URN={urn}")
            
        else:
            print(f"❌ Error getting profile: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    code = get_authorization_code()
    if code:
        token = get_access_token(code)
        if token:
            get_person_urn(token)
