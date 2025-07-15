# ==================== DYNAMIC INTERRUPT WORKFLOW ====================
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

def create_dynamic_interrupt_workflow():
    """
    Create SDLC workflow using DYNAMIC INTERRUPTS (Official LangGraph Pattern)
    
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
    workflow.add_node("create_design_documents", create_design_documents)
    
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

    # Route back to PO review after revision (for iteration cycles)
    workflow.add_edge("revise_user_stories", "product_owner_review")
    workflow.add_edge("create_design_documents", END)
    
    # ⭐ COMPILE WITHOUT interrupt_before - interrupts are INSIDE nodes
    compiled_workflow = workflow.compile(
        checkpointer=MemorySaver()  # Only checkpointer needed
    )
    
    print("🔧 Dynamic LangGraph interrupt workflow created")
    print("🎯 Uses interrupt() INSIDE nodes (official pattern)")
    print("⚡ Resume with Command(resume=value)")
    
    return compiled_workflow