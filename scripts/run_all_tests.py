#!/usr/bin/env python3
"""
Fast Test Runner - Execute all performance tests quickly
"""

import asyncio
import subprocess
import time
import sys
from pathlib import Path

API_URL = "https://w7pifyp624nwwvrcjomh47ynsy0shwce.lambda-url.us-east-1.on.aws/"

async def run_quick_test():
    """Run quick performance test"""
    print("🚀 Running Quick Test...")
    exec(open('scripts/quick_test.py').read())

def run_performance_test():
    """Run full performance test"""
    print("\n📊 Running Performance Test...")
    cmd = [
        sys.executable, 'scripts/performance_test.py',
        '--url', API_URL,
        '--users', '15',
        '--requests', '50'
    ]
    subprocess.run(cmd)

def run_stress_test():
    """Run stress test"""
    print("\n🔥 Running Stress Test...")
    cmd = [
        sys.executable, 'scripts/stress_test.py',
        '--url', API_URL,
        '--max-users', '25',
        '--ramp-duration', '60',
        '--test-duration', '120'
    ]
    subprocess.run(cmd)

async def main():
    """Run all tests in sequence"""
    print("⚡ GenAI Pipeline - Fast Test Suite")
    print("=" * 50)
    
    start_time = time.time()
    
    # Quick test first
    await run_quick_test()
    
    # Performance test
    run_performance_test()
    
    # Stress test
    run_stress_test()
    
    total_time = time.time() - start_time
    print(f"\n✅ All tests completed in {total_time:.1f}s")

if __name__ == "__main__":
    asyncio.run(main())