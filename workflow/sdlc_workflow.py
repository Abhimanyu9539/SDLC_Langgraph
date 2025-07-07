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

# ==================== main.py ====================
import asyncio
from state.sdlc_state import SDLCState
from workflow.sdlc_workflow import create_sdlc_workflow

async def run_sdlc_workflow():
    """Example of running the SDLC workflow"""
    
    # Create the workflow
    workflow = create_sdlc_workflow()
    
    # Initial state
    initial_state = SDLCState(
        requirements="Build a user authentication system with dashboard for managing customer data",
        user_stories=[],
        design_docs={},
        code={},
        test_cases=[],
        review_feedback={},
        approval_status="",
        current_stage="initial",
        iteration_count=0,
        project_id="PROJ-001",
        timestamp="",
        stakeholders=["Product Owner", "Tech Lead", "QA Lead"],
        security_scan_results={},
        test_results={},
        deployment_status=""
    )
    
    # Run the workflow
    print("🚀 Starting SDLC Workflow...")
    result = await workflow.ainvoke(initial_state)
    
    print("\n" + "="*60)
    print("WORKFLOW RESULTS")
    print("="*60)
    print(f"Current Stage: {result['current_stage']}")
    print(f"User Stories Generated: {len(result['user_stories'])}")
    
    for story in result['user_stories']:
        print(f"- {story['id']}: {story['title']} (Priority: {story['priority']})")
    
    return result

if __name__ == "__main__":
    asyncio.run(run_sdlc_workflow())