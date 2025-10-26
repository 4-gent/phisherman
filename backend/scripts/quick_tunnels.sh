#!/bin/bash
# Quick Tunnel Start Script
# Creates HTTPS tunnels using cloudflared for all agents

echo "🌐 Starting HTTPS Tunnels"
echo "=========================="

# Kill existing tunnels
pkill cloudflared 2>/dev/null || true
pkill ngrok 2>/dev/null || true
sleep 2

mkdir -p diagnostics

# Use cloudflared for each port
PORTS=(8001 8002 8003 8004 8005)
PIDS=()

for port in "${PORTS[@]}"; do
    echo "Starting tunnel for port $port..."
    cloudflared tunnel --url http://localhost:$port > "diagnostics/tunnel_${port}.log" 2>&1 &
    PIDS+=($!)
    sleep 2
done

echo ""
echo "⏳ Waiting for tunnels to initialize..."
sleep 5

echo ""
echo "📋 Extracting tunnel URLs..."
echo ""

# Extract URLs from log files
TUNNELS='{}'
for port in "${PORTS[@]}"; do
    if [ -f "diagnostics/tunnel_${port}.log" ]; then
        URL=$(grep -o 'https://[^ ]*\.trycloudflare\.com' "diagnostics/tunnel_${port}.log" | head -1)
        if [ ! -z "$URL" ]; then
            echo "Port $port: $URL"
            TUNNELS=$(echo "$TUNNELS" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    data['$port'] = sys.stdin.read().strip()
    print(json.dumps(data))
except:
    print(sys.stdin.read())
" <<< "$URL")
        fi
    fi
done

# Save tunnels.json
echo "$TUNNELS" > diagnostics/tunnels.json

echo ""
echo "=========================="
echo "✅ Tunnels started"
echo "=========================="
echo ""
echo "Tunnel PIDs: ${PIDS[@]}"
echo ""
echo "To stop tunnels: pkill cloudflared"
echo ""
echo "Press Ctrl+C to stop..."

# Keep running
trap "echo 'Stopping tunnels...'; pkill cloudflared; exit" INT TERM
wait

