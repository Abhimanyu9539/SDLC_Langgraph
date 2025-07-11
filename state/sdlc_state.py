from typing import TypedDict, List, Dict, Any

class SDLCState(TypedDict):
    """Complete state structure for the SDLC workflow"""
    # Core Data
    requirements: str
    user_stories: List[Dict[str, Any]]
    design_docs: Dict[str, Any]
    code: Dict[str, str]
    test_cases: List[Dict[str, Any]]
    
    # Review and Feedback
    review_feedback: Dict[str, Any]
    approval_status: str
    current_stage: str
    iteration_count: int
    
    # Metadata
    project_id: str
    timestamp: str
    stakeholders: List[str]
    
    # Quality Gates
    security_scan_results: Dict[str, Any]
    test_results: Dict[str, Any]
    deployment_status: str

    review_type: str  # "human", "ai", "auto" 
    human_review_requested: bool  # Flag for human review