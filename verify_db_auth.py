import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def post_json(url, data, token=None):
    params = json.dumps(data).encode('utf8')
    headers = {'content-type': 'application/json'}
    if token:
        headers['Authorization'] = f"Bearer {token}"
        
    req = urllib.request.Request(url, data=params, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf8'))
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def verify_db_auth():
    print("Verifying Database & Auth...")
    username = f"AuthUser_{int(time.time())}"
    password = "password123"
    
    # 1. Register
    print(f"\n[1] Registering user: {username}")
    reg_res = post_json(f"{BASE_URL}/register", {"username": username, "password": password})
    print(f"Register Response: {reg_res}")
    
    # 2. Login
    print(f"\n[2] Logging in...")
    login_res = post_json(f"{BASE_URL}/login", {"username": username, "password": password})
    print(f"Login Response: {login_res}")
    
    token = None
    if login_res and 'access_token' in login_res:
        token = login_res['access_token']
        print(f"Login Success! Token: {token[:20]}...")
    else:
        print("Login Failed.")
        return

    # 3. Send Message (Update Reputation)
    print(f"\n[3] Sending toxic message to lower reputation...")
    # Send a toxic message
    post_json(f"{BASE_URL}/analyze", {"message": "stupid", "username": username}, token)
    
    # Check status
    check_res = post_json(f"{BASE_URL}/analyze", {"message": "hello", "username": username}, token)
    if check_res:
        score = check_res.get('reputation_score')
        print(f"Current Reputation: {score}")
        if score < 100:
            print("PASS: Reputation updated in DB.")
        else:
            print("FAIL: Reputation NOT updated.")

    return username

if __name__ == "__main__":
    verify_db_auth()
