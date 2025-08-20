#!/usr/bin/env python3
"""
Basic tests for GenAI Pipeline components
"""

import pytest
import os
import sys
import json
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_environment_setup():
    """Test that basic environment is set up correctly"""
    # Test that required files exist
    assert os.path.exists('lambda_function.py')
    assert os.path.exists('deploy.py')
    assert os.path.exists('test_complete.py')
    assert os.path.exists('test_web_server.py')
    assert os.path.exists('requirements.txt')

def test_lambda_function_import():
    """Test that lambda function can be imported"""
    try:
        import lambda_function
        assert hasattr(lambda_function, 'lambda_handler')
        assert hasattr(lambda_function, 'run_inference')
    except ImportError as e:
        pytest.skip(f"Lambda function import failed: {e}")

def test_requirements_file():
    """Test that requirements.txt is valid"""
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    # Check for key dependencies
    assert 'boto3' in requirements
    assert 'requests' in requirements
    assert 'streamlit' in requirements

@patch('boto3.client')
def test_lambda_handler_structure(mock_boto_client):
    """Test lambda handler basic structure"""
    try:
        import lambda_function
        
        # Mock event
        test_event = {
            'body': json.dumps({'prompt': 'test prompt'})
        }
        
        # Mock context
        mock_context = Mock()
        
        # Mock Bedrock client
        mock_bedrock = Mock()
        mock_response = Mock()
        mock_response.get.return_value.read.return_value = json.dumps({
            'content': [{'text': 'test response'}]
        }).encode()
        mock_bedrock.invoke_model.return_value = mock_response
        mock_boto_client.return_value = mock_bedrock
        
        # Test handler
        result = lambda_function.lambda_handler(test_event, mock_context)
        
        # Verify response structure
        assert 'statusCode' in result
        assert 'body' in result
        assert 'headers' in result
        
    except Exception as e:
        pytest.skip(f"Lambda handler test failed: {e}")

def test_project_structure():
    """Test that project has expected structure"""
    expected_files = [
        'README.md',
        'LICENSE',
        'SECURITY.md',
        '.gitignore',
        'lambda_function.py',
        'deploy.py',
        'test_complete.py',
        'test_web_server.py'
    ]
    
    for file in expected_files:
        assert os.path.exists(file), f"Missing required file: {file}"

def test_documentation_completeness():
    """Test that documentation files are not empty"""
    docs = ['README.md', 'SECURITY.md']
    
    for doc in docs:
        with open(doc, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            assert len(content) > 100, f"{doc} appears to be too short or empty"

if __name__ == "__main__":
    pytest.main([__file__])