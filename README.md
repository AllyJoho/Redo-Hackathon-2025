# 🎓 BYU Course Advisor

**Multi-agent AI system that helps undecided first-year students find courses that keep their options open**

[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)](https://github.com/AllyJoho/Redo-Hackathon-2025)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 🎯 Overview

**The Problem:** First-year students with undecided majors risk taking courses that don't count toward their eventual degree, potentially adding an extra semester or year to graduation.

**Our Solution:** An intelligent AI advisor that recommends courses applying to multiple majors, keeping options open while making progress toward graduation.

### Key Features
- 🤖 **Multi-Agent System** - 5 specialized AI agents working together
- 💬 **Conversational Interface** - Natural chat with context awareness
- ✅ **Self-Validating** - 5 quality checks ensure recommendation accuracy
- 🔍 **RAG Architecture** - Semantic search over vector database
- 📊 **Real-Time Visualization** - Watch agents work together
- 🎯 **Versatility Scoring** - Courses ranked by multi-major applicability

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- 2GB free disk space
- (Optional) OpenAI API key for enhanced responses

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/AllyJoho/Redo-Hackathon-2025.git
cd Redo-Hackathon-2025

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create config file (optional - for AI features)
cp config.py.template config.py
# Edit config.py and add your OpenAI API key

# 5. Generate course data and build database
python byu_data_generator.py
python rag_system_setup.py

# 6. Launch the app
streamlit run streamlit_ui_phase3.py
```

Open your browser to **http://localhost:8501**

---

## 🤖 System Architecture

### Multi-Agent Workflow

Our system uses 5 specialized AI agents that collaborate autonomously:

```
Student Profile Input
        ↓
┌───────────────────────────────────────────────────┐
│  1. Planning Agent    → Analyzes profile          │
│  2. Search Agent      → Queries vector database   │
│  3. Analysis Agent    → Ranks by versatility      │
│  4. Explanation Agent → Generates reasoning        │
│  5. Validation Agent  → Quality checks (5 tests)  │
└───────────────────────────────────────────────────┘
        ↓
Course Recommendations + Confidence Score
        ↓
Interactive Chat (Phase 3)
```

### Technology Stack

- **Backend:** Python 3.12
- **Vector Database:** ChromaDB (persistent, local)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **LLM Integration:** OpenAI GPT-4o-mini / Anthropic Claude
- **UI Framework:** Streamlit
- **Architecture:** RAG (Retrieval Augmented Generation)

---

## 📁 Project Structure

```
Redo-Hackathon-2025/
├── agentic_chatbot_phase2.py    # Main multi-agent system
├── chat_agent.py                 # Phase 3: Conversational AI
├── validation_agent.py           # Phase 2: Quality checks
├── streamlit_ui_phase3.py        # Main UI (recommended)
├── streamlit_ui_phase2.py        # Backup UI (workflow focus)
├── streamlit_ui_enhanced.py      # Backup UI (basic)
├── byu_data_generator.py         # Generate course data
├── rag_system_setup.py           # Build vector database
├── config.py.template            # Configuration template
├── requirements.txt              # Python dependencies
├── data/                         # Course & program data (generated)
├── chroma_db/                    # Vector database (generated)
└── docs/                         # Documentation
```

---

## 💬 Features by Phase

### Phase 1: LLM Integration
- AI-powered intent parsing
- Natural language explanations
- GPT & Claude support
- Graceful fallback to templates

### Phase 2: Validation & Workflow
- 5 automated quality checks
- Confidence scoring (0-100)
- Real-time agent visualization
- Issue detection & warnings

### Phase 3: Interactive Chat ⭐
- Conversational interface
- Context-aware responses
- Intent detection (8+ types)
- Suggested follow-up questions
- Chat history management

---

## 🎮 Usage

### Basic Flow

1. **Fill Profile** - Interests, majors considering, career goals
2. **Enable Chat Mode** - Toggle for conversational experience
3. **Get Recommendations** - Watch 5 agents collaborate
4. **Chat About Results** - Ask questions, explore options

### Example Questions

- "Why was ACCTG 200 recommended?"
- "How difficult are these courses?"
- "Tell me more about [course name]"
- "How does this help my career goals?"
- "Show me easier alternatives"

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# API Keys (optional - system works without them)
OPENAI_API_KEY = "your-key-here"
ANTHROPIC_API_KEY = "your-key-here"

# Provider Selection
AI_PROVIDER = "openai"  # or "anthropic"

# Model Settings
OPENAI_MODEL = "gpt-4o-mini"  # Cheap & fast
TEMPERATURE = 0.2              # Deterministic responses
MAX_TOKENS = 1000              # Response length

# Feature Flags
USE_LLM_FOR_PLANNING = True
USE_LLM_FOR_EXPLANATIONS = True
USE_LLM_FOR_FOLLOWUP = True
```

---

## 📊 Data

### Course Database
- **9 BYU programs** across Business and STEM
- **28 unique courses** with descriptions
- **24 multi-major courses** for versatility

### Vector Collections
- `programs` - Major programs with requirements
- `classes` - Individual courses with metadata
- `overlap` - Multi-major courses (key feature)

---

## 🧪 Testing

System includes validation for:
- ✅ All 5 agents execute successfully
- ✅ Validation checks pass (4-5 out of 5)
- ✅ Confidence scores typically 80-95%
- ✅ Chat intent detection accurate
- ✅ Graceful fallback when API unavailable

---

## 🚢 Deployment

### For Hackathon/Demo
```bash
streamlit run streamlit_ui_phase3.py --server.port 8501
```

### For Production
- Deploy on Streamlit Cloud, Heroku, or AWS
- Use environment variables for API keys
- Configure persistent storage for `chroma_db/`
- Add authentication if needed

---

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- [ ] Add more BYU programs and courses
- [ ] Implement course pathway visualization
- [ ] Add scheduling/calendar integration
- [ ] Export recommendations to PDF
- [ ] Mobile-responsive UI improvements
- [ ] Multi-university support

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **BYU Homecoming 2025 Redo Hackathon** - Original development
- **OpenAI** - GPT-4o-mini for natural language
- **Anthropic** - Claude for alternative LLM support
- **ChromaDB** - Vector database infrastructure
- **Streamlit** - Web UI framework

---

## 📧 Contact

**Project Maintainer:** Allison Johanson  
**GitHub:** [@AllyJoho](https://github.com/AllyJoho)  
**Repository:** [Redo-Hackathon-2025](https://github.com/AllyJoho/Redo-Hackathon-2025)

---

## 📚 Documentation

- **[PHASE3_COMPLETE.md](PHASE3_COMPLETE.md)** - Complete Phase 3 guide
- **[FINAL_SYSTEM_OVERVIEW.md](FINAL_SYSTEM_OVERVIEW.md)** - Full system documentation
- **[docs/archive/](docs/archive/)** - Historical documentation

---

**Built with ❤️ for helping students find their path** 🎓✨
