#!/bin/bash
# Stop All Phisherman Agents
# Safe stop script for mac/linux (kills only the launched processes)

echo "🛑 Stopping Phisherman Agents..."
echo "=" "============================================================================"

# Kill processes on agent ports
for port in 8001 8002 8003 8004 8005; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "Stopping process on port $port (PID: $pid)"
        kill -TERM $pid 2>/dev/null || kill -9 $pid 2>/dev/null
    else
        echo "No process found on port $port"
    fi
done

# Wait for processes to terminate
sleep 2

# Force kill any remaining processes
for port in 8001 8002 8003 8004 8005; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "Force killing process on port $port (PID: $pid)"
        kill -9 $pid 2>/dev/null
    fi
done

echo ""
echo "✅ All agents stopped"
echo "=" "============================================================================"

