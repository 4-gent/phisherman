#!/usr/bin/env python3
"""
Proxy Server for Agentverse Hosted Agents
Server-side proxy to communicate with uAgent agents using proper envelope format
"""

from flask import Flask, request, jsonify
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Agent endpoints from .env
AGENT_ENDPOINTS = {
    "phish_master": os.getenv("PHISH_MASTER_ENDPOINT", "http://127.0.0.1:8001/submit"),
    "finance_phisher": os.getenv("FINANCE_PHISHER_ENDPOINT", "http://127.0.0.1:8002/submit"),
    "health_phisher": os.getenv("HEALTH_PHISHER_ENDPOINT", "http://127.0.0.1:8003/submit"),
    "personal_phisher": os.getenv("PERSONAL_PHISHER_ENDPOINT", "http://127.0.0.1:8004/submit"),
    "phish_refiner": os.getenv("PHISH_REFINER_ENDPOINT", "http://127.0.0.1:8005/submit"),
}

# Proxy configuration
PROXY_KEY = os.getenv("PROXY_KEY", "change-this-key-in-production")
RATE_LIMIT_PER_MINUTE = 60  # TODO: Implement rate limiting

def log_request(agent_name: str, request_data: dict, response_data: dict, status_code: int):
    """Log requests/responses to file, redacting sensitive headers"""
    log_dir = "diagnostics/proxy_logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "request": {
            "method": request.method,
            "url": request.url,
            "headers": {k: v for k, v in request.headers if k != "Authorization"},
            "body": request_data
        },
        "response": {
            "status_code": status_code,
            "body": response_data
        }
    }
    
    with open(f"{log_dir}/proxy_requests.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def create_uagent_envelope(message_content: dict, recipient_address: str = "agent1wzx2akp7cfv"):
    """Create uAgent envelope format with ChatMessage"""
    from uuid import uuid4
    
    # Create proper ChatMessage structure
    chat_message = {
        "timestamp": datetime.utcnow().isoformat(),
        "msg_id": str(uuid4()),
        "content": [
            {
                "type": "text",
                "text": message_content.get("message", message_content.get("text", ""))
            }
        ]
    }
    
    # Wrap in envelope for uAgent
    return {
        "sender": "proxy_server",
        "recipient": recipient_address,
        "message": chat_message
    }

@app.route('/api/agent/<agent_name>', methods=['POST'])
def proxy_agent(agent_name):
    """Proxy endpoint for agent communication"""
    
    # Validate API key
    api_key = request.headers.get('x-proxy-key')
    if not api_key or api_key != PROXY_KEY:
        return jsonify({"error": "Unauthorized - Invalid or missing x-proxy-key header"}), 401
    
    # Validate agent name
    if agent_name not in AGENT_ENDPOINTS:
        return jsonify({"error": f"Unknown agent: {agent_name}"}), 404
    
    # Get request data
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "Invalid JSON payload"}), 400
    except:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    # Get agent endpoint
    agent_endpoint = AGENT_ENDPOINTS[agent_name]
    
    # Create uAgent envelope
    envelope = create_uagent_envelope(request_data)
    
    # Forward request to agent
    try:
        response = requests.post(
            agent_endpoint,
            json=envelope,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Parse response
        try:
            response_data = response.json()
        except:
            response_data = {"text": response.text}
        
        # Log request/response
        log_request(agent_name, request_data, response_data, response.status_code)
        
        # Return response
        return jsonify({
            "agent": agent_name,
            "status": response.status_code,
            "data": response_data
        }), response.status_code
        
    except requests.exceptions.Timeout:
        error_data = {"error": "Agent request timeout"}
        log_request(agent_name, request_data, error_data, 504)
        return jsonify(error_data), 504
        
    except requests.exceptions.ConnectionError:
        error_data = {"error": "Agent endpoint unreachable"}
        log_request(agent_name, request_data, error_data, 503)
        return jsonify(error_data), 503
        
    except Exception as e:
        error_data = {"error": str(e)}
        log_request(agent_name, request_data, error_data, 500)
        return jsonify(error_data), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "proxy": "active",
        "agents_configured": list(AGENT_ENDPOINTS.keys())
    })

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List available agents"""
    return jsonify({
        "agents": list(AGENT_ENDPOINTS.keys()),
        "endpoints": AGENT_ENDPOINTS
    })

if __name__ == '__main__':
    print("🚀 Starting Agent Proxy Server")
    print(f"Proxy Key: {PROXY_KEY[:10]}...")
    print(f"Agents: {', '.join(AGENT_ENDPOINTS.keys())}")
    print("API: POST /api/agent/<agent_name>")
    print("Health: GET /health")
    print("\n⚠️  Note: This is a development server. Use a production WSGI server for production.")
    
    app.run(host='0.0.0.0', port=3000, debug=True)

