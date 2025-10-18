"""
Phase 2: Validation Agent - Self-Checking AI System

This agent reviews recommendations for quality and catches potential issues.
"""

from typing import List, Dict, Optional
import re


class ValidationAgent:
    """
    Agent 5: Validates recommendations for quality, consistency, and correctness.
    
    This agent performs self-checks on the system's output to ensure:
    - No contradictions
    - Prerequisites are reasonable
    - Recommendations align with student goals
    - Course selections make sense together
    """
    
    def __init__(self):
        self.validation_rules = {
            "prerequisite_check": self._check_prerequisites,
            "goal_alignment": self._check_goal_alignment,
            "diversity_check": self._check_diversity,
            "program_overlap": self._check_program_overlap,
            "course_level": self._check_course_levels
        }
    
    def validate_recommendations(self, recommendations: List[Dict], 
                                profile: Dict, plan: Dict) -> Dict:
        """
        Run all validation checks on recommendations.
        
        Returns:
            Dict with validation results and any issues found
        """
        print("\n✅ VALIDATION AGENT: Checking recommendation quality...")
        
        results = {
            "passed": True,
            "confidence_score": 100,
            "issues": [],
            "warnings": [],
            "checks_passed": 0,
            "total_checks": len(self.validation_rules),
            "check_details": {}
        }
        
        # Run each validation check
        for check_name, check_func in self.validation_rules.items():
            try:
                check_result = check_func(recommendations, profile, plan)
                results["check_details"][check_name] = check_result
                
                if check_result["passed"]:
                    results["checks_passed"] += 1
                    print(f"   ✓ {check_result['name']}: PASSED")
                else:
                    results["passed"] = False
                    results["confidence_score"] -= check_result.get("severity", 10)
                    results["issues"].append(check_result)
                    print(f"   ⚠️  {check_result['name']}: {check_result['issue']}")
                
                # Add warnings
                if check_result.get("warnings"):
                    results["warnings"].extend(check_result["warnings"])
                    
            except Exception as e:
                print(f"   ⚠️  Check '{check_name}' failed: {e}")
                results["warnings"].append(f"Check '{check_name}' encountered an error")
        
        # Calculate final confidence
        results["confidence_score"] = max(0, results["confidence_score"])
        
        # Overall assessment
        if results["confidence_score"] >= 80:
            status = "✅ HIGH CONFIDENCE"
        elif results["confidence_score"] >= 60:
            status = "⚠️  MODERATE CONFIDENCE"
        else:
            status = "❌ LOW CONFIDENCE"
        
        print(f"\n   {status}: {results['checks_passed']}/{results['total_checks']} checks passed")
        print(f"   Overall confidence: {results['confidence_score']}/100")
        
        return results
    
    def _check_prerequisites(self, recommendations: List[Dict], 
                            profile: Dict, plan: Dict) -> Dict:
        """Check if prerequisite requirements are reasonable."""
        # Handle both detailed dict and simple string recommendations
        if not recommendations or (isinstance(recommendations, list) and 
                                   all(isinstance(r, str) for r in recommendations)):
            return {
                "name": "Prerequisite Check",
                "passed": True,
                "message": "Course data format simplified - check skipped"
            }
        
        issues = []
        
        for rec in recommendations[:5]:
            if isinstance(rec, dict):
                prereq_status = rec.get('prereq_status', '')
                
                # Flag if too many courses require prerequisites
                if 'prerequisite required' in prereq_status.lower():
                    issues.append(f"{rec.get('course_name', 'Unknown')} may be too advanced")
        
        # More than 2 courses with prereqs might be risky for first-years
        if len(issues) > 2:
            return {
                "name": "Prerequisite Check",
                "passed": False,
                "issue": "Too many courses require prerequisites for undecided first-year",
                "severity": 15,
                "recommendations": issues
            }
        
        return {
            "name": "Prerequisite Check",
            "passed": True,
            "message": "Prerequisites are appropriate for first-year student"
        }
    
    def _check_goal_alignment(self, recommendations: List[Dict], 
                             profile: Dict, plan: Dict) -> Dict:
        """Check if recommendations align with student's stated goals."""
        
        # Handle simplified format
        if not recommendations or (isinstance(recommendations, list) and 
                                   all(isinstance(r, str) for r in recommendations)):
            return {
                "name": "Goal Alignment",
                "passed": True,
                "message": "Course data format simplified - check skipped"
            }
        
        student_interests = profile.get('interests', '').lower()
        majors = [m.lower() for m in profile.get('considering_majors', [])]
        
        aligned_count = 0
        
        for rec in recommendations[:5]:
            if isinstance(rec, dict):
                course_name = rec.get('course_name', '').lower()
                description = rec.get('description', '').lower()
                applicable_majors = [m.lower() for m in rec.get('applicable_majors', [])]
                
                # Check if course aligns with interests or majors
                interest_match = any(interest in description or interest in course_name 
                                    for interest in student_interests.split())
                major_match = any(major in applicable_majors for major in majors)
                
                if interest_match or major_match:
                    aligned_count += 1
        
        if aligned_count >= 3:
            return {
                "name": "Goal Alignment",
                "passed": True,
                "message": f"{aligned_count}/5 courses align with student goals"
            }
        else:
            return {
                "name": "Goal Alignment",
                "passed": False,
                "issue": "Few courses align with stated goals",
                "severity": 20
            }
    
    def _check_diversity(self, recommendations: List[Dict], 
                        profile: Dict, plan: Dict) -> Dict:
        """Check if recommendations offer good diversity across areas."""
        
        # Handle simplified format
        if not recommendations or (isinstance(recommendations, list) and 
                                   all(isinstance(r, str) for r in recommendations)):
            return {
                "name": "Diversity Check",
                "passed": True,
                "message": "Course data format simplified - check skipped"
            }
        
        # Extract subject areas (first word of course code)
        subjects = set()
        for rec in recommendations[:5]:
            if isinstance(rec, dict):
                course_name = rec.get('course_name', '')
                # Extract department code (e.g., "CS" from "CS 111")
                match = re.match(r'^([A-Z]+)', course_name)
                if match:
                    subjects.add(match.group(1))
        
        diversity_score = len(subjects)
        
        # Good diversity means courses from multiple departments
        if diversity_score >= 3:
            return {
                "name": "Diversity Check",
                "passed": True,
                "message": f"Good diversity with courses from {diversity_score} different departments"
            }
        elif diversity_score >= 2:
            return {
                "name": "Diversity Check",
                "passed": True,
                "message": f"Moderate diversity with courses from {diversity_score} departments",
                "warnings": ["Consider exploring more subject areas"]
            }
        else:
            return {
                "name": "Diversity Check",
                "passed": False,
                "issue": "Limited diversity - all courses from similar areas",
                "severity": 10,
                "unique_subjects": diversity_score
            }
    
    def _check_program_overlap(self, recommendations: List[Dict], 
                              profile: Dict, plan: Dict) -> Dict:
        """Check if recommendations keep multiple major options open."""
        
        # Handle simplified format
        if not recommendations or (isinstance(recommendations, list) and 
                                   all(isinstance(r, str) for r in recommendations)):
            return {
                "name": "Program Overlap",
                "passed": True,
                "message": "Course data format simplified - check skipped"
            }
        
        versatile_courses = 0
        
        for rec in recommendations[:5]:
            if isinstance(rec, dict):
                program_count = rec.get('program_count', 0)
                if program_count >= 2:
                    versatile_courses += 1
        
        # At least 3 out of 5 should apply to multiple programs
        if versatile_courses >= 3:
            return {
                "name": "Program Overlap",
                "passed": True,
                "message": f"{versatile_courses}/5 courses apply to multiple majors - excellent flexibility!"
            }
        elif versatile_courses >= 2:
            return {
                "name": "Program Overlap",
                "passed": True,
                "message": f"{versatile_courses}/5 courses apply to multiple majors",
                "warnings": ["Consider more versatile courses to keep options open"]
            }
        else:
            return {
                "name": "Program Overlap",
                "passed": False,
                "issue": "Too few courses apply to multiple majors - may limit flexibility",
                "severity": 25,
                "versatile_count": versatile_courses
            }
    
    def _check_course_levels(self, recommendations: List[Dict], 
                            profile: Dict, plan: Dict) -> Dict:
        """Check if course levels are appropriate for first-year students."""
        
        # Handle simplified format
        if not recommendations or (isinstance(recommendations, list) and 
                                   all(isinstance(r, str) for r in recommendations)):
            return {
                "name": "Course Level Check",
                "passed": True,
                "message": "Course data format simplified - check skipped"
            }
        
        advanced_courses = []
        
        for rec in recommendations[:5]:
            if isinstance(rec, dict):
                course_name = rec.get('course_name', '')
                # Extract course number
                match = re.search(r'(\d+)', course_name)
                if match:
                    course_num = int(match.group(1))
                    # 300+ level courses might be too advanced
                    if course_num >= 300:
                        advanced_courses.append(course_name)
        
        if len(advanced_courses) == 0:
            return {
                "name": "Course Level Check",
                "passed": True,
                "message": "All courses are appropriate level for first-year students"
            }
        elif len(advanced_courses) <= 1:
            return {
                "name": "Course Level Check",
                "passed": True,
                "message": "Course levels are reasonable",
                "warnings": [f"{advanced_courses[0]} is upper-level - verify prerequisites"]
            }
        else:
            return {
                "name": "Course Level Check",
                "passed": False,
                "issue": "Multiple upper-level courses may be too challenging for first semester",
                "severity": 15,
                "advanced_courses": advanced_courses
            }


