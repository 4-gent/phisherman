#!/bin/bash
# Start HTTPS Tunnels for All Agents
# Supports ngrok and Cloudflare Tunnel (cloudflared)

echo "🌐 Starting HTTPS Tunnels for Phisherman Agents"
echo "=========================================================="

TUNNEL_TYPE="ngrok"  # Options: ngrok, cloudflare

# Check for tunnel software
if command -v ngrok &> /dev/null; then
    TUNNEL_TYPE="ngrok"
    echo "✅ Found ngrok"
elif command -v cloudflared &> /dev/null; then
    TUNNEL_TYPE="cloudflare"
    echo "✅ Found cloudflared"
else
    echo "❌ No tunnel software found. Please install ngrok or cloudflared"
    echo "   ngrok: https://ngrok.com/download"
    echo "   cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation"
    exit 1
fi

echo "Using: $TUNNEL_TYPE"
echo ""

# Create tunnels.json
TUNNELS_FILE="diagnostics/tunnels.json"
mkdir -p diagnostics
echo "{}" > $TUNNELS_FILE

# Start tunnels for each port
PORTS=(8001 8002 8003 8004 8005)
TUNNEL_PIDS=()

for port in "${PORTS[@]}"; do
    echo "Starting tunnel for port $port..."
    
    if [ "$TUNNEL_TYPE" == "ngrok" ]; then
        # Start ngrok tunnel
        ngrok http $port > "diagnostics/ngrok_${port}.log" 2>&1 &
        PID=$!
        TUNNEL_PIDS+=($PID)
        
        # Wait for ngrok to start
        sleep 3
        
        # Get ngrok tunnel URL
        NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')" 2>/dev/null)
        
        if [ ! -z "$NGROK_URL" ]; then
            echo "  ✅ Tunnel started: $NGROK_URL"
            # Update tunnels.json
            python3 -c "import json; data=json.load(open('$TUNNELS_FILE')); data['$port']='$NGROK_URL'; json.dump(data, open('$TUNNELS_FILE', 'w'), indent=2)"
        else
            echo "  ⚠️  Could not get tunnel URL"
        fi
        
    elif [ "$TUNNEL_TYPE" == "cloudflare" ]; then
        # Start cloudflared tunnel
        cloudflared tunnel --url http://localhost:$port > "diagnostics/cloudflare_${port}.log" 2>&1 &
        PID=$!
        TUNNEL_PIDS+=($PID)
        
        # Wait for cloudflared to start
        sleep 3
        
        # Extract URL from log
        CLOUDFLARE_URL=$(grep -o 'https://[^ ]*\.trycloudflare\.com' "diagnostics/cloudflare_${port}.log" | head -1)
        
        if [ ! -z "$CLOUDFLARE_URL" ]; then
            echo "  ✅ Tunnel started: $CLOUDFLARE_URL"
            # Update tunnels.json
            python3 -c "import json; data=json.load(open('$TUNNELS_FILE')); data['$port']='$CLOUDFLARE_URL'; json.dump(data, open('$TUNNELS_FILE', 'w'), indent=2)"
        else
            echo "  ⚠️  Could not get tunnel URL"
        fi
    fi
    
    sleep 1
done

echo ""
echo "=========================================================="
echo "✅ Tunnels started"
echo "=========================================================="
echo ""
echo "Tunnel PIDs: ${TUNNEL_PIDS[@]}"
echo ""
echo "Press Ctrl+C to stop all tunnels"
echo ""

# Wait for user interrupt
trap "echo 'Stopping tunnels...'; kill ${TUNNEL_PIDS[@]} 2>/dev/null; exit" INT TERM

# Keep script running
wait

