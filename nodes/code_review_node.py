# ==================== CODE REVIEW NODE ====================
# File: nodes/code_review_node.py

from datetime import datetime
from typing import List, Dict, Any
from langgraph.types import interrupt, Command
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def code_review_dynamic(state: SDLCState) -> SDLCState:
    """
    Code Review using DYNAMIC INTERRUPTS (Official Pattern)
    Allows user to choose: human review, AI review, or auto-approve
    """
    
    print("\n👨‍💻 Code Review - Dynamic Interrupt Pattern")
    print("🎯 Using interrupt() function inside node (official approach)")
    
    code_files = state.get("code", {})
    if not code_files:
        print("⚠️ No code files found - auto-approving")
        return {
            **state,
            "approval_status": "approved",
            "current_stage": "code_review_complete",
            "timestamp": datetime.now().isoformat()
        }
    
    # ⭐ DYNAMIC INTERRUPT - This pauses execution and waits for user input
    user_choice = interrupt({
        "type": "code_review_choice",
        "question": "How would you like to review the generated code?",
        "options": {
            "human": "👤 I'll review it myself (Human Code Review)",
            "ai": "🤖 Let AI review it automatically (AI Code Review)",
            "auto": "⚡ Auto-approve and continue (Skip Review)"
        },
        "context": {
            "code_files_count": len(code_files),
            "current_iteration": state.get("iteration_count", 0),
            "project_id": state.get("project_id", "unknown")
        },
        "code_preview": {
            "files": list(code_files.keys())[:5],  # Show first 5 filenames
            "total_files": len(code_files),
            "file_sizes": {filename: len(content) for filename, content in list(code_files.items())[:3]}
        }
    })
    
    print(f"✅ User selected: {user_choice}")
    
    # Process the user's choice
    if user_choice == "human":
        print("👤 Processing human code review...")
        review_result = _handle_human_code_review_dynamic(state)
    elif user_choice == "ai":
        print("🤖 Processing AI code review...")
        review_result = _handle_ai_code_review_dynamic(state)
    elif user_choice == "auto":
        print("⚡ Auto-approving...")
        review_result = _handle_auto_approve_code_dynamic(state)
    else:
        print(f"⚠️ Unknown choice '{user_choice}' - defaulting to AI review")
        review_result = _handle_ai_code_review_dynamic(state)
    
    # Save review to history
    review_history = state.get("review_history", [])
    review_record = {
        "iteration": state.get("iteration_count", 0),
        "stage": "code_review",
        "reviewer": review_result.get("reviewer", "Unknown"),
        "status": review_result.get("status", "unknown"),
        "feedback": review_result.get("feedback", ""),
        "suggestions": review_result.get("suggestions", []),
        "timestamp": review_result.get("timestamp", datetime.now().isoformat()),
        "code_quality_score": review_result.get("code_quality_score"),
        "maintainability_score": review_result.get("maintainability_score"),
        "review_method": user_choice
    }
    review_history.append(review_record)
    
    # Update state with review results
    updated_state = {
        **state,
        "review_feedback": review_result,
        "approval_status": review_result.get("status", "approved"),
        "current_stage": "code_review_complete",
        "timestamp": datetime.now().isoformat(),
        "review_history": review_history
    }
    
    print(f"✅ Code review completed - Status: {review_result.get('status', 'approved')}")
    print(f"👤 Reviewer: {review_result.get('reviewer', 'Unknown')}")
    
    return updated_state

def _handle_human_code_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """
    Handle human code review using dynamic interrupts
    Can use MULTIPLE interrupts for detailed review process
    """
    
    code_files = state.get("code", {})
    
    # Prepare code files summary for review
    code_summary = {
        "total_files": len(code_files),
        "files": []
    }
    
    # Extract key information about each file
    for filename, content in code_files.items():
        file_info = {
            "filename": filename,
            "lines": len(content.split('\n')) if content else 0,
            "size_chars": len(content),
            "preview": content[:200] + "..." if len(content) > 200 else content
        }
        code_summary["files"].append(file_info)
    
    # ⭐ FIRST INTERRUPT: Show code files and get overall decision
    overall_decision = interrupt({
        "type": "human_code_review_decision",
        "prompt": "Please review the generated code files:",
        "code_files": code_summary,
        "question": "What's your overall decision about this generated code?",
        "options": {
            "approve": "✅ Approve - code looks good, ready for next phase",
            "request_changes": "⚠️ Request changes - code needs improvements",
            "reject": "❌ Reject - significant code issues found"
        }
    })
    
    feedback = ""
    suggestions = []
    
    # ⭐ SECOND INTERRUPT: Get detailed feedback if not approved
    if overall_decision != "approve":
        detailed_feedback = interrupt({
            "type": "human_code_review_feedback",
            "prompt": f"You chose to '{overall_decision}'. Please provide detailed code feedback:",
            "question": "What specific changes or improvements are needed in the code?",
                            "help_text": "Be specific about code quality, structure, or functionality issues."
        })
        
        feedback = detailed_feedback.get("feedback", "") if isinstance(detailed_feedback, dict) else str(detailed_feedback)
        
        # ⭐ THIRD INTERRUPT: Get specific suggestions (optional)
        if feedback:
            suggestion_input = interrupt({
                "type": "human_code_review_suggestions",
                "prompt": "Any specific code improvement suggestions?",
                "question": "Provide actionable code suggestions (optional):",
                "current_feedback": feedback,
                "help_text": "Press Enter to skip, or provide specific code improvements"
            })
            
            if suggestion_input and str(suggestion_input).strip():
                suggestions = [str(suggestion_input).strip()]
    
    return {
        "status": overall_decision,
        "feedback": feedback or f"Human code review completed with decision: {overall_decision}",
        "reviewer": "Human",
        "timestamp": datetime.now().isoformat(),
        "approval_status": overall_decision,
        "suggestions": suggestions,
        "approved_files": list(code_files.keys()) if overall_decision == "approve" else [],
        "rejected_files": list(code_files.keys()) if overall_decision == "reject" else [],
        "code_quality_score": 8,
        "maintainability_score": 8,
        "review_method": "human_dynamic"
    }

