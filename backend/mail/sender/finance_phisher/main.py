#!/usr/bin/env python3
"""
Finance Phisher Agent - Generates financial phishing templates for training.
This agent specializes in creating believable financial phishing scenarios.
"""

import json
import asyncio
from typing import Dict, List, Any
from uagents import Agent, Context, Model
# from uagents.setup import fund_agent_if_low  # Disabled for mailbox mode

# Initialize the agent
finance_phisher = Agent(
    name="finance_phisher",
    seed="finance-phisher-seed-key-2025",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)

# Fund the agent if needed (disabled for mailbox mode)
# fund_agent_if_low(finance_phisher.wallet.address())

class FinanceRequest(Model):
    """Request model for financial phishing template generation"""
    urgency_level: int = 5
    target_audience: str = "general"
    scenario_type: str = "payment_verification"  # payment_verification, invoice, account_suspension, etc.

class FinanceResponse(Model):
    """Response model for financial phishing templates"""
    template_id: str
    subject: str
    preheader: str
    html_body: str
    plain_text_body: str
    placeholders: List[Dict[str, str]]
    urgency_score: int
    safety_flags: List[str]
    recommended_redirect: str

@finance_phisher.on_message(model=FinanceRequest)
async def handle_finance_request(ctx: Context, sender: str, msg: FinanceRequest):
    """Handle financial phishing template generation requests"""
    ctx.logger.info(f"Received finance phishing request: {msg.scenario_type}")
    
    # System prompt for the finance phisher
    system_prompt = f"""
    You are the Finance Phisher, an AI agent specialized in generating financial phishing training emails.
    
    Your expertise:
    - Financial institution communications (banks, credit cards, payment processors)
    - Invoice and payment-related scenarios
    - Account security and verification requests
    - Investment and trading platform communications
    
    Current request:
    - Scenario Type: {msg.scenario_type}
    - Urgency Level: {msg.urgency_level}
    - Target Audience: {msg.target_audience}
    
    Generate a financial phishing template that is:
    - Believable but clearly educational
    - Appropriate for financial training scenarios
    - Safe for training purposes
    - Includes proper safety flags and placeholders
    """
    
    # Generate financial phishing template
    template = generate_finance_template(msg)
    
    # Create structured response
    response = FinanceResponse(
        template_id=f"finance_{msg.scenario_type}_{ctx.storage.get('template_count', 0) + 1}",
        subject=template["subject"],
        preheader=template["preheader"],
        html_body=template["html_body"],
        plain_text_body=template["plain_text_body"],
        placeholders=template["placeholders"],
        urgency_score=msg.urgency_level,
        safety_flags=template["safety_flags"],
        recommended_redirect=f"training_finance_{msg.scenario_type}"
    )
    
    # Update template count
    ctx.storage.set('template_count', ctx.storage.get('template_count', 0) + 1)
    
    # Send response
    await ctx.send(sender, response)
    
    # Log the generated template
    ctx.logger.info(f"Generated finance phishing template: {response.template_id}")

