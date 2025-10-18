"""
Enhanced Streamlit UI for BYU Undecided Major Advisor
Now with GPT-powered explanations and follow-up Q&A!
"""

import streamlit as st
import sys

# Try to import enhanced version, fall back to basic if not available
try:
    from agentic_chatbot_enhanced import EnhancedAgenticCourseAdvisor, StudentProfile
    from config import USE_LLM_FOR_FOLLOWUP, AI_PROVIDER
    ENHANCED_MODE = True
except ImportError:
    from agentic_chatbot import AgenticCourseAdvisor as EnhancedAgenticCourseAdvisor, StudentProfile
    USE_LLM_FOR_FOLLOWUP = False
    AI_PROVIDER = None
    ENHANCED_MODE = False

# Page configuration
st.set_page_config(
    page_title="BYU Undecided Major Advisor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #002E5D 0%, #0062B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .course-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #002E5D;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .course-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #002E5D;
        margin-bottom: 0.5rem;
    }
    .course-description {
        color: #444;
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    .highlight-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #0062B8;
        margin: 1rem 0;
    }
    .ai-badge {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-left: 1rem;
    }
    .followup-box {
        background-color: #f0f7ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0062B8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "advisor" not in st.session_state:
    st.session_state.advisor = EnhancedAgenticCourseAdvisor()
if "followup_questions" not in st.session_state:
    st.session_state.followup_questions = []

# Header
ai_badge = f'<span class="ai-badge">🤖 AI-Powered by {AI_PROVIDER.upper()}</span>' if ENHANCED_MODE and AI_PROVIDER else ''
st.markdown(f'<h1 class="main-header">🎓 BYU Undecided Major Advisor{ai_badge}</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multi-Agent AI System • Vector Database • Personalized Recommendations</p>', unsafe_allow_html=True)

# Sidebar for student profile
with st.sidebar:
    st.header("👤 Your Profile")
    
    # Show AI status
    if ENHANCED_MODE and AI_PROVIDER:
        st.success(f"✅ Enhanced Mode: {AI_PROVIDER.upper()}")
    else:
        st.info("ℹ️ Template Mode (Add API key for AI)")
    
    st.divider()
    
    interests = st.text_area(
        "What are you interested in?",
        placeholder="e.g., business, technology, helping people, data analysis...",
        help="Be specific! The AI will analyze your interests to find the best matches."
    )
    
    majors = st.text_input(
        "What majors are you considering?",
        placeholder="e.g., Business, Computer Science, Mathematics",
        help="Separate multiple majors with commas"
    )
    
    career_goals = st.text_area(
        "Career goals (optional)",
        placeholder="e.g., work in tech consulting, become a data scientist...",
        help="This helps personalize recommendations"
    )
    
    if st.button("🚀 Get Recommendations", type="primary", use_container_width=True):
        if interests and majors:
            # Create student profile
            major_list = [m.strip() for m in majors.split(",")]
            profile = StudentProfile(
                interests=interests,
                considering_majors=major_list,
                career_goals=career_goals
            )
            
            # Get recommendations
            with st.spinner("🤖 Multi-agent system analyzing your profile...\n\n🔍 Searching vector database...\n\n📊 Ranking courses..."):
                results = st.session_state.advisor.get_recommendations(profile)
            
            # Store in session state
            st.session_state.results = results
            st.session_state.followup_questions = []  # Reset follow-ups
            st.success("✅ Recommendations ready!")
            st.rerun()
        else:
            st.error("Please fill in your interests and majors!")
    
    # Info about the system
    st.divider()
    st.caption("🔧 **System Architecture:**")
    st.caption("• 4 Specialized AI Agents")
    st.caption("• ChromaDB Vector Database")
    st.caption("• Semantic Embeddings")
    if ENHANCED_MODE and AI_PROVIDER:
        st.caption(f"• {AI_PROVIDER.upper()} Integration")

# Main content area
if "results" in st.session_state:
    results = st.session_state.results
    
    # Display recommendations
    st.header("📚 Your Personalized Course Recommendations")
    
    # Show course cards
    for i, rec in enumerate(results["recommendations"][:5], 1):
        with st.container():
            majors_list = ", ".join(rec.get('applicable_majors', [])) if rec.get('applicable_majors') else "Multiple programs"
            
            # Versatility indicator
            score = rec['versatility_score']
            if score >= 80:
                score_color = "🟢"
                score_label = "Highly Versatile"
            elif score >= 60:
                score_color = "🟡"
                score_label = "Moderately Versatile"
            else:
                score_color = "🟠"
                score_label = "Specialized"
            
            st.markdown(f"""
            <div class="course-card">
                <div class="course-title">{i}. {rec['course_name']} - {rec['title']}</div>
                <div class="course-description">{rec['description']}</div>
                <p><strong>{score_color} Versatility:</strong> {rec['versatility_score']:.0f}/100 ({score_label})</p>
                <p><strong>🎯 Applies to:</strong> {rec['program_count']} major(s) — {majors_list}</p>
                <p><strong>✅ Prerequisites:</strong> {rec.get('prereq_status', 'Check with advisor')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Show AI-generated explanation
    st.header("💡 Why These Courses?")
    
    if ENHANCED_MODE and AI_PROVIDER:
        st.info("🤖 This explanation was generated by AI based on your specific profile")
    
    st.markdown(results['explanation'])
    
    # Follow-up Q&A Section (only if LLM is enabled)
    if USE_LLM_FOR_FOLLOWUP:
        st.divider()
        st.header("💬 Have Questions?")
        
        # Show previous Q&A
        for qa in st.session_state.followup_questions:
            st.markdown(f"""
            <div class="followup-box">
                <strong>❓ You asked:</strong> {qa['question']}<br><br>
                <strong>🤖 Answer:</strong> {qa['answer']}
            </div>
            """, unsafe_allow_html=True)
        
        # Input for new question
        with st.form("followup_form", clear_on_submit=True):
            st.write("Ask me anything about your recommendations!")
            followup_question = st.text_input(
                "Your question:",
                placeholder="e.g., Which course should I take first? What if I decide to switch majors?",
                label_visibility="collapsed"
            )
            submitted = st.form_submit_button("Ask", use_container_width=True)
            
            if submitted and followup_question:
                with st.spinner("🤖 Thinking..."):
                    answer = st.session_state.advisor.ask_followup(
                        followup_question,
                        results
                    )
                
                st.session_state.followup_questions.append({
                    "question": followup_question,
                    "answer": answer
                })
                st.rerun()
        
        # Suggested questions
        if len(st.session_state.followup_questions) == 0:
            st.caption("**💡 Try asking:**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Which course should I take first semester?", use_container_width=True):
                    with st.spinner("🤖 Thinking..."):
                        answer = st.session_state.advisor.ask_followup(
                            "Which course should I take first semester?",
                            results
                        )
                    st.session_state.followup_questions.append({
                        "question": "Which course should I take first semester?",
                        "answer": answer
                    })
                    st.rerun()
            
            with col2:
                if st.button("What if I change my mind about my major?", use_container_width=True):
                    with st.spinner("🤖 Thinking..."):
                        answer = st.session_state.advisor.ask_followup(
                            "What if I change my mind about my major?",
                            results
                        )
                    st.session_state.followup_questions.append({
                        "question": "What if I change my mind about my major?",
                        "answer": answer
                    })
                    st.rerun()
    
else:
    # Welcome message
    st.info("👈 Fill out your profile in the sidebar to get started!")
    
    tab1, tab2, tab3 = st.tabs(["📖 How It Works", "🤖 AI Features", "🎯 Demo Examples"])
    
    with tab1:
        st.markdown("""
        ### How Our Multi-Agent System Works:
        
        1. **🤖 Planning Agent** - Analyzes your interests and creates a search strategy
        2. **🔍 Search Agent** - Queries our vector database of BYU courses using semantic search
        3. **📊 Analysis Agent** - Ranks courses by versatility and compatibility
        4. **💬 Explanation Agent** - Generates personalized reasoning for each recommendation
        5. **❓ Q&A Agent** - Answers your follow-up questions *(if AI is enabled)*
        
        ### What Makes It Smart:
        
        - **Vector Database (ChromaDB)** - Fast semantic search using embeddings
        - **Agentic Workflow** - Multiple specialized agents working together
        - **RAG Architecture** - Retrieves relevant data before generating responses
        - **Hybrid Scoring** - Combines multiple factors for best results
        """)
    
    with tab2:
        if ENHANCED_MODE and AI_PROVIDER:
            st.success(f"✅ **Enhanced Mode Active** - Using {AI_PROVIDER.upper()}")
            st.markdown("""
            ### AI-Powered Features:
            
            - 🧠 **Intelligent Intent Understanding** - GPT analyzes your interests deeply
            - ✍️ **Natural Language Explanations** - Personalized narratives, not templates
            - 💬 **Conversational Q&A** - Ask follow-up questions about recommendations
            - 🎯 **Context-Aware Reasoning** - AI considers your specific situation
            
            ### How We Use AI:
            
            1. **Local Vector Search** (Fast & Free) - Find relevant courses
            2. **GPT Analysis** (Smart) - Understand context and generate explanations
            3. **Best of Both Worlds** - Speed + Intelligence
            """)
        else:
            st.warning("⚠️ **Template Mode** - Running without AI")
            st.markdown("""
            ### To Enable AI Features:
            
            1. Get an API key from [OpenAI](https://platform.openai.com/) or [Anthropic](https://console.anthropic.com/)
            2. Add it to `config.py`
            3. Install the library: `pip install openai` or `pip install anthropic`
            4. Restart the app
            
            Even without AI, you still get:
            - ✅ Vector database search
            - ✅ Multi-agent workflow
            - ✅ Versatility scoring
            - ✅ Template-based explanations
            """)
    
    with tab3:
        st.markdown("""
        ### Try These Example Profiles:
        
        **Example 1: Business + Tech**
        - **Interests:** "business and technology, want to understand both sides"
        - **Majors:** Information Systems, Finance, Computer Science
        - **Career:** "Work in tech consulting or fintech"
        
        **Example 2: STEM Explorer**
        - **Interests:** "math, data analysis, and programming"
        - **Majors:** Computer Science, Mathematics, Statistics
        - **Career:** "Data scientist or machine learning engineer"
        
        **Example 3: Undecided STEM**
        - **Interests:** "science and problem solving, not sure about specifics"
        - **Majors:** Physics, Computer Engineering, Mathematics
        - **Career:** "Something in research or development"
        """)

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🎓 BYU Hackathon 2025")
with col2:
    st.caption("🤖 Multi-Agent AI System")
with col3:
    if ENHANCED_MODE and AI_PROVIDER:
        st.caption(f"⚡ Powered by {AI_PROVIDER.upper()}")
    else:
        st.caption("📊 Vector Database Powered")
