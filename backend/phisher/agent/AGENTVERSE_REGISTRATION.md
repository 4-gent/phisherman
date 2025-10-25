# Agentverse Registration Guide for Phisherman Agents

This guide explains how to register the Phisherman agents on Agentverse for discovery by ASI:One.

## 🎯 **Overview**

Agentverse is Fetch.ai's agent discovery platform. Once registered, your agents become discoverable by ASI:One and other agents in the ecosystem.

## 📋 **Prerequisites**

1. **Fetch.ai Account**: Create account at [Agentverse](https://agentverse.ai)
2. **Testnet Tokens**: Get testnet FET tokens for registration
3. **Agent Endpoints**: Ensure agents are running and accessible

## 🔧 **Step 1: Prepare Agents for Registration**

### **Agent Configuration Requirements**

Each agent needs:
- **Unique Name**: Must be globally unique
- **Description**: Clear description of capabilities
- **Endpoints**: HTTP endpoints for communication
- **Protocol**: Chat Protocol v0.3.0 compatibility
- **Metadata**: Tags, categories, and capabilities

### **Current Agent Setup**

```python
# Example agent configuration
agent = Agent(
    name="phish_master",  # Must be unique globally
    seed="phish-master-seed-key-2025",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)
```

## 🌐 **Step 2: Agentverse Registration Process**

### **2.1 Access Agentverse**
1. Go to [https://agentverse.ai](https://agentverse.ai)
2. Connect your wallet (MetaMask, etc.)
3. Switch to Fetch.ai testnet

### **2.2 Register Each Agent**

For each agent, you'll need:

#### **phish_master (Orchestrator)**
```json
{
  "name": "phish_master",
  "description": "Orchestrates phishing template generation across domain agents for cybersecurity training",
  "capabilities": [
    "phishing_template_generation",
    "agent_coordination", 
    "template_aggregation"
  ],
  "endpoints": ["http://127.0.0.1:8001/submit"],
  "protocol": "chat_v0.3.0",
  "tags": ["cybersecurity", "training", "orchestration"]
}
```

#### **finance_phisher**
```json
{
  "name": "finance_phisher",
  "description": "Generates financial phishing templates for cybersecurity training",
  "capabilities": [
    "financial_phishing_templates",
    "payment_verification_scenarios",
    "banking_alerts"
  ],
  "endpoints": ["http://127.0.0.1:8002/submit"],
  "protocol": "chat_v0.3.0",
  "tags": ["finance", "phishing", "training"]
}
```

#### **health_phisher**
```json
{
  "name": "health_phisher", 
  "description": "Generates healthcare phishing templates for cybersecurity training",
  "capabilities": [
    "healthcare_phishing_templates",
    "medical_appointments",
    "insurance_verification"
  ],
  "endpoints": ["http://127.0.0.1:8003/submit"],
  "protocol": "chat_v0.3.0",
  "tags": ["healthcare", "phishing", "training"]
}
```

#### **personal_phisher**
```json
{
  "name": "personal_phisher",
  "description": "Generates personal information phishing templates for cybersecurity training", 
  "capabilities": [
    "personal_phishing_templates",
    "account_verification",
    "security_alerts"
  ],
  "endpoints": ["http://127.0.0.1:8004/submit"],
  "protocol": "chat_v0.3.0",
  "tags": ["personal", "phishing", "training"]
}
```

#### **phish_refiner**
```json
{
  "name": "phish_refiner",
  "description": "Refines existing phishing templates based on instructions",
  "capabilities": [
    "template_refinement",
    "tone_adjustment",
    "content_modification"
  ],
  "endpoints": ["http://127.0.0.1:8005/submit"],
  "protocol": "chat_v0.3.0",
  "tags": ["refinement", "chatbot", "training"]
}
```

## 🚀 **Step 3: Registration Commands**

### **3.1 Start Agents**
```bash
# Terminal 1 - phish_master
cd backend/mail/sender/phish_master
python3 main.py

# Terminal 2 - finance_phisher  
cd backend/mail/sender/finance_phisher
python3 main.py

# Terminal 3 - health_phisher
cd backend/mail/sender/health_phisher
python3 main.py

# Terminal 4 - personal_phisher
cd backend/mail/sender/personal_phisher
python3 main.py

# Terminal 5 - phish_refiner
cd backend/mail/sender/phish_refiner
python3 main.py
```

### **3.2 Register on Agentverse**

1. **Access Agentverse Dashboard**
2. **Click "Register Agent"**
3. **Fill in agent details** (use JSON configs above)
4. **Pay registration fee** (testnet FET tokens)
5. **Verify agent is discoverable**

## 🔍 **Step 4: ASI:One Discovery Testing**

### **4.1 Test Discovery**
1. Go to [ASI:One](https://asi.one)
2. Search for your agents by name
3. Verify they appear in search results
4. Test agent communication

### **4.2 Discovery Query Example**
```python
# Example discovery query
from uagents import Agent

# Search for Phisherman agents
search_results = agent.search_agents(
    query="phishing training",
    tags=["cybersecurity", "training"]
)
```

## 📊 **Step 5: Agent Metadata Enhancement**

### **5.1 Add Rich Metadata**
```python
# Enhanced agent configuration
agent = Agent(
    name="phish_master",
    seed="phish-master-seed-key-2025", 
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
    # Enhanced metadata
    description="AI orchestrator for phishing training email generation",
    capabilities=[
        "phishing_template_generation",
        "multi_domain_coordination", 
        "template_aggregation",
        "urgency_scoring"
    ],
    tags=["cybersecurity", "training", "orchestration", "fetch.ai"],
    version="1.0.0",
    author="Phisherman Team",
    license="MIT"
)
```

### **5.2 Agent Discovery Keywords**
- **Primary**: "phishing", "training", "cybersecurity"
- **Secondary**: "email", "templates", "security", "awareness"
- **Technical**: "uagent", "fetch.ai", "agentverse"

## 🧪 **Step 6: Testing Registration**

### **6.1 Local Testing**
```bash
# Test agent endpoints
curl -X POST http://127.0.0.1:8001/submit \
  -H "Content-Type: application/json" \
  -d '{"domain": "finance", "urgency_level": 5}'
```

### **6.2 Agentverse Testing**
1. **Verify agent appears in search**
2. **Test agent communication**
3. **Verify response format**
4. **Check error handling**

## 🎯 **Step 7: Production Deployment**

### **7.1 Cloud Deployment**
- Deploy agents to cloud (AWS, GCP, Azure)
- Update endpoints to public URLs
- Configure SSL certificates
- Set up monitoring

### **7.2 Agentverse Production**
- Update agent endpoints to production URLs
- Add production metadata
- Configure rate limiting
- Set up health checks

## 📝 **Registration Checklist**

- [ ] All 5 agents running locally
- [ ] Agent endpoints accessible
- [ ] Unique agent names
- [ ] Proper descriptions and tags
- [ ] Chat Protocol v0.3.0 compatibility
- [ ] Testnet FET tokens available
- [ ] Agentverse account created
- [ ] Agents registered on Agentverse
- [ ] Discovery tested on ASI:One
- [ ] Communication tested between agents

## 🚨 **Common Issues & Solutions**

### **Issue: Agent not discoverable**
- **Solution**: Check agent name uniqueness
- **Solution**: Verify endpoint accessibility
- **Solution**: Ensure proper metadata

### **Issue: Communication failures**
- **Solution**: Check network connectivity
- **Solution**: Verify agent endpoints
- **Solution**: Test with curl commands

### **Issue: Registration failures**
- **Solution**: Ensure sufficient testnet tokens
- **Solution**: Check agent name availability
- **Solution**: Verify agent is running

## 📚 **Additional Resources**

- [Agentverse Documentation](https://docs.agentverse.ai)
- [uAgents Framework](https://docs.uagents.ai)
- [ASI:One Platform](https://asi.one)
- [Fetch.ai Testnet](https://testnet-faucet.fetch.ai)

## 🎉 **Success Criteria**

Your agents are successfully registered when:
1. ✅ All agents appear in Agentverse search
2. ✅ Agents are discoverable by ASI:One
3. ✅ Communication works between agents
4. ✅ Templates generate correctly
5. ✅ End-to-end workflow functions

---

**Next Steps**: After registration, focus on creating a comprehensive demo workflow that showcases the full agent ecosystem in action!
