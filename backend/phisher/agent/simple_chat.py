#!/usr/bin/env python3
"""
Simple Terminal Chat Interface for Phisherman Agents
Interactive CLI to chat with agents via keyword-based responses
"""

import sys
from datetime import datetime

# Agent configuration with keyword responses
AGENTS = {
    "1": {
        "name": "phish_master",
        "display": "Phish Master (Orchestrator)",
        "port": 8001,
        "description": "Coordinates phishing template generation across domain agents",
        "is_orchestrator": True,
        "responses": {
            "finance": "I'll coordinate with the Finance Phisher to generate a financial phishing template for training.",
            "health": "I'll coordinate with the Health Phisher to generate a healthcare phishing template for training.",
            "personal": "I'll coordinate with the Personal Phisher to generate a personal information phishing template for training.",
            "refine": "I'll send the template to Phish Refiner for optimization and improvement.",
            "default": "I coordinate phishing template generation. Domains: finance, health, personal. Say 'generate finance template' or similar."
        }
    },
    "2": {
        "name": "finance_phisher",
        "display": "Finance Phisher",
        "port": 8002,
        "description": "Generates financial phishing templates",
        "is_orchestrator": False,
        "domain": "finance",
        "responses": {
            "bank": "I'll generate a banking phishing template targeting account verification scenarios.",
            "payment": "I'll generate a payment phishing template for payment verification scenarios.",
            "invoice": "I'll generate an invoice/billing phishing template for training.",
            "credit": "I'll generate a credit card phishing template for security training.",
            "default": "I generate financial phishing templates. Try: banking, payment, invoice, or credit card scenarios."
        },
        "template": {
            "template_id": "FIN001",
            "subject": "Urgent: Account Verification Required",
            "preheader": "Your payment information needs verification",
            "html_body": "<html><body><h2>Account Verification Required</h2><p>Dear [Name],</p><p>We need to verify your account information immediately. Please click below to secure your account.</p><a href='[VERIFY_LINK]'>Verify Account</a></body></html>",
            "plain_text_body": "Account Verification Required\n\nDear [Name],\n\nWe need to verify your account information immediately. Please visit [VERIFY_LINK] to secure your account.",
            "urgency_score": 8,
            "safety_flags": ["requests_payment_info", "urgent_action_required"]
        }
    },
    "3": {
        "name": "health_phisher",
        "display": "Health Phisher",
        "port": 8003,
        "description": "Generates healthcare phishing templates",
        "is_orchestrator": False,
        "domain": "health",
        "responses": {
            "appointment": "I'll generate a medical appointment/prescription phishing template.",
            "insurance": "I'll generate a health insurance phishing template for training.",
            "pharmaceutical": "I'll generate a pharmaceutical/drug safety phishing template.",
            "medical": "I'll generate a general healthcare phishing template for training.",
            "default": "I generate healthcare phishing templates. Try: appointment, insurance, pharmaceutical, or medical scenarios."
        },
        "template": {
            "template_id": "HLT001",
            "subject": "Medical Records Update Required",
            "preheader": "Your health information needs verification",
            "html_body": "<html><body><h2>Medical Records Update</h2><p>Dear [Name],</p><p>We need to update your medical records. Please provide verification by clicking below.</p><a href='[VERIFY_LINK]'>Update Records</a></body></html>",
            "plain_text_body": "Medical Records Update\n\nDear [Name],\n\nWe need to update your medical records. Please visit [VERIFY_LINK] to provide verification.",
            "urgency_score": 7,
            "safety_flags": ["requests_medical_data", "personal_information"]
        }
    },
    "4": {
        "name": "personal_phisher",
        "display": "Personal Phisher",
        "port": 8004,
        "description": "Generates personal information phishing templates",
        "is_orchestrator": False,
        "domain": "personal",
        "responses": {
            "social": "I'll generate a social media phishing template for account verification scenarios.",
            "email": "I'll generate an email account phishing template for training.",
            "password": "I'll generate a password reset phishing template for security training.",
            "identity": "I'll generate an identity verification phishing template.",
            "default": "I generate personal phishing templates. Try: social media, email account, password reset, or identity verification scenarios."
        },
        "template": {
            "template_id": "PER001",
            "subject": "Account Security Verification",
            "preheader": "Secure your account immediately",
            "html_body": "<html><body><h2>Security Alert</h2><p>Dear [Name],</p><p>We detected unusual activity on your account. Please verify your identity immediately.</p><a href='[VERIFY_LINK]'>Verify Identity</a></body></html>",
            "plain_text_body": "Security Alert\n\nDear [Name],\n\nWe detected unusual activity on your account. Please visit [VERIFY_LINK] to verify your identity.",
            "urgency_score": 9,
            "safety_flags": ["requests_personal_info", "security_alert"]
        }
    },
    "5": {
        "name": "phish_refiner",
        "display": "Phish Refiner",
        "port": 8005,
        "description": "Refines and improves phishing templates",
        "is_orchestrator": False,
        "responses": {
            "realism": "I'll enhance the template's realism and believability for training purposes.",
            "tone": "I'll refine the language and tone to be more persuasive and professional.",
            "urgency": "I'll optimize the urgency and persuasion techniques in the template.",
            "design": "I'll improve the visual design and formatting of the template.",
            "default": "I refine phishing templates. Try: improve realism, adjust tone, enhance urgency, or optimize design."
        }
    }
}

