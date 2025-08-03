from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state.sdlc_state import SDLCState
from nodes.requirements_node import ui_user_inputs_requirements
from nodes.user_stories_node import auto_generate_user_stories
from nodes.product_owner_review_node import product_owner_review, revise_user_stories, route_after_po_review

def create_proper_interrupt_workflow():
    """Create SDLC workflow using proper LangGraph interrupt pattern"""
    
    # Initialize the graph
    workflow = StateGraph(SDLCState)
    
    # Add ALL nodes to the graph
    workflow.add_node("ui_user_inputs_requirements", ui_user_inputs_requirements)
    workflow.add_node("auto_generate_user_stories", auto_generate_user_stories)
    workflow.add_node("product_owner_review", product_owner_review)
    workflow.add_node("revise_user_stories", revise_user_stories)
    
    # Set entry point
    workflow.set_entry_point("ui_user_inputs_requirements")
    
    # Add edges - complete workflow structure
    workflow.add_edge("ui_user_inputs_requirements", "auto_generate_user_stories")
    workflow.add_edge("auto_generate_user_stories", "product_owner_review")
    
    # Add conditional routing after PO review
    workflow.add_conditional_edges(
        "product_owner_review",
        route_after_po_review,
        {
            "create_design_documents": END,  # Approved - go to design
            "revise_user_stories": "revise_user_stories"  # Needs revision
        }
    )

    workflow.add_edge("revise_user_stories", "product_owner_review")
    
    # Compile with interrupt BEFORE product_owner_review
    compiled_workflow = workflow.compile(
        interrupt_before=["product_owner_review"],
        checkpointer= MemorySaver()
    )
    
    print("[TOOLS] Proper LangGraph interrupt workflow created")
    print("🛑 Will pause BEFORE product_owner_review node")
    print("💡 Use workflow.update_state() to modify review behavior")
    
    return compiled_workflow