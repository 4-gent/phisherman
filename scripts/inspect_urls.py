#!/usr/bin/env python3
"""
Generate Inspector URLs for all agents
Reads agent logs/addresses and outputs Inspector URLs to diagnostics/inspector_urls.txt
"""

import json
import urllib.parse
from pathlib import Path

# Agent configuration
AGENTS = [
    {"name": "phish_master", "port": 8001},
    {"name": "finance_phisher", "port": 8002},
    {"name": "health_phisher", "port": 8003},
    {"name": "personal_phisher", "port": 8004},
    {"name": "phish_refiner", "port": 8005},
]

def get_agent_address(agent_name):
    """Try to extract agent address from data files"""
    data_file = Path(__file__).parent.parent / "backend" / "phisher" / "agent" / agent_name / f"{agent_name}_data.json"
    
    # Alternative data file pattern
    alt_patterns = [
        f"agent*_data.json",
        f"{agent_name}_address.txt",
    ]
    
    # Try main data file
    if data_file.exists():
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
                return data.get("address", f"agent_{agent_name}")
        except:
            pass
    
    # Try alternative patterns
    agent_dir = Path(__file__).parent.parent / "backend" / "phisher" / "agent" / agent_name
    for pattern in alt_patterns:
        for file in agent_dir.glob(pattern):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    if "address" in data:
                        return data["address"]
            except:
                pass
    
    # Fallback to generated address
    return f"agent_{agent_name}"

def generate_inspector_url(agent, https_url, address):
    """Generate Inspector URL"""
    url_encoded = urllib.parse.quote(https_url, safe='')
    inspector_url = f"https://agentverse.ai/inspect/?uri={url_encoded}&address={address}"
    return inspector_url

def main():
    """Main function"""
    print("=" * 70)
    print("🔍 Generating Inspector URLs")
    print("=" * 70)
    
    inspector_urls = []
    
    # Check if tunnels.json exists
    tunnels_file = Path(__file__).parent.parent / "diagnostics" / "tunnels.json"
    
    if not tunnels_file.exists():
        print("⚠️  tunnels.json not found. Run tunnels_start.sh first.")
        print("   For now, generating URLs with localhost addresses")
    
    tunnels = {}
    if tunnels_file.exists():
        with open(tunnels_file, 'r') as f:
            tunnels = json.load(f)
    
    diagnostics_dir = Path(__file__).parent.parent / "diagnostics"
    diagnostics_dir.mkdir(exist_ok=True)
    
    output_file = diagnostics_dir / "inspector_urls.txt"
    
    with open(output_file, 'w') as f:
        f.write("Inspector URLs for Phisherman Agents\n")
        f.write("=" * 70 + "\n\n")
        
        for agent in AGENTS:
            # Get agent address
            address = get_agent_address(agent["name"])
            
            # Get HTTPS URL (or fallback to localhost)
            https_url = tunnels.get(str(agent["port"]), f"http://127.0.0.1:{agent['port']}")
            
            # Generate Inspector URL
            inspector_url = generate_inspector_url(agent, https_url, address)
            
            inspector_urls.append({
                "agent": agent["name"],
                "port": agent["port"],
                "https_url": https_url,
                "address": address,
                "inspector_url": inspector_url
            })
            
            print(f"\n{agent['name']}:")
            print(f"  Port: {agent['port']}")
            print(f"  Address: {address}")
            print(f"  HTTPS URL: {https_url}")
            print(f"  Inspector URL: {inspector_url}")
            
            f.write(f"{agent['name']}:\n")
            f.write(f"  Port: {agent['port']}\n")
            f.write(f"  Address: {address}\n")
            f.write(f"  HTTPS URL: {https_url}\n")
            f.write(f"  Inspector URL: {inspector_url}\n\n")
    
    print("\n" + "=" * 70)
    print(f"✅ Inspector URLs saved to: {output_file}")
    print("=" * 70)
    
    print("\n📋 Next Steps:")
    print("1. Open each Inspector URL in your browser")
    print("2. Click 'Connect' → Choose 'Mailbox'")
    print("3. After connection succeeds, copy the mailbox endpoint")
    print("4. Provide the mailbox endpoints to update Agentverse")

if __name__ == "__main__":
    main()

