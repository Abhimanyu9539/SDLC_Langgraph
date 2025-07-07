from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils

def auto_generate_user_stories(state: SDLCState) -> SDLCState:
    """
    Node 2: Auto-generate user stories from requirements
    """
    print("📖 Generating User Stories from Requirements")
    
    # Generate user stories using OpenAI
    user_stories = _generate_stories_from_requirements(state["requirements"])
    
    # Update state
    updated_state = {
        **state,
        "user_stories": user_stories,
        "current_stage": "user_stories_generated",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"✅ Generated {len(user_stories)} user stories")
    return updated_state

def _generate_stories_from_requirements(requirements: str) -> List[Dict[str, Any]]:
    """Generate user stories from requirements using LangChain OpenAI"""
    
    llm_utils = LLMUtils()
    
    system_prompt = """
    You are an expert Product Owner and Agile Coach. Your task is to analyze requirements and create comprehensive user stories.
    
    For each user story, you should:
    1. Follow the format: "As a [persona], I want [goal] so that [benefit]"
    2. Include detailed acceptance criteria
    3. Assign story points (1, 2, 3, 5, 8, 13)
    4. Set priority (High, Medium, Low)
    5. Add any dependencies or assumptions
    6. Include definition of done criteria
    
    Return the response as a JSON array of user stories with this structure:
    {
        "id": "US-001",
        "title": "Brief title",
        "description": "As a... I want... so that...",
        "acceptance_criteria": ["Given... When... Then..."],
        "story_points": 5,
        "priority": "High",
        "persona": "End User",
        "dependencies": [],
        "definition_of_done": ["Criteria 1", "Criteria 2"],
        "business_value": "Description of business value"
    }
    
    Focus on creating INVEST stories (Independent, Negotiable, Valuable, Estimable, Small, Testable).
    """
    
    user_prompt = f"""
    Based on the following requirements document, generate comprehensive user stories:
    
    {requirements}
    
    Create user stories that cover all functional requirements. Include stories for different user personas.
    Return ONLY the JSON array, no additional text.
    """
    
    try:
        user_stories = llm_utils.get_json_completion(system_prompt, user_prompt)
        print("🤖 User stories generated using LangChain OpenAI")
        return user_stories
        
    except Exception as e:
        print(f"❌ Error generating user stories: {e}")
        # Fallback stories
        return [
            {
                "id": "US-001",
                "title": "User Authentication",
                "description": "As an end user, I want to securely log into the system so that I can access my personal dashboard",
                "acceptance_criteria": [
                    "Given valid credentials, when I log in, then I should be redirected to my dashboard",
                    "Given invalid credentials, when I log in, then I should see an error message"
                ],
                "story_points": 8,
                "priority": "High",
                "persona": "End User",
                "dependencies": [],
                "definition_of_done": ["Unit tests written", "Security review completed"],
                "business_value": "Enables secure access to user data"
            }
        ]