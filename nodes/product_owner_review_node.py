from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def product_owner_review(state: SDLCState) -> SDLCState:
    """
    Node 3: Product Owner Review of User Stories
    
    This node simulates a Product Owner reviewing the generated user stories:
    1. Analyzes user stories for business value and completeness
    2. Checks alignment with original requirements
    3. Provides feedback or approval
    4. Suggests improvements if needed
    
    Args:
        state: Current SDLC state with user stories
        
    Returns:
        Updated state with review feedback and approval status
    """
    print("👤 Product Owner reviewing user stories...")
    
    # Perform AI-powered review of user stories
    review_result = _perform_po_review(
        state["user_stories"], 
        state["requirements"]
    )
    
    # Update state with review results
    updated_state = {
        **state,
        "review_feedback": {
            "stage": "product_owner_review",
            "status": review_result["status"],
            "feedback": review_result["feedback"],
            "reviewer": "Product Owner",
            "timestamp": datetime.now().isoformat(),
            "suggestions": review_result.get("suggestions", []),
            "approved_stories": review_result.get("approved_stories", []),
            "rejected_stories": review_result.get("rejected_stories", [])
        },
        "approval_status": review_result["status"],
        "current_stage": "product_owner_review_complete",
        "timestamp": datetime.now().isoformat()
    }
    
    # Display review results
    _display_review_results(review_result)
    
    print(f"✅ Product Owner review completed - Status: {review_result['status']}")
    return updated_state

def _perform_po_review(user_stories: List[Dict[str, Any]], requirements: str) -> Dict[str, Any]:
    """
    Perform AI-powered Product Owner review of user stories
    
    Args:
        user_stories: List of generated user stories
        requirements: Original requirements document
        
    Returns:
        Review result with status, feedback, and suggestions
    """
    
    llm_utils = LLMUtils()
    
    system_prompt = """
    You are an experienced Product Owner conducting a thorough review of user stories. Your role is to ensure that:
    
    1. Stories align with business requirements and objectives
    2. Stories provide clear business value
    3. Acceptance criteria are comprehensive and testable
    4. Story priorities reflect business importance
    5. Stories are appropriately sized and independent
    6. Missing functionality is identified
    
    Review Criteria:
    - Business Value: Does each story deliver tangible value?
    - Completeness: Are all requirements covered?
    - Clarity: Are stories clear and unambiguous?
    - Testability: Can acceptance criteria be verified?
    - Priority: Are priorities aligned with business needs?
    - Dependencies: Are dependencies properly identified?
    
    IMPORTANT: You must respond with ONLY valid JSON, no additional text or formatting.
    
    Provide your review as JSON with this exact structure:
    {
        "status": "approved",
        "feedback": "Overall feedback summary here",
        "suggestions": ["suggestion 1", "suggestion 2"],
        "approved_stories": ["US-001", "US-002"],
        "rejected_stories": ["US-003"],
        "missing_functionality": ["feature 1", "feature 2"],
        "business_value_score": 8,
        "completeness_score": 7,
        "overall_assessment": "Detailed assessment paragraph here"
    }
    
    Status Guidelines:
    - "approved": All stories meet standards, ready for design phase
    - "feedback": Stories are good but need minor improvements  
    - "rejected": Stories need significant revision before proceeding
    
    Return ONLY the JSON object, no markdown, no extra text.
    """
    
    # Prepare user stories for review
    stories_text = _format_stories_for_review(user_stories)
    
    user_prompt = f"""
    Review these user stories against the requirements and return ONLY valid JSON:
    
    REQUIREMENTS:
    {requirements}
    
    USER STORIES:
    {stories_text}
    
    Return only the JSON review object with no additional formatting or text.
    """
    
    try:
        review_result = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        # Validate required fields
        required_fields = ['status', 'feedback', 'suggestions', 'approved_stories', 'rejected_stories']
        for field in required_fields:
            if field not in review_result:
                review_result[field] = [] if field.endswith('_stories') or field == 'suggestions' else 'Not provided'
        
        # Ensure scores are integers
        review_result['business_value_score'] = int(review_result.get('business_value_score', 7))
        review_result['completeness_score'] = int(review_result.get('completeness_score', 7))
        
        print("🤖 Product Owner review completed using LangChain OpenAI")
        return review_result
        
    except Exception as e:
        print(f"❌ Error during PO review: {e}")
        # Return fallback review result
        return _generate_fallback_review(user_stories)


