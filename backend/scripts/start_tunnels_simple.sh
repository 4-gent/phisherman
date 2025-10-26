#!/bin/bash
# Start HTTPS Tunnels - Simple Version
# This creates tunnels for each agent port

echo "🌐 Starting HTTPS Tunnels for Phisherman Agents"
echo "=========================================================="

# Kill any existing ngrok processes
pkill ngrok 2>/dev/null || true
sleep 2

# Create tunnels directory if needed
mkdir -p diagnostics

echo "Starting ngrok tunnels..."
echo ""

# Start ngrok tunnels in background for each port
for port in 8001 8002 8003 8004 8005; do
    echo "Starting tunnel for port $port..."
    ngrok http $port > "diagnostics/ngrok_${port}.log" 2>&1 &
    sleep 3
done

echo ""
echo "⏳ Waiting for tunnels to initialize..."
sleep 5

echo ""
echo "Fetching tunnel URLs..."
echo ""

# Get tunnel URLs from ngrok API
TUNNELS='{}'
for port in 8001 8002 8003 8004 8005; do
    # Try to get URL from ngrok API
    URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'tunnels' in data and len(data['tunnels']) > 0:
        print(data['tunnels'][0]['public_url'])
except:
    pass
" 2>/dev/null || echo "")
    
    if [ ! -z "$URL" ]; then
        echo "  Port $port: $URL"
        TUNNELS=$(echo "$TUNNELS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
data['$port'] = sys.stdin.read().strip()
print(json.dumps(data))
" <<< "$URL")
    else
        echo "  Port $port: Could not fetch URL"
    fi
done

# Save to tunnels.json
echo "$TUNNELS" > diagnostics/tunnels.json

echo ""
echo "=========================================================="
echo "✅ Tunnels started"
echo "=========================================================="
echo ""
echo "📋 Tunnel URLs saved to: diagnostics/tunnels.json"
echo ""
echo "Press Ctrl+C to stop all tunnels"
echo ""

# Keep script running
wait

