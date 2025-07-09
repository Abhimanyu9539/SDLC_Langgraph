# ==================== USER STORIES NODE ====================
# File: nodes/user_stories_node.py

from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def auto_generate_user_stories(state: SDLCState) -> SDLCState:
    """
    Node 2: Auto-generate user stories from requirements
    
    This node takes the enhanced requirements and:
    1. Analyzes the requirements to identify user personas
    2. Generates comprehensive user stories with acceptance criteria
    3. Prioritizes stories based on business value
    4. Formats stories in standard Agile format
    
    Args:
        state: Current SDLC state with requirements
        
    Returns:
        Updated state with generated user stories
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
    
    system_prompt = f"""
    You are an expert Product Owner and Agile Coach. Your task is to analyze requirements and create comprehensive user stories.
    
    IMPORTANT CONSTRAINTS:
    - Generate EXACTLY {settings.MAX_USER_STORIES} user stories, no more, no less
    - Focus on the most critical and high-value functionality first
    - Prioritize core features over nice-to-have features
    
    For each user story, you should:
    1. Follow the format: "As a [persona], I want [goal] so that [benefit]"
    2. Include detailed acceptance criteria
    3. Assign story points (1, 2, 3, 5, 8, 13)
    4. Set priority (High, Medium, Low)
    5. Add any dependencies or assumptions
    6. Include definition of done criteria
    
    Return the response as a JSON array of EXACTLY {settings.MAX_USER_STORIES} user stories with this structure:
    {{
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
    }}
    
    Focus on creating INVEST stories (Independent, Negotiable, Valuable, Estimable, Small, Testable).
    Remember: EXACTLY {settings.MAX_USER_STORIES} stories only.
    """
    
    user_prompt = f"""
    Based on the following requirements document, generate EXACTLY {settings.MAX_USER_STORIES} user stories covering the most important functionality:
    
    {requirements}
    
    Create the {settings.MAX_USER_STORIES} most critical user stories that provide maximum business value.
    Return ONLY the JSON array with exactly {settings.MAX_USER_STORIES} stories, no additional text.
    """
    
    try:
        user_stories = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        # Enforce story limit in case AI doesn't follow instructions
        if len(user_stories) > settings.MAX_USER_STORIES:
            user_stories = user_stories[:settings.MAX_USER_STORIES]
            print(f"⚠️ Trimmed to {settings.MAX_USER_STORIES} stories as per limit")
        
        print(f"🤖 Generated {len(user_stories)} user stories (limit: {settings.MAX_USER_STORIES})")
        return user_stories
        
    except Exception as e:
        print(f"❌ Error generating user stories: {e}")
        # Fallback stories - exactly MAX_USER_STORIES
        fallback_stories = [
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
            },
            {
                "id": "US-002",
                "title": "Dashboard View",
                "description": "As an authenticated user, I want to view my dashboard so that I can see my key information",
                "acceptance_criteria": [
                    "Given I'm logged in, when I access dashboard, then I see my data",
                    "Given dashboard loads, when I refresh, then data updates"
                ],
                "story_points": 5,
                "priority": "High",
                "persona": "End User",
                "dependencies": ["US-001"],
                "definition_of_done": ["UI implemented", "Performance tested"],
                "business_value": "Provides users with immediate value"
            },
            {
                "id": "US-003",
                "title": "User Profile Management",
                "description": "As a user, I want to manage my profile information so that I can keep my data current",
                "acceptance_criteria": [
                    "Given I'm logged in, when I update profile, then changes are saved",
                    "Given invalid data, when I submit, then I see validation errors"
                ],
                "story_points": 3,
                "priority": "Medium",
                "persona": "End User",
                "dependencies": ["US-001"],
                "definition_of_done": ["CRUD operations implemented", "Validation added"],
                "business_value": "Allows users to maintain accurate information"
            }
        ]
        return fallback_stories[:settings.MAX_USER_STORIES]