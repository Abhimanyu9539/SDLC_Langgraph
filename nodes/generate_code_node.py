# ==================== SIMPLIFIED PYTHON-ONLY GENERATE CODE NODE ====================
# File: nodes/generate_code_node.py

from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings
import traceback

def generate_code(state: SDLCState) -> SDLCState:
    """
    Generate Python Code File based on approved design documents
    
    Simplified to generate only one Python implementation file
    """
    
    print("\n💻 Generating Python Code File")
    
    design_docs = state.get("design_docs", {})
    user_stories = state.get("user_stories", [])
    
    # Debug information
    print(f"🔍 DEBUG: Design docs available: {bool(design_docs)}")
    print(f"🔍 DEBUG: User stories count: {len(user_stories)}")
    
    if not design_docs:
        print("⚠️ No design documents found - cannot generate code")
        return {
            **state,
            "current_stage": "code_generation_failed",
            "timestamp": datetime.now().isoformat()
        }
    
    print(f"🐍 Generating Python implementation file...")
    
    # Generate single Python file
    python_code = _generate_python_implementation(user_stories, design_docs)
    
    # Create code dictionary with single file
    code_files = {
        "main.py": python_code
    }
    
    # Debug the results
    print(f"🔍 DEBUG: Generated Python file with {len(python_code)} characters")
    print(f"🔍 DEBUG: File preview: {python_code[:200]}...")
    
    # Update state with generated code
    updated_state = {
        **state,
        "code": code_files,
        "current_stage": "code_generated",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"✅ Python code file generated successfully")
    print(f"📄 Generated main.py with implementation")
    
    return updated_state

def _generate_python_implementation(user_stories: List[Dict[str, Any]], design_docs: Dict[str, Any]) -> str:
    """Generate a single Python implementation file using LLM"""
    
    llm_utils = LLMUtils()
    
    # Extract key user stories for context
    stories_text = _format_user_stories_for_python(user_stories[:settings.MAX_USER_STORIES])
    
    # Extract design information
    design_summary = _extract_design_summary(design_docs)
    
    # System prompt for Python code generation
    system_prompt = """
    You are an experienced Python Developer. Generate a complete, working Python application based on the provided design specifications and user stories.
    
    REQUIREMENTS:
    1. Create a single, comprehensive Python file (main.py)
    2. Include all necessary imports at the top
    3. Implement classes and functions to fulfill the user stories
    4. Add proper error handling and logging
    5. Include docstrings for classes and main functions
    6. Use Python best practices and PEP 8 style
    7. Make the code functional and executable
    8. Include a main() function and if __name__ == "__main__" block
    
    STRUCTURE YOUR CODE:
    - Imports
    - Constants/Configuration
    - Classes (if needed)
    - Functions
    - Main execution block
    
    FOCUS ON:
    - Implementing the core functionality described in user stories
    - Clean, readable, maintainable code
    - Proper error handling
    - Basic logging/print statements for debugging
    
    Return ONLY the Python code, no explanations or markdown formatting.
    """
    
    user_prompt = f"""
    Generate a complete Python application that implements the following requirements:
    
    USER STORIES:
    {stories_text}
    
    DESIGN CONTEXT:
    {design_summary}
    
    Create a working Python file that implements the core functionality described in the user stories.
    Focus on creating a functional application that addresses the main requirements.
    """
    
    try:
        print("🤖 Generating Python code using LLM...")
        print(f"🔍 DEBUG: System prompt length: {len(system_prompt)}")
        print(f"🔍 DEBUG: User prompt length: {len(user_prompt)}")
        
        # Use get_completion instead of get_json_completion
        python_code = llm_utils.get_completion(system_prompt, user_prompt)
        
        # Clean up the response (remove markdown if present)
        python_code = _clean_python_code_response(python_code)
        
        print(f"✅ Python code generated successfully")
        print(f"📏 Generated code length: {len(python_code)} characters")
        
        # Validate that we got actual Python code
        if len(python_code.strip()) < 50:
            print("⚠️ Generated code seems too short, using fallback")
            return _generate_fallback_python_code(design_summary)
        
        return python_code
        
    except Exception as e:
        print(f"❌ Error generating Python code: {e}")
        print(f"❌ Error type: {type(e)}")
        print(f"❌ Full traceback: {traceback.format_exc()}")
        
        print("🔄 Using fallback Python code generation...")
        return _generate_fallback_python_code(design_summary)

