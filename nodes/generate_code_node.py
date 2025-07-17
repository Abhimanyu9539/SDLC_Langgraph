# ==================== GENERATE CODE NODE ====================
# File: nodes/generate_code_node.py

from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def generate_code(state: SDLCState) -> SDLCState:
    """
    Generate Code based on approved design documents
    
    This node generates code implementation based on:
    - Approved design documents
    - Original requirements
    - User stories
    
    Similar to design document generation - just creates and stores the code
    """
    
    print("\n💻 Generating Code Implementation")
    
    design_docs = state.get("design_docs", {})
    user_stories = state.get("user_stories", [])
    requirements = state.get("requirements", "")
    
    if not design_docs:
        print("⚠️ No approved design documents found - cannot generate code")
        return {
            **state,
            "current_stage": "code_generation_failed",
            "timestamp": datetime.now().isoformat()
        }
    
    print(f"📚 Generating code based on design documents and {len(user_stories)} user stories...")
    
    # Generate code using AI
    generated_code = _generate_code_implementation(requirements, user_stories, design_docs)
    
    # Update state with generated code
    updated_state = {
        **state,
        "code": generated_code,
        "current_stage": "code_generated",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"✅ Code generated successfully")
    print(f"📄 Generated {len(generated_code)} code modules")
    
    return updated_state

