# Phisherman Agent Management Scripts

This directory contains scripts for managing and operating the Phisherman agents with Fetch.ai Mailbox + Agentverse integration.

## Scripts Overview

### Agent Management
- **start_all.py** - Launch all 5 agents in subprocesses with log streaming
- **stop_all.sh** - Safely stop all agents (macOS/Linux)

### Diagnostics & Inspection
- **ports_status.py** - Check Port → PID → Listening status
- **inspect_urls.py** - Generate Inspector URLs for agent connection
- **verify_chat.py** - Verify Chat Protocol functionality

### Tunnel Management
- **tunnels_start.sh** - Start HTTPS tunnels (ngrok or Cloudflare)

### Agentverse Integration
- **update_agentverse_endpoints.py** - Update Agentverse with mailbox endpoints

## Usage

### Start All Agents
```bash
python3 scripts/start_all.py
```

### Stop All Agents
```bash
./scripts/stop_all.sh
```

### Check Port Status
```bash
python3 scripts/ports_status.py
```

### Start HTTPS Tunnels
```bash
./scripts/tunnels_start.sh
```

### Generate Inspector URLs
```bash
python3 scripts/inspect_urls.py
```

### Verify Chat Protocol
```bash
python3 scripts/verify_chat.py
```

### Update Agentverse Endpoints
```bash
python3 scripts/update_agentverse_endpoints.py
```

## Workflow

1. **Start agents**: `python3 scripts/start_all.py`
2. **Check status**: `python3 scripts/ports_status.py`
3. **Start tunnels**: `./scripts/tunnels_start.sh`
4. **Generate Inspector URLs**: `python3 scripts/inspect_urls.py`
5. **Connect via Inspector**: Open URLs, connect via Mailbox
6. **Update Agentverse**: Provide mailbox endpoints, run update script
7. **Verify**: `python3 scripts/verify_chat.py`

## Output Files

All diagnostics are saved to `diagnostics/` directory:
- `ports_status.txt` - Port status report
- `inspector_urls.txt` - Inspector URLs for each agent
- `tunnels.json` - HTTPS tunnel URLs
- `mailbox_verify.txt` - Chat verification results
- `agentverse_update.txt` - Update instructions

## Agent Configuration

- **phish_master**: Port 8001
- **finance_phisher**: Port 8002
- **health_phisher**: Port 8003
- **personal_phisher**: Port 8004
- **phish_refiner**: Port 8005

All agents use:
- Chat Protocol v0.3.0
- Mailbox enabled
- uAgents framework

