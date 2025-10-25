#!/usr/bin/env python3
"""
Update Agentverse Endpoints
Reads mailbox endpoints from agentverse_endpoints.env and provides update instructions
"""

import json
import os
from pathlib import Path

def read_endpoints_env():
    """Read endpoints from env file"""
    env_file = Path(__file__).parent.parent / "agentverse_endpoints.env"
    
    if not env_file.exists():
        print("⚠️  agentverse_endpoints.env not found")
        print("   Please create this file with mailbox endpoints in format:")
        print("   phish_master=https://mailbox.example.com/agent1...")
        return {}
    
    endpoints = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    endpoints[parts[0].strip()] = parts[1].strip()
    
    return endpoints

def main():
    """Main function"""
    print("=" * 70)
    print("📝 Agentverse Endpoint Update Instructions")
    print("=" * 70)
    
    endpoints = read_endpoints_env()
    
    if not endpoints:
        print("\nNo endpoints found. Please provide mailbox endpoints.")
        return
    
    diagnostics_dir = Path(__file__).parent.parent / "diagnostics"
    diagnostics_dir.mkdir(exist_ok=True)
    
    output_file = diagnostics_dir / "agentverse_update.txt"
    
    with open(output_file, 'w') as f:
        f.write("Agentverse Endpoint Update Instructions\n")
        f.write("=" * 70 + "\n\n")
        
        for agent_name, endpoint in endpoints.items():
            f.write(f"{agent_name}:\n")
            f.write(f"  Mailbox Endpoint: {endpoint}\n")
            f.write(f"\n  Update Steps:\n")
            f.write(f"  1. Log in to https://agentverse.ai\n")
            f.write(f"  2. Navigate to '{agent_name}' agent settings\n")
            f.write(f"  3. Update the 'Endpoint' field to: {endpoint}\n")
            f.write(f"  4. Save changes\n\n")
            
            print(f"\n{agent_name}:")
            print(f"  Endpoint: {endpoint}")
    
    print("\n" + "=" * 70)
    print(f"✅ Instructions saved to: {output_file}")
    print("=" * 70)
    
    print("\n📋 Manual Update Steps:")
    print("1. Log in to https://agentverse.ai")
    print("2. For each agent, navigate to agent settings")
    print("3. Update the 'Endpoint' field with the mailbox URL")
    print("4. Save changes")
    print("\nNote: Agentverse may require API key authentication for programmatic updates.")

if __name__ == "__main__":
    main()

