# ==================== UPDATED STATE FOR DYNAMIC INTERRUPTS ====================
# File: state/sdlc_state.py (Updated)

from typing import TypedDict, List, Dict, Any

class SDLCState(TypedDict):
    """
    Complete state structure for the SDLC workflow
    Updated for dynamic interrupt pattern
    """
    
    # ===== CORE DATA =====
    requirements: str
    user_stories: List[Dict[str, Any]]
    design_docs: Dict[str, Any]
    code: Dict[str, str]
    test_cases: List[Dict[str, Any]]
    
    # ===== REVIEW AND FEEDBACK =====
    review_feedback: Dict[str, Any]
    approval_status: str
    current_stage: str
    iteration_count: int
    
    # ===== NEW: ENHANCED REVIEW HISTORY =====
    review_history: List[Dict[str, Any]]  # Complete history of all reviews
    
    # ===== METADATA =====
    project_id: str
    timestamp: str
    stakeholders: List[str]
    
    # ===== QUALITY GATES =====
    security_scan_results: Dict[str, Any]
    test_results: Dict[str, Any]
    deployment_status: str

    # ===== LEGACY FIELDS (for backward compatibility) =====
    review_type: str  # Still used for compatibility
    human_review_requested: bool  # Still used for compatibility