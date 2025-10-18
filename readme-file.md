# 🎓 BYU Undecided Major Advisor

**An AI-powered course recommendation system for first-year students exploring their major options.**

![Multi-Agent Architecture](https://img.shields.io/badge/AI-Multi--Agent-blue)
![RAG System](https://img.shields.io/badge/RAG-Vector%20DB-green)
![Status](https://img.shields.io/badge/Status-Hackathon%20Ready-success)

---

## 🎯 The Problem

**First-year students with undecided majors risk taking courses that don't count toward their eventual degree, potentially adding an extra year to graduation - costing $30,000+ in tuition.**

At BYU, students interested in multiple majors often don't know which courses provide the most flexibility. Taking the wrong classes early can lock them into a path or waste credits.

## 💡 The Solution

An intelligent course advisor that uses **multi-agent AI** and **vector database search (RAG)** to recommend courses that:

- ✅ Apply to multiple majors simultaneously
- ✅ Keep options open for exploration
- ✅ Match student interests and career goals
- ✅ Have clear prerequisites and availability

## 🤖 Agentic Workflow

Unlike simple AI chatbots, our system uses **four specialized agents** working together:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Planning   │ --> │   Search    │ --> │  Analysis   │ --> │ Explanation │
│    Agent    │     │    Agent    │     │    Agent    │     │    Agent    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      ↓                    ↓                   ↓                     ↓
 Understands         Queries vector      Ranks courses        Generates
 student goals       database (RAG)      by versatility       clear advice
```

### Agent Details:

1. **Planning Agent**: Analyzes student interests, identifies target program categories, and creates a search strategy
2. **Search Agent**: Uses semantic search on vector database to find relevant courses from 40+ course catalog
3. **Analysis Agent**: Calculates compatibility scores, checks prerequisites, evaluates multi-major applicability
4. **Explanation Agent**: Generates natural language explanations with clear reasoning for each recommendation

## 🏗️ Technical Architecture

- **Vector Database**: ChromaDB (local, no API costs)
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Data**: 9 BYU majors, 40+ courses with full metadata
- **UI**: Streamlit (interactive chat interface)
- **Cost**: $0 - everything runs locally!

## 📊 Data Coverage

### Programs (9 majors):
- **Business**: Information Systems, Finance, Accounting
- **Computing**: Computer Science, Computer Engineering  
- **Mathematics**: Pure Math, Applied & Computational Math, Statistics
- **Sciences**: Applied Physics

### Key Insights:
- **20+ courses** apply to multiple majors
- **MATH 112 & 113** → Required by 6 majors
- **CS 111** → Gateway to 5 different programs
- **Business core** → Shared across all business majors

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install chromadb sentence-transformers streamlit

# 2. Generate course data
python byu_data_generator.py

# 3. Build vector database
python rag_system_setup.py

# 4. Launch the UI
streamlit run chatbot_ui.py
```

**Open browser to:** `http://localhost:8501`

## 🎬 Demo Examples

### Example 1: Business + Tech Student
**Input:**
- Interests: "Technology and business, want to work in tech consulting"
- Considering: Information Systems, Finance, Computer Science

**Output:**
- IS 201 (Intro to Information Systems) → Applies to 3 majors
- STAT 121 (Statistics) → Required across Business + STEM
- ACC 200 (Principles of Accounting) → Foundation for all business

### Example 2: STEM Undecided
**Input:**
- Interests: "Math, programming, and data analysis"
- Considering: Computer Science, Mathematics, Statistics

**Output:**
- MATH 112 (Calculus 1) → Required by 6 majors
- CS 111 (Intro to CS) → Gateway to Computing + Math
- STAT 121 → Applicable to all three majors

## 🏆 Why This Wins

### Best Use of AI:
- ✅ Multi-agent agentic workflow (not just a single AI call)
- ✅ RAG architecture with vector database
- ✅ Semantic search using embeddings
- ✅ Sophisticated compatibility scoring

### Most Creative First-Year Solution:
- ✅ Addresses real financial impact ($30k+ in wasted tuition)
- ✅ Reduces first-year stress and uncertainty
- ✅ Data-driven, personalized recommendations
- ✅ Immediately practical and usable

### Grand Prize:
- ✅ Complete, polished prototype
- ✅ Real data from BYU's 2025-26 catalog
- ✅ Beautiful, intuitive interface
- ✅ Scalable to any institution
- ✅ Technical sophistication + practical value

## 📈 Impact Metrics

- **Students helped**: Potentially 1,000+ BYU first-years annually
- **Money saved**: $30,000+ per student (avoiding extra year)
- **Time saved**: Prevents 12+ months of additional coursework
- **Decision quality**: Data-driven vs. guesswork

## 🔮 Future Enhancements

- [ ] Add all BYU majors (60+ programs)
- [ ] Real-time course availability
- [ ] Semester-by-semester planning
- [ ] Integration with degree audit systems
- [ ] Mobile app version
- [ ] Multi-university support

## 👥 Team

Built for BYU Hackathon 2025

## 📄 License

MIT License - Feel free to adapt for your institution!

---

**Made with ❤️ and AI for first-year students everywhere**