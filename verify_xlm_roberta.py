from toxicity_model import ToxicityDetector
import time

def test_phrase(detector, phrase, expected_type):
    print(f"\nTesting: '{phrase}'")
    start = time.time()
    try:
        result = detector.predict(phrase)
        elapsed = time.time() - start
        
        message_type = result['message_type']
        reason = result.get('reason', 'N/A')
        severity = result.get('severity', 'None')
        
        status = "PASSED" if message_type == expected_type else "FAILED"
        print(f"[{status}] Type: {message_type} | Sev: {severity} | Reason: {reason} | Time: {elapsed:.4f}s")
        return status == "PASSED"
    except Exception as e:
        print(f"[ERROR] Exception during prediction: {e}")
        return False

if __name__ == "__main__":
    print("Initializing ToxicityDetector (loading model)...")
    try:
        detector = ToxicityDetector()
        if detector.sentiment_analyzer is None:
            print("[WARNING] Model failed to load. Only keyword detection will work.")
        else:
            print("[SUCCESS] Model loaded successfully.")

        tests = [
            ("You are stupid", "toxic"), # High - Keyword
            ("Gomma", "toxic"), # High - Keyword

            ("You ruin everything you touch.", "toxic"), # Hope for Medium
            ("Stop talking, nobody cares.", "toxic"), # Hope for Medium

            ("I wish you would just go away forever.", "toxic"), # Hope for Low/Medium
            ("This is not good.", "non-toxic"), # Test phrase
            ("I dislike this video.", "toxic"), # Hope for Low
            ("This stream is terrible.", "toxic") # Hope for Low
        ]

        with open("verification_output.txt", "w", encoding="utf-8") as f:
            for phrase, expected in tests:
                print(f"Testing: '{phrase}'")
                try:
                    result = detector.predict(phrase)
                    message_type = result['message_type']
                    reason = result.get('reason', 'N/A')
                    severity = result.get('severity', 'None')
                    status = "PASSED" if message_type == expected else "FAILED"
                    
                    output_line = f"[{status}] Phrase: '{phrase}' | Type: {message_type} | Sev: {severity} | Reason: {reason}\n"
                    print(output_line.strip())
                    f.write(output_line)
                except Exception as e:
                    print(f"[ERROR] {e}")
                    f.write(f"[ERROR] {e}\n")
        
    except Exception as e:
        print(f"Critical Error: {e}")
