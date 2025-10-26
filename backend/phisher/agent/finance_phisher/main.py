"""
Finance Phisher Agent - Hosted on Agentverse
Generates financial phishing templates for cybersecurity training.
"""

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent, StartSessionContent, EndSessionContent
from datetime import datetime
from uuid import uuid4
import json

# Initialize agent
agent = Agent(name="finance_phisher")
protocol = Protocol()

def txt(s: str) -> ChatMessage:
    """Helper to create text message"""
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=str(uuid4()),
        content=[TextContent(type="text", text=s)]
    )

def generate_finance_email(scenario: str = "banking") -> dict:
    """Generate financial phishing email templates"""
    
    templates = {
        "banking": {
            "subject": "🔴 URGENT: Unauthorized Transaction Detected - Immediate Verification Required",
            "preheader": "Security alert: Verify your account now",
            "html_body": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #dc3545; color: white; padding: 20px; text-align: center; }
        .content { background: #f9f9f9; padding: 30px; border: 1px solid #ddd; }
        .button { background: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        .alert { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .transaction { background: white; padding: 15px; border: 1px solid #ddd; margin: 15px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🏦 Security Alert</h2>
        </div>
        <div class="content">
            <h3>Unauthorized Transaction Detected</h3>
            <p>Dear {{recipient_name}},</p>
            <p>We have detected a suspicious transaction on your account that requires immediate verification.</p>
            
            <div class="alert">
                <strong>⚠️ Action Required:</strong> Please verify this transaction within 24 hours or your account will be temporarily suspended for security.
            </div>
            
            <div class="transaction">
                <p><strong>Transaction Details:</strong></p>
                <p>Amount: ${{amount}}</p>
                <p>Merchant: {{merchant_name}}</p>
                <p>Date: {{transaction_date}}</p>
                <p>Status: PENDING VERIFICATION</p>
            </div>
            
            <p>If you recognize this transaction, please click below to verify:</p>
            <p style="text-align: center;">
                <a href="{{verification_link}}" class="button">Verify Transaction</a>
            </p>
            
            <p>If you did not authorize this transaction, please contact our fraud department immediately.</p>
            <p>Thank you for your prompt attention to this security matter.</p>
        </div>
        <div class="footer">
            <p>© 2024 Trust Bank. Protecting your financial security.</p>
            <p>This is an automated security notification.</p>
        </div>
    </div>
</body>
</html>
            """,
            "plain_text_body": """
Unauthorized Transaction Detected - Action Required

Dear {{recipient_name}},

We have detected a suspicious transaction on your account that requires immediate verification.

⚠️ ACTION REQUIRED: Please verify this transaction within 24 hours or your account will be temporarily suspended for security.

Transaction Details:
Amount: ${{amount}}
Merchant: {{merchant_name}}
Date: {{transaction_date}}
Status: PENDING VERIFICATION

If you recognize this transaction, please verify here:
{{verification_link}}

If you did not authorize this transaction, please contact our fraud department immediately.

Thank you for your prompt attention to this security matter.

© 2024 Trust Bank. Protecting your financial security.
            """
        },
        "payment": {
            "subject": "Payment Verification Required - Account Update Needed",
            "preheader": "Verify your payment information",
            "html_body": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; text-align: center; }
        .content { background: #f9f9f9; padding: 30px; border: 1px solid #ddd; }
        .button { background: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        .info { background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 15px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>💳 Payment Services</h2>
        </div>
        <div class="content">
            <h3>Payment Method Update Required</h3>
            <p>Dear {{recipient_name}},</p>
            <p>We need to verify your payment information to ensure continued service.</p>
            
            <div class="info">
                <strong>📋 Update Required:</strong> Your payment method requires verification due to recent security updates.
            </div>
            
            <p>Please click below to update your payment information:</p>
            <p style="text-align: center;">
                <a href="{{verification_link}}" class="button">Update Payment Info</a>
            </p>
            
            <p>This update is required to maintain uninterrupted service. The process takes less than 3 minutes.</p>
            <p>Thank you for being a valued customer.</p>
        </div>
        <div class="footer">
            <p>© 2024 Payment Services. Secure & Verified.</p>
            <p>Your payment security is our priority.</p>
        </div>
    </div>
</body>
</html>
            """,
            "plain_text_body": """
Payment Method Update Required

Dear {{recipient_name}},

We need to verify your payment information to ensure continued service.

📋 UPDATE REQUIRED: Your payment method requires verification due to recent security updates.

Please update your payment information here:
{{verification_link}}

This update is required to maintain uninterrupted service. The process takes less than 3 minutes.

Thank you for being a valued customer.

© 2024 Payment Services. Secure & Verified.
            """
        }
    }
    
    return templates.get(scenario, templates["banking"])

@protocol.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    
    # Handle session start
    if any(isinstance(c, StartSessionContent) for c in msg.content):
        await ctx.send(sender, txt("Finance Phisher ready. I generate financial phishing templates for cybersecurity training. How can I help?"))
        return
    
    # Handle session end
    if any(isinstance(c, EndSessionContent) for c in msg.content):
        ctx.logger.info("Session ended")
        return
    
    # Extract user text
    user_text = msg.text() or ""
    ctx.logger.info(f"Received message: {user_text}")
    
    # Process the request and generate email
    scenario = "banking"
    if "payment" in user_text.lower() or "paypal" in user_text.lower():
        scenario = "payment"
    elif "invoice" in user_text.lower() or "billing" in user_text.lower():
        scenario = "banking"
    elif "credit" in user_text.lower() or "card" in user_text.lower():
        scenario = "payment"
    
    # Generate the email template
    email = generate_finance_email(scenario)
    
    # Create response with full email details
    response = f"""
💳 GENERATED FINANCIAL PHISHING EMAIL 💳

Subject: {email['subject']}
Preheader: {email['preheader']}

📧 EMAIL CONTENT:
{email['plain_text_body']}

📊 FULL EMAIL DATA:
{json.dumps(email, indent=2)}

✅ Financial phishing template ready for cybersecurity training!
"""
    await ctx.send(sender, txt(response))
    
    # Handle end session request
    if "end" in user_text.lower() or "quit" in user_text.lower():
        await ctx.send(sender, ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=str(uuid4()),
            content=[EndSessionContent(type="end-session")]
        ))

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
