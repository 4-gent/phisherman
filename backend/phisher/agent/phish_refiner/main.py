"""
Phish Refiner Agent - Hosted on Agentverse
Refines and improves phishing templates for cybersecurity training.
"""

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent, StartSessionContent, EndSessionContent
from datetime import datetime
from uuid import uuid4
import json

# Initialize agent
agent = Agent(name="phish_refiner")
protocol = Protocol()

def txt(s: str) -> ChatMessage:
    """Helper to create text message"""
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=str(uuid4()),
        content=[TextContent(type="text", text=s)]
    )

def refine_email_template(email_type: str = "generic") -> dict:
    """Generate refined and improved phishing email templates"""
    
    templates = {
        "generic": {
            "subject": "⚠️ URGENT ACTION REQUIRED: Account Security Verification Needed",
            "preheader": "Your account security requires immediate attention",
            "html_body": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
        .container { max-width: 650px; margin: 20px auto; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 30px 20px; text-align: center; }
        .content { padding: 40px 30px; background: #ffffff; }
        .button { background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 6px; display: inline-block; margin: 25px 0; font-weight: bold; box-shadow: 0 4px 6px rgba(0,123,255,0.3); }
        .alert { background: #fff3cd; border-left: 5px solid #ffc107; padding: 20px; margin: 25px 0; border-radius: 4px; }
        .highlight { background: #f8f9fa; padding: 20px; border-radius: 6px; margin: 20px 0; border: 1px solid #dee2e6; }
        .footer { background: #f8f9fa; padding: 25px; text-align: center; color: #6c757d; font-size: 13px; border-top: 1px solid #dee2e6; }
        .badge { display: inline-block; background: #dc3545; color: white; padding: 5px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0; font-size: 28px;">Security Alert</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">Account Verification Center</p>
        </div>
        <div class="content">
            <span class="badge">HIGH PRIORITY</span>
            <h2 style="color: #dc3545; margin-top: 10px;">Immediate Action Required</h2>
            
            <p>Dear {{recipient_name}},</p>
            
            <p>Our automated security systems have detected unusual activity associated with your account. To protect your account and prevent unauthorized access, we need to verify your identity immediately.</p>
            
            <div class="alert">
                <strong style="color: #856404;">🔔 IMPORTANT:</strong> Failure to verify your account within <strong>24 hours</strong> will result in temporary account suspension for security purposes.
            </div>
            
            <div class="highlight">
                <h3 style="margin-top: 0; color: #495057;">What We Detected:</h3>
                <ul style="margin: 10px 0;">
                    <li>Login attempt from unrecognized device</li>
                    <li>Location: Unknown origin</li>
                    <li>Time: {{detection_time}}</li>
                </ul>
            </div>
            
            <p>If this activity was authorized by you, please confirm your identity by clicking the secure verification link below:</p>
            
            <p style="text-align: center;">
                <a href="{{verification_link}}" class="button">Verify My Account Now</a>
            </p>
            
            <p style="font-size: 14px; color: #6c757d;">If you did not authorize this activity, please verify your account immediately and contact our security team.</p>
            
            <p>Thank you for helping us keep your account secure.</p>
            
            <p style="margin-top: 30px;">
                <strong>Security Team</strong><br>
                Account Protection Department
            </p>
        </div>
        <div class="footer">
            <p style="margin: 0;">© 2024 Secure Systems Inc. All rights reserved.</p>
            <p style="margin: 5px 0 0 0;">This is an automated security notification. Please do not reply to this email.</p>
            <p style="margin: 10px 0 0 0; font-size: 11px;">This email was sent to {{recipient_email}} | ID: {{security_id}}</p>
        </div>
    </div>
</body>
</html>
            """,
            "plain_text_body": """
URGENT ACTION REQUIRED: Account Security Verification Needed

HIGH PRIORITY

Dear {{recipient_name}},

Our automated security systems have detected unusual activity associated with your account. To protect your account and prevent unauthorized access, we need to verify your identity immediately.

🔔 IMPORTANT: Failure to verify your account within 24 hours will result in temporary account suspension for security purposes.

What We Detected:
- Login attempt from unrecognized device
- Location: Unknown origin
- Time: {{detection_time}}

If this activity was authorized by you, please confirm your identity by visiting the secure verification link below:

{{verification_link}}

If you did not authorize this activity, please verify your account immediately and contact our security team.

Thank you for helping us keep your account secure.

Security Team
Account Protection Department

© 2024 Secure Systems Inc. All rights reserved.
This is an automated security notification.
            """
        }
    }
    
    return templates.get(email_type, templates["generic"])

@protocol.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    
    # Handle session start
    if any(isinstance(c, StartSessionContent) for c in msg.content):
        await ctx.send(sender, txt("Phish Refiner ready. I refine and improve phishing templates for better training effectiveness. How can I help?"))
        return
    
    # Handle session end
    if any(isinstance(c, EndSessionContent) for c in msg.content):
        ctx.logger.info("Session ended")
        return
    
    # Extract user text
    user_text = msg.text() or ""
    ctx.logger.info(f"Received message: {user_text}")
    
    # Generate refined email template
    email = refine_email_template("generic")
    
    # Create response with full email details
    response = f"""
✨ REFINED PHISHING EMAIL TEMPLATE ✨

Subject: {email['subject']}
Preheader: {email['preheader']}

📧 EMAIL CONTENT:
{email['plain_text_body']}

📊 FULL EMAIL DATA:
{json.dumps(email, indent=2)}

✅ Enhanced phishing template ready for cybersecurity training!
📝 Improvements applied:
   - Enhanced visual design with gradients
   - Improved urgency indicators
   - Better structured content layout
   - Professional tone optimization
   - Added security badges and highlights
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
