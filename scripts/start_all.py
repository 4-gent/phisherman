#!/usr/bin/env python3
"""
Start All Phisherman Agents
Launches all 5 agents in separate subprocesses and streams logs to logs/*.log
"""

import subprocess
import sys
import os
import time
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path(__file__).parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Agent configuration
AGENTS = [
    {"name": "phish_master", "port": 8001, "script": "backend/mail/sender/phish_master/main.py"},
    {"name": "finance_phisher", "port": 8002, "script": "backend/mail/sender/finance_phisher/main.py"},
    {"name": "health_phisher", "port": 8003, "script": "backend/mail/sender/health_phisher/main.py"},
    {"name": "personal_phisher", "port": 8004, "script": "backend/mail/sender/personal_phisher/main.py"},
    {"name": "phish_refiner", "port": 8005, "script": "backend/mail/sender/phish_refiner/main.py"},
]

def check_port(port):
    """Check if port is already in use"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def start_agent(agent):
    """Start a single agent process"""
    script_path = Path(__file__).parent.parent / agent["script"]
    log_file = logs_dir / f"{agent['name']}.log"
    
    # Check if port is in use
    if check_port(agent["port"]):
        print(f"⚠️  Port {agent['port']} already in use for {agent['name']}")
        return None
    
    # Start agent process
    print(f"🚀 Starting {agent['name']} on port {agent['port']}...")
    
    try:
        with open(log_file, 'w') as f:
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=str(Path(__file__).parent.parent)
            )
        
        # Give agent time to start
        time.sleep(2)
        
        if process.poll() is None:
            print(f"✅ {agent['name']} started (PID: {process.pid})")
            return process
        else:
            print(f"❌ {agent['name']} failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting {agent['name']}: {e}")
        return None

def main():
    """Main function to start all agents"""
    print("=" * 70)
    print("🎯 Starting Phisherman Agents")
    print("=" * 70)
    
    processes = []
    
    # Start all agents
    for agent in AGENTS:
        process = start_agent(agent)
        if process:
            processes.append((agent["name"], process))
        time.sleep(1)  # Stagger startup
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Agent Status Summary")
    print("=" * 70)
    
    for name, process in processes:
        if process.poll() is None:
            print(f"✅ {name}: Running (PID: {process.pid})")
        else:
            print(f"❌ {name}: Stopped")
    
    print("\n" + "=" * 70)
    print("🌐 Agent Endpoints")
    print("=" * 70)
    for agent in AGENTS:
        print(f"  {agent['name']}: http://127.0.0.1:{agent['port']}")
    
    print("\n" + "=" * 70)
    print("📝 Log Files")
    print("=" * 70)
    for agent in AGENTS:
        log_file = logs_dir / f"{agent['name']}.log"
        print(f"  {agent['name']}: {log_file}")
    
    print("\n" + "=" * 70)
    print("Press Ctrl+C to stop all agents")
    print("=" * 70)
    
    # Wait for all processes
    try:
        for name, process in processes:
            process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping all agents...")
        for name, process in processes:
            if process.poll() is None:
                process.terminate()
                print(f"  Stopped {name}")

if __name__ == "__main__":
    main()

