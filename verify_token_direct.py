import requests

token = "AQW7Cq-oP_KbLYc-7N0v0PidXXqyG2sGPswsK0xPxEkDOKPwyQaD7jqkVX_Md6hLA46NXpx0-seSlZEpL7vg9L4wrS2yiLm_CyL39CGdcjGd8Ne_onZjgyc_xHh1G_dI5gdBxRMV8NiV_IAgDM0lLEgJaK7fPoisR_lpmz2jubS0uAUZEd0FWqU08-OmUKps85f_lMdQmQ-r1PLiO_gChe0Y-MBJ1ujlhXMrfGqKCFAyEoZB846ptBLQNFHrLywNqebHrvYgdBqNFIAvu-DejfQrR6BVIA1cWHi1LaJIbS13MaOZRoFmpBF990r6rKvY0wf3MJ6Fd4S2LqDa6yIIuUm-5WqWuQ"

print(f"Testing Token: {token[:10]}...{token[-10:]}")

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
}

try:
    print("Sending request to https://api.linkedin.com/v2/me ...")
    response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    print("\nTesting https://api.linkedin.com/v2/userinfo ...")
    response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

except Exception as e:
    print(f"Exception: {e}")
