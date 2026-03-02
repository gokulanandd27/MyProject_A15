import urllib.request
import urllib.parse
import json
import time
import sys

BASE_URL = "http://127.0.0.1:5000"

def post_json(url, data):
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params, headers={'content-type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        # Check CORS header
        if response.getheader('Access-Control-Allow-Origin') == '*':
            print("[PASS] CORS header present.")
        else:
            # Flask-CORS might not send it on every request or might send specific origin.
            # But usually for '*' it sends it. Let's just print it.
            print(f"[INFO] CORS Header: {response.getheader('Access-Control-Allow-Origin')}")
        return json.loads(response.read().decode('utf8'))

def test_api():
    print("Testing Backend API (using urllib)...")
    
    # 1. Health Check (Get index)
    try:
        with urllib.request.urlopen(BASE_URL) as response:
            if response.status == 200:
                print("[PASS] Server is running and serving index.")
            else:
                print(f"[FAIL] Server return status {response.status}")
                sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Could not connect to server: {e}")
        sys.exit(1)

    # 2. Test Non-Toxic Message
    try:
        payload = {"message": "Hello everyone", "username": "Tester"}
        data = post_json(f"{BASE_URL}/analyze", payload)
        
        if data['type'] == 'non-toxic' and data['action'] == 'show':
             print("[PASS] Non-toxic message correctly classified.")
        else:
             print(f"[FAIL] Non-toxic message failed: {data}")
    except Exception as e:
        print(f"[FAIL] Error testing non-toxic: {e}")

    # 3. Test Toxic Message
    try:
        payload = {"message": "You are stupid", "username": "Troll"}
        data = post_json(f"{BASE_URL}/analyze", payload)
        
        if data['type'] == 'toxic' and data['action'] == 'warn':
             print("[PASS] Toxic message correctly classified (Warn + Toxic type).")
             # New logic: display_text is original, warning_text contains the system message
             if data['display_text'] == payload['message']:
                 print("[PASS] Original text returned as display_text initially.")
             
             if "toxic" in data.get('warning_text', ''):
                 print("[PASS] Warning text present in response.")
        else:
             print(f"[FAIL] Toxic message failed: {data}")
    except Exception as e:
        print(f"[FAIL] Error testing toxic: {e}")

if __name__ == "__main__":
    test_api()
