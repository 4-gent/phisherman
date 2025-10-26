# Agentverse Agent Integration Guide

This guide explains how to integrate the Phisherman agents hosted on Agentverse into your application.

## 📋 Prerequisites

- Python 3.8+ OR Node.js 16+
- Agents running locally or hosted on Agentverse
- Basic understanding of REST APIs

## 🔧 Setup

### 1. Environment Configuration

Create a `.env` file in `backend/phisher/agent/`:

```bash
# Proxy Configuration
PROXY_KEY=your-secure-proxy-key-here

# Agent Endpoints (Local)
PHISH_MASTER_ENDPOINT=http://127.0.0.1:8001/submit
FINANCE_PHISHER_ENDPOINT=http://127.0.0.1:8002/submit
HEALTH_PHISHER_ENDPOINT=http://127.0.0.1:8003/submit
PERSONAL_PHISHER_ENDPOINT=http://127.0.0.1:8004/submit
PHISH_REFINER_ENDPOINT=http://127.0.0.1:8005/submit

# For Agentverse Hosted Agents (replace when available):
# PHISH_MASTER_ENDPOINT=https://agentverse.ai/api/agent/phish_master
# FINANCE_PHISHER_ENDPOINT=https://agentverse.ai/api/agent/finance_phisher
# etc.

# Proxy Server Port
PORT=3000
```

### 2. Python Proxy Setup

```bash
# Install dependencies
pip install flask requests python-dotenv

# Run the proxy server
python3 proxy_agent_server.py
```

### 3. Node.js Proxy Setup

```bash
# Install dependencies
npm install

# Run the proxy server
npm start
```

## 🚀 Usage

### API Endpoints

**Proxy Endpoint:**
```
POST /api/agent/<agent_name>
```

**Headers Required:**
- `Content-Type: application/json`
- `x-proxy-key: <your-proxy-key-from-env>`

**Request Body:**
```json
{
  "message": "your message here"
}
```

### Example: JavaScript Fetch

```javascript
// Call proxy from frontend
async function callAgent(agentName, message) {
  const response = await fetch('http://localhost:3000/api/agent/' + agentName, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-proxy-key': 'your-secure-proxy-key-here'  // Set via env, not hardcoded!
    },
    body: JSON.stringify({
      message: message
    })
  });
  
  const data = await response.json();
  return data;
}

// Usage examples
callAgent('phish_master', 'finance');
callAgent('finance_phisher', 'bank');
callAgent('health_phisher', 'appointment');
```

### Example: Python Requests

```python
import requests

def call_agent(agent_name, message):
    url = f'http://localhost:3000/api/agent/{agent_name}'
    headers = {
        'Content-Type': 'application/json',
        'x-proxy-key': 'your-secure-proxy-key-here'  # From .env
    }
    data = {'message': message}
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Usage
result = call_agent('phish_master', 'finance')
print(result)
```

### Example: cURL

```bash
# Test phish_master
curl -X POST http://localhost:3000/api/agent/phish_master \
  -H "Content-Type: application/json" \
  -H "x-proxy-key: your-secure-proxy-key-here" \
  -d '{"message": "finance"}'

# Test finance_phisher
curl -X POST http://localhost:3000/api/agent/finance_phisher \
  -H "Content-Type: application/json" \
  -H "x-proxy-key: your-secure-proxy-key-here" \
  -d '{"message": "bank"}'
```

## 🤖 Available Agents

| Agent Name | Description | Example Messages |
|------------|-------------|-------------------|
| `phish_master` | Orchestrator | "finance", "health", "personal", "refine" |
| `finance_phisher` | Financial templates | "bank", "payment", "invoice" |
| `health_phisher` | Healthcare templates | "appointment", "insurance", "medical" |
| `personal_phisher` | Personal info templates | "social media", "email", "password" |
| `phish_refiner` | Template refinement | "realism", "tone", "urgency" |

## 📊 Health Check

Check proxy status:

```bash
curl http://localhost:3000/health
```

List all agents:

```bash
curl http://localhost:3000/api/agents
```

## 🔒 Security

- **Never expose `PROXY_KEY` in frontend code**
- Always validate API key on server-side
- Use HTTPS in production
- Implement rate limiting (TODO in current implementation)
- Redact sensitive headers in logs

## 📝 Logging

All requests/responses are logged to:
- `diagnostics/proxy_logs/proxy_requests.log`

Logs include:
- Timestamp
- Agent name
- Request details (headers redacted)
- Response status and body

## 🧪 Smoke Tests

Run automated smoke tests:

```bash
cd diagnostics
chmod +x smoke_tests.sh
./smoke_tests.sh
```

## 🐛 Troubleshooting

### Agent Unreachable (503)
- Check if agent is running locally
- Verify endpoint URL in `.env`
- Check firewall settings

### Invalid API Key (401)
- Verify `PROXY_KEY` in `.env` matches header value
- Check for typos or extra spaces

### Bad Request (400)
- Ensure JSON payload is valid
- Verify message field is present

### Timeout (504)
- Agent may be slow to respond
- Check agent logs for errors
- Increase timeout in proxy code

## 📚 Additional Resources

- Agent test results: `diagnostics/agent_tests/`
- Proxy logs: `diagnostics/proxy_logs/`
- Agent addresses: See `AGENT_REGISTRATION_INFO.md`

## ⚠️ Notes

- Current implementation uses local endpoints
- Update `.env` with Agentverse hosted URLs when available
- Rate limiting is stubbed but not implemented
- Use production WSGI server (gunicorn, pm2) for production

