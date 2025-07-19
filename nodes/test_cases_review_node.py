# ==================== TEST CASES REVIEW NODE ====================
# File: nodes/test_cases_review_node.py

from datetime import datetime
from typing import List, Dict, Any
from langgraph.types import interrupt, Command
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def test_cases_review_dynamic(state: SDLCState) -> SDLCState:
    """
    Test Cases Review using DYNAMIC INTERRUPTS (Official Pattern)
    Allows user to choose: human review, AI review, or auto-approve
    """
    
    print("\n🧪 Test Cases Review - Dynamic Interrupt Pattern")
    print("🎯 Reviewing generated test cases for quality and coverage")
    
    test_cases = state.get("test_cases", {})
    if not test_cases:
        print("⚠️ No test cases found - auto-approving")
        return {
            **state,
            "approval_status": "approved",
            "current_stage": "test_cases_review_complete",
            "timestamp": datetime.now().isoformat()
        }
    
    # ⭐ DYNAMIC INTERRUPT - Test cases review choice
    user_choice = interrupt({
        "type": "test_cases_review_choice",
        "question": "How would you like to review the generated test cases?",
        "options": {
            "human": "👤 I'll review test cases myself (Human Test Review)",
            "ai": "🤖 Let AI review test quality (AI Test Review)",
            "auto": "⚡ Auto-approve and continue (Skip Test Review)"
        },
        "context": {
            "test_files_count": len(test_cases),
            "current_iteration": state.get("iteration_count", 0),
            "project_id": state.get("project_id", "unknown")
        },
        "test_preview": {
            "files": list(test_cases.keys()),
            "total_files": len(test_cases),
            "test_stats": _analyze_test_statistics(test_cases),
            "coverage_areas": _identify_test_coverage_areas(test_cases)
        }
    })
    
    print(f"✅ User selected: {user_choice}")
    
    # Process the user's choice
    if user_choice == "human":
        print("👤 Processing human test cases review...")
        review_result = _handle_human_test_review_dynamic(state)
    elif user_choice == "ai":
        print("🤖 Processing AI test cases review...")
        review_result = _handle_ai_test_review_dynamic(state)
    elif user_choice == "auto":
        print("⚡ Auto-approving test cases...")
        review_result = _handle_auto_approve_test_dynamic(state)
    else:
        print(f"⚠️ Unknown choice '{user_choice}' - defaulting to AI test review")
        review_result = _handle_ai_test_review_dynamic(state)
    
    # Save review to history
    review_history = state.get("review_history", [])
    review_record = {
        "iteration": state.get("iteration_count", 0),
        "stage": "test_cases_review",
        "reviewer": review_result.get("reviewer", "Unknown"),
        "status": review_result.get("status", "unknown"),
        "feedback": review_result.get("feedback", ""),
        "suggestions": review_result.get("suggestions", []),
        "timestamp": review_result.get("timestamp", datetime.now().isoformat()),
        "test_quality_score": review_result.get("test_quality_score"),
        "coverage_score": review_result.get("coverage_score"),
        "completeness_score": review_result.get("completeness_score"),
        "review_method": user_choice
    }
    review_history.append(review_record)
    
    # Update state with review results
    updated_state = {
        **state,
        "review_feedback": review_result,
        "approval_status": review_result.get("status", "approved"),
        "current_stage": "test_cases_review_complete",
        "timestamp": datetime.now().isoformat(),
        "review_history": review_history
    }
    
    print(f"✅ Test cases review completed - Status: {review_result.get('status', 'approved')}")
    print(f"👤 Reviewer: {review_result.get('reviewer', 'Unknown')}")
    print(f"🎯 Test Quality Score: {review_result.get('test_quality_score', 'N/A')}/10")
    
    return updated_state

