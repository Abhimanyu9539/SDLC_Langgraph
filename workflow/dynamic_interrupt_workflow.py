# ==================== UPDATED DYNAMIC INTERRUPT WORKFLOW ====================
# File: workflow/dynamic_interrupt_workflow.py

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state.sdlc_state import SDLCState
from nodes.requirements_node import ui_user_inputs_requirements
from nodes.user_stories_node import auto_generate_user_stories
from nodes.dynamic_review_node import (
    product_owner_review_dynamic, 
    revise_user_stories_dynamic, 
    route_after_po_review_dynamic
)
from nodes.design_documents_node import create_design_documents
from nodes.design_review_node import (
    design_review_dynamic,
    revise_design_documents_dynamic,
    route_after_design_review_dynamic
)

from nodes.generate_code_node import generate_code
from nodes.code_review_node import (
    code_review_dynamic,
    route_after_code_review_dynamic
)
from nodes.fix_code_after_review_node import fix_code_after_review_dynamic

def create_dynamic_interrupt_workflow():
    """
    Create SDLC workflow using DYNAMIC INTERRUPTS (Official LangGraph Pattern)
    Updated to include Design Documents creation and Design Review
    
    Complete workflow flow:
    Requirements → User Stories → PO Review → Design Documents → Design Review → (Future: Code Generation)
    
    Key differences from static interrupts:
    - No interrupt_before/interrupt_after in compile()
    - interrupt() calls INSIDE the nodes
    - Resume with Command(resume=value)
    - Cleaner, more modern approach
    """
    
    # Initialize the graph
    workflow = StateGraph(SDLCState)
    
    # Add ALL nodes to the graph
    workflow.add_node("ui_user_inputs_requirements", ui_user_inputs_requirements)
    workflow.add_node("auto_generate_user_stories", auto_generate_user_stories)
    workflow.add_node("product_owner_review", product_owner_review_dynamic)  # ← Uses interrupt() inside
    workflow.add_node("revise_user_stories", revise_user_stories_dynamic)
    workflow.add_node("create_design_documents", create_design_documents)  # ← NEW: Design docs generation (no interrupts)
    workflow.add_node("design_review", design_review_dynamic)  # ← NEW: Design review with interrupts
    workflow.add_node("revise_design_documents", revise_design_documents_dynamic)  # ← NEW: Design revision
    workflow.add_node("generate_code", generate_code)
    workflow.add_node("code_review", code_review_dynamic)
    workflow.add_node("fix_code_after_review", fix_code_after_review_dynamic)

    # Set entry point
    workflow.set_entry_point("ui_user_inputs_requirements")
    
    # Add edges - complete workflow structure
    workflow.add_edge("ui_user_inputs_requirements", "auto_generate_user_stories")
    workflow.add_edge("auto_generate_user_stories", "product_owner_review")
    
    # Add conditional routing after PO review
    workflow.add_conditional_edges(
        "product_owner_review",
        route_after_po_review_dynamic,
        {
            "create_design_documents": "create_design_documents",  # Approved - go to design
            "revise_user_stories": "revise_user_stories"  # Needs revision
        }
    )

    # Route back to PO review after user story revision (for iteration cycles)
    workflow.add_edge("revise_user_stories", "product_owner_review")
    
    # Design documents flow
    workflow.add_edge("create_design_documents", "design_review")
    
    # Add conditional routing after design review
    workflow.add_conditional_edges(
        "design_review",
        route_after_design_review_dynamic,
        {
            "generate_code": "generate_code",  # Approved - end for now (future: go to code generation)
            "revise_design_documents": "revise_design_documents"  # Needs revision
        }
    )
    
    # Route back to design review after design revision (for iteration cycles)
    workflow.add_edge("revise_design_documents", "design_review")

    # Code generation flow
    workflow.add_edge("generate_code", "code_review")
    workflow.add_conditional_edges(
        "code_review",
        route_after_code_review_dynamic,
        {
            "security_review": END,  # Approved - end for now
            "fix_code_after_review": "fix_code_after_review"  # Needs revision
        }
    
    )
    workflow.add_edge("fix_code_after_review", "code_review")
    
    # ⭐ COMPILE WITHOUT interrupt_before - interrupts are INSIDE nodes
    compiled_workflow = workflow.compile(
        checkpointer=MemorySaver()  # Only checkpointer needed
    )
    
    print("🔧 Dynamic LangGraph interrupt workflow created")
    print("🎯 Uses interrupt() INSIDE nodes (official pattern)")
    print("⚡ Resume with Command(resume=value)")
    print("🆕 Now includes:")
    print("   • Product Owner Review (with interrupts)")
    print("   • Design Documents Creation (generation only)")
    print("   • Design Review (with interrupts)")
    print("   • User Story & Design Document revision cycles")
    
    return compiled_workflow