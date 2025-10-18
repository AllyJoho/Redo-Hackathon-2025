"""
Phase 3: Interactive Chat Agent
Handles conversational interactions with context awareness and memory
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

try:
    from config import OPENAI_API_KEY
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False
    client = None


@dataclass
class ChatMessage:
    """Represents a single chat message"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    metadata: Optional[Dict] = None


class ChatAgent:
    """
    Intelligent chat agent that maintains conversation context
    and provides natural, helpful responses about course recommendations
    """
    
    def __init__(self):
        self.chat_history: List[ChatMessage] = []
        self.context = {
            "recommendations": [],
            "student_profile": {},
            "current_topic": None
        }
        
        # Initialize with system message
        self._add_system_message()
    
    def _add_system_message(self):
        """Set up the system prompt for the chat agent"""
        system_prompt = """You are a helpful BYU course advisor assistant specializing in helping undecided first-year students. 
You help students understand course recommendations, explore different majors, and make informed decisions.

Key responsibilities:
- Explain why specific courses were recommended
- Discuss career paths and major options
- Answer questions about prerequisites, difficulty, and workload
- Help students understand how courses apply to different majors
- Be encouraging and supportive
- Keep responses concise but informative (2-4 sentences typically)

Tone: Friendly, knowledgeable, encouraging, concise"""
        
        self.chat_history.append(ChatMessage(
            role="system",
            content=system_prompt
        ))
    
    def update_context(self, recommendations: List[Dict], profile: Dict):
        """Update the conversation context with new recommendations and profile"""
        self.context["recommendations"] = recommendations
        self.context["student_profile"] = profile
        
        # Add context message to chat
        context_msg = f"""Current student profile:
- Interests: {profile.get('interests', 'Not specified')}
- Considering majors: {', '.join(profile.get('considering_majors', []))}
- Career goals: {profile.get('career_goals', 'Not specified')}

Top recommended courses:
"""
        for i, rec in enumerate(recommendations[:5], 1):
            context_msg += f"{i}. {rec['course_name']} - {rec['title']}\n"
        
        self.chat_history.append(ChatMessage(
            role="system",
            content=context_msg,
            metadata={"type": "context_update"}
        ))
    
    def chat(self, user_message: str) -> str:
        """
        Process a user message and generate a response
        
        Args:
            user_message: The user's question or comment
            
        Returns:
            Assistant's response
        """
        # Add user message to history
        self.chat_history.append(ChatMessage(
            role="user",
            content=user_message
        ))
        
        # Detect intent
        intent = self._detect_intent(user_message)
        
        # Generate response based on AI availability
        if AI_AVAILABLE:
            response = self._generate_ai_response(user_message, intent)
        else:
            response = self._generate_template_response(user_message, intent)
        
        # Add assistant response to history
        self.chat_history.append(ChatMessage(
            role="assistant",
            content=response,
            metadata={"intent": intent}
        ))
        
        return response
    
    def _detect_intent(self, message: str) -> str:
        """Detect the user's intent from their message"""
        message_lower = message.lower()
        
        # Intent patterns
        if any(word in message_lower for word in ["why", "explain", "reasoning"]):
            return "explanation"
        elif any(word in message_lower for word in ["tell me more", "more about", "details"]):
            return "details"
        elif any(word in message_lower for word in ["hard", "difficult", "easy", "workload"]):
            return "difficulty"
        elif any(word in message_lower for word in ["prerequisite", "prereq", "requirement"]):
            return "prerequisites"
        elif any(word in message_lower for word in ["career", "job", "work"]):
            return "career"
        elif any(word in message_lower for word in ["major", "program", "degree"]):
            return "major"
        elif any(word in message_lower for word in ["alternative", "other", "different", "instead"]):
            return "alternatives"
        elif any(word in message_lower for word in ["schedule", "when", "semester"]):
            return "scheduling"
        else:
            return "general"
    
    def _generate_ai_response(self, message: str, intent: str) -> str:
        """Generate response using GPT"""
        try:
            # Build messages for API
            api_messages = []
            
            # Add last 10 messages for context (excluding system context updates)
            for msg in self.chat_history[-10:]:
                if msg.metadata and msg.metadata.get("type") == "context_update":
                    continue
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Add current user message
            api_messages.append({
                "role": "user",
                "content": message
            })
            
            # Call OpenAI API only if client is available
            if client is not None:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages,
                    max_tokens=200,
                    temperature=0.7
                )
                content = response.choices[0].message.content
                return content.strip() if content is not None else ""
            else:
                raise RuntimeError("OpenAI client is not available.")
            
        except Exception as e:
            print(f"AI generation error: {e}")
            return self._generate_template_response(message, intent)
    
    def _generate_template_response(self, message: str, intent: str) -> str:
        """Generate template-based response (fallback)"""
        recs = self.context.get("recommendations", [])
        profile = self.context.get("student_profile", {})
        
        if intent == "explanation":
            if recs:
                course = recs[0]
                return f"Great question! {course['course_name']} was recommended because it's highly versatile (applies to {course.get('program_count', 0)} majors) and aligns well with your interests in {profile.get('interests', 'your chosen fields')}. It's a strategic choice that keeps your options open!"
            return "These courses were chosen based on their versatility and alignment with your interests and potential majors."
        
        elif intent == "details":
            if recs:
                course = recs[0]
                return f"Let me tell you more about {course['title']}! {course['description']} This course has a versatility score of {course.get('versatility_score', 0):.0f}/100 and applies to multiple majors including {', '.join(course.get('applicable_majors', [])[:3])}."
            return "I'd be happy to provide more details about any specific course. Which one interests you?"
        
        elif intent == "difficulty":
            return "Great question about difficulty! As a first-year student, I'd recommend starting with foundational courses. The ones I've recommended are appropriate for your level and will build essential skills. Always check with your advisor about workload balance!"
        
        elif intent == "prerequisites":
            if recs:
                course = recs[0]
                prereq = course.get('prereq_status', 'Check with advisor')
                return f"For {course['course_name']}, the prerequisites are: {prereq}. Most of these recommended courses are designed to be accessible to first-year students!"
            return "Most of these courses are accessible to first-year students, but it's always good to verify prerequisites with your advisor."
        
        elif intent == "career":
            goals = profile.get('career_goals', '')
            if goals:
                return f"Considering your interest in {goals}, these courses provide foundational knowledge that will be valuable. They also keep multiple career paths open while you explore your options!"
            return "These courses offer great foundations for various career paths! They're versatile enough to support multiple directions as you discover what excites you most."
        
        elif intent == "major":
            majors = profile.get('considering_majors', [])
            if majors:
                return f"Since you're considering {', '.join(majors)}, I've focused on courses that apply to multiple programs. This strategy lets you explore while making progress toward several potential majors!"
            return "These courses are strategically chosen to apply to multiple majors, giving you flexibility as you explore your options!"
        
        elif intent == "alternatives":
            return "Absolutely! I can adjust recommendations based on your preferences. What would you like to change? (e.g., easier courses, different focus area, more technical/creative options)"
        
        elif intent == "scheduling":
            return "Most of these courses are offered multiple semesters. I'd recommend taking 2-3 of these per semester alongside your general education requirements. Your advisor can help you build a specific schedule!"
        
        else:  # general
            return "I'm here to help you understand these course recommendations and explore your options! Feel free to ask about specific courses, majors, career paths, or anything else you're curious about."
    
    def get_chat_history(self, include_system: bool = False) -> List[Dict]:
        """
        Get formatted chat history for display
        
        Args:
            include_system: Whether to include system messages
            
        Returns:
            List of message dictionaries
        """
        history = []
        for msg in self.chat_history:
            # Skip system messages unless requested
            if msg.role == "system" and not include_system:
                continue
            
            # Skip context updates
            if msg.metadata and msg.metadata.get("type") == "context_update":
                continue
            
            history.append({
                "role": msg.role,
                "content": msg.content,
                "metadata": msg.metadata
            })
        
        return history
    
    def clear_history(self):
        """Clear chat history and reset context"""
        self.chat_history.clear()
        self._add_system_message()
        self.context = {
            "recommendations": [],
            "student_profile": {},
            "current_topic": None
        }
    
    def get_suggested_questions(self) -> List[str]:
        """Generate suggested follow-up questions based on context"""
        suggestions = []
        
        recs = self.context.get("recommendations", [])
        profile = self.context.get("student_profile", {})
        
        if recs:
            # Course-specific questions
            first_course = recs[0]
            suggestions.append(f"Tell me more about {first_course['course_name']}")
            suggestions.append(f"Why was {first_course['course_name']} recommended?")
            
            # General questions
            suggestions.append("What are the prerequisites for these courses?")
            suggestions.append("How difficult are these courses?")
            
            # Major-related
            if profile.get('considering_majors'):
                suggestions.append("How do these courses relate to my potential majors?")
            
            # Career-related
            if profile.get('career_goals'):
                suggestions.append("How will these courses help my career goals?")
        
        return suggestions[:4]  # Return top 4 suggestions


if __name__ == "__main__":
    # Test the chat agent
    print("🤖 Testing Chat Agent...")
    
    agent = ChatAgent()
    
    # Simulate context
    test_recs = [
        {
            "course_name": "ACCTG 200",
            "title": "Financial Accounting",
            "description": "Introduction to financial accounting principles",
            "versatility_score": 85,
            "program_count": 3,
            "applicable_majors": ["Business", "Accounting", "Finance"]
        }
    ]
    
    test_profile = {
        "interests": "business and data analysis",
        "considering_majors": ["Business", "Information Systems"],
        "career_goals": "consulting or data analytics"
    }
    
    agent.update_context(test_recs, test_profile)
    
    # Test conversation
    test_messages = [
        "Why was ACCTG 200 recommended?",
        "How difficult is this course?",
        "Tell me more about the prerequisites"
    ]
    
    for msg in test_messages:
        print(f"\n👤 User: {msg}")
        response = agent.chat(msg)
        print(f"🤖 Assistant: {response}")
    
    print("\n\n💡 Suggested questions:")
    for q in agent.get_suggested_questions():
        print(f"  - {q}")
    
    print("\n✅ Chat agent test complete!")
