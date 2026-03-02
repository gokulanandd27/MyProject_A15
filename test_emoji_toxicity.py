from toxicity_model import ToxicityDetector

def test_emojis():
    detector = ToxicityDetector()
    
    test_cases = [
        ("This is disgusting 🤮", "Medium"),
        ("You resemble a 🤡", "Medium"),
        ("I hate you 🖕", "High"),
        ("🖕🏻", "High"),
        ("Just a normal message", "non-toxic"),
        ("Mixed emojis 🤮 and 🖕", "High"), # High should take precedence if checked first
        ("💩", "Medium")
    ]
    
    print("Testing Toxic Emoji Detection...")
    for text, expected_severity in test_cases:
        result = detector.predict(text)
        status = result.get('message_type')
        severity = result.get('severity', 'None')
        
        print(f"Text: '{text}'")
        print(f"  Expected: {expected_severity}")
        print(f"  Got: {status} ({severity})")
        
        if expected_severity == "non-toxic":
             if status == "non-toxic":
                 print("  [PASS]")
             else:
                 print("  [FAIL]")
        else:
            if status == "toxic" and severity == expected_severity:
                print("  [PASS]")
            else:
                print("  [FAIL]")
        print("-" * 20)

if __name__ == "__main__":
    test_emojis()
