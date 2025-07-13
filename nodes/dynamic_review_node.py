# ==================== DYNAMIC REVIEW NODE (INTERRUPT INSIDE) ====================
# File: nodes/dynamic_review_node.py

from datetime import datetime
from typing import List, Dict, Any
from langgraph.types import interrupt, Command
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def product_owner_review_dynamic(state: SDLCState) -> SDLCState:
    """
    Product Owner Review using DYNAMIC INTERRUPTS (Official Pattern)
    
    Key changes from static approach:
    - interrupt() is called INSIDE this function
    - No need for external state management
    - Direct value passing via Command(resume=value)
    - More context-aware and cleaner
    """
    
    print("\n👤 Product Owner Review - Dynamic Interrupt Pattern")
    print("🎯 Using interrupt() function inside node (official approach)")
    
    user_stories = state.get("user_stories", [])
    if not user_stories:
        print("⚠️ No user stories found - auto-approving")
        return {
            **state,
            "approval_status": "approved",
            "current_stage": "product_owner_review_complete",
            "timestamp": datetime.now().isoformat()
        }
    
    # ⭐ DYNAMIC INTERRUPT - This pauses execution and waits for user input
    user_choice = interrupt({
        "type": "review_choice",
        "question": "How would you like to review these user stories?",
        "options": {
            "human": "👤 I'll review them myself (Human Review)",
            "ai": "🤖 Let AI review them automatically (AI Review)",
            "auto": "⚡ Auto-approve and continue (Skip Review)"
        },
        "context": {
            "user_stories_count": len(user_stories),
            "current_iteration": state.get("iteration_count", 0),
            "project_id": state.get("project_id", "unknown")
        },
        "user_stories_preview": [
            {
                "id": story.get("id", f"US-{i+1}"),
                "title": story.get("title", "Untitled"),
                "priority": story.get("priority", "Unknown")
            }
            for i, story in enumerate(user_stories[:3])  # Show first 3
        ]
    })
    
    print(f"✅ User selected: {user_choice}")
    
    # Process the user's choice
    if user_choice == "human":
        print("👤 Processing human review...")
        review_result = _handle_human_review_dynamic(state)
    elif user_choice == "ai":
        print("🤖 Processing AI review...")
        review_result = _handle_ai_review_dynamic(state)
    elif user_choice == "auto":
        print("⚡ Auto-approving...")
        review_result = _handle_auto_approve_dynamic(state)
    else:
        print(f"⚠️ Unknown choice '{user_choice}' - defaulting to AI review")
        review_result = _handle_ai_review_dynamic(state)
    
    # Save review to history
    review_history = state.get("review_history", [])
    review_record = {
        "iteration": state.get("iteration_count", 0),
        "stage": "product_owner_review",
        "reviewer": review_result.get("reviewer", "Unknown"),
        "status": review_result.get("status", "unknown"),
        "feedback": review_result.get("feedback", ""),
        "suggestions": review_result.get("suggestions", []),
        "timestamp": review_result.get("timestamp", datetime.now().isoformat()),
        "business_value_score": review_result.get("business_value_score"),
        "completeness_score": review_result.get("completeness_score"),
        "review_method": user_choice
    }
    review_history.append(review_record)
    
    # Update state with review results
    updated_state = {
        **state,
        "review_feedback": review_result,
        "approval_status": review_result.get("status", "approved"),
        "current_stage": "product_owner_review_complete",
        "timestamp": datetime.now().isoformat(),
        "review_history": review_history
    }
    
    print(f"✅ Review completed - Status: {review_result.get('status', 'approved')}")
    print(f"👤 Reviewer: {review_result.get('reviewer', 'Unknown')}")
    
    return updated_state

