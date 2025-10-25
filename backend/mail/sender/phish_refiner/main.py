#!/usr/bin/env python3
"""
Phish Refiner Agent - A chatbot that modifies existing phishing templates.
This agent acts as a refinement tool for adjusting tone, content, and style of phishing templates.
"""

import json
import asyncio
from typing import Dict, List, Any
from uagents import Agent, Context, Model
# from uagents.setup import fund_agent_if_low  # Disabled for mailbox mode

# Initialize the agent
phish_refiner = Agent(
    name="phish_refiner",
    seed="phish-refiner-seed-key-2025",
    port=8005,
    endpoint=["http://127.0.0.1:8005/submit"],
)

# Fund the agent if needed (disabled for mailbox mode)
# fund_agent_if_low(phish_refiner.wallet.address())

class RefinementRequest(Model):
    """Request model for template refinement"""
    original_template: Dict[str, Any]
    refinement_instructions: str
    target_tone: str = "neutral"  # formal, casual, urgent, friendly, etc.
    urgency_adjustment: int = 0  # -5 to +5 adjustment
    content_focus: str = "general"  # specific areas to focus on

class RefinementResponse(Model):
    """Response model for refined templates"""
    refined_template: Dict[str, Any]
    changes_made: List[str]
    refinement_summary: str
    confidence_score: float

@phish_refiner.on_message(model=RefinementRequest)
async def handle_refinement_request(ctx: Context, sender: str, msg: RefinementRequest):
    """Handle template refinement requests"""
    ctx.logger.info(f"Received refinement request with instructions: {msg.refinement_instructions}")
    
    # System prompt for the phish refiner
    system_prompt = f"""
    You are the Phish Refiner, an AI chatbot specialized in modifying phishing training templates.
    
    Your capabilities:
    - Adjust tone and style (formal, casual, urgent, friendly, professional)
    - Modify urgency levels and emotional triggers
    - Refine content for specific target audiences
    - Improve believability while maintaining educational value
    - Add or remove specific elements based on instructions
    
    Current refinement request:
    - Instructions: {msg.refinement_instructions}
    - Target Tone: {msg.target_tone}
    - Urgency Adjustment: {msg.urgency_adjustment}
    - Content Focus: {msg.content_focus}
    
    Refine the template to be:
    - More effective for training purposes
    - Appropriate for the specified tone and audience
    - Safe and educational
    - Believable but clearly a training scenario
    """
    
    # Refine the template
    refined_template, changes_made = refine_template(msg)
    
    # Create structured response
    response = RefinementResponse(
        refined_template=refined_template,
        changes_made=changes_made,
        refinement_summary=f"Refined template with {msg.target_tone} tone and {len(changes_made)} modifications",
        confidence_score=0.85
    )
    
    # Send response
    await ctx.send(sender, response)
    
    # Log the refinement
    ctx.logger.info(f"Refined template with {len(changes_made)} changes")

def refine_template(request: RefinementRequest) -> tuple[Dict[str, Any], List[str]]:
    """Refine a phishing template based on instructions"""
    
    original = request.original_template
    changes_made = []
    
    # Create a copy of the original template
    refined = original.copy()
    
    # Adjust urgency score
    if request.urgency_adjustment != 0:
        original_urgency = refined.get("urgency_score", 5)
        new_urgency = max(1, min(10, original_urgency + request.urgency_adjustment))
        refined["urgency_score"] = new_urgency
        changes_made.append(f"Adjusted urgency from {original_urgency} to {new_urgency}")
    
    # Adjust tone based on target_tone
    if request.target_tone == "formal":
        refined["subject"] = f"RE: {refined.get('subject', '')}"
        changes_made.append("Added formal 'RE:' prefix to subject")
        
    elif request.target_tone == "urgent":
        if "URGENT" not in refined.get("subject", ""):
            refined["subject"] = f"URGENT: {refined.get('subject', '')}"
            changes_made.append("Added URGENT prefix to subject")
            
    elif request.target_tone == "friendly":
        # Add friendly greeting
        html_body = refined.get("html_body", "")
        if "Dear" in html_body:
            html_body = html_body.replace("Dear", "Hi there!")
            refined["html_body"] = html_body
            changes_made.append("Changed formal greeting to friendly tone")
    
    # Apply specific refinement instructions
    if "increase urgency" in request.refinement_instructions.lower():
        refined["urgency_score"] = min(10, refined.get("urgency_score", 5) + 2)
        changes_made.append("Increased urgency level")
        
    if "make more formal" in request.refinement_instructions.lower():
        # Add formal language elements
        refined["subject"] = f"Official Notice: {refined.get('subject', '')}"
        changes_made.append("Added formal 'Official Notice' prefix")
        
    if "add deadline" in request.refinement_instructions.lower():
        # Add deadline to content
        html_body = refined.get("html_body", "")
        deadline_text = "<p style='color: #dc3545; font-weight: bold;'>Deadline: 24 hours from receipt of this message.</p>"
        refined["html_body"] = html_body.replace("</div>", f"{deadline_text}</div>")
        changes_made.append("Added 24-hour deadline")
        
    if "hr email" in request.refinement_instructions.lower():
        # Make it look like HR email
        refined["subject"] = f"HR Department: {refined.get('subject', '')}"
        refined["preheader"] = "Human Resources notification"
        changes_made.append("Modified to appear as HR department email")
    
    # Update template_id to reflect refinement
    original_id = refined.get("template_id", "template")
    refined["template_id"] = f"{original_id}_refined"
    
    return refined, changes_made

@phish_refiner.on_event("startup")
async def startup(ctx: Context):
    """Initialize the agent on startup"""
    ctx.logger.info("Phish Refiner agent started and ready to refine phishing templates")
    ctx.storage.set('refinement_count', 0)

if __name__ == "__main__":
    print("Phish Refiner Agent - Phishing Template Refinement Chatbot")
    print("=" * 60)
    print("System Prompt: Chatbot for modifying existing phishing templates")
    print("Capabilities: Tone adjustment, urgency modification, content refinement")
    print("=" * 60)
    
    # Example structured JSON output
    example_output = {
        "refined_template": {
            "template_id": "phish_finance_001_refined",
            "subject": "URGENT: Payment Verification Required - Action Needed",
            "preheader": "Your account needs immediate attention to prevent suspension",
            "html_body": "<html><body><h2>Payment Verification Required</h2><p>We have detected unusual activity on your account ending in [account_last_four]. To protect your account, we need to verify your payment information immediately.</p></body></html>",
            "plain_text_body": "Payment Verification Required\n\nWe have detected unusual activity on your account ending in [account_last_four]. Please verify your payment information immediately.",
            "placeholders": [
                {"name": "recipient_name", "description": "Target's full name"},
                {"name": "account_last_four", "description": "Last 4 digits of account number"},
                {"name": "verification_link", "description": "Training verification link"}
            ],
            "urgency_score": 9,
            "safety_flags": ["requests_payment_info", "urgent_action_required", "account_suspension_threat"],
            "recommended_redirect": "training_finance_payment_verification"
        },
        "changes_made": [
            "Added URGENT prefix to subject",
            "Increased urgency level",
            "Added 24-hour deadline"
        ],
        "refinement_summary": "Refined template with urgent tone and 3 modifications",
        "confidence_score": 0.85
    }
    
    print("Example Output Structure:")
    print(json.dumps(example_output, indent=2))
    print("=" * 60)
    
    # Run the agent
    phish_refiner.run()
