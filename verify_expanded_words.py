import requests
import time
import sys

BASE_URL = 'http://localhost:5000'
USERNAME = "ExpansionTester"

def wait_for_server():
    print("Waiting for server...")
    for i in range(10):
        try:
            requests.get(BASE_URL)
            return True
        except:
            time.sleep(1)
    return False

def test_word(word, expected_severity):
    print(f"Testing word: '{word}' (Expected: {expected_severity})")
    try:
        r = requests.post(f"{BASE_URL}/analyze", json={'message': f"You are a {word}", 'username': USERNAME})
        data = r.json()
        
        actual_severity = data.get('severity')
        warning = data.get('warning_text', '')
        
        if actual_severity == expected_severity:
            print(f"  PASS: Detected as {actual_severity}")
            return True
        else:
            print(f"  FAIL: Expected {expected_severity}, got {actual_severity}. Warning: {warning}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

if __name__ == "__main__":
    if not wait_for_server():
        print("Server not running")
        sys.exit(1)

    print("\n--- Verifying Expanded Toxic Word List ---\n")
    
    # Test new Medium words
    test_word("clown", "Medium")
    test_word("weirdo", "Medium")
    test_word("scrub", "Medium")

    # Test new High words
    test_word("terrorist", "High")
    test_word("scam", "High")
    test_word("f**k", "High") # Obfuscated
    test_word("n*gga", "High") # Obfuscated

    print("\nDone.")
