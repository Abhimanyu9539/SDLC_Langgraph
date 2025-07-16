# ==================== DESIGN DOCUMENTS NODE ====================
# File: nodes/design_documents_node.py

from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def create_design_documents(state: SDLCState) -> SDLCState:
    """
    Create Design Documents (Functional and Technical)
    
    This node generates comprehensive design documentation based on:
    - Approved user stories
    - Original requirements
    
    Similar to user story generation - just creates and stores the documents
    """
    
    print("\n🎨 Creating Design Documents - Functional and Technical")
    
    user_stories = state.get("user_stories", [])
    requirements = state.get("requirements", "")
    
    if not user_stories:
        print("⚠️ No approved user stories found - cannot create design documents")
        return {
            **state,
            "current_stage": "design_documents_failed",
            "timestamp": datetime.now().isoformat()
        }
    
    print(f"📚 Creating design documents for {len(user_stories)} user stories...")
    
    # Generate consolidated design document using AI
    design_docs = _generate_consolidated_design_document(requirements, user_stories)
    
    # Update state with design documents
    updated_state = {
        **state,
        "design_docs": design_docs,
        "current_stage": "design_documents_created",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"✅ Design documents created successfully")
    print(f"📄 Generated consolidated design document")
    
    return updated_state

def _generate_consolidated_design_document(requirements: str, user_stories: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a single consolidated design document using AI"""
    
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
    
    system_prompt = """
    You are a Senior Software Architect and Technical Lead. Create a comprehensive, consolidated design document.
    
    Your design document should include all essential technical specifications in one cohesive document:
    
    1. SYSTEM ARCHITECTURE
       - High-level system overview
       - Component architecture and relationships
       - Technology stack recommendations
       - Integration points
    
    2. DATABASE DESIGN
       - Entity relationships and data model
       - Key tables and their relationships
       - Data validation and constraints
    
    3. API DESIGN
       - Core API endpoints and methods
       - Authentication and authorization approach
       - Request/response patterns
    
    4. USER INTERFACE DESIGN
       - Key pages/screens and navigation flow
       - Component hierarchy and interactions
       - Responsive design considerations
    
    5. SECURITY & PERFORMANCE
       - Security measures and protocols
       - Performance optimization strategies
       - Monitoring and logging approach
    
    Return as JSON with this structure:
    {
        "title": "Technical Design Document",
        "summary": "Executive summary of the design",
        "system_architecture": {
            "overview": "High-level system description",
            "components": ["List of main system components"],
            "technology_stack": {
                "frontend": "Frontend technology choice and rationale",
                "backend": "Backend technology choice and rationale",
                "database": "Database choice and rationale",
                "infrastructure": "Infrastructure and deployment approach"
            },
            "integration_points": ["Key system integrations"]
        },
        "database_design": {
            "overview": "Database design approach",
            "entities": ["Core data entities"],
            "relationships": "Key entity relationships",
            "considerations": "Performance and scaling considerations"
        },
        "api_design": {
            "overview": "API design approach",
            "authentication": "Authentication strategy",
            "core_endpoints": ["Main API endpoints"],
            "patterns": "Request/response patterns and conventions"
        },
        "ui_design": {
            "overview": "User interface design approach",
            "navigation": "Navigation structure",
            "key_pages": ["Main application pages"],
            "responsive_strategy": "Mobile and desktop considerations"
        },
        "security_performance": {
            "security_measures": ["Key security implementations"],
            "performance_strategy": "Performance optimization approach",
            "monitoring": "Monitoring and observability strategy"
        },
        "implementation_notes": "Key implementation considerations and next steps"
    }
    
    Keep the design comprehensive but concise to manage token usage effectively.
    Focus on the most critical design decisions and technical specifications.
    """
    
    user_prompt = f"""
    Create a comprehensive technical design document for this project:
    
    REQUIREMENTS:
    {requirements}
    
    USER STORIES:
    {stories_text}
    
    Focus on creating a practical, implementable design that addresses all user stories and requirements.
    Ensure the design is technically sound and provides clear guidance for development.
    """
    
    try:
        print("🔧 Generating consolidated design document...")
        design_doc = llm_utils.get_json_completion(system_prompt, user_prompt)
        print("✅ Design document generated successfully")
        return design_doc
        
    except Exception as e:
        print(f"❌ Error generating design document: {e}")
        return _generate_fallback_design_document()

def _generate_fallback_design_document() -> Dict[str, Any]:
    """Generate fallback design document when AI generation fails"""
    
    return {
        "title": "Technical Design Document (Fallback)",
        "summary": "Basic design document generated due to AI processing error - requires manual completion",
        "system_architecture": {
            "overview": "Modern web application with separated frontend and backend",
            "components": ["Frontend Application", "Backend API", "Database", "Authentication Service"],
            "technology_stack": {
                "frontend": "React/Vue.js for responsive user interface",
                "backend": "Node.js/Python for API development",
                "database": "PostgreSQL/MongoDB for data persistence",
                "infrastructure": "Docker containers with cloud deployment"
            },
            "integration_points": ["Frontend-Backend API", "Authentication Service", "External APIs"]
        },
        "database_design": {
            "overview": "Relational database design with normalized tables",
            "entities": ["Users", "Sessions", "Application Data", "Audit Logs"],
            "relationships": "Standard user-data relationships with proper foreign keys",
            "considerations": "Indexing for performance, backup strategies"
        },
        "api_design": {
            "overview": "RESTful API with standard HTTP methods",
            "authentication": "JWT-based authentication with role-based access",
            "core_endpoints": ["Authentication", "User Management", "Data CRUD Operations"],
            "patterns": "Standard REST patterns with consistent error handling"
        },
        "ui_design": {
            "overview": "Responsive web interface with intuitive navigation",
            "navigation": "Header navigation with sidebar for main features",
            "key_pages": ["Login/Register", "Dashboard", "Main Application Views", "Settings"],
            "responsive_strategy": "Mobile-first design with progressive enhancement"
        },
        "security_performance": {
            "security_measures": ["Input validation", "Authentication", "HTTPS", "Data encryption"],
            "performance_strategy": "Caching, database optimization, CDN usage",
            "monitoring": "Application logging, performance metrics, error tracking"
        },
        "implementation_notes": "This is a fallback design document. Please review and enhance manually before proceeding to development."
    }