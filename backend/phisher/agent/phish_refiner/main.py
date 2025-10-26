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
### Phish Refiner Agent
##
## This agent specializes in refining and improving phishing email templates for cybersecurity training.
## It focuses on enhancing realism, improving social engineering techniques, and optimizing template effectiveness.
##

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)

# the subject that this assistant is an expert in
subject_matter = "phishing template refinement"

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
            create_text_chat(f"Hi! I'm a {subject_matter} expert, how can I help?", end_session=False),
        )

    text = msg.text()
    if not text:
        return

    try:
        r = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": f"""You are a helpful assistant who only answers questions about {subject_matter}. If the user asks about any other topics, you should politely say that you do not know about them.

You specialize in refining and improving phishing email templates for cybersecurity training. Your expertise includes:
- Template realism enhancement
- Social engineering optimization
- Language and tone refinement
- Urgency and persuasion techniques
- Visual design improvements
- Call-to-action optimization
- Personalization strategies
- Psychological manipulation techniques
- Template effectiveness analysis
- A/B testing recommendations

When refining phishing templates, always focus on:
- Making templates more believable and realistic
- Improving social engineering techniques
- Enhancing psychological triggers
- Optimizing for different target demographics
- Ensuring educational value for training
- Maintaining ethical boundaries
- Improving template effectiveness metrics

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
