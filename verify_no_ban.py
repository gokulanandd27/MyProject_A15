import requests
import time
from app import app, db, User, reputation_manager

BASE_URL = 'http://localhost:5000'
USERNAME = "NoBanUser"

def test_no_ban():
    # 1. Setup: Force reputation to 0
    print(f"Setting up user '{USERNAME}' with 0 reputation...")
    with app.app_context():
        user = User.query.filter_by(username=USERNAME).first()
        if not user:
            user = User(username=USERNAME, reputation_score=100)
            db.session.add(user)
        
        user.reputation_score = 0
        user.is_banned = True # Simulate existing ban state to see if logic overrides it or ignores it
        
        # We manually set is_banned=True to test if get_user_status IGNORES it. 
        # But wait, get_user_status reads from DB. If I commented out the check, it should ignore the DB flag.
        
        db.session.commit()
        print(f"User setup complete. Banned={user.is_banned}, Score={user.reputation_score}")

    # 2. Check Status via Internal Method (should be active)
    status = reputation_manager.get_user_status(USERNAME)
    print(f"Internal Status Check: {status}")
    
    if status['status'] == 'active':
        print("PASS: User status is ACTIVE despite low score/ban flag.")
    else:
        print(f"FAIL: User status is {status['status']}")

    # 3. Try access via API
    print(f"Sending message as '{USERNAME}'...")
    try:
        r = requests.post(f"{BASE_URL}/analyze", json={'message': 'hello from low rep', 'username': USERNAME})
        print(f"API Response Code: {r.status_code}")
        print(f"API Response: {r.json()}")
        
        if r.status_code == 200 and r.json().get('action') != 'block':
             print("PASS: Message accepted.")
        else:
             print("FAIL: Message blocked or error.")
            
    except Exception as e:
        print(f"API Request Failed: {e}")

if __name__ == "__main__":
    test_no_ban()
