#!/bin/bash
# Smoke Tests for Agent Proxy
# Tests each agent through the proxy server

PROXY_URL="http://localhost:3000"
PROXY_KEY="your-secure-proxy-key-here"  # Update with actual key from .env

echo "🧪 Running Smoke Tests for Agent Proxy"
echo "=========================================="
echo ""

# Function to test an agent
test_agent() {
    local agent_name=$1
    local test_message=$2
    
    echo "Testing $agent_name..."
    echo "Message: $test_message"
    
    curl -X POST "$PROXY_URL/api/agent/$agent_name" \
        -H "Content-Type: application/json" \
        -H "x-proxy-key: $PROXY_KEY" \
        -d "{\"message\": \"$test_message\"}" \
        -w "\nHTTP Status: %{http_code}\n" \
        -s | jq .
    
    echo ""
    echo "---"
    echo ""
}

# Test all agents
test_agent "phish_master" "finance"
test_agent "finance_phisher" "bank"
test_agent "health_phisher" "appointment"
test_agent "personal_phisher" "social media"
test_agent "phish_refiner" "realism"

echo "✅ Smoke tests complete!"
echo ""
echo "Check diagnostics/proxy_logs/proxy_requests.log for detailed logs"

