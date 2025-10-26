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
### Phish Master Orchestrator
##
## This agent orchestrates phishing template generation across domain agents for cybersecurity training.
## It coordinates with finance_phisher, health_phisher, personal_phisher, and phish_refiner agents.
##

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)

# the subject that this assistant is an expert in
subject_matter = "phishing template generation and cybersecurity training"

client = OpenAI(
    # By default, we are using the ASI-1 LLM endpoint and model
    base_url='https://api.asi1.ai/v1',
    # You can get an ASI-1 api key by creating an account at https://asi1.ai/dashboard/api-keys
    api_key='INSERT_YOUR_API_HERE',
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
            create_text_chat(f"Hi! I'm the phish_master orchestrator for cybersecurity training. I coordinate phishing template generation across domain agents. How can I help?", end_session=False),
        )

    text = msg.text()
    if not text:
        return

    try:
        r = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": f"""You are the phish_master orchestrator for cybersecurity training. You coordinate phishing template generation across domain agents (finance_phisher, health_phisher, personal_phisher, phish_refiner). 

Your capabilities include:
- Phishing template generation
- Agent coordination
- Template aggregation
- Multi-domain routing

Generate structured JSON templates with fields: template_id, subject, preheader, html_body, plain_text_body, placeholders, urgency_score, safety_flags, recommended_redirect.

Always focus on cybersecurity training and phishing awareness. If asked about other topics, politely redirect to your expertise in phishing template generation."""},
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
