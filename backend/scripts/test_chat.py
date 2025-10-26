#!/usr/bin/env python3
"""
Interactive Chat Test for Phisherman Agents
Test agents directly in the terminal with chat messages
"""

import requests
import json
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any

# Agent configuration
AGENTS = {
    "phish_master": {"port": 8001, "name": "Phish Master"},
    "finance_phisher": {"port": 8002, "name": "Finance Phisher"},
    "health_phisher": {"port": 8003, "name": "Health Phisher"},
    "personal_phisher": {"port": 8004, "name": "Personal Phisher"},
    "phish_refiner": {"port": 8005, "name": "Phish Refiner"},
}

def check_agent_running(port: int) -> bool:
    """Check if agent is running on the port"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def send_message_to_agent(agent_name: str, message: str) -> str:
    """Send a message to an agent and get response"""
    agent = AGENTS.get(agent_name)
    if not agent:
        return f"❌ Agent '{agent_name}' not found"
    
    if not check_agent_running(agent["port"]):
        return f"❌ Agent is not running on port {agent['port']}"
    
    # Note: Since agents use uAgent protocol, we can't directly HTTP POST
    # This is a placeholder for demonstration
    return f"✅ Message sent to {agent['name']}: '{message}' (Note: Requires uAgent Inspector for actual chat)"

def main():
    """Main interactive chat loop"""
    print("=" * 70)
    print("💬 Phisherman Agent Chat Tester")
    print("=" * 70)
    print()
    
    # Check which agents are running
    print("Checking agent status...")
    print()
    
    running_agents = []
    for agent_name, config in AGENTS.items():
        is_running = check_agent_running(config["port"])
        status = "✅ Running" if is_running else "❌ Not Running"
        print(f"  {config['name']} ({agent_name}): {status}")
        if is_running:
            running_agents.append(agent_name)
    
    print()
    
    if not running_agents:
        print("⚠️  No agents are running!")
        print()
        print("To start agents, run:")
        print("  python3 backend/scripts/start_all.py")
        print()
        return
    
    print("=" * 70)
    print("📝 Agent Testing Instructions")
    print("=" * 70)
    print()
    print("Available agents:")
    for agent_name in running_agents:
        print(f"  • {AGENTS[agent_name]['name']}")
    print()
    print("Since these agents use the uAgent Chat Protocol, you need to test them")
    print("using the Inspector UI. Here's how:")
    print()
    print("1. Make sure agents are running (check output above)")
    print("2. Start Inspector for each agent from Agentverse dashboard")
    print("3. Use Inspector UI to send chat messages")
    print()
    print("Example test messages:")
    print("  • 'generate finance template' (for phish_master)")
    print("  • 'banking phishing' (for finance_phisher)")
    print("  • 'medical appointment' (for health_phisher)")
    print("  • 'social media account' (for personal_phisher)")
    print("  • 'improve realism' (for phish_refiner)")
    print()
    print("=" * 70)
    print("📊 Quick Agent Commands Reference")
    print("=" * 70)
    print()
    print("Phish Master:")
    print("  • 'finance' → Coordinate with Finance Phisher")
    print("  • 'health' → Coordinate with Health Phisher")
    print("  • 'personal' → Coordinate with Personal Phisher")
    print("  • 'refine' → Send to Phish Refiner")
    print()
    print("Finance Phisher:")
    print("  • 'bank' → Banking phishing template")
    print("  • 'payment' → Payment verification template")
    print("  • 'invoice' → Invoice/billing template")
    print()
    print("Health Phisher:")
    print("  • 'appointment' → Medical appointment template")
    print("  • 'insurance' → Health insurance template")
    print("  • 'pharmaceutical' → Drug safety template")
    print()
    print("Personal Phisher:")
    print("  • 'social media' → Social media phishing")
    print("  • 'email account' → Email account phishing")
    print("  • 'password reset' → Password reset phishing")
    print()
    print("Phish Refiner:")
    print("  • 'realism' → Enhance realism")
    print("  • 'tone' → Refine language/tone")
    print("  • 'urgency' → Optimize urgency")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()

