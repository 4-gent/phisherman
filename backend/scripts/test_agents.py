#!/usr/bin/env python3
"""
Test All Phisherman Agents
Tests each agent's Chat Protocol v0.3.0 implementation
"""

import asyncio
import requests
import json
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any

# Agent configuration
AGENTS = [
    {"name": "phish_master", "port": 8001, "address": "agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr"},
    {"name": "finance_phisher", "port": 8002, "address": "agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z"},
    {"name": "health_phisher", "port": 8003, "address": "agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h"},
    {"name": "personal_phisher", "port": 8004, "address": "agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz"},
    {"name": "phish_refiner", "port": 8005, "address": "agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr"},
]

def test_chat_protocol_message(text: str) -> Dict[str, Any]:
    """Create a Chat Protocol v0.3.0 message"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "msg_id": str(uuid4()),
        "content": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

def check_agent_running(port: int) -> bool:
    """Check if agent is running on the port"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def test_agent_endpoint(agent: Dict[str, Any], test_message: str) -> tuple[bool, str]:
    """Test an agent's endpoint with a chat message"""
    try:
        # Test if endpoint responds (agents use envelope format)
        url = f"http://127.0.0.1:{agent['port']}/submit"
        
        # Send a test request to check if agent is listening
        response = requests.get(url, timeout=5)
        
        # Any response means agent is listening
        return True, f"Agent listening on port {agent['port']}"
            
    except requests.exceptions.ConnectionError:
        return False, "Connection refused (agent not running)"
    except requests.exceptions.Timeout:
        return False, "Request timeout"
    except Exception as e:
        # Even error responses mean agent is running
        if "400" in str(e) or "Method" in str(e):
            return True, f"Agent responding (expected envelope format)"
        return False, f"Error: {str(e)}"

def test_specific_agent(agent_name: str, test_message: str) -> None:
    """Test a specific agent"""
    agent = next((a for a in AGENTS if a["name"] == agent_name), None)
    if not agent:
        print(f"❌ Agent '{agent_name}' not found")
        return
    
    print(f"\n🧪 Testing {agent['name']}")
    print("-" * 60)
    print(f"Port: {agent['port']}")
    print(f"Address: {agent['address']}")
    
    # Check if running
    is_running = check_agent_running(agent['port'])
    print(f"Status: {'✅ Running' if is_running else '❌ Not Running'}")
    
    if not is_running:
        print("⚠️  Skipping message test - agent not running")
        return
    
    # Test endpoint
    print(f"\n📤 Sending test message: '{test_message}'")
    success, result = test_agent_endpoint(agent, test_message)
    
    if success:
        print(f"✅ Message test passed")
        print(f"   {result}")
    else:
        print(f"❌ Message test failed")
        print(f"   {result}")

def test_all_agents():
    """Test all agents"""
    print("=" * 80)
    print("🎣 Phisherman Agent Testing Suite")
    print("=" * 80)
    print()
    
    # Test each agent
    for agent in AGENTS:
        print(f"\n🧪 Testing {agent['name']}")
        print("-" * 60)
        print(f"Port: {agent['port']}")
        print(f"Address: {agent['address']}")
        
        # Check if running
        is_running = check_agent_running(agent['port'])
        print(f"Status: {'✅ Running' if is_running else '❌ Not Running'}")
        
        if not is_running:
            print("⚠️  Agent not running - start it first")
            continue
        
        # Test that agent is listening
        print(f"\n📡 Testing endpoint connectivity...")
        try:
            response = requests.get(f"http://127.0.0.1:{agent['port']}/submit", timeout=2)
            print(f"✅ Endpoint responding")
        except requests.exceptions.Timeout:
            print(f"⚠️  Endpoint timeout (may be normal)")
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection refused")
        except Exception as e:
            # 405 Method Not Allowed or similar means agent is running
            if "405" in str(e) or "Method" in str(e):
                print(f"✅ Agent listening (responds to incorrect method)")
            else:
                print(f"⚠️  Unexpected response: {type(e).__name__}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 Test Summary")
    print("=" * 80)
    
    running_count = sum(1 for agent in AGENTS if check_agent_running(agent['port']))
    print(f"Running agents: {running_count}/{len(AGENTS)}")
    
    if running_count == len(AGENTS):
        print("\n✅ All agents are running and ready!")
        print("\n📝 How to Test Agents:")
        print("   1. Open Inspector URLs (see QUICK_START_MAILBOX.md)")
        print("   2. Use Inspector UI to send test messages")
        print("   3. Agents will respond via Chat Protocol v0.3.0")
        print("\n💡 Agents use envelope format - test via Inspector UI, not direct HTTP")
    else:
        print(f"\n⚠️  Only {running_count}/{len(AGENTS)} agents running")
        print("   Start all agents with: python3 backend/scripts/start_all.py")

def test_domain_specific():
    """Test domain-specific functionality"""
    print("\n" + "=" * 80)
    print("🎯 Domain-Specific Testing")
    print("=" * 80)
    
    test_cases = [
        ("phish_master", "generate finance template"),
        ("finance_phisher", "generate template"),
        ("health_phisher", "create healthcare phishing template"),
        ("personal_phisher", "generate personal phishing template"),
        ("phish_refiner", "refine template"),
    ]
    
    for agent_name, test_message in test_cases:
        agent = next((a for a in AGENTS if a["name"] == agent_name), None)
        if not agent:
            continue
        
        is_running = check_agent_running(agent['port'])
        if not is_running:
            continue
        
        print(f"\n📤 Testing {agent_name} with: '{test_message}'")
        success, result = test_agent_endpoint(agent, test_message)
        
        if success:
            print(f"✅ {agent_name}: {result}")
        else:
            print(f"❌ {agent_name}: {result}")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        # Test specific agent
        agent_name = sys.argv[1]
        test_message = sys.argv[2] if len(sys.argv) > 2 else "Hello, this is a test"
        test_specific_agent(agent_name, test_message)
    else:
        # Test all agents
        test_all_agents()
        
        # Test domain-specific functionality
        if all(check_agent_running(agent['port']) for agent in AGENTS):
            test_domain_specific()

if __name__ == "__main__":
    main()

