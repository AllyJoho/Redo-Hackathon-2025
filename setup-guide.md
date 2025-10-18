# 🎓 BYU Undecided Major Advisor - Complete Setup Guide

## 📋 What You've Built

An **AI-powered course advisor** using a **multi-agent agentic workflow** to help first-year students with undecided majors find courses that keep their options open!

### Key Features:
- ✅ **9 BYU majors** across Business, STEM, and Data Science
- ✅ **Multi-agent system** (Planning → Search → Analysis → Explanation)
- ✅ **Vector database** with RAG (Retrieval Augmented Generation)
- ✅ **Beautiful Streamlit UI** for demos
- ✅ **100% FREE** - no API costs!

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install chromadb sentence-transformers streamlit numpy pandas
```

### Step 2: Generate Course Data

```bash
python byu_data_generator.py
```

**Expected output:**
```
✓ BYU COURSE DATA GENERATION COMPLETE!
📊 STATISTICS:
   • 9 programs
   • 40+ unique classes
   • 20+ multi-major classes
```

This creates the `data/` folder with:
- `programs.json` - All major requirements
- `classes.json` - Course details
- `class_overlap.json` - Multi-major courses

### Step 3: Build Vector Database

```bash
python rag_system_setup.py
```

**Expected output:**
```
🔨 BUILDING VECTOR DATABASE
✓ Added 9 programs to database
✓ Added 40+ classes to database
✓ Added 20+ multi-major classes to database
✅ RAG SYSTEM READY!
```

This creates the `chroma_db/` folder with your vector database.

### Step 4: Test the Agentic System (Optional)

```bash
python agentic_chatbot.py
```

This runs automated tests showing the multi-agent workflow in action!

### Step 5: Launch the UI

```bash
streamlit run chatbot_ui.py
```

**Your browser will open to:** `http://localhost:8501`

---

## 🎬 Demo Script for Hackathon

### Opening (30 seconds)
"Hi! I'm [Name] and I built an AI-powered course advisor for first-year students who haven't decided on a major yet. The problem? Taking the wrong classes can add an extra year to graduation, costing tens of thousands of dollars."

### The Problem (30 seconds)
"At BYU, if you're undecided between Computer Science, Math, and Statistics, you might not know that taking MATH 112 and CS 111 in your first semester keeps ALL THREE options open. But taking a course specific to just one major could lock you in."

### The Solution (1 minute)
"My solution uses a **multi-agent AI system** with four specialized agents:
1. **Planning Agent** - Understands student goals
2. **Search Agent** - Queries a vector database of courses
3. **Analysis Agent** - Ranks courses by versatility
4. **Explanation Agent** - Provides clear reasoning

Let me show you..." [Switch to demo]

### Live Demo (2 minutes)
**Test Case 1:** Business + Tech Student
- Interests: "I love technology and business, maybe tech consulting"
- Majors: Information Systems, Finance, Computer Science
- **Show results:** Recommends IS 201, STAT 121, ACC 200
- **Key point:** "See how these 3 courses apply to all their majors?"

**Test Case 2:** STEM Undecided
- Interests: "Math, programming, and data"
- Majors: Computer Science, Mathematics, Statistics
- **Show results:** Recommends MATH 112, CS 111, STAT 121
- **Key point:** "These form a solid foundation regardless of final choice"

### Technical Highlights (1 minute)
"The agentic workflow is key - instead of a single AI call, we have specialized agents:
- Built with **Chroma** (vector database) and **Sentence Transformers** (embeddings)
- **RAG system** retrieves relevant courses before generating recommendations
- **Multi-agent coordination** ensures thorough analysis
- All running **locally** - no expensive API calls!"

### Closing (30 seconds)
"This helps students explore options without wasting credits or money. It's scalable to any college, any major set. Thank you!"

---

## 📊 Scoring Strategy

### For "Best Use of AI"
**Talking points:**
- ✅ Multi-agent agentic workflow (not just one AI call!)
- ✅ RAG system with vector database
- ✅ Semantic search using embeddings
- ✅ Sophisticated ranking algorithm
- ✅ Real-world problem with measurable impact

