#!/usr/bin/env python3
"""
Check Port Status
Reports Port → PID → Listening (Y/N) for all agent ports
"""

import socket
import subprocess
from pathlib import Path

# Agent configuration
AGENTS = [
    {"name": "phish_master", "port": 8001},
    {"name": "finance_phisher", "port": 8002},
    {"name": "health_phisher", "port": 8003},
    {"name": "personal_phisher", "port": 8004},
    {"name": "phish_refiner", "port": 8005},
]

def get_pid_for_port(port):
    """Get PID for process using a port"""
    try:
        # Use lsof on Unix systems
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'],
            capture_output=True,
            text=True
        )
        pid = result.stdout.strip()
        return pid if pid else None
    except:
        return None

def check_port_listening(port):
    """Check if port is listening"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def main():
    """Main function"""
    print("=" * 70)
    print("🔍 Port Status Report")
    print("=" * 70)
    
    status_report = []
    
    for agent in AGENTS:
        port = agent["port"]
        pid = get_pid_for_port(port)
        listening = check_port_listening(port)
        
        status_report.append({
            "agent": agent["name"],
            "port": port,
            "pid": pid,
            "listening": "Y" if listening else "N"
        })
        
        print(f"\n{agent['name']}:")
        print(f"  Port: {port}")
        print(f"  PID: {pid if pid else 'None'}")
        print(f"  Listening: {'✅ YES' if listening else '❌ NO'}")
    
    # Save report
    diagnostics_dir = Path(__file__).parent.parent / "diagnostics"
    diagnostics_dir.mkdir(exist_ok=True)
    
    output_file = diagnostics_dir / "ports_status.txt"
    
    with open(output_file, 'w') as f:
        f.write("Port Status Report\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"{'Agent':<20} {'Port':<8} {'PID':<10} {'Listening':<10}\n")
        f.write("-" * 70 + "\n")
        
        for status in status_report:
            f.write(f"{status['agent']:<20} {status['port']:<8} {status['pid'] or 'None':<10} {status['listening']:<10}\n")
    
    print("\n" + "=" * 70)
    print(f"✅ Status report saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()

