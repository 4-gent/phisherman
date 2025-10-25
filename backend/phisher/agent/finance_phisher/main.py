#!/usr/bin/env python3
"""
Finance Phisher Agent - Generates financial phishing templates for training.
Chat Protocol v0.3.0 implementation with Mailbox support.
"""

from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage, TextContent, StartSessionContent, EndSessionContent, chat_protocol_spec
)

AGENT_NAME = "finance_phisher"
SEED = "finance_phisher"
PORT = 8002

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
        await ctx.send(sender, txt(f"Finance Phisher ready. I generate financial phishing templates for cybersecurity training. Examples: payment verification, invoices, account suspension."))
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
        response = """I'll generate a financial phishing template with:
- Subject: Urgent Payment Verification Required
- Scenario: Banking or payment verification
- Safety flags: Educational training use only
- Template for phishing awareness training"""
    elif "template" in user_text.lower():
        response = "Financial phishing scenarios include: payment verification, invoice overdue, account suspension, banking alerts."
    else:
        response = f"[Finance Phisher] I specialize in financial phishing templates. Say 'generate template' for a financial phishing example."
    
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
    print("Finance Phisher Agent - Financial Phishing Template Generator")
    print("=" * 60)
    print(f"Name: {AGENT_NAME}")
    print(f"Port: {PORT}")
    print(f"Mailbox: Enabled")
    print(f"Protocol: Chat Protocol v0.3.0")
    print("=" * 60)
    agent.run()