def _generate_code_implementation(requirements: str, user_stories: List[Dict[str, Any]], design_docs: Dict[str, Any]) -> Dict[str, Any]:
    """Generate code implementation using AI based on design documents"""
    
    llm_utils = LLMUtils()
    
    # Format user stories for AI processing
    stories_summary = []
    for story in user_stories:
        story_text = f"""
        ID: {story.get('id', 'N/A')}
        Title: {story.get('title', 'N/A')}
        Description: {story.get('description', 'N/A')}
        Acceptance Criteria: {story.get('acceptance_criteria', [])}
        Priority: {story.get('priority', 'N/A')}
        """
        stories_summary.append(story_text.strip())
    
    stories_text = "\n" + "="*50 + "\n".join(stories_summary)
    
    # Format design documents for AI processing
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
    """
    
    system_prompt = """
    You are a Senior Software Developer and Technical Lead. Generate a comprehensive code implementation based on the design documents, requirements, and user stories provided.
    
    Your code implementation should include key modules and components but be practical and focused. Generate code that:
    
    1. BACKEND IMPLEMENTATION
       - Core API endpoints and business logic
       - Database models and schema implementation
       - Authentication and authorization logic
       - Key service classes and utilities
    
    2. FRONTEND IMPLEMENTATION
       - Main application components
       - Key UI components and layouts
       - State management and API integration
       - Routing and navigation
    
    3. DATABASE IMPLEMENTATION
       - Database schema/migration scripts
       - Model definitions
       - Key queries and operations
    
    4. CONFIGURATION & SETUP
       - Application configuration
       - Environment setup
       - Dependencies and requirements
    
    5. TESTING FRAMEWORK
       - Basic test structure
       - Key test cases framework
       - Testing utilities
    
    Return as JSON with this structure:
    {
        "summary": "Overview of the generated code implementation",
        "technology_stack": {
            "backend": "Backend technology and key frameworks",
            "frontend": "Frontend technology and key frameworks",
            "database": "Database technology and setup",
            "testing": "Testing framework and approach"
        },
        "backend_code": {
            "api_endpoints": "Core API implementation code",
            "business_logic": "Main business logic and services",
            "database_models": "Database model definitions",
            "authentication": "Authentication and authorization code",
            "utilities": "Utility functions and helpers"
        },
        "frontend_code": {
            "main_components": "Primary application components",
            "ui_components": "Reusable UI components",
            "state_management": "State management implementation",
            "routing": "Application routing setup",
            "api_integration": "API integration and data fetching"
        },
        "database_code": {
            "schema_migration": "Database schema and migration scripts",
            "models": "Database model implementations",
            "queries": "Key database queries and operations",
            "indexes": "Database indexes and optimizations"
        },
        "configuration": {
            "app_config": "Application configuration files",
            "environment": "Environment setup and variables",
            "dependencies": "Dependencies and requirements",
            "deployment": "Deployment configuration"
        },
        "testing_code": {
            "test_structure": "Testing framework setup",
            "unit_tests": "Key unit test implementations",
            "integration_tests": "Integration test examples",
            "test_utilities": "Testing utilities and helpers"
        },
        "implementation_notes": "Key implementation details and next steps"
    }
    
    Keep the code comprehensive but practical. Focus on the core functionality that addresses the user stories.
    Generate actual code snippets where appropriate, but keep them concise due to token limitations.
    """
    
    user_prompt = f"""
    Generate a comprehensive code implementation for this project:
    
    REQUIREMENTS:
    {requirements}
    
    USER STORIES:
    {stories_text}
    
    DESIGN DOCUMENTS:
    {design_text}
    
    Focus on creating practical, implementable code that addresses all user stories and follows the design specifications.
    Ensure the code is well-structured, follows best practices, and provides a solid foundation for development.
    """
    
    try:
        print("🔧 Generating code implementation...")
        code_implementation = llm_utils.get_json_completion(system_prompt, user_prompt)
        print("✅ Code implementation generated successfully")
        return code_implementation
        
    except Exception as e:
        print(f"❌ Error generating code implementation: {e}")
        return _generate_fallback_code_implementation()

def _generate_fallback_code_implementation() -> Dict[str, Any]:
    """Generate fallback code implementation when AI generation fails"""
    
    return {
        "summary": "Basic code implementation structure (Fallback) - requires manual completion",
        "technology_stack": {
            "backend": "Node.js/Express or Python/FastAPI for API development",
            "frontend": "React/Vue.js for user interface",
            "database": "PostgreSQL/MongoDB for data persistence",
            "testing": "Jest/Pytest for testing framework"
        },
        "backend_code": {
            "api_endpoints": "// TODO: Implement REST API endpoints based on design\n// GET /api/users, POST /api/auth, etc.",
            "business_logic": "// TODO: Implement core business logic services\n// UserService, AuthService, etc.",
            "database_models": "// TODO: Define database models\n// User, Session, ApplicationData models",
            "authentication": "// TODO: Implement JWT-based authentication\n// login, register, token validation",
            "utilities": "// TODO: Implement utility functions\n// validation, logging, error handling"
        },
        "frontend_code": {
            "main_components": "// TODO: Implement main application components\n// App, Dashboard, LoginForm",
            "ui_components": "// TODO: Create reusable UI components\n// Button, Input, Modal, etc.",
            "state_management": "// TODO: Implement state management\n// Redux/Vuex or Context API",
            "routing": "// TODO: Set up application routing\n// React Router or Vue Router",
            "api_integration": "// TODO: Implement API integration\n// axios/fetch for API calls"
        },
        "database_code": {
            "schema_migration": "-- TODO: Create database schema migration\n-- CREATE TABLE users, sessions, etc.",
            "models": "// TODO: Implement database models\n// ORM model definitions",
            "queries": "-- TODO: Implement key database queries\n-- SELECT, INSERT, UPDATE operations",
            "indexes": "-- TODO: Create database indexes\n-- CREATE INDEX for performance"
        },
        "configuration": {
            "app_config": "// TODO: Application configuration\n// config.js, settings.json",
            "environment": "// TODO: Environment variables\n// .env file setup",
            "dependencies": "// TODO: Dependencies list\n// package.json, requirements.txt",
            "deployment": "// TODO: Deployment configuration\n// Dockerfile, docker-compose.yml"
        },
        "testing_code": {
            "test_structure": "// TODO: Testing framework setup\n// Jest config, test directory structure",
            "unit_tests": "// TODO: Unit test implementations\n// test user service, auth service",
            "integration_tests": "// TODO: Integration test examples\n// API endpoint tests",
            "test_utilities": "// TODO: Testing utilities\n// test helpers, mock data"
        },
        "implementation_notes": "This is a fallback code implementation structure. Please review and implement manually based on the design documents and requirements."
    }