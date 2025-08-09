#!/usr/bin/env python3
"""
Simple test script for the SDLC API
Tests the AsyncWorkflowRunner integration
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing SDLC API with AsyncWorkflowRunner...")
    
    # Test health check
    print("\n1. Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Test workflow start
    print("\n2. Testing workflow start...")
    payload = {
        "requirements": "Build a simple calculator app with basic operations",
        "project_name": "SimpleCalculator"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/workflow/start", json=payload)
        print(f"Start workflow: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Session ID: {result['session_id']}")
            session_id = result["session_id"]
            
            # Test status check
            print("\n3. Testing status check...")
            time.sleep(2)  # Give workflow time to start
            
            status_response = requests.get(f"{BASE_URL}/workflow/{session_id}/status")
            print(f"Status check: {status_response.status_code}")
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"Status: {status['status']}")
                print(f"Stage: {status['current_stage']}")
                print(f"Progress: {status['progress']}")
                
                if status.get('pending_interrupt'):
                    print(f"Pending interrupt: {status['pending_interrupt']['type']}")
            else:
                print(f"Status error: {status_response.text}")
                
            # Test session list
            print("\n4. Testing session list...")
            sessions_response = requests.get(f"{BASE_URL}/workflow/sessions")
            print(f"Sessions: {sessions_response.status_code} - {len(sessions_response.json())} sessions")
            
        else:
            print(f"Start error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()