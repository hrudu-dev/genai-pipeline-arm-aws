#!/usr/bin/env python3
"""Local test script for GenAI Pipeline"""

import os
import sys
sys.path.append('src')

# Load environment variables
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

from inference import run_inference

def test_inference():
    """Test inference function locally"""
    test_data = {'prompt': 'What is artificial intelligence?'}
    
    print("🧪 Testing GenAI Pipeline locally...")
    print(f"Input: {test_data}")
    
    result = run_inference(test_data)
    print(f"Result: {result}")
    
    if result.get('inference_complete'):
        print("✅ Inference successful!")
    else:
        print(f"⚠️  Inference failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_inference()