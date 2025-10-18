"""
AI Chatbot utility for analyzing student interests and matching with majors
"""
import os
from typing import List, Dict, Any
from openai import OpenAI

class MajorAdvisorChatbot:
    """AI-powered chatbot for major exploration and scheduling"""
    
    def __init__(self, majors_data: List[Dict[str, Any]]):
        """
        Initialize the chatbot with major data
        
        Args:
            majors_data: List of major information dictionaries
        """
        self.majors_data = majors_data
        api_key = os.getenv('OPENAI_API_KEY', '')
        self.use_mock = not api_key or api_key == 'your-openai-api-key-here'
        
        if not self.use_mock:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
    
    def analyze_interests(self, user_message: str) -> Dict[str, Any]:
        """
        Analyze user interests and provide major recommendations
        
        Args:
            user_message: User's message describing their interests
            
        Returns:
            Dictionary with recommendations and analysis
        """
        if self.use_mock:
            return self._mock_analysis(user_message)
        
        try:
            # Create context about available majors
            majors_context = self._create_majors_context()
            
            # Create the prompt for OpenAI
            system_prompt = f"""You are an AI advisor for BYU students helping them explore majors.
You have access to the following majors at BYU:

{majors_context}

Your role is to:
1. Understand student interests from their messages
2. Match their interests with suitable majors
3. Explain why certain majors fit their interests
4. Suggest courses that keep multiple academic paths open
5. Help them avoid wasted credits

Be friendly, encouraging, and informative. Provide specific major recommendations with reasoning."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            
            # Extract recommended majors from the response
            recommended_majors = self._extract_recommended_majors(ai_response)
            
            return {
                "response": ai_response,
                "recommended_majors": recommended_majors,
                "success": True
            }
            
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return self._mock_analysis(user_message)
    
    def _create_majors_context(self) -> str:
        """Create a formatted context string about available majors"""
        context = []
        for major in self.majors_data:
            context.append(
                f"- {major['name']} ({major['college']}): {major['description']}\n"
                f"  Key interests: {', '.join(major['interests'])}\n"
                f"  Career paths: {', '.join(major['career_paths'])}"
            )
        return "\n\n".join(context)
    
    def _extract_recommended_majors(self, ai_response: str) -> List[str]:
        """Extract major IDs mentioned in the AI response"""
        recommended = []
        for major in self.majors_data:
            if major['name'].lower() in ai_response.lower():
                recommended.append(major['id'])
        return recommended
    
    def _mock_analysis(self, user_message: str) -> Dict[str, Any]:
        """Provide mock recommendations when OpenAI is not available"""
        message_lower = user_message.lower()
        
        # Simple keyword-based matching
        recommendations = []
        
        if any(word in message_lower for word in ['code', 'program', 'software', 'computer', 'tech']):
            recommendations.append('cs')
        if any(word in message_lower for word in ['business', 'entrepreneur', 'manage', 'finance', 'money']):
            recommendations.append('business')
        if any(word in message_lower for word in ['help', 'people', 'counsel', 'psychology', 'mind', 'behavior']):
            recommendations.append('psychology')
        if any(word in message_lower for word in ['engineer', 'build', 'design', 'machine', 'mechanical']):
            recommendations.append('mechanical-engineering')
        if any(word in message_lower for word in ['nurse', 'healthcare', 'medical', 'patient', 'hospital']):
            recommendations.append('nursing')
        if any(word in message_lower for word in ['write', 'literature', 'english', 'story', 'book']):
            recommendations.append('english')
        if any(word in message_lower for word in ['biology', 'science', 'nature', 'lab', 'research']):
            recommendations.append('biology')
        if any(word in message_lower for word in ['account', 'tax', 'audit', 'numbers', 'finance']):
            recommendations.append('accounting')
        
        # Default recommendations if no matches
        if not recommendations:
            recommendations = ['cs', 'business', 'psychology']
        
        # Get major names for response
        major_names = [m['name'] for m in self.majors_data if m['id'] in recommendations[:3]]
        
        response = f"""Based on your interests, I'd recommend exploring these majors at BYU:

{', '.join(major_names[:3])}

These majors align well with what you've shared. Here's why:

"""
        
        for major_id in recommendations[:3]:
            major = next((m for m in self.majors_data if m['id'] == major_id), None)
            if major:
                response += f"• {major['name']}: {major['description']}\n\n"
        
        response += """I can help you create a first-year schedule that keeps multiple paths open. Would you like to see recommended courses?"""
        
        return {
            "response": response,
            "recommended_majors": recommendations[:3],
            "success": True
        }
    
    def generate_schedule(self, major_ids: List[str], semester: str = "Fall") -> Dict[str, Any]:
        """
        Generate an optimized course schedule that keeps multiple paths open
        
        Args:
            major_ids: List of major IDs to consider
            semester: Which semester (Fall/Winter)
            
        Returns:
            Dictionary with schedule recommendations
        """
        # Find common courses across selected majors
        selected_majors = [m for m in self.majors_data if m['id'] in major_ids]
        
        if not selected_majors:
            return {"schedule": [], "reasoning": "No valid majors selected", "success": False}
        
        # Collect all first-year courses
        all_courses = []
        course_counts = {}
        
        for major in selected_majors:
            for course in major.get('first_year_courses', []):
                if course not in course_counts:
                    course_counts[course] = 0
                course_counts[course] += 1
                if course not in all_courses:
                    all_courses.append(course)
        
        # Sort courses by how many majors they apply to (prioritize common courses)
        sorted_courses = sorted(all_courses, key=lambda c: course_counts.get(c, 0), reverse=True)
        
        # Typical 15-credit semester = 5 courses (3 credits each)
        recommended_schedule = sorted_courses[:5]
        
        reasoning = f"""This schedule is optimized to keep your options open for {len(selected_majors)} potential majors:
{', '.join([m['name'] for m in selected_majors])}

The courses are selected because:
"""
        
        for course in recommended_schedule:
            count = course_counts.get(course, 0)
            if count > 1:
                reasoning += f"• {course}: Required for {count} of your potential majors\n"
            elif course in ["English 115", "GE electives"]:
                reasoning += f"• {course}: University requirement that doesn't limit your major choice\n"
            else:
                reasoning += f"• {course}: Important prerequisite for your selected path\n"
        
        return {
            "schedule": recommended_schedule,
            "reasoning": reasoning,
            "majors_considered": [m['name'] for m in selected_majors],
            "semester": semester,
            "success": True
        }
