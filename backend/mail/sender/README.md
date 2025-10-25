# Phisherman AI Agents - Fetch.ai Ecosystem

This directory contains the 5 AI agents for the Phisherman phishing training system, built for the Fetch.ai track at CalHacks 2025.

## 🎯 Project Overview

**Phisherman** generates safe, simulated phishing training emails for cybersecurity awareness using the Fetch.ai ecosystem (uAgents + Agentverse + ASI:One).

## 🧩 Agent Architecture

### 1. **phish_master** (Orchestrator)
- **Port**: 8001
- **Role**: Coordinates phishing template generation
- **Capabilities**: 
  - Chooses appropriate domain agents
  - Routes requests to specialized agents
  - Calls phish_refiner for adjustments
  - Aggregates final results

### 2. **finance_phisher** (Financial Domain)
- **Port**: 8002
- **Role**: Generates financial phishing templates
- **Scenarios**: Payment verification, invoices, account suspension, banking alerts
- **Templates**: Payment verification, invoice overdue, account suspension notices

### 3. **health_phisher** (Healthcare Domain)
- **Port**: 8003
- **Role**: Generates health-related phishing templates
- **Scenarios**: Appointments, medical records, insurance, test results
- **Templates**: Appointment reminders, medical records updates, insurance verification

### 4. **personal_phisher** (Personal Domain)
- **Port**: 8004
- **Role**: Generates personal information phishing templates
- **Scenarios**: Account verification, data updates, security alerts, subscriptions
- **Templates**: Account verification, profile updates, security alerts, subscription renewals

### 5. **phish_refiner** (Refinement Chatbot)
- **Port**: 8005
- **Role**: Modifies existing templates based on instructions
- **Capabilities**: Tone adjustment, urgency modification, content refinement
- **Instructions**: "increase urgency", "make more formal", "add deadline", "hr email"

## 📦 Output Format

All agents output structured JSON with the following schema:

```json
{
  "template_id": "unique_template_identifier",
  "subject": "Email subject line",
  "preheader": "Email preheader text",
  "html_body": "HTML email content",
  "plain_text_body": "Plain text email content",
  "placeholders": [
    {"name": "placeholder_name", "description": "Description of placeholder"}
  ],
  "urgency_score": 0-10,
  "safety_flags": ["flag1", "flag2"],
  "recommended_redirect": "training_link_slug"
}
```

## 🚀 Getting Started

### Prerequisites
```bash
# Install dependencies
pip install -r ../../Requirements.txt

# Ensure you have uAgents and Fetch.ai dependencies
pip install uagents>=0.4.0
```

### Running Individual Agents

```bash
# Run phish_master (orchestrator)
cd phish_master
python main.py

# Run finance_phisher
cd finance_phisher  
python main.py

# Run health_phisher
cd health_phisher
python main.py

# Run personal_phisher
cd personal_phisher
python main.py

# Run phish_refiner
cd phish_refiner
python main.py
```

### Testing Communication

```bash
# Run the communication example
python communication_example.py
```

## 🔄 Agent Communication Flow

1. **Request Received**: phish_master receives a phishing generation request
2. **Domain Routing**: phish_master routes to appropriate domain agent (finance/health/personal)
3. **Template Generation**: Domain agent generates specialized template
4. **Optional Refinement**: phish_refiner modifies template if needed
5. **Result Aggregation**: phish_master aggregates final structured JSON

## 🛡️ Safety Features

- **Safety Flags**: Each template includes safety flags for training purposes
- **Educational Focus**: Templates are designed for cybersecurity training
- **No Real Phishing**: All templates are safe simulations
- **Structured Output**: Consistent JSON format for easy processing

## 📋 Example Usage

### Generate Finance Phishing Template
```python
# Request to phish_master
{
  "domain": "finance",
  "urgency_level": 8,
  "target_audience": "general",
  "custom_requirements": "payment verification scenario"
}
```

### Refine Existing Template
```python
# Request to phish_refiner
{
  "original_template": {...},
  "refinement_instructions": "increase urgency and make more formal",
  "target_tone": "urgent",
  "urgency_adjustment": 2
}
```

## 🏗️ Agent Registration

For Agentverse registration, each agent includes:
- **Mailbox endpoints** for discovery
- **Chat Protocol v0.3.0** compatibility
- **ASI:One** discoverability
- **Structured message models** for communication

## 📁 Directory Structure

```
backend/mail/sender/
├── phish_master/
│   └── main.py
├── finance_phisher/
│   └── main.py
├── health_phisher/
│   └── main.py
├── personal_phisher/
│   └── main.py
├── phish_refiner/
│   └── main.py
├── communication_example.py
└── README.md
```

## 🎯 Hackathon Deliverables

- ✅ 4 discoverable agents on Agentverse
- ✅ Working local JSON exchange between agents
- ✅ Safe demo (no real phishing emails)
- ✅ Structured template generation
- ✅ Agent communication patterns
- ✅ Ready for Fetch.ai ecosystem integration

## 🔧 Development Notes

- Each agent runs on a different port (8001-8005)
- Agents use uAgent framework for Fetch.ai compatibility
- All templates include safety flags and educational focus
- Communication is message-based using structured models
- Ready for Agentverse registration and ASI:One discovery
