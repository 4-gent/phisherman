# 🔗 Inspector URLs with HTTPS Tunnels

## ✅ Required: HTTPS Tunnels Running

The Inspector needs public HTTPS URLs to connect to your local agents. We're using Cloudflare tunnels.

## 🌐 Tunnel URLs

| Port | Agent | Tunnel URL |
|------|-------|------------|
| 8001 | phish_master | https://pubmed-halo-tiger-appliances.trycloudflare.com |
| 8002 | finance_phisher | https://upgrading-maximum-night-wooden.trycloudflare.com |
| 8003 | health_phisher | https://tea-privacy-humans-diesel.trycloudflare.com |
| 8004 | personal_phisher | https://moscow-moves-heart-businesses.trycloudflare.com |
| 8005 | phish_refiner | https://chairs-amendments-scenic-binding.trycloudflare.com |

## 🔗 Use These Inspector URLs

### 1. Phish Master
```
https://agentverse.ai/inspect/?uri=https%3A//pubmed-halo-tiger-appliances.trycloudflare.com&address=agent1qfpmv2htn2ghdynju29tdyt3razc0ankga79v9e07fg8m23ccmsqj33sjkr
```

### 2. Finance Phisher
```
https://agentverse.ai/inspect/?uri=https%3A//upgrading-maximum-night-wooden.trycloudflare.com&address=agent1qvunf4lkpkdfmdd92ge3phey9xyezrfn283ffsntrnrfz6cx6zakyul3k3z
```

### 3. Health Phisher
```
https://agentverse.ai/inspect/?uri=https%3A//tea-privacy-humans-diesel.trycloudflare.com&address=agent1qggxrwyhksn8ffqd5s6u0ztwq495dtqnlk95v2sg26f4slnvsw5p6nkst6h
```

### 4. Personal Phisher
```
https://agentverse.ai/inspect/?uri=https%3A//moscow-moves-heart-businesses.trycloudflare.com&address=agent1qwvljjd5a4ersv9lfj2j6apfedc74fljcjtk0smgfcf44zareuc26act6vz
```

### 5. Phish Refiner
```
https://agentverse.ai/inspect/?uri=https%3A//chairs-amendments-scenic-binding.trycloudflare.com&address=agent1q2ks99xch7w9jg69pwg7453kjlcw874g0ks59c67fzt6uq8dn7rqwh3nxrr
```

## 📝 Instructions

1. **Click each Inspector URL above** (open in new tabs)
2. **Verify agent is found** (should see agent details)
3. **Click "Connect"** button
4. **Select "Mailbox"** option
5. **Wait for success** message

## ✅ Verify Tunnels Are Running

```bash
# Check if tunnels are active
ps aux | grep cloudflared

# Check tunnel logs
tail -f diagnostics/tunnel_8001.log
```

## 🚨 If Tunnels Stop

Restart them with:
```bash
bash backend/scripts/quick_tunnels.sh
```

---

**Status**: Ready to register with HTTPS tunnels! 🚀

