#!/usr/bin/env python3
"""
Phisherman Terminal CLI - Safe Educational Tool
Production-ready terminal interface for cybersecurity training template generation.

SAFETY: This tool generates ONLY sanitized, non-actionable educational content.
NO real phishing emails, links, or sendable content are produced.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import uuid

# Create necessary directories
os.makedirs("diagnostics/templates", exist_ok=True)
os.makedirs("diagnostics", exist_ok=True)

# Global state
current_template: Optional[Dict[str, Any]] = None
template_history: list = []

# Agent configuration
AGENTS = {
    "1": {
        "name": "phish_master",
        "display": "🎯 Phish Master (Orchestrator)",
        "description": "Coordinates phishing template generation across domain agents"
    },
    "2": {
        "name": "finance_phisher",
        "display": "💰 Finance Phisher",
        "description": "Generates financial phishing templates"
    },
    "3": {
        "name": "health_phisher",
        "display": "🏥 Health Phisher",
        "description": "Generates healthcare phishing templates"
    },
    "4": {
        "name": "personal_phisher",
        "display": "👤 Personal Phisher",
        "description": "Generates personal information phishing templates"
    },
    "5": {
        "name": "phish_refiner",
        "display": "✨ Phish Refiner",
        "description": "Refines and improves phishing templates"
    }
}

def log_chat(timestamp: str, agent: str, user_input: str, response: str):
    """Log chat interactions"""
    log_entry = f"[{timestamp}] {agent}: {user_input} -> {response}\n"
    with open("diagnostics/chat_history.txt", "a") as f:
        f.write(log_entry)

def log_refusal(reason: str, user_input: str):
    """Log safety refusals"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "reason": reason,
        "user_input": user_input,
        "type": "safety_refusal"
    }
    with open("diagnostics/refusals.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"\n⚠️  SAFETY REFUSAL: {reason}")
    print(f"   For security reasons, I cannot generate real phishing content.")
    print(f"   Instead, here's what I can provide:")
    print(f"   - Sanitized scenario descriptions")
    print(f"   - Red flag identification training")
    print(f"   - Placeholder templates")
    print(f"   - Educational safety notes")

def check_safety(user_input: str) -> bool:
    """Check if user input requests unsafe content"""
    unsafe_patterns = [
        "chase bank", "bank of america", "wells fargo", "citi", "real link",
        "actual email", "send this", "click here", "http://", "https://",
        "@", ".com", ".org", "phishing", "steal", "hack"
    ]
    
    user_lower = user_input.lower()
    for pattern in unsafe_patterns:
        if pattern in user_lower:
            return False
    return True

def generate_safe_template(domain: str) -> Dict[str, Any]:
    """Generate a safe, sanitized template"""
    template_id = f"{domain.upper()[:3]}{uuid.uuid4().hex[:8]}"
    
    templates = {
        "finance": {
            "template_id": template_id,
            "scenario_title": "Financial Account Verification Exercise",
            "sanitized_description": "This template demonstrates common tactics used in financial phishing: urgent account verification requests, payment information requests, and security alerts. The template includes typical red flags like urgent action requirements and requests for sensitive information.",
            "subject": "[FINANCIAL_INSTITUTION_NAME] Account Verification Required",
            "preheader": "Action required to secure your account",
            "html_body": """<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
<div style="max-width: 600px; margin: 0 auto;">
<h2 style="color: #333;">Account Verification Required</h2>
<p>Dear [Name],</p>
<p>We have detected unusual activity on your account and need to verify your identity immediately to protect your financial information.</p>
<p><strong>Security Alert:</strong> Multiple failed login attempts were detected from an unknown location.</p>
<p>To secure your account, please verify your identity by clicking the button below:</p>
<p style="text-align: center; margin: 30px 0;">
<a href="[TRAINING_REDIRECT_LINK]" style="background-color: #0066cc; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Account</a>
</p>
<p style="color: #666; font-size: 12px;">If you did not attempt to access your account, please contact our security team immediately.</p>
<p>Best regards,<br>Security Team<br>[FINANCIAL_INSTITUTION_NAME]</p>
</div>
</body>
</html>""",
            "plain_text_body": """Account Verification Required

Dear [Name],

We have detected unusual activity on your account and need to verify your identity immediately to protect your financial information.

Security Alert: Multiple failed login attempts were detected from an unknown location.

To secure your account, please verify your identity by visiting:
[TRAINING_REDIRECT_LINK]

If you did not attempt to access your account, please contact our security team immediately.

Best regards,
Security Team
[FINANCIAL_INSTITUTION_NAME]""",
            "red_flags": [
                "Requests immediate action",
                "Asks for account verification",
                "Contains urgency language",
                "May request sensitive information",
                "Email sender may be spoofed"
            ],
            "training_objectives": [
                "Identify urgency manipulation tactics",
                "Recognize account verification scams",
                "Understand social engineering in financial context",
                "Practice detecting red flags"
            ],
            "urgency_score": 8,
            "safety_notes": [
                "This is an educational template only",
                "Contains NO real links or actionable content",
                "Intended for cybersecurity awareness training",
                "Should NEVER be used for actual phishing"
            ]
        },
        "health": {
            "template_id": template_id,
            "scenario_title": "Healthcare Information Update Exercise",
            "sanitized_description": "This template illustrates healthcare phishing tactics: medical records updates, insurance verification, and health information requests. Common patterns include urgency about health coverage and requests for personal medical data.",
            "subject": "[HEALTHCARE_PROVIDER] Medical Records Update Required",
            "preheader": "Your health information needs attention",
            "html_body": """<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
<div style="max-width: 600px; margin: 0 auto;">
<h2 style="color: #0066cc;">Medical Records Update</h2>
<p>Dear [Name],</p>
<p>Your healthcare provider account requires immediate verification to ensure your medical records are secure and up to date.</p>
<p><strong>Important:</strong> We need to verify your health insurance information to maintain coverage.</p>
<p>Please update your medical records by clicking below:</p>
<p style="text-align: center; margin: 30px 0;">
<a href="[TRAINING_REDIRECT_LINK]" style="background-color: #0066cc; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Update Medical Records</a>
</p>
<p style="color: #666; font-size: 12px;">This is required to maintain your health coverage.</p>
<p>Best regards,<br>Patient Services<br>[HEALTHCARE_PROVIDER]</p>
</div>
</body>
</html>""",
            "plain_text_body": """Medical Records Update

Dear [Name],

Your healthcare provider account requires immediate verification to ensure your medical records are secure and up to date.

Important: We need to verify your health insurance information to maintain coverage.

Please update your medical records by visiting:
[TRAINING_REDIRECT_LINK]

This is required to maintain your health coverage.

Best regards,
Patient Services
[HEALTHCARE_PROVIDER]""",
            "red_flags": [
                "Requests health information verification",
                "Mentions medical records",
                "Uses urgency about health coverage",
                "May request personal medical data",
                "Healthcare institution branding may be spoofed"
            ],
            "training_objectives": [
                "Identify healthcare-specific phishing tactics",
                "Recognize medical data scam patterns",
                "Understand social engineering in healthcare context",
                "Practice detecting healthcare phishing red flags"
            ],
            "urgency_score": 7,
            "safety_notes": [
                "This is an educational template only",
                "Contains NO real links or actionable content",
                "Intended for cybersecurity awareness training",
                "Should NEVER be used for actual phishing"
            ]
        },
        "personal": {
            "template_id": template_id,
            "scenario_title": "Personal Account Security Exercise",
            "sanitized_description": "This template demonstrates personal information phishing: social media account alerts, identity verification requests, and security warnings. Typical patterns include detected suspicious activity and requests for identity confirmation.",
            "subject": "[SERVICE_NAME] Security Alert",
            "preheader": "Unusual activity detected on your account",
            "html_body": """<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
<div style="max-width: 600px; margin: 0 auto;">
<h2 style="color: #dc3545;">🚨 Security Alert</h2>
<p>Dear [Name],</p>
<p>We detected unusual activity on your account. Someone attempted to access your account from an unrecognized device.</p>
<p><strong>Alert Details:</strong></p>
<ul>
<li>Location: Unknown IP Address</li>
<li>Time: [DATE_TIME]</li>
<li>Status: Login Attempt Failed</li>
</ul>
<p>To protect your account, please verify your identity immediately:</p>
<p style="text-align: center; margin: 30px 0;">
<a href="[TRAINING_REDIRECT_LINK]" style="background-color: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Identity</a>
</p>
<p style="color: #666; font-size: 12px;">If this wasn't you, secure your account now.</p>
<p>Best regards,<br>Security Team<br>[SERVICE_NAME]</p>
</div>
</body>
</html>""",
            "plain_text_body": """Security Alert

Dear [Name],

We detected unusual activity on your account. Someone attempted to access your account from an unrecognized device.

Alert Details:
- Location: Unknown IP Address
- Time: [DATE_TIME]
- Status: Login Attempt Failed

To protect your account, please verify your identity immediately:
[TRAINING_REDIRECT_LINK]

If this wasn't you, secure your account now.

Best regards,
Security Team
[SERVICE_NAME]""",
            "red_flags": [
                "Reports suspicious account activity",
                "Requests identity verification",
                "Creates sense of urgency",
                "May request personal information",
                "Service branding may be spoofed"
            ],
            "training_objectives": [
                "Identify social engineering in personal contexts",
                "Recognize security alert scams",
                "Understand identity theft tactics",
                "Practice detecting personal phishing red flags"
            ],
            "urgency_score": 9,
            "safety_notes": [
                "This is an educational template only",
                "Contains NO real links or actionable content",
                "Intended for cybersecurity awareness training",
                "Should NEVER be used for actual phishing"
            ]
        }
    }
    
    return templates.get(domain, templates["finance"])

def print_header():
    """Print application header"""
    print("\n" + "="*70)
    print("🎓 Phisherman Terminal CLI - Educational Cybersecurity Tool")
    print("="*70)
    print("⚠️  SAFETY NOTICE: This tool generates ONLY sanitized, educational content.")
    print("    NO real phishing emails or actionable content will be produced.\n")

def print_agents():
    """Print available agents"""
    print("📋 Available Agents:")
    print("-"*70)
    for key, agent in AGENTS.items():
        print(f"{key}. {agent['display']}")
        print(f"   {agent['description']}")
    print("-"*70)

def print_help():
    """Print help information"""
    print("\n" + "="*70)
    print("📖 Commands")
    print("="*70)
    print("\n🎯 Navigation:")
    print("   • 1-5 or agent name    - Select an agent")
    print("   • help                 - Show this help")
    print("   • back                 - Return to agent selection")
    print("   • quit / exit          - Exit application")
    print("\n📄 Template Commands:")
    print("   • show                 - Display current template")
    print("   • refine               - Open refinement chat")
    print("   • export               - Save template to file")
    print("\n✨ Refinement Commands:")
    print("   • improve_tone:<style> - Change tone (formal/casual/urgent)")
    print("   • increase_urgency     - Raise urgency level")
    print("   • decrease_urgency     - Lower urgency level")
    print("   • focus_on_red_flags   - Highlight red flags")
    print("   • done                 - Complete refinement")
    print("\n⚠️  Safety:")
    print("   • Real phishing content will be refused")
    print("   • Only sanitized, educational content is generated")
    print("   • All refusals are logged for audit")
    print("="*70)

def export_template(template: Dict[str, Any]):
    """Export template to JSON file"""
    if not template:
        print("❌ No template to export")
        return
    
    filename = f"diagnostics/templates/{template['template_id']}.json"
    with open(filename, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"\n✅ Template exported to: {filename}")
    print(f"   Template ID: {template['template_id']}")

def display_template(template: Dict[str, Any]):
    """Display template in readable format"""
    print("\n" + "="*70)
    print("📄 TEMPLATE")
    print("="*70)
    print(f"\n🆔 Template ID: {template['template_id']}")
    print(f"📝 Scenario: {template['scenario_title']}")
    print(f"\n📖 Description:")
    print(f"   {template['sanitized_description']}")
    
    # Display actual email content
    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📧 EMAIL CONTENT")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    print(f"\n📝 Subject: {template.get('subject', 'N/A')}")
    print(f"🔔 Preheader: {template.get('preheader', 'N/A')}")
    
    print(f"\n🌐 HTML Body:")
    html_body = template.get('html_body', 'N/A')
    # Show HTML in a readable format
    print(html_body)
    
    print(f"\n📝 Plain Text Body:")
    print(template.get('plain_text_body', 'N/A'))
    
    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 TEMPLATE METADATA")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    print(f"\n🚩 Red Flags:")
    for flag in template['red_flags']:
        print(f"   • {flag}")
    print(f"\n🎯 Training Objectives:")
    for obj in template['training_objectives']:
        print(f"   • {obj}")
    print(f"\n⚠️  Urgency Score: {template['urgency_score']}/10")
    print(f"\n✅ Safety Notes:")
    for note in template['safety_notes']:
        print(f"   • {note}")
    print("="*70)

def refine_template(template: Dict[str, Any], instruction: str) -> Dict[str, Any]:
    """Apply refinement to template"""
    refined = template.copy()
    instruction_lower = instruction.lower()
    
    if instruction_lower.startswith("improve_tone:"):
        tone = instruction.split(":")[1].strip()
        refined["sanitized_description"] += f" Tone has been adjusted to {tone}."
        # Update actual email content based on tone
        if tone == "urgent":
            refined["subject"] = "URGENT: " + refined.get("subject", "")
            refined["html_body"] = refined["html_body"].replace("<p>Dear", "<p><strong style='color: #dc3545;'>ACTION REQUIRED</strong></p><p>Dear")
            refined["plain_text_body"] = "ACTION REQUIRED\n\n" + refined["plain_text_body"]
        elif tone == "formal":
            refined["html_body"] = refined["html_body"].replace("<p>Dear", "<p>Dear Valued Customer,<br><br>")
            refined["plain_text_body"] = refined["plain_text_body"].replace("Dear", "Dear Valued Customer,")
        return refined
    
    if "increase_urgency" in instruction_lower:
        refined["urgency_score"] = min(10, refined["urgency_score"] + 1)
        refined["subject"] = "URGENT: " + refined.get("subject", "")
        refined["html_body"] = refined["html_body"].replace("<p>Dear", "<p><strong style='color: #dc3545;'>⚠️ URGENT ACTION REQUIRED</strong></p><p>Dear")
        refined["plain_text_body"] = "⚠️ URGENT ACTION REQUIRED\n\n" + refined["plain_text_body"]
        refined["sanitized_description"] += " Urgency has been increased."
        return refined
    
    if "decrease_urgency" in instruction_lower:
        refined["urgency_score"] = max(0, refined["urgency_score"] - 1)
        refined["subject"] = refined["subject"].replace("URGENT: ", "")
        refined["html_body"] = refined["html_body"].replace("<p><strong style='color: #dc3545;'>⚠️ URGENT ACTION REQUIRED</strong></p><p>", "<p>")
        refined["plain_text_body"] = refined["plain_text_body"].replace("⚠️ URGENT ACTION REQUIRED\n\n", "")
        refined["sanitized_description"] += " Urgency has been decreased."
        return refined
    
    if "focus_on_red_flags" in instruction_lower:
        refined["red_flags"].append("Enhanced red flag visibility for training")
        refined["html_body"] = refined["html_body"].replace("</div>", "<p style='background: #fff3cd; padding: 10px; border-left: 3px solid #ffc107;'>⚠️ Important: Please verify the sender's authenticity before clicking any links.</p></div>")
        refined["plain_text_body"] += "\n\n⚠️ Important: Please verify the sender's authenticity before clicking any links."
        refined["sanitized_description"] += " Red flags have been highlighted."
        return refined
    
    return refined

def main():
    """Main application loop"""

    global current_template

    if choice in AGENTS:
        agent = AGENTS[choice]
        chat_with_agent(agent)

    global current_template
    
    print_header()
    
    while True:
        print_agents()
        
        choice = input("\nSelect an agent (1-5), 'help', or 'quit': ").strip().lower()
        
        if choice in ['q', 'quit', 'exit']:
            print("\n👋 Thanks for using Phisherman Terminal CLI!")
            print("   Remember: This tool is for educational purposes only.")
            break
        
        if choice == 'help':
            print_help()
            continue
        
        if choice in AGENTS:
            agent = AGENTS[choice]
            chat_with_agent(agent)
        else:
            print("\n❌ Invalid choice. Type 'help' for available commands.")

def chat_with_agent(agent: Dict[str, Any]):
    """Chat with selected agent"""
    global current_template
    
    # print(f"\n{'='*70}")
    # print(f"💬 Chatting with {agent['display']}")
    # print(f"{'='*70}")
    
    # Handle different agent types
    # if agent['name'] == 'phish_master':
    #     orchestrate_flow()
    # elif agent['name'] == 'phish_refiner':
    #     refiner_chat()
    # else:
    #     print(f"\n{agent['display']}: Please use Phish Master to generate templates.")
    #     print("   Type 'back' to return to main menu.")

    try:
        if(agent['name'] == 'phish_master'):
            orchestrate_flow()
        elif agent['name'] == 'phish_refiner':
            refiner_chat()
    except Exception as e:
        print("Error in chat_with_agent", e)

def orchestrate_flow(choice):
    """Handle Phish Master orchestration flow"""
    global current_template
    
    # print("\n🎯 Phish Master: I coordinate template generation.")
    # print("\n📋 Choose a domain:")
    # print("   1. Finance")
    # print("   2. Health")
    # print("   3. Personal")
    # print("\nOr type 'back' to return.")
    # print("-"*70)
    
    if choice in ['1', 'financial']:
        current_template = generate_safe_template("finance")
        return current_template
        # display_template(current_template)
    elif choice in ['2', 'health']:
        current_template = generate_safe_template("health")
        return current_template
        # display_template(current_template)
    elif choice in ['3', 'personal']:
        current_template = generate_safe_template("personal")
        return current_template
        # display_template(current_template)
    else:
        print("❌ Invalid choice. Enter 1, 2, or 3.")

    # while True:
    #     choice = input("\nYour choice: ").strip().lower()
        
    #     if choice == 'back':
    #         break
        
    #     if choice in ['1', 'finance']:
    #         current_template = generate_safe_template("finance")
    #         print(current_template)
    #         # display_template(current_template)
    #     elif choice in ['2', 'health']:
    #         current_template = generate_safe_template("health")
    #         print(current_template)
    #         # display_template(current_template)
    #     elif choice in ['3', 'personal']:
    #         current_template = generate_safe_template("personal")
    #         print(current_template)
    #         # display_template(current_template)
    #     else:
    #         print("❌ Invalid choice. Enter 1, 2, or 3.")
    #         continue
        
    #     # Offer refinement
    #     refine_choice = input("\n💡 Type 'refine' to improve this template, or 'back': ").strip().lower()
    #     if refine_choice == 'refine':
    #         refiner_chat()
    #     else:
    #         break

def refiner_chat():
    """Interactive refinement chat"""
    global current_template
    
    if not current_template:
        print("\n❌ No template available. Generate one first using Phish Master.")
        return
    
    print(f"\n{'='*70}")
    print(f"✨ Chatting with Phish Refiner")
    print(f"{'='*70}")
    print("Refinement commands: improve_tone:<style>, increase_urgency, decrease_urgency,")
    print("focus_on_red_flags, show, export, done")
    print("-"*70)
    
    print("\n💡 You can refine:")
    print("   • Tone (formal/casual/urgent)")
    print("   • Urgency level")
    print("   • Red flag visibility")
    print("   • Email content")
    print("-"*70)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['done', 'exit', 'back']:
            print("\n✅ Refinement complete!")
            break
        
        if user_input.lower() == 'show':
            display_template(current_template)
            continue
        
        if user_input.lower() == 'export':
            export_template(current_template)
            continue
        
        # Safety check
        if not check_safety(user_input):
            log_refusal("Attempted to request real phishing content", user_input)
            continue
        
        # Apply refinement
        refined = refine_template(current_template, user_input)
        if refined != current_template:
            current_template = refined
            print("\n✅ Refinement applied!")
            print(f"   Template updated: {current_template['template_id']}")
            print(f"   Changes made to: email content and metadata")
        else:
            print("\n⚠️  Command not recognized. Type 'done' for help.")

# if __name__ == "__main__":
#     main()

