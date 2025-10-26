#!/usr/bin/env node
/**
 * Proxy Server for Agentverse Hosted Agents
 * Server-side proxy to communicate with uAgent agents using proper envelope format
 */

const express = require('express');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(express.json());

// Agent endpoints from .env
const AGENT_ENDPOINTS = {
    phish_master: process.env.PHISH_MASTER_ENDPOINT || 'http://127.0.0.1:8001/submit',
    finance_phisher: process.env.FINANCE_PHISHER_ENDPOINT || 'http://127.0.0.1:8002/submit',
    health_phisher: process.env.HEALTH_PHISHER_ENDPOINT || 'http://127.0.0.1:8003/submit',
    personal_phisher: process.env.PERSONAL_PHISHER_ENDPOINT || 'http://127.0.0.1:8004/submit',
    phish_refiner: process.env.PHISH_REFINER_ENDPOINT || 'http://127.0.0.1:8005/submit',
};

// Proxy configuration
const PROXY_KEY = process.env.PROXY_KEY || 'change-this-key-in-production';
const RATE_LIMIT_PER_MINUTE = 60; // TODO: Implement rate limiting

/**
 * Log requests/responses to file, redacting sensitive headers
 */
function logRequest(agentName, requestData, responseData, statusCode, req) {
    const logDir = 'diagnostics/proxy_logs';
    if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
    }

    const logEntry = {
        timestamp: new Date().toISOString(),
        agent: agentName,
        request: {
            method: req.method,
            url: req.url,
            headers: Object.fromEntries(
                Object.entries(req.headers).filter(([k]) => k !== 'authorization')
            ),
            body: requestData
        },
        response: {
            status_code: statusCode,
            body: responseData
        }
    };

    fs.appendFileSync(
        path.join(logDir, 'proxy_requests.log'),
        JSON.stringify(logEntry) + '\n'
    );
}

/**
 * Create uAgent envelope format
 */
function createUAgentEnvelope(messageContent) {
    const { v4: uuidv4 } = require('uuid');

    return {
        sender: 'proxy_server',
        recipient: 'agent1wzx2akp7cfv', // Default recipient
        message: {
            timestamp: new Date().toISOString(),
            msg_id: uuidv4(),
            content: [
                {
                    type: 'text',
                    text: messageContent.message || messageContent.text || ''
                }
            ]
        }
    };
}

/**
 * Proxy endpoint for agent communication
 */
app.post('/api/agent/:agentName', async (req, res) => {
    const agentName = req.params.agentName;

    // Validate API key
    const apiKey = req.headers['x-proxy-key'];
    if (!apiKey || apiKey !== PROXY_KEY) {
        return res.status(401).json({
            error: 'Unauthorized - Invalid or missing x-proxy-key header'
        });
    }

    // Validate agent name
    if (!AGENT_ENDPOINTS[agentName]) {
        return res.status(404).json({
            error: `Unknown agent: ${agentName}`
        });
    }

    // Get request data
    const requestData = req.body;
    if (!requestData) {
        return res.status(400).json({
            error: 'Invalid JSON payload'
        });
    }

    // Get agent endpoint
    const agentEndpoint = AGENT_ENDPOINTS[agentName];

    // Create uAgent envelope
    const envelope = createUAgentEnvelope(requestData);

    // Forward request to agent
    try {
        const response = await axios.post(agentEndpoint, envelope, {
            headers: { 'Content-Type': 'application/json' },
            timeout: 30000
        });

        // Parse response
        let responseData;
        try {
            responseData = response.data;
        } catch (e) {
            responseData = { text: response.data };
        }

        // Log request/response
        logRequest(agentName, requestData, responseData, response.status, req);

        // Return response
        return res.status(response.status).json({
            agent: agentName,
            status: response.status,
            data: responseData
        });

    } catch (error) {
        let errorData;
        let statusCode = 500;

        if (error.code === 'ECONNABORTED') {
            errorData = { error: 'Agent request timeout' };
            statusCode = 504;
        } else if (error.code === 'ECONNREFUSED') {
            errorData = { error: 'Agent endpoint unreachable' };
            statusCode = 503;
        } else {
            errorData = { error: error.message };
        }

        logRequest(agentName, requestData, errorData, statusCode, req);
        return res.status(statusCode).json(errorData);
    }
});

/**
 * Health check endpoint
 */
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        proxy: 'active',
        agents_configured: Object.keys(AGENT_ENDPOINTS)
    });
});

/**
 * List available agents
 */
app.get('/api/agents', (req, res) => {
    res.json({
        agents: Object.keys(AGENT_ENDPOINTS),
        endpoints: AGENT_ENDPOINTS
    });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log('🚀 Starting Agent Proxy Server');
    console.log(`Proxy Key: ${PROXY_KEY.substring(0, 10)}...`);
    console.log(`Agents: ${Object.keys(AGENT_ENDPOINTS).join(', ')}`);
    console.log('API: POST /api/agent/<agent_name>');
    console.log('Health: GET /health');
    console.log(`\n✅ Server running on http://localhost:${PORT}`);
});

