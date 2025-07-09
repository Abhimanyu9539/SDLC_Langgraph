from langgraph.graph import StateGraph, END
from state.sdlc_state import SDLCState
from nodes.requirements_node import ui_user_inputs_requirements
from nodes.user_stories_node import auto_generate_user_stories
from nodes.product_owner_review_node import product_owner_review, revise_user_stories, route_after_po_review

def create_sdlc_workflow():
    """Create and configure the LangGraph workflow for SDLC"""
    
    # Initialize the graph
    workflow = StateGraph(SDLCState)
    
    # Add nodes to the graph
    workflow.add_node("ui_user_inputs_requirements", ui_user_inputs_requirements)
    workflow.add_node("auto_generate_user_stories", auto_generate_user_stories)
    workflow.add_node("product_owner_review", product_owner_review)
    workflow.add_node("revise_user_stories", revise_user_stories)
    
    # Set entry point
    workflow.set_entry_point("ui_user_inputs_requirements")
    
    # Add edges (workflow flow)
    workflow.add_edge("ui_user_inputs_requirements", "auto_generate_user_stories")
    workflow.add_edge("auto_generate_user_stories", "product_owner_review")

    # Add conditional edge for PO Review routing
    workflow.add_conditional_edges(
        "product_owner_review", 
        route_after_po_review,
        {
            "create_design_documents": END, 
            "revise_user_stories": "revise_user_stories"
        }
    )
    
    # Route back to PO review after revision
    workflow.add_edge("revise_user_stories", "product_owner_review")
    
    
    # Compile the workflow
    compiled_workflow = workflow.compile()
    
    print("🔧 LangGraph workflow created")
    return compiled_workflow

