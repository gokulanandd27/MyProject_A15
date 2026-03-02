import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def post_json(url, data):
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params, headers={'content-type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf8'))
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def verify_reputation():
    with open("reputation_results.txt", "w") as f:
        f.write("Verifying Reputation System...\n")
        username = f"TestUser_{int(time.time())}" # Unique user
        
        # 1. Initial Check (First Message)
        f.write("\n[1] Sending first message (Should be active, Score 100)\n")
        data = post_json(f"{BASE_URL}/analyze", {"message": "Hello", "username": username})
        if data:
            f.write(f"Status: {data.get('user_status')}, Score: {data.get('reputation_score')}\n")
            if data.get('reputation_score') == 100: 
                f.write("PASS: Initial score is 100.\n")
            else:
                f.write(f"FAIL: Initial score is {data.get('reputation_score')}\n")

        # 2. Reduce Score (Send Toxic Messages)
        f.write("\n[2] Sending toxic messages to lower score...\n")
        
        # Send 4 High Toxicity messages (20 points each). 100 -> 80 -> 60 -> 40 -> 20 (Muted)
        for i in range(1, 6):
            data = post_json(f"{BASE_URL}/analyze", {"message": "You are stupid", "username": username})
            if data:
                f.write(f"Msg {i}: Status: {data.get('user_status')}, Score: {data.get('reputation_score')}, Action: {data.get('action')}\n")
                
                if data.get('user_status') == 'muted':
                    f.write("PASS: User is MUTED.\n")
                    break
        
        # 3. Verify Blocked when Muted
        f.write("\n[3] Sending message while muted...\n")
        data = post_json(f"{BASE_URL}/analyze", {"message": "Am I muted?", "username": username})
        if data and data.get('action') == 'block':
             f.write(f"PASS: Message blocked. Reason: {data.get('warning_text')}\n")
        elif data:
             f.write(f"FAIL: Message NOT blocked. Action: {data.get('action')}\n")
        else:
             f.write("FAIL: No response received.\n")

if __name__ == "__main__":
    verify_reputation()
