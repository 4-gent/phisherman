# Fetch.ai Evidence Checklist

**Pre-judging checklist for Phisherman submission**

---

## Agent Links & IDs

### Hosted Agents on Agentverse

- [ ] **Phish Master**
  - Agentverse URL: `https://agentverse.ai/agent/phish_master`
  - Address: `agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr`
  - Port: 8001
  - Screenshot: `screenshots/phish_master_agentverse.png`

- [ ] **Finance Phisher**
  - Agentverse URL: `https://agentverse.ai/agent/finance_phisher`
  - Address: `agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z`
  - Port: 8002
  - Screenshot: `screenshots/finance_phisher_agentverse.png`

- [ ] **Health Phisher**
  - Agentverse URL: `https://agentverse.ai/agent/health_phisher`
  - Address: `agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h`
  - Port: 8003
  - Screenshot: `screenshots/health_phisher_agentverse.png`

- [ ] **Personal Phisher**
  - Agentverse URL: `https://agentverse.ai/agent/personal_phisher`
  - Address: `agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz`
  - Port: 8004
  - Screenshot: `screenshots/personal_phisher_agentverse.png`

- [ ] **Phish Refiner**
  - Agentverse URL: `https://agentverse.ai/agent/phish_refiner`
  - Address: `agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr`
  - Port: 8005
  - Screenshot: `screenshots/phish_refiner_agentverse.png`

- [ ] **Teacher Agent** (if registered)
  - Agentverse URL: `https://agentverse.ai/agent/teacher_agent`
  - Port: 8006
  - Screenshot: `screenshots/teacher_agent_agentverse.png`

---

## Chat Interface Screenshots

### Phish Master
- [ ] Screenshot: Chat interface showing "generate finance template" request
- [ ] Screenshot: Response with sanitized JSON template
- [ ] File: `screenshots/phish_master_chat.png`

### Finance Phisher
- [ ] Screenshot: Chat interface showing banking scenario request
- [ ] Screenshot: Response with financial phishing template
- [ ] File: `screenshots/finance_phisher_chat.png`

### Phish Refiner
- [ ] Screenshot: Chat interface showing refinement request
- [ ] Screenshot: Response with improved template
- [ ] File: `screenshots/phish_refiner_chat.png`

### Teacher Agent
- [ ] Screenshot: Chat interface showing "teach suspicious_link" request
- [ ] Screenshot: Response with lesson content
- [ ] File: `screenshots/teacher_agent_chat.png`

---

## Agentverse Analytics

### Rating & Interaction Metrics
- [ ] Screenshot: Phish Master rating panel (if available)
- [ ] Screenshot: Interaction metrics (messages, sessions)
- [ ] Screenshot: SEO coach recommendations
- [ ] File: `screenshots/agentverse_analytics.png`

### Search Results
- [ ] Screenshot: ASI:One search for "phishing training"
- [ ] Screenshot: Search results showing Phisherman agents
- [ ] File: `screenshots/agentverse_search.png`

---

## Protocol Compliance Evidence

### Agent Manifest
- [ ] Screenshot: `/agent_info` endpoint response
- [ ] Example:
  ```json
  {
    "name": "phish_master",
    "chat_protocol_version": "v0.3.0",
    "endpoints": {
      "chat": "/chat",
      "health": "/health"
    }
  }
  ```
- [ ] File: `screenshots/agent_manifest.png`

### ChatMessage Structure
- [ ] Code snippet: ChatMessage import and usage
- [ ] Code snippet: StartSessionContent handler
- [ ] Code snippet: TextContent handler
- [ ] Code snippet: EndSessionContent handler
- [ ] File: `screenshots/protocol_compliance.png`

---

## Interoperability Evidence

### Multi-Agent Message Flow
- [ ] Screenshot: Phish Master routing to Finance Phisher
- [ ] Log snippet: Agent-to-agent message logs
- [ ] File: `screenshots/multi_agent_flow.png`

### Cross-Agent Discovery
- [ ] Code snippet: Agent discovery query
- [ ] Screenshot: External agent calling Phish Master
- [ ] File: `screenshots/cross_agent_discovery.png`

---

## App Integration Evidence

### API Request/Response
- [ ] curl command example:
  ```bash
  curl -X POST http://localhost:8080/api/campaign \
    -H "Content-Type: application/json" \
    -d '{"template": "finance"}'
  ```
- [ ] Response JSON example:
  ```json
  {
    "success": true,
    "template": {
      "subject": "🔴 URGENT: Account Verification Required",
      "html_body": "...",
      "plain_text_body": "..."
    }
  }
  ```
- [ ] File: `screenshots/api_request_response.png`

### Postman Collection
- [ ] Postman collection file: `docs/postman_collection.json`
- [ ] Screenshot: Postman request/response
- [ ] File: `screenshots/postman_example.png`

---

## Quiz Frontend Evidence

### Quiz UI Screens
- [ ] Screenshot: Quiz question display
- [ ] Screenshot: Answer selection interface
- [ ] Screenshot: Scoreboard showing +10/–10 scoring
- [ ] Screenshot: Completed quiz session results
- [ ] File: `screenshots/quiz_ui.png`

