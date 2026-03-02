import requests
import time
import sys

BASE_URL = 'http://localhost:5000'
USERNAME = "SeverityTester"

def wait_for_server():
    print("Waiting for server to start...")
    for i in range(30):
        try:
            requests.get(BASE_URL)
            print("Server is up!")
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            print(".", end="", flush=True)
    print("\nServer timed out.")
    return False

def test_severity():
    if not wait_for_server():
        sys.exit(1)

    print(f"Testing Severity Levels for user '{USERNAME}'...")
    
    # 1. Test High Severity
    print("\n--- Sending HIGH severity message ('fuck') ---")
    try:
        r = requests.post(f"{BASE_URL}/analyze", json={'message': 'fuck you', 'username': USERNAME})
        if r.status_code != 200:
             print(f"Error: Server returned {r.status_code}")
             print(r.text)
             return

        data = r.json()
        print(f"Response: {data.get('warning_text', 'No warning')}")
        
        if data.get('severity') == 'High':
            print("PASS: Detected as High Severity")
        else:
            print(f"FAIL: Expected High, got {data.get('severity')}")
            
    except Exception as e:
        print(f"Error: {e}")

    # 2. Test Medium Severity
    print("\n--- Sending MEDIUM severity message ('stupid') ---")
    try:
        r = requests.post(f"{BASE_URL}/analyze", json={'message': 'you are stupid', 'username': USERNAME})
        if r.status_code != 200:
             print(f"Error: Server returned {r.status_code}")
             return

        data = r.json()
        print(f"Response: {data.get('warning_text', 'No warning')}")
        
        if data.get('severity') == 'Medium':
             print("PASS: Detected as Medium Severity")
        else:
             print(f"FAIL: Expected Medium, got {data.get('severity')}")

    except Exception as e:
        print(f"Error: {e}")

    # 3. Verify Persistence
    print("\n--- Verifying Persistence (GET /messages) ---")
    try:
        time.sleep(1)
        r = requests.get(f"{BASE_URL}/messages")
        messages = r.json()
        
        # Check last 2 messages
        found_high = False
        found_medium = False
        
        for m in messages:
            if m['username'] == USERNAME:
                if 'stupid' in m['display_text'] and m.get('severity') == 'Medium':
                    found_medium = True
                if 'fuck' in m['display_text'] and m.get('severity') == 'High':
                    found_high = True
                    
        if found_high and found_medium:
             print("PASS: Both High and Medium severity persisted correctly.")
        else:
             print(f"FAIL: Persistence check failed. High={found_high}, Medium={found_medium}")
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_severity()
