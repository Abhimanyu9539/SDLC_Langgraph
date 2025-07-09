from datetime import datetime
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils

def _validate_and_enhance_requirements(raw_requirements:str) -> str:
    """Validate and enhance requirements using LangChain OpenAI"""

    llm_utils = LLMUtils()

    system_prompt = """
    You are an expert Business Analyst and Requirements Engineer. Your task is to analyze, validate, and enhance software requirements.
    
    Given raw requirements, you should:
    1. Identify and clarify any ambiguous or incomplete requirements
    2. Add missing functional and non-functional requirements
    3. Structure the requirements in a clear, professional format
    4. Add technical considerations and constraints
    5. Identify potential risks and dependencies
    6. Ensure requirements are testable and measurable
    
    Format your response as a comprehensive requirements document that includes:
    - Executive Summary
    - Functional Requirements
    - Non-Functional Requirements (Performance, Security, Scalability, etc.)
    - Technical Constraints
    - Dependencies and Assumptions
    - Success Criteria
    - Risk Assessment
    """

    user_prompt = f"""
    Please analyze and enahance the following raw requirements.

    {raw_requirements}
    Create a comprehensive, well-structured requirements document 
    that will serve as the foundation for the entire software development lifecycle.
    """

    try:
        enhanced_requirements = llm_utils.get_completion(system_prompt, user_prompt)
        print("🤖 Requirements enhanced using LangChain OpenAI")
        return enhanced_requirements
    
    except Exception as e:
        print(f"❌ Error enhancing requirements: {e}")
        return f"""
            REQUIREMENTS DOCUMENT (Fallback)
            ===============================

            Original Requirements:
            {raw_requirements}

            Note: Enhanced analysis unavailable due to API error.
            Please review and enhance manually before proceeding.
        """
    

def ui_user_inputs_requirements(state: SDLCState) -> SDLCState:
    """
    Node 1: Capture and validate user input requirements
    """
    print("🚀 Starting SDLC Workflow - Capturing Requirements")
    
    # Validate and enhance requirements using OpenAI
    enhanced_requirements = _validate_and_enhance_requirements(state["requirements"])
    
    # Update state
    updated_state = {
        **state,
        "requirements": enhanced_requirements,
        "current_stage": "requirements_captured",
        "timestamp": datetime.now().isoformat(),
        "iteration_count": 0,
        "approval_status": "pending"
    }
    
    print(f"✅ Requirements captured and validated")
    return updated_state