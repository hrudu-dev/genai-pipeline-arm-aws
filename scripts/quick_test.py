#!/usr/bin/env python3
"""
Quick Performance Test - Ultra-fast API testing
"""

import asyncio
import aiohttp
import time
import json
from datetime import datetime

API_URL = "https://w7pifyp624nwwvrcjomh47ynsy0shwce.lambda-url.us-east-1.on.aws/"

async def quick_test(concurrent=20, total=100):
    """Ultra-fast performance test"""
    print(f"⚡ Quick Test: {concurrent} concurrent, {total} total requests")
    
    connector = aiohttp.TCPConnector(
        limit=concurrent * 2,
        keepalive_timeout=30,
        enable_cleanup_closed=True
    )
    
    async with aiohttp.ClientSession(connector=connector) as session:
        start_time = time.time()
        
        # Simple prompts for speed
        prompts = ["Hi", "Test", "Quick", "Fast", "Speed"]
        
        tasks = []
        for i in range(total):
            prompt = prompts[i % len(prompts)]
            task = make_request(session, prompt)
            tasks.append(task)
        
        # Execute with concurrency limit
        semaphore = asyncio.Semaphore(concurrent)
        
        async def bounded_request(task):
            async with semaphore:
                return await task
        
        results = await asyncio.gather(*[bounded_request(task) for task in tasks])
        total_time = time.time() - start_time
        
        # Quick analysis
        successful = sum(1 for r in results if r['success'])
        response_times = [r['time'] for r in results if r['success']]
        
        print(f"✅ Results: {successful}/{total} success ({successful/total*100:.1f}%)")
        print(f"⚡ Speed: {total/total_time:.1f} req/s")
        if response_times:
            print(f"⏱️  Avg time: {sum(response_times)/len(response_times):.3f}s")

async def make_request(session, prompt):
    """Make single request"""
    start = time.time()
    try:
        async with session.post(
            API_URL,
            json={"prompt": prompt},
            timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            elapsed = time.time() - start
            
            if response.status == 200:
                data = await response.json()
                return {
                    'success': data.get('inference_complete', False),
                    'time': elapsed
                }
            else:
                return {'success': False, 'time': elapsed}
                
    except Exception:
        return {'success': False, 'time': time.time() - start}

if __name__ == "__main__":
    asyncio.run(quick_test())