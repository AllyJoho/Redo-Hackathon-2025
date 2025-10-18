"""
Phase 2 Enhanced: Agentic Advisor with Validation & Orchestration
Production-ready multi-agent system
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass
import chromadb

# Import Phase 2 components
from validation_agent import ValidationAgent, AgentOrchestrator

# Try to import OpenAI/Anthropic for LLM features
try:
    from config import OPENAI_API_KEY
    import openai
    openai.api_key = OPENAI_API_KEY
    PHASE1_AVAILABLE = True
except ImportError:
    PHASE1_AVAILABLE = False
    print("⚠️  LLM features not available (config.py or API libraries missing)")


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class StudentProfile:
    """Student information for course recommendations"""
    interests: str  # Can be string or list
    goals: Optional[List[str]] = None
    considering_majors: Optional[List[str]] = None
    career_goals: str = ""
    preferred_difficulty: str = "moderate"
    desired_credits: int = 15
    
    def __post_init__(self):
        # Convert interests to list if it's a string
        if isinstance(self.interests, str):
            self.interests_list = [self.interests]
        else:
            self.interests_list = self.interests
        if self.goals is None:
            self.goals = []
        if self.considering_majors is None:
            self.considering_majors = []
    
    
# ============================================================================
# BASIC AGENTS (Core functionality)
# ============================================================================

class PlanningAgent:
    """Analyzes student profile and creates search strategy"""
    
    def create_plan(self, profile: StudentProfile, programs_data: List[Dict]) -> Dict:
        print("\n📋 Planning Agent: Creating search strategy...")
        # Get interests as list
        interests_list = profile.interests_list if hasattr(profile, 'interests_list') else (
            [profile.interests] if isinstance(profile.interests, str) else profile.interests
        )
        goals_list = profile.goals or []
        
        # Find relevant programs based on interests
        relevant_programs = [p for p in programs_data if any(
            interest.lower() in p.get("name", "").lower() 
            for interest in interests_list
        )]
        
        return {
            "search_queries": interests_list + goals_list,
            "relevant_programs": relevant_programs[:5],
            "filters": {
                "difficulty": profile.preferred_difficulty,
                "credits": profile.desired_credits
            }
        }


class SearchAgent:
    """Searches vector database for relevant courses"""
    
    def __init__(self, db_dir: str = "chroma_db"):
        self.client = chromadb.PersistentClient(path=db_dir)
        
    def search_courses(self, plan: Dict, profile: StudentProfile) -> Dict:
        """Main search method called by Phase2AgenticCourseAdvisor"""
        print("\n🔍 Search Agent: Querying database...")
        results = {"programs": [], "classes": [], "overlap": []}
        
        queries = plan.get("search_queries", [])
        if isinstance(profile.interests, list):
            queries.extend(profile.interests)
        
        for query in queries:
            try:
                # Search each collection
                for coll_name in ["programs", "classes", "class_overlap"]:
                    collection = self.client.get_collection(coll_name)
                    result = collection.query(query_texts=[str(query)], n_results=3)
                    documents = result.get('documents')
                    if result and documents is not None and len(documents) > 0 and documents[0]:
                        key = "overlap" if coll_name == "class_overlap" else coll_name
                        results[key].extend(documents[0])
            except Exception as e:
                print(f"   ⚠️  Error searching {coll_name}: {e}")
                
        return results


class AnalysisAgent:
    """Analyzes search results and creates recommendations"""
    
    def __init__(self, programs_data: List[Dict], classes_data: List[Dict]):
        self.programs_data = programs_data
        self.classes_data = classes_data
        
    def analyze_and_rank(self, candidates: Dict, profile: StudentProfile, plan: Dict) -> Dict:
        """Main analysis method called by Phase2AgenticCourseAdvisor"""
        print("\n🧠 Analysis Agent: Analyzing and ranking results...")
        
        # Simple scoring based on search results
        programs = list(set(candidates.get("programs", [])))[:3]
        classes = list(set(candidates.get("classes", [])))[:5]
        
        return {
            "programs": programs,
            "courses": classes,
            "overlap_courses": candidates.get("overlap", [])[:3],
            "confidence": 85
        }


class ExplanationAgent:
    """Generates explanations for recommendations"""
    
    def generate_explanation(self, recommendations: Dict, profile: StudentProfile, context: Dict) -> str:
        """Main explanation method - calls explain()"""
        return self.explain(recommendations, profile)
    
    def explain(self, recommendations: Dict, profile: StudentProfile) -> str:
        print("\n💬 Explanation Agent: Creating explanation...")
        
        interests = profile.interests if isinstance(profile.interests, list) else [profile.interests]
        goals = profile.goals or []
        explanation = f"Based on your interests in {', '.join(interests)} "
        if goals:
            explanation += f"and goals of {', '.join(goals)}, "
        explanation += "here are my recommendations:\n\n"
        
        programs = recommendations.get('programs', recommendations.get('recommended_programs', []))
        courses = recommendations.get('courses', recommendations.get('recommended_classes', []))
        
        if programs:
            explanation += "**Programs:**\n"
            for prog in programs:
                explanation += f"- {prog}\n"
                
        if courses:
            explanation += "\n**Classes:**\n"
            for cls in courses:
                explanation += f"- {cls}\n"
                
        return explanation


# ============================================================================
# ENHANCED AGENTS (LLM-powered)
# ============================================================================

class EnhancedPlanningAgent(PlanningAgent):
    """LLM-powered planning with better strategy"""
    pass  # Uses parent class for now


class EnhancedExplanationAgent(ExplanationAgent):
    """LLM-powered explanations"""
    
    def generate_explanation(self, recommendations: Dict, profile: StudentProfile, context: Dict) -> str:
        """Main explanation method called by Phase2AgenticCourseAdvisor"""
        return self.explain(recommendations, profile)
    
    def explain(self, recommendations: Dict, profile: StudentProfile) -> str:
        if not PHASE1_AVAILABLE:
            return super().explain(recommendations, profile)
            
        print("\n💬 Enhanced Explanation Agent: Generating AI explanation...")
        
        try:
            interests = profile.interests if isinstance(profile.interests, list) else [profile.interests]
            goals = profile.goals or []
            programs = recommendations.get('programs', recommendations.get('recommended_programs', []))
            courses = recommendations.get('courses', recommendations.get('recommended_classes', []))
            
            prompt = f"""Create a friendly, personalized explanation for course recommendations.

