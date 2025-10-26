#!/usr/bin/env python3
"""
Personal Phisher Agent - Generates personal-info phishing templates for training.
Chat Protocol v0.3.0 implementation with Mailbox support.
"""

from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage, TextContent, StartSessionContent, EndSessionContent, chat_protocol_spec
)

AGENT_NAME = "personal_phisher"
SEED = "personal_phisher"
PORT = 8004

# Initialize agent with mailbox support
agent = Agent(name=AGENT_NAME, seed=SEED, port=PORT, mailbox=True)
protocol = Protocol()

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
        await ctx.send(sender, txt(f"Personal Phisher ready. I generate personal information phishing templates for cybersecurity training. Examples: account verification, security alerts, subscriptions."))
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
        response = """I'll generate a personal information phishing template with:
- Subject: Account Security Verification Required
- Scenario: Personal account or identity verification
- Safety flags: Educational training use only
- Template for phishing awareness training"""
    elif "template" in user_text.lower():
        response = "Personal phishing scenarios include: account verification, profile updates, security alerts, subscription renewals."
    else:
        response = f"[Personal Phisher] I specialize in personal information phishing templates. Say 'generate template' for a personal phishing example."
    
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
    print("Personal Phisher Agent - Personal Information Phishing Template Generator")
    print("=" * 60)
    print(f"Name: {AGENT_NAME}")
    print(f"Address: {agent.address}")
    print(f"Port: {PORT}")
    print(f"Mailbox: Enabled")
    print(f"Protocol: Chat Protocol v0.3.0")
    print("=" * 60)
    agent.run()