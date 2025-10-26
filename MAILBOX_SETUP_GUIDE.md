# 🎣 Phisherman Mailbox Setup Guide

Complete guide for setting up mailbox functionality following [Fetch.ai Agentverse Mailbox documentation](https://uagents.fetch.ai/docs/agentverse/mailbox).

## 📋 Overview

Mailbox allows agents to receive messages even when offline. Messages are stored in the mailbox and collected when agents come back online.

**Key Benefits:**
- ✅ Agents don't need to be always online
- ✅ Messages wait in mailbox until agent is available
- ✅ Works behind firewalls
- ✅ Discoverable via ASI:One

## 🚀 Quick Start

### Step 1: Verify Setup

Run the verification script:

```bash
python3 backend/scripts/verify_mailbox.py
```

This will show:
- ✅ Agent status (running/not running)
- ✅ Inspector URLs for each agent
- ✅ Mailbox connectivity test

### Step 2: All Agents Are Already Configured

All 5 agents already have `mailbox=True` configured:

- ✅ `phish_master` (port 8001)
- ✅ `finance_phisher` (port 8002)
- ✅ `health_phisher` (port 8003)
- ✅ `personal_phisher` (port 8004)
- ✅ `phish_refiner` (port 8005)

### Step 3: Register Agents via Inspector UI

For each agent, follow these steps:

1. **Click the Inspector URL** (see below)
2. **Click "Connect" button** in the Inspector UI
3. **Select "Mailbox" option**
4. **Verify registration** in Agentverse → My Agents

## 🔗 Inspector URLs

Copy and paste these URLs in your browser:

### 1. Phish Master (Orchestrator)
```
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8001&address=agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr
```

### 2. Finance Phisher
```
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8002&address=agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z
```

### 3. Health Phisher
```
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8003&address=agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h
```

### 4. Personal Phisher
```
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8004&address=agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz
```

### 5. Phish Refiner
```
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8005&address=agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr
```

## 📊 Current Status

Run this command to check agent status:

```bash
python3 backend/scripts/verify_mailbox.py
```

Expected output:
```
📊 Checking Agent Status
--------------------------------------------------------------------------------
phish_master         | Port  8001 | Code: ✅ Running
finance_phisher      | Port  8002 | Code: ✅ Running
health_phisher       | Port  8003 | Code: ✅ Running
personal_phisher     | Port  8004 | Code: ✅ Running
phish_refiner        | Port  8005 | Code: ✅ Running
```

## ✅ Success Criteria

After completing registration, you should see:

1. ✅ All agents listed in **Agentverse → My Agents**
2. ✅ Each agent has a **"Mailbox" tag**
3. ✅ Agents are discoverable via **ASI:One**
4. ✅ Agents can receive messages even when temporarily offline

## 🧪 Testing Mailbox Functionality

### Test Offline Reception

1. **Send a message** to an agent while it's running
2. **Stop the agent** (Ctrl+C)
3. **Wait 10 seconds** (messages go to mailbox)
4. **Restart the agent**
5. **Agent receives messages** from mailbox

### Expected Log Output

When an agent starts with mailbox=True, you should see:

```
INFO:     [phish_master]: Starting mailbox client for https://agentverse.ai
INFO:     [phish_master]: Mailbox access token acquired
INFO:     [phish_master]: Registration on Almanac API successful
INFO:     [phish_master]: Registering on almanac contract...
INFO:     [phish_master]: Registering on almanac contract...complete
INFO:     [mailbox]: Successfully registered as mailbox agent in Agentverse
```

## 🔧 Technical Details

### Agent Configuration

Each agent is configured with:

```python
agent = Agent(
    name="phish_master",
    seed="phish_master",
    port=8001,
    mailbox=True  # Enables mailbox functionality
)
```

### Mailbox Architecture

```
┌─────────────┐
│   Agent     │ ───────► Collects messages from mailbox
└─────────────┘
      ▲
      │ mailbox client
      │
┌─────────────┐
│  Agentverse │ ◄─────── Mailbox (stores messages)
│   Mailbox   │
└─────────────┘
      ▲
      │
┌─────────────┐
│ Other Agents│ Send messages → Mailbox → Agent
└─────────────┘
```

## 📝 Important Notes

### Dedicated Mailboxes

⚠️ **Critical**: Each agent needs its own dedicated mailbox. Don't share mailboxes between agents.

### Always-On Requirement

While mailbox allows temporary offline operation, agents still need to be:
- Running regularly to collect messages
- Accessible via their inspector URLs
- Properly registered on Agentverse

### Message Retention

Messages are stored in the mailbox until:
- Agent collects them
- Mailbox storage limit reached
- Manual cleanup

## 🐛 Troubleshooting

### Issue: Inspector URL not working

**Solution**: Ensure agent is running on the correct port:
```bash
lsof -i :8001  # Check if port is in use
```

### Issue: Mailbox connection failed

**Solution**: Check network connectivity:
```bash
curl https://agentverse.ai
```

### Issue: Messages not received

**Solution**: 
1. Verify agent has mailbox=True
2. Check agent is registered on Agentverse
3. Ensure agent has run recently to collect messages

## 📚 References

- [Fetch.ai Mailbox Documentation](https://uagents.fetch.ai/docs/agentverse/mailbox)
- [Agentverse Platform](https://agentverse.ai)
- [ASI:One Discovery](https://asi.one)
- Current setup in: `AGENT_REGISTRATION_INFO.md`

## 🎯 Next Steps

After mailbox registration:

1. **Test agent discovery** on ASI:One
2. **Send test messages** between agents
3. **Verify offline reception** (stop/restart agents)
4. **Document agent capabilities** in Agentverse
5. **Create demo workflow** showcasing mailbox functionality

---

**Status**: Ready for registration 🚀
**Last Updated**: Based on Fetch.ai Mailbox documentation v0.3.0+

