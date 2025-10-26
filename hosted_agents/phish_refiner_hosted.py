"""
Phish Refiner Agent - Hosted on Agentverse
Refines and improves phishing templates.
"""

from datetime import datetime
from uuid import uuid4

from openai import OpenAI
from uagents import Context, Protocol, Agent
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)

subject_matter = "refining and improving phishing templates for cybersecurity training"

client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key='INSERT_YOUR_API_HERE',
)

agent = Agent(name="phish_refiner")
protocol = Protocol(spec=chat_protocol_spec)

@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    if any(isinstance(item, StartSessionContent) for item in msg.content):
        await ctx.send(
            sender,
            create_text_chat(f"Hi! I'm a {subject_matter} expert. I refine and improve phishing templates for better training effectiveness. I can adjust tone, urgency, and content. How can I help?"),
        )

    text = msg.text()
    if not text:
        return

    try:
        r = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": f"""You are a helpful assistant who {subject_matter}. Provide specific, actionable refinement suggestions including tone adjustments, urgency optimization, content enhancements, and social engineering techniques. Always include educational training warnings. Generate refinement suggestions immediately in one response without asking for clarification."""},
                {"role": "user", "content": text},
            ],
            max_tokens=2048,
        )

        response = str(r.choices[0].message.content)
    except Exception as e:
        ctx.logger.exception('Error querying model')
        response = f"An error occurred while processing the request. Please try again later. {e}"

    await ctx.send(sender, create_text_chat(response))

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

agent.include(protocol, publish_manifest=True)