def generate_finance_template(request: FinanceRequest) -> Dict[str, Any]:
    """Generate financial phishing templates based on scenario type"""
    
    templates = {
        "payment_verification": {
            "subject": "Urgent: Payment Verification Required - Action Needed",
            "preheader": "Your account needs immediate attention to prevent suspension",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #dc3545;">Payment Verification Required</h2>
                    <p>Dear [recipient_name],</p>
                    <p>We have detected unusual activity on your account ending in [account_last_four]. To protect your account, we need to verify your payment information immediately.</p>
                    <p style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;">
                        <strong>Action Required:</strong> Please verify your payment details within 24 hours to prevent account suspension.
                    </p>
                    <p>Click the button below to verify your information:</p>
                    <a href="[verification_link]" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Payment Info</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Payment Verification Required
            
            Dear [recipient_name],
            
            We have detected unusual activity on your account ending in [account_last_four]. To protect your account, we need to verify your payment information immediately.
            
            ACTION REQUIRED: Please verify your payment details within 24 hours to prevent account suspension.
            
            Click here to verify: [verification_link]
            """,
            "placeholders": [
                {"name": "recipient_name", "description": "Target's full name"},
                {"name": "account_last_four", "description": "Last 4 digits of account number"},
                {"name": "verification_link", "description": "Training verification link"}
            ],
            "safety_flags": ["requests_payment_info", "urgent_action_required", "account_suspension_threat"]
        },
        "invoice": {
            "subject": "Invoice Payment Overdue - Immediate Action Required",
            "preheader": "Your invoice payment is past due",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #dc3545;">Invoice Payment Overdue</h2>
                    <p>Dear [recipient_name],</p>
                    <p>Your invoice #[invoice_number] for $[amount] is now [days_overdue] days overdue.</p>
                    <p style="background-color: #f8d7da; padding: 15px; border-left: 4px solid #dc3545;">
                        <strong>Late Payment Fee:</strong> A $[late_fee] late payment fee has been applied to your account.
                    </p>
                    <p>Please remit payment immediately to avoid additional fees and service interruption.</p>
                    <a href="[payment_link]" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Pay Now</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Invoice Payment Overdue
            
            Dear [recipient_name],
            
            Your invoice #[invoice_number] for $[amount] is now [days_overdue] days overdue.
            
            LATE PAYMENT FEE: A $[late_fee] late payment fee has been applied to your account.
            
            Please remit payment immediately to avoid additional fees and service interruption.
            
            Pay now: [payment_link]
            """,
            "placeholders": [
                {"name": "recipient_name", "description": "Target's full name"},
                {"name": "invoice_number", "description": "Invoice number"},
                {"name": "amount", "description": "Invoice amount"},
                {"name": "days_overdue", "description": "Days overdue"},
                {"name": "late_fee", "description": "Late payment fee amount"},
                {"name": "payment_link", "description": "Training payment link"}
            ],
            "safety_flags": ["requests_payment", "late_fee_threat", "service_interruption"]
        },
        "account_suspension": {
            "subject": "Account Suspension Notice - Immediate Verification Required",
            "preheader": "Your account will be suspended without immediate action",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #dc3545;">Account Suspension Notice</h2>
                    <p>Dear [recipient_name],</p>
                    <p>We have detected suspicious activity on your account [account_number]. For your security, we need to verify your identity immediately.</p>
                    <p style="background-color: #f8d7da; padding: 15px; border-left: 4px solid #dc3545;">
                        <strong>URGENT:</strong> Your account will be suspended in 2 hours if verification is not completed.
                    </p>
                    <p>Please click below to verify your account and prevent suspension:</p>
                    <a href="[verification_link]" style="background-color: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Account Now</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Account Suspension Notice
            
            Dear [recipient_name],
            
            We have detected suspicious activity on your account [account_number]. For your security, we need to verify your identity immediately.
            
            URGENT: Your account will be suspended in 2 hours if verification is not completed.
            
            Please click below to verify your account and prevent suspension:
            [verification_link]
            """,
            "placeholders": [
                {"name": "recipient_name", "description": "Target's full name"},
                {"name": "account_number", "description": "Account number or username"},
                {"name": "verification_link", "description": "Training verification link"}
            ],
            "safety_flags": ["account_suspension_threat", "urgent_verification", "suspicious_activity"]
        }
    }
    
    return templates.get(request.scenario_type, templates["payment_verification"])

@finance_phisher.on_event("startup")
async def startup(ctx: Context):
    """Initialize the agent on startup"""
    ctx.logger.info("Finance Phisher agent started and ready to generate financial phishing templates")
    ctx.storage.set('template_count', 0)

if __name__ == "__main__":
    print("Finance Phisher Agent - Financial Phishing Template Generator")
    print("=" * 60)
    print("System Prompt: Specializes in financial phishing scenarios for training")
    print("Capabilities: Payment verification, invoices, account suspension, banking alerts")
    print("=" * 60)
    
    # Example structured JSON output
    example_output = {
        "template_id": "finance_payment_verification_001",
        "subject": "Urgent: Payment Verification Required - Action Needed",
        "preheader": "Your account needs immediate attention to prevent suspension",
        "html_body": "<html><body><h2>Payment Verification Required</h2><p>We have detected unusual activity on your account ending in [account_last_four]. To protect your account, we need to verify your payment information immediately.</p></body></html>",
        "plain_text_body": "Payment Verification Required\n\nWe have detected unusual activity on your account ending in [account_last_four]. Please verify your payment information immediately.",
        "placeholders": [
            {"name": "recipient_name", "description": "Target's full name"},
            {"name": "account_last_four", "description": "Last 4 digits of account number"},
            {"name": "verification_link", "description": "Training verification link"}
        ],
        "urgency_score": 8,
        "safety_flags": ["requests_payment_info", "urgent_action_required", "account_suspension_threat"],
        "recommended_redirect": "training_finance_payment_verification"
    }
    
    print("Example Output Structure:")
    print(json.dumps(example_output, indent=2))
    print("=" * 60)
    
    # Run the agent
    finance_phisher.run()
