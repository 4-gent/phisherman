# 🚀 Quick Start: Mailbox Registration

## ✅ Current Status

All 5 agents are **ready for mailbox registration**!

### Agents Running
- ✅ phish_master (port 8001)
- ✅ finance_phisher (port 8002)
- ✅ health_phisher (port 8003)
- ✅ personal_phisher (port 8004)
- ✅ phish_refiner (port 8005)

### Configuration
- ✅ All agents have `mailbox=True`
- ✅ All agents use Chat Protocol v0.3.0
- ✅ All agents have unique addresses

## 🎯 Action Required

**You need to manually register each agent via the Inspector UI** (this is by design according to Fetch.ai docs).

### Registration Steps (Repeat for Each Agent)

1. Click the Inspector URL below
2. Click **"Connect"** button
3. Select **"Mailbox"** option
4. Verify in Agentverse → My Agents

## 🔗 Click These URLs

### [Phish Master Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8001&address=agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr)

### [Finance Phisher Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8002&address=agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z)

### [Health Phisher Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8003&address=agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h)

### [Personal Phisher Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8004&address=agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz)

### [Phish Refiner Inspector](https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8005&address=agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr)

## 📋 Verification

Run this command anytime to check status:

```bash
python3 backend/scripts/verify_mailbox.py
```

## 📚 Full Documentation

See `MAILBOX_SETUP_GUIDE.md` for complete details.

## 🎉 After Registration

Once all agents are registered:
- ✅ Appear in Agentverse → My Agents with "Mailbox" tag
- ✅ Discoverable via ASI:One
- ✅ Can receive messages when offline
- ✅ Messages stored in mailbox until collected

---

**Reference**: [Fetch.ai Mailbox Documentation](https://uagents.fetch.ai/docs/agentverse/mailbox)

