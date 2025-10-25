#!/usr/bin/env python3
"""
Phish Master Agent - The orchestrator for phishing training email generation.
This agent coordinates with domain-specific agents to generate phishing templates.
"""

import json
import asyncio
from typing import Dict, List, Any
from uagents import Agent, Context, Model
# from uagents.setup import fund_agent_if_low  # Disabled for mailbox mode

# Initialize the agent
phish_master = Agent(
    name="phish_master",
    seed="phish-master-seed-key-2025",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

# Fund the agent if needed (disabled for mailbox mode)
# fund_agent_if_low(phish_master.wallet.address())

class PhishingRequest(Model):
    """Request model for phishing template generation"""
    domain: str  # "finance", "health", or "personal"
    urgency_level: int = 5  # 1-10 scale
    target_audience: str = "general"
    custom_requirements: str = ""

class PhishingResponse(Model):
    """Response model for aggregated phishing templates"""
    template_id: str
    subject: str
    preheader: str
    html_body: str
    plain_text_body: str
    placeholders: List[Dict[str, str]]
    urgency_score: int
    safety_flags: List[str]
    recommended_redirect: str
    domain_used: str
    generated_by: str

@phish_master.on_message(model=PhishingRequest)
async def handle_phishing_request(ctx: Context, sender: str, msg: PhishingRequest):
    """Handle phishing template generation requests"""
    ctx.logger.info(f"Received phishing request for domain: {msg.domain}")
    
    # System prompt for the orchestrator
    system_prompt = f"""
    You are the Phish Master, an AI orchestrator for generating safe phishing training emails.
    
    Your role:
    1. Choose the appropriate domain agent based on the request
    2. Coordinate with domain-specific agents (finance_phisher, health_phisher, personal_phisher)
    3. Call phish_refiner to adjust tone/content if needed
    4. Aggregate final results into structured JSON
    
    Current request:
    - Domain: {msg.domain}
    - Urgency Level: {msg.urgency_level}
    - Target Audience: {msg.target_audience}
    - Custom Requirements: {msg.custom_requirements}
    
    Generate a phishing template that is:
    - Safe for training purposes
    - Believable but clearly educational
    - Appropriate for the specified domain
    - Scored for urgency and safety
    """
    
    # Simulate coordination with domain agents
    template_data = await coordinate_domain_agents(msg)
    
    # Create structured response
    response = PhishingResponse(
        template_id=f"phish_{msg.domain}_{ctx.storage.get('template_count', 0) + 1}",
        subject=template_data["subject"],
        preheader=template_data["preheader"],
        html_body=template_data["html_body"],
        plain_text_body=template_data["plain_text_body"],
        placeholders=template_data["placeholders"],
        urgency_score=msg.urgency_level,
        safety_flags=template_data["safety_flags"],
        recommended_redirect=f"training_{msg.domain}_link",
        domain_used=msg.domain,
        generated_by="phish_master"
    )
    
    # Update template count
    ctx.storage.set('template_count', ctx.storage.get('template_count', 0) + 1)
    
    # Send response
    await ctx.send(sender, response)
    
    # Log the generated template
    ctx.logger.info(f"Generated phishing template: {response.template_id}")

async def coordinate_domain_agents(request: PhishingRequest) -> Dict[str, Any]:
    """Coordinate with domain-specific agents to generate templates"""
    
    # This is a placeholder for actual agent communication
    # In a real implementation, this would call other agents via uAgent messaging
    
    domain_templates = {
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
    
    return domain_templates.get(request.domain, domain_templates["personal"])

@phish_master.on_event("startup")
async def startup(ctx: Context):
    """Initialize the agent on startup"""
    ctx.logger.info("Phish Master agent started and ready to coordinate phishing template generation")
    ctx.storage.set('template_count', 0)

if __name__ == "__main__":
    print("Phish Master Agent - Orchestrator for Phishing Training")
    print("=" * 50)
    print("System Prompt: Orchestrates phishing template generation across domain agents")
    print("Capabilities: Domain selection, agent coordination, template aggregation")
    print("=" * 50)
    
    # Example structured JSON output
    example_output = {
        "template_id": "phish_finance_001",
        "subject": "Urgent: Payment Verification Required",
        "preheader": "Your account needs immediate attention",
        "html_body": "<html><body><h2>Payment Verification Required</h2><p>We need to verify your payment information to prevent account suspension.</p></body></html>",
        "plain_text_body": "Payment Verification Required\n\nWe need to verify your payment information to prevent account suspension.",
        "placeholders": [
            {"name": "recipient_name", "description": "Target's full name"},
            {"name": "account_number", "description": "Last 4 digits of account"}
        ],
        "urgency_score": 8,
        "safety_flags": ["requests_payment_info", "urgent_action_required"],
        "recommended_redirect": "training_finance_link",
        "domain_used": "finance",
        "generated_by": "phish_master"
    }
    
    print("Example Output Structure:")
    print(json.dumps(example_output, indent=2))
    print("=" * 50)
    
    # Run the agent
    phish_master.run()
