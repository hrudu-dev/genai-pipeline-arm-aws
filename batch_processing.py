#!/usr/bin/env python3
"""
Batch processing for GenAI Pipeline
"""

import os
import json
import requests
import time
import concurrent.futures
import argparse
from pathlib import Path

# Hardcoded credentials - only for testing
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

# Lambda function URL
LAMBDA_URL = "https://cr7c7lxj5mt2lwvyi57s2o6arq0paars.lambda-url.us-east-1.on.aws/"

def process_prompt(prompt):
    """Process a single prompt using the Lambda function"""
    try:
        # Prepare request
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt
        }
        
        # Send request
        response = requests.post(LAMBDA_URL, headers=headers, json=data)
        
        # Parse response
        response_body = response.json()
        
        return {
            'prompt': prompt,
            'result': response_body.get('result', ''),
            'success': response_body.get('inference_complete', False)
        }
    except Exception as e:
        return {
            'prompt': prompt,
            'error': str(e),
            'success': False
        }

def process_batch(prompts, max_workers=5):
    """Process a batch of prompts in parallel"""
    results = []
    
    print(f"Processing {len(prompts)} prompts with {max_workers} workers...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_prompt = {executor.submit(process_prompt, prompt): prompt for prompt in prompts}
        
        for future in concurrent.futures.as_completed(future_to_prompt):
            prompt = future_to_prompt[future]
            try:
                result = future.result()
                results.append(result)
                
                if result['success']:
                    print(f"[SUCCESS] Processed: {prompt[:30]}...")
                else:
                    print(f"[FAILED] Failed: {prompt[:30]}... - {result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"[ERROR] Error processing {prompt[:30]}...: {str(e)}")
                results.append({
                    'prompt': prompt,
                    'error': str(e),
                    'success': False
                })
    
    return results

def process_file(file_path, output_path=None, max_workers=5):
    """Process prompts from a file"""
    # Read prompts from file
    with open(file_path, 'r') as f:
        prompts = [line.strip() for line in f if line.strip()]
    
    # Process prompts
    results = process_batch(prompts, max_workers)
    
    # Write results to file
    if output_path is None:
        output_path = f"{file_path}.results.json"
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results written to {output_path}")
    
    # Print summary
    successful = sum(1 for r in results if r['success'])
    print(f"Summary: {successful}/{len(results)} prompts processed successfully")
    
    return results

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Batch processing for GenAI Pipeline')
    parser.add_argument('file', help='File containing prompts (one per line)')
    parser.add_argument('--output', '-o', help='Output file for results (default: input_file.results.json)')
    parser.add_argument('--workers', '-w', type=int, default=5, help='Maximum number of concurrent workers')
    
    args = parser.parse_args()
    
    process_file(args.file, args.output, args.workers)

if __name__ == "__main__":
    main()