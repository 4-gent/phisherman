#!/usr/bin/env python3
"""
Agentverse Registration Script for Phisherman Agents
This script helps register all 5 agents on Agentverse for discovery.
"""

import json
import asyncio
import requests
from typing import Dict, List, Any

class AgentverseRegistrar:
    """Handles registration of Phisherman agents on Agentverse"""
    
    def __init__(self):
        self.agents_config = {
            "phish_master": {
                "name": "phish_master",
                "description": "Orchestrates phishing template generation across domain agents for cybersecurity training",
                "capabilities": [
                    "phishing_template_generation",
                    "agent_coordination", 
                    "template_aggregation",
                    "multi_domain_routing"
                ],
                "endpoints": ["http://127.0.0.1:8001/submit"],
                "protocol": "chat_v0.3.0",
                "tags": ["cybersecurity", "training", "orchestration", "fetch.ai"],
                "version": "1.0.0",
                "author": "Phisherman Team",
                "license": "MIT"
            },
            "finance_phisher": {
                "name": "finance_phisher",
                "description": "Generates financial phishing templates for cybersecurity training",
                "capabilities": [
                    "financial_phishing_templates",
                    "payment_verification_scenarios",
                    "banking_alerts",
                    "invoice_generation"
                ],
                "endpoints": ["http://127.0.0.1:8002/submit"],
                "protocol": "chat_v0.3.0",
                "tags": ["finance", "phishing", "training", "banking"],
                "version": "1.0.0",
                "author": "Phisherman Team",
                "license": "MIT"
            },
            "health_phisher": {
                "name": "health_phisher", 
                "description": "Generates healthcare phishing templates for cybersecurity training",
                "capabilities": [
                    "healthcare_phishing_templates",
                    "medical_appointments",
                    "insurance_verification",
                    "test_results_notifications"
                ],
                "endpoints": ["http://127.0.0.1:8003/submit"],
                "protocol": "chat_v0.3.0",
                "tags": ["healthcare", "phishing", "training", "medical"],
                "version": "1.0.0",
                "author": "Phisherman Team",
                "license": "MIT"
            },
            "personal_phisher": {
                "name": "personal_phisher",
                "description": "Generates personal information phishing templates for cybersecurity training", 
                "capabilities": [
                    "personal_phishing_templates",
                    "account_verification",
                    "security_alerts",
                    "subscription_management"
                ],
                "endpoints": ["http://127.0.0.1:8004/submit"],
                "protocol": "chat_v0.3.0",
                "tags": ["personal", "phishing", "training", "security"],
                "version": "1.0.0",
                "author": "Phisherman Team",
                "license": "MIT"
            },
            "phish_refiner": {
                "name": "phish_refiner",
                "description": "Refines existing phishing templates based on instructions",
                "capabilities": [
                    "template_refinement",
                    "tone_adjustment",
                    "content_modification",
                    "urgency_modification"
                ],
                "endpoints": ["http://127.0.0.1:8005/submit"],
                "protocol": "chat_v0.3.0",
                "tags": ["refinement", "chatbot", "training", "modification"],
                "version": "1.0.0",
                "author": "Phisherman Team",
                "license": "MIT"
            }
        }
    
    def check_agent_status(self, agent_name: str) -> bool:
        """Check if an agent is running and accessible"""
        try:
            config = self.agents_config[agent_name]
            endpoint = config["endpoints"][0]
            
            # Test agent endpoint
            response = requests.get(f"{endpoint.replace('/submit', '/status')}", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_registration_json(self, agent_name: str) -> Dict[str, Any]:
        """Generate registration JSON for an agent"""
        return self.agents_config[agent_name]
    
    def print_registration_instructions(self):
        """Print step-by-step registration instructions"""
        print("🚀 Phisherman Agent Registration Instructions")
        print("=" * 60)
        print()
        print("📋 STEP 1: Start All Agents")
        print("-" * 30)
        print("Open 5 terminal windows and run:")
        print("Terminal 1: cd backend/mail/sender/phish_master && python3 main.py")
        print("Terminal 2: cd backend/mail/sender/finance_phisher && python3 main.py")
        print("Terminal 3: cd backend/mail/sender/health_phisher && python3 main.py")
        print("Terminal 4: cd backend/mail/sender/personal_phisher && python3 main.py")
        print("Terminal 5: cd backend/mail/sender/phish_refiner && python3 main.py")
        print()
        
        print("🌐 STEP 2: Access Agentverse")
        print("-" * 30)
        print("1. Go to https://agentverse.ai")
        print("2. Connect your wallet (MetaMask)")
        print("3. Switch to Fetch.ai testnet")
        print("4. Get testnet FET tokens from faucet if needed")
        print()
        
        print("📝 STEP 3: Register Each Agent")
        print("-" * 30)
        for agent_name in self.agents_config.keys():
            print(f"\n🔹 Registering {agent_name}:")
            config = self.generate_registration_json(agent_name)
            print(f"   Name: {config['name']}")
            print(f"   Description: {config['description']}")
            print(f"   Endpoint: {config['endpoints'][0]}")
            print(f"   Tags: {', '.join(config['tags'])}")
            print(f"   Capabilities: {', '.join(config['capabilities'])}")
        print()
        
        print("🧪 STEP 4: Test Registration")
        print("-" * 30)
        print("1. Verify agents appear in Agentverse search")
        print("2. Test discovery on ASI:One")
        print("3. Test agent communication")
        print("4. Run end-to-end workflow")
        print()
        
        print("✅ STEP 5: Success Criteria")
        print("-" * 30)
        print("✓ All agents discoverable on Agentverse")
        print("✓ Agents accessible via ASI:One")
        print("✓ Communication working between agents")
        print("✓ Templates generating correctly")
        print("✓ End-to-end workflow functional")
    
    def test_agent_communication(self):
        """Test communication between agents"""
        print("\n🧪 Testing Agent Communication")
        print("-" * 40)
        
        # Test each agent endpoint
        for agent_name, config in self.agents_config.items():
            endpoint = config["endpoints"][0]
            print(f"Testing {agent_name} at {endpoint}...")
            
            try:
                # Test with a simple request
                test_data = {
                    "domain": "finance",
                    "urgency_level": 5,
                    "target_audience": "general"
                }
                
                response = requests.post(
                    endpoint,
                    json=test_data,
                    timeout=10,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    print(f"✅ {agent_name}: Communication successful")
                else:
                    print(f"❌ {agent_name}: Communication failed (Status: {response.status_code})")
                    
            except Exception as e:
                print(f"❌ {agent_name}: Connection error - {str(e)}")
    
    def generate_agentverse_configs(self):
        """Generate configuration files for each agent"""
        print("\n📄 Generating Agentverse Configuration Files")
        print("-" * 50)
        
        for agent_name, config in self.agents_config.items():
            filename = f"{agent_name}_agentverse_config.json"
            
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Generated: {filename}")
            print(f"   Use this config when registering {agent_name} on Agentverse")
    
    def run_registration_checklist(self):
        """Run through the registration checklist"""
        print("\n📋 Registration Checklist")
        print("-" * 30)
        
        checklist_items = [
            ("All agents running locally", self._check_all_agents_running),
            ("Agent endpoints accessible", self._check_endpoints_accessible),
            ("Unique agent names", self._check_unique_names),
            ("Proper descriptions and tags", self._check_metadata),
            ("Chat Protocol v0.3.0 compatibility", self._check_protocol_compatibility)
        ]
        
        for item, check_func in checklist_items:
            status = "✅" if check_func() else "❌"
            print(f"{status} {item}")
    
    def _check_all_agents_running(self) -> bool:
        """Check if all agents are running"""
        running_count = sum(1 for agent in self.agents_config.keys() 
                           if self.check_agent_status(agent))
        return running_count == len(self.agents_config)
    
    def _check_endpoints_accessible(self) -> bool:
        """Check if endpoints are accessible"""
        return self._check_all_agents_running()
    
    def _check_unique_names(self) -> bool:
        """Check if agent names are unique"""
        names = [config["name"] for config in self.agents_config.values()]
        return len(names) == len(set(names))
    
    def _check_metadata(self) -> bool:
        """Check if metadata is properly configured"""
        for config in self.agents_config.values():
            required_fields = ["name", "description", "capabilities", "tags"]
            if not all(field in config for field in required_fields):
                return False
        return True
    
    def _check_protocol_compatibility(self) -> bool:
        """Check if agents use Chat Protocol v0.3.0"""
        for config in self.agents_config.values():
            if config.get("protocol") != "chat_v0.3.0":
                return False
        return True

def main():
    """Main function to run the registration process"""
    registrar = AgentverseRegistrar()
    
    print("🎯 Phisherman Agent Registration Assistant")
    print("=" * 50)
    
    # Print registration instructions
    registrar.print_registration_instructions()
    
    # Generate configuration files
    registrar.generate_agentverse_configs()
    
    # Run checklist
    registrar.run_registration_checklist()
    
    # Test communication
    registrar.test_agent_communication()
    
    print("\n🎉 Registration Setup Complete!")
    print("Next: Follow the instructions above to register on Agentverse")

if __name__ == "__main__":
    main()
