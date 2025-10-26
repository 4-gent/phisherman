#!/usr/bin/env python3
"""
Mailbox Agent Implementation for Agentverse Registration
This creates mailbox-compatible agents that can be registered on Agentverse
"""

import json
import asyncio
import threading
import time
from typing import Dict, Any, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

# Agent configurations
AGENTS_CONFIG = {
    "phish_master": {
        "name": "Phish Master Orchestrator",
        "port": 8001,
        "description": "Orchestrates phishing template generation across domain agents",
        "capabilities": ["phishing_template_generation", "agent_coordination", "template_aggregation"]
    },
    "finance_phisher": {
        "name": "Finance Phisher Agent",
        "port": 8002,
        "description": "Generates financial phishing templates for cybersecurity training",
        "capabilities": ["financial_phishing_templates", "payment_verification_scenarios", "banking_alerts"]
    },
    "health_phisher": {
        "name": "Health Phisher Agent",
        "port": 8003,
        "description": "Generates healthcare phishing templates for cybersecurity training",
        "capabilities": ["healthcare_phishing_templates", "medical_records_scenarios", "health_alerts"]
    },
    "personal_phisher": {
        "name": "Personal Phisher Agent",
        "port": 8004,
        "description": "Generates personal information phishing templates for cybersecurity training",
        "capabilities": ["personal_phishing_templates", "identity_verification_scenarios", "account_security"]
    },
    "phish_refiner": {
        "name": "Phish Refiner Agent",
        "port": 8005,
        "description": "Refines and improves phishing templates for better training effectiveness",
        "capabilities": ["template_refinement", "tone_adjustment", "content_optimization"]
    }
}

class ChatMessage(BaseModel):
    text: str
    sender: str = "user"

class PhishingRequest(BaseModel):
    domain: str
    urgency_level: int = 5
    target_audience: str = "general"
    custom_requirements: str = ""

class PhishingResponse(BaseModel):
    template_id: str
    subject: str
    preheader: str
    html_body: str
    plain_text_body: str
    placeholders: List[Dict[str, str]]
    urgency_score: int
    safety_flags: List[str]
    recommended_redirect: str
    domain_used: str
    generated_by: str

def create_agent_app(agent_name: str, config: Dict[str, Any]) -> FastAPI:
    """Create a FastAPI app for a specific agent"""
    app = FastAPI(title=f"{config['name']} API", version="1.0.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "ok", "agent": agent_name, "version": "1.0.0"}
    
    @app.get("/agent_info")
    async def agent_info():
        """Agent information endpoint for Agentverse registration"""
        return {
            "name": config["name"],
            "description": config["description"],
            "capabilities": config["capabilities"],
            "chat_protocol_version": "v0.3.0",
            "endpoints": {
                "chat": f"/chat",
                "health": f"/health",
                "generate": f"/generate"
            }
        }
    
    @app.post("/chat")
    async def chat_endpoint(message: ChatMessage):
        """Chat Protocol v0.3.0 compatible endpoint"""
        try:
            # Process the chat message
            response_text = await process_chat_message(agent_name, message.text)
            return {
                "text": response_text,
                "agent": agent_name,
                "timestamp": time.time()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/generate")
    async def generate_endpoint(request: PhishingRequest):
        """Generate phishing template endpoint"""
        try:
            template = await generate_phishing_template(agent_name, request)
            return template
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return app

async def process_chat_message(agent_name: str, message: str) -> str:
    """Process chat messages based on agent type"""
    
    if agent_name == "phish_master":
        return f"Phish Master: I'll coordinate with domain agents to generate a phishing template for: {message}"
    
    elif agent_name == "finance_phisher":
        return f"Finance Phisher: I'll create a financial phishing template for: {message}"
    
    elif agent_name == "health_phisher":
        return f"Health Phisher: I'll create a healthcare phishing template for: {message}"
    
    elif agent_name == "personal_phisher":
        return f"Personal Phisher: I'll create a personal information phishing template for: {message}"
    
    elif agent_name == "phish_refiner":
        return f"Phish Refiner: I'll refine and improve the phishing template: {message}"
    
    else:
        return f"Unknown agent: {message}"

async def generate_phishing_template(agent_name: str, request: PhishingRequest) -> Dict[str, Any]:
    """Generate phishing templates based on agent type"""
    
    base_template = {
        "template_id": f"{agent_name}_{request.domain}_{int(time.time())}",
        "subject": f"Urgent: {request.domain.title()} Verification Required",
        "preheader": "Your account needs immediate attention",
        "html_body": f"<html><body><h2>{request.domain.title()} Verification Required</h2><p>Please verify your information.</p></body></html>",
        "plain_text_body": f"{request.domain.title()} Verification Required\n\nPlease verify your information.",
        "placeholders": [
            {"name": "recipient_name", "description": "Target's full name"},
            {"name": "verification_link", "description": "Training verification link"}
        ],
        "urgency_score": request.urgency_level,
        "safety_flags": ["requests_verification", "urgent_action_required"],
        "recommended_redirect": f"training_{request.domain}_verification",
        "domain_used": request.domain,
        "generated_by": agent_name
    }
    
    # Customize based on agent type
    if agent_name == "finance_phisher":
        base_template.update({
            "subject": "Urgent: Payment Verification Required",
            "preheader": "Your payment information needs verification",
            "safety_flags": ["requests_payment_info", "urgent_action_required"]
        })
    elif agent_name == "health_phisher":
        base_template.update({
            "subject": "Medical Records Update Required",
            "preheader": "Your health information needs verification",
            "safety_flags": ["requests_medical_data", "personal_information"]
        })
    elif agent_name == "personal_phisher":
        base_template.update({
            "subject": "Account Security Verification",
            "preheader": "Secure your account immediately",
            "safety_flags": ["requests_personal_info", "security_alert"]
        })
    elif agent_name == "phish_refiner":
        base_template.update({
            "subject": "Refined: Security Verification Required",
            "preheader": "Enhanced security verification needed",
            "safety_flags": ["refined_template", "enhanced_security"]
        })
    
    return base_template

def start_agent_server(agent_name: str, config: Dict[str, Any]):
    """Start a single agent server"""
    app = create_agent_app(agent_name, config)
    port = config["port"]
    
    print(f"🚀 Starting {config['name']} on port {port}")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    except Exception as e:
        print(f"❌ Error starting {agent_name}: {e}")

def start_all_agents():
    """Start all agents in separate threads"""
    threads = []
    
    for agent_name, config in AGENTS_CONFIG.items():
        thread = threading.Thread(
            target=start_agent_server,
            args=(agent_name, config),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        time.sleep(1)  # Stagger startup
    
    print("🎯 All Phisherman agents started in mailbox mode")
    print("=" * 60)
    print("Available agents:")
    for agent_name, config in AGENTS_CONFIG.items():
        print(f"  {config['name']}: http://127.0.0.1:{config['port']}")
    print("=" * 60)
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all agents...")

if __name__ == "__main__":
    start_all_agents()