### For "Most Creative First-Year Solution"
**Talking points:**
- ✅ Directly addresses financial impact (extra year = $30k+)
- ✅ Reduces stress and uncertainty for first-years
- ✅ Data-driven recommendations, not generic advice
- ✅ Scalable to any institution

### For "Grand Prize"
**Talking points:**
- ✅ Complete, working prototype
- ✅ Real BYU data (9 majors, 40+ courses)
- ✅ Beautiful, intuitive UI
- ✅ Technical sophistication (multi-agent system)
- ✅ Clear value proposition
- ✅ Immediately deployable

---

## 🎯 Key Demo Tips

### DO:
- ✅ Start with the problem (extra year = expensive!)
- ✅ Show 2-3 different student profiles
- ✅ Highlight the "program_count" metric (courses that apply to multiple majors)
- ✅ Explain the agentic workflow clearly
- ✅ Mention it's all local/free (impressive technically)

### DON'T:
- ❌ Get bogged down in technical details
- ❌ Show code unless asked
- ❌ Spend too long on one example
- ❌ Forget to mention the multi-agent architecture

---

## 🛠️ Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Chroma database errors
```bash
# Delete and rebuild
rm -rf chroma_db/
python rag_system_setup.py
```

### Streamlit won't start
```bash
# Check if port 8501 is in use
streamlit run chatbot_ui.py --server.port 8502
```

### Embeddings model download fails
The first time you run it, sentence-transformers downloads a ~90MB model. Make sure you have internet connection. It only happens once!

---

## 🚀 Quick Improvements (If You Have Time)

### Priority 1: Add More Majors (30 min)
Edit `byu_data_generator.py` and add more programs from your PDFs.

### Priority 2: Better Explanations (30 min)
Edit `ExplanationAgent.generate_explanation()` in `agentic_chatbot.py` to add more personality.

### Priority 3: Save Student Sessions (20 min)
Add a "Save Profile" button that stores student preferences.

### Priority 4: Comparison View (30 min)
Show side-by-side comparison of 2-3 majors with shared courses highlighted.

---

## 📁 File Structure

```
your-project/
├── data/
│   ├── programs.json          # Generated by byu_data_generator.py
│   ├── classes.json
│   └── class_overlap.json
├── chroma_db/                 # Generated by rag_system_setup.py
│   └── [vector database files]
├── byu_data_generator.py      # Run FIRST
├── rag_system_setup.py        # Run SECOND
├── agentic_chatbot.py         # Run THIRD (optional test)
├── chatbot_ui.py              # Run FOURTH (the demo!)
└── requirements.txt
```

---

## 🎤 Sample Q&A

**Q: How is this different from just asking ChatGPT?**
A: ChatGPT doesn't know BYU's specific requirements or which classes overlap between majors. Our system has BYU's actual course catalog in a vector database and uses specialized agents to analyze course compatibility.

**Q: Why use multiple agents instead of one AI call?**
A: Each agent has a specific job - planning, searching, analyzing, explaining. This gives more reliable results than asking a general AI to do everything at once. It's like having a team of advisors instead of one person.

**Q: Could this work at other schools?**
A: Absolutely! You just need to feed it different course data. The system is completely agnostic to the institution.

**Q: What if a student changes their mind about majors?**
A: That's the beauty of it - our recommendations are specifically chosen to keep multiple options open. If they change from CS to Math, many of their classes still count!

**Q: How accurate is this compared to a human advisor?**
A: It's meant to complement human advisors, not replace them. It gives students a starting point before meeting with their advisor. The final decision should always involve a real person.

---

## 🎉 You're Ready!

Your project is:
- ✅ **Technically impressive** (multi-agent AI, RAG, vector DB)
- ✅ **Practically useful** (solves a real $30k+ problem)
- ✅ **Fully functional** (working prototype, not just slides)
- ✅ **Well-presented** (beautiful UI, clear value prop)

**Good luck at the hackathon! 🚀**