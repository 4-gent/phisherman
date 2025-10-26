# Testing Phisherman Agents

This guide shows you how to test the simplified agents in the terminal.

## Quick Start

### 1. Start All Agents

```bash
# From the project root
python3 backend/scripts/start_all.py
```

This will start all 5 agents on ports 8001-8005.

### 2. Verify Agents Are Running

```bash
# Check agent status
python3 backend/scripts/test_chat.py
```

This will show you which agents are running and provide testing instructions.

### 3. Test Individual Agents

You can also start agents individually:

```bash
# Terminal 1 - Phish Master
cd backend/phisher/agent/phish_master
python3 main.py

# Terminal 2 - Finance Phisher
cd backend/phisher/agent/finance_phisher
python3 main.py

# Terminal 3 - Health Phisher
cd backend/phisher/agent/health_phisher
python3 main.py

# Terminal 4 - Personal Phisher
cd backend/phisher/agent/personal_phisher
python3 main.py

# Terminal 5 - Phish Refiner
cd backend/phisher/agent/phish_refiner
python3 main.py
```

## Agent Behaviors

### Phish Master (Port 8001)
- Responds to keywords: `finance`, `health`, `personal`, `refine`
- Acts as orchestrator for other agents

### Finance Phisher (Port 8002)
- Responds to keywords: `bank`, `payment`, `invoice`, `credit`
- Generates financial phishing templates

### Health Phisher (Port 8003)
- Responds to keywords: `appointment`, `insurance`, `pharmaceutical`, `medical`
- Generates healthcare phishing templates

### Personal Phisher (Port 8004)
- Responds to keywords: `social`, `email`, `password`, `identity`
- Generates personal information phishing templates

### Phish Refiner (Port 8005)
- Responds to keywords: `realism`, `tone`, `urgency`, `design`
- Refines and improves templates

## Testing with Inspector

Since these agents use the uAgent Chat Protocol, you'll need to use the Inspector UI:

1. **Start the agents** (using `start_all.py` or individually)
2. **Register agents on Agentverse** (if needed)
3. **Open Inspector** for each agent from the Agentverse dashboard
4. **Send test messages** through the Inspector UI

## Test Messages Examples

### For Phish Master:
- "generate finance template"
- "I need a health phishing template"
- "create personal phishing scenario"
- "refine my template"

### For Finance Phisher:
- "generate banking phishing template"
- "create payment verification email"
- "invoice phishing scenario"

### For Health Phisher:
- "medical appointment phishing"
- "health insurance phishing"
- "pharmaceutical safety alert"

### For Personal Phisher:
- "social media account phishing"
- "email account verification"
- "password reset phishing"

### For Phish Refiner:
- "improve realism"
- "adjust tone"
- "enhance urgency"

## Stopping Agents

Press `Ctrl+C` in the terminal where agents are running, or if using `start_all.py`, press `Ctrl+C` in that terminal.

## Logs

Agent logs are saved in `backend/logs/`:
- `phish_master.log`
- `finance_phisher.log`
- `health_phisher.log`
- `personal_phisher.log`
- `phish_refiner.log`

## Troubleshooting

### Agents Won't Start
- Check if ports 8001-8005 are already in use
- Verify Python dependencies are installed
- Check logs in `backend/logs/` for errors

### Can't Connect to Agents
- Ensure agents are running (check with `test_chat.py`)
- Verify firewall settings allow local connections
- Check that ports aren't blocked

### No Response from Agents
- Verify agents are running
- Check logs for errors
- Ensure you're using the Inspector UI (agents use uAgent protocol, not HTTP)
