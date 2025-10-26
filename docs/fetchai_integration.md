# Phisherman Fetch.ai Integration Guide

**Comprehensive documentation of how Phisherman leverages the Fetch.ai stack for cybersecurity training**

---

## Overview

Phisherman is a cybersecurity training platform that uses **6 specialized AI agents** to generate safe, educational phishing email templates for organizational security awareness programs. The system demonstrates sophisticated multi-agent orchestration using Fetch.ai's **uAgents framework** and **Agentverse** discovery platform.

### Agent Architecture

| Agent | Role | Purpose |
|-------|------|---------|
| **Phish Master** | Orchestrator | Coordinates requests across domain agents, aggregates outputs |
| **Finance Phisher** | Domain Specialist | Generates financial phishing templates (banking, payments) |
| **Health Phisher** | Domain Specialist | Creates healthcare phishing scenarios (medical records, insurance) |
| **Personal Phisher** | Domain Specialist | Develops personal information phishing templates (social, passwords) |
| **Phish Refiner** | Content Optimizer | Refines and improves templates with better urgency, clarity, structure |
| **Teacher Agent** | Educational Trainer | Provides lessons on phishing detection; conducts quizzes via WebSocket |

### End-to-End Training Flow

```
User Request → Phish Master (orchestrator)
                    ↓
            Domain Agent Selection
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
    Finance      Health     Personal
                    ↓
            Template Generation
                    ↓
            Phish Refiner (optional)
                    ↓
        Sanitized Training Template
                    ↓
            Quiz Pipeline (Teacher Agent)
                    ↓
        User Training & Scoring (+10/–10)
```

---

## uAgents Usage

### Agent Definition Pattern

All agents follow a consistent uAgents pattern:

```python
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage, 
    TextContent, 
    StartSessionContent, 
    EndSessionContent
)

# Initialize agent with unique name
agent = Agent(name="phish_master")
protocol = Protocol()

# Message helper
def txt(s: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=str(uuid4()),
        content=[TextContent(type="text", text=s)]
    )

# Chat Protocol handler
@protocol.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    # Handle session start
    if any(isinstance(c, StartSessionContent) for c in msg.content):
        await ctx.send(sender, txt("Agent ready..."))
        return
    
    # Handle session end
    if any(isinstance(c, EndSessionContent) for c in msg.content):
        ctx.logger.info("Session ended")
        return
    
    # Process text messages
    user_text = msg.text() or ""
    # ... agent-specific logic ...
    
    await ctx.send(sender, txt(response))

# Include protocol with manifest publishing
agent.include(protocol, publish_manifest=True)
```

### Chat Protocol v0.3.0 Compliance

All agents implement **Chat Protocol v0.3.0** with:

1. **Message Structure**: `ChatMessage` with `timestamp`, `msg_id`, `content[]`
2. **Content Types**:
   - `TextContent` for text messages
   - `StartSessionContent` for session initiation
   - `EndSessionContent` for session termination
3. **Async Handlers**: All message handlers are `async` functions
4. **Manifest Publishing**: `publish_manifest=True` enables Agentverse discovery

### Message Routing & Orchestration

**Phish Master** orchestrates multi-agent workflows:

```python
# Example orchestration flow
if "finance" in user_text.lower():
    # Route to Finance Phisher (or generate directly)
    domain = "finance"
    email = generate_email_template(domain)
elif "refine" in user_text.lower():
    # Route to Phish Refiner
    response = "Sending template to Phish Refiner..."
```

**Message Flow Example**:
1. User → Phish Master: "generate finance template"
2. Phish Master → Finance Phisher: Domain-specific request
3. Finance Phisher → Phish Master: Generated template JSON
4. Phish Master → User: Aggregated response

### Safety Design

#### 1. Sanitized Outputs
- **No Real Links**: All URLs use placeholders `{{verification_link}}`
- **No Real Senders**: Email addresses are template variables `{{recipient_email}}`
- **Training Context**: All content marked "for cybersecurity training"

#### 2. Refusal Paths
All agents check for harmful requests:

```python
def is_harmful_request(text: str) -> bool:
    harmful_patterns = [
        "generate phishing", "create phishing",
        "impersonate", "spoof", "steal credentials",
        "real phishing", "actual phishing"
    ]
    # Refuse if patterns detected
```

#### 3. Audit Logs
- All agent interactions logged to `backend/logs/`
- Session tracking with unique `msg_id`
- Safety refusal events logged for review

---

## Agentverse Usage

### Hosted Deployment Model

We chose **hosted Agentverse deployment** over mailbox-only for:

1. **Public Reach**: Agents discoverable by ASI:One and other users
2. **Stability**: Hosted infrastructure ensures 24/7 availability
3. **Analytics**: Built-in rating, interaction tracking, SEO metrics
4. **Interoperability**: Standard endpoints enable cross-agent communication

