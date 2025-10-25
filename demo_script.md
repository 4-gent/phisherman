# 🎯 Phisherman Demo Script (60-90 seconds)

**For CalHacks 2025 - Fetch.ai Track Judges**

## Demo Flow

### 1. Introduction (10 seconds)
"Hi! I'm presenting Phisherman, an AI-powered phishing training platform built for the Fetch.ai track. We use 5 specialized AI agents to generate safe, educational phishing emails for cybersecurity training."

### 2. Show Agent Architecture (15 seconds)
"Let me show you our 5 AI agents working together:
- **Phish Master**: Orchestrates everything
- **Finance Phisher**: Creates banking phishing templates  
- **Health Phisher**: Generates healthcare phishing scenarios
- **Personal Phisher**: Develops personal info phishing templates
- **Phish Refiner**: Optimizes and improves templates"

### 3. Start All Agents (10 seconds)
```bash
./start_all.sh
```
"All agents are now running in mailbox mode for Agentverse registration."

### 4. Demonstrate Health Checks (10 seconds)
```bash
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8002/health
curl http://127.0.0.1:8003/health
curl http://127.0.0.1:8004/health
curl http://127.0.0.1:8005/health
```
"All 5 agents are responding and healthy."

### 5. Show Chat Protocol (10 seconds)
```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Generate a financial phishing template"}'
```
"Chat Protocol v0.3.0 is working - agents can communicate with each other."

### 6. Generate Phishing Template (10 seconds)
```bash
curl -X POST http://127.0.0.1:8002/generate \
  -H "Content-Type: application/json" \
  -d '{"domain": "finance", "urgency_level": 8}'
```
"Here's a financial phishing template generated for training purposes."

### 7. Show Agentverse Configs (10 seconds)
"These JSON configs are ready for Agentverse registration. Each agent has:
- Chat Protocol v0.3.0 compatibility
- Mailbox endpoint configuration  
- Safety statements for educational use
- ASI:One discovery tags"

### 8. Test ASI:One Discovery (5 seconds)
"After registration, these agents will be discoverable on ASI:One with tags like 'phishing', 'cybersecurity', 'training'."

## Key Points to Emphasize

### Technical Achievements
- ✅ **5 AI agents** working together
- ✅ **Mailbox mode** for Agentverse compatibility
- ✅ **Chat Protocol v0.3.0** compliance
- ✅ **No blockchain registration** required
- ✅ **FastAPI-based** endpoints

### Safety & Ethics
- 🛡️ **Educational purpose only**
- 🛡️ **Safe, controlled environment**
- 🛡️ **Clear training material marking**
- 🛡️ **No real phishing attacks**

### Fetch.ai Integration
- 🔗 **Agentverse registration ready**
- 🔗 **ASI:One discovery compatible**
- 🔗 **uAgents framework used**
- 🔗 **Mailbox agent pattern**

## Demo Commands Summary

```bash
# Start all agents
./start_all.sh

# Test health
curl http://127.0.0.1:8001/health

# Test chat protocol
curl -X POST http://127.0.0.1:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Generate a financial phishing template"}'

# Generate template
curl -X POST http://127.0.0.1:8002/generate \
  -H "Content-Type: application/json" \
  -d '{"domain": "finance", "urgency_level": 8}'

# Show config files
ls agentverse_configs/
```

## Backup Demo (if technical issues)

If the live demo fails:

1. **Show the code structure**: "Here's our 5-agent architecture"
2. **Show config files**: "These are ready for Agentverse registration"
3. **Show test results**: "Our verification shows all agents working"
4. **Show safety measures**: "All content is for educational training only"

## Questions to Expect

**Q: How do the agents communicate?**
A: Through Chat Protocol v0.3.0 and mailbox endpoints. The Phish Master orchestrates, domain agents generate templates, and the refiner optimizes them.

**Q: Is this safe for production?**
A: Yes, all content is clearly marked as training material. No real phishing attacks are conducted.

**Q: How does Agentverse integration work?**
A: We use mailbox mode - no blockchain registration needed. Agents are registered with JSON configs and discoverable through ASI:One.

**Q: What makes this different?**
A: We use 5 specialized AI agents working together, with proper safety measures and Fetch.ai ecosystem integration.

## Demo Success Metrics

- ✅ All 5 agents start successfully
- ✅ Health checks return 200 OK
- ✅ Chat protocol responds correctly
- ✅ Template generation works
- ✅ Agentverse configs are ready
- ✅ Safety statements are clear
