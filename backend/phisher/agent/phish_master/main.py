"""
Phish Master Agent - Hosted on Agentverse
Orchestrator for phishing training email generation.
"""

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent, StartSessionContent, EndSessionContent
from datetime import datetime
from uuid import uuid4
import json

# Initialize agent
agent = Agent(name="phish_master")
protocol = Protocol()

def txt(s: str) -> ChatMessage:
    """Helper to create text message"""
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=str(uuid4()),
        content=[TextContent(type="text", text=s)]
    )

def generate_email_template(domain: str, urgency: str = "high") -> dict:
    """Generate a phishing email template"""
    
    templates = {
        "finance": {
            "subject": "🔴 URGENT: Account Verification Required - Immediate Action Needed",
            "preheader": "Your financial account requires immediate verification",
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
        .button { background: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        .warning { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Account Security Alert</h2>
        </div>
        <div class="content">
            <h3>Immediate Action Required</h3>
            <p>Dear {{recipient_name}},</p>
            <p>We detected unusual activity on your account. For your security, we need to verify your identity immediately.</p>
            
            <div class="warning">
                <strong>⚠️ Security Notice:</strong> Your account will be temporarily restricted if verification is not completed within 24 hours.
            </div>
            
            <p>Please click the button below to verify your account:</p>
            <p style="text-align: center;">
                <a href="{{verification_link}}" class="button">Verify Account Now</a>
            </p>
            
            <p>If you did not attempt to access your account, please contact our security team immediately.</p>
            <p>This is an automated security message. Please do not reply to this email.</p>
        </div>
        <div class="footer">
            <p>© 2024 Financial Services. All rights reserved.</p>
            <p>This email was sent for security purposes only.</p>
        </div>
    </div>
</body>
</html>
            """,
            "plain_text_body": """
SECURITY ALERT - Immediate Action Required

Dear {{recipient_name}},

We detected unusual activity on your account. For your security, we need to verify your identity immediately.

⚠️ WARNING: Your account will be temporarily restricted if verification is not completed within 24 hours.

Please visit this link to verify your account:
{{verification_link}}

If you did not attempt to access your account, please contact our security team immediately.

This is an automated security message. Please do not reply to this email.

© 2024 Financial Services. All rights reserved.
            """
        },
        "health": {
            "subject": "Important: Medical Records Update Required",
            "preheader": "Your health information needs verification",
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
            <h2>Healthcare Provider</h2>
        </div>
        <div class="content">
            <h3>Patient Records Update</h3>
            <p>Dear {{recipient_name}},</p>
            <p>Your healthcare provider needs to update your medical records. This is required to ensure the accuracy of your health information.</p>
            
            <div class="info">
                <strong>📋 Record Update:</strong> Please review and confirm your information to maintain access to your patient portal.
            </div>
            
            <p>Click below to access your patient portal and update your records:</p>
            <p style="text-align: center;">
                <a href="{{verification_link}}" class="button">Update Medical Records</a>
            </p>
            
            <p>This update should take less than 5 minutes. Please complete it at your earliest convenience.</p>
            <p>If you have questions, please contact our patient support line.</p>
        </div>
        <div class="footer">
            <p>© 2024 Healthcare Provider. HIPAA Compliant.</p>
            <p>This is a secure communication.</p>
        </div>
    </div>
</body>
</html>
            """,
            "plain_text_body": """
Patient Records Update Required

Dear {{recipient_name}},

Your healthcare provider needs to update your medical records. This is required to ensure the accuracy of your health information.

📋 RECORD UPDATE: Please review and confirm your information to maintain access to your patient portal.

Please visit this link to update your records:
{{verification_link}}

This update should take less than 5 minutes. Please complete it at your earliest convenience.

If you have questions, please contact our patient support line.

© 2024 Healthcare Provider. HIPAA Compliant.
            """
        },
        "personal": {
            "subject": "Security Alert: Unusual Login Activity Detected",
            "preheader": "Secure your account immediately",
            "html_body": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #ff6600; color: white; padding: 20px; text-align: center; }
        .content { background: #f9f9f9; padding: 30px; border: 1px solid #ddd; }
        .button { background: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        .alert { background: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Account Security Center</h2>
        </div>
        <div class="content">
            <h3>⚠️ Unusual Activity Detected</h3>
            <p>Dear {{recipient_name}},</p>
            <p>We noticed a login attempt from an unrecognized device in your account. If this was you, no action is needed.</p>
            
            <div class="alert">
                <strong>🔒 Security Alert:</strong> A new device signed in to your account from an unfamiliar location.
            </div>
            
            <p><strong>Login Details:</strong></p>
            <ul>
                <li>Location: Unknown</li>
                <li>Device: Unknown Device</li>
                <li>Time: Recent</li>
            </ul>
            
            <p>If this wasn't you, please secure your account immediately:</p>
            <p style="text-align: center;">
                <a href="{{verification_link}}" class="button">Secure Account Now</a>
            </p>
            
            <p>We recommend changing your password immediately if you did not authorize this login.</p>
        </div>
        <div class="footer">
            <p>© 2024 Account Security Center. Protecting your privacy.</p>
            <p>This is an automated security notification.</p>
        </div>
    </div>
</body>
</html>
            """,
            "plain_text_body": """
Unusual Activity Detected - Security Alert

Dear {{recipient_name}},

We noticed a login attempt from an unrecognized device in your account. If this was you, no action is needed.

🔒 SECURITY ALERT: A new device signed in to your account from an unfamiliar location.

Login Details:
- Location: Unknown
- Device: Unknown Device
- Time: Recent

If this wasn't you, please secure your account immediately:
{{verification_link}}

We recommend changing your password immediately if you did not authorize this login.

© 2024 Account Security Center. Protecting your privacy.
            """
        }
    }
    
    return templates.get(domain, templates["finance"])

@protocol.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    
    # Handle session start
    if any(isinstance(c, StartSessionContent) for c in msg.content):
        await ctx.send(sender, txt("Phish Master ready. I coordinate phishing template generation across domain agents. How can I help?"))
        return
    
    # Handle session end
    if any(isinstance(c, EndSessionContent) for c in msg.content):
        ctx.logger.info("Session ended")
        return
    
    # Extract user text
    user_text = msg.text() or ""
    ctx.logger.info(f"Received message: {user_text}")
    
    # Process the request and generate email content
    domain = None
    if "finance" in user_text.lower():
        domain = "finance"
    elif "health" in user_text.lower() or "medical" in user_text.lower():
        domain = "health"
    elif "personal" in user_text.lower():
        domain = "personal"
    
    if domain:
        # Generate the email template
        email = generate_email_template(domain)
        
        # Create response with full email details
        response = f"""
🎯 GENERATED PHISHING EMAIL TEMPLATE 🎯

Subject: {email['subject']}
Preheader: {email['preheader']}

📧 EMAIL CONTENT:
{email['plain_text_body']}

📊 FULL EMAIL DATA:
{json.dumps(email, indent=2)}

✅ Template ready for cybersecurity training!
"""
        await ctx.send(sender, txt(response))
    elif "refine" in user_text.lower():
        response = "I'll send the template to Phish Refiner for optimization and improvement."
        await ctx.send(sender, txt(response))
    else:
        response = "I coordinate phishing template generation. Domains: finance, health, personal. Say 'generate finance template' or similar."
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
