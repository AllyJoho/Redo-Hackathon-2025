"""
Phase 2 UI: Enhanced Streamlit interface with visual workflow display
Shows agents working in real-time with progress bars and validation results
"""

import streamlit as st
import time

# Try to import Phase 2 system
try:
    from agentic_chatbot_phase2 import Phase2AgenticCourseAdvisor, StudentProfile
    PHASE2_AVAILABLE = True
except ImportError:
    # Fallback to Phase 1 or basic
    try:
        from agentic_chatbot_enhanced import EnhancedAgenticCourseAdvisor as Phase2AgenticCourseAdvisor, StudentProfile
    except ImportError:
        from agentic_chatbot import AgenticCourseAdvisor as Phase2AgenticCourseAdvisor, StudentProfile
    PHASE2_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="BYU Undecided Major Advisor - Phase 2",
    page_icon="🎓",
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
    .agent-complete div {
        color: #1b5e20 !important;
    }
    .agent-running {
        border: 2px solid #2196F3;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        animation: pulse 1.5s infinite;
    }
    .agent-running div {
        color: #0d47a1 !important;
    }
    @keyframes pulse {
        0%, 100% { 
            opacity: 1;
            transform: scale(1);
        }
        50% { 
            opacity: 0.85;
            transform: scale(1.02);
        }
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "advisor" not in st.session_state:
    st.session_state.advisor = Phase2AgenticCourseAdvisor()
if "show_workflow" not in st.session_state:
    st.session_state.show_workflow = True

# Header
st.markdown('<h1 class="main-header">🎓 BYU Undecided Major Advisor</h1>', unsafe_allow_html=True)

if PHASE2_AVAILABLE:
    st.markdown('<p style="text-align: center; color: #666;">Phase 2: Multi-Agent System with Validation & Real-Time Workflow</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="text-align: center; color: #666;">Multi-Agent AI System • Personalized Recommendations</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("👤 Your Profile")
    
    if PHASE2_AVAILABLE:
        st.success("✅ Phase 2: Validation Enabled")
    
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
    
    # Workflow visualization toggle
    if PHASE2_AVAILABLE:
        st.session_state.show_workflow = st.checkbox(
            "Show Agent Workflow",
            value=True,
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
            
            # Create placeholder for workflow if enabled
            if st.session_state.show_workflow and PHASE2_AVAILABLE:
                st.session_state.workflow_placeholder = st.empty()
            
            with st.spinner("🤖 Multi-agent system working..."):
                results = st.session_state.advisor.get_recommendations(profile)
            
            st.session_state.results = results
            st.success("✅ Recommendations ready!")
            st.rerun()
        else:
            st.error("Please fill in your interests and majors!")

# Main content
if "results" in st.session_state:
    results = st.session_state.results
    
    # Phase 2: Show workflow visualization
    if PHASE2_AVAILABLE and "workflow" in results and st.session_state.show_workflow:
        st.header("🔄 Agent Workflow")
        
        workflow_steps = [step for step in results.get("workflow", []) if step["status"] == "complete"]
        
        if workflow_steps:
            # Create columns based on number of completed steps (max 5)
            num_cols = min(len(workflow_steps), 5)
            cols = st.columns(num_cols)
            agent_emojis = {"Planning": "🤖", "Search": "🔍", "Analysis": "📊", 
                           "Explanation": "💬", "Validation": "✅"}
            
            for idx, step in enumerate(workflow_steps[:5]):  # Only show first 5
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
    
    # Phase 2: Show validation results
    if PHASE2_AVAILABLE and "validation" in results:
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
    
    # Course recommendations
    st.header("📚 Your Personalized Course Recommendations")
    
    for i, rec in enumerate(results["recommendations"][:5], 1):
        majors_list = ", ".join(rec.get('applicable_majors', [])) if rec.get('applicable_majors') else "Multiple programs"
        
        score = rec.get('versatility_score', 0)
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
            <p style="color: #1a1a1a; margin: 0.8rem 0 0.5rem 0; line-height: 1.6; font-size: 1rem;">{rec['description']}</p>
            <p style="color: #1a1a1a; margin: 0.4rem 0; font-size: 0.95rem;"><strong style="color: #002E5D;">{score_color} Versatility:</strong> {score:.0f}/100 ({score_label})</p>
            <p style="color: #1a1a1a; margin: 0.4rem 0; font-size: 0.95rem;"><strong style="color: #002E5D;">🎯 Applies to:</strong> {rec.get('program_count', 0)} major(s) — {majors_list}</p>
            <p style="color: #1a1a1a; margin: 0.4rem 0; font-size: 0.95rem;"><strong style="color: #002E5D;">✅ Prerequisites:</strong> {rec.get('prereq_status', 'Check with advisor')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Explanation
    st.header("💡 Why These Courses?")
    st.markdown(results.get('explanation', 'No explanation available'))
    
else:
    # Welcome screen
    st.info("👈 Fill out your profile in the sidebar to get started!")
    
    tab1, tab2 = st.tabs(["📖 How It Works", "🎯 Phase 2 Features"])
    
    with tab1:
        st.markdown("""
        ### Multi-Agent Agentic Workflow:
        
        1. **🤖 Planning Agent** - Analyzes your profile and creates search strategy
        2. **🔍 Search Agent** - Queries vector database with semantic search
        3. **📊 Analysis Agent** - Ranks courses by versatility and fit
        4. **💬 Explanation Agent** - Generates personalized reasoning
        5. **✅ Validation Agent** - Quality checks and self-validation *(Phase 2)*
        
        ### Technology Stack:
        - Vector Database (ChromaDB)
        - Semantic Embeddings
        - Multi-Agent Coordination
        - Self-Validation System *(Phase 2)*
        """)
    
    with tab2:
        if PHASE2_AVAILABLE:
            st.success("✅ Phase 2 Features Active!")
            st.markdown("""
            ### What's New in Phase 2:
            
            #### 🔍 **Validation Agent**
            - Checks recommendations for quality
            - Verifies prerequisites are reasonable
            - Ensures goal alignment
            - Confirms program overlap
            - Validates course levels
            
            #### 📊 **Real-Time Workflow**
            - Watch each agent work
            - See confidence scores
            - Track progress visually
            - Understand the process
            
            #### ✅ **Quality Assurance**
            - 5 automated checks
            - Confidence scoring
            - Issue detection
            - Warning system
            
            #### 🎯 **Self-Checking AI**
            - System validates its own work
            - Catches potential problems
            - Builds trust through transparency
            """)
        else:
            st.warning("Phase 2 features not available")
            st.info("Phase 2 adds validation and visual workflow tracking")

# Footer
st.divider()
if PHASE2_AVAILABLE:
    st.caption("🎓 Phase 2: Multi-Agent System with Validation | BYU Hackathon 2025")
else:
    st.caption("🎓 Multi-Agent AI System | BYU Hackathon 2025")
