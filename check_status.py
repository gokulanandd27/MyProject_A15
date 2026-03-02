from toxicity_model import ToxicityDetector
import time

print("Starting model load test...")
start = time.time()
try:
    detector = ToxicityDetector()
    print("Model loaded successfully!")
    print(f"Time taken: {time.time() - start:.2f}s")
    
    # Test prediction
    print("Testing prediction...")
    res = detector.predict("test message")
    print(f"Result: {res}")
    
except Exception as e:
    print(f"Runtime Error: {e}")