### Registration Flow

Each agent registers on Agentverse with:

#### 1. **Agent Identity**
```json
{
  "agent_name": "phish_master",
  "display_name": "Phish Master Orchestrator",
  "description": "AI Orchestrator for Phishing Training Email Generation"
}
```

#### 2. **Chat Protocol Declaration**
```json
{
  "chat_protocol_version": "v0.3.0",
  "endpoints": {
    "chat": "/chat",
    "health": "/health",
    "agent_info": "/agent_info"
  }
}
```

#### 3. **SEO & Discovery Fields**
```json
{
  "tags": ["phishing", "cybersecurity", "training", "orchestrator"],
  "capabilities": [
    "phishing_template_generation",
    "agent_coordination",
    "template_aggregation"
  ],
  "sample_query": "Generate a financial phishing training email"
}
```

#### 4. **README & Documentation**
- Links to GitHub repository
- Safety statements
- Usage examples
- Technical details (framework, dependencies)

### Discovery Mechanisms

#### ASI:One Search
Agents become searchable via:
- **Name search**: "phish_master", "finance_phisher"
- **Tag search**: "phishing", "cybersecurity", "training"
- **Capability search**: "template_generation", "agent_coordination"

#### Agent-to-Agent Discovery
Other agents can discover Phisherman agents via:
```python
# Example discovery query
search_results = agent.search_agents(
    query="phishing training",
    tags=["cybersecurity", "training"]
)
```

### Interoperability

**Standard Chat Protocol** enables:
- ✅ Any Agentverse agent can call ours via `/chat` endpoint
- ✅ Our agents can call other protocol-compliant agents
- ✅ Message format standardized (ChatMessage v0.3.0)
- ✅ Session management via StartSessionContent/EndSessionContent

**Example Interoperability**:
```python
# External agent calling Phish Master
response = await ctx.send(
    "agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr",
    txt("generate finance template")
)
```

### Performance & Analytics

Agentverse provides:
- **Rating System**: Users rate agent performance (1–5 stars)
- **Interaction Metrics**: Messages sent, sessions started, error rates
- **SEO Coach**: Recommendations for better discoverability
- **Usage Analytics**: Peak hours, request patterns, domain distribution

**What We Track**:
- Template generation counts by domain (finance/health/personal)
- Refinement requests
- Session durations
- Refusal events (safety triggers)

---

## Mailbox / Inspector

### Purpose of Inspector

Fetch.ai's **Inspector** tool provides:
- **Mailbox Connection**: Bridge between local agents and Agentverse
- **Message Relay**: Routes messages to/from mailbox endpoints
- **Debugging**: Visual inspection of agent messages
- **Testing**: Verify agent responses before full registration

### Mailbox Connection Model

**Conceptual Flow**:
```
Local Agent (port 8001)
    ↓
Inspector URL (agentverse.ai/inspect)
    ↓
Mailbox Server (mailbox.fetch.ai)
    ↓
Agentverse Discovery (registered agents)
```

### Deployment Choice: Hosted vs Mailbox

**We Chose Hosted Because**:
- ✅ **Reliability**: Hosted agents stay online for demo/judging
- ✅ **Public Access**: Judges can test without local setup
- ✅ **Analytics**: Built-in metrics for scoring
- ✅ **Zero Configuration**: No Inspector setup needed

**Mailbox Alternative** (for development):
- Requires running agents locally
- Inspector URLs needed for testing
- Less reliable for public demos

---

## Endpoints & App Integration

### Server-Side Proxy Pattern

Our Flask backend acts as a **thin proxy** to hosted agents:

```python
# backend/routes/routes.py
@app.route('/api/campaign', methods=['POST'])
def email_template_route():
    template = data.get('template')
    # Call orchestration function
    email_template = orchestrate_flow(template)
    return jsonify({'success': True, 'template': email_template})
```

**Why Proxy?**
- ✅ **Security**: No API keys exposed to frontend
- ✅ **Abstraction**: Frontend doesn't need agent addresses
- ✅ **Error Handling**: Centralized error management
- ✅ **Caching**: Can cache common templates

### Public HTTPS Endpoints

Hosted agents expose standard endpoints:

```
GET  /health          → Agent health check
GET  /agent_info      → Agent metadata
POST /chat            → Chat Protocol messages
POST /generate        → Template generation (custom)
```

**Example Request**:
```bash
curl -X POST https://agentverse.ai/api/agent/phish_master/chat \
  -H "Content-Type: application/json" \
  -d '{
    "content": [{"type": "text", "text": "generate finance template"}]
  }'
```

### Event/Log Pipeline

**Diagnostics Layer**:
- `backend/diagnostics/` contains connection logs
- `backend/logs/` stores agent-specific logs
- Session tracking with unique IDs

**Safety Logs**:
- Refusal events logged
- Template exports tracked
- User interactions audited

