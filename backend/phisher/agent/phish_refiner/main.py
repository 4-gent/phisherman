#!/usr/bin/env python3
"""
Phish Refiner Agent - Refines and improves phishing templates.
Chat Protocol v0.3.0 implementation with Mailbox support.
"""

from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage, TextContent, StartSessionContent, EndSessionContent, chat_protocol_spec
)

AGENT_NAME = "phish_refiner"
SEED = "phish_refiner"
PORT = 8005

# Initialize agent with mailbox support
agent = Agent(name=AGENT_NAME, seed=SEED, port=PORT, mailbox=True)
protocol = Protocol(spec=chat_protocol_spec)

def txt(s: str) -> ChatMessage:
    """Helper to create text message"""
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=str(uuid4()),
        content=[TextContent(type="text", text=s)]
    )

@protocol.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages using Chat Protocol v0.3.0"""
    
    # Handle session start
    if any(isinstance(c, StartSessionContent) for c in msg.content):
        await ctx.send(sender, txt(f"Phish Refiner ready. I refine and improve phishing templates for better training effectiveness. I can adjust tone, urgency, and content."))
        return
    
    # Handle session end
    if any(isinstance(c, EndSessionContent) for c in msg.content):
        ctx.logger.info("Session ended")
        return
    
    # Extract user text
    user_text = msg.text() or ""
    ctx.logger.info(f"Received message: {user_text}")
    
    # Process the request
    if "refine" in user_text.lower() or "improve" in user_text.lower():
        response = """I'll refine the phishing template with:
- Tone adjustment (formal, urgent, friendly)
- Urgency level optimization
- Content enhancement for training effectiveness
- Safety flags updated for educational purposes"""
    elif "tone" in user_text.lower():
        response = "I can adjust tone to: formal, casual, urgent, friendly, or professional based on training needs."
    elif "urgency" in user_text.lower():
        response = "I can modify urgency scores from 1-10 to optimize training effectiveness."
    else:
        response = f"[Phish Refiner] I refine and improve phishing templates. Say 'refine template' or describe specific improvements needed."
    
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
    print("Phish Refiner Agent - Phishing Template Refinement")
    print("=" * 60)
    print(f"Name: {AGENT_NAME}")
    print(f"Port: {PORT}")
    print(f"Mailbox: Enabled")
    print(f"Protocol: Chat Protocol v0.3.0")
    print("=" * 60)
    agent.run()
