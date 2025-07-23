"""
Cached inference module for GenAI Pipeline
"""

import json
import os
import boto3
import hashlib
import time
from datetime import datetime, timedelta

# Cache TTL in seconds (default: 1 hour)
CACHE_TTL = int(os.environ.get('CACHE_TTL', 3600))

def get_cache_key(prompt):
    """Generate a cache key for a prompt"""
    # Create a hash of the prompt to use as the cache key
    return hashlib.md5(prompt.encode('utf-8')).hexdigest()

def get_from_cache(cache_key):
    """Get a cached response from DynamoDB"""
    try:
        # Create DynamoDB client
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('CACHE_TABLE_NAME', 'GenAIPipelineCache'))
        
        # Get item from cache
        response = table.get_item(Key={'cache_key': cache_key})
        
        # Check if item exists and is not expired
        if 'Item' in response:
            item = response['Item']
            expiration_time = datetime.fromisoformat(item['expiration_time'])
            
            if expiration_time > datetime.now():
                print(f"Cache hit for key: {cache_key}")
                return item['response']
        
        print(f"Cache miss for key: {cache_key}")
        return None
    except Exception as e:
        print(f"Error getting from cache: {str(e)}")
        return None

def save_to_cache(cache_key, response):
    """Save a response to DynamoDB cache"""
    try:
        # Create DynamoDB client
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('CACHE_TABLE_NAME', 'GenAIPipelineCache'))
        
        # Calculate expiration time
        expiration_time = (datetime.now() + timedelta(seconds=CACHE_TTL)).isoformat()
        
        # Save item to cache
        table.put_item(Item={
            'cache_key': cache_key,
            'response': response,
            'expiration_time': expiration_time,
            'created_at': datetime.now().isoformat()
        })
        
        print(f"Saved to cache: {cache_key}")
        return True
    except Exception as e:
        print(f"Error saving to cache: {str(e)}")
        return False

def run_cached_inference(data, inference_function):
    """Run inference with caching"""
    prompt = data.get('prompt', '')
    
    # Check if caching is enabled
    if os.environ.get('ENABLE_CACHE', 'true').lower() == 'true':
        # Generate cache key
        cache_key = get_cache_key(prompt)
        
        # Try to get from cache
        cached_response = get_from_cache(cache_key)
        if cached_response:
            return cached_response
    
    # Run inference
    response = inference_function(data)
    
    # Save to cache if successful
    if response.get('inference_complete') and os.environ.get('ENABLE_CACHE', 'true').lower() == 'true':
        save_to_cache(get_cache_key(prompt), response)
    
    return response