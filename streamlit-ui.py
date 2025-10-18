"""
Streamlit UI for BYU Undecided Major Advisor
Beautiful, interactive chat interface for the hackathon demo!
"""

import streamlit as st
from agentic_chatbot import AgenticCourseAdvisor, StudentProfile

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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "advisor" not in st.session_state:
    st.session_state.advisor = AgenticCourseAdvisor()

# Header
st.markdown('<h1 class="main-header">🎓 BYU Undecided Major Advisor</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by AI • Personalized Course Recommendations</p>', unsafe_allow_html=True)

# Sidebar for student profile
with st.sidebar:
    st.header("👤 Your Profile")
    
    interests = st.text_area(
        "What are you interested in?",
        placeholder="e.g., business, technology, helping people..."
    )
    
    majors = st.text_input(
        "What majors are you considering?",
        placeholder="e.g., Business, Computer Science"
    )
    
    career_goals = st.text_area(
        "Career goals (optional)",
        placeholder="e.g., work in tech industry, start a business..."
    )
    
    if st.button("🚀 Get Recommendations", type="primary"):
        if interests and majors:
            # Create student profile
            major_list = [m.strip() for m in majors.split(",")]
            profile = StudentProfile(
                interests=interests,
                considering_majors=major_list,
                career_goals=career_goals
            )
            
            # Get recommendations
            with st.spinner("🔍 Analyzing your profile and searching for courses..."):
                results = st.session_state.advisor.get_recommendations(profile)
            
            # Store in session state
            st.session_state.results = results
            st.success("✅ Recommendations ready!")
        else:
            st.error("Please fill in your interests and majors!")

# Main content area
if "results" in st.session_state:
    results = st.session_state.results
    
    # Display recommendations
    st.header("📚 Your Personalized Course Recommendations")
    
    for i, rec in enumerate(results["recommendations"], 1):
        with st.container():
            majors_list = ", ".join(rec['applicable_majors']) if rec['applicable_majors'] else "Multiple programs"
            st.markdown(f"""
            <div class="course-card">
                <div class="course-title">{i}. {rec['course_name']} - {rec['title']}</div>
                <div class="course-description">{rec['description']}</div>
                <p><strong>📊 Versatility Score:</strong> {rec['versatility_score']:.0f}/100</p>
                <p><strong>🎯 Applies to:</strong> {rec['program_count']} major(s) - {majors_list}</p>
                <p><strong>✅ Prerequisites:</strong> {rec['prereq_status']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Show explanation
    st.header("💡 Recommendation Reasoning")
    st.markdown(f"""
    <div class="highlight-box">
        {results['explanation']}
    </div>
    """, unsafe_allow_html=True)
else:
    # Welcome message
    st.info("👈 Fill out your profile in the sidebar to get started!")
    
    st.markdown("""
    ### How it works:
    
    1. **Tell us about yourself** - Share your interests and majors you're considering
    2. **AI analyzes your profile** - Our multi-agent system evaluates your needs
    3. **Get personalized recommendations** - Receive 5 courses tailored to your goals
    4. **Understand the reasoning** - See why each course was recommended
    
    ### Features:
    
    - 🤖 **Multi-agent AI system** for intelligent analysis
    - 📊 **Program overlap analysis** to find versatile courses
    - 🎯 **Personalized recommendations** based on your unique profile
    - 💬 **Clear explanations** for every recommendation
    """)