### WebSocket Connection
- [ ] Screenshot: Browser DevTools showing WebSocket connection
- [ ] Screenshot: Socket.io events (quiz:init, quiz:question, quiz:feedback)
- [ ] File: `screenshots/websocket_connection.png`

### Terminal Demo
- [ ] Screenshot: Teacher Agent CLI
- [ ] Screenshot: `list` command output
- [ ] Screenshot: `teach suspicious_link` command output
- [ ] Screenshot: `quiz suspicious_link` command output
- [ ] File: `screenshots/teacher_cli.png`

---

## Safety Evidence

### Refusal Example
- [ ] Screenshot: Harmful request → refusal message
- [ ] Example request: "generate actual phishing email"
- [ ] Example response: "I cannot generate actual phishing content..."
- [ ] File: `screenshots/refusal_example.png`

### Sanitized Output Example
- [ ] Screenshot: Template showing placeholder URLs
- [ ] Example: `{{verification_link}}`, `{{recipient_email}}`
- [ ] Code snippet: Sanitization logic
- [ ] File: `screenshots/sanitized_output.png`

### Audit Logs
- [ ] Log snippet: Refusal events
- [ ] Log snippet: Template generation events
- [ ] Log snippet: Session tracking
- [ ] File: `screenshots/audit_logs.png`

---

## Documentation Evidence

### README Files
- [ ] Main README: `README.md`
- [ ] Agent README: `backend/phisher/agent/README.md`
- [ ] Agentverse Registration: `backend/phisher/agent/AGENTVERSE_REGISTRATION.md`
- [ ] Integration Guide: `docs/fetchai_integration.md`

### Code Examples
- [ ] Agent code: `backend/phisher/agent/phish_master/main.py`
- [ ] Protocol handlers: `backend/phisher/agent/finance_phisher/main.py`
- [ ] Quiz implementation: `frontend/src/routes/quiz.js`
- [ ] Teacher agent: `backend/trainer/teacher.py`

---

## Testing Evidence

### Agent Communication Tests
- [ ] Test script: `backend/scripts/test_agent_communication.py`
- [ ] Test results: Screenshot or log file
- [ ] File: `screenshots/agent_tests.png`

### Quiz Socket Tests
- [ ] Test spec: `tests/quiz_socket_spec.md`
- [ ] Test results: Screenshot or log file
- [ ] File: `screenshots/quiz_tests.png`

---

## Quick Screenshot Capture Script

```bash
# Capture Agentverse pages
# Requires: macOS with `screencapture` command

# Agentverse pages
screencapture -l $(pgrep -f "Safari|Chrome") screenshots/phish_master_agentverse.png
screencapture -l $(pgrep -f "Safari|Chrome") screenshots/finance_phisher_agentverse.png
screencapture -l $(pgrep -f "Safari|Chrome") screenshots/phish_refiner_agentverse.png

# Chat interfaces
screencapture -l $(pgrep -f "Safari|Chrome") screenshots/phish_master_chat.png
screencapture -l $(pgrep -f "Safari|Chrome") screenshots/finance_phisher_chat.png

# Quiz UI
screencapture -l $(pgrep -f "Safari|Chrome") screenshots/quiz_ui.png
```

---

## Pre-Submission Checklist

### Essential Screenshots (Must Have)
- [ ] At least 3 Agentverse agent pages
- [ ] At least 2 "Chat with Agent" interfaces
- [ ] 1 Quiz UI screenshot with scoring
- [ ] 1 Refusal example
- [ ] 1 Sanitized output example

### Documentation (Must Have)
- [ ] Main integration guide (`docs/fetchai_integration.md`)
- [ ] Criteria mapping (`docs/fetchai_criteria_mapping.md`)
- [ ] Demo script (`docs/fetchai_demo_script.md`)
- [ ] Architecture diagram (`docs/fetchai_architecture.md`)

### Code Evidence (Must Have)
- [ ] Agent code showing Chat Protocol v0.3.0
- [ ] Refusal handler implementation
- [ ] Sanitization logic
- [ ] Quiz WebSocket implementation

### Optional (Nice to Have)
- [ ] Agentverse analytics dashboard
- [ ] ASI:One search results
- [ ] Postman collection
- [ ] Video demo (90 seconds)

---

## Submission Package

### Files to Include
```
docs/
├── fetchai_integration.md          ✅ Main narrative
├── fetchai_criteria_mapping.md     ✅ Criteria table
├── fetchai_demo_script.md           ✅ Demo script
├── fetchai_architecture.md         ✅ Diagrams
├── fetchai_evidence_checklist.md   ✅ This file
└── fetchai_one_pager.md            ✅ Summary

screenshots/
├── phish_master_agentverse.png
├── finance_phisher_agentverse.png
├── phish_refiner_agentverse.png
├── phish_master_chat.png
├── finance_phisher_chat.png
├── quiz_ui.png
├── refusal_example.png
└── sanitized_output.png
```

---

**Status**: [ ] Ready for Submission

**Last Updated**: Before judging begins

**Next Steps**: Capture remaining screenshots, verify all links work, test demo flow

