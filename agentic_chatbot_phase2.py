"""
Phase 2 Enhanced: Agentic Advisor with Validation & Orchestration
"""

import json
from typing import List, Dict, Optional
import sys

# Import Phase 1 enhanced version
try:
    from agentic_chatbot_enhanced import (
        EnhancedPlanningAgent, SearchAgent, AnalysisAgent,
        EnhancedExplanationAgent, ConversationalAgent, StudentProfile
    )
    PHASE1_AVAILABLE = True
except ImportError:
    # Fallback to basic version
    from agentic_chatbot import (
        PlanningAgent as EnhancedPlanningAgent,
        SearchAgent, AnalysisAgent, StudentProfile
    )
    PHASE1_AVAILABLE = False
    print("⚠️  Phase 1 enhancements not available, using basic agents")

# Import Phase 2 components
from validation_agent import ValidationAgent, AgentOrchestrator


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
            # Use basic explanation for Phase 1 features
            from agentic_chatbot import ExplanationAgent
            self.explanation_agent = ExplanationAgent()
            self.conversational_agent = None
            print("   ✓ Basic agents loaded")
        
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
            candidates, plan, profile
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
        
        validation_results = self.validation_agent.validate_recommendations(
            recommendations,
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
            "recommendations": recommendations[:5],
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