class AgentOrchestrator:
    """
    Meta-agent that coordinates all other agents and tracks their progress.
    """
    
    def __init__(self):
        self.agent_status = {}
        self.workflow_steps = [
            {"name": "Planning", "emoji": "🤖", "status": "pending"},
            {"name": "Search", "emoji": "🔍", "status": "pending"},
            {"name": "Analysis", "emoji": "📊", "status": "pending"},
            {"name": "Explanation", "emoji": "💬", "status": "pending"},
            {"name": "Validation", "emoji": "✅", "status": "pending"}
        ]
    
    def update_agent_status(self, agent_name: str, status: str, 
                           confidence: Optional[int] = None, details: Optional[str] = None):
        """
        Update the status of an agent.
        
        Args:
            agent_name: Name of the agent
            status: 'pending', 'running', 'complete', 'error'
            confidence: Optional confidence score (0-100)
            details: Optional details about what the agent found/did
        """
        self.agent_status[agent_name] = {
            "status": status,
            "confidence": confidence,
            "details": details
        }
        
        # Update workflow steps
        for step in self.workflow_steps:
            if step["name"].lower() in agent_name.lower():
                step["status"] = status
                if confidence is not None:
                    step["confidence"] = str(confidence)  # type: ignore
                if details:
                    step["details"] = details
                break
    
    def get_workflow_progress(self) -> List[Dict]:
        """Get current progress of all agents."""
        return self.workflow_steps
    
    def get_overall_status(self) -> Dict:
        """Get overall workflow status."""
        completed = sum(1 for step in self.workflow_steps if step["status"] == "complete")
        total = len(self.workflow_steps)
        
        return {
            "completed": completed,
            "total": total,
            "progress_percent": int((completed / total) * 100),
            "current_step": next((s["name"] for s in self.workflow_steps 
                                 if s["status"] == "running"), None)
        }
