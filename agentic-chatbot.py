"""
Agentic Course Advisor Chatbot - Multi-agent system for course recommendations.

This implements an agentic workflow with multiple specialized agents:
1. Planning Agent - Understands student goals and creates a plan
2. Search Agent - Finds relevant courses from vector DB
3. Analysis Agent - Evaluates course overlap and compatibility
4. Explanation Agent - Provides clear reasoning for recommendations
"""

import json
from typing import List, Dict, Tuple
import chromadb
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass

@dataclass
class StudentProfile:
    """Student information and preferences."""
    interests: str
    considering_majors: List[str]
    career_goals: str = ""
    completed_courses: List[str] = None
    skills: List[str] = None
    
    def __post_init__(self):
        if self.completed_courses is None:
            self.completed_courses = []
        if self.skills is None:
            self.skills = []


class PlanningAgent:
    """
    Agent 1: Analyzes student input and creates a recommendation strategy.
    """
    
    def create_plan(self, profile: StudentProfile, programs_data: List[Dict]) -> Dict:
        """
        Create a structured plan for course recommendations.
        
        Returns:
            Plan with target areas, priorities, and search strategy
        """
        print("\n🤖 PLANNING AGENT: Analyzing student profile...")
        
        # Identify relevant program categories
        categories = set()
        relevant_programs = []
        
        for prog in programs_data:
            if any(major.lower() in prog['program_name'].lower() 
                   for major in profile.considering_majors):
                categories.add(prog['program_category'])
                relevant_programs.append(prog['program_name'])
        
        # Build search strategy
        plan = {
            "student_interests": profile.interests,
            "target_categories": list(categories),
            "relevant_programs": relevant_programs,
            "search_priorities": [],
            "recommendations_needed": 5
        }
        
        # Determine search priorities
        if "business" in profile.interests.lower() or "Business" in categories:
            plan["search_priorities"].append("business_foundation")
        if any(term in profile.interests.lower() for term in ["program", "tech", "computer", "software"]):
            plan["search_priorities"].append("computing")
        if any(term in profile.interests.lower() for term in ["math", "data", "analytics", "statistics"]):
            plan["search_priorities"].append("quantitative")
        if any(term in profile.interests.lower() for term in ["science", "physics", "engineering"]):
            plan["search_priorities"].append("stem")
        
        # Default priority if nothing specific
        if not plan["search_priorities"]:
            plan["search_priorities"].append("versatile_foundation")
        
        print(f"   ✓ Identified {len(relevant_programs)} relevant programs")
        print(f"   ✓ Target categories: {', '.join(categories)}")
        print(f"   ✓ Search priorities: {', '.join(plan['search_priorities'])}")
        
        return plan