def _handle_ai_code_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle AI code review - automated technical code review"""
    
    llm_utils = LLMUtils()
    code_files = state.get("code", {})
    design_docs = state.get("design_docs", {})
    user_stories = state.get("user_stories", [])
    
    system_prompt = """
    You are an experienced Senior Software Engineer and Code Reviewer conducting a thorough code review.
    
    Evaluate the code based on:
    - Code quality and best practices
    - Performance implications
    - Maintainability and readability
    - Alignment with design specifications
    - Implementation of user story requirements
    - Error handling and edge cases
    - Code structure and organization
    
    Provide your review as JSON with this structure:
    {
        "status": "approve" | "request_changes" | "reject",
        "feedback": "Overall code review summary",
        "suggestions": ["List of specific code improvement suggestions"],
        "approved_files": ["List of approved file names"],
        "rejected_files": ["List of files needing work"],
        "code_quality_score": 1-10,
        "maintainability_score": 1-10,
        "overall_assessment": "Detailed technical assessment",
        "key_strengths": ["Main strengths of the code"],
        "key_concerns": ["Main code issues or areas for improvement"],
        "performance_issues": ["Performance optimization suggestions"]
    }
    
    Return ONLY the JSON object, no additional text.
    """
    
    # Format code files for review (limit content to manage tokens)
    code_review_text = "CODE FILES FOR REVIEW:\n\n"
    for filename, content in code_files.items():
        # Limit content size for token management
        content_preview = content[:1000] + "\n... [truncated]" if len(content) > 1000 else content
        code_review_text += f"=== {filename} ===\n{content_preview}\n\n"
    
    # Add design context
    design_context = f"DESIGN SPECIFICATIONS:\n{design_docs.get('summary', 'No design summary available')}\n\n"
    user_stories_context = f"USER STORIES COUNT: {len(user_stories)}\n"
    
    user_prompt = f"""
    Review this generated code against the design specifications and user stories:
    
    {design_context}
    {user_stories_context}
    
    {code_review_text}
    
    Provide a thorough code review focusing on quality, security, and implementation correctness.
    """
    
    try:
        review_result = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        # Ensure required fields
        review_result.update({
            "reviewer": "AI",
            "timestamp": datetime.now().isoformat(),
            "approval_status": review_result.get("status", "approve"),
            "review_method": "ai_dynamic"
        })
        
        print("🤖 AI Senior Engineer code review completed")
        return review_result
        
    except Exception as e:
        print(f"❌ AI code review failed: {e}")
        return _handle_auto_approve_code_dynamic(state)

def _handle_auto_approve_code_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle auto-approve code files"""
    
    code_files = state.get("code", {})
    
    return {
        "status": "approve",
        "feedback": "Auto-approved by user choice - code review skipped",
        "reviewer": "Auto",
        "timestamp": datetime.now().isoformat(),
        "approval_status": "approve",
        "suggestions": [],
        "approved_files": list(code_files.keys()),
        "rejected_files": [],
        "code_quality_score": 7,
        "maintainability_score": 7,
        "overall_assessment": "Automatically approved without review",
        "review_method": "auto_dynamic"
    }

def route_after_code_review_dynamic(state: SDLCState) -> str:
    """Route after code review based on approval status and iteration limits"""
    
    approval_status = state.get("approval_status", "")
    iteration_count = state.get("iteration_count", 0)
    
    if approval_status == "approve":
        print("✅ Code approved - proceeding to next phase")
        return "security_review"  # Next phase
    elif iteration_count >= settings.MAX_ITERATIONS:
        print(f"⚠️ Maximum iterations ({settings.MAX_ITERATIONS}) reached - proceeding to next phase")
        return "security_review"
    else:
        print(f"⚠️ Code needs revision - iteration {iteration_count + 1}/{settings.MAX_ITERATIONS}")
        return "fix_code_after_review"