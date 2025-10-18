#!/bin/bash
# Cleanup script - Remove old/unused files

echo "🧹 Cleaning up old files..."

# Remove old Python files (superseded by Phase 2/3)
echo "  • Removing old chatbot files..."
rm -f agentic_chatbot.py
rm -f agentic_chatbot_enhanced.py
rm -f streamlit-ui.py

# Remove duplicate/old documentation
echo "  • Removing duplicate docs..."
rm -f readme-file.md
rm -f setup-guide.md

# Fix requirements filename
echo "  • Fixing requirements.txt..."
if [ -f requirements-txt.txt ]; then
    mv requirements-txt.txt requirements.txt
fi

# Create archive directory for old docs (optional)
echo "  • Archiving old documentation..."
mkdir -p docs/archive
mv -f API_KEY_INSTRUCTIONS.md docs/archive/ 2>/dev/null || true
mv -f DEMO_CHEAT_SHEET.md docs/archive/ 2>/dev/null || true
mv -f PHASE1_SETUP.md docs/archive/ 2>/dev/null || true
mv -f PHASE2_COMPLETE.md docs/archive/ 2>/dev/null || true
mv -f PHASE2_STRATEGY.md docs/archive/ 2>/dev/null || true
mv -f PHASE3_QUICKSTART.md docs/archive/ 2>/dev/null || true
mv -f PUSH_SUCCESS.md docs/archive/ 2>/dev/null || true

# Keep only the essential docs in root
echo "  • Keeping: README.md, PHASE3_COMPLETE.md, FINAL_SYSTEM_OVERVIEW.md"

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📁 Production files remaining:"
echo "  Core:"
echo "    - agentic_chatbot_phase2.py"
echo "    - chat_agent.py"
echo "    - validation_agent.py"
echo "  UI:"
echo "    - streamlit_ui_phase3.py (recommended)"
echo "    - streamlit_ui_phase2.py (backup)"
echo "    - streamlit_ui_enhanced.py (backup)"
echo "  Data:"
echo "    - byu_data_generator.py"
echo "    - rag_system_setup.py"
echo "  Config:"
echo "    - config.py (local, gitignored)"
echo "    - config.py.template"
echo "  Docs:"
echo "    - README.md"
echo "    - PHASE3_COMPLETE.md"
echo "    - FINAL_SYSTEM_OVERVIEW.md"
echo "    - docs/archive/ (old docs)"
