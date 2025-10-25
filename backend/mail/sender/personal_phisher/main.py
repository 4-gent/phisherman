#!/usr/bin/env python3
"""
Personal Phisher Agent - Generates personal-info phishing templates for training.
This agent specializes in creating believable personal information phishing scenarios.
"""

import json
import asyncio
from typing import Dict, List, Any
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Initialize the agent
personal_phisher = Agent(
    name="personal_phisher",
    seed="personal-phisher-seed-key-2025",
    port=8004,
    endpoint=["http://127.0.0.1:8004/submit"],
)

# Fund the agent if needed (disabled for demo)
# fund_agent_if_low(personal_phisher.wallet.address())

class PersonalRequest(Model):
    """Request model for personal phishing template generation"""
    urgency_level: int = 5
    target_audience: str = "general"
    scenario_type: str = "account_verification"  # account_verification, data_update, security_alert, etc.

class PersonalResponse(Model):
    """Response model for personal phishing templates"""
    template_id: str
    subject: str
    preheader: str
    html_body: str
    plain_text_body: str
    placeholders: List[Dict[str, str]]
    urgency_score: int
    safety_flags: List[str]
    recommended_redirect: str

@personal_phisher.on_message(model=PersonalRequest)
async def handle_personal_request(ctx: Context, sender: str, msg: PersonalRequest):
    """Handle personal phishing template generation requests"""
    ctx.logger.info(f"Received personal phishing request: {msg.scenario_type}")
    
    # System prompt for the personal phisher
    system_prompt = f"""
    You are the Personal Phisher, an AI agent specialized in generating personal information phishing training emails.
    
    Your expertise:
    - Social media and online account communications
    - Personal data verification and update requests
    - Account security and login notifications
    - Identity verification and profile updates
    - Personal service communications (shopping, subscriptions, etc.)
    
    Current request:
    - Scenario Type: {msg.scenario_type}
    - Urgency Level: {msg.urgency_level}
    - Target Audience: {msg.target_audience}
    
    Generate a personal phishing template that is:
    - Believable but clearly educational
    - Appropriate for personal information training scenarios
    - Safe for training purposes
    - Includes proper safety flags and placeholders
    """
    
    # Generate personal phishing template
    template = generate_personal_template(msg)
    
    # Create structured response
    response = PersonalResponse(
        template_id=f"personal_{msg.scenario_type}_{ctx.storage.get('template_count', 0) + 1}",
        subject=template["subject"],
        preheader=template["preheader"],
        html_body=template["html_body"],
        plain_text_body=template["plain_text_body"],
        placeholders=template["placeholders"],
        urgency_score=msg.urgency_level,
        safety_flags=template["safety_flags"],
        recommended_redirect=f"training_personal_{msg.scenario_type}"
    )
    
    # Update template count
    ctx.storage.set('template_count', ctx.storage.get('template_count', 0) + 1)
    
    # Send response
    await ctx.send(sender, response)
    
    # Log the generated template
    ctx.logger.info(f"Generated personal phishing template: {response.template_id}")

