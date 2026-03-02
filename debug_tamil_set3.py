from toxicity_model import ToxicityDetector
import re

detector = ToxicityDetector()
keywords_to_check = ["லூசு புண்டா", "தேவிடியா சுன்னி"]

print("Checking keywords in High Severity List...")
for k in keywords_to_check:
    if k in detector.high_severity_keywords:
        print(f"YES: '{k}' is in the list.")
    else:
        print(f"NO: '{k}' is NOT in the list.")

print("-" * 20)
print("Testing Regex Matching...")

for k in keywords_to_check:
    # Mimic the logic in toxicity_model.py
    found = False
    for word in detector.high_severity_keywords:
        # We only care about the specific word for this debug
        if word == k:
            pattern = re.compile(r'\b' + re.escape(word) + r'\b')
            if pattern.search(k.lower()):
                 print(f"MATCH: '{word}' found in '{k}'")
                 found = True
            else:
                 print(f"FAIL: '{word}' regex did NOT match '{k}'")
    if not found:
        print(f"ERROR: Could not find match for '{k}' even with itself.")