def _analyze_test_statistics(test_cases: Dict[str, str]) -> Dict[str, Any]:
    """Analyze statistics about the generated test cases"""
    
    stats = {
        "total_test_functions": 0,
        "test_classes": 0,
        "fixtures": 0,
        "parametrized_tests": 0,
        "mock_usage": 0,
        "assertion_types": [],
        "test_categories": []
    }
    
    for filename, content in test_cases.items():
        lines = content.split('\n')
        
        for line in lines:
            stripped = line.strip()
            
            # Count test functions
            if stripped.startswith('def test_'):
                stats["total_test_functions"] += 1
            
            # Count test classes
            elif stripped.startswith('class Test'):
                stats["test_classes"] += 1
            
            # Count fixtures
            elif '@pytest.fixture' in stripped:
                stats["fixtures"] += 1
            
            # Count parametrized tests
            elif '@pytest.mark.parametrize' in stripped:
                stats["parametrized_tests"] += 1
            
            # Count mock usage
            elif 'Mock' in stripped or 'mock' in stripped:
                stats["mock_usage"] += 1
            
            # Identify assertion types
            if 'assert ' in stripped:
                if 'assert_' not in stripped:  # Basic assert
                    if 'basic_assert' not in stats["assertion_types"]:
                        stats["assertion_types"].append('basic_assert')
                else:
                    # Custom assertion methods
                    if 'custom_assert' not in stats["assertion_types"]:
                        stats["assertion_types"].append('custom_assert')
            
            # Identify test categories
            if 'pytest.raises' in stripped:
                if 'exception_testing' not in stats["test_categories"]:
                    stats["test_categories"].append('exception_testing')
            
            if 'integration' in stripped.lower():
                if 'integration_tests' not in stats["test_categories"]:
                    stats["test_categories"].append('integration_tests')
            
            if 'user_story' in stripped.lower() or 'acceptance' in stripped.lower():
                if 'user_story_tests' not in stats["test_categories"]:
                    stats["test_categories"].append('user_story_tests')
    
    return stats

def _identify_test_coverage_areas(test_cases: Dict[str, str]) -> List[str]:
    """Identify what areas are covered by the test cases"""
    
    coverage_areas = []
    
    for filename, content in test_cases.items():
        content_lower = content.lower()
        
        # Check for different types of test coverage
        if 'def test_' in content_lower:
            coverage_areas.append("Unit Testing")
        
        if 'class test' in content_lower:
            coverage_areas.append("Class Testing")
        
        if 'integration' in content_lower:
            coverage_areas.append("Integration Testing")
        
        if 'user_story' in content_lower or 'acceptance' in content_lower:
            coverage_areas.append("User Story Testing")
        
        if 'error' in content_lower or 'exception' in content_lower:
            coverage_areas.append("Error Handling Testing")
        
        if 'parametrize' in content_lower:
            coverage_areas.append("Parametrized Testing")
        
        if 'mock' in content_lower:
            coverage_areas.append("Mocking and Isolation")
        
        if 'fixture' in content_lower:
            coverage_areas.append("Test Fixtures")
        
        if 'performance' in content_lower or 'load' in content_lower:
            coverage_areas.append("Performance Testing")
        
        if 'security' in content_lower:
            coverage_areas.append("Security Testing")
    
    return list(set(coverage_areas)) if coverage_areas else ["Basic Testing"]