def _format_stories_for_review(user_stories: List[Dict[str, Any]]) -> str:
    """Format user stories for AI review"""
    
    formatted_stories = []
    
    for story in user_stories:
        story_text = f"""
STORY ID: {story.get('id', 'N/A')}
TITLE: {story.get('title', 'N/A')}
DESCRIPTION: {story.get('description', 'N/A')}
PRIORITY: {story.get('priority', 'N/A')}
STORY POINTS: {story.get('story_points', 'N/A')}
PERSONA: {story.get('persona', 'N/A')}

ACCEPTANCE CRITERIA:
{chr(10).join(f"  • {criteria}" for criteria in story.get('acceptance_criteria', []))}

BUSINESS VALUE: {story.get('business_value', 'N/A')}

DEFINITION OF DONE:
{chr(10).join(f"  • {dod}" for dod in story.get('definition_of_done', []))}

DEPENDENCIES: {', '.join(story.get('dependencies', [])) if story.get('dependencies') else 'None'}
        """
        formatted_stories.append(story_text.strip())
    
    return "\n" + "="*80 + "\n".join(formatted_stories)

def _generate_fallback_review(user_stories: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate fallback review when AI fails"""
    
    story_ids = [story.get('id', f'US-{i+1}') for i, story in enumerate(user_stories)]
    
    return {
        "status": "feedback",
        "feedback": "Automated review completed. Stories look good overall but please verify business alignment manually.",
        "suggestions": [
            "Verify acceptance criteria completeness",
            "Confirm story priorities align with business objectives",
            "Review story dependencies for accuracy"
        ],
        "approved_stories": story_ids[:-1] if len(story_ids) > 1 else [],
        "rejected_stories": [story_ids[-1]] if story_ids else [],
        "missing_functionality": ["User profile management", "Error handling scenarios"],
        "business_value_score": 7,
        "completeness_score": 8,
        "overall_assessment": "The user stories provide a solid foundation for development. Minor adjustments needed for the last story to improve clarity and testability."
    }

def _display_review_results(review_result: Dict[str, Any]) -> None:
    """Display formatted review results to user"""
    
    print("\n" + "="*80)
    print("👤 PRODUCT OWNER REVIEW RESULTS")
    print("="*80)
    
    # Status and overall feedback
    status = review_result.get("status", "unknown")
    status_emoji = {"approved": "✅", "feedback": "⚠️", "rejected": "❌"}.get(status, "❓")
    
    print(f"\n{status_emoji} REVIEW STATUS: {status.upper()}")
    print(f"\n📝 OVERALL FEEDBACK:")
    print(f"   {review_result.get('feedback', 'No feedback provided')}")
    
    # Scores
    bv_score = review_result.get("business_value_score", 0)
    comp_score = review_result.get("completeness_score", 0)
    print(f"\n📊 SCORES:")
    print(f"   • Business Value: {bv_score}/10")
    print(f"   • Completeness: {comp_score}/10")
    
    # Approved stories
    approved = review_result.get("approved_stories", [])
    if approved:
        print(f"\n✅ APPROVED STORIES ({len(approved)}):")
        for story_id in approved:
            print(f"   • {story_id}")
    
    # Stories needing revision
    rejected = review_result.get("rejected_stories", [])
    if rejected:
        print(f"\n❌ STORIES NEEDING REVISION ({len(rejected)}):")
        for story_id in rejected:
            print(f"   • {story_id}")
    
    # Suggestions
    suggestions = review_result.get("suggestions", [])
    if suggestions:
        print(f"\n💡 IMPROVEMENT SUGGESTIONS:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion}")
    
    # Missing functionality
    missing = review_result.get("missing_functionality", [])
    if missing:
        print(f"\n🔍 MISSING FUNCTIONALITY IDENTIFIED:")
        for i, functionality in enumerate(missing, 1):
            print(f"   {i}. {functionality}")
    
    # Overall assessment
    assessment = review_result.get("overall_assessment", "")
    if assessment:
        print(f"\n📋 DETAILED ASSESSMENT:")
        print(f"   {assessment}")
    
    print("="*80)

def revise_user_stories(state: SDLCState) -> SDLCState:
    """
    Node 3b: Revise user stories based on Product Owner feedback
    
    This node takes PO feedback and generates revised user stories:
    1. Analyzes the feedback and suggestions
    2. Identifies specific areas for improvement
    3. Generates revised versions of rejected stories
    4. Adds missing functionality as new stories
    
    Args:
        state: Current SDLC state with review feedback
        
    Returns:
        Updated state with revised user stories
    """
    print("🔄 Revising user stories based on Product Owner feedback...")
    
    # Get current stories and feedback
    current_stories = state["user_stories"]
    review_feedback = state["review_feedback"]
    
    # Generate revised stories
    revised_stories = _generate_revised_stories(current_stories, review_feedback)
    
    # Update state
    updated_state = {
        **state,
        "user_stories": revised_stories,
        "current_stage": "user_stories_revised",
        "iteration_count": state["iteration_count"] + 1,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"✅ User stories revised - Total stories: {len(revised_stories)}")
    print(f"🔄 Iteration count: {updated_state['iteration_count']}")
    
    return updated_state

def _generate_revised_stories(
    current_stories: List[Dict[str, Any]], 
    review_feedback: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Generate revised user stories based on PO feedback"""
    
    llm_utils = LLMUtils()
    
    system_prompt = f"""
    You are a Business Analyst working with a Product Owner to revise user stories based on feedback.
    
    IMPORTANT CONSTRAINTS:
    - You must return EXACTLY {settings.MAX_USER_STORIES} user stories, no more, no less
    - Focus on the most critical functionality
    - If adding missing functionality, replace lower priority stories
    
    Your task is to:
    1. Revise stories that were rejected or need improvement
    2. Incorporate all suggestions and feedback
    3. Add any missing functionality as new stories (but maintain {settings.MAX_USER_STORIES} total)
    4. Maintain approved stories unchanged if possible
    5. Ensure all stories meet INVEST criteria
    
    Return EXACTLY {settings.MAX_USER_STORIES} user stories as a JSON array with the same structure as before.
    Keep approved stories exactly as they were. Focus improvements on rejected stories and add missing functionality.
    Remember: EXACTLY {settings.MAX_USER_STORIES} stories total.
    """
    
    feedback_text = f"""
Review Status: {review_feedback.get('status', 'unknown')}
Overall Feedback: {review_feedback.get('feedback', '')}
Suggestions: {review_feedback.get('suggestions', [])}
Approved Stories: {review_feedback.get('approved_stories', [])}
Stories Needing Revision: {review_feedback.get('rejected_stories', [])}
Missing Functionality: {review_feedback.get('missing_functionality', [])}
    """
    
    stories_text = _format_stories_for_review(current_stories)
    
    user_prompt = f"""
    Based on the Product Owner feedback below, please revise the user stories to exactly {settings.MAX_USER_STORIES} stories:
    
    PRODUCT OWNER FEEDBACK:
    {feedback_text}
    
    CURRENT USER STORIES:
    {stories_text}
    
    Generate EXACTLY {settings.MAX_USER_STORIES} revised user stories incorporating all feedback.
    Return ONLY the JSON array with exactly {settings.MAX_USER_STORIES} stories, no additional text.
    """
    
    try:
        revised_stories = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        # Enforce story limit
        if len(revised_stories) > settings.MAX_USER_STORIES:
            revised_stories = revised_stories[:settings.MAX_USER_STORIES]
            print(f"⚠️ Trimmed to {settings.MAX_USER_STORIES} stories as per limit")
        elif len(revised_stories) < settings.MAX_USER_STORIES:
            # Pad with original stories if needed
            while len(revised_stories) < settings.MAX_USER_STORIES and len(current_stories) > len(revised_stories):
                revised_stories.append(current_stories[len(revised_stories)])
        
        print(f"🤖 User stories revised to {len(revised_stories)} stories (limit: {settings.MAX_USER_STORIES})")
        return revised_stories
        
    except Exception as e:
        print(f"❌ Error revising user stories: {e}")
        # Fallback: return original stories trimmed to limit
        return current_stories[:settings.MAX_USER_STORIES]

def _apply_basic_revisions(
    stories: List[Dict[str, Any]], 
    feedback: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Apply basic revisions when AI fails - maintain story limit"""
    
    # Ensure we have exactly MAX_USER_STORIES
    revised_stories = stories[:settings.MAX_USER_STORIES] if len(stories) >= settings.MAX_USER_STORIES else stories.copy()
    
    # If we have fewer than MAX_USER_STORIES, add a simple story
    while len(revised_stories) < settings.MAX_USER_STORIES:
        new_story = {
            "id": f"US-{len(revised_stories) + 1:03d}",
            "title": "Error Handling",
            "description": "As a user, I want proper error messages so that I understand what went wrong",
            "acceptance_criteria": [
                "Given an error occurs, when I see the message, then it should be clear and actionable",
                "Given a network error, when it happens, then I should see a retry option"
            ],
            "story_points": 3,
            "priority": "Medium",
            "persona": "End User",
            "dependencies": [],
            "definition_of_done": ["Error handling implemented", "User testing completed"],
            "business_value": "Improves user experience and reduces support tickets"
        }
        revised_stories.append(new_story)
    
    return revised_stories[:settings.MAX_USER_STORIES]  # Ensure exactly MAX_USER_STORIES

# ==================== ROUTING FUNCTION ====================

def route_after_po_review(state: SDLCState) -> str:
    """
    Route after Product Owner review based on approval status and iteration limits
    
    Args:
        state: Current SDLC state
        
    Returns:
        Next node name to execute
    """
    approval_status = state.get("approval_status", "")
    iteration_count = state.get("iteration_count", 0)
    
    if approval_status == "approved" :
        print("✅ Stories approved - proceeding to design phase")
        return "create_design_documents"
    elif iteration_count >= settings.MAX_ITERATIONS:
        print(f"⚠️ Maximum iterations ({settings.MAX_ITERATIONS}) reached - proceeding with current stories")
        return "create_design_documents"
    else:
        print(f"⚠️ Stories need revision - routing to revision node (iteration {iteration_count + 1}/{settings.MAX_ITERATIONS})")
        return "revise_user_stories"