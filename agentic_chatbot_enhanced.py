"""
Enhanced Agentic Course Advisor - Phase 1: LLM Integration
Adds GPT/Claude for intelligent natural language generation.
"""

import json
from typing import List, Dict, Optional
import chromadb
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
import os

# Import configuration
try:
    from config import (
        OPENAI_API_KEY, ANTHROPIC_API_KEY, AI_PROVIDER,
        OPENAI_MODEL, ANTHROPIC_MODEL, TEMPERATURE, MAX_TOKENS,
        USE_LLM_FOR_PLANNING, USE_LLM_FOR_EXPLANATIONS, USE_LLM_FOR_FOLLOWUP
    )
    
    # Initialize AI client based on provider
    if AI_PROVIDER == "openai":
        from openai import OpenAI
        ai_client = OpenAI(api_key=OPENAI_API_KEY)
        MODEL = OPENAI_MODEL
    elif AI_PROVIDER == "anthropic":
        from anthropic import Anthropic
        ai_client = Anthropic(api_key=ANTHROPIC_API_KEY)
        MODEL = ANTHROPIC_MODEL
    else:
        print("⚠️  No AI provider configured - using template-based responses")
        ai_client = None
        MODEL = None
        
except ImportError as e:
    print(f"⚠️  Config not found or API library not installed: {e}")
    print("    Falling back to template-based responses")
    ai_client = None
    AI_PROVIDER = None
    USE_LLM_FOR_PLANNING = False
    USE_LLM_FOR_EXPLANATIONS = False
    USE_LLM_FOR_FOLLOWUP = False

# Import base classes from original file
from agentic_chatbot import (
    StudentProfile, PlanningAgent as BasePlanningAgent,
    SearchAgent, AnalysisAgent
)


class EnhancedPlanningAgent(BasePlanningAgent):
    """
    Enhanced Planning Agent - Uses LLM to better understand student input.
    """
    
    def create_plan(self, profile: StudentProfile, programs_data: List[Dict]) -> Dict:
        """
        Create a plan with optional LLM enhancement for better intent understanding.
        """
        # First, get the base plan
        base_plan = super().create_plan(profile, programs_data)
        
        # If LLM is enabled, enhance the plan
        if USE_LLM_FOR_PLANNING and ai_client:
            print("   🤖 Enhancing plan with AI...")
            enhanced_priorities = self._enhance_with_llm(profile, base_plan)
            if enhanced_priorities:
                base_plan["search_priorities"] = enhanced_priorities
                print(f"   ✓ AI-enhanced priorities: {', '.join(enhanced_priorities)}")
        
        return base_plan
    
    def _enhance_with_llm(self, profile: StudentProfile, base_plan: Dict) -> Optional[List[str]]:
        """Use LLM to extract deeper insights from student input."""
        try:
            majors_str = ", ".join(profile.considering_majors)
            
            if AI_PROVIDER == "openai":
                response = ai_client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": """You are an academic advisor analyzing student interests.
Extract 2-4 key academic focus areas from their description.
Return ONLY a JSON array of focus areas like: ["business_foundation", "computing", "quantitative"]

Valid focus areas: business_foundation, computing, quantitative, stem, versatile_foundation, humanities, social_sciences"""
                        },
                        {
                            "role": "user",
                            "content": f"""Student interests: {profile.interests}
Considering majors: {majors_str}
Career goals: {profile.career_goals or 'Not specified'}"""
                        }
                    ],
                    temperature=0.3,
                    max_tokens=100
                )
                
                # Parse the response
                content = response.choices[0].message.content.strip()
                priorities = json.loads(content)
                return priorities if isinstance(priorities, list) else None
                
            elif AI_PROVIDER == "anthropic":
                response = ai_client.messages.create(
                    model=MODEL,
                    max_tokens=100,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""You are an academic advisor. Extract 2-4 key focus areas from this student profile.

Student interests: {profile.interests}
Considering majors: {majors_str}
Career goals: {profile.career_goals or 'Not specified'}

Return ONLY a JSON array like: ["business_foundation", "computing"]
Valid areas: business_foundation, computing, quantitative, stem, versatile_foundation"""
                        }
                    ]
                )
                
                content = response.content[0].text.strip()
                priorities = json.loads(content)
                return priorities if isinstance(priorities, list) else None
                
        except Exception as e:
            print(f"   ⚠️  LLM enhancement failed: {e}")
            return None


