import urllib.request
import json
import sys
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

def verify():
    with open("verification_output.txt", "w") as f:
        f.write("Verifying 'reason' and 'severity' fields in API response...\n")
        
        # Payload with a known toxic word
        payload = {"message": "You are stupid", "username": "Tester"}
        
        f.write(f"Sending toxic message: {payload['message']}\n")
        data = post_json(f"{BASE_URL}/analyze", payload)
        
        if not data:
            f.write("[FAIL] No response from server.\n")
            return

        f.write(f"Response Received: {json.dumps(data, indent=2)}\n")
        
        if data.get('type') == 'toxic':
            f.write("[PASS] Message correctly classified as toxic.\n")
        else:
            f.write(f"[FAIL] Message not classified as toxic. Type: {data.get('type')}\n")
            
        reason = data.get('reason')
        severity = data.get('severity')
        
        if reason == "Contains banned words/slurs":
            f.write(f"[PASS] 'reason' field correctly updated: {reason}\n")
        elif reason:
            f.write(f"[FAIL] 'reason' field present but OLD or WRONG: {reason}\n")
        else:
            f.write("[FAIL] 'reason' field MISSING.\n")
            
        if severity:
            f.write(f"[PASS] 'severity' field present: {severity}\n")
        else:
            f.write("[FAIL] 'severity' field MISSING.\n")
            
        if reason and severity:
            f.write("\nSUCCESS: Both fields are present.\n")
        else:
            f.write("\nFAILURE: Missing fields.\n")

if __name__ == "__main__":
    verify()
