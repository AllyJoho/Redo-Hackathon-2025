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
        background-color: #e