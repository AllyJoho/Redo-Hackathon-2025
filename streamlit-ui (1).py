"""
Streamlit UI for BYU Undecided Major Advisor
Beautiful, interactive chat interface for the hackathon demo!
"""

import streamlit as st
from agentic_chatbot import AgenticCourseAdvisor, StudentProfile
import json

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
        border-radius: 8px;
        border-left: 4px solid #0062B8;
        margin: 1rem 0;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #002E5D;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0062B8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'advisor' not in st.session_state:
    with st.spinner('🔧 Loading AI advisor system...'):
        st.session_state.advisor = AgenticCourseAdvisor()
        st.session_state.history = []

if 'current_results' not in st.session_state:
    st.session_state.current_results = None

# Header
st.markdown('<div class="main-header">🎓 BYU Undecided Major Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered course recommendations for exploring your options</div>', unsafe_allow_html=True)

# Sidebar - Student Profile Input
with st.sidebar:
    st.header("👤 Your Profile")
    st.markdown("Tell us about yourself so we can personalize your recommendations!")
    
    # Input fields
    student_name = st.text_input("Name (optional)", placeholder="e.g., Alex")
    
    interests = st.text_area(
        "What are you interested in?",
        placeholder="e.g., I love technology and business, want to understand how companies use data...",
        height=100,
        help="Describe your academic interests, passions, or what excites you!"
    )
    
    st.markdown("**Majors you're considering:**")
    
    # Available majors organized by category
    major_options = {
        "Business": ["Information Systems", "Finance", "Accounting"],
        "Computing": ["Computer Science", "Computer Engineering"],
        "Mathematics & Data": ["Mathematics", "Mathematics - Applied & Computational", 
                              "Statistics - Applied Statistics & Analytics"],
        "Physical Sciences": ["Applied Physics"]
    }
    
    selected_majors = []
    
    for category, majors in major_options.items():
        with st.expander(f"📚 {category}"):
            for major in majors:
                if st.checkbox(major, key=f"major_{major}"):
                    selected_majors.append(major)
    
    career_goals = st.text_area(
        "Career goals (optional)",
        placeholder="e.g., Work at a tech startup, become a financial analyst...",
        height=80
    )
    
    completed_courses = st.text_input(
        "Courses already taken (optional)",
        placeholder="e.g., MATH 112, CS 111",
        help="Separate with commas"
    )
    
    st.markdown("---")
    get_recommendations = st.button("✨ Get Recommendations", type="primary")

# Main content area
if not get_recommendations and st.session_state.current_results is None:
    # Welcome screen
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Programs Covered", "9", delta="Business, STEM, Data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Course Database", "40+", delta="Updated for 2025-26")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Multi-Major Classes", "20+", delta="Keep options open")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Info boxes
    st.markdown("### 🎯 How This Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="highlight-box">
        <h4>🤖 AI-Powered Recommendations</h4>
        <p>Our system uses advanced AI agents to:</p>
        <ul>
            <li>Understand your interests and goals</li>
            <li>Search through BYU's course catalog</li>
            <li>Find classes that apply to multiple majors</li>
            <li>Explain why each course is recommended</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
        <h4>💡 Explore Without Commitment</h4>
        <p>Perfect for first-year students who:</p>
        <ul>
            <li>Haven't declared a major yet</li>
            <li>Are considering switching majors</li>
            <li>Want to keep multiple options open</li>
            <li>Need flexible course planning</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Get Started")
    st.info("👈 Fill out your profile in the sidebar and click **Get Recommendations** to begin!")
    
    # Example queries
    with st.expander("💭 Example: What kind of input works best?"):
        st.markdown("""
        **Good examples:**
        - "I'm interested in technology and business, want to work at a startup"
        - "Love data analysis and solving problems with math"
        - "Want to learn programming but also interested in finance"
        - "Exploring engineering and computer science options"
        
        **Tip:** The more specific you are, the better our recommendations!
        """)

# Process recommendations
elif get_recommendations and interests and selected_majors:
    with st.spinner('🤖 AI agents analyzing your profile...'):
        # Create student profile
        completed_list = [c.strip() for c in completed_courses.split(',')] if completed_courses else []
        
        profile = StudentProfile(
            interests=interests,
            considering_majors=selected_majors,
            career_goals=career_goals,
            completed_courses=completed_list
        )
        
        # Get recommendations
        results = st.session_state.advisor.get_recommendations(profile)
        st.session_state.current_results = results
        st.session_state.history.append({
            "profile": profile,
            "results": results
        })

# Display results
if st.session_state.current_results:
    results = st.session_state.current_results
    
    # Summary
    st.success(f"✅ Found {len(results['recommendations'])} courses perfectly suited for you!")
    
    # Display explanation
    st.markdown("### 💬 Personalized Advice")
    st.markdown(results['explanation'])
    
    st.markdown("---")
    
    # Detailed course cards
    st.markdown("### 📚 Recommended Courses")
    
    for i, course in enumerate(results['recommendations'], 1):
        with st.container():
            st.markdown(f'<div class="course-card">', unsafe_allow_html=True)
            
            # Course header with badge
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f'<div class="course-title">{i}. {course["course_name"]} - {course["title"]}</div>',
                    unsafe_allow_html=True
                )
            with col2:
                if course['compatibility_score'] >= 80:
                    st.markdown("🌟 **Top Pick**")
                st.markdown(f"**{course['credit_hours']} credits**")
            
            # Course description
            st.markdown(f'<div class="course-description">{course["description"]}</div>', 
                       unsafe_allow_html=True)
            
            # Metrics in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Programs",
                    f"{course['program_count']} majors",
                    help="Number of majors this course applies to"
                )
            
            with col2:
                st.metric(
                    "Versatility",
                    f"{course['versatility_score']}/100",
                    help="Higher = keeps more options open"
                )
            
            with col3:
                st.metric(
                    "Match Score",
                    f"{int(course['compatibility_score'])}%",
                    help="How well this fits your profile"
                )
            
            # Expandable details
            with st.expander("📋 More Details"):
                st.markdown(f"**Category:** {course['category']}")
                st.markdown(f"**Prerequisites:** {course['prereq_status']}")
                st.markdown(f"**Applies to these programs:**")
                for prog in course['applies_to_programs']:
                    st.markdown(f"- {prog}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download Recommendations"):
            # Create downloadable JSON
            download_data = {
                "student_interests": interests,
                "considering_majors": selected_majors,
                "recommendations": results['recommendations']
            }
            st.download_button(
                "💾 Download JSON",
                data=json.dumps(download_data, indent=2),
                file_name="course_recommendations.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🔄 Get New Recommendations"):
            st.session_state.current_results = None
            st.rerun()
    
    with col3:
        if st.button("📊 View Analysis"):
            st.markdown("### 📊 Recommendation Analysis")
            st.json(results['plan'])

elif get_recommendations:
    st.warning("⚠️ Please fill in your interests and select at least one major to get recommendations!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🎓 BYU Course Advisor**")
    st.markdown("Built for first-year students")

with col2:
    st.markdown("**🤖 Powered by**")
    st.markdown("Multi-agent AI system")

with col3:
    st.markdown("**📚 Data Source**")
    st.markdown("BYU 2025-26 Catalog")