def generate_personal_template(request: PersonalRequest) -> Dict[str, Any]:
    """Generate personal phishing templates based on scenario type"""
    
    templates = {
        "account_verification": {
            "subject": "Account Verification Required - [service_name]",
            "preheader": "Please verify your account to maintain access",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #007bff;">Account Verification Required</h2>
                    <p>Dear [user_name],</p>
                    <p>We need to verify your account information to ensure the security of your [service_name] account.</p>
                    <p style="background-color: #d1ecf1; padding: 15px; border-left: 4px solid #17a2b8;">
                        <strong>Verification Required:</strong> Please verify your account details to maintain full access to your account.
                    </p>
                    <p>Click below to verify your account:</p>
                    <a href="[verification_link]" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Account</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Account Verification Required
            
            Dear [user_name],
            
            We need to verify your account information to ensure the security of your [service_name] account.
            
            Verification Required: Please verify your account details to maintain full access to your account.
            
            Click below to verify your account:
            [verification_link]
            """,
            "placeholders": [
                {"name": "user_name", "description": "User's full name or username"},
                {"name": "service_name", "description": "Service or platform name"},
                {"name": "verification_link", "description": "Training verification link"}
            ],
            "safety_flags": ["requests_personal_info", "account_verification", "access_threat"]
        },
        "data_update": {
            "subject": "Profile Update Required - [platform_name]",
            "preheader": "Your profile information needs to be updated",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #ffc107;">Profile Update Required</h2>
                    <p>Dear [user_name],</p>
                    <p>We need to update your profile information to ensure accurate account details and better service.</p>
                    <p style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;">
                        <strong>Update Required:</strong> Please update your profile information within 7 days to maintain account functionality.
                    </p>
                    <p>Click below to update your profile:</p>
                    <a href="[update_link]" style="background-color: #ffc107; color: black; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Update Profile</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Profile Update Required
            
            Dear [user_name],
            
            We need to update your profile information to ensure accurate account details and better service.
            
            Update Required: Please update your profile information within 7 days to maintain account functionality.
            
            Click below to update your profile:
            [update_link]
            """,
            "placeholders": [
                {"name": "user_name", "description": "User's full name or username"},
                {"name": "platform_name", "description": "Platform or service name"},
                {"name": "update_link", "description": "Training update link"}
            ],
            "safety_flags": ["requests_personal_info", "profile_update", "functionality_threat"]
        },
        "security_alert": {
            "subject": "Security Alert - Unusual Activity Detected",
            "preheader": "We detected unusual activity on your account",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #dc3545;">Security Alert</h2>
                    <p>Dear [user_name],</p>
                    <p>We have detected unusual activity on your account from [location] at [login_time].</p>
                    <p style="background-color: #f8d7da; padding: 15px; border-left: 4px solid #dc3545;">
                        <strong>SECURITY ALERT:</strong> If this wasn't you, please secure your account immediately.
                    </p>
                    <p>Click below to review and secure your account:</p>
                    <a href="[security_link]" style="background-color: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Secure Account</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Security Alert
            
            Dear [user_name],
            
            We have detected unusual activity on your account from [location] at [login_time].
            
            SECURITY ALERT: If this wasn't you, please secure your account immediately.
            
            Click below to review and secure your account:
            [security_link]
            """,
            "placeholders": [
                {"name": "user_name", "description": "User's full name or username"},
                {"name": "location", "description": "Suspicious login location"},
                {"name": "login_time", "description": "Time of suspicious activity"},
                {"name": "security_link", "description": "Training security link"}
            ],
            "safety_flags": ["security_alert", "unusual_activity", "account_compromise"]
        },
        "subscription_renewal": {
            "subject": "Subscription Renewal Required - [service_name]",
            "preheader": "Your subscription is about to expire",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #28a745;">Subscription Renewal Required</h2>
                    <p>Dear [subscriber_name],</p>
                    <p>Your [service_name] subscription is set to expire on [expiration_date]. To continue enjoying our services, please renew your subscription.</p>
                    <p style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745;">
                        <strong>Renewal Required:</strong> Renew before [expiration_date] to avoid service interruption.
                    </p>
                    <p>Click below to renew your subscription:</p>
                    <a href="[renewal_link]" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Renew Subscription</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Subscription Renewal Required
            
            Dear [subscriber_name],
            
            Your [service_name] subscription is set to expire on [expiration_date]. To continue enjoying our services, please renew your subscription.
            
            Renewal Required: Renew before [expiration_date] to avoid service interruption.
            
            Click below to renew your subscription:
            [renewal_link]
            """,
            "placeholders": [
                {"name": "subscriber_name", "description": "Subscriber's name"},
                {"name": "service_name", "description": "Service or subscription name"},
                {"name": "expiration_date", "description": "Subscription expiration date"},
                {"name": "renewal_link", "description": "Training renewal link"}
            ],
            "safety_flags": ["requests_payment", "service_interruption", "subscription_renewal"]
        }
    }
    
    return templates.get(request.scenario_type, templates["account_verification"])

@personal_phisher.on_event("startup")
async def startup(ctx: Context):
    """Initialize the agent on startup"""
    ctx.logger.info("Personal Phisher agent started and ready to generate personal phishing templates")
    ctx.storage.set('template_count', 0)

if __name__ == "__main__":
    print("Personal Phisher Agent - Personal Information Phishing Template Generator")
    print("=" * 70)
    print("System Prompt: Specializes in personal information phishing scenarios for training")
    print("Capabilities: Account verification, data updates, security alerts, subscriptions")
    print("=" * 70)
    
    # Example structured JSON output
    example_output = {
        "template_id": "personal_account_verification_001",
        "subject": "Account Verification Required - [service_name]",
        "preheader": "Please verify your account to maintain access",
        "html_body": "<html><body><h2>Account Verification Required</h2><p>We need to verify your account information to ensure the security of your [service_name] account.</p></body></html>",
        "plain_text_body": "Account Verification Required\n\nWe need to verify your account information to ensure the security of your [service_name] account.",
        "placeholders": [
            {"name": "user_name", "description": "User's full name or username"},
            {"name": "service_name", "description": "Service or platform name"},
            {"name": "verification_link", "description": "Training verification link"}
        ],
        "urgency_score": 7,
        "safety_flags": ["requests_personal_info", "account_verification", "access_threat"],
        "recommended_redirect": "training_personal_account_verification"
    }
    
    print("Example Output Structure:")
    print(json.dumps(example_output, indent=2))
    print("=" * 70)
    
    # Run the agent
    personal_phisher.run()