class EnhancedExplanationAgent:
    """
    Enhanced Explanation Agent - Uses LLM for personalized, natural explanations.
    """
    
    def generate_explanation(self, recommendations: List[Dict], 
                           profile: StudentProfile, plan: Dict) -> str:
        """
        Generate explanation with optional LLM enhancement.
        """
        print("\n💬 EXPLANATION AGENT: Creating recommendations...")
        
        # If LLM is enabled, use it for natural language generation
        if USE_LLM_FOR_EXPLANATIONS and ai_client:
            print("   🤖 Generating AI-powered explanation...")
            llm_explanation = self._generate_with_llm(recommendations, profile, plan)
            if llm_explanation:
                return llm_explanation
        
        # Fallback to template-based explanation
        return self._generate_template_explanation(recommendations, profile)
    
    def _generate_with_llm(self, recommendations: List[Dict], 
                          profile: StudentProfile, plan: Dict) -> Optional[str]:
        """Use LLM to generate personalized explanation."""
        try:
            # Prepare recommendation data
            rec_summary = []
            for i, rec in enumerate(recommendations[:5], 1):
                rec_summary.append({
                    "rank": i,
                    "course": f"{rec['course_name']} - {rec['title']}",
                    "description": rec['description'],
                    "programs_count": rec['program_count'],
                    "applicable_majors": rec.get('applicable_majors', []),
                    "versatility_score": rec['versatility_score'],
                    "prerequisites": rec.get('prereq_status', 'Check with advisor')
                })
            
            majors_str = ", ".join(profile.considering_majors)
            
            system_prompt = """You are an enthusiastic BYU academic advisor helping undecided first-year students.

Your job is to explain course recommendations in a clear, encouraging, and personalized way.

Guidelines:
- Be conversational and supportive
- Explain WHY each course is valuable for THEIR specific situation
- Highlight courses that can apply to multiple majors (keeps options open)
- Minimize risk of taking unnecessary courses
- Maximize chance of courses applying to the major I will choose
- Mention versatility scores to show flexibility
- Be encouraging about exploration
- Use emojis sparingly (1-2 per section)
- Keep explanations concise but informative
- Format with markdown (bold, bullet points)"""

            user_prompt = f"""Create a personalized course recommendation explanation for this student:

**Student Profile:**
- Interests: {profile.interests}
- Considering majors: {majors_str}
- Career goals: {profile.career_goals or 'Still exploring'}

**Recommended Courses:**
{json.dumps(rec_summary, indent=2)}

**Instructions:**
1. Start with a brief personalized introduction
2. For each of the top 5 courses, explain:
   - Why it's great for THEIR specific interests
   - How many majors it applies to (if > 1, emphasize flexibility!)
   - A unique insight or benefit
3. End with strategic advice about keeping options open
4. Use markdown formatting
5. Keep total length under 800 words"""

            if AI_PROVIDER == "openai":
                response = ai_client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS
                )
                return response.choices[0].message.content.strip()
                
            elif AI_PROVIDER == "anthropic":
                response = ai_client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                    messages=[
                        {
                            "role": "user",
                            "content": f"{system_prompt}\n\n{user_prompt}"
                        }
                    ]
                )
                return response.content[0].text.strip()
                
        except Exception as e:
            print(f"   ⚠️  LLM generation failed: {e}")
            return None
    
    def _generate_template_explanation(self, recommendations: List[Dict], 
                                      profile: StudentProfile) -> str:
        """Fallback template-based explanation."""
        explanation = []
        
        majors_str = ", ".join(profile.considering_majors)
        explanation.append(
            f"Based on your interest in {majors_str} and your goals around "
            f"{profile.interests.lower()}, here are my top course recommendations:\n"
        )
        
        for i, rec in enumerate(recommendations[:5], 1):
            explanation.append(f"\n**{i}. {rec['course_name']} - {rec['title']}**")
            explanation.append(f"{rec['description']}\n")
            
            if rec['program_count'] > 1:
                explanation.append(
                    f"✨ Applies to **{rec['program_count']} different majors** - keeps your options open!"
                )
            
            if rec.get('applicable_majors'):
                majors_list = ", ".join(rec['applicable_majors'])
                explanation.append(f"📚 Relevant to: {majors_list}")
            
            explanation.append(
                f"📊 Versatility score: **{rec['versatility_score']}/100**\n"
            )
        
        explanation.append(
            "\n💡 **Strategic Advice:** "
            "These courses provide a strong foundation while keeping multiple major options open!"
        )
        
        return "\n".join(explanation)


class ConversationalAgent:
    """
    NEW Agent 5: Handles follow-up questions and clarifications.
    """
    
    def __init__(self):
        self.conversation_history = []
    
    def answer_followup(self, question: str, context: Dict) -> str:
        """
        Answer follow-up questions about recommendations.
        """
        if not USE_LLM_FOR_FOLLOWUP or not ai_client:
            return "I'd be happy to answer questions, but LLM is not configured. Please check config.py"
        
        try:
            # Build context from previous recommendations
            context_str = json.dumps({
                "recommendations": context.get("recommendations", [])[:5],
                "student_profile": {
                    "interests": context.get("profile", {}).get("interests", ""),
                    "majors": context.get("profile", {}).get("considering_majors", [])
                }
            }, indent=2)
            
            if AI_PROVIDER == "openai":
                response = ai_client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a helpful BYU academic advisor. Answer questions about the course recommendations clearly and concisely.
