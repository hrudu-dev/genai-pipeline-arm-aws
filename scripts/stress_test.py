#!/usr/bin/env python3
"""
Stress Testing Suite for GenAI Pipeline
Tests system limits and breaking points
"""

import asyncio
import aiohttp
import time
import json
import statistics
from datetime import datetime
from pathlib import Path
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class StressTestSuite:
    def __init__(self, api_url):
        self.api_url = api_url.rstrip('/')
        self.results = []
        
    async def ramp_up_test(self, max_users=50, ramp_duration=300, test_duration=600):
        """Gradually increase load to find breaking point"""
        print(f"🔥 Starting ramp-up stress test...")
        print(f"   Max users: {max_users}")
        print(f"   Ramp duration: {ramp_duration}s")
        print(f"   Test duration: {test_duration}s")
        print("-" * 60)
        
        start_time = time.time()
        current_users = 1
        user_increment = max_users / (ramp_duration / 10)  # Increase every 10 seconds
        
        connector = aiohttp.TCPConnector(limit=max_users * 2)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            active_tasks = set()
            
            while time.time() - start_time < test_duration:
                current_time = time.time() - start_time
                
                # Calculate target users based on ramp-up
                if current_time < ramp_duration:
                    target_users = int(1 + (current_time / ramp_duration) * (max_users - 1))
                else:
                    target_users = max_users
                
                # Adjust active tasks to match target users
                while len(active_tasks) < target_users:
                    task = asyncio.create_task(self.continuous_request(session))
                    active_tasks.add(task)
                
                # Remove completed tasks
                completed_tasks = [task for task in active_tasks if task.done()]
                for task in completed_tasks:
                    active_tasks.remove(task)
                    try:
                        result = await task
                        self.results.append(result)
                    except Exception as e:
                        self.results.append({
                            'success': False,
                            'error': str(e),
                            'timestamp': datetime.now().isoformat()
                        })
                
                # Print progress every 30 seconds
                if int(current_time) % 30 == 0:
                    success_rate = self.calculate_success_rate()
                    print(f"⏱️  {int(current_time)}s - Users: {len(active_tasks)}/{target_users} - Success: {success_rate:.1f}%")
                
                await asyncio.sleep(1)
            
            # Cancel remaining tasks
            for task in active_tasks:
                task.cancel()
            
            return time.time() - start_time
    
    async def continuous_request(self, session):
        """Make continuous requests until cancelled"""
        prompts = [
            "Quick test",
            "Fast response needed",
            "Speed test",
            "Performance check",
            "Rapid fire test"
        ]
        
        request_count = 0
        while True:
            try:
                prompt = prompts[request_count % len(prompts)]
                start_time = time.time()
                
                async with session.post(
                    self.api_url,
                    json={"prompt": prompt},
                    headers={"Content-Type": "application/json"}
                ) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'success': data.get('inference_complete', False),
                            'response_time': response_time,
                            'request_count': request_count + 1,
                            'timestamp': datetime.now().isoformat()
                        }
                    else:
                        return {
                            'success': False,
                            'response_time': response_time,
                            'error': f"HTTP {response.status}",
                            'timestamp': datetime.now().isoformat()
                        }
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
            
            request_count += 1
            await asyncio.sleep(0.1)  # Brief pause between requests
    
    def calculate_success_rate(self):
        """Calculate current success rate"""
        if not self.results:
            return 0.0
        
        successful = sum(1 for r in self.results if r.get('success', False))
        return (successful / len(self.results)) * 100
    
    def analyze_stress_results(self, total_time):
        """Analyze stress test results"""
        if not self.results:
            return None
        
        successful_results = [r for r in self.results if r.get('success', False)]
        response_times = [r['response_time'] for r in successful_results if 'response_time' in r]
        
        if not response_times:
            return {
                'total_requests': len(self.results),
                'successful_requests': 0,
                'success_rate': 0,
                'total_time': total_time
            }
        
        return {
            'total_requests': len(self.results),
            'successful_requests': len(successful_results),
            'success_rate': (len(successful_results) / len(self.results)) * 100,
            'total_time': total_time,
            'avg_response_time': statistics.mean(response_times),
            'max_response_time': max(response_times),
            'min_response_time': min(response_times),
            'requests_per_second': len(self.results) / total_time
        }

async def main():
    """Main stress testing function"""
    parser = argparse.ArgumentParser(description='GenAI Pipeline Stress Test')
    parser.add_argument('--url', required=True, help='API endpoint URL')
    parser.add_argument('--max-users', type=int, default=50, help='Maximum concurrent users')
    parser.add_argument('--ramp-duration', type=int, default=300, help='Ramp-up duration in seconds')
    parser.add_argument('--test-duration', type=int, default=600, help='Total test duration in seconds')
    
    args = parser.parse_args()
    
    print("🔥 GenAI Pipeline - Stress Test Suite")
    print("Finding System Breaking Points")
    print("=" * 60)
    
    test_suite = StressTestSuite(args.url)
    
    try:
        total_time = await test_suite.ramp_up_test(
            max_users=args.max_users,
            ramp_duration=args.ramp_duration,
            test_duration=args.test_duration
        )
        
        stats = test_suite.analyze_stress_results(total_time)
        
        if stats:
            print("\n" + "=" * 60)
            print("🔥 STRESS TEST RESULTS")
            print("=" * 60)
            print(f"Total Requests: {stats['total_requests']}")
            print(f"Successful: {stats['successful_requests']}")
            print(f"Success Rate: {stats['success_rate']:.1f}%")
            print(f"Requests/Second: {stats['requests_per_second']:.2f}")
            
            if 'avg_response_time' in stats:
                print(f"Avg Response Time: {stats['avg_response_time']:.3f}s")
                print(f"Max Response Time: {stats['max_response_time']:.3f}s")
        
    except KeyboardInterrupt:
        print("\n⚠️  Stress test interrupted")
    except Exception as e:
        print(f"\n❌ Stress test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())