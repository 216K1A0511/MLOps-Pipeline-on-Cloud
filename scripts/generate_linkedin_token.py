import os
import secrets
import requests
import webbrowser
from urllib.parse import urlencode
from flask import Flask, request, redirect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/callback'

if not CLIENT_ID or not CLIENT_SECRET:
    print("[ERROR] LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET must be set in .env file")
    exit(1)

app = Flask(__name__)

# State to prevent CSRF
state = secrets.token_hex(16)

@app.route('/')
def home():
    """Redirect to LinkedIn Authorization URL"""
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': 'w_member_social r_liteprofile openid email',
    }
    auth_url = 'https://www.linkedin.com/oauth/v2/authorization?' + urlencode(params)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    """Handle the callback from LinkedIn"""
    code = request.args.get('code')
    returned_state = request.args.get('state')
    
    if returned_state != state:
        return "Error: State mismatch. Possible CSRF attack.", 400
    
    if not code:
        return "Error: No code received", 400
    
    # Exchange code for access token
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        data = response.json()
        access_token = data.get('access_token')
        
        # Verify token immediately
        me_response = requests.get('https://api.linkedin.com/v2/me', headers={
            'Authorization': f'Bearer {access_token}'
        })
        userinfo_response = requests.get('https://api.linkedin.com/v2/userinfo', headers={
            'Authorization': f'Bearer {access_token}'
        })
        
        urn = "Unknown"
        if me_response.status_code == 200:
            urn = me_response.json().get('id', 'Unknown')
        
        return f"""
        <h1>Authentication Results</h1>
        <p><strong>Access Token:</strong> <br><code>{access_token}</code></p>
        
        <h3>Verification Status:</h3>
        <ul>
            <li><strong>v2/me Endpoint:</strong> {me_response.status_code} - {me_response.text}</li>
            <li><strong>v2/userinfo Endpoint:</strong> {userinfo_response.status_code} - {userinfo_response.text}</li>
        </ul>
        
        <p><strong>Person URN:</strong> {urn}</p>
        
        <p>If Status is 200, please copy the Access Token and URN.</p>
        <p>If Status is 401, the token is invalid immediately (check Client Secret?).</p>
        
        <script>window.stop();</script>
        """
        
    except Exception as e:
        return f"Error exchanging token: {e}", 500

def get_urn(access_token):
    # Deprecated in favor of inline check above
    pass

if __name__ == "__main__":
    print("="*60)
    print("[KEY] LinkedIn Token Generator")
    print("="*60)
    print(f"1. Make sure your LinkedIn App Redirect URL is set to: {REDIRECT_URI}")
    print("2. I will open a browser window for you to login.")
    print("3. After login, copy the Access Token and URN from the browser.")
    print("\nStarting server on port 8000...")
    
    # Open browser automatically
    webbrowser.open('http://localhost:8000')
    
    app.run(port=8000)