class SearchAgent:
    """
    Agent 2: Queries the vector database for relevant courses.
    """
    
    def __init__(self, db_path: str = "chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.overlap_col = self.client.get_collection("overlap")
        self.classes_col = self.client.get_collection("classes")
    
    def search_courses(self, plan: Dict, profile: StudentProfile, 
                      n_results: int = 10) -> List[Dict]:
        """
        Search for courses based on the plan.
        
        Returns:
            List of candidate courses with metadata
        """
        print("\n🔍 SEARCH AGENT: Querying vector database...")
        
        # Build comprehensive search query
        query_parts = [
            profile.interests,
            f"majors: {', '.join(profile.considering_majors)}"
        ]
        
        if profile.career_goals:
            query_parts.append(f"career goals: {profile.career_goals}")
        
        if plan["search_priorities"]:
            query_parts.append(f"focus areas: {', '.join(plan['search_priorities'])}")
        
        query = " | ".join(query_parts)
        
        # Search overlap collection (multi-major courses)
        overlap_results = self.overlap_col.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Convert to structured format
        candidates = []
        for doc, metadata, distance in zip(
            overlap_results['documents'][0],
            overlap_results['metadatas'][0],
            overlap_results['distances'][0]
        ):
            candidates.append({
                "course_id": metadata['course_id'],
                "course_name": metadata['course_name'],
                "title": metadata['title'],
                "program_count": metadata['program_count'],
                "versatility_score": metadata['versatility_score'],
                "category": metadata['category'],
                "relevance_score": 1 - distance,  # Convert distance to similarity
                "document": doc
            })
        
        print(f"   ✓ Found {len(candidates)} candidate courses")
        return candidates


class AnalysisAgent:
    """
    Agent 3: Analyzes course compatibility and creates ranked recommendations.
    """
    
    def __init__(self, programs_data: List[Dict], classes_data: List[Dict]):
        self.programs_data = programs_data
        self.classes_data = classes_data
        
        # Build lookup tables
        self.class_lookup = {c['course_id']: c for c in classes_data}
        self.program_lookup = {p['program_id']: p for p in programs_data}
    
    def analyze_and_rank(self, candidates: List[Dict], plan: Dict, 
                        profile: StudentProfile) -> List[Dict]:
        """
        Analyze courses and rank by usefulness for undecided students.
        
        Returns:
            Ranked list of recommendations with detailed analysis
        """
        print("\n📊 ANALYSIS AGENT: Ranking courses...")
        
        recommendations = []
        
        for candidate in candidates:
            # Get full course details
            course_details = self.class_lookup.get(candidate['course_id'])
            if not course_details:
                continue
            
            # Calculate compatibility score
            score = self._calculate_compatibility_score(
                candidate, course_details, plan, profile
            )
            
            # Check if student can take it (prerequisites)
            can_take, prereq_status = self._check_prerequisites(
                course_details, profile.completed_courses
            )
            
            # Determine which of student's target majors this applies to
            applicable_majors = [
                major for major in profile.considering_majors
                if any(major.lower() in prog.lower() 
                      for prog in course_details['applies_to_programs'])
            ]
            
            recommendations.append({
                "course_id": candidate['course_id'],
                "course_name": candidate['course_name'],
                "title": candidate['title'],
                "credit_hours": course_details['credit_hours'],
                "description": course_details['description'],
                "prerequisites": course_details['prerequisites'],
                "category": candidate['category'],
                "program_count": candidate['program_count'],
                "versatility_score": candidate['versatility_score'],
                "compatibility_score": score,
                "can_take_now": can_take,
                "prereq_status": prereq_status,
                "applicable_majors": applicable_majors,
                "applies_to_programs": course_details['applies_to_programs']
            })
        
        # Sort by compatibility score
        recommendations.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        print(f"   ✓ Ranked {len(recommendations)} courses")
        return recommendations[:5]  # Return top 5
    
    def _calculate_compatibility_score(self, candidate: Dict, 
                                      course_details: Dict,
                                      plan: Dict, profile: StudentProfile) -> float:
        """Calculate how well a course fits the student's needs."""
        score = 0.0
        
        # Base score from relevance
        score += candidate['relevance_score'] * 30
        
        # Versatility bonus (more majors = better for undecided)
        score += (candidate['program_count'] / 6) * 30  # Normalized to max 6 programs
        
        # Category match bonus
        if candidate['category'].lower() in plan['search_priorities']:
            score += 20
        
        # Applicable to student's considering majors
        applicable_count = sum(
            1 for major in profile.considering_majors
            if any(major.lower() in prog.lower() 
                  for prog in course_details['applies_to_programs'])
        )
        score += (applicable_count / len(profile.considering_majors)) * 20
        
        return min(score, 100)  # Cap at 100
    
    def _check_prerequisites(self, course: Dict, 
                           completed: List[str]) -> Tuple[bool, str]:
        """Check if student has completed prerequisites."""
        prereqs = course['prerequisites']
        
        if not prereqs or prereqs.strip() == "":
            return True, "No prerequisites required"
        
        # Simple check (in real system, would parse prereq logic)
        if completed:
            return True, f"Prerequisites: {prereqs} (check with advisor)"
        
        return True, f"Prerequisites: {prereqs}"


class ExplanationAgent:
    """
    Agent 4: Generates natural language explanations for recommendations.
    """
    
    def generate_explanation(self, recommendations: List[Dict], 
                           profile: StudentProfile, plan: Dict) -> str:
        """
        Create a comprehensive explanation of recommendations.
        
        Returns:
            Natural language explanation
        """
        print("\n💬 EXPLANATION AGENT: Creating recommendations...")
        
        explanation = []
        
        # Introduction
        majors_str = ", ".join(profile.considering_majors)
        explanation.append(
            f"Based on your interest in {majors_str} and your goals around "
            f"{profile.interests.lower()}, here are my top course recommendations:\n"
        )
        
        # Recommendations with detailed explanations
        for i, rec in enumerate(recommendations, 1):
            explanation.append(f"\n{i}. **{rec['course_name']} - {rec['title']}** "
                             f"({rec['credit_hours']} credits)")
            explanation.append(f"   {rec['description']}")
            
            # Why it's recommended
            explanation.append(f"\n   ✨ **Why this course:**")
            
            if rec['program_count'] > 1:
                explanation.append(
                    f"   • Applies to **{rec['program_count']} different majors** - "
                    f"keeps your options open!"
                )
            
            if rec['applicable_majors']:
                majors_list = ", ".join(rec['applicable_majors'])
                explanation.append(
                    f"   • Directly relevant to your interests: **{majors_list}**"
                )
            
            explanation.append(
                f"   • Versatility score: **{rec['versatility_score']}/100** "
                f"(higher = more flexible)"
            )
            
            # Prerequisites
            explanation.append(f"\n   📋 {rec['prereq_status']}")
            
            if rec['compatibility_score'] >= 80:
                explanation.append("   🌟 **Highly recommended** for your situation!")
        
        # Summary advice
        explanation.append(
            f"\n\n💡 **Strategic Advice:**\n"
            f"Taking these courses will give you a strong foundation while "
            f"keeping multiple major options open. They're all valuable regardless "
            f"of which path you ultimately choose!"
        )
        
        return "\n".join(explanation)


class AgenticCourseAdvisor:
    """
    Main coordinator that orchestrates all agents in an agentic workflow.
    """
    
    def __init__(self, data_dir: str = "data", db_dir: str = "chroma_db"):
        print("\n🚀 Initializing Agentic Course Advisor...")
        
        # Load data
        self.programs_data = self._load_json(f"{data_dir}/programs.json")
        self.classes_data = self._load_json(f"{data_dir}/classes.json")
        
        # Initialize agents
        self.planning_agent = PlanningAgent()
        self.search_agent = SearchAgent(db_dir)
        self.analysis_agent = AnalysisAgent(self.programs_data, self.classes_data)
        self.explanation_agent = ExplanationAgent()
        
        print("✓ All agents initialized!")
    
    def _load_json(self, filepath: str) -> List[Dict]:
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def get_recommendations(self, profile: StudentProfile) -> Dict:
        """
        Main workflow: orchestrates all agents to generate recommendations.
        
        This is the AGENTIC part - multiple specialized agents working together!
        """
        print("\n" + "=" * 70)
        print("🎯 AGENTIC WORKFLOW: COURSE RECOMMENDATION SYSTEM")
        print("=" * 70)
        
        # Agent 1: Planning
        plan = self.planning_agent.create_plan(profile, self.programs_data)
        
        # Agent 2: Search
        candidates = self.search_agent.search_courses(plan, profile)
        
        # Agent 3: Analysis
        recommendations = self.analysis_agent.analyze_and_rank(
            candidates, plan, profile
        )
        
        # Agent 4: Explanation
        explanation = self.explanation_agent.generate_explanation(
            recommendations, profile, plan
        )
        
        print("\n" + "=" * 70)
        print("✅ WORKFLOW COMPLETE")
        print("=" * 70)
        
        return {
            "recommendations": recommendations,
            "explanation": explanation,
            "plan": plan
        }


# Example usage and testing
def test_advisor():
    """Test the agentic advisor with sample student profiles."""
    advisor = AgenticCourseAdvisor()
    
    # Test Case 1: Student considering business and tech
    print("\n\n" + "=" * 70)
    print("TEST CASE 1: Business + Tech Student")
    print("=" * 70)
    
    profile1 = StudentProfile(
        interests="business and technology, want to understand both sides",
        considering_majors=["Information Systems", "Finance", "Computer Science"],
        career_goals="Work in tech consulting or fintech"
    )
    
    result1 = advisor.get_recommendations(profile1)
    print("\n" + result1["explanation"])
    
    # Test Case 2: STEM undecided
    print("\n\n" + "=" * 70)
    print("TEST CASE 2: STEM Undecided Student")
    print("=" * 70)
    
    profile2 = StudentProfile(
        interests="math, data, and programming",
        considering_majors=["Computer Science", "Mathematics", "Statistics"],
        career_goals="Data science or software engineering"
    )
    
    result2 = advisor.get_recommendations(profile2)
    print("\n" + result2["explanation"])


if __name__ == "__main__":
    test_advisor()