def print_header():
    """Print header"""
    print("\n" + "="*70)
    print("🤖 Phisherman Agent Terminal Chat")
    print("="*70)

def print_agents():
    """Print available agents"""
    print("\n📋 Available Agents:")
    print("-"*70)
    for key, agent in AGENTS.items():
        print(f"{key}. {agent['display']}")
        print(f"   {agent['description']}")
    print("-"*70)

def get_agent_response(agent_info: dict, user_input: str) -> str:
    """Get response from agent based on keywords"""
    user_lower = user_input.lower()
    
    # Check for keywords
    for keyword, response in agent_info["responses"].items():
        if keyword != "default" and keyword in user_lower:
            return response
    
    # Return default response
    return agent_info["responses"]["default"]

def chat_with_agent(agent_info: dict):
    """Interactive chat with an agent"""
    display_name = agent_info["display"]
    
    print(f"\n{'='*70}")
    print(f"💬 Chatting with {display_name}")
    print(f"{'='*70}")
    print(f"Type 'exit' or 'quit' to end chat")
    print(f"Type 'help' for suggestions")
    print("-"*70)
    
    # Check if orchestrator and show options
    if agent_info.get("is_orchestrator"):
        print(f"\n{display_name}: Hello! I coordinate phishing template generation.")
        print("\n📋 Choose a domain:")
        print("   1. Finance")
        print("   2. Health")
        print("   3. Personal")
        print("\nOr type a message directly.")
        print("-"*70)
    else:
        # Show welcome message
        print(f"\n{display_name}: Hello! I'm ready to help.")
        print("-"*70)
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input(f"\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print(f"\n👋 Ending chat with {display_name}")
                break
            
            if user_input.lower() == 'help':
                print("\n💡 Message suggestions:")
                for keyword, response in agent_info["responses"].items():
                    if keyword != "default":
                        print(f"   • '{keyword}'")
                continue
            
            # Handle orchestrator workflow
            if agent_info.get("is_orchestrator"):
                # Check for domain selection
                if user_input.lower() in ['1', 'finance']:
                    response = chat_with_domain_agent("finance")
                    print(f"\n{display_name}: {response}")
                    # Offer to refine
                    offer_refinement()
                elif user_input.lower() in ['2', 'health']:
                    response = chat_with_domain_agent("health")
                    print(f"\n{display_name}: {response}")
                    # Offer to refine
                    offer_refinement()
                elif user_input.lower() in ['3', 'personal']:
                    response = chat_with_domain_agent("personal")
                    print(f"\n{display_name}: {response}")
                    # Offer to refine
                    offer_refinement()
                else:
                    # Regular keyword response
                    agent_response = get_agent_response(agent_info, user_input)
                    print(f"\n{display_name}: {agent_response}")
            else:
                # Regular agent chat
                agent_response = get_agent_response(agent_info, user_input)
                print(f"\n{display_name}: {agent_response}")
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Ending chat with {display_name}")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def chat_with_domain_agent(domain: str) -> str:
    """Simulate Phish Master talking to domain agents and getting template"""
    print(f"\n🤖 Coordinating with {domain.title()} Phisher...")
    
    # Find the domain agent
    domain_agent = None
    for agent_key, agent in AGENTS.items():
        if agent.get("domain") == domain:
            domain_agent = agent
            break
    
    if not domain_agent:
        return f"Error: Could not find {domain} agent"
    
    # Simulate agent conversation
    print(f"   → Connecting to {domain_agent['display']}...")
    print(f"   → Generating template...")
    
    # Get template from agent
    template = domain_agent.get("template", {})
    
    # Format the response with full email content
    html_body = template.get('html_body', 'N/A')
    plain_text_body = template.get('plain_text_body', 'N/A')
    
    return f"""
✅ Template Generated Successfully!

📧 Template ID: {template.get('template_id', 'N/A')}
📝 Subject: {template.get('subject', 'N/A')}
🔔 Preheader: {template.get('preheader', 'N/A')}
⚠️  Urgency Score: {template.get('urgency_score', 'N/A')}/10
🚩 Safety Flags: {', '.join(template.get('safety_flags', []))}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 EMAIL CONTENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 HTML Version:
{html_body}

📝 Plain Text Version:
{plain_text_body}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The {domain.title()} Phisher has generated your phishing training template.

💡 Would you like to refine this template with Phish Refiner?
   Type 'refine' to continue with refinement.
"""

def offer_refinement() -> str:
    """Offer to refine the template with Phish Refiner"""
    try:
        user_input = input(f"\nYour choice: ").strip().lower()
        
        if user_input in ['refine', 'yes', 'y', '1']:
            # Directly chat with Phish Refiner
            print(f"\n🤖 Connecting to Phish Refiner...")
            print(f"   → Template received from Phish Master")
            print(f"   → Ready for refinement")
            
            # Start interactive chat with Phish Refiner
            chat_with_refiner()
            return None
        else:
            return None
            
    except KeyboardInterrupt:
        return None

def chat_with_refiner():
    """Direct chat with Phish Refiner for template refinement"""
    refiner_info = AGENTS["5"]  # Phish Refiner
    
    # Store current template state
    current_template = {
        "subject": "Account Verification Required",
        "html_body": "<html><body><h2>Account Verification Required</h2><p>Dear [Name],</p><p>We need to verify your account information immediately. Please click below to secure your account.</p><a href='[VERIFY_LINK]'>Verify Account</a></body></html>",
        "plain_text_body": "Account Verification Required\n\nDear [Name],\n\nWe need to verify your account information immediately. Please visit [VERIFY_LINK] to secure your account."
    }
    
    print(f"\n{'='*70}")
    print(f"💬 Chatting with {refiner_info['display']}")
    print(f"{'='*70}")
    print(f"Type 'exit' or 'quit' to end refinement")
    print(f"Type 'help' for refinement suggestions")
    print(f"Type 'show' to see current template")
    print("-"*70)
    
    print(f"\n{refiner_info['display']}: Hello! I'm ready to refine your template.")
    print(f"   What would you like me to improve?")
    print("-"*70)
    
    # Chat loop with Phish Refiner
    while True:
        try:
            user_input = input(f"\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'q', 'done']:
                print(f"\n{refiner_info['display']}: Refinement complete!")
                print(f"✅ Your template has been optimized for cybersecurity training.")
                break
            
            if user_input.lower() == 'help':
                print("\n💡 Refinement suggestions:")
                print("   • 'realism' - Enhance realism and believability")
                print("   • 'tone' - Refine language and tone")
                print("   • 'urgency' - Optimize urgency and persuasion")
                print("   • 'design' - Improve visual design")
                print("   • 'show' - Display current template")
                print("   • 'done' - Complete refinement")
                continue
            
            if user_input.lower() == 'show':
                show_template(current_template)
                continue
            
            # Check for natural language refinement requests
            refined = apply_refinement(user_input, current_template)
            
            if refined:
                # Update template with refined version
                current_template = refined
                print(f"\n{refiner_info['display']}: I've applied your requested changes!")
                print(f"\n✅ Refinement applied! Your template has been enhanced.")
                print(f"   Realism Score: 9/10 | Urgency: Optimized | Tone: Enhanced")
                print(f"\n📄 UPDATED TEMPLATE:")
                show_template(current_template)
            else:
                # Get standard refiner response
                refiner_response = get_agent_response(refiner_info, user_input)
                print(f"\n{refiner_info['display']}: {refiner_response}")
                
        except KeyboardInterrupt:
            print(f"\n\n{refiner_info['display']}: Refinement interrupted.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def show_template(template: dict):
    """Display the current template"""
    print(f"\n{'='*70}")
    print(f"📄 CURRENT TEMPLATE")
    print(f"{'='*70}")
    print(f"\n📝 Subject: {template.get('subject', 'N/A')}")
    print(f"\n🌐 HTML Body:")
    print(template.get('html_body', 'N/A'))
    print(f"\n📝 Plain Text Body:")
    print(template.get('plain_text_body', 'N/A'))
    print(f"{'='*70}")

def apply_refinement(instruction: str, current_template: dict) -> dict:
    """Apply refinement based on user instruction and return updated template"""
    instruction_lower = instruction.lower()
    
    # Create a copy to modify
    refined_template = current_template.copy()
    
    # Natural language processing for refinements
    if 'social security' in instruction_lower or 'social' in instruction_lower:
        refined_template["subject"] = "URGENT: Social Security Account Verification Required"
        refined_template["html_body"] = "<html><body><h2>Social Security Account Alert</h2><p>Dear [Name],</p><p>We need to verify your Social Security account information immediately to protect your benefits. Unusual activity has been detected.</p><p><strong>Action Required:</strong> Click below to verify your identity and secure your account.</p><a href='[VERIFY_LINK]' style='background: #ff6600; color: white; padding: 12px 24px; text-decoration: none;'>Verify Account Now</a></body></html>"
        refined_template["plain_text_body"] = "Social Security Account Alert\n\nDear [Name],\n\nWe need to verify your Social Security account information immediately to protect your benefits. Unusual activity has been detected.\n\nAction Required: Visit [VERIFY_LINK] to verify your identity and secure your account."
        return refined_template
    
    if 'personal' in instruction_lower and 'security' in instruction_lower:
        refined_template["subject"] = "Security Alert: Account Compromise Detected"
        refined_template["html_body"] = "<html><body><h2>🚨 Security Alert</h2><p>Dear [Name],</p><p>We detected suspicious activity on your account. Your personal information may be at risk.</p><p>Please verify your identity immediately to prevent unauthorized access.</p><a href='[VERIFY_LINK]'>Secure Account</a></body></html>"
        refined_template["plain_text_body"] = "Security Alert\n\nDear [Name],\n\nWe detected suspicious activity on your account. Your personal information may be at risk.\n\nPlease verify your identity immediately: [VERIFY_LINK]"
        return refined_template
    
    if 'medical' in instruction_lower or 'health' in instruction_lower:
        refined_template["subject"] = "Medical Records Update Required"
        refined_template["html_body"] = "<html><body><h2>Medical Records Verification</h2><p>Dear [Name],</p><p>Your medical records need immediate verification to ensure accurate healthcare services.</p><p>Please update your information by clicking below.</p><a href='[VERIFY_LINK]'>Update Medical Records</a></body></html>"
        refined_template["plain_text_body"] = "Medical Records Verification\n\nDear [Name],\n\nYour medical records need immediate verification to ensure accurate healthcare services.\n\nPlease update your information: [VERIFY_LINK]"
        return refined_template
    
    if 'financial' in instruction_lower or 'money' in instruction_lower or 'payment' in instruction_lower:
        refined_template["subject"] = "Payment Verification Required - Action Needed"
        refined_template["html_body"] = "<html><body><h2>Payment Account Verification</h2><p>Dear [Name],</p><p>We need to verify your payment information to prevent fraudulent transactions.</p><p>Please confirm your details immediately.</p><a href='[VERIFY_LINK]'>Verify Payment Info</a></body></html>"
        refined_template["plain_text_body"] = "Payment Account Verification\n\nDear [Name],\n\nWe need to verify your payment information to prevent fraudulent transactions.\n\nPlease confirm your details: [VERIFY_LINK]"
        return refined_template
    
    if 'government' in instruction_lower or 'irs' in instruction_lower or 'tax' in instruction_lower:
        refined_template["subject"] = "IRS Account Verification Required"
        refined_template["html_body"] = "<html><body><h2>IRS Account Verification</h2><p>Dear [Name],</p><p>The Internal Revenue Service requires immediate verification of your account to process your tax information securely.</p><p>Official action required. Click below to verify.</p><a href='[VERIFY_LINK]'>Verify IRS Account</a></body></html>"
        refined_template["plain_text_body"] = "IRS Account Verification\n\nDear [Name],\n\nThe Internal Revenue Service requires immediate verification of your account to process your tax information securely.\n\nOfficial action required: [VERIFY_LINK]"
        return refined_template
    
    if 'insurance' in instruction_lower:
        refined_template["subject"] = "Insurance Policy Update Required"
        refined_template["html_body"] = "<html><body><h2>Insurance Policy Verification</h2><p>Dear [Name],</p><p>Your insurance policy requires immediate verification to maintain coverage.</p><p>Please update your information to avoid service interruption.</p><a href='[VERIFY_LINK]'>Update Policy</a></body></html>"
        refined_template["plain_text_body"] = "Insurance Policy Verification\n\nDear [Name],\n\nYour insurance policy requires immediate verification to maintain coverage.\n\nPlease update your information: [VERIFY_LINK]"
        return refined_template
    
    if 'more urgent' in instruction_lower or 'increase urgency' in instruction_lower:
        refined_template["subject"] = "URGENT: " + refined_template["subject"]
        refined_template["html_body"] = refined_template["html_body"].replace("<p>Dear", "<p><strong>URGENT ACTION REQUIRED</strong></p><p>Dear")
        refined_template["plain_text_body"] = "URGENT ACTION REQUIRED\n\n" + refined_template["plain_text_body"]
        return refined_template
    
    if 'make it' in instruction_lower or 'change it' in instruction_lower or 'update' in instruction_lower:
        refined_template["subject"] = "Updated: " + refined_template["subject"]
        refined_template["html_body"] = refined_template["html_body"].replace("<p>Dear", "<p><em>Enhanced for training purposes</em></p><p>Dear")
        return refined_template
    
    if 'tone' in instruction_lower:
        refined_template["html_body"] = refined_template["html_body"].replace("We need to", "We urgently need to")
        refined_template["plain_text_body"] = refined_template["plain_text_body"].replace("We need to", "We urgently need to")
        return refined_template
    
    if 'realism' in instruction_lower or 'believable' in instruction_lower:
        refined_template["html_body"] = refined_template["html_body"].replace("<h2>", "<h2 style='color: #0066cc;'>")
        refined_template["html_body"] = refined_template["html_body"] + "<p><small>Official secure communication</small></p>"
        return refined_template
    
    # Default response for unrecognized instructions
    return None

def main():
    """Main function"""
    print_header()
    
    while True:
        print_agents()
        
        choice = input("\nSelect an agent (1-5) or 'q' to quit: ").strip()
        
        if choice.lower() in ['q', 'quit', 'exit']:
            print("\n👋 Goodbye!")
            break
        
        if choice in AGENTS:
            agent_info = AGENTS[choice]
            chat_with_agent(agent_info)
        else:
            print("\n❌ Invalid choice. Please select 1-5 or 'q' to quit.")

if __name__ == "__main__":
    main()

