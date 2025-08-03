import asyncio
from typing import Dict, Any, Optional
from state.sdlc_state import SDLCState
from workflow.proper_interrupt_workflow import create_proper_interrupt_workflow
from utils.simple_review_handler import ask_review_choice, handle_review_choice
from datetime import datetime

class ProperWorkflowRunner:
    """Proper LangGraph interrupt workflow runner following official documentation"""
    
    def __init__(self):
        self.workflow = create_proper_interrupt_workflow()
        self.config = {"configurable": {"thread_id": "1"}}  # Thread for state tracking
    
    async def   run_workflow_with_interrupts(self, initial_state: SDLCState) -> SDLCState:
        """
        Run workflow using proper LangGraph interrupt pattern
        
        Following: https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/#pause-using-interrupt
        """
        
        print("🚀 Starting Proper LangGraph Interrupt Workflow")
        print("📖 Following official LangGraph interrupt documentation")
        
        # Start the workflow once
        print(f"\n⚡ Starting initial workflow execution...")
        result = await self.workflow.ainvoke(initial_state, config=self.config)
        
        # ⭐ LOOP to handle multiple interrupts (for iteration cycles)
        while True:
            # Check if interrupted
            state_info = await self.workflow.aget_state(self.config)
            print("######### State info", state_info)
            if state_info.next:
                # Workflow is paused
                current_values = state_info.values
                print(f"\n🛑 Workflow interrupted. Next step: {state_info.next}")
                print(f"📊 Current state: {current_values.get('current_stage', 'unknown')}")
                print(f"🔄 Current iteration: {current_values.get('iteration_count', 0)}")
                
                # Get user choice for review
                user_stories = current_values.get("user_stories", [])
                if user_stories:
                    choice = ask_review_choice("Product Owner Review", user_stories)
                    
                    # Update state based on choice
                    state_updates = self._prepare_state_updates_for_choice(choice)
                    
                    print(f"\n[TOOLS] Updating workflow state for {choice} choice...")
                    print(f"📝 State updates: {state_updates}")
                    
                    await self.workflow.aupdate_state(self.config, state_updates)
                    
                    # Verify state was updated
                    updated_state_info = await self.workflow.aget_state(self.config)
                    updated_values = updated_state_info.values
                    print(f"🔍 Verification - Updated state contains:")
                    print(f"   review_type: {updated_values.get('review_type', 'NOT SET')}")
                    print(f"   human_review_requested: {updated_values.get('human_review_requested', 'NOT SET')}")
                    
                    # ⭐ Resume workflow with None (continue from interrupt point)
                    print(f"\n▶️ Resuming workflow from interrupt point...")
                    result = await self.workflow.ainvoke(None, config=self.config)
                    
                    # ⭐ After resume, check if we need to continue the loop
                    # The workflow might pause again if there's another iteration needed
                    continue
                    
                else:
                    print("⚠️ No user stories found, ending workflow")
                    return result or updated_values
            else:
                # Workflow completed
                print("🎉 Workflow execution completed!")
                final_state_info = await self.workflow.aget_state(self.config)
                return result or final_state_info.values
    
    def _prepare_state_updates_for_choice(self, choice: str) -> Dict[str, Any]:
        """
        Prepare state updates based on user choice
        
        This modifies only the specific fields needed to influence node behavior
        """
        
        print(f"🎯 Preparing state updates for choice: {choice}")
        
        if choice == "human":
            return {
                "review_type": "human",
                "human_review_requested": True,
            }
            
        elif choice == "ai":
            return {
                "review_type": "ai", 
                "human_review_requested": False,
            }
            
        elif choice == "auto":
            # For auto-approve, pre-set the review results
            return {
                "review_type": "auto",
                "human_review_requested": False,
                "approval_status": "approved",
                "review_feedback": {
                    "status": "approved",
                    "feedback": "Auto-approved by user choice",
                    "reviewer": "Auto",
                    "timestamp": datetime.now().isoformat(),
                    "approval_status": "approved"
                }
            }
        else:
            # Default to AI review
            return {
                "review_type": "ai",
                "human_review_requested": False,
            }
    
    async def _handle_interrupt_with_choice(self, current_state: SDLCState, choice: str) -> SDLCState:
        """
        DEPRECATED: This method is replaced by _prepare_state_updates_for_choice
        Keeping for backward compatibility
        """
        return self._prepare_state_updates_for_choice(choice)
    
    async def get_workflow_state(self) -> Dict[str, Any]:
        """Get current workflow state"""
        state = await self.workflow.aget_state(self.config)
        return {
            "values": state.values,
            "next": state.next,
            "metadata": state.metadata
        }
    
    async def update_workflow_state(self, updates: Dict[str, Any]) -> None:
        """Update workflow state"""
        await self.workflow.aupdate_state(self.config, updates)

# ==================== CONVENIENCE FUNCTION ====================

async def run_proper_workflow(requirements: str) -> Dict[str, Any]:
    """
    Convenience function using proper LangGraph interrupt pattern
    
    Args:
        requirements: User requirements string
        
    Returns:
        Dictionary with workflow results
    """
    
    # Create initial state - NOW WITH ALL REQUIRED FIELDS
    initial_state = SDLCState(
        requirements=requirements,
        user_stories=[],
        design_docs={},
        code={},
        test_cases=[],
        review_feedback={},
        approval_status="",
        current_stage="initial",
        iteration_count=0,
        project_id="PROPER-001",
        timestamp="",
        stakeholders=["Product Owner", "Tech Lead", "QA Lead"],
        security_scan_results={},
        test_results={},
        deployment_status="",
        review_preferences={},
        review_history=[],
        current_interrupt_node="",
        requires_review_choice=False,
        review_type="",  # Will be set during interrupt
        human_review_requested=False  # Will be set during interrupt
    )
    
    try:
        # Run workflow with proper interrupt handling
        runner = ProperWorkflowRunner()
        final_state = await runner.run_workflow_with_interrupts(initial_state)
        
        return {
            "success": True,
            "final_state": final_state,
            "user_stories_count": len(final_state.get("user_stories", [])),
            "final_stage": final_state.get("current_stage", "unknown"),
            "iterations": final_state.get("iteration_count", 0),
            "approval_status": final_state.get("approval_status", "unknown"),
            "review_type": final_state.get("review_type", "unknown"),
            "timestamp": final_state.get("timestamp", "")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }