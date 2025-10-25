#!/usr/bin/env python3
"""
Execute Complete Agentverse Flow
Automates the entire process from start to verification
"""

import subprocess
import sys
import time
from pathlib import Path

def run_script(script_name, description):
    """Run a script and display results"""
    print(f"\n{'=' * 70}")
    print(f"📋 {description}")
    print(f"{'=' * 70}")
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"⚠️  Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False

def main():
    """Main execution flow"""
    print("=" * 70)
    print("🚀 Phisherman Agentverse Integration - Automated Execution")
    print("=" * 70)
    
    steps = [
        ("ports_status.py", "Check Port Status (Pre-flight Check)"),
        ("start_all.py", "Start All Agents"),
        ("verify_chat.py", "Verify Chat Protocol"),
    ]
    
    results = {}
    
    for script, description in steps:
        success = run_script(script, description)
        results[description] = success
        
        if not success:
            print(f"\n⚠️  Step failed: {description}")
            print("   Please check logs for details")
        
        time.sleep(2)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Execution Summary")
    print("=" * 70)
    
    for description, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {description}")
    
    print("\n" + "=" * 70)
    print("📝 Next Steps (Manual)")
    print("=" * 70)
    print("1. Start HTTPS tunnels: ./scripts/tunnels_start.sh")
    print("2. Generate Inspector URLs: python3 scripts/inspect_urls.py")
    print("3. Open Inspector URLs and connect via Mailbox")
    print("4. Provide mailbox endpoints to update Agentverse")
    print("5. Run update script: python3 scripts/update_agentverse_endpoints.py")
    print("=" * 70)

if __name__ == "__main__":
    main()

