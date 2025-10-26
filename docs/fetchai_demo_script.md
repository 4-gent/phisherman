# Phisherman Demo Script for Judges

**60–90 second live demonstration of Fetch.ai integration**

---

## Pre-Demo Setup (Before Judging)

1. ✅ Open Agentverse in browser: https://agentverse.ai
2. ✅ Open terminal with Teacher Agent ready: `cd backend/trainer && python cli.py`
3. ✅ Open web quiz in browser: `http://localhost:3000/quiz?topic=suspicious_link`
4. ✅ Have Agentverse agent URLs ready:
   - Phish Master: `https://agentverse.ai/agent/phish_master`
   - Finance Phisher: `https://agentverse.ai/agent/finance_phisher`
   - Phish Refiner: `https://agentverse.ai/agent/phish_refiner`

---

## Demo Script (90 seconds)

### Opening (10 seconds)

> "Hi! I'm showing you **Phisherman**, a cybersecurity training platform built with Fetch.ai's **uAgents** and **Agentverse**. We have 6 AI agents working together to generate safe phishing training emails."

### Step 1: Agentverse Search & Analytics (20 seconds)

**Action**:
- Open Agentverse search
- Type "phish_master"
- Click on Phish Master agent page

**Say**:
> "Here's our **Phish Master** orchestrator agent registered on Agentverse. Notice the rating panel and analytics—this shows agent performance metrics."

**Highlight**:
- ✅ Agent page visible
- ✅ Rating/analytics panel
- ✅ Search discoverability
- ✅ Rich metadata (tags, capabilities, README)

---

### Step 2: Chat with Agent - Generate Template (25 seconds)

**Action**:
- Click "Chat with Agent" on Phish Master page
- Type: `generate finance template`
- Show response with sanitized JSON

**Say**:
> "Let me request a finance phishing template. Notice the response is **sanitized**—no real links or email addresses, just placeholders. This is safe for training."

**Highlight**:
- ✅ Chat Protocol v0.3.0 interface
- ✅ Real-time agent response
- ✅ Sanitized output (placeholders)
- ✅ JSON structure for templates

**Response Should Show**:
```json
{
  "subject": "🔴 URGENT: Account Verification Required",
  "html_body": "... {{verification_link}} ...",
  "plain_text_body": "... {{verification_link}} ..."
}
```

---

### Step 3: Multi-Agent Orchestration (15 seconds)

**Action**:
- Show how Phish Master routes to Finance Phisher
- Or show Finance Phisher agent page

**Say**:
> "Phish Master orchestrates across domain agents. Here's the **Finance Phisher**—notice it's a separate agent that Phish Master can call via Chat Protocol."

**Highlight**:
- ✅ Multi-agent architecture
- ✅ Agent-to-agent communication
- ✅ Protocol interoperability

---

### Step 4: Refinement with Phish Refiner (10 seconds)

**Action**:
- Open Phish Refiner agent page
- Click "Chat with Agent"
- Request: `refine the template to reduce urgency`

**Say**:
> "We can refine templates with our **Phish Refiner** agent—it improves clarity, reduces urgency, adds red flags."

**Highlight**:
- ✅ Refinement workflow
- ✅ Content optimization
- ✅ Constraint-based editing

---

### Step 5: Teacher Agent - Quiz Pipeline (15 seconds)

**Action**:
- Switch to terminal
- Show Teacher Agent commands:
  ```
  > list
  > teach suspicious_link
  > quiz suspicious_link
  ```

**Say**:
> "Our **Teacher Agent** provides educational lessons and quizzes. You can see it teaches concepts like suspicious links, then quizzes users."

**Highlight**:
- ✅ Educational content
- ✅ Interactive quiz
- ✅ Concept teaching

---

### Step 6: Web Quiz with Scoring (10 seconds)

**Action**:
- Switch to browser showing quiz UI
- Show quiz question and socket connection
- Show +10/–10 scoring display

**Say**:
> "The web quiz uses WebSocket for real-time scoring—+10 for correct, –10 for incorrect. This tracks training progress."

**Highlight**:
- ✅ Real-time WebSocket integration
- ✅ Scoring system (+10/–10)
- ✅ User progress tracking

---

### Closing - Agentverse Advantages (10 seconds)

**Say**:
> "**Why Agentverse?** Our agents are **hosted** for reliability, **discoverable** by ASI:One, **interoperable** with other agents via Chat Protocol, and **measurable** with analytics. Thank you!"

**Key Points**:
- ✅ Hosted: 24/7 availability
- ✅ Discoverable: Searchable on ASI:One
- ✅ Interoperable: Standard Chat Protocol
- ✅ Measurable: Rating & analytics

---

## Alternative Short Demo (60 seconds)

If time is limited, skip Steps 3–4 and focus on:

1. **Agentverse Page** (15s) - Show Phish Master with analytics
2. **Chat with Agent** (20s) - Generate finance template, show sanitized output
3. **Teacher Agent** (15s) - Quick `teach` and `quiz` commands
4. **Web Quiz** (10s) - Show scoring system

---

## Troubleshooting

### If Agentverse is Slow
- Have screenshots ready of agent pages
- Show pre-recorded demo video

### If Chat Interface Doesn't Load
- Use curl command instead:
  ```bash
  curl -X POST https://agentverse.ai/api/agent/phish_master/chat \
    -H "Content-Type: application/json" \
    -d '{"content": [{"type": "text", "text": "generate finance template"}]}'
  ```

### If Teacher Agent Fails
- Show quiz UI instead
- Explain the CLI interface conceptually

---

## Key Talking Points to Emphasize

1. **"6 Agents"**: Phish Master + 5 specialists (Finance, Health, Personal, Refiner, Teacher)
2. **"Chat Protocol v0.3.0"**: Standard message format for interoperability
3. **"Sanitized"**: No real phishing content—safe for training
4. **"Orchestration"**: Phish Master coordinates multiple agents
5. **"Analytics"**: Agentverse provides rating/interaction metrics
6. **"Hosted"**: Reliability for demos and production use

---

## Post-Demo Checklist

- [ ] Confirm judges saw Agentverse page
- [ ] Confirm judges saw chat interface
- [ ] Confirm judges saw sanitized output
- [ ] Confirm judges understood multi-agent flow
- [ ] Answer any questions about:
  - Safety mechanisms
  - Protocol compliance
  - Interoperability
  - Analytics/metrics

---

**Demo Materials Ready?**
- ✅ Agentverse URLs bookmarked
- ✅ Terminal with Teacher Agent ready
- ✅ Web quiz open in browser
- ✅ Screenshots backup prepared
- ✅ Key talking points memorized

