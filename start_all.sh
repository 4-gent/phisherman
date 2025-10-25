#!/bin/bash
# Start All Phisherman Agents in Mailbox Mode
# This script starts all 5 agents for Agentverse registration

echo "🎯 Starting Phisherman Agents for Agentverse Registration"
echo "=========================================================="

# Kill any existing processes on agent ports
echo "🧹 Cleaning up existing processes..."
lsof -ti:8001,8002,8003,8004,8005 | xargs kill -9 2>/dev/null || true

# Wait a moment for ports to be released
sleep 2

# Start the mailbox agent server
echo "🚀 Starting mailbox agent server..."
cd /Users/raghavgautam/Documents/GitHub/phisherman/backend/mail/sender
python3 mailbox_agent.py &

# Wait for agents to start
echo "⏳ Waiting for agents to initialize..."
sleep 5

# Test each agent
echo "🧪 Testing agent endpoints..."
for port in 8001 8002 8003 8004 8005; do
    echo -n "Testing port $port... "
    if curl -s http://127.0.0.1:$port/health > /dev/null; then
        echo "✅ OK"
    else
        echo "❌ FAILED"
    fi
done

echo ""
echo "🎉 All agents are running in mailbox mode!"
echo "=========================================================="
echo "Agent URLs:"
echo "  Phish Master:    http://127.0.0.1:8001"
echo "  Finance Phisher: http://127.0.0.1:8002"
echo "  Health Phisher:  http://127.0.0.1:8003"
echo "  Personal Phisher: http://127.0.0.1:8004"
echo "  Phish Refiner:   http://127.0.0.1:8005"
echo ""
echo "Endpoints for each agent:"
echo "  /health     - Health check"
echo "  /agent_info - Agent information for Agentverse"
echo "  /chat       - Chat Protocol v0.3.0 endpoint"
echo "  /generate   - Generate phishing templates"
echo ""
echo "Press Ctrl+C to stop all agents"
echo "=========================================================="

# Keep script running
wait
