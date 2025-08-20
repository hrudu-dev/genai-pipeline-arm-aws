#!/usr/bin/env python3
"""
GenAI Pipeline - Web Test Server
Easy-to-use Streamlit web interface for testing the GenAI Pipeline
"""

import streamlit as st
import requests
import time
import json
from datetime import datetime

# Configuration
API_URL = "https://w7pifyp624nwwvrcjomh47ynsy0shwce.lambda-url.us-east-1.on.aws/"

# Test cases
TESTS = [
    {"name": "Basic AI Query", "prompt": "What is artificial intelligence?"},
    {"name": "Code Generation", "prompt": "Write a Python hello world program"},
    {"name": "Technical Explanation", "prompt": "Explain quantum computing in simple terms"},
    {"name": "Creative Writing", "prompt": "Create a haiku about clouds"},
    {"name": "ARM64 Knowledge", "prompt": "What are the benefits of ARM64 processors?"}
]

def call_api(prompt):
    """Call the GenAI API"""
    start_time = time.time()
    
    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json={"prompt": prompt},
            timeout=30
        )
        
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if data.get('inference_complete'):
                return {
                    'success': True,
                    'time': response_time,
                    'result': data['result']
                }
            else:
                return {
                    'success': False,
                    'time': response_time,
                    'error': data.get('error', 'Unknown error')
                }
        else:
            return {
                'success': False,
                'time': response_time,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
            
    except Exception as e:
        response_time = time.time() - start_time
        return {
            'success': False,
            'time': response_time,
            'error': str(e)
        }

def main():
    """Main web interface"""
    st.set_page_config(
        page_title="GenAI Pipeline Test Suite",
        page_icon="🧪",
        layout="wide"
    )
    
    # Header
    st.title("🧪 GenAI Pipeline - Complete Test Suite")
    st.markdown("**ARM64 Optimized AI Testing** • 40% Cost Savings • 20% Faster")
    
    # Sidebar with metrics
    with st.sidebar:
        st.header("📊 Test Metrics")
        
        if 'test_results' not in st.session_state:
            st.session_state.test_results = []
        
        total_tests = len(TESTS)
        completed = len(st.session_state.test_results)
        successful = sum(1 for r in st.session_state.test_results if r['success'])
        success_rate = (successful / completed * 100) if completed > 0 else 0
        avg_time = (sum(r['time'] for r in st.session_state.test_results) / completed) if completed > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Tests", total_tests)
            st.metric("Success Rate", f"{success_rate:.1f}%")
        with col2:
            st.metric("Completed", completed)
            st.metric("Avg Time", f"{avg_time:.2f}s")
        
        # ARM64 Benefits
        st.markdown("---")
        st.markdown("### 🚀 ARM64 Benefits")
        st.markdown("""
        - 40% cost savings vs x86
        - 20% performance improvement  
        - 25% faster cold starts
        - Better energy efficiency
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.header("🎮 Controls")
        
        if st.button("🚀 Run Complete Test Suite", type="primary", use_container_width=True):
            st.session_state.test_results = []
            run_complete_test()
        
        if st.button("🧪 Run Single Test", use_container_width=True):
            run_single_test()
        
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.test_results = []
            st.rerun()
    
    with col1:
        st.header("📋 Test Results")
        
        if st.session_state.test_results:
            display_results()
        else:
            st.info("Click 'Run Complete Test Suite' to start testing")

def run_complete_test():
    """Run all tests"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, test in enumerate(TESTS):
        status_text.text(f"Running: {test['name']}")
        progress_bar.progress((i) / len(TESTS))
        
        result = call_api(test['prompt'])
        result['test_name'] = test['name']
        result['prompt'] = test['prompt']
        st.session_state.test_results.append(result)
        
        time.sleep(0.5)  # Brief pause between tests
    
    progress_bar.progress(1.0)
    status_text.text("✅ All tests completed!")
    
    # Final summary
    successful = sum(1 for r in st.session_state.test_results if r['success'])
    total = len(st.session_state.test_results)
    
    if successful == total:
        st.success(f"🎉 All tests passed! ({successful}/{total})")
    elif successful > total * 0.8:
        st.warning(f"⚠️ Most tests passed ({successful}/{total})")
    else:
        st.error(f"❌ Several tests failed ({successful}/{total})")
    
    # Trigger rerun to show final results
    st.rerun()

def run_single_test():
    """Run a single selected test"""
    test_choice = st.selectbox("Select a test:", [t['name'] for t in TESTS])
    selected_test = next(t for t in TESTS if t['name'] == test_choice)
    
    if st.button("Run Selected Test"):
        with st.spinner(f"Running {selected_test['name']}..."):
            result = call_api(selected_test['prompt'])
            result['test_name'] = selected_test['name']
            result['prompt'] = selected_test['prompt']
            
            if result['success']:
                st.success(f"✅ {selected_test['name']} - {result['time']:.2f}s")
                st.text_area("Response:", result['result'], height=200)
            else:
                st.error(f"❌ {selected_test['name']} - {result['error']}")

def display_results():
    """Display test results"""
    for i, result in enumerate(st.session_state.test_results):
        with st.expander(
            f"{'✅' if result['success'] else '❌'} {result['test_name']} - {result['time']:.2f}s",
            expanded=False
        ):
            st.write(f"**Prompt:** {result['prompt']}")
            
            if result['success']:
                st.success("Success!")
                # Use code block instead of text_area to avoid key conflicts
                st.code(result['result'], language=None)
            else:
                st.error(f"Error: {result['error']}")

if __name__ == "__main__":
    main()