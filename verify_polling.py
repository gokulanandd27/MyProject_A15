import requests
import time

BASE_URL = 'http://localhost:5000'

def test_polling():
    # 1. Send a toxic message
    print(f"Sending TOXIC message to {BASE_URL}/analyze...")
    payload = {'message': "stupid", 'username': "PollCheckUser"}
    try:
        r = requests.post(f"{BASE_URL}/analyze", json=payload)
        print(f"Send Status: {r.status_code}")
        # print(f"Send Response: {r.json()}") # We know this works from previous tests
    except Exception as e:
        print(f"Send Failed: {e}")
        return

    time.sleep(1)

    # 2. Poll messages and check for persistence of warning
    print(f"Polling {BASE_URL}/messages...")
    try:
        r = requests.get(f"{BASE_URL}/messages")
        print(f"Poll Status: {r.status_code}")
        data = r.json()
        
        # Find our message
        found = False
        for msg in data:
            if msg.get('username') == "PollCheckUser" and msg.get('display_text') == "stupid":
                found = True
                print(f"Found Message: {msg}")
                
                # VERIFY WARNING FIELDS
                if msg.get('warning_text') and msg.get('duration') == '7 seconds':
                    print("PASS: Warning fields persisted in polling!")
                else:
                    print(f"FAIL: Warning fields missing. warning_text={msg.get('warning_text')}, duration={msg.get('duration')}")
                break
        
        if not found:
            print("FAIL: Could not find the test message in polling response.")
            
    except Exception as e:
        print(f"Poll Failed: {e}")

if __name__ == "__main__":
    test_polling()
