#!/usr/bin/env python3
"""
Phish Master Agent - Orchestrator for phishing training email generation.
Chat Protocol v0.3.0 implementation with Mailbox support.
"""

from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage, TextContent, StartSessionContent, EndSessionContent, chat_protocol_spec
)

AGENT_NAME = "phish_master"
SEED = "phish_master"
PORT = 8001

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
        await ctx.send(sender, txt(f"Phish Master ready. I coordinate phishing template generation across domain agents. How can I help?"))
        return
    
    # Handle session end
    if any(isinstance(c, EndSessionContent) for c in msg.content):
        ctx.logger.info("Session ended")
        return
    
    # Extract user text
    user_text = msg.text() or ""
    ctx.logger.info(f"Received message: {user_text}")
    
    # Process the request
    if "finance" in user_text.lower():
        response = "I'll coordinate with the Finance Phisher to generate a financial phishing template for training."
    elif "health" in user_text.lower() or "medical" in user_text.lower():
        response = "I'll coordinate with the Health Phisher to generate a healthcare phishing template for training."
    elif "personal" in user_text.lower():
        response = "I'll coordinate with the Personal Phisher to generate a personal information phishing template for training."
    elif "refine" in user_text.lower():
        response = "I'll send the template to Phish Refiner for optimization and improvement."
    else:
        response = f"[Phish Master] I coordinate phishing template generation. Domains: finance, health, personal. Say 'generate finance template' or similar."
    
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
    print("Phish Master Agent - Orchestrator for Phishing Training")
    print("=" * 60)
    print(f"Name: {AGENT_NAME}")
    print(f"Port: {PORT}")
    print(f"Mailbox: Enabled")
    print(f"Protocol: Chat Protocol v0.3.0")
    print("=" * 60)
    agent.run()
