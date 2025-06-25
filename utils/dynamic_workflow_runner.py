# ==================== UPDATED DYNAMIC WORKFLOW RUNNER ====================
# File: utils/dynamic_workflow_runner.py

import asyncio
from typing import Dict, Any, List
from langgraph.types import Command
from state.sdlc_state import SDLCState
from workflow.dynamic_interrupt_workflow import create_dynamic_interrupt_workflow
from datetime import datetime

class DynamicWorkflowRunner:
    """
    Workflow runner using DYNAMIC INTERRUPTS (Official LangGraph Pattern)
    Updated to handle both PO Review and Design Review interrupts
    
    Key differences from static approach:
    - No manual state management
    - Cleaner interrupt handling with __interrupt__ key
    - Direct value passing with Command(resume=value)
    - Automatic interrupt detection and handling
    """
    
    def __init__(self):
        self.workflow = create_dynamic_interrupt_workflow()
        self.config = {"configurable": {"thread_id": "dynamic-thread-1"}}
    
    async def run_workflow_with_dynamic_interrupts(self, initial_state: SDLCState) -> Dict[str, Any]:
        """
        Run workflow using dynamic interrupts - handles both PO and Design reviews!
        
        How it works:
        1. Start workflow normally
        2. Check for __interrupt__ key in result
        3. Handle interrupt with user input
        4. Resume with Command(resume=value)
        5. Repeat until workflow completes
        """
        
        print("🚀 Starting Dynamic Interrupt Workflow")
        print("🎯 Using interrupt() inside nodes (official pattern)")
        
        try:
            # Start the workflow
            print(f"\n⚡ Starting workflow execution...")
            result = await self.workflow.ainvoke(initial_state, config=self.config)
            
            # ⭐ MAIN INTERRUPT HANDLING LOOP
            interrupt_count = 0
            while result.get("__interrupt__"):
                interrupt_count += 1
                interrupts = result["__interrupt__"]
                
                print(f"\n🛑 Workflow interrupted #{interrupt_count}")
                print(f"📊 Number of interrupts: {len(interrupts)}")
                
                # Handle the interrupt(s)
                if len(interrupts) == 1:
                    # Single interrupt - most common case
                    user_response = await self._handle_single_interrupt(interrupts[0])
                    
                    # Resume with user response
                    print(f"▶️ Resuming workflow with response: {user_response}")
                    result = await self.workflow.ainvoke(
                        Command(resume=user_response), 
                        config=self.config
                    )
                else:
                    # Multiple interrupts - handle batch
                    user_responses = await self._handle_multiple_interrupts(interrupts)
                    
                    # Resume with response mapping
                    print(f"▶️ Resuming workflow with {len(user_responses)} responses")
                    result = await self.workflow.ainvoke(
                        Command(resume=user_responses), 
                        config=self.config
                    )
            
            print(f"\n🎉 Workflow completed successfully!")
            print(f"📊 Total interrupts handled: {interrupt_count}")
            
            return {
                "success": True,
                "final_state": result,
                "user_stories_count": len(result.get("user_stories", [])),
                "design_docs_created": bool(result.get("design_docs")),
                "final_stage": result.get("current_stage", "unknown"),
                "iterations": result.get("iteration_count", 0),
                "approval_status": result.get("approval_status", "unknown"),
                "interrupts_handled": interrupt_count,
                "timestamp": result.get("timestamp", datetime.now().isoformat())
            }
            
        except Exception as e:
            print(f"\n❌ Workflow execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def _handle_single_interrupt(self, interrupt_obj) -> Any:
        """
        Handle a single interrupt with user interaction
        Now supports both PO Review and Design Review interrupts
        """
        
        interrupt_data = interrupt_obj.value
        interrupt_type = interrupt_data.get("type", "unknown")
        
        print(f"🔍 Interrupt type: {interrupt_type}")
        
        # Route to appropriate handler based on interrupt type
        if interrupt_type == "review_choice":
            return self._handle_review_choice_interrupt(interrupt_data)
        elif interrupt_type == "human_review_decision":
            return self._handle_human_review_decision(interrupt_data)
        elif interrupt_type == "human_review_feedback":
            return self._handle_human_review_feedback(interrupt_data)
        elif interrupt_type == "human_review_suggestions":
            return self._handle_human_review_suggestions(interrupt_data)
        # NEW: Design Review Interrupts
        elif interrupt_type == "design_review_choice":
            return self._handle_design_review_choice_interrupt(interrupt_data)
        elif interrupt_type == "human_design_review_decision":
            return self._handle_human_design_review_decision(interrupt_data)
        elif interrupt_type == "human_design_review_feedback":
            return self._handle_human_design_review_feedback(interrupt_data)
        elif interrupt_type == "human_design_review_suggestions":
            return self._handle_human_design_review_suggestions(interrupt_data)
        else:
            # Generic handler for unknown types
            return self._handle_generic_interrupt(interrupt_data)
    
    # ==================== PO REVIEW INTERRUPT HANDLERS ====================
    
    def _handle_review_choice_interrupt(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle the initial PO review choice (human/ai/auto)"""
        
        question = interrupt_data.get("question", "Choose review method:")
        options = interrupt_data.get("options", {})
        context = interrupt_data.get("context", {})
        stories_preview = interrupt_data.get("user_stories_preview", [])
        
        print(f"\n❓ {question}")
        print(f"📊 Context: {context.get('user_stories_count', 0)} stories, iteration {context.get('current_iteration', 0)}")
        
        if stories_preview:
            print(f"\n📖 User Stories Preview:")
            for story in stories_preview:
                print(f"  • {story['id']}: {story['title']} (Priority: {story['priority']})")
        
        print(f"\n🎛️ Available options:")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            choice = input(f"\nYour choice ({'/'.join(options.keys())}): ").strip().lower()
            if choice in options:
                print(f"✅ You selected: {options[choice]}")
                return choice
            print(f"❌ Invalid choice. Please choose from: {list(options.keys())}")
    
    def _handle_human_review_decision(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle human PO review decision (approve/request_changes/reject)"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        options = interrupt_data.get("options", {})
        stories = interrupt_data.get("stories", [])
        
        print(f"\n📋 {prompt}")
        
        if stories:
            print(f"\n📚 User Stories to Review:")
            for story in stories:
                print(f"\n{story['number']}. {story['id']}: {story['title']}")
                print(f"   📝 {story['description']}")
                print(f"   🎯 Priority: {story['priority']} | Points: {story['story_points']}")
                print(f"   ✅ Acceptance Criteria: {story['acceptance_criteria_count']}")
        
        print(f"\n❓ {question}")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            decision = input(f"\nYour decision ({'/'.join(options.keys())}): ").strip().lower()
            if decision in options:
                print(f"✅ You decided: {options[decision]}")
                return decision
            print(f"❌ Invalid decision. Please choose from: {list(options.keys())}")
    
    def _handle_human_review_feedback(self, interrupt_data: Dict[str, Any]) -> Dict[str, str]:
        """Handle detailed PO feedback collection"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        
        print(f"\n💬 {prompt}")
        print(f"❓ {question}")
        
        feedback = input("\nYour detailed feedback: ").strip()
        
        if not feedback:
            feedback = "No specific feedback provided"
        
        print(f"✅ Feedback recorded: {feedback[:100]}{'...' if len(feedback) > 100 else ''}")
        
        return {"feedback": feedback}
    
    def _handle_human_review_suggestions(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle PO suggestions collection"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        current_feedback = interrupt_data.get("current_feedback", "")
        help_text = interrupt_data.get("help_text", "")
        
        print(f"\n💡 {prompt}")
        if current_feedback:
            print(f"📝 Current feedback: {current_feedback}")
        print(f"❓ {question}")
        if help_text:
            print(f"ℹ️ {help_text}")
        
        suggestion = input("\nYour suggestion (or press Enter to skip): ").strip()
        
        if suggestion:
            print(f"✅ Suggestion recorded: {suggestion}")
        else:
            print("⏭️ No suggestion provided - skipping")
            suggestion = ""
        
        return suggestion
    
    # ==================== DESIGN REVIEW INTERRUPT HANDLERS ====================
    
    def _handle_design_review_choice_interrupt(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle design review choice interrupt"""
        
        question = interrupt_data.get("question", "Choose design review method:")
        options = interrupt_data.get("options", {})
        context = interrupt_data.get("context", {})
        design_preview = interrupt_data.get("design_preview", {})
        
        print(f"\n❓ {question}")
        print(f"📊 Context: Design docs available: {context.get('design_docs_available', False)}, iteration {context.get('current_iteration', 0)}")
        
        if design_preview:
            print(f"\n📋 Design Document Preview:")
            print(f"  📄 Title: {design_preview.get('title', 'N/A')}")
            print(f"  📝 Summary: {design_preview.get('summary', 'N/A')}")
            sections = design_preview.get('sections', [])
            if sections:
                print(f"  🗂️ Sections: {', '.join(sections[:5])}{'...' if len(sections) > 5 else ''}")
        
        print(f"\n🎛️ Available options:")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            choice = input(f"\nYour choice ({'/'.join(options.keys())}): ").strip().lower()
            if choice in options:
                print(f"✅ You selected: {options[choice]}")
                return choice
            print(f"❌ Invalid choice. Please choose from: {list(options.keys())}")
    
    def _handle_human_design_review_decision(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle human design review decision"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        options = interrupt_data.get("options", {})
        design_document = interrupt_data.get("design_document", {})
        
        print(f"\n📋 {prompt}")
        
        if design_document:
            print(f"\n📄 Design Document: {design_document.get('title', 'N/A')}")
            print(f"📝 Summary: {design_document.get('summary', 'N/A')}")
            
            sections = design_document.get('sections', [])
            if sections:
                print(f"\n🗂️ Design Sections:")
                for section in sections:
                    print(f"  • {section['name']}: {section['overview'][:100]}{'...' if len(section['overview']) > 100 else ''}")
        
        print(f"\n❓ {question}")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            decision = input(f"\nYour decision ({'/'.join(options.keys())}): ").strip().lower()
            if decision in options:
                print(f"✅ You decided: {options[decision]}")
                return decision
            print(f"❌ Invalid decision. Please choose from: {list(options.keys())}")
    
    def _handle_human_design_review_feedback(self, interrupt_data: Dict[str, Any]) -> Dict[str, str]:
        """Handle design review feedback collection"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        
        print(f"\n💬 {prompt}")
        print(f"❓ {question}")
        
        feedback = input("\nYour detailed technical feedback: ").strip()
        
        if not feedback:
            feedback = "No specific technical feedback provided"
        
        print(f"✅ Technical feedback recorded: {feedback[:100]}{'...' if len(feedback) > 100 else ''}")
        
        return {"feedback": feedback}
    
    def _handle_human_design_review_suggestions(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle design review suggestions collection"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        current_feedback = interrupt_data.get("current_feedback", "")
        help_text = interrupt_data.get("help_text", "")
        
        print(f"\n💡 {prompt}")
        if current_feedback:
            print(f"📝 Current feedback: {current_feedback}")
        print(f"❓ {question}")
        if help_text:
            print(f"ℹ️ {help_text}")
        
        suggestion = input("\nYour technical suggestion (or press Enter to skip): ").strip()
        
        if suggestion:
            print(f"✅ Technical suggestion recorded: {suggestion}")
        else:
            print("⏭️ No technical suggestion provided - skipping")
            suggestion = ""
        
        return suggestion
    
    # ==================== GENERIC HANDLER ====================
    
    def _handle_generic_interrupt(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle unknown/generic interrupts"""
        
        question = interrupt_data.get("question", "Please provide input:")
        options = interrupt_data.get("options", {})
        
        print(f"\n❓ {question}")
        
        if options:
            print("Available options:")
            for key, value in options.items():
                print(f"  {key}: {value}")
            
            while True:
                choice = input(f"\nYour choice ({'/'.join(options.keys())}): ").strip()
                if choice in options:
                    return choice
                print(f"❌ Invalid choice. Please choose from: {list(options.keys())}")
        else:
            return input("Your response: ").strip()
    
    async def _handle_multiple_interrupts(self, interrupts) -> List[Any]:
        """Handle multiple interrupts (rarely used but included for completeness)"""
        
        print(f"\n🔄 Handling {len(interrupts)} simultaneous interrupts...")
        responses = []
        
        for i, interrupt_obj in enumerate(interrupts, 1):
            print(f"\n--- Interrupt {i}/{len(interrupts)} ---")
            response = await self._handle_single_interrupt(interrupt_obj)
            responses.append(response)
        
        return responses