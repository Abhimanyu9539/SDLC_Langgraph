from datetime import datetime
from typing import List, Dict, Any
from langgraph.types import interrupt, Command
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def design_review_dynamic(state: SDLCState) -> SDLCState:
    """
    Design Review using DYNAMIC INTERRUPTS (Official Pattern)
    Allows user to choose: human review, AI review, or auto-approve
    """
    
    print("\n👨‍💻 Design Review - Dynamic Interrupt Pattern")
    print("🎯 Using interrupt() function inside node (official approach)")
    
    design_docs = state.get("design_docs", {})
    if not design_docs:
        print("⚠️ No design documents found - auto-approving")
        return {
            **state,
            "approval_status": "approved",
            "current_stage": "design_review_complete",
            "timestamp": datetime.now().isoformat()
        }
    
    # ⭐ DYNAMIC INTERRUPT - This pauses execution and waits for user input
    user_choice = interrupt({
        "type": "design_review_choice",
        "question": "How would you like to review the design documents?",
        "options": {
            "human": "👤 I'll review them myself (Human Review)",
            "ai": "🤖 Let AI review them automatically (AI Review)",
            "auto": "⚡ Auto-approve and continue (Skip Review)"
        },
        "context": {
            "design_docs_available": bool(design_docs),
            "design_title": design_docs.get("title", "Technical Design Document"),
            "current_iteration": state.get("iteration_count", 0),
            "project_id": state.get("project_id", "unknown")
        },
        "design_preview": {
            "title": design_docs.get("title", "Technical Design Document"),
            "summary": design_docs.get("summary", "Design document summary")[:150] + "..." if len(design_docs.get("summary", "")) > 150 else design_docs.get("summary", ""),
            "sections": list(design_docs.keys()) if isinstance(design_docs, dict) else ["Design document available"]
        }
    })
    
    print(f"✅ User selected: {user_choice}")
    
    # Process the user's choice
    if user_choice == "human":
        print("👤 Processing human review...")
        review_result = _handle_human_design_review_dynamic(state)
    elif user_choice == "ai":
        print("🤖 Processing AI review...")
        review_result = _handle_ai_design_review_dynamic(state)
    elif user_choice == "auto":
        print("⚡ Auto-approving...")
        review_result = _handle_auto_approve_design_dynamic(state)
    else:
        print(f"⚠️ Unknown choice '{user_choice}' - defaulting to AI review")
        review_result = _handle_ai_design_review_dynamic(state)
    
    # Save review to history
    review_history = state.get("review_history", [])
    review_record = {
        "iteration": state.get("iteration_count", 0),
        "stage": "design_review",
        "reviewer": review_result.get("reviewer", "Unknown"),
        "status": review_result.get("status", "unknown"),
        "feedback": review_result.get("feedback", ""),
        "suggestions": review_result.get("suggestions", []),
        "timestamp": review_result.get("timestamp", datetime.now().isoformat()),
        "technical_score": review_result.get("technical_score"),
        "completeness_score": review_result.get("completeness_score"),
        "review_method": user_choice
    }
    review_history.append(review_record)
    
    # Update state with review results
    updated_state = {
        **state,
        "review_feedback": review_result,
        "approval_status": review_result.get("status", "approved"),
        "current_stage": "design_review_complete",
        "timestamp": datetime.now().isoformat(),
        "review_history": review_history
    }
    
    print(f"✅ Design review completed - Status: {review_result.get('status', 'approved')}")
    print(f"👤 Reviewer: {review_result.get('reviewer', 'Unknown')}")
    
    return updated_state

