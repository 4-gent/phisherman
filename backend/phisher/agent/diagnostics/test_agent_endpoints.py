#!/usr/bin/env python3
"""
Test Agent Endpoints and Save Results
Tests each agent's endpoint and saves raw HTTP request/response
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any
import sys
import os

# Agent configuration
AGENTS = {
    "phish_master": {"port": 8001, "name": "Phish Master"},
    "finance_phisher": {"port": 8002, "name": "Finance Phisher"},
    "health_phisher": {"port": 8003, "name": "Health Phisher"},
    "personal_phisher": {"port": 8004, "name": "Personal Phisher"},
    "phish_refiner": {"port": 8005, "name": "Phish Refiner"},
}

def check_port_available(port: int) -> bool:
    """Check if port is in use"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def test_agent_endpoint(agent_name: str, port: int) -> Dict[str, Any]:
    """Test an agent endpoint and return results"""
    results = {
        "agent": agent_name,
        "port": port,
        "timestamp": datetime.now().isoformat(),
        "reachable": False,
        "http_status": None,
        "error": None,
        "response_body": None,
        "endpoint_tested": None
    }
    
    base_url = f"http://127.0.0.1:{port}"
    
    # Test if port is listening
    if not check_port_available(port):
        results["error"] = "Port not listening - agent may not be running"
        return results
    
    # Try common uAgent endpoints
    endpoints_to_try = [
        "/submit",
        "/chat",
        "/message",
        "/",
    ]
    
    # Test payload - simple chat message
    test_payload = {
        "message": "smoke test: hello",
        "content": [{"type": "text", "text": "smoke test: hello"}]
    }
    
    for endpoint in endpoints_to_try:
        try:
            url = f"{base_url}{endpoint}"
            results["endpoint_tested"] = url
            
            # Try POST first
            response = requests.post(
                url,
                json=test_payload,
                timeout=5,
                headers={"Content-Type": "application/json"}
            )
            
            results["reachable"] = True
            results["http_status"] = response.status_code
            
            try:
                results["response_body"] = response.json()
            except:
                results["response_body"] = response.text[:500]  # Limit text
            
            # If successful, stop trying endpoints
            if response.status_code < 500:
                break
                
        except requests.exceptions.ConnectionError:
            results["error"] = "Connection refused"
            continue
        except requests.exceptions.Timeout:
            results["error"] = "Request timeout"
            continue
        except Exception as e:
            results["error"] = str(e)
            continue
    
    return results

def save_test_results(agent_name: str, results: Dict[str, Any]):
    """Save test results to file"""
    output_dir = "diagnostics/agent_tests"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{output_dir}/{agent_name}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Agent Endpoint Test Results\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"Agent: {results['agent']}\n")
        f.write(f"Port: {results['port']}\n")
        f.write(f"Timestamp: {results['timestamp']}\n")
        f.write(f"Endpoint Tested: {results['endpoint_tested']}\n")
        f.write(f"Reachable: {results['reachable']}\n")
        f.write(f"HTTP Status: {results['http_status']}\n")
        f.write(f"Error: {results['error']}\n\n")
        
        f.write(f"Request Details:\n")
        f.write(f"{'-'*60}\n")
        f.write(f"Method: POST\n")
        f.write(f"URL: {results['endpoint_tested']}\n")
        f.write(f"Payload: {json.dumps({'message': 'smoke test: hello'}, indent=2)}\n\n")
        
        f.write(f"Response:\n")
        f.write(f"{'-'*60}\n")
        if results['response_body']:
            f.write(f"{json.dumps(results['response_body'], indent=2)}\n")
        else:
            f.write("No response body\n")
    
    print(f"✅ Saved results to {filename}")

def main():
    """Main function"""
    print("🧪 Testing Agent Endpoints")
    print("="*60)
    
    all_results = []
    
    for agent_name, config in AGENTS.items():
        print(f"\nTesting {agent_name} on port {config['port']}...")
        results = test_agent_endpoint(agent_name, config['port'])
        all_results.append(results)
        
        # Print summary
        if results['reachable']:
            print(f"  ✅ Reachable - Status: {results['http_status']}")
        else:
            print(f"  ❌ Not reachable - {results['error']}")
        
        # Save results
        save_test_results(agent_name, results)
    
    # Print summary table
    print("\n" + "="*60)
    print("SUMMARY TABLE")
    print("="*60)
    print(f"{'Agent':<20} {'Endpoint':<40} {'Reachable':<12} {'Status':<10} {'Notes'}")
    print("-"*60)
    
    for result in all_results:
        reachable = "✅ Yes" if result['reachable'] else "❌ No"
        status = str(result['http_status']) if result['http_status'] else "N/A"
        endpoint = result['endpoint_tested'] or "N/A"
        notes = result['error'] or "OK"
        
        print(f"{result['agent']:<20} {endpoint:<40} {reachable:<12} {status:<10} {notes}")

if __name__ == "__main__":
    main()

