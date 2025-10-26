# Phisherman - Fetch.ai Integration One-Pager

**CalHacks 2025 - Fetch.ai Track Submission**

---

## Problem → Solution

**Problem**: Organizations need safe, realistic phishing training without exposing employees to real attacks. Manual template creation is time-consuming and inconsistent.

**Solution**: Phisherman uses **6 specialized AI agents** on Fetch.ai's **Agentverse** to automatically generate sanitized phishing training emails. Multi-agent orchestration enables domain-specific templates (finance, healthcare, personal) with refinement and educational quiz capabilities.

---

## Fetch.ai Usage

### Agentverse Platform
- ✅ **6 Hosted Agents**: phish_master, finance_phisher, health_phisher, personal_phisher, phish_refiner, teacher_agent
- ✅ **Public Discovery**: Searchable by ASI:One, tags: "phishing", "cybersecurity", "training"
- ✅ **Analytics**: Rating system, interaction metrics, SEO recommendations
- ✅ **Interoperability**: Standard Chat Protocol enables cross-agent communication

### uAgents Framework
- ✅ **Multi-Agent Orchestration**: Phish Master coordinates domain agents
- ✅ **Chat Protocol v0.3.0**: Full compliance with StartSessionContent, TextContent, EndSessionContent
- ✅ **Manifest Publishing**: `publish_manifest=True` enables Agentverse discovery
- ✅ **Async Handlers**: Proper async/await message handling

### Interoperability
- ✅ **Protocol Compliance**: Any Agentverse agent can call ours via `/chat` endpoint
- ✅ **Agent Discovery**: Can discover and call other protocol-compliant agents
- ✅ **Standard Endpoints**: `/health`, `/agent_info`, `/chat` for consistent integration

---

## System Architecture

```
┌─────────────────┐
│  React Frontend │ ──→ Flask Proxy ──→ Phish Master (Orchestrator)
└─────────────────┘                           │
                                              ├─→ Finance Phisher
                    Agentverse (Hosted)       ├─→ Health Phisher
                    Discovery & Analytics     ├─→ Personal Phisher
                                              ├─→ Phish Refiner
                                              └─→ Teacher Agent (Quiz)
```

**Chat Protocol v0.3.0** enables agent-to-agent communication  
**Safety Layer**: Refusal handlers, sanitized outputs, audit logs

---

## Key Features

### 1. Template Generation
- **Domain-Specific**: Finance, healthcare, personal information scenarios
- **Sanitized**: No real links or email addresses (placeholders only)
- **Safe for Training**: All content marked "for cybersecurity training"

### 2. Template Refinement
- **Content Optimization**: Improve urgency, clarity, structure
- **Constraint-Based**: Reduce urgency, emphasize red flags
- **Professional Tone**: Enhanced visual design and formatting

### 3. Educational Training
- **Lessons**: Teach phishing detection concepts (suspicious links, abnormal emails)
- **Interactive Quiz**: Real-time scoring (+10 correct, –10 incorrect)
- **WebSocket Integration**: Live feedback and progress tracking

### 4. Multi-Agent Orchestration
- **Request Routing**: Phish Master coordinates domain agents
- **Response Aggregation**: Combines outputs into comprehensive templates
- **Extensible Design**: Easy to add new domain agents

---

## Safety & Ethics

- ✅ **Refusal Paths**: Agents refuse harmful requests (actual phishing generation)
- ✅ **Sanitized Outputs**: All templates use placeholders (`{{verification_link}}`)
- ✅ **Audit Logs**: All interactions logged for review
- ✅ **Training Context**: Content clearly marked "for cybersecurity training"

---

## Demo Steps

1. **Agentverse Search**: Search "phish_master" → View agent page with analytics
2. **Chat with Agent**: Request "generate finance template" → Show sanitized JSON
3. **Multi-Agent Flow**: Show Phish Master routing to Finance Phisher
4. **Refinement**: Request template refinement → Show improved output
5. **Teacher Agent**: Terminal commands `teach suspicious_link`, `quiz suspicious_link`
6. **Web Quiz**: Show quiz UI with +10/–10 scoring

**Time**: 60–90 seconds | **Full Script**: `docs/fetchai_demo_script.md`

---

## Technical Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | uAgents (Latest) |
| Chat Protocol | v0.3.0 |
| Discovery Platform | Agentverse (Hosted) |
| Backend | Flask + Python 3.11+ |
| Frontend | React + WebSocket |
| Teacher Agent | Python CLI + Socket.io |

---

## Evidence & Documentation

- **Integration Guide**: `docs/fetchai_integration.md`
- **Criteria Mapping**: `docs/fetchai_criteria_mapping.md`
- **Architecture**: `docs/fetchai_architecture.md`
- **Demo Script**: `docs/fetchai_demo_script.md`
- **Evidence Checklist**: `docs/fetchai_evidence_checklist.md`

**Screenshots**: Agentverse pages, chat interfaces, quiz UI, refusal examples

---

## Why This Qualifies

1. ✅ **Agentverse**: 6 hosted agents with rich metadata, analytics, search visibility
2. ✅ **uAgents**: Multi-agent orchestration using Chat Protocol v0.3.0
3. ✅ **Interoperability**: Standard protocol enables cross-agent communication
4. ✅ **Real Problem**: Automated phishing training workflow
5. ✅ **Meaningful Actions**: Generate, refine, teach, quiz
6. ✅ **Strong Implementation**: Hosted, reliable, safe, documented

---

## Team & Repository

**Team**: Phisherman Team (CalHacks 2025)  
**Repository**: https://github.com/raghavgautam/phisherman  
**Track**: Fetch.ai  
**Demo Links**: See `docs/fetchai_evidence_checklist.md` for Agentverse URLs

---

**For judges**: See `docs/fetchai_demo_script.md` for detailed demo flow