def _handle_human_design_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """
    Handle human design review using dynamic interrupts
    Can use MULTIPLE interrupts for detailed review process
    """
    
    design_docs = state.get("design_docs", {})
    
    # Prepare design document summary for review
    design_summary = {
        "title": design_docs.get("title", "Technical Design Document"),
        "summary": design_docs.get("summary", "No summary available"),
        "sections": []
    }
    
    # Extract key sections for display
    if isinstance(design_docs, dict):
        for section_name, section_content in design_docs.items():
            if section_name not in ["title", "summary"] and isinstance(section_content, dict):
                section_summary = {
                    "name": section_name.replace('_', ' ').title(),
                    "overview": section_content.get("overview", "No overview available")
                }
                design_summary["sections"].append(section_summary)
    
    # ⭐ FIRST INTERRUPT: Show design document and get overall decision
    overall_decision = interrupt({
        "type": "human_design_review_decision",
        "prompt": "Please review the design document:",
        "design_document": design_summary,
        "question": "What's your overall decision about this design document?",
        "options": {
            "approve": "✅ Approve - ready for development phase",
            "request_changes": "⚠️ Request changes - need improvements",
            "reject": "❌ Reject - significant design issues found"
        }
    })
    
    feedback = ""
    suggestions = []
    
    # ⭐ SECOND INTERRUPT: Get detailed feedback if not approved
    if overall_decision != "approve":
        detailed_feedback = interrupt({
            "type": "human_design_review_feedback",
            "prompt": f"You chose to '{overall_decision}'. Please provide detailed feedback:",
            "question": "What specific changes or improvements are needed in the design?",
            "help_text": "Be specific about what needs to be changed in the design document."
        })
        
        feedback = detailed_feedback.get("feedback", "") if isinstance(detailed_feedback, dict) else str(detailed_feedback)
        
        # ⭐ THIRD INTERRUPT: Get specific suggestions (optional)
        if feedback:
            suggestion_input = interrupt({
                "type": "human_design_review_suggestions",
                "prompt": "Any specific technical suggestions for improvement?",
                "question": "Provide actionable technical suggestions (optional):",
                "current_feedback": feedback,
                "help_text": "Press Enter to skip, or provide specific technical suggestions"
            })
            
            if suggestion_input and str(suggestion_input).strip():
                suggestions = [str(suggestion_input).strip()]
    
    return {
        "status": overall_decision,
        "feedback": feedback or f"Human design review completed with decision: {overall_decision}",
        "reviewer": "Human",
        "timestamp": datetime.now().isoformat(),
        "approval_status": overall_decision,
        "suggestions": suggestions,
        "approved_sections": list(design_docs.keys()) if overall_decision == "approve" else [],
        "rejected_sections": list(design_docs.keys()) if overall_decision == "reject" else [],
        "technical_score": 8,
        "completeness_score": 8,
        "review_method": "human_dynamic"
    }

def _handle_ai_design_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle AI design review - automated technical review"""
    
    llm_utils = LLMUtils()
    design_docs = state.get("design_docs", {})
    requirements = state.get("requirements", "")
    user_stories = state.get("user_stories", [])
    
    system_prompt = """
    You are an experienced Technical Lead and Software Architect conducting a thorough review of design documents.
    
    Evaluate the design document based on:
    - Technical soundness and feasibility
    - Alignment with requirements and user stories
    - Completeness and clarity
    - Scalability and maintainability
    - Security considerations
    - Performance implications
    
    Provide your review as JSON with this structure:
    {
        "status": "approve" | "request_changes" | "reject",
        "feedback": "Overall technical feedback summary",
        "suggestions": ["List of specific technical suggestions"],
        "approved_sections": ["List of approved sections"],
        "rejected_sections": ["List of sections needing work"],
        "technical_score": 1-10,
        "completeness_score": 1-10,
        "overall_assessment": "Detailed technical assessment",
        "key_strengths": ["Main strengths of the design"],
        "key_concerns": ["Main technical concerns or gaps"]
    }
    
    Return ONLY the JSON object, no additional text.
    """
    
    # Format design document for review
    design_text = f"""
    DESIGN DOCUMENT:
    Title: {design_docs.get('title', 'N/A')}
    Summary: {design_docs.get('summary', 'N/A')}
    
    SYSTEM ARCHITECTURE:
    {design_docs.get('system_architecture', 'Not provided')}
    
    DATABASE DESIGN:
    {design_docs.get('database_design', 'Not provided')}
    
    API DESIGN:
    {design_docs.get('api_design', 'Not provided')}
    
    UI DESIGN:
    {design_docs.get('ui_design', 'Not provided')}
    
    SECURITY & PERFORMANCE:
    {design_docs.get('security_performance', 'Not provided')}
    
    IMPLEMENTATION NOTES:
    {design_docs.get('implementation_notes', 'Not provided')}
    """
    
    user_prompt = f"""
    Review this design document against the requirements and user stories:
    
    REQUIREMENTS:
    {requirements}
    
    USER STORIES COUNT: {len(user_stories)}
    
    DESIGN DOCUMENT TO REVIEW:
    {design_text}
    
    Provide a thorough technical review focusing on implementation feasibility and completeness.
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
        
        print("🤖 AI Technical Lead design review completed")
        return review_result
        
    except Exception as e:
        print(f"❌ AI design review failed: {e}")
        return _handle_auto_approve_design_dynamic(state)

