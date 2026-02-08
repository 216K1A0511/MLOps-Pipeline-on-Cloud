import requests
import os
import sys
from dotenv import load_dotenv

def get_linkedin_urn():
    """
    Fetch the LinkedIn Person URN using the access token from .env
    """
    load_dotenv()
    
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    if not access_token:
        print("[ERROR] LINKEDIN_ACCESS_TOKEN not found in .env file")
        return None

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    
    print("Fetching LinkedIn information...")
    try:
        response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
        response.raise_for_status()
        
        user_data = response.json()
        urn = user_data.get('id')
        
        if urn:
            print(f"\n[SUCCESS] Your LinkedIn Person URN is: {urn}")
            print(f"-> Use this value for the 'LINKEDIN_PERSON_URN' secret in GitHub.")
            return urn
        else:
            print("[ERROR] Could not find 'id' in the response.")
            print(user_data)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error fetching data: {e}")
        if hasattr(e, 'response') and e.response is not None:
             try:
                print(f"Response: {e.response.text}")
             except:
                print("Response could not be decoded")
        return None

if __name__ == "__main__":
    get_linkedin_urn()