def _handle_human_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """
    Handle human review using dynamic interrupts
    Can use MULTIPLE interrupts for detailed review process
    """
    
    user_stories = state.get("user_stories", [])
    
    # Prepare stories for review display
    stories_summary = []
    for i, story in enumerate(user_stories, 1):
        summary = {
            "number": i,
            "id": story.get("id", f"US-{i:03d}"),
            "title": story.get("title", "Untitled"),
            "description": story.get("description", "No description")[:100] + "...",
            "priority": story.get("priority", "Unknown"),
            "story_points": story.get("story_points", "TBD"),
            "acceptance_criteria_count": len(story.get("acceptance_criteria", []))
        }
        stories_summary.append(summary)
    
    # ⭐ FIRST INTERRUPT: Show stories and get overall decision
    overall_decision = interrupt({
        "type": "human_review_decision",
        "prompt": "Please review these user stories:",
        "stories": stories_summary,
        "question": "What's your overall decision about these user stories?",
        "options": {
            "approve": "✅ Approve all - ready for design phase",
            "request_changes": "⚠️ Request changes - need improvements",
            "reject": "❌ Reject all - significant issues found"
        }
    })
    
    feedback = ""
    suggestions = []
    
    # ⭐ SECOND INTERRUPT: Get detailed feedback if not approved
    if overall_decision != "approve":
        detailed_feedback = interrupt({
            "type": "human_review_feedback",
            "prompt": f"You chose to '{overall_decision}'. Please provide detailed feedback:",
            "question": "What specific changes or improvements are needed?",
            "help_text": "Be specific about what needs to be changed in the user stories."
        })
        
        feedback = detailed_feedback.get("feedback", "") if isinstance(detailed_feedback, dict) else str(detailed_feedback)
        
        # ⭐ THIRD INTERRUPT: Get specific suggestions (optional)
        if feedback:
            suggestion_input = interrupt({
                "type": "human_review_suggestions",
                "prompt": "Any specific suggestions for improvement?",
                "question": "Provide actionable suggestions (optional):",
                "current_feedback": feedback,
                "help_text": "Press Enter to skip, or provide specific suggestions"
            })
            
            if suggestion_input and str(suggestion_input).strip():
                suggestions = [str(suggestion_input).strip()]
    
    return {
        "status": overall_decision,
        "feedback": feedback or f"Human review completed with decision: {overall_decision}",
        "reviewer": "Human",
        "timestamp": datetime.now().isoformat(),
        "approval_status": overall_decision,
        "suggestions": suggestions,
        "approved_stories": [s.get("id", f"US-{i+1}") for i, s in enumerate(user_stories)] if overall_decision == "approve" else [],
        "rejected_stories": [s.get("id", f"US-{i+1}") for i, s in enumerate(user_stories)] if overall_decision == "reject" else [],
        "business_value_score": 8,
        "completeness_score": 8,
        "review_method": "human_dynamic"
    }

def _handle_ai_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle AI review - same logic as before but cleaner integration"""
    
    llm_utils = LLMUtils()
    user_stories = state.get("user_stories", [])
    requirements = state.get("requirements", "")
    
    system_prompt = """
    You are an experienced Product Owner conducting a thorough review of user stories.
    
    Evaluate the stories based on:
    - INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
    - Alignment with requirements
    - Clarity and completeness
    - Business value
    
    Provide your review as JSON with this structure:
    {
        "status": "approve" | "request_changes" | "reject",
        "feedback": "Overall feedback summary",
        "suggestions": ["List of specific suggestions"],
        "approved_stories": ["List of approved story IDs"],
        "rejected_stories": ["List of rejected story IDs"],
        "business_value_score": 1-10,
        "completeness_score": 1-10,
        "overall_assessment": "Detailed assessment"
    }
    
    Return ONLY the JSON object, no additional text.
    """
    
    # Format stories for review
    stories_text = "\n".join([
        f"ID: {story.get('id', 'N/A')}\n"
        f"TITLE: {story.get('title', 'N/A')}\n"
        f"DESCRIPTION: {story.get('description', 'N/A')}\n"
        f"PRIORITY: {story.get('priority', 'N/A')}\n"
        f"STORY POINTS: {story.get('story_points', 'N/A')}\n"
        f"ACCEPTANCE CRITERIA: {story.get('acceptance_criteria', [])}\n"
        f"BUSINESS VALUE: {story.get('business_value', 'N/A')}\n"
        for story in user_stories
    ])
    
    user_prompt = f"""
    Review these user stories against requirements:
    
    REQUIREMENTS: {requirements}
    
    USER STORIES:
    {stories_text}
    
    Return only JSON review.
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
        
        print("🤖 AI Product Owner review completed")
        return review_result
        
    except Exception as e:
        print(f"❌ AI review failed: {e}")
        return _handle_auto_approve_dynamic(state)

