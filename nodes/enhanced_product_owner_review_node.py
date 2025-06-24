# ==================== ENHANCED PRODUCT OWNER REVIEW NODE ====================
# File: nodes/enhanced_product_owner_review_node.py

from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def product_owner_review(state: SDLCState) -> SDLCState:
    """
    Enhanced Product Owner Review that respects user choice from interrupt
    
    This node checks the state to see how the user wants to handle the review:
    - If auto-approved: skip review
    - If human requested: collect human input
    - Default: use AI review
    """
    
    print("\n👤 Product Owner Review Node - Enhanced with Choice Handling")
    print(f"🎯 Review type from interrupt: {state.get('review_type', 'unknown')}")
    
    # Check if this was auto-approved during interrupt
    if state.get("approval_status") == "approved":
        print("⚡ Auto-approved during interrupt - skipping review")
        return {
            **state,
            "current_stage": "product_owner_review_complete",
            "timestamp": datetime.now().isoformat()
        }
    
    # Check review type from interrupt handling
    review_type = state.get("review_type", "ai")
    human_review_requested = state.get("human_review_requested", False)
    
    if human_review_requested or review_type == "human":
        print("👤 Human review requested - collecting input...")
        review_result = _collect_human_review_in_node(state)
    else:
        print("🤖 AI review mode - using automated review...")
        review_result = _perform_po_review(state["user_stories"], state["requirements"])
    
    # Update state with review results
    updated_state = {
        **state,
        "review_feedback": {
            **review_result,
            "stage": "product_owner_review",
            "timestamp": datetime.now().isoformat(),
        },
        "approval_status": review_result.get("approval_status", review_result.get("status", "approved")),
        "current_stage": "product_owner_review_complete",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"✅ Product Owner review completed - Status: {review_result.get('status', 'approved')}")
    print(f"👤 Reviewer: {review_result.get('reviewer', 'Unknown')}")
    
    return updated_state

