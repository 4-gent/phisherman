# Terminal Chat Interface for Phisherman Agents

Chat with agents directly in your terminal, similar to Agentverse Inspector!

## 🚀 Quick Start

```bash
cd backend/phisher/agent
python3 simple_chat.py
```

## 📝 Usage

1. **Select an agent** by entering a number (1-5)
2. **Type messages** and receive responses
3. **Type 'help'** for keyword suggestions
4. **Type 'exit'** to return to agent selection
5. **Type 'q'** to quit

## 🤖 Available Agents

### 1. Phish Master (Orchestrator)
Coordinates phishing template generation across domain agents.

**Keywords:** finance, health, personal, refine

**Example:**
```
You: finance
Phish Master: I'll coordinate with the Finance Phisher to generate a financial phishing template for training.
```

### 2. Finance Phisher
Generates financial phishing templates.

**Keywords:** bank, payment, invoice, credit

**Example:**
```
You: bank
Finance Phisher: I'll generate a banking phishing template targeting account verification scenarios.
```

### 3. Health Phisher
Generates healthcare phishing templates.

**Keywords:** appointment, insurance, pharmaceutical, medical

**Example:**
```
You: appointment
Health Phisher: I'll generate a medical appointment/prescription phishing template.
```

### 4. Personal Phisher
Generates personal information phishing templates.

**Keywords:** social, email, password, identity

**Example:**
```
You: social
Personal Phisher: I'll generate a social media phishing template for account verification scenarios.
```

### 5. Phish Refiner
Refines and improves phishing templates.

**Keywords:** realism, tone, urgency, design

**Example:**
```
You: realism
Phish Refiner: I'll enhance the template's realism and believability for training purposes.
```

## 💡 Tips

- **Type 'help'** to see suggested keywords for the current agent
- Keywords are case-insensitive
- Partial keyword matching works (e.g., "finance" matches "I need finance template")
- Type 'exit' to switch agents
- Type 'q' to quit completely

## 🎯 Example Session

```
======================================================================
🤖 Phisherman Agent Terminal Chat
======================================================================

📋 Available Agents:
----------------------------------------------------------------------
1. Phish Master (Orchestrator)
   Coordinates phishing template generation across domain agents
2. Finance Phisher
   Generates financial phishing templates
...

Select an agent (1-5) or 'q' to quit: 1

======================================================================
💬 Chatting with Phish Master (Orchestrator)
======================================================================
Type 'exit' or 'quit' to end chat
Type 'help' for suggestions
----------------------------------------------------------------------

Phish Master (Orchestrator): Hello! I'm ready to help.
----------------------------------------------------------------------

You: finance
Phish Master (Orchestrator): I'll coordinate with the Finance Phisher to generate a financial phishing template for training.

You: help
💡 Message suggestions:
   • 'finance'
   • 'health'
   • 'personal'
   • 'refine'

You: exit
👋 Ending chat with Phish Master (Orchestrator)
```

## 🔧 Requirements

- Python 3.8+
- No additional dependencies (uses only stdlib)

## 📚 Notes

- This is a simplified chat interface that simulates agent responses
- Messages are processed using keyword matching
- Responses match the actual agent behavior
- Perfect for testing and demonstration

## 🆚 Comparison with Inspector

**Agentverse Inspector:**
- Requires web browser
- Connects to hosted agents
- Uses full uAgent protocol

**Terminal Chat:**
- Works in terminal
- Connects to local agents
- Uses keyword-based responses
- Fast and lightweight

Both give you the same conversational experience!