def _handle_auto_approve_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle auto-approve - instant approval"""
    
    user_stories = state.get("user_stories", [])
    story_ids = [story.get("id", f"US-{i+1}") for i, story in enumerate(user_stories)]
    
    return {
        "status": "approve",
        "feedback": "Auto-approved by user choice - review skipped",
        "reviewer": "Auto",
        "timestamp": datetime.now().isoformat(),
        "approval_status": "approve",
        "suggestions": [],
        "approved_stories": story_ids,
        "rejected_stories": [],
        "business_value_score": 7,
        "completeness_score": 7,
        "overall_assessment": "Automatically approved without review",
        "review_method": "auto_dynamic"
    }

def revise_user_stories_dynamic(state: SDLCState) -> SDLCState:
    """
    Revise user stories based on feedback using dynamic pattern
    """
    print("🔄 Revising user stories based on Product Owner feedback...")
    
    current_stories = state.get("user_stories", [])
    review_feedback = state.get("review_feedback", {})
    current_iteration = state.get("iteration_count", 0)
    
    # Generate revised stories using AI
    revised_stories = _generate_revised_stories_dynamic(current_stories, review_feedback)
    
    # Update state for next iteration
    updated_state = {
        **state,
        "user_stories": revised_stories,
        "current_stage": "user_stories_revised", 
        "iteration_count": current_iteration + 1,
        "timestamp": datetime.now().isoformat(),
        # Clear review feedback for next iteration
        "review_feedback": {},
        "approval_status": ""  # Reset for next review
    }
    
    print(f"✅ User stories revised - Total stories: {len(revised_stories)}")
    print(f"🔄 Moving to iteration {updated_state['iteration_count']}")
    
    return updated_state

def _generate_revised_stories_dynamic(current_stories: List[Dict[str, Any]], review_feedback: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate revised stories using LLM based on feedback"""
    
    llm_utils = LLMUtils()
    
    feedback_summary = f"""
    Review Status: {review_feedback.get('status', 'unknown')}
    Feedback: {review_feedback.get('feedback', 'No specific feedback')}
    Suggestions: {review_feedback.get('suggestions', [])}
    Business Value Score: {review_feedback.get('business_value_score', 'N/A')}/10
    Completeness Score: {review_feedback.get('completeness_score', 'N/A')}/10
    """
    
    system_prompt = f"""
    You are a Business Analyst revising user stories based on Product Owner feedback.
    
    IMPORTANT CONSTRAINTS:
    - Return EXACTLY {settings.MAX_USER_STORIES} user stories
    - Apply the feedback to improve the stories
    - Maintain story structure and improve content
    - Address specific concerns raised
    
    Apply the feedback to improve:
    1. Story clarity and completeness
    2. INVEST criteria compliance
    3. Business value alignment
    4. Acceptance criteria quality
    
    Return exactly {settings.MAX_USER_STORIES} improved user stories as JSON array.
    """
    
    stories_json = str(current_stories)
    
    user_prompt = f"""
    Revise these user stories based on the Product Owner feedback:
    
    FEEDBACK TO ADDRESS:
    {feedback_summary}
    
    CURRENT USER STORIES:
    {stories_json}
    
    Apply the feedback and return EXACTLY {settings.MAX_USER_STORIES} improved stories as JSON array.
    """
    
    try:
        revised_stories = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        # Enforce story limit
        if len(revised_stories) > settings.MAX_USER_STORIES:
            revised_stories = revised_stories[:settings.MAX_USER_STORIES]
        elif len(revised_stories) < settings.MAX_USER_STORIES:
            # Pad with original stories if needed
            while len(revised_stories) < settings.MAX_USER_STORIES and len(current_stories) > len(revised_stories):
                revised_stories.append(current_stories[len(revised_stories)])
        
        print(f"🤖 Stories revised using AI based on feedback")
        return revised_stories
        
    except Exception as e:
        print(f"❌ Error revising stories: {e}")
        return current_stories[:settings.MAX_USER_STORIES]

def route_after_po_review_dynamic(state: SDLCState) -> str:
    """Route after PO review based on approval status and iteration limits"""
    
    approval_status = state.get("approval_status", "")
    iteration_count = state.get("iteration_count", 0)
    
    if approval_status == "approve":
        print("✅ Stories approved - proceeding to design phase")
        return "create_design_documents"
    elif iteration_count >= settings.MAX_ITERATIONS:
        print(f"⚠️ Maximum iterations ({settings.MAX_ITERATIONS}) reached - proceeding to design")
        return "create_design_documents"
    else:
        print(f"⚠️ Stories need revision - iteration {iteration_count + 1}/{settings.MAX_ITERATIONS}")
        return "revise_user_stories"

def create_design_documents(state: SDLCState) -> SDLCState:
    """Create design documents (placeholder for final step)"""
    
    print("🎨 Creating design documents...")
    
    design_docs = {
        "architecture": "High-level system architecture",
        "database_schema": "Database design and schema",
        "api_specification": "REST API endpoints and contracts",
        "ui_wireframes": "User interface wireframes and mockups"
    }
    
    return {
        **state,
        "design_docs": design_docs,
        "current_stage": "design_documents_created",
        "timestamp": datetime.now().isoformat()
    }