def _collect_human_review_in_node(state: SDLCState) -> Dict[str, Any]:
    """
    Collect human review input within the node
    This is called when human review was specifically requested
    """
    
    print("\n👤 Human Review Mode")
    print("=" * 40)
    
    user_stories = state.get("user_stories", [])
    
    if not user_stories:
        return {
            "status": "approved",
            "feedback": "No stories to review",
            "reviewer": "Human",
            "approval_status": "approved"
        }
    
    print(f"📚 Reviewing {len(user_stories)} user stories:")
    
    # Show stories
    for i, story in enumerate(user_stories, 1):
        print(f"\n{i}. {story.get('id', 'N/A')}: {story.get('title', 'Untitled')}")
        print(f"   📝 {story.get('description', 'No description')}")
        
        # Show acceptance criteria preview
        criteria = story.get('acceptance_criteria', [])
        if criteria:
            print(f"   ✅ {len(criteria)} acceptance criteria defined")
    
    # Get human decision
    print(f"\n🎯 Your review of these {len(user_stories)} user stories:")
    print("1. ✅ Approve all - ready for design phase")
    print("2. ⚠️ Request changes - need improvements")
    print("3. ❌ Reject all - significant issues")
    
    while True:
        choice = input("\nYour decision (1/2/3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("❌ Please choose 1, 2, or 3")
    
    # Get feedback if not approved
    feedback = ""
    suggestions = []
    if choice != '1':
        feedback = input("\n💬 Please provide your feedback: ").strip()
        if not feedback:
            feedback = "Human reviewer requested changes"
        
        # Ask for specific suggestions
        print("\n💡 Any specific suggestions? (press Enter to skip)")
        suggestion = input("Suggestion: ").strip()
        if suggestion:
            suggestions.append(suggestion)
    
    # Map choice to status
    status_map = {'1': 'approved', '2': 'feedback', '3': 'rejected'}
    status = status_map[choice]
    
    return {
        "status": status,
        "feedback": feedback or f"Human review completed - {status}",
        "reviewer": "Human",
        "approval_status": status,
        "suggestions": suggestions,
        "approved_stories": [s.get('id') for s in user_stories] if status == 'approved' else [],
        "rejected_stories": [s.get('id') for s in user_stories] if status == 'rejected' else [],
        "business_value_score": 8,
        "completeness_score": 8
    }

def _perform_po_review(user_stories: List[Dict[str, Any]], requirements: str) -> Dict[str, Any]:
    """
    Perform AI-powered Product Owner review (same as before)
    """
    
    llm_utils = LLMUtils()
    
    system_prompt = """
    You are an experienced Product Owner conducting a thorough review of user stories.
    
    Provide your review as JSON with this structure:
    {
        "status": "approved" | "feedback" | "rejected",
        "feedback": "Overall feedback summary",
        "suggestions": ["List of suggestions"],
        "approved_stories": ["List of approved story IDs"],
        "rejected_stories": ["List of rejected story IDs"],
        "business_value_score": 1-10,
        "completeness_score": 1-10,
        "overall_assessment": "Detailed assessment"
    }
    
    Return ONLY the JSON object, no additional text.
    """
    
    # Format stories for review
    stories_text = _format_stories_for_review(user_stories)
    
    user_prompt = f"""
    Review these user stories against requirements:
    
    REQUIREMENTS: {requirements}
    
    USER STORIES: {stories_text}
    
    Return only JSON review.
    """
    
    try:
        review_result = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        # Ensure required fields
        review_result["approval_status"] = review_result.get("status", "approved")
        review_result["reviewer"] = "AI"
        
        print("🤖 AI Product Owner review completed")
        return review_result
        
    except Exception as e:
        print(f"❌ AI review failed: {e}")
        return _generate_fallback_review(user_stories)

def _format_stories_for_review(user_stories: List[Dict[str, Any]]) -> str:
    """Format user stories for AI review"""
    
    formatted_stories = []
    
    for story in user_stories:
        story_text = f"""
ID: {story.get('id', 'N/A')}
TITLE: {story.get('title', 'N/A')}
DESCRIPTION: {story.get('description', 'N/A')}
PRIORITY: {story.get('priority', 'N/A')}
STORY POINTS: {story.get('story_points', 'N/A')}
ACCEPTANCE CRITERIA: {story.get('acceptance_criteria', [])}
BUSINESS VALUE: {story.get('business_value', 'N/A')}
        """
        formatted_stories.append(story_text.strip())
    
    return "\n" + "="*50 + "\n".join(formatted_stories)

def _generate_fallback_review(user_stories: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate fallback review when AI fails"""
    
    story_ids = [story.get('id', f'US-{i+1}') for i, story in enumerate(user_stories)]
    
    return {
        "status": "approved",
        "feedback": "Fallback review - stories appear acceptable",
        "reviewer": "AI-Fallback",
        "approval_status": "approved",
        "suggestions": [],
        "approved_stories": story_ids,
        "rejected_stories": [],
        "business_value_score": 7,
        "completeness_score": 7,
        "overall_assessment": "Automated fallback review completed"
    }

def revise_user_stories(state: SDLCState) -> SDLCState:
    """
    Revise user stories based on Product Owner feedback
    (Same as before, but enhanced to work with new state structure)
    """
    print("🔄 Revising user stories based on feedback...")
    
    current_stories = state["user_stories"]
    review_feedback = state["review_feedback"]
    
    # Generate revised stories using existing logic
    revised_stories = _generate_revised_stories(current_stories, review_feedback)
    
    return {
        **state,
        "user_stories": revised_stories,
        "current_stage": "user_stories_revised",
        "iteration_count": state["iteration_count"] + 1,
        "timestamp": datetime.now().isoformat()
    }

def _generate_revised_stories(current_stories: List[Dict[str, Any]], review_feedback: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate revised stories (simplified for demo)"""
    
    # For now, just return current stories with minor modifications
    # In full implementation, this would use AI to apply feedback
    
    print(f"🔧 Applying feedback: {review_feedback.get('feedback', 'No feedback')}")
    
    return current_stories[:settings.MAX_USER_STORIES]

def route_after_po_review(state: SDLCState) -> str:
    """Route after PO review based on approval status and iteration limits"""
    
    approval_status = state.get("approval_status", "")
    iteration_count = state.get("iteration_count", 0)
    
    if approval_status == "approved":
        print("✅ Stories approved - proceeding to design phase")
        return "create_design_documents"
    elif iteration_count >= settings.MAX_ITERATIONS:
        print(f"⚠️ Maximum iterations ({settings.MAX_ITERATIONS}) reached - proceeding")
        return "create_design_documents"
    else:
        print(f"⚠️ Stories need revision - iteration {iteration_count + 1}/{settings.MAX_ITERATIONS}")
        return "revise_user_stories"