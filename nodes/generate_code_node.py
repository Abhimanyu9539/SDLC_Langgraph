# ==================== FLEXIBLE GENERATE CODE NODE ====================
# File: nodes/generate_code_node.py

from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def generate_code(state: SDLCState) -> SDLCState:
    """
    Generate Code Files based on approved design documents
    
    Flexible approach: Generate code based on what's actually specified in design
    No assumptions about technology stack or architecture
    """
    
    print("\n💻 Generating Code Files")
    
    design_docs = state.get("design_docs", {})
    user_stories = state.get("user_stories", [])
    
    if not design_docs:
        print("⚠️ No design documents found - cannot generate code")
        return {
            **state,
            "current_stage": "code_generation_failed",
            "timestamp": datetime.now().isoformat()
        }
    
    print(f"📚 Generating code files based on design specifications...")
    
    # Generate code files based on actual design
    code_files = _generate_flexible_code_files(user_stories, design_docs)
    
    # Update state with generated code
    updated_state = {
        **state,
        "code": code_files,
        "current_stage": "code_generated",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"✅ Code files generated successfully")
    print(f"📄 Generated {len(code_files)} code files")
    
    return updated_state

def _generate_flexible_code_files(user_stories: List[Dict[str, Any]], design_docs: Dict[str, Any]) -> Dict[str, str]:
    """Generate code files based on actual design specifications"""
    
    llm_utils = LLMUtils()
    
    # Extract key user stories (limit to manage context)
    key_stories = []
    for story in user_stories[:settings.MAX_USER_STORIES]:
        story_summary = {
            "title": story.get('title', 'Feature'),
            "description": story.get('description', '')[:120],
            "acceptance_criteria": story.get('acceptance_criteria', [])[:2]
        }
        key_stories.append(story_summary)
    
    # Extract what's actually specified in design
    design_summary = _extract_design_essentials(design_docs)
    
    system_prompt = """
    You are a developer. Generate practical code files based on the design specifications provided.
    
    IMPORTANT RULES:
    1. Use ONLY the technology stack specified in the design documents
    2. Generate code files that match the architecture described
    3. Don't assume frontend/backend split unless specified
    4. Generate 3-6 essential code files based on what's actually needed
    5. Keep each file focused and practical (30-100 lines)
    6. Use appropriate file extensions based on the specified technology
    
    If the design specifies:
    - Python: Generate .py files
    - JavaScript/Node: Generate .js files
    - React: Generate .jsx files
    - Vue: Generate .vue files
    - PHP: Generate .php files
    - Java: Generate .java files
    - Simple web app: Generate .html, .css, .js files
    
    Return as JSON with filename: code_content pairs.
    Generate only what's needed based on the design specifications.
    """
    
    user_prompt = f"""
    Generate code files for this application based on the design specifications:
    
    USER STORIES TO IMPLEMENT:
    {key_stories}
    
    DESIGN SPECIFICATIONS:
    {design_summary}
    
    Generate practical, working code files that implement the core functionality.
    Use the exact technology stack and architecture specified in the design.
    Focus on the essential files needed to implement the user stories.
    """
    
    try:
        print("🔧 Generating code files based on design specifications...")
        code_files = llm_utils.get_json_completion(system_prompt, user_prompt)
        print("✅ Code files generated")
        
        if isinstance(code_files, dict) and len(code_files) > 0:
            return code_files
        else:
            print("⚠️ Invalid code generation response, using fallback")
            return _generate_fallback_code_files(design_summary)
        
    except Exception as e:
        print(f"❌ Error generating code: {e}")
        return _generate_fallback_code_files(design_summary)

def _extract_design_essentials(design_docs: Dict[str, Any]) -> str:
    """Extract essential design information for code generation"""
    
    # Get system architecture info
    system_arch = design_docs.get('system_architecture', {})
    tech_stack = system_arch.get('technology_stack', {})
    components = system_arch.get('components', [])
    
    # Get API design info
    api_design = design_docs.get('api_design', {})
    api_overview = api_design.get('overview', '')
    
    # Get database design info
    db_design = design_docs.get('database_design', {})
    db_entities = db_design.get('entities', [])
    
    # Get UI design info
    ui_design = design_docs.get('ui_design', {})
    ui_overview = ui_design.get('overview', '')
    
    # Format the essential information
    design_summary = f"""
    TECHNOLOGY STACK:
    {tech_stack}
    
    SYSTEM COMPONENTS:
    {components}
    
    API DESIGN:
    {api_overview}
    
    DATABASE ENTITIES:
    {db_entities}
    
    UI APPROACH:
    {ui_overview}
    """
    
    return design_summary.strip()

def _generate_fallback_code_files(design_summary: str) -> Dict[str, str]:
    """Generate simple fallback when code generation fails"""
    
    return {
        "README.md": """# Code Generation Failed

Code generation was not successful. Please try again.

## What to do:
1. Check that design documents are complete
2. Verify technology stack is clearly specified
3. Ensure user stories provide enough detail
4. Try running the code generation again

## Manual Implementation:
If code generation continues to fail, you can implement manually based on:
- Design documents in the previous step
- User stories requirements
- Technology stack specified in design

Try again with code generation or proceed with manual implementation."""
    }