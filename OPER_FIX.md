# Opera/Inspector URL Fix

## 🎯 The Issue

Opera **is NOT** the problem. The issue is that Inspector URLs need **HTTPS tunnel URLs**, not localhost URLs.

Current Inspector URLs point to: `http://127.0.0.1:8001` ❌  
Required: `https://some-random-subdomain.trycloudflare.com` ✅

## ✅ The Solution

### Step 1: Start HTTPS Tunnels

Open a new terminal and run:

```bash
cd /Users/raghavgautam/Documents/GitHub/phisherman
./scripts/quick_tunnels.sh
```

This will start HTTPS tunnels for all agents. Wait for the output showing URLs like:
```
Port 8001: https://xyz-1234.trycloudflare.com
Port 8002: https://abc-5678.trycloudflare.com
...
```

### Step 2: Generate New Inspector URLs

In **another terminal**, run:

```bash
cd /Users/raghavgautam/Documents/GitHub/phisherman
python3 scripts/inspect_urls.py
```

This will create new Inspector URLs with HTTPS tunnel URLs.

### Step 3: Open in Opera (or any browser)

Open `diagnostics/inspector_urls.txt` and copy the new URLs. They should now look like:

```
https://agentverse.ai/inspect/?uri=https%3A//xyz-1234.trycloudflare.com&address=agent1...
```

### Step 4: Connect via Mailbox

1. Open the URL in Opera (or Chrome/Firefox/Safari)
2. Click "Connect" button
3. Select "Mailbox" option
4. Wait for connection
5. Copy the mailbox endpoint URL

## 🚨 Important Notes

- **Opera is fine** - The issue was localhost URLs, not Opera
- **Keep tunnels running** - Don't close the tunnel terminal until done
- **Try different browser** - If Opera still has issues, try Chrome or Firefox
- **Check firewall** - macOS firewall might block cloudflared ports

## 🔧 Alternative: Use ngrok Instead

If cloudflared doesn't work, use ngrok:

```bash
# Install ngrok (if not already)
brew install ngrok

# Start tunnel for one agent (8001)
ngrok http 8001

# Copy the HTTPS URL shown
# Repeat for other ports in separate terminals
```

## 📞 Still Having Issues?

If Opera still blocks or shows errors:
1. Try Chrome: `open -a "Google Chrome" <inspector_url>`
2. Try Firefox: `open -a Firefox <inspector_url>`
3. Try Safari: `open -a Safari <inspector_url>`
4. Check Opera's VPN/security settings - disable ad blocker temporarily

