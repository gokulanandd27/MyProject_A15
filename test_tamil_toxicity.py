from toxicity_model import ToxicityDetector

def test_tamil():
    detector = ToxicityDetector()
    
    test_cases = [
        ("You are a muttal", "Medium"),
        ("He is a ayokkiyan", "High"),
        ("நீ ஒரு முட்டாள்", "Medium"),
        ("அவன் ஒரு மோசடி", "High"),
        ("Simple text", "non-toxic"),
        ("மடையன்", "Medium"),
        ("சோம்பேறி", "Medium"),
        ("மண்டைய போடு", "High"),
        ("porukki", "Medium"),
        ("தாயோலி", "High"),
        ("புண்டா", "High"),
        ("தேவிடியா சுன்னி", "High"),
        ("லூசு புண்டா", "High")
    ]
    
    print("Testing Tamil Toxicity Detection...")
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
    test_tamil()
