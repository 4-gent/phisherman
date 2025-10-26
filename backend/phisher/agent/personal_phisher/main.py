"""
Personal Phisher Agent - Hosted on Agentverse
Generates personal information phishing templates for cybersecurity training.
"""

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent, StartSessionContent, EndSessionContent
from datetime import datetime
from uuid import uuid4
import json

# Initialize agent
agent = Agent(name="personal_phisher")
protocol = Protocol()

def txt(s: str) -> ChatMessage:
    """Helper to create text message"""
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=str(uuid4()),
        content=[TextContent(type="text", text=s)]
    )

def generate_personal_email(scenario: str = "security") -> dict:
    """Generate personal information phishing email templates"""
    
    templates = {
        "security": {
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
            <h2>🔒 Account Security Center</h2>
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
        },
        "social": {
            "subject": "Password Reset Request - Account Verification",
            "preheader": "Reset your password",
            "html_body": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #4267B2; color: white; padding: 20px; text-align: center; }
        .content { background: #f9f9f9; padding: 30px; border: 1px solid #ddd; }
        .button { background: #4267B2; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
        .info { background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 15px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Social Media Platform</h2>
        </div>
        <div class="content">
            <h3>Password Reset Request</h3>
            <p>Hello {{recipient_name}},</p>
            <p>We received a request to reset your password. If you made this request, please click the button below.</p>
            
            <div class="info">
                <strong>ℹ️ Note:</strong> This link will expire in 24 hours for security purposes.
            </div>
            
            <p>Click below to reset your password:</p>
            <p style="text-align: center;">
                <a href="{{verification_link}}" class="button">Reset Password</a>
            </p>
            
            <p>If you did not request a password reset, please ignore this email and your password will remain unchanged.</p>
            <p>Thank you for helping us keep your account secure.</p>
        </div>
        <div class="footer">
            <p>© 2024 Social Media Platform. Your privacy matters.</p>
            <p>This is an automated message.</p>
        </div>
    </div>
</body>
</html>
            """,
            "plain_text_body": """
Password Reset Request

Hello {{recipient_name}},

We received a request to reset your password. If you made this request, please click the link below.

ℹ️ NOTE: This link will expire in 24 hours for security purposes.

Reset your password here:
{{verification_link}}

If you did not request a password reset, please ignore this email and your password will remain unchanged.

Thank you for helping us keep your account secure.

© 2024 Social Media Platform. Your privacy matters.
            """
        }
    }
    
    return templates.get(scenario, templates["security"])

@protocol.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    
    # Handle session start
    if any(isinstance(c, StartSessionContent) for c in msg.content):
        await ctx.send(sender, txt("Personal Phisher ready. I generate personal information phishing templates for cybersecurity training. How can I help?"))
        return
    
    # Handle session end
    if any(isinstance(c, EndSessionContent) for c in msg.content):
        ctx.logger.info("Session ended")
        return
    
    # Extract user text
    user_text = msg.text() or ""
    ctx.logger.info(f"Received message: {user_text}")
    
    # Process the request and generate email
    scenario = "security"
    if "social" in user_text.lower() or "facebook" in user_text.lower() or "instagram" in user_text.lower():
        scenario = "social"
    elif "password" in user_text.lower() or "reset" in user_text.lower():
        scenario = "social"
    
    # Generate the email template
    email = generate_personal_email(scenario)
    
    # Create response with full email details
    response = f"""
🔒 GENERATED PERSONAL PHISHING EMAIL 🔒

Subject: {email['subject']}
Preheader: {email['preheader']}

📧 EMAIL CONTENT:
{email['plain_text_body']}

📊 FULL EMAIL DATA:
{json.dumps(email, indent=2)}

✅ Personal phishing template ready for cybersecurity training!
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
