#!/usr/bin/env python3
"""
Health Phisher Agent - Generates health-related phishing templates for training.
Chat Protocol v0.3.0 implementation with Mailbox support.
"""

from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage, TextContent, StartSessionContent, EndSessionContent, chat_protocol_spec
)

AGENT_NAME = "health_phisher"
SEED = "health_phisher"
PORT = 8003

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
        await ctx.send(sender, txt(f"Health Phisher ready. I generate healthcare phishing templates for cybersecurity training. Examples: appointments, medical records, insurance verification."))
        return
    
    # Handle session end
    if any(isinstance(c, EndSessionContent) for c in msg.content):
        ctx.logger.info("Session ended")
        return
    
    # Extract user text
    user_text = msg.text() or ""
    ctx.logger.info(f"Received message: {user_text}")
    
    # Process the request
    if "generate" in user_text.lower() or "create" in user_text.lower():
        response = """I'll generate a healthcare phishing template with:
- Subject: Medical Records Update Required
- Scenario: Healthcare or medical information verification
- Safety flags: Educational training use only
- Template for phishing awareness training"""
    elif "template" in user_text.lower():
        response = "Healthcare phishing scenarios include: appointment reminders, medical records updates, insurance verification, test results."
    else:
        response = f"[Health Phisher] I specialize in healthcare phishing templates. Say 'generate template' for a healthcare phishing example."
    
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
    print("Health Phisher Agent - Healthcare Phishing Template Generator")
    print("=" * 60)
    print(f"Name: {AGENT_NAME}")
    print(f"Port: {PORT}")
    print(f"Mailbox: Enabled")
    print(f"Protocol: Chat Protocol v0.3.0")
    print("=" * 60)
    agent.run()