def _handle_human_test_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """
    Handle human test cases review using dynamic interrupts
    Can use MULTIPLE interrupts for detailed test review process
    """
    
    test_cases = state.get("test_cases", {})
    
    # Prepare test cases summary for review
    test_summary = {
        "total_files": len(test_cases),
        "statistics": _analyze_test_statistics(test_cases),
        "coverage_areas": _identify_test_coverage_areas(test_cases),
        "files": []
    }
    
    # Extract key information about each test file
    for filename, content in test_cases.items():
        file_info = {
            "filename": filename,
            "lines": len(content.split('\n')) if content else 0,
            "size_chars": len(content),
            "test_functions": content.count('def test_'),
            "test_classes": content.count('class Test'),
            "preview": content[:400] + "..." if len(content) > 400 else content
        }
        test_summary["files"].append(file_info)
    
    # ⭐ FIRST INTERRUPT: Show test analysis and get overall decision
    overall_decision = interrupt({
        "type": "human_test_review_decision",
        "prompt": "Please review the generated test cases for quality and coverage:",
        "test_analysis": test_summary,
        "question": "What's your overall assessment of these test cases?",
        "options": {
            "approve": "✅ Approve - test cases are comprehensive and well-structured",
            "request_changes": "⚠️ Request changes - test cases need improvements",
            "reject": "❌ Reject - test cases are insufficient or poorly structured"
        }
    })
    
    feedback = ""
    suggestions = []
    test_gaps = []
    
    # ⭐ SECOND INTERRUPT: Get detailed test feedback if not approved
    if overall_decision != "approve":
        detailed_feedback = interrupt({
            "type": "human_test_review_feedback",
            "prompt": f"You chose to '{overall_decision}'. Please provide detailed test feedback:",
            "question": "What specific improvements are needed in the test cases?",
            "help_text": "Be specific about test coverage gaps, quality issues, or missing test scenarios."
        })
        
        feedback = detailed_feedback.get("feedback", "") if isinstance(detailed_feedback, dict) else str(detailed_feedback)
        
        # ⭐ THIRD INTERRUPT: Get specific test improvement suggestions
        if feedback:
            improvement_suggestions = interrupt({
                "type": "human_test_improvement_suggestions",
                "prompt": "What specific test improvements or additional test cases are needed?",
                "question": "Provide actionable suggestions for improving the test suite:",
                "current_feedback": feedback,
                "help_text": "Suggest specific test cases, coverage areas, or testing approaches to add."
            })
            
            if improvement_suggestions and str(improvement_suggestions).strip():
                suggestions = [str(improvement_suggestions).strip()]
                
                # Extract test gaps for metrics
                suggestion_text = str(improvement_suggestions).lower()
                if 'coverage' in suggestion_text:
                    test_gaps.append("Test Coverage")
                if 'edge case' in suggestion_text:
                    test_gaps.append("Edge Cases")
                if 'integration' in suggestion_text:
                    test_gaps.append("Integration Tests")
                if 'error' in suggestion_text or 'exception' in suggestion_text:
                    test_gaps.append("Error Handling")
    
    # Calculate test quality scores
    quality_scores = _calculate_test_quality_scores(overall_decision, test_summary, test_gaps)
    
    return {
        "status": overall_decision,
        "feedback": feedback or f"Human test review completed with decision: {overall_decision}",
        "reviewer": "Human",
        "timestamp": datetime.now().isoformat(),
        "approval_status": overall_decision,
        "suggestions": suggestions,
        "test_quality_score": quality_scores["quality"],
        "coverage_score": quality_scores["coverage"],
        "completeness_score": quality_scores["completeness"],
        "test_gaps_identified": test_gaps,
        "approved_files": list(test_cases.keys()) if overall_decision == "approve" else [],
        "flagged_files": list(test_cases.keys()) if overall_decision in ["request_changes", "reject"] else [],
        "review_method": "human_dynamic"
    }

