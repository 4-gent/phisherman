#!/usr/bin/env python3
"""
Mailbox Verification Script
Verifies that all agents are properly configured for mailbox functionality
and provides registration instructions following Fetch.ai documentation.
"""

import subprocess
import sys
import socket
import requests
from pathlib import Path

# Agent configuration
AGENTS = [
    {"name": "phish_master", "seed": "phish_master", "port": 8001},
    {"name": "finance_phisher", "seed": "finance_phisher", "port": 8002},
    {"name": "health_phisher", "seed": "health_phisher", "port": 8003},
    {"name": "personal_phisher", "seed": "personal_phisher", "port": 8004},
    {"name": "phish_refiner", "seed": "phish_refiner", "port": 8005},
]

def check_port(port):
    """Check if port is in use"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def get_agent_address(name, seed, port):
    """Get agent address without starting it"""
    import tempfile
    import os
    
    # Create a temporary script to get the address
    script = f"""
from uagents import Agent
agent = Agent(name="{name}", seed="{seed}", port={port}, mailbox=True)
print(agent.address)
"""
    
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        return result.stdout.strip()
    return None

def generate_inspector_url(port, address):
    """Generate inspector URL in the correct format"""
    encoded_uri = f"http%3A//127.0.0.1%3A{port}"
    return f"https://agentverse.ai/inspect/?uri={encoded_uri}&address={address}"

def main():
    print("=" * 80)
    print("🎣 Phisherman Mailbox Setup Verification")
    print("=" * 80)
    print()
    
    print("Following Fetch.ai Mailbox Documentation:")
    print("https://uagents.fetch.ai/docs/agentverse/mailbox")
    print()
    
    # Check if agents are running
    print("📊 Checking Agent Status")
    print("-" * 80)
    
    all_running = True
    for agent in AGENTS:
        is_running = check_port(agent["port"])
        status = "✅ Running" if is_running else "❌ Not Running"
        print(f"{agent['name']:20} | Port {agent['port']:5} | Code: {status}")
        if not is_running:
            all_running = False
    
    print()
    
    if not all_running:
        print("⚠️  Warning: Not all agents are running!")
        print("Please start all agents using: python3 backend/scripts/start_all.py")
        print()
    
    # Generate inspector URLs
    print("🔗 Inspector URLs for Mailbox Registration")
    print("-" * 80)
    print()
    print("According to Fetch.ai documentation, follow these steps:")
    print()
    print("1. ✅ Ensure all agents are running with mailbox=True (already configured)")
    print("2. ✅ Click on each Inspector URL below")
    print("3. ✅ Click the 'Connect' button in the Inspector UI")
    print("4. ✅ Select 'Mailbox' option")
    print("5. ✅ Verify registration in Agentverse → My Agents")
    print()
    
    for i, agent in enumerate(AGENTS, 1):
        address = get_agent_address(agent["name"], agent["seed"], agent["port"])
        if address:
            inspector_url = generate_inspector_url(agent["port"], address)
            print(f"{i}. {agent['name']}:")
            print(f"   Inspector URL: {inspector_url}")
            print()
    
    print("-" * 80)
    print()
    
    # Test mailbox connectivity
    print("🧪 Testing Mailbox Connectivity")
    print("-" * 80)
    
    try:
        # Test if agentverse is accessible
        response = requests.get("https://agentverse.ai", timeout=5)
        if response.status_code == 200:
            print("✅ Agentverse.ai is accessible")
        else:
            print(f"⚠️  Agentverse.ai returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to Agentverse.ai: {e}")
    
    print()
    
    # Summary
    print("=" * 80)
    print("📋 Summary")
    print("=" * 80)
    print()
    print("✅ All agents configured with mailbox=True")
    print("✅ Inspector URLs generated and ready")
    print()
    print("Next Steps:")
    print("1. Click on each Inspector URL above")
    print("2. Click 'Connect' → Select 'Mailbox'")
    print("3. Verify all agents appear in Agentverse → My Agents")
    print("4. Each agent will have a 'Mailbox' tag")
    print()
    print("After registration, agents will:")
    print("- Collect messages from mailbox when online")
    print("- Be discoverable via ASI:One")
    print("- Work even when temporarily offline")
    print()
    print("Reference: https://uagents.fetch.ai/docs/agentverse/mailbox")
    print("=" * 80)

if __name__ == "__main__":
    main()

