#!/bin/bash
# Phisherman Terminal CLI - 60 Second Demo Script
# Safe, educational demonstration for judges/demo

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║      🎓 Phisherman Terminal CLI - 60 Second Demo                     ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Goal: Generate and refine a safe cybersecurity training template"
echo "⚠️  Note: NO real phishing content will be generated"
echo ""
echo "Starting demo..."
echo ""
sleep 2

# Run the CLI with automated input
echo "1
1
refine
improve_tone:urgent
increase_urgency
done
export
quit" | python3 phisherman_cli.py

echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "✅ Demo Complete!"
echo ""
echo "📁 Generated Files:"
echo "   • diagnostics/templates/<template_id>.json"
echo "   • diagnostics/chat_history.txt"
echo ""
echo "🎓 Template Contents:"
echo "   • Scenario title"
echo "   • Sanitized description"
echo "   • Placeholders (no real content)"
echo "   • Red flags"
echo "   • Training objectives"
echo "   • Safety notes"
echo ""
echo "⚠️  Remember: All content is educational and non-actionable."
echo "════════════════════════════════════════════════════════════════════════"

