"""
Phase 3 UI: Interactive Chat Interface
Real conversational experience with context awareness
"""

import streamlit as st
import time

# Import Phase 2 & 3 systems
from agentic_chatbot_phase2 import Phase2AgenticCourseAdvisor, StudentProfile
from chat_agent import ChatAgent

PHASE3_AVAILABLE = True

# Page configuration
st.set_page_config(
    page_title="BYU Course Advisor - Phase 3 Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        color: #002E5D;
        margin-bottom: 0.5rem;
    }
    .course-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #002E5D;
        background: linear-gradient(135deg, #e3f2fd 0%, #f8f9fa 100%);
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .course-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #002E5D;
        margin-bottom: 0.5rem;
    }
    .course-card p {
        color: #1a1a1a;
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    .course-card strong {
        color: #002E5D;
        font-weight: 600;
    }
    .chat-message {
        padding: 1rem 1.2rem;
        border-radius: 15px;
        margin: 0.8rem 0;
        line-height: 1.6;
        animation: fadeIn 0.3s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .user-message {
        background: linear-gradient(135deg, #002E5D 0%, #0062B8 100%);
        color: white;
        margin-left: 20%;
        border-bottom-right-radius: 5px;
    }
    .assistant-message {
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
        color: #1a1a1a;
        margin-right: 20%;
        border-bottom-left-radius: 5px;
        border-left: 4px solid #4CAF50;
    }
    .suggested-question {
        display: inline-block;
        padding: 0.6rem 1rem;
        margin: 0.3rem;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196F3;
        border-radius: 20px;
        color: #0d47a1;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .suggested-question:hover {
        background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.3);
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    .agent-box {
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #ddd;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    .agent-complete {
        border: 2px solid #4CAF50;
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8f4 100%);
    }
    .validation-badge {
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .badge-high { 
        background: linear-gradient(135deg, #66bb6a 0%, #4CAF50 100%);
        color: white;
    }
    .badge-medium { 
        background: linear-gradient(135deg, #ffa726 0%, #FF9800 100%);
        color: white;
    }
    .badge-low { 
        background: linear-gradient(135deg, #ef5350 0%, #f44336 100%);
        color: white;
    }
    .phase-badge {
        background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "advisor" not in st.session_state:
    st.session_state.advisor = Phase2AgenticCourseAdvisor()
if "chat_agent" not in st.session_state and PHASE3_AVAILABLE:
    st.session_state.chat_agent = ChatAgent()
if "show_workflow" not in st.session_state:
    st.session_state.show_workflow = False  # Default off for chat mode
if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = False

# Header
st.markdown('<h1 class="main-header">💬 BYU Course Advisor <span class="phase-badge">PHASE 3</span></h1>', unsafe_allow_html=True)

if PHASE3_AVAILABLE:
    st.markdown('<p style="text-align: center; color: #666;">Interactive Chat Mode • Multi-Agent System • Real-Time Conversation</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="text-align: center; color: #666;">Multi-Agent AI System • Personalized Recommendations</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("👤 Your Profile")
    
    if PHASE3_AVAILABLE:
        st.success("✅ Phase 3: Chat Mode Active!")
    
    st.divider()
    
    interests = st.text_area(
        "What are you interested in?",
        placeholder="e.g., business, technology, data analysis...",
        help="Be specific about your interests"
    )
    
    majors = st.text_input(
        "What majors are you considering?",
        placeholder="e.g., Business, Computer Science",
        help="Separate with commas"
    )
    
    career_goals = st.text_area(
        "Career goals (optional)",
        placeholder="e.g., tech consulting, data science..."
    )
    
    st.divider()
    
    # Mode selection
    if PHASE3_AVAILABLE:
        st.session_state.chat_mode = st.checkbox(
            "💬 Enable Chat Mode",
            value=st.session_state.chat_mode,
            help="Have a conversation about your recommendations"
        )
    
    # Workflow visualization toggle (for non-chat mode)
    if not st.session_state.chat_mode:
        st.session_state.show_workflow = st.checkbox(
            "Show Agent Workflow",
            value=st.session_state.show_workflow,
            help="Display real-time agent activity"
        )
    
    if st.button("🚀 Get Recommendations", type="primary", use_container_width=True):
        if interests and majors:
            major_list = [m.strip() for m in majors.split(",")]
            profile = StudentProfile(
                interests=interests,
                considering_majors=major_list,
                career_goals=career_goals
            )
            
            with st.spinner("🤖 Multi-agent system working..."):
                results = st.session_state.advisor.get_recommendations(profile)
            
            st.session_state.results = results
            
            # Initialize chat with context if in chat mode
            if PHASE3_AVAILABLE and st.session_state.chat_mode:
                st.session_state.chat_agent.update_context(
                    results["recommendations"],
                    {
                        "interests": interests,
                        "considering_majors": major_list,
                        "career_goals": career_goals
                    }
                )
            
            st.success("✅ Recommendations ready!")
            st.rerun()
        else:
            st.error("Please fill in your interests and majors!")
    
    # Clear chat button
    if PHASE3_AVAILABLE and st.session_state.chat_mode and "results" in st.session_state:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_agent.clear_history()
            st.success("Chat cleared!")
            st.rerun()

# Main content
if "results" in st.session_state:
    results = st.session_state.results
    
    # PHASE 3: Chat Mode
    if PHASE3_AVAILABLE and st.session_state.chat_mode:
        st.header("💬 Chat with Your Advisor")
        
        # Display chat history
        chat_history = st.session_state.chat_agent.get_chat_history()
        
        if chat_history:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
                elif msg["role"] == "assistant":
                    st.markdown(f'<div class="chat-message assistant-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👋 Hi! I'm here to help you understand your course recommendations. Ask me anything!")
        
        st.divider()
        
        # Suggested questions
        suggestions = st.session_state.chat_agent.get_suggested_questions()
        if suggestions:
            st.markdown("**💡 Suggested questions:**")
            cols = st.columns(2)
            for idx, suggestion in enumerate(suggestions):
                with cols[idx % 2]:
                    if st.button(suggestion, key=f"suggestion_{idx}", use_container_width=True):
                        # Process the suggested question
                        response = st.session_state.chat_agent.chat(suggestion)
                        st.rerun()
        
        st.divider()
        
        # Chat input
        user_input = st.text_input(
            "Ask a question:",
            placeholder="e.g., Why was this course recommended? How difficult is it?",
            key="chat_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("💬 Send", type="primary", use_container_width=True):
                if user_input:
                    response = st.session_state.chat_agent.chat(user_input)
                    st.rerun()
                else:
                    st.warning("Please enter a question!")
        
        st.divider()
    
    # Show workflow if enabled (non-chat mode)
    if not st.session_state.chat_mode and "workflow" in results and st.session_state.show_workflow:
        st.header("🔄 Agent Workflow")
        
        workflow_steps = [step for step in results.get("workflow", []) if step["status"] == "complete"]
        
        if workflow_steps:
            num_cols = min(len(workflow_steps), 5)
            cols = st.columns(num_cols)
            agent_emojis = {"Planning": "🤖", "Search": "🔍", "Analysis": "📊", 
                           "Explanation": "💬", "Validation": "✅"}
            
            for idx, step in enumerate(workflow_steps[:5]):
                with cols[idx]:
                    emoji = agent_emojis.get(step["agent"], "🔹")
                    confidence_html = ""
                    if 'confidence' in step:
                        confidence_html = f'<div style="text-align: center; margin-top: 0.5rem;"><span class="validation-badge badge-high">{step.get("confidence", "N/A")}%</span></div>'
                    
                    st.markdown(f"""
                    <div class="agent-box agent-complete">
                        <div style="font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;">{emoji}</div>
                        <div style="text-align: center; font-weight: bold; color: #1b5e20; font-size: 1.1rem; margin-bottom: 0.3rem;">{step['agent']}</div>
                        <div style="text-align: center; font-size: 0.85rem; color: #2e7d32; font-weight: 500;">{step['message']}</div>
                        {confidence_html}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.divider()
    
    # Show validation results (if not in chat mode)
    if not st.session_state.chat_mode and "validation" in results:
        validation = results["validation"]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            conf_score = validation["confidence_score"]
            if conf_score >= 80:
                badge_class = "badge-high"
                status_emoji = "✅"
            elif conf_score >= 60:
                badge_class = "badge-medium"
                status_emoji = "⚠️"
            else:
                badge_class = "badge-low"
                status_emoji = "❌"
            
            st.metric("Confidence Score", f"{conf_score}/100")
            st.markdown(f'<span class="validation-badge {badge_class}">{status_emoji} {["Low", "Medium", "High"][min(conf_score//30, 2)]} Confidence</span>', unsafe_allow_html=True)
        
        with col2:
            st.metric("Quality Checks", 
                     f"{validation['checks_passed']}/{validation['total_checks']}",
                     f"{validation['checks_passed']} passed")
        
        with col3:
            issues_count = len(validation.get('issues', []))
            warnings_count = len(validation.get('warnings', []))
            st.metric("Issues Found", issues_count)
            if warnings_count > 0:
                st.caption(f"⚠️ {warnings_count} warnings")
        
        # Show issues if any
        if validation.get('issues'):
            with st.expander("⚠️ View Issues", expanded=False):
                for issue in validation['issues']:
                    st.warning(f"**{issue['name']}:** {issue['issue']}")
        
        # Show warnings if any
        if validation.get('warnings'):
            with st.expander("💡 View Warnings", expanded=False):
                for warning in validation['warnings']:
                    st.info(warning)
        
        st.divider()
    
    # Course recommendations (always show)
    if not st.session_state.chat_mode:
        st.header("📚 Your Personalized Course Recommendations")
    else:
        st.header("📚 Your Course Recommendations")
    
    # Get recommendations - now a dict with programs, courses, overlap_courses
    recs = results.get("recommendations", {})
    
    # Display programs
    if recs.get("programs"):
        st.subheader("🎓 Recommended Programs")
        for i, program in enumerate(recs["programs"][:3], 1):
            st.markdown(f"""
            <div class="course-card">
                <div class="course-title">{i}. {program}</div>
            </div>
            """, unsafe_allow_html=True)
        st.divider()
    
    # Display courses
    if recs.get("courses"):
        st.subheader("📖 Recommended Courses")
        for i, course in enumerate(recs["courses"][:5], 1):
            st.markdown(f"""
            <div class="course-card">
                <div class="course-title">{i}. {course}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Display overlap courses if any
    if recs.get("overlap_courses"):
        st.divider()
        st.subheader("🔗 Multi-Major Courses")
        st.caption("These courses count toward multiple majors")
        for i, course in enumerate(recs["overlap_courses"][:3], 1):
            st.markdown(f"""
            <div class="course-card">
                <div class="course-title">{i}. {course}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Explanation (if not in chat mode)
    if not st.session_state.chat_mode:
        st.header("💡 Why These Courses?")
        st.markdown(results.get('explanation', 'No explanation available'))
    
else:
    # Welcome screen
    st.info("👈 Fill out your profile in the sidebar to get started!")
    
    tab1, tab2, tab3 = st.tabs(["📖 How It Works", "🎯 Features", "💬 Phase 3: Chat"])
    
    with tab1:
        st.markdown("""
        ### Multi-Agent Agentic Workflow:
        
        1. **🤖 Planning Agent** - Analyzes your profile and creates search strategy
        2. **🔍 Search Agent** - Queries vector database with semantic search
        3. **📊 Analysis Agent** - Ranks courses by versatility and fit
        4. **💬 Explanation Agent** - Generates personalized reasoning
        5. **✅ Validation Agent** - Quality checks and self-validation
        
        ### Technology Stack:
        - Vector Database (ChromaDB)
        - Semantic Embeddings
        - Multi-Agent Coordination
        - Self-Validation System
        - Interactive Chat Interface *(Phase 3)*
        """)
    
    with tab2:
        st.success("✅ All Features Active!")
        st.markdown("""
        #### 🔍 **Validation Agent**
        - Checks recommendations for quality
        - Verifies prerequisites are reasonable
        - Ensures goal alignment
        
        #### 📊 **Real-Time Workflow**
        - Watch each agent work
        - See confidence scores
        - Track progress visually
        
        #### ✅ **Quality Assurance**
        - 5 automated checks
        - Confidence scoring
        - Issue detection
        """)
    
    with tab3:
        if PHASE3_AVAILABLE:
            st.success("✅ Phase 3 Chat Features Active!")
            st.markdown("""
            ### What's New in Phase 3:
            
            #### 💬 **Interactive Chat Interface**
            - Have natural conversations about recommendations
            - Ask follow-up questions anytime
            - Context-aware responses
            - Multi-turn conversations
            
            #### 🤖 **Intelligent Responses**
            - Understands your intent
            - Provides detailed explanations
            - Suggests relevant follow-up questions
            - Remembers conversation history
            
            #### 🎯 **Smart Features**
            - AI-powered explanations (when API available)
            - Template-based fallback
            - Suggested questions
            - Clear, helpful responses
            
            #### 💡 **Use Cases**
            - "Why was this course recommended?"
            - "Tell me more about ACCTG 200"
            - "How difficult are these courses?"
            - "What about prerequisites?"
            - "How do these relate to my career goals?"
            """)
        else:
            st.warning("Phase 3 features not available")

# Footer
st.divider()
if PHASE3_AVAILABLE:
    st.caption("💬 Phase 3: Interactive Chat Mode | Multi-Agent System | BYU Hackathon 2025")
else:
    st.caption("🎓 Multi-Agent AI System | BYU Hackathon 2025")
