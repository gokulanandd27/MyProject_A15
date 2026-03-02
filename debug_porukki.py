from toxicity_model import ToxicityDetector
import re

detector = ToxicityDetector()
print("Checking if 'porukki' is in medium list...")
if "porukki" in detector.medium_severity_keywords:
    print("YES, 'porukki' is in the list.")
else:
    print("NO, 'porukki' is NOT in the list.")

print(f"List length: {len(detector.medium_severity_keywords)}")

text = "porukki"
found = False
for word in detector.medium_severity_keywords:
    if word == "porukki":
        pattern = re.compile(r'\b' + re.escape(word) + r'\b')
        if pattern.search(text):
            print(f"MATCHED: {word}")
            found = True
        else:
             print(f"REGEX FAILED for {word}")

if not found:
    print("No match found loop.")
