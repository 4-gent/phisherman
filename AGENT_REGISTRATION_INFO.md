# 🎣 Phisherman Agents - Mailbox Registration Info

Following the [Fetch.ai Agentverse Mailbox approach](https://uagents.fetch.ai/docs/agentverse/mailbox)

## ✅ All 5 Agents Running Successfully

All agents are configured with `mailbox=True` and running locally. Use the Inspector URLs below to register them on Agentverse.

---

## 🤖 Agent 1: Phish Master (Orchestrator)

**Agent Details:**
- **Name:** phish_master
- **Address:** `agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr`
- **Port:** 8001
- **URL:** http://127.0.0.1:8001
- **Inspector URL:** https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8001&address=agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr

**Purpose:** Orchestrates phishing template generation across domain agents

---

## 💰 Agent 2: Finance Phisher

**Agent Details:**
- **Name:** finance_phisher
- **Address:** `agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z`
- **Port:** 8002
- **URL:** http://127.0.0.1:8002
- **Inspector URL:** https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8002&address=agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z

**Purpose:** Generates financial phishing templates (payment verification, invoices, banking alerts)

---

## 🏥 Agent 3: Health Phisher

**Agent Details:**
- **Name:** health_phisher
- **Address:** `agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h`
- **Port:** 8003
- **URL:** http://127.0.0.1:8003
- **Inspector URL:** https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8003&address=agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h

**Purpose:** Creates healthcare phishing scenarios (medical records, insurance verification)

---

## 👤 Agent 4: Personal Phisher

**Agent Details:**
- **Name:** personal_phisher
- **Address:** `agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz`
- **Port:** 8004
- **URL:** http://127.0.0.1:8004
- **Inspector URL:** https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8004&address=agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz

**Purpose:** Develops personal information phishing templates (account security, identity verification)

---

## 🔧 Agent 5: Phish Refiner

**Agent Details:**
- **Name:** phish_refiner
- **Address:** `agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr`
- **Port:** 8005
- **URL:** http://127.0.0.1:8005
- **Inspector URL:** https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8005&address=agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr

**Purpose:** Optimizes and improves phishing templates

---

## 📋 Registration Steps (from Fetch.ai Documentation)

1. **Make sure all agents are running** (they should be running on ports 8001-8005)

2. **For each agent:**
   - Click on the Inspector URL above
   - You'll be redirected to the Inspector UI
   - Click the **Connect** button
   - Select **Mailbox** option
   - The agent will register on Agentverse with a Mailbox tag

3. **Verify Registration:**
   - Go to **Agentverse → My Agents** tab
   - You should see all 5 agents listed with **Mailbox** tags
   - Agents should be discoverable via ASI:One

---

## 🎯 Quick Registration Links

Click these links directly in your browser:

1. [Phish Master Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8001&address=agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr)
2. [Finance Phisher Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8002&address=agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z)
3. [Health Phisher Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8003&address=agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h)
4. [Personal Phisher Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8004&address=agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz)
5. [Phish Refiner Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8005&address=agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr)

---

## ⚠️ Important Notes

- **Make sure agents stay running** while registering
- Each agent needs a **dedicated Mailbox** (as per Fetch.ai docs)
- Once registered, agents will collect messages from their mailboxes when online
- For a demo, you can stop and restart agents to show messages waiting in the mailbox

---

## 🔗 References

- [Fetch.ai Agentverse Mailbox Documentation](https://uagents.fetch.ai/docs/agentverse/mailbox)
- Agent logs: `backend/logs/*.log`
- All agents are listening on their respective ports and ready for registration!

