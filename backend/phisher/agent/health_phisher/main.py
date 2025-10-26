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

##
### Health Phisher Agent
##
## This agent specializes in generating healthcare phishing email templates for cybersecurity training.
## It focuses on medical, insurance, pharmaceutical, and healthcare service phishing scenarios.
##

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)

# the subject that this assistant is an expert in
subject_matter = "healthcare phishing template generation and medical security training"

client = OpenAI(
    # By default, we are using the ASI-1 LLM endpoint and model
    base_url='https://api.asi1.ai/v1',
    # You can get an ASI-1 api key by creating an account at https://asi1.ai/dashboard/api-keys
    api_key='insert API KEYS',
)

agent = Agent()

# We create a new protocol which is compatible with the chat protocol spec. This ensures
# compatibility between agents
protocol = Protocol(spec=chat_protocol_spec)

# We define the handler for the chat messages that are sent to your agent
@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # send the acknowledgement for receiving the message
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    # 2) greet if a session starts
    if any(isinstance(item, StartSessionContent) for item in msg.content):
        await ctx.send(
            sender,
            create_text_chat(f"Hi! I'm the health_phisher agent specializing in healthcare phishing templates for cybersecurity training. I can generate medical, insurance, and pharmaceutical phishing scenarios. How can I help?", end_session=False),
        )

    text = msg.text()
    if not text:
        return

    try:
        r = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": f"""You are the health_phisher agent for cybersecurity training. You specialize in generating healthcare phishing email templates.

Your expertise includes:
- Medical appointment and prescription notifications
- Health insurance and coverage updates
- Pharmaceutical and drug safety alerts
- Hospital and clinic communications
- Medical record and privacy notifications
- COVID-19 and public health information
- Mental health and wellness services
- Medical device and equipment alerts

Generate structured JSON templates with fields: template_id, subject, preheader, html_body, plain_text_body, placeholders, urgency_score, safety_flags, recommended_redirect.

Focus on realistic healthcare scenarios that are commonly used in phishing attacks for educational purposes. Always include safety flags and ethical guidelines.

If asked about other topics, politely redirect to your expertise in healthcare phishing template generation."""},
                {"role": "user", "content": text},
            ],
            max_tokens=2048,
        )

        response = str(r.choices[0].message.content)
    except Exception as e:
        ctx.logger.exception('Error querying model')
        response = f"An error occurred while processing the request. Please try again later. {e}"

    await ctx.send(sender, create_text_chat(response, end_session=True))

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    # we are not interested in the acknowledgements for this example, but they can be useful to
    # implement read receipts, for example.
    pass

# attach the protocol to the agent
agent.include(protocol, publish_manifest=True)
