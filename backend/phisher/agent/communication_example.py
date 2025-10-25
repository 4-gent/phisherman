#!/usr/bin/env python3
"""
Communication Example - Demonstrates message-based communication between agents.
This file shows how phish_master coordinates with domain agents.
"""

import asyncio
import json
from typing import Dict, Any

# Example of how agents would communicate in a real implementation
class AgentCommunicationExample:
    """Example class showing agent communication patterns"""
    
    def __init__(self):
        self.agent_endpoints = {
            "phish_master": "http://127.0.0.1:8001/submit",
            "finance_phisher": "http://127.0.0.1:8002/submit", 
            "health_phisher": "http://127.0.0.1:8003/submit",
            "personal_phisher": "http://127.0.0.1:8004/submit",
            "phish_refiner": "http://127.0.0.1:8005/submit"
        }
    
    async def simulate_phishing_generation(self, domain: str, urgency: int = 5) -> Dict[str, Any]:
        """Simulate the full phishing generation workflow"""
        
        print(f"🎯 Phish Master: Coordinating phishing generation for domain: {domain}")
        
        # Step 1: Phish Master receives request
        request = {
            "domain": domain,
            "urgency_level": urgency,
            "target_audience": "general",
            "custom_requirements": ""
        }
        
        print(f"📨 Request received: {json.dumps(request, indent=2)}")
        
        # Step 2: Route to appropriate domain agent
        domain_agent = f"{domain}_phisher"
        print(f"🔄 Routing to {domain_agent}")
        
        # Step 3: Generate template (simulated)
        template = await self._generate_domain_template(domain, urgency)
        
        # Step 4: Optional refinement
        if urgency > 7:
            print("🔧 High urgency detected - sending to phish_refiner for enhancement")
            template = await self._refine_template(template, "increase urgency")
        
        # Step 5: Aggregate final result
        final_result = {
            "template_id": f"phish_{domain}_{urgency}_001",
            "subject": template["subject"],
            "preheader": template["preheader"],
            "html_body": template["html_body"],
            "plain_text_body": template["plain_text_body"],
            "placeholders": template["placeholders"],
            "urgency_score": urgency,
            "safety_flags": template["safety_flags"],
            "recommended_redirect": f"training_{domain}_link",
            "domain_used": domain,
            "generated_by": "phish_master",
            "workflow": [
                "phish_master received request",
                f"routed to {domain_agent}",
                "template generated",
                "refinement applied" if urgency > 7 else "no refinement needed",
                "final template aggregated"
            ]
        }
        
        print(f"✅ Final template generated: {final_result['template_id']}")
        return final_result
    
    async def _generate_domain_template(self, domain: str, urgency: int) -> Dict[str, Any]:
        """Simulate domain agent template generation"""
        
        templates = {
            "finance": {
                "subject": "Urgent: Payment Verification Required",
                "preheader": "Your account needs immediate attention",
                "html_body": "<html><body><h2>Payment Verification Required</h2><p>We need to verify your payment information to prevent account suspension.</p></body></html>",
                "plain_text_body": "Payment Verification Required\n\nWe need to verify your payment information to prevent account suspension.",
                "placeholders": [
                    {"name": "recipient_name", "description": "Target's full name"},
                    {"name": "account_number", "description": "Last 4 digits of account"}
                ],
                "safety_flags": ["requests_payment_info", "urgent_action_required"]
            },
            "health": {
                "subject": "Medical Records Update Required",
                "preheader": "Your health information needs verification",
                "html_body": "<html><body><h2>Medical Records Update</h2><p>Please verify your medical information to ensure accurate records.</p></body></html>",
                "plain_text_body": "Medical Records Update\n\nPlease verify your medical information to ensure accurate records.",
                "placeholders": [
                    {"name": "patient_name", "description": "Patient's full name"},
                    {"name": "date_of_birth", "description": "Patient's date of birth"}
                ],
                "safety_flags": ["requests_medical_data", "personal_information"]
            },
            "personal": {
                "subject": "Account Security Verification",
                "preheader": "Secure your account immediately",
                "html_body": "<html><body><h2>Account Security Alert</h2><p>We detected unusual activity on your account. Please verify your identity.</p></body></html>",
                "plain_text_body": "Account Security Alert\n\nWe detected unusual activity on your account. Please verify your identity.",
                "placeholders": [
                    {"name": "username", "description": "Account username"},
                    {"name": "last_login", "description": "Last login date"}
                ],
                "safety_flags": ["requests_personal_info", "security_alert"]
            }
        }
        
        print(f"🤖 {domain}_phisher: Generating template for {domain} domain")
        return templates.get(domain, templates["personal"])
    
    async def _refine_template(self, template: Dict[str, Any], instructions: str) -> Dict[str, Any]:
        """Simulate template refinement"""
        
        print(f"🔧 phish_refiner: Applying refinement - {instructions}")
        
        # Simulate refinement
        refined = template.copy()
        if "increase urgency" in instructions.lower():
            refined["subject"] = f"URGENT: {refined['subject']}"
            refined["urgency_score"] = min(10, refined.get("urgency_score", 5) + 2)
        
        return refined

async def main():
    """Main function to demonstrate agent communication"""
    
    print("🚀 Phisherman Agent Communication Demo")
    print("=" * 50)
    
    communication = AgentCommunicationExample()
    
    # Example 1: Finance phishing with high urgency
    print("\n📧 Example 1: Finance Phishing (High Urgency)")
    finance_result = await communication.simulate_phishing_generation("finance", 8)
    print(f"Generated: {finance_result['template_id']}")
    print(f"Subject: {finance_result['subject']}")
    print(f"Urgency: {finance_result['urgency_score']}")
    
    # Example 2: Health phishing with normal urgency
    print("\n🏥 Example 2: Health Phishing (Normal Urgency)")
    health_result = await communication.simulate_phishing_generation("health", 5)
    print(f"Generated: {health_result['template_id']}")
    print(f"Subject: {health_result['subject']}")
    print(f"Urgency: {health_result['urgency_score']}")
    
    # Example 3: Personal phishing with low urgency
    print("\n👤 Example 3: Personal Phishing (Low Urgency)")
    personal_result = await communication.simulate_phishing_generation("personal", 3)
    print(f"Generated: {personal_result['template_id']}")
    print(f"Subject: {personal_result['subject']}")
    print(f"Urgency: {personal_result['urgency_score']}")
    
    print("\n✅ Communication demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
