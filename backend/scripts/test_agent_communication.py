#!/usr/bin/env python3
"""
Test Agent Communication with Proper Envelope Format
Sends actual messages to agents using uagents protocol
"""

import asyncio
from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context
from uagents_core.contrib.protocols.chat import (
    ChatMessage, TextContent, StartSessionContent
)

# Agent addresses
AGENTS = {
    "phish_master": "agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr",
    "finance_phisher": "agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z",
    "health_phisher": "agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h",
    "personal_phisher": "agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz",
    "phish_refiner": "agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr",
}

# Test messages
TEST_MESSAGES = {
    "phish_master": "generate finance template",
    "finance_phisher": "create a payment verification template",
    "health_phisher": "generate medical records update template",
    "personal_phisher": "create account security verification template",
    "phish_refiner": "refine template to be more urgent",
}

# Create test client agent
test_client = Agent(name="test_client", seed="test_client_seed_12345")

def txt(s: str) -> ChatMessage:
    """Helper to create text message"""
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=str(uuid4()),
        content=[TextContent(type="text", text=s)]
    )

async def test_agent_send(agent_name: str, agent_address: str, test_message: str):
    """Test communication with a specific agent"""
    print(f"\n🧪 Testing {agent_name}")
    print("-" * 60)
    print(f"Address: {agent_address}")
    print(f"Message: '{test_message}'")
    
    try:
        # Create a context to send messages
        ctx = Context(test_client, None)
        
        # Send message to agent
        print(f"📤 Sending message...")
        await ctx.send(agent_address, txt(test_message))
        
        # Wait a bit for response
        await asyncio.sleep(2)
        
        print(f"✅ Message sent successfully")
        print(f"💡 Check {agent_name} logs for response")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

async def test_all_agents():
    """Test all agents"""
    print("=" * 80)
    print("🎣 Testing Agent Communication")
    print("=" * 80)
    print()
    
    for agent_name, agent_address in AGENTS.items():
        test_message = TEST_MESSAGES.get(agent_name, "Hello")
        await test_agent_send(agent_name, agent_address, test_message)
        await asyncio.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 80)
    print("✅ Communication Tests Complete")
    print("=" * 80)
    print("\n💡 Check individual agent logs to see responses:")
    print("   - backend/logs/phish_master.log")
    print("   - backend/logs/finance_phisher.log")
    print("   - backend/logs/health_phisher.log")
    print("   - backend/logs/personal_phisher.log")
    print("   - backend/logs/phish_refiner.log")

if __name__ == "__main__":
    print("Starting agent communication tests...")
    print("This will send messages to each agent using the proper uagents protocol")
    print()
    
    try:
        asyncio.run(test_all_agents())
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted")
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")