def _format_user_stories_for_python(user_stories: List[Dict[str, Any]]) -> str:
    """Format user stories for Python code generation"""
    
    if not user_stories:
        return "No specific user stories provided - create a basic application structure."
    
    formatted_stories = []
    
    for i, story in enumerate(user_stories, 1):
        story_text = f"""
        Story {i}: {story.get('title', 'Feature Implementation')}
        Description: {story.get('description', 'No description available')}
        
        Acceptance Criteria:
        """
        
        criteria = story.get('acceptance_criteria', [])
        if criteria:
            for j, criterion in enumerate(criteria, 1):
                story_text += f"        {j}. {criterion}\n"
        else:
            story_text += "        - Implement basic functionality as described\n"
        
        formatted_stories.append(story_text.strip())
    
    return "\n\n".join(formatted_stories)

def _extract_design_summary(design_docs: Dict[str, Any]) -> str:
    """Extract relevant design information for Python implementation"""
    
    if not design_docs:
        return "No specific design requirements - implement as a console application."
    
    summary_parts = []
    
    # Main summary
    main_summary = design_docs.get('summary', '')
    if main_summary:
        summary_parts.append(f"Overview: {main_summary}")
    
    # System architecture
    sys_arch = design_docs.get('system_architecture', {})
    if sys_arch:
        overview = sys_arch.get('overview', '')
        if overview:
            summary_parts.append(f"Architecture: {overview}")
        
        components = sys_arch.get('components', [])
        if components:
            summary_parts.append(f"Components: {', '.join(components)}")
    
    # Database design
    db_design = design_docs.get('database_design', {})
    if db_design:
        entities = db_design.get('entities', [])
        if entities:
            summary_parts.append(f"Data Entities: {', '.join(entities)}")
    
    # API design
    api_design = design_docs.get('api_design', {})
    if api_design:
        overview = api_design.get('overview', '')
        if overview:
            summary_parts.append(f"API Approach: {overview}")
    
    # Implementation notes
    impl_notes = design_docs.get('implementation_notes', '')
    if impl_notes:
        summary_parts.append(f"Implementation Notes: {impl_notes}")
    
    if summary_parts:
        return "\n".join(summary_parts)
    else:
        return "Implement as a Python console application with appropriate classes and functions."

def _clean_python_code_response(response: str) -> str:
    """Clean up LLM response to extract just the Python code"""
    
    # Remove markdown code blocks if present
    if "```python" in response:
        # Extract content between ```python and ```
        start_marker = "```python"
        end_marker = "```"
        
        start_idx = response.find(start_marker)
        if start_idx != -1:
            start_idx += len(start_marker)
            end_idx = response.find(end_marker, start_idx)
            if end_idx != -1:
                response = response[start_idx:end_idx].strip()
    
    elif "```" in response:
        # Extract content between ``` blocks
        parts = response.split("```")
        if len(parts) >= 3:
            response = parts[1].strip()
    
    # Remove any leading/trailing whitespace
    response = response.strip()
    
    return response

def _generate_fallback_python_code(design_summary: str) -> str:
    """Generate basic fallback Python code when LLM generation fails"""
    
    fallback_code = '''#!/usr/bin/env python3
"""
Generated Application - Fallback Implementation

This is a basic Python application structure created when
the main code generation process encountered issues.

Please review and enhance this code based on your requirements.
"""

import logging
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Application:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.name = "Generated Application"
        self.version = "1.0.0"
        self.created_at = datetime.now()
        logger.info(f"Initializing {self.name} v{self.version}")
    
    def run(self):
        """Main application logic"""
        try:
            logger.info("Starting application...")
            
            # TODO: Implement main application logic here
            # Based on design requirements and user stories
            
            self.display_welcome()
            self.process_main_functionality()
            
            logger.info("Application completed successfully")
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise
    
    def display_welcome(self):
        """Display welcome message"""
        print(f"Welcome to {self.name} v{self.version}")
        print(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
    
    def process_main_functionality(self):
        """Implement main business logic"""
        # TODO: Replace with actual implementation
        # based on user stories and design requirements
        
        print("Processing main functionality...")
        
        # Example placeholder operations
        data = self.load_data()
        results = self.process_data(data)
        self.save_results(results)
        
        print("Main functionality completed")
    
    def load_data(self) -> List[Dict[str, Any]]:
        """Load application data"""
        # TODO: Implement data loading logic
        logger.info("Loading data...")
        return [{"id": 1, "name": "Sample Data"}]
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process the loaded data"""
        # TODO: Implement data processing logic
        logger.info(f"Processing {len(data)} data items...")
        return data
    
    def save_results(self, results: List[Dict[str, Any]]):
        """Save processing results"""
        # TODO: Implement result saving logic
        logger.info(f"Saving {len(results)} results...")

def main():
    """Main entry point"""
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print("\\nApplication interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
'''
    
    return fallback_code