def _handle_auto_approve_design_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle auto-approve design documents"""
    
    design_docs = state.get("design_docs", {})
    section_count = len(design_docs) if isinstance(design_docs, dict) else 1
    
    return {
        "status": "approve",
        "feedback": "Auto-approved by user choice - design review skipped",
        "reviewer": "Auto",
        "timestamp": datetime.now().isoformat(),
        "approval_status": "approve",
        "suggestions": [],
        "approved_sections": list(design_docs.keys()) if isinstance(design_docs, dict) else ["design_document"],
        "rejected_sections": [],
        "technical_score": 7,
        "completeness_score": 7,
        "overall_assessment": "Automatically approved without review",
        "review_method": "auto_dynamic"
    }

def revise_design_documents_dynamic(state: SDLCState) -> SDLCState:
    """
    Revise design documents based on feedback using dynamic pattern
    """
    print("🔄 Revising design documents based on review feedback...")
    
    current_design_docs = state.get("design_docs", {})
    review_feedback = state.get("review_feedback", {})
    current_iteration = state.get("iteration_count", 0)
    
    # Generate revised design documents using AI
    revised_design_docs = _generate_revised_design_documents_dynamic(current_design_docs, review_feedback)
    
    # Update state for next iteration
    updated_state = {
        **state,
        "design_docs": revised_design_docs,
        "current_stage": "design_documents_revised", 
        "iteration_count": current_iteration + 1,
        "timestamp": datetime.now().isoformat(),
        # Clear review feedback for next iteration
        "review_feedback": {},
        "approval_status": ""  # Reset for next review
    }
    
    print(f"✅ Design documents revised")
    print(f"🔄 Moving to iteration {updated_state['iteration_count']}")
    
    return updated_state

def _generate_revised_design_documents_dynamic(current_design_docs: Dict[str, Any], review_feedback: Dict[str, Any]) -> Dict[str, Any]:
    """Generate revised design documents using LLM based on feedback"""
    
    llm_utils = LLMUtils()
    
    feedback_summary = f"""
    Review Status: {review_feedback.get('status', 'unknown')}
    Feedback: {review_feedback.get('feedback', 'No specific feedback')}
    Suggestions: {review_feedback.get('suggestions', [])}
    Technical Score: {review_feedback.get('technical_score', 'N/A')}/10
    Completeness Score: {review_feedback.get('completeness_score', 'N/A')}/10
    Key Concerns: {review_feedback.get('key_concerns', [])}
    """
    
    system_prompt = f"""
    You are a Senior Software Architect revising design documents based on technical review feedback.
    
    Apply the feedback to improve the design document:
    1. Address technical concerns and gaps
    2. Improve clarity and completeness
    3. Enhance technical soundness
    4. Strengthen security and performance considerations
    5. Maintain the same structure but improve content
    
    Return the improved design document with the same JSON structure as the original.
    """
    
    design_docs_json = str(current_design_docs)
    
    user_prompt = f"""
    Revise this design document based on the technical review feedback:
    
    FEEDBACK TO ADDRESS:
    {feedback_summary}
    
    CURRENT DESIGN DOCUMENT:
    {design_docs_json}
    
    Apply the feedback and return the improved design document as JSON.
    """
    
    try:
        revised_design_docs = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        print(f"🤖 Design documents revised using AI based on feedback")
        return revised_design_docs
        
    except Exception as e:
        print(f"❌ Error revising design documents: {e}")
        return current_design_docs

def route_after_design_review_dynamic(state: SDLCState) -> str:
    """Route after design review based on approval status and iteration limits"""
    
    approval_status = state.get("approval_status", "")
    iteration_count = state.get("iteration_count", 0)
    
    if approval_status == "approve":
        print("✅ Design documents approved - proceeding to code generation phase")
        return "generate_code"
    elif iteration_count >= settings.MAX_ITERATIONS:
        print(f"⚠️ Maximum iterations ({settings.MAX_ITERATIONS}) reached - proceeding to code generation")
        return "generate_code"
    else:
        print(f"⚠️ Design documents need revision - iteration {iteration_count + 1}/{settings.MAX_ITERATIONS}")
        return "revise_design_documents"