Keep responses under 200 words. Be encouraging and informative."""
                        },
                        {
                            "role": "user",
                            "content": f"Context: {context_str}\n\nStudent question: {question}"
                        }
                    ],
                    temperature=0.7,
                    max_tokens=300
                )
                return response.choices[0].message.content.strip()
                
            elif AI_PROVIDER == "anthropic":
                response = ai_client.messages.create(
                    model=MODEL,
                    max_tokens=300,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""You are a BYU academic advisor. Answer this student's question about their course recommendations.

Context: {context_str}

Student question: {question}

Keep your response under 200 words, be encouraging and informative."""
                        }
                    ]
                )
                return response.content[0].text.strip()
                
        except Exception as e:
            return f"Sorry, I encountered an error: {e}"


class EnhancedAgenticCourseAdvisor:
    """
    Enhanced main coordinator with LLM-powered agents.
    """
    
    def __init__(self, data_dir: str = "data", db_dir: str = "chroma_db"):
        print("\n🚀 Initializing Enhanced Agentic Course Advisor...")
        
        # Load data
        self.programs_data = self._load_json(f"{data_dir}/programs.json")
        self.classes_data = self._load_json(f"{data_dir}/classes.json")
        
        # Initialize agents (enhanced versions)
        self.planning_agent = EnhancedPlanningAgent()
        self.search_agent = SearchAgent(db_dir)
        self.analysis_agent = AnalysisAgent(self.programs_data, self.classes_data)
        self.explanation_agent = EnhancedExplanationAgent()
        self.conversational_agent = ConversationalAgent()
        
        # Show which features are enabled
        features = []
        if USE_LLM_FOR_PLANNING:
            features.append("AI Planning")
        if USE_LLM_FOR_EXPLANATIONS:
            features.append("AI Explanations")
        if USE_LLM_FOR_FOLLOWUP:
            features.append("AI Q&A")
        
        if features:
            print(f"✓ Enhanced features enabled: {', '.join(features)}")
            print(f"✓ Using {AI_PROVIDER.upper()} ({MODEL})")
        else:
            print("✓ Running in template mode (no API key configured)")
        
        print("✓ All agents initialized!")
    
    def _load_json(self, filepath: str) -> List[Dict]:
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def get_recommendations(self, profile: StudentProfile) -> Dict:
        """
        Main workflow with enhanced LLM capabilities.
        """
        print("\n" + "=" * 70)
        print("🎯 ENHANCED AGENTIC WORKFLOW: COURSE RECOMMENDATION SYSTEM")
        print("=" * 70)
        
        # Agent 1: Planning (Enhanced with LLM)
        plan = self.planning_agent.create_plan(profile, self.programs_data)
        
        # Agent 2: Search (Vector DB - unchanged, still fast!)
        candidates = self.search_agent.search_courses(plan, profile)
        
        # Agent 3: Analysis (Rule-based scoring)
        recommendations = self.analysis_agent.analyze_and_rank(
            candidates, plan, profile
        )
        
        # Agent 4: Explanation (Enhanced with LLM)
        explanation = self.explanation_agent.generate_explanation(
            recommendations, profile, plan
        )
        
        print("\n" + "=" * 70)
        print("✅ ENHANCED WORKFLOW COMPLETE")
        print("=" * 70)
        
        return {
            "recommendations": recommendations,
            "explanation": explanation,
            "plan": plan,
            "profile": {
                "interests": profile.interests,
                "considering_majors": profile.considering_majors,
                "career_goals": profile.career_goals
            }
        }
    
    def ask_followup(self, question: str, context: Dict) -> str:
        """
        Agent 5: Answer follow-up questions about recommendations.
        """
        return self.conversational_agent.answer_followup(question, context)


# Test function
def test_enhanced_advisor():
    """Test the enhanced advisor."""
    advisor = EnhancedAgenticCourseAdvisor()
    
    profile = StudentProfile(
        interests="business and technology, interested in how tech companies work",
        considering_majors=["Information Systems", "Finance", "Computer Science"],
        career_goals="Work in tech consulting or product management"
    )
    
    result = advisor.get_recommendations(profile)
    print("\n" + "=" * 70)
    print("EXPLANATION:")
    print("=" * 70)
    print(result["explanation"])
    
    # Test follow-up
    if USE_LLM_FOR_FOLLOWUP:
        print("\n" + "=" * 70)
        print("TESTING FOLLOW-UP Q&A:")
        print("=" * 70)
        followup = advisor.ask_followup(
            "Which of these courses is best to take in my first semester?",
            result
        )
        print(followup)


if __name__ == "__main__":
    test_enhanced_advisor()