---

## Security Model

### No Secrets in Code

**Environment-Managed Keys**:
```python
# config.py
AGENTVERSE_KEY = os.environ.get('AGENTVERSE_KEY')
ASI1_API_KEY = os.environ.get('ASI1_API_KEY', "")  # Optional
```

**Best Practices**:
- ✅ `.env` files excluded from git
- ✅ Keys loaded at runtime via `os.environ`
- ✅ No hardcoded credentials
- ✅ Separate configs for dev/prod

### Sanitized Training Content

**Template Variables**:
```json
{
  "verification_link": "{{verification_link}}",
  "recipient_name": "{{recipient_name}}",
  "recipient_email": "{{recipient_email}}"
}
```

**No Actionable Phish Content**:
- All links are placeholders
- Email addresses are template variables
- No real sender domains
- Content marked "for training purposes"

### Strict Refusal Cases

**Teacher Agent** refuses harmful requests:
```python
if is_harmful_request(user_text):
    return "I cannot generate actual phishing content. 
            I provide educational training only."
```

**All Agents** check for:
- Phishing generation requests
- Impersonation attempts
- Credential theft scenarios
- Real link/domain requests

### Audit Logs

**Logging Structure**:
```
backend/logs/
  ├── phish_master.log
  ├── finance_phisher.log
  ├── health_phisher.log
  ├── personal_phisher.log
  ├── phish_refiner.log
  └── trainer_teacher.log
```

**Logged Events**:
- All incoming messages (with msg_id)
- Refusal events (safety triggers)
- Template generation (sanitized)
- Session start/end
- Errors and exceptions

---

## Why This Qualifies for Fetch.ai Track

### 1. **Agentverse Integration** ✅
- **Hosted Agents**: All 6 agents registered on Agentverse
- **Public Discovery**: Searchable by ASI:One and other users
- **Rich Metadata**: Tags, capabilities, SEO fields, README links
- **Analytics**: Rating system, interaction metrics, performance tracking
- **Interoperability**: Standard Chat Protocol enables cross-agent communication

### 2. **uAgents Framework** ✅
- **Multi-Agent Orchestration**: Phish Master coordinates 5 agents
- **Chat Protocol v0.3.0**: Full compliance with message schema
- **Manifest Publishing**: `publish_manifest=True` enables discovery
- **Async Message Handling**: Proper async/await patterns
- **Session Management**: StartSessionContent/EndSessionContent handlers

### 3. **Real Problem & Meaningful Actions** ✅
- **Problem**: Organizations need safe phishing training without real attacks
- **Actions**: 
  - Generate sanitized training templates
  - Refine templates with constraints
  - Teach phishing detection concepts
  - Conduct interactive quizzes (+10/–10 scoring)
- **Value**: Automated workflow replaces manual template creation

### 4. **Strong Implementation** ✅
- **Stable Deployment**: Hosted agents ensure reliability
- **Proxy Integration**: Clean API for frontend/app access
- **Logging & Diagnostics**: Comprehensive audit trail
- **Safety First**: Refusal paths, sanitized outputs, audit logs
- **Testing**: Agent communication tests, quiz socket tests

### 5. **User Experience** ✅
- **Hosted Reliability**: Agents always available for demo
- **Clean API**: Simple POST requests, JSON responses
- **Terminal Demo**: CLI interface for Teacher Agent
- **Web Quiz**: Real-time scoring with WebSocket feedback
- **Exports**: Template JSON export for campaigns

### 6. **Documentation** ✅
- **README**: Comprehensive setup guide
- **Agent Docs**: Agentverse registration guides
- **API Examples**: curl commands, Postman collections
- **Screenshots**: Agentverse pages, chat interfaces
- **Diagnostics**: Connection logs, status summaries

---

## Technical Stack Summary

| Component | Technology | Version |
|-----------|-----------|---------|
| **Agent Framework** | uAgents | Latest |
| **Chat Protocol** | Chat Protocol | v0.3.0 |
| **Discovery Platform** | Agentverse | Hosted |
| **Protocol Library** | uagents_core.contrib.protocols.chat | Latest |
| **Backend** | Flask + Python | 3.11+ |
| **Frontend** | React + WebSocket | Latest |
| **Teacher Agent** | Python CLI + Socket.io | Latest |

---

## Next Steps for Judges

1. **Visit Agentverse**: Search for "phish_master" or "phishing training"
2. **Chat with Agent**: Use "Chat with Agent" feature
3. **Test Orchestration**: Request finance/health/personal templates
4. **Try Refiner**: Request template refinement
5. **Teacher Agent**: Test quiz pipeline via terminal or web UI
6. **Check Analytics**: View rating/interaction metrics on Agentverse

---

**Repository**: https://github.com/raghavgautam/phisherman  
**Track**: Fetch.ai - CalHacks 2025  
**Team**: Phisherman Team

