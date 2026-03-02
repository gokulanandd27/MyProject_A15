import requests
import time
import sys

BASE_URL = 'http://localhost:5000'

def print_pass(message):
    print(f"✅ PASS: {message}")

def print_fail(message):
    print(f"❌ FAIL: {message}")

def test_manual_endpoints():
    print("\n--- Testing Manual Moderation Endpoints ---")
    username = "ManualTestUser"
    
    # 1. Unban to start fresh
    print(f"Testing Unban for {username}...")
    resp = requests.post(f"{BASE_URL}/api/moderate/unban", json={'username': username})
    if resp.status_code == 200:
        print_pass("Unban successful")
    else:
        print_fail(f"Unban failed: {resp.text}")

    # 2. Check status (should be active)
    # We can check status by trying to send a message
    resp = requests.post(f"{BASE_URL}/analyze", json={'username': username, 'message': 'Hello world'})
    data = resp.json()
    if data.get('user_status') == 'active':
        print_pass("User is active")
    else:
        print_fail(f"User should be active but is {data.get('user_status')}")

    # 3. Manual Mute
    print(f"Testing Manual Mute for {username}...")
    resp = requests.post(f"{BASE_URL}/api/moderate/mute", json={'username': username, 'duration': 10})
    if resp.status_code == 200:
        print_pass("Manual mute successful")
    else:
        print_fail(f"Manual mute failed: {resp.text}")

    # Verify muted
    resp = requests.post(f"{BASE_URL}/analyze", json={'username': username, 'message': 'Hello world'})
    data = resp.json()
    if data.get('user_status') == 'muted':
        print_pass("User is correctly muted")
    else:
        print_fail(f"User should be muted but is {data.get('user_status')}")

    # 4. Manual Unmute
    print(f"Testing Manual Unmute for {username}...")
    resp = requests.post(f"{BASE_URL}/api/moderate/unmute", json={'username': username})
    if resp.status_code == 200:
        print_pass("Manual unmute successful")
    else:
        print_fail(f"Manual unmute failed: {resp.text}")

    # Verify active
    resp = requests.post(f"{BASE_URL}/analyze", json={'username': username, 'message': 'Hello world'})
    data = resp.json()
    if data.get('user_status') == 'active':
        print_pass("User is active again")
    else:
        print_fail(f"User should be active but is {data.get('user_status')}")

    # 5. Manual Ban
    print(f"Testing Manual Ban for {username}...")
    resp = requests.post(f"{BASE_URL}/api/moderate/ban", json={'username': username})
    if resp.status_code == 200:
        print_pass("Manual ban successful")
    else:
        print_fail(f"Manual ban failed: {resp.text}")

    # Verify banned
    resp = requests.post(f"{BASE_URL}/analyze", json={'username': username, 'message': 'Hello world'})
    data = resp.json()
    if data.get('user_status') == 'banned':
        print_pass("User is correctly banned")
    else:
        print_fail(f"User should be banned but is {data.get('user_status')}")

def test_automatic_moderation():
    print("\n--- Testing Automatic Moderation ---")
    username = "AutoTestUser"
    
    # Reset
    requests.post(f"{BASE_URL}/api/moderate/unban", json={'username': username})
    requests.post(f"{BASE_URL}/api/moderate/unmute", json={'username': username})
    
    toxic_msg = "idiot stupid"
    
    # Hit until muted
    print(f"Sending toxic message for {username}...")
    # Should mute immediately after ONE message now
    resp = requests.post(f"{BASE_URL}/analyze", json={'username': username, 'message': toxic_msg})
    data = resp.json()
    # The first response might carry the toxic flag but user status might update after?
    # Actually update_score sets mute. get_user_status is called BEFORE analysis in app.py logic.
    # So the current message is processed, score updated (and muted).
    # The NEXT message should be blocked.
    
    print("Sending check message to verify immediate mute...")
    resp = requests.post(f"{BASE_URL}/analyze", json={'username': username, 'message': "Am I muted?"})
    data = resp.json()
    status = data.get('user_status')
    message = data.get('display_text', '')
    
    print(f"Check Msg: Status={status}, Message='{message}'")

    if status == 'muted':
        print_pass("User automatically muted immediately")
        # Check specific message format
        if "⚠️" in message and "wait" in message:
             print_pass(f"Mute message format verified: {message}")
        else:
             print_fail(f"Mute message format unexpected: {message}")
        
        # TEST: Mute Expiry & Safe Message Handling
        # Manually expire the mute (simulating time passing)
        print("Simulating mute expiry...")
        requests.post(f"{BASE_URL}/api/moderate/unmute", json={'username': username})
        
        # User still has low score (from toxic hits)
        # Send SAFE message -> Should NOT be muted
        print("Sending SAFE message with low score...")
        resp = requests.post(f"{BASE_URL}/analyze", json={'username': username, 'message': "I am good now"})
        data = resp.json()
        status = data.get('user_status')
        score = data.get('reputation_score')
        
        if status == 'active':
             print_pass(f"User remains active after safe message (Score: {score})")
        else:
             print_fail(f"User was re-muted after safe message! (Status: {status}, Score: {score})")

    else:
        print_fail(f"User was not muted immediately. Status: {status}")

if __name__ == "__main__":
    try:
        test_manual_endpoints()
        test_automatic_moderation()
    except Exception as e:
        print_fail(f"Exception during test: {e}")
