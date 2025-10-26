"""
Health Phisher Agent - Hosted on Agentverse
Generates healthcare phishing templates for cybersecurity training.
"""

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent, StartSessionContent, EndSessionContent
from datetime import datetime
from uuid import uuid4
import json

# Initialize agent
agent = Agent(name="health_phisher")
protocol = Protocol()

def txt(s: str) -> ChatMessage:
    """Helper to create text message"""
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=str(uuid4()),
        content=[TextContent(type="text", text=s)]
    )

def generate_health_email(scenario: str = "medical") -> dict:
    """Generate healthcare phishing email templates"""
    
    templates = {
        "medical": {
            "subject": "Important: Medical Records Update Required",
            "preheader": "Verify your health information",
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
        .button { background: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        .info { background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 15px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🏥 Patient Portal</h2>
        </div>
        <div class="content">
            <h3>Medical Records Update Required</h3>
            <p>Dear {{recipient_name}},</p>
            <p>Your healthcare provider needs to update your medical records to ensure accuracy and continued access to your patient portal.</p>
            
            <div class="info">
                <strong>📋 Action Required:</strong> Please review and confirm your medical information to maintain portal access.
            </div>
            
            <p>Click below to access your patient portal:</p>
            <p style="text-align: center;">
                <a href="{{verification_link}}" class="button">Update Medical Records</a>
            </p>
            
            <p>This update should take less than 5 minutes. Your information is protected under HIPAA regulations.</p>
            <p>If you have questions, please contact our patient support line.</p>
        </div>
        <div class="footer">
            <p>© 2024 Healthcare Provider. HIPAA Compliant.</p>
            <p>Your health information is secure and confidential.</p>
        </div>
    </div>
</body>
</html>
            """,
            "plain_text_body": """
Medical Records Update Required

Dear {{recipient_name}},

Your healthcare provider needs to update your medical records to ensure accuracy and continued access to your patient portal.

📋 ACTION REQUIRED: Please review and confirm your medical information to maintain portal access.

Please visit this link to update your records:
{{verification_link}}

This update should take less than 5 minutes. Your information is protected under HIPAA regulations.

If you have questions, please contact our patient support line.

© 2024 Healthcare Provider. HIPAA Compliant.
            """
        },
        "insurance": {
            "subject": "Health Insurance Coverage Update - Verification Needed",
            "preheader": "Your coverage requires verification",
            "html_body": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #28a745; color: white; padding: 20px; text-align: center; }
        .content { background: #f9f9f9; padding: 30px; border: 1px solid #ddd; }
        .button { background: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        .alert { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🏥 Health Insurance</h2>
        </div>
        <div class="content">
            <h3>Coverage Verification Required</h3>
            <p>Dear {{recipient_name}},</p>
            <p>We need to verify your health insurance coverage to ensure continued benefits.</p>
            
            <div class="alert">
                <strong>⚠️ Important:</strong> Please verify your coverage details within 7 days to avoid any interruption in benefits.
            </div>
            
            <p>Click below to verify your coverage:</p>
            <p style="text-align: center;">
                <a href="{{verification_link}}" class="button">Verify Coverage</a>
            </p>
            
            <p>This verification helps us maintain accurate records and ensure you receive the benefits you're entitled to.</p>
            <p>Thank you for your prompt attention.</p>
        </div>
        <div class="footer">
            <p>© 2024 Health Insurance. Protecting your health.</p>
            <p>Secure and confidential.</p>
        </div>
    </div>
</body>
</html>
            """,
            "plain_text_body": """
Health Insurance Coverage Update

Dear {{recipient_name}},

We need to verify your health insurance coverage to ensure continued benefits.

⚠️ IMPORTANT: Please verify your coverage details within 7 days to avoid any interruption in benefits.

Please verify your coverage here:
{{verification_link}}

This verification helps us maintain accurate records and ensure you receive the benefits you're entitled to.

Thank you for your prompt attention.

© 2024 Health Insurance. Protecting your health.
            """
        }
    }
    
    return templates.get(scenario, templates["medical"])

@protocol.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    
    # Handle session start
    if any(isinstance(c, StartSessionContent) for c in msg.content):
        await ctx.send(sender, txt("Health Phisher ready. I generate healthcare phishing templates for cybersecurity training. How can I help?"))
        return
    
    # Handle session end
    if any(isinstance(c, EndSessionContent) for c in msg.content):
        ctx.logger.info("Session ended")
        return
    
    # Extract user text
    user_text = msg.text() or ""
    ctx.logger.info(f"Received message: {user_text}")
    
    # Process the request and generate email
    scenario = "medical"
    if "insurance" in user_text.lower() or "coverage" in user_text.lower():
        scenario = "insurance"
    elif "appointment" in user_text.lower() or "prescription" in user_text.lower():
        scenario = "medical"
    
    # Generate the email template
    email = generate_health_email(scenario)
    
    # Create response with full email details
    response = f"""
🏥 GENERATED HEALTHCARE PHISHING EMAIL 🏥

Subject: {email['subject']}
Preheader: {email['preheader']}

📧 EMAIL CONTENT:
{email['plain_text_body']}

📊 FULL EMAIL DATA:
{json.dumps(email, indent=2)}

✅ Healthcare phishing template ready for cybersecurity training!
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
