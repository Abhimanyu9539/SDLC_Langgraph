from langgraph.graph import StateGraph, END
from state.sdlc_state import SDLCState
from nodes.requirements_node import ui_user_inputs_requirements
from nodes.user_stories_node import auto_generate_user_stories

def create_sdlc_workflow():
    """Create and configure the LangGraph workflow for SDLC"""
    
    # Initialize the graph
    workflow = StateGraph(SDLCState)
    
    # Add nodes to the graph
    workflow.add_node("ui_user_inputs_requirements", ui_user_inputs_requirements)
    workflow.add_node("auto_generate_user_stories", auto_generate_user_stories)
    
    # Set entry point
    workflow.set_entry_point("ui_user_inputs_requirements")
    
    # Add edges (workflow flow)
    workflow.add_edge("ui_user_inputs_requirements", "auto_generate_user_stories")
    
    # For now, end after user stories (we'll add more nodes later)
    workflow.add_edge("auto_generate_user_stories", END)
    
    # Compile the workflow
    compiled_workflow = workflow.compile()
    
    print("🔧 LangGraph workflow created with 2 nodes")
    return compiled_workflow

