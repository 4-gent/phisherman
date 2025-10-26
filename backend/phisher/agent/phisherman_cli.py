#!/usr/bin/env python3
"""
Phisherman Terminal CLI - Safe Educational Tool
Production-ready terminal interface for cybersecurity training template generation.

SAFETY: This tool generates ONLY sanitized, non-actionable educational content.
NO real phishing emails, links, or sendable content are produced.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import uuid
import re

# Add backend directory to path for trainer import
backend_path = os.path.join(os.path.dirname(__file__), '..', '..')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

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
    },
    "6": {
        "name": "teacher",
        "display": "🎓 Teacher (Phishing Awareness)",
        "description": "Educational lessons on phishing detection and prevention"
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
    """Apply refinement to template using natural-language instructions.

    This function understands simple NL commands like:
      - "make it more urgent" / "increase urgency"
      - "make it less urgent" / "decrease urgency"
      - "make tone:formal" / "make tone:casual" / "make tone:urgent"
      - "shorten" / "make concise"
      - "lengthen" / "expand"
      - "highlight red flags" / "focus on red flags"
      - "add bullet points"
      - "simplify language"
      - free-form instructions are applied with safe, heuristic edits to html_body and plain_text_body

    Always returns a new dict (does not mutate the input).
    """
    refined = template.copy()
    # make shallow copies of mutable fields to avoid accidental shared-state
    refined["html_body"] = str(refined.get("html_body", ""))
    refined["plain_text_body"] = str(refined.get("plain_text_body", ""))
    refined["sanitized_description"] = str(refined.get("sanitized_description", ""))
    refined["red_flags"] = list(refined.get("red_flags", []))
    refined["training_objectives"] = list(refined.get("training_objectives", []))
    urgency = int(refined.get("urgency_score", 0))

    instr = (instruction or "").strip()
    instr_low = instr.lower()

    def add_urgent_banner():
        nonlocal refined
        if "⚠️ URGENT ACTION REQUIRED" not in refined["html_body"]:
            refined["html_body"] = refined["html_body"].replace(
                "<div style=\"max-width: 600px; margin: 0 auto;\">",
                "<div style=\"max-width: 600px; margin: 0 auto;\"><p style='color:#a71d2a;font-weight:700;'>⚠️ URGENT ACTION REQUIRED</p>"
            )
        if "⚠️ URGENT ACTION REQUIRED" not in refined["plain_text_body"]:
            refined["plain_text_body"] = "⚠️ URGENT ACTION REQUIRED\n\n" + refined["plain_text_body"]

    def remove_urgent_banner():
        nonlocal refined
        refined["html_body"] = refined["html_body"].replace("⚠️ URGENT ACTION REQUIRED", "")
        refined["plain_text_body"] = refined["plain_text_body"].replace("⚠️ URGENT ACTION REQUIRED\n\n", "")

    def shorten_text(text: str, max_sentences: int = 2) -> str:
        # naive sentence splitter
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        short = " ".join(sentences[:max_sentences])
        return short if short else text

    def simplify_text(text: str) -> str:
        # dumb simplifications for common phrases
        replacements = {
            "please verify your identity": "please confirm your identity",
            "we have detected unusual activity on your account": "we noticed activity on your account",
            "we need to verify": "we need to check",
            "immediately": "as soon as possible",
            "to protect your account": "to keep your account safe"
        }
        out = text
        for k, v in replacements.items():
            out = re.sub(re.escape(k), v, out, flags=re.IGNORECASE)
        return out

    changed = False

    # Tone commands
    if "improve_tone:" in instr_low or instr_low.startswith("make tone") or "tone:" in instr_low:
        # parse tone
        tone_match = re.search(r"(?:improve_tone:|tone:|make tone[:\s])\s*([a-zA-Z]+)", instr_low)
        tone = (tone_match.group(1).strip()) if tone_match else None
        if tone:
            if tone in ("urgent", "increase_urgency", "urgent_tone"):
                urgency = min(10, urgency + 2)
                refined["subject"] = "URGENT: " + refined.get("subject", "")
                add_urgent_banner()
                refined["sanitized_description"] += f" Tone set to {tone}."
            elif tone in ("formal", "formal_tone"):
                refined["html_body"] = refined["html_body"].replace("<p>Dear", "<p>Dear Valued Customer,<br><br>")
                refined["plain_text_body"] = refined["plain_text_body"].replace("Dear", "Dear Valued Customer,")
                refined["sanitized_description"] += " Tone adjusted to formal."
            elif tone in ("casual", "friendly", "informal"):
                refined["html_body"] = refined["html_body"].replace("<p>Dear", "<p>Hi there,")
                refined["plain_text_body"] = refined["plain_text_body"].replace("Dear [Name],", "Hi there,")
                refined["sanitized_description"] += " Tone adjusted to casual/friendly."
            changed = True

    # Increase / decrease urgency
    if "increase_urgency" in instr_low or "more urgent" in instr_low or "make it more urgent" in instr_low:
        urgency = min(10, urgency + 1)
        refined["subject"] = "URGENT: " + refined.get("subject", "")
        add_urgent_banner()
        refined["sanitized_description"] += " Urgency increased."
        changed = True

    if "decrease_urgency" in instr_low or "less urgent" in instr_low or "make it less urgent" in instr_low:
        urgency = max(0, urgency - 1)
        refined["subject"] = refined.get("subject", "").replace("URGENT: ", "")
        remove_urgent_banner()
        refined["sanitized_description"] += " Urgency decreased."
        changed = True

    # Shorten / lengthen
    if "shorten" in instr_low or "concise" in instr_low or "make it shorter" in instr_low:
        refined["html_body"] = shorten_text(refined["html_body"], max_sentences=2)
        refined["plain_text_body"] = shorten_text(refined["plain_text_body"], max_sentences=2)
        refined["sanitized_description"] += " Content shortened for brevity."
        changed = True

    if "lengthen" in instr_low or "expand" in instr_low or "make it longer" in instr_low:
        # duplicate key sentences as a naive expansion
        refined["html_body"] = refined["html_body"] + "<p>We emphasize this point to aid training and clarity.</p>"
        refined["plain_text_body"] = refined["plain_text_body"] + "\n\nWe emphasize this point to aid training and clarity."
        refined["sanitized_description"] += " Content expanded."
        changed = True

    # Simplify language
    if "simplify" in instr_low or "plain language" in instr_low:
        refined["html_body"] = simplify_text(refined["html_body"])
        refined["plain_text_body"] = simplify_text(refined["plain_text_body"])
        refined["sanitized_description"] += " Language simplified."
        changed = True

    # Highlight red flags
    if "focus_on_red_flags" in instr_low or "highlight red flags" in instr_low or "show red flags" in instr_low:
        if "Enhanced red flag visibility for training" not in refined["red_flags"]:
            refined["red_flags"].append("Enhanced red flag visibility for training")
        # insert a visible note in the html body
        if "Important: Please verify the sender's authenticity" not in refined["html_body"]:
            refined["html_body"] = refined["html_body"].replace(
                "</div>",
                "<p style='background:#fff3cd;padding:10px;border-left:3px solid #ffc107;'>⚠️ Important: Please verify the sender's authenticity before acting on this message.</p></div>"
            )
        refined["plain_text_body"] += "\n\n⚠️ Important: Please verify the sender's authenticity before acting on this message."
        refined["sanitized_description"] += " Red flags highlighted."
        changed = True

    # Add bullet points helper
    if "add bullet" in instr_low or "bullet points" in instr_low or "make a list" in instr_low:
        # try to find a paragraph to convert into bullets (naive)
        first_para = ""
        match = re.search(r"<p>(.*?)</p>", refined["html_body"], flags=re.DOTALL)
        if match:
            first_para = match.group(1)
            bullets = "".join(f"<li>{line.strip()}</li>" for line in re.split(r'[.;]\s*', re.sub(r'<.*?>', '', first_para)) if line.strip())
            if bullets:
                list_html = f"<ul style='margin-left:20px'>{bullets}</ul>"
                refined["html_body"] = refined["html_body"].replace(f"<p>{first_para}</p>", list_html)
                refined["sanitized_description"] += " Converted a paragraph to bullet points."
                changed = True

    # Free-form adjustments: look for keywords and apply safe edits
    if "add signature" in instr_low or "include signature" in instr_low:
        if "Best regards" not in refined["html_body"]:
            refined["html_body"] = refined["html_body"].replace("</div>\n</body>", "<p>Best regards,<br/>Security Team</p></div>\n</body>")
            refined["plain_text_body"] += "\n\nBest regards,\nSecurity Team"
            refined["sanitized_description"] += " Signature added."
            changed = True

    # If instruction is a short natural sentence that doesn't match rules, attempt a best-effort substitution:
    if not changed and instr_low:
        # heuristics: increase/decrease urgency words
        if any(w in instr_low for w in ["urgent", "asap", "immediately", "now"]):
            urgency = min(10, urgency + 1)
            add_urgent_banner()
            refined["subject"] = "URGENT: " + refined.get("subject", "")
            refined["sanitized_description"] += " Applied urgency heuristics based on instruction."
            changed = True
        elif any(w in instr_low for w in ["friendly", "casual", "warm", "nice"]):
            refined["html_body"] = refined["html_body"].replace("<p>Dear", "<p>Hi there,")
            refined["sanitized_description"] += " Applied friendly tone heuristics."
            changed = True
        elif any(w in instr_low for w in ["simplify", "easy to read", "plain english"]):
            refined["html_body"] = simplify_text(refined["html_body"])
            refined["plain_text_body"] = simplify_text(refined["plain_text_body"])
            refined["sanitized_description"] += " Applied plain-language heuristics."
            changed = True

    # clamp urgency and set back
    refined["urgency_score"] = max(0, min(10, urgency))

    # ensure subject formatting cleanup (no repeated URGENT: prefixes)
    refined["subject"] = re.sub(r"(URGENT:\s*){2,}", "URGENT: ", refined.get("subject", ""))

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
        
        choice = input("\nSelect an agent (1-6), 'help', or 'quit': ").strip().lower()
        
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

def refine_prompt(template_input, user_input):
    try:
        refined = refine_template(template_input, user_input)
        if refined != current_template:
            current_template = refined
            return current_template
    except Exception as e:
        print("Exception at refine_prompt in phisherman_cli", e)

# if __name__ == "__main__":
#     main()

def teacher_session():
    """Launch teacher session"""
    try:
        from backend.trainer.cli import run_teacher_session
        run_teacher_session()
    except ImportError as e:
        print(f"\n❌ Error importing teacher module: {e}")
        print("   Teacher functionality may not be available.")
        print("   Type 'back' to return to main menu.")
    except Exception as e:
        print(f"\n❌ Error starting teacher session: {e}")
        print("   Type 'back' to return to main menu.")