def _handle_ai_test_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle AI test cases review - automated test quality analysis"""
    
    llm_utils = LLMUtils()
    test_cases = state.get("test_cases", {})
    code_files = state.get("code", {})
    user_stories = state.get("user_stories", [])
    
    system_prompt = """
    You are a Senior QA Engineer and Test Automation Expert conducting a comprehensive review of test cases.
    
    Evaluate the test cases based on:
    - Test coverage completeness (do tests cover all functions/classes?)
    - Test quality and best practices
    - User story and acceptance criteria coverage
    - Edge case and error condition testing
    - Test structure and organization
    - Use of appropriate testing frameworks and patterns
    - Mock usage and test isolation
    - Test maintainability and readability
    - Performance and integration test coverage
    - Test data management and fixtures
    
    Provide your test review as JSON with this structure:
    {
        "status": "approve" | "request_changes" | "reject",
        "feedback": "Comprehensive test quality assessment summary",
        "suggestions": ["List of specific test improvement recommendations"],
        "test_quality_score": 1-10,
        "coverage_score": 1-10,
        "completeness_score": 1-10,
        "test_strengths": ["List of good testing practices found"],
        "test_gaps": ["List of missing test coverage areas"],
        "missing_test_scenarios": ["Specific test cases that should be added"],
        "code_coverage_assessment": "Assessment of how well tests cover the actual code",
        "user_story_coverage": "How well tests validate user story acceptance criteria",
        "overall_assessment": "Detailed test quality analysis summary"
    }
    
    Return ONLY the JSON object, no additional text.
    """
    
    # Format test cases for review
    test_review_text = "TEST CASES FOR REVIEW:\n\n"
    for filename, content in test_cases.items():
        test_review_text += f"=== {filename} ===\n{content}\n\n"
    
    # Add code context for coverage assessment
    code_context = "ORIGINAL CODE TO TEST:\n\n"
    for filename, content in code_files.items():
        # Limit content size for token management
        content_preview = content[:800] + "\n... [truncated]" if len(content) > 800 else content
        code_context += f"=== {filename} ===\n{content_preview}\n\n"
    
    # Add user story context
    user_stories_context = f"USER STORIES COUNT: {len(user_stories)}\n"
    if user_stories:
        user_stories_context += "USER STORIES SUMMARY:\n"
        for story in user_stories[:3]:  # First 3 stories for context
            user_stories_context += f"- {story.get('title', 'Untitled')}: {story.get('description', '')[:100]}...\n"
    
    user_prompt = f"""
    Review these test cases for quality, coverage, and completeness:
    
    {user_stories_context}
    
    {code_context}
    
    {test_review_text}
    
    Provide a thorough test quality review focusing on coverage completeness, testing best practices, and alignment with code functionality and user requirements.
    """
    
    try:
        review_result = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        # Ensure required fields and add metadata
        review_result.update({
            "reviewer": "AI",
            "timestamp": datetime.now().isoformat(),
            "approval_status": review_result.get("status", "approve"),
            "review_method": "ai_dynamic"
        })
        
        print("🤖 AI QA Expert test review completed")
        return review_result
        
    except Exception as e:
        print(f"❌ AI test review failed: {e}")
        return _handle_auto_approve_test_dynamic(state)

def _handle_auto_approve_test_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle auto-approve test cases"""
    
    test_cases = state.get("test_cases", {})
    test_stats = _analyze_test_statistics(test_cases)
    
    return {
        "status": "approve",
        "feedback": "Auto-approved by user choice - test review skipped",
        "reviewer": "Auto",
        "timestamp": datetime.now().isoformat(),
        "approval_status": "approve",
        "suggestions": [],
        "test_quality_score": 7,
        "coverage_score": 7,
        "completeness_score": 7,
        "test_gaps_identified": [],
        "approved_files": list(test_cases.keys()),
        "flagged_files": [],
        "overall_assessment": "Test cases automatically approved without review",
        "review_method": "auto_dynamic"
    }

def _calculate_test_quality_scores(decision: str, test_summary: Dict[str, Any], test_gaps: List[str]) -> Dict[str, int]:
    """Calculate test quality scores based on review decision and analysis"""
    
    base_scores = {
        "approve": {"quality": 8, "coverage": 8, "completeness": 8},
        "request_changes": {"quality": 6, "coverage": 5, "completeness": 6},
        "reject": {"quality": 3, "coverage": 3, "completeness": 3}
    }
    
    scores = base_scores.get(decision, {"quality": 6, "coverage": 6, "completeness": 6}).copy()
    
    # Adjust based on test statistics
    stats = test_summary.get("statistics", {})
    
    # Bonus for good test practices
    if stats.get("fixtures", 0) > 0:
        scores["quality"] += 1
    if stats.get("parametrized_tests", 0) > 0:
        scores["coverage"] += 1
    if stats.get("mock_usage", 0) > 0:
        scores["quality"] += 1
    if len(stats.get("test_categories", [])) > 3:
        scores["completeness"] += 1
    
    # Penalty for identified gaps
    gap_penalty = min(len(test_gaps), 3)
    scores["coverage"] = max(1, scores["coverage"] - gap_penalty)
    scores["completeness"] = max(1, scores["completeness"] - gap_penalty)
    
    # Ensure scores stay within 1-10 range
    for key in scores:
        scores[key] = max(1, min(10, scores[key]))
    
    return scores

def route_after_test_review_dynamic(state: SDLCState) -> str:
    """Route after test review based on approval status and iteration limits"""
    
    approval_status = state.get("approval_status", "")
    iteration_count = state.get("iteration_count", 0)
    
    if approval_status == "approve":
        print("✅ Test cases approved - proceeding to QA testing phase")
        return "deployment"  # Next phase: execute the tests
    elif iteration_count >= settings.MAX_ITERATIONS:
        print(f"⚠️ Maximum iterations ({settings.MAX_ITERATIONS}) reached - proceeding to QA testing")
        return "deployment"
    else:
        print(f"⚠️ Test cases need revision - iteration {iteration_count + 1}/{settings.MAX_ITERATIONS}")
        return "revise_test_cases"