#!/usr/bin/env python3
"""
Terminal Chat Interface for Phisherman Agents
Interactive CLI to chat with agents, similar to Agentverse Inspector
"""

import requests
import json
from datetime import datetime
from uuid import uuid4
from typing import Optional

# Agent configuration
AGENTS = {
    "1": {
        "name": "phish_master",
        "display": "Phish Master (Orchestrator)",
        "port": 8001,
        "address": "agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr",
        "description": "Coordinates phishing template generation across domain agents"
    },
    "2": {
        "name": "finance_phisher",
        "display": "Finance Phisher",
        "port": 8002,
        "address": "agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z",
        "description": "Generates financial phishing templates"
    },
    "3": {
        "name": "health_phisher",
        "display": "Health Phisher",
        "port": 8003,
        "address": "agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h",
        "description": "Generates healthcare phishing templates"
    },
    "4": {
        "name": "personal_phisher",
        "display": "Personal Phisher",
        "port": 8004,
        "address": "agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz",
        "description": "Generates personal information phishing templates"
    },
    "5": {
        "name": "phish_refiner",
        "display": "Phish Refiner",
        "port": 8005,
        "address": "agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr",
        "description": "Refines and improves phishing templates"
    }
}

def create_chat_message(text: str) -> dict:
    """Create proper ChatMessage format for uAgent"""
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

def create_envelope(message: dict, recipient: str = "agent1wzx2akp7cfv") -> dict:
    """Create uAgent envelope"""
    return {
        "sender": "terminal_user",
        "recipient": recipient,
        "message": message
    }

def send_message_to_agent(agent_name: str, port: int, message: str, agent_address: str) -> Optional[dict]:
    """Send message to agent and get response"""
    url = f"http://127.0.0.1:{port}/submit"
    
    # Create ChatMessage
    chat_msg = create_chat_message(message)
    
    # Create envelope with proper agent address
    envelope = create_envelope(chat_msg, agent_address)
    
    try:
        response = requests.post(
            url,
            json=envelope,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            # Try to extract useful info from error
            try:
                error_data = response.json()
                return {"error": error_data.get("error", f"HTTP {response.status_code}")}
            except:
                return {"error": f"HTTP {response.status_code}: {response.text[:100]}"}
                
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused - agent may not be running"}
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except Exception as e:
        return {"error": str(e)}

def check_agent_running(port: int) -> bool:
    """Check if agent is running"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def print_header():
    """Print header"""
    print("\n" + "="*70)
    print("🤖 Phisherman Agent Terminal Chat")
    print("="*70)

def print_agents():
    """Print available agents"""
    print("\n📋 Available Agents:")
    print("-"*70)
    for key, agent in AGENTS.items():
        status = "🟢" if check_agent_running(agent["port"]) else "🔴"
        print(f"{key}. {status} {agent['display']}")
        print(f"   {agent['description']}")
    print("-"*70)

def chat_with_agent(agent_info: dict):
    """Interactive chat with an agent"""
    agent_name = agent_info["name"]
    display_name = agent_info["display"]
    port = agent_info["port"]
    agent_address = agent_info["address"]
    
    print(f"\n{'='*70}")
    print(f"💬 Chatting with {display_name}")
    print(f"{'='*70}")
    print(f"Type 'exit' or 'quit' to end chat")
    print(f"Type 'help' for suggestions")
    print("-"*70)
    
    # Send initial message to start session
    print(f"\n{display_name}: Connecting...")
    initial_response = send_message_to_agent(agent_name, port, "hello", agent_address)
    
    if initial_response and "error" not in initial_response:
        print(f"\n{display_name}: Connected! How can I help?")
    elif initial_response and "error" in initial_response:
        print(f"\n⚠️  Note: {initial_response['error']}")
        print("   Continuing anyway - this is expected for local uAgent agents")
    
    print("-"*70)
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input(f"\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print(f"\n👋 Ending chat with {display_name}")
                break
            
            if user_input.lower() == 'help':
                print("\n💡 Message suggestions:")
                if agent_name == "phish_master":
                    print("   • 'finance' - Coordinate with Finance Phisher")
                    print("   • 'health' - Coordinate with Health Phisher")
                    print("   • 'personal' - Coordinate with Personal Phisher")
                elif agent_name == "finance_phisher":
                    print("   • 'bank' - Banking phishing template")
                    print("   • 'payment' - Payment verification template")
                elif agent_name == "health_phisher":
                    print("   • 'appointment' - Medical appointment template")
                    print("   • 'insurance' - Health insurance template")
                elif agent_name == "personal_phisher":
                    print("   • 'social media' - Social media phishing")
                    print("   • 'email account' - Email account phishing")
                elif agent_name == "phish_refiner":
                    print("   • 'realism' - Enhance realism")
                    print("   • 'tone' - Refine language/tone")
                continue
            
            # Send message to agent
            print(f"\n⏳ Sending message...")
            response = send_message_to_agent(agent_name, port, user_input, agent_address)
            
            # Handle response
            if response:
                if "error" in response:
                    print(f"\n⚠️  Error: {response['error']}")
                else:
                    # Try to extract text from response
                    response_text = extract_response_text(response)
                    if response_text:
                        print(f"\n{display_name}: {response_text}")
                    else:
                        print(f"\n{display_name}: {json.dumps(response, indent=2)}")
            else:
                print(f"\n⚠️  No response from agent")
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Ending chat with {display_name}")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def extract_response_text(response: dict) -> Optional[str]:
    """Extract text response from agent response"""
    # Try different response formats
    if isinstance(response, dict):
        # Check for nested message structure
        if "message" in response:
            msg = response["message"]
            if isinstance(msg, dict) and "content" in msg:
                for content in msg["content"]:
                    if isinstance(content, dict) and "text" in content:
                        return content["text"]
        # Check for direct text field
        if "text" in response:
            return response["text"]
        # Check for response field
        if "response" in response:
            return str(response["response"])
    return None

def main():
    """Main function"""
    print_header()
    
    while True:
        print_agents()
        
        choice = input("\nSelect an agent (1-5) or 'q' to quit: ").strip()
        
        if choice.lower() in ['q', 'quit', 'exit']:
            print("\n👋 Goodbye!")
            break
        
        if choice in AGENTS:
            agent_info = AGENTS[choice]
            
            # Check if agent is running
            if not check_agent_running(agent_info["port"]):
                print(f"\n❌ {agent_info['display']} is not running!")
                print(f"   Start it with: python3 {agent_info['name']}/main.py")
                continue
            
            # Start chat
            chat_with_agent(agent_info)
        else:
            print("\n❌ Invalid choice. Please select 1-5 or 'q' to quit.")

if __name__ == "__main__":
    main()