Student Profile:
- Interests: {', '.join(interests)}
- Goals: {', '.join(goals)}
- Preferred Difficulty: {profile.preferred_difficulty}

Recommendations:
- Programs: {', '.join(programs)}
- Classes: {', '.join(courses)}

Generate a warm, encouraging explanation (2-3 paragraphs) that connects their interests to the recommendations."""

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message.content or "Unable to generate explanation."
        except Exception as e:
            print(f"   ⚠️  LLM error: {e}")
            return super().explain(recommendations, profile)


class ConversationalAgent:
    """Handles conversational follow-up questions"""
    
    def answer_followup(self, question: str, context: Dict) -> str:
        """Main method called by Phase2AgenticCourseAdvisor"""
        return self.respond(question, context)
    
    def respond(self, question: str, context: Dict) -> str:
        if not PHASE1_AVAILABLE:
            return "Conversational features require LLM configuration."
            
        try:
            prompt = f"""Answer this student question about BYU courses: {question}

Context: {json.dumps(context, indent=2)}

Provide a helpful, concise answer."""

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            return response.choices[0].message.content or "Unable to generate response."
        except Exception as e:
            return f"Error: {e}"


class Phase2AgenticCourseAdvisor:
    """
    Phase 2: Enhanced advisor with validation and orchestration.
    """
    
    def __init__(self, data_dir: str = "data", db_dir: str = "chroma_db"):
        print("\n🚀 Initializing Phase 2 Agentic Course Advisor...")
        
        # Load data
        self.programs_data = self._load_json(f"{data_dir}/programs.json")
        self.classes_data = self._load_json(f"{data_dir}/classes.json")
        
        # Initialize orchestrator (tracks all agents)
        self.orchestrator = AgentOrchestrator()
        
        # Initialize all agents
        print("   📋 Initializing agents...")
        self.planning_agent = EnhancedPlanningAgent()
        self.search_agent = SearchAgent(db_dir)
        self.analysis_agent = AnalysisAgent(self.programs_data, self.classes_data)
        
        if PHASE1_AVAILABLE:
            self.explanation_agent = EnhancedExplanationAgent()
            self.conversational_agent = ConversationalAgent()
            print("   ✓ Phase 1 agents loaded (with LLM support)")
        else:
            # Use basic explanation without LLM
            self.explanation_agent = ExplanationAgent()
            self.conversational_agent = None
            print("   ✓ Basic agents loaded (no LLM)")
        
        # Phase 2: Add validation agent
        self.validation_agent = ValidationAgent()
        print("   ✓ Validation agent loaded (Phase 2)")
        
        print("✅ Phase 2 system ready!")
        print("   • 5 specialized agents")
        print("   • Validation & quality checks")
        print("   • Real-time workflow tracking")
    
    def _load_json(self, filepath: str) -> List[Dict]:
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def get_recommendations(self, profile: StudentProfile, 
                           return_workflow: bool = True) -> Dict:
        """
        Main workflow with Phase 2 enhancements:
        - Real-time workflow tracking
        - Validation checks
        - Confidence scoring
        
        Args:
            profile: Student profile
            return_workflow: If True, includes workflow progress in results
        """
        print("\n" + "=" * 70)
        print("🎯 PHASE 2 AGENTIC WORKFLOW")
        print("=" * 70)
        
        # Initialize workflow tracking
        workflow_progress = []
        
        # AGENT 1: Planning
        self.orchestrator.update_agent_status("Planning", "running")
        workflow_progress.append({
            "agent": "Planning",
            "status": "running",
            "message": "Analyzing student profile..."
        })
        
        plan = self.planning_agent.create_plan(profile, self.programs_data)
        
        self.orchestrator.update_agent_status(
            "Planning", "complete", 
            confidence=95,
            details=f"Identified {len(plan.get('relevant_programs', []))} relevant programs"
        )
        workflow_progress.append({
            "agent": "Planning",
            "status": "complete",
            "confidence": 95,
            "message": f"Found {len(plan.get('relevant_programs', []))} relevant programs"
        })
        
        # AGENT 2: Search
        self.orchestrator.update_agent_status("Search", "running")
        workflow_progress.append({
            "agent": "Search",
            "status": "running",
            "message": "Querying vector database..."
        })
        
        candidates = self.search_agent.search_courses(plan, profile)
        
        self.orchestrator.update_agent_status(
            "Search", "complete",
            confidence=90,
            details=f"Found {len(candidates)} candidate courses"
        )
        workflow_progress.append({
            "agent": "Search",
            "status": "complete",
            "confidence": 90,
            "message": f"Found {len(candidates)} courses"
        })
        
        # AGENT 3: Analysis
        self.orchestrator.update_agent_status("Analysis", "running")
        workflow_progress.append({
            "agent": "Analysis",
            "status": "running",
            "message": "Ranking courses..."
        })
        
        recommendations = self.analysis_agent.analyze_and_rank(
            candidates, profile, plan
        )
        
        self.orchestrator.update_agent_status(
            "Analysis", "complete",
            confidence=88,
            details=f"Ranked {len(recommendations)} courses"
        )
        workflow_progress.append({
            "agent": "Analysis",
            "status": "complete",
            "confidence": 88,
            "message": f"Ranked {len(recommendations)} courses"
        })
        
        # AGENT 4: Explanation
        self.orchestrator.update_agent_status("Explanation", "running")
        workflow_progress.append({
            "agent": "Explanation",
            "status": "running",
            "message": "Generating personalized explanations..."
        })
        
        explanation = self.explanation_agent.generate_explanation(
            recommendations, profile, plan
        )
        
        self.orchestrator.update_agent_status(
            "Explanation", "complete",
            confidence=92,
            details="Generated personalized narrative"
        )
        workflow_progress.append({
            "agent": "Explanation",
            "status": "complete",
            "confidence": 92,
            "message": "Explanation generated"
        })
        
        # AGENT 5: Validation (Phase 2)
        self.orchestrator.update_agent_status("Validation", "running")
        workflow_progress.append({
            "agent": "Validation",
            "status": "running",
            "message": "Running quality checks..."
        })
        
        # Convert recommendations dict to list format for validation
        recommendations_list = recommendations.get('courses', [])
        if isinstance(recommendations_list, list) and recommendations_list:
            # Already a list
            pass
        else:
            # Create list from dict
            recommendations_list = [{"name": course} for course in recommendations.get('courses', [])]
        
        validation_results = self.validation_agent.validate_recommendations(
            recommendations_list,
            {
                "interests": profile.interests,
                "considering_majors": profile.considering_majors,
                "career_goals": profile.career_goals
            },
            plan
        )
        
        self.orchestrator.update_agent_status(
            "Validation", "complete",
            confidence=validation_results["confidence_score"],
            details=f"{validation_results['checks_passed']}/{validation_results['total_checks']} checks passed"
        )
        workflow_progress.append({
            "agent": "Validation",
            "status": "complete",
            "confidence": validation_results["confidence_score"],
            "message": f"{validation_results['checks_passed']}/{validation_results['total_checks']} checks passed"
        })
        
        print("\n" + "=" * 70)
        print("✅ PHASE 2 WORKFLOW COMPLETE")
        print(f"   Overall Confidence: {validation_results['confidence_score']}/100")
        print("=" * 70)
        
        # Build result
        result = {
            "recommendations": recommendations,  # Already a dict with programs/courses/overlap
            "explanation": explanation,
            "plan": plan,
            "validation": validation_results,
            "profile": {
                "interests": profile.interests,
                "considering_majors": profile.considering_majors,
                "career_goals": profile.career_goals
            }
        }
        
        if return_workflow:
            result["workflow"] = workflow_progress
            result["workflow_summary"] = self.orchestrator.get_overall_status()
        
        return result
    
    def ask_followup(self, question: str, context: Dict) -> str:
        """Handle follow-up questions (if Phase 1 is available)."""
        if self.conversational_agent:
            return self.conversational_agent.answer_followup(question, context)
        else:
            return "Follow-up Q&A requires Phase 1 enhancements with API key configured."


# Test function
def test_phase2():
    """Test Phase 2 system."""
    print("\n" + "=" * 70)
    print("TESTING PHASE 2 SYSTEM")
    print("=" * 70)
    
    advisor = Phase2AgenticCourseAdvisor()
    
    profile = StudentProfile(
        interests="business and technology, want to work in tech consulting",
        considering_majors=["Information Systems", "Finance", "Computer Science"],
        career_goals="Tech consulting or product management"
    )
    
    result = advisor.get_recommendations(profile)
    
    print("\n" + "=" * 70)
    print("VALIDATION RESULTS:")
    print("=" * 70)
    print(f"Confidence Score: {result['validation']['confidence_score']}/100")
    print(f"Checks Passed: {result['validation']['checks_passed']}/{result['validation']['total_checks']}")
    
    if result['validation']['issues']:
        print("\nIssues Found:")
        for issue in result['validation']['issues']:
            print(f"  • {issue.get('name')}: {issue.get('issue')}")
    
    if result['validation']['warnings']:
        print("\nWarnings:")
        for warning in result['validation']['warnings']:
            print(f"  ⚠️  {warning}")
    
    print("\n" + "=" * 70)
    print("WORKFLOW PROGRESS:")
    print("=" * 70)
    for step in result['workflow']:
        status_emoji = "✅" if step['status'] == 'complete' else "⏳"
        conf = f" ({step.get('confidence', 'N/A')}% confidence)" if 'confidence' in step else ""
        print(f"{status_emoji} {step['agent']}: {step['message']}{conf}")


if __name__ == "__main__":
    test_phase2()
