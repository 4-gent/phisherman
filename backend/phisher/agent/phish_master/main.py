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
### Phish Master Agent
##
## This agent is the orchestrator for phishing template generation.
## It coordinates between domain-specific agents (finance, health, personal) and the refinement agent.
##

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)

# the subject that this assistant is an expert in
subject_matter = "phishing template generation coordination"

client = OpenAI(
    # By default, we are using the ASI-1 LLM endpoint and model
    base_url='https://api.asi1.ai/v1',

    # You can get an ASI-1 api key by creating an account at https://asi1.ai/dashboard/api-keys
    api_key='insert API KEY',
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
            create_text_chat(f"Hi! I'm the Phish Master orchestrator. I coordinate phishing template generation across domain agents (finance, health, personal). How can I help you generate a phishing training template?", end_session=False),
        )

    text = msg.text()
    if not text:
        return

    try:
        r = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": f"""You are the Phish Master orchestrator for phishing template generation in cybersecurity training. If the user asks about other topics, politely redirect to your expertise.

You coordinate between specialized domain agents:
- finance_phisher: Banking, payment, invoice phishing
- health_phisher: Medical, insurance, pharmaceutical phishing
- personal_phisher: Social media, account verification phishing
- phish_refiner: Template refinement and improvement

Your responsibilities include:
- Understanding user requirements
- Routing to appropriate domain agents
- Coordinating multi-step workflows
- Aggregating agent responses
- Suggesting template refinement when needed
- Providing educational context

When helping users:
- Identify which domain agent they need (finance, health, personal)
- Suggest appropriate workflows
- Coordinate between agents if needed
- Provide clear, structured guidance
- Always emphasize educational training purposes

Remember: These templates are for educational and training purposes only to help organizations improve their cybersecurity awareness."""},
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
    # we are not required to handle acknowledgements
    pass


# we include the protocol in the agent
agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
