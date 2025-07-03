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
    Updated to handle PO Review, Design Review, and Code Review interrupts
    
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
        Run workflow using dynamic interrupts - handles PO, Design, and Code reviews!
        
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
                "security_scan_results": len(result.get("security_scan_results", {})),
                "test_files_generated": len(result.get("test_cases", {})),
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
        Now supports PO Review, Design Review, and Code Review interrupts
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
        
        # Design Review Interrupts
        elif interrupt_type == "design_review_choice":
            return self._handle_design_review_choice_interrupt(interrupt_data)
        elif interrupt_type == "human_design_review_decision":
            return self._handle_human_design_review_decision(interrupt_data)
        elif interrupt_type == "human_design_review_feedback":
            return self._handle_human_design_review_feedback(interrupt_data)
        elif interrupt_type == "human_design_review_suggestions":
            return self._handle_human_design_review_suggestions(interrupt_data)
        
        # NEW: Code Review Interrupts
        elif interrupt_type == "code_review_choice":
            return self._handle_code_review_choice_interrupt(interrupt_data)
        elif interrupt_type == "human_code_review_decision":
            return self._handle_human_code_review_decision(interrupt_data)
        elif interrupt_type == "human_code_review_feedback":
            return self._handle_human_code_review_feedback(interrupt_data)
        elif interrupt_type == "human_code_review_suggestions":
            return self._handle_human_code_review_suggestions(interrupt_data)
        
        # NEW: Security Review Interrupts
        elif interrupt_type == "security_review_choice":
            return self._handle_security_review_choice_interrupt(interrupt_data)
        elif interrupt_type == "human_security_review_decision":
            return self._handle_human_security_review_decision(interrupt_data)
        elif interrupt_type == "human_security_review_feedback":
            return self._handle_human_security_review_feedback(interrupt_data)
        elif interrupt_type == "human_security_risk_assessment":
            return self._handle_human_security_risk_assessment(interrupt_data)
        
        # NEW: Test Cases Review Interrupts
        elif interrupt_type == "test_cases_review_choice":
            return self._handle_test_cases_review_choice_interrupt(interrupt_data)
        elif interrupt_type == "human_test_review_decision":
            return self._handle_human_test_review_decision(interrupt_data)
        elif interrupt_type == "human_test_review_feedback":
            return self._handle_human_test_review_feedback(interrupt_data)
        elif interrupt_type == "human_test_improvement_suggestions":
            return self._handle_human_test_improvement_suggestions(interrupt_data)
        
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
    
    # ==================== NEW: SECURITY REVIEW INTERRUPT HANDLERS ====================
    
    def _handle_security_review_choice_interrupt(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle security review choice interrupt"""
        
        question = interrupt_data.get("question", "Choose security review method:")
        options = interrupt_data.get("options", {})
        context = interrupt_data.get("context", {})
        security_preview = interrupt_data.get("security_preview", {})
        
        print(f"\n❓ {question}")
        print(f"🔒 Context: {context.get('code_files_count', 0)} code files, iteration {context.get('current_iteration', 0)}")
        
        if security_preview:
            print(f"\n🔍 Security Analysis Preview:")
            files = security_preview.get('files', [])
            if files:
                print(f"  📁 Files: {', '.join(files)}")
            
            languages = security_preview.get('code_languages', [])
            if languages:
                print(f"  💻 Languages: {', '.join(languages)}")
            
            security_areas = security_preview.get('potential_security_areas', [])
            if security_areas:
                print(f"  🔒 Security Areas: {', '.join(security_areas)}")
        
        print(f"\n🎛️ Available options:")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            choice = input(f"\nYour choice ({'/'.join(options.keys())}): ").strip().lower()
            if choice in options:
                print(f"✅ You selected: {options[choice]}")
                return choice
            print(f"❌ Invalid choice. Please choose from: {list(options.keys())}")
    
    def _handle_human_security_review_decision(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle human security review decision"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        options = interrupt_data.get("options", {})
        security_analysis = interrupt_data.get("security_analysis", {})
        
        print(f"\n📋 {prompt}")
        
        if security_analysis:
            total_files = security_analysis.get('total_files', 0)
            languages = security_analysis.get('languages', [])
            security_areas = security_analysis.get('security_areas', [])
            
            print(f"\n🔒 Security Analysis Summary:")
            print(f"  📊 Total files: {total_files}")
            if languages:
                print(f"  💻 Languages: {', '.join(languages)}")
            if security_areas:
                print(f"  🔍 Security areas: {', '.join(security_areas)}")
            
            files = security_analysis.get('files', [])
            for file_info in files[:3]:  # Show first 3 files
                filename = file_info.get('filename', 'Unknown')
                lines = file_info.get('lines', 0)
                security_keywords = file_info.get('security_keywords', {})
                
                print(f"\n📄 {filename} ({lines} lines)")
                if security_keywords:
                    print(f"   🔑 Security keywords: {', '.join(security_keywords.keys())}")
                
                preview = file_info.get('preview', '')
                if preview:
                    print(f"   Preview: {preview[:150]}{'...' if len(preview) > 150 else ''}")
        
        print(f"\n❓ {question}")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            decision = input(f"\nYour decision ({'/'.join(options.keys())}): ").strip().lower()
            if decision in options:
                print(f"✅ You decided: {options[decision]}")
                return decision
            print(f"❌ Invalid decision. Please choose from: {list(options.keys())}")
    
    def _handle_human_security_review_feedback(self, interrupt_data: Dict[str, Any]) -> Dict[str, str]:
        """Handle security review feedback collection"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        
        print(f"\n💬 {prompt}")
        print(f"❓ {question}")
        
        feedback = input("\nYour detailed security feedback: ").strip()
        
        if not feedback:
            feedback = "No specific security feedback provided"
        
        print(f"✅ Security feedback recorded: {feedback[:100]}{'...' if len(feedback) > 100 else ''}")
        
        return {"feedback": feedback}
    
    def _handle_human_security_risk_assessment(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle security risk assessment collection"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        risk_options = interrupt_data.get("risk_options", {})
        current_feedback = interrupt_data.get("current_feedback", "")
        
        print(f"\n🎯 {prompt}")
        if current_feedback:
            print(f"📝 Current feedback: {current_feedback}")
        print(f"❓ {question}")
        
        if risk_options:
            print(f"\n🚨 Risk Level Options:")
            for key, description in risk_options.items():
                print(f"  {key}: {description}")
            
            while True:
                risk_choice = input(f"\nRisk level ({'/'.join(risk_options.keys())}): ").strip().lower()
                if risk_choice in risk_options:
                    print(f"✅ Risk level set: {risk_options[risk_choice]}")
                    
                    # Get suggestions
                    suggestions = input("\nSpecific security improvement suggestions (optional): ").strip()
                    
                    return {
                        "risk_level": risk_choice,
                        "suggestions": suggestions if suggestions else ""
                    }
                print(f"❌ Invalid risk level. Please choose from: {list(risk_options.keys())}")
        else:
            suggestion = input("\nYour security improvement suggestion: ").strip()
            return suggestion if suggestion else "medium"
    
    # ==================== NEW: TEST CASES REVIEW INTERRUPT HANDLERS ====================
    
    def _handle_test_cases_review_choice_interrupt(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle test cases review choice interrupt"""
        
        question = interrupt_data.get("question", "Choose test review method:")
        options = interrupt_data.get("options", {})
        context = interrupt_data.get("context", {})
        test_preview = interrupt_data.get("test_preview", {})
        
        print(f"\n❓ {question}")
        print(f"🧪 Context: {context.get('test_files_count', 0)} test files, iteration {context.get('current_iteration', 0)}")
        
        if test_preview:
            print(f"\n📊 Test Cases Preview:")
            files = test_preview.get('files', [])
            if files:
                print(f"  📁 Test files: {', '.join(files)}")
            print(f"  📊 Total files: {test_preview.get('total_files', 0)}")
            
            test_stats = test_preview.get('test_stats', {})
            if test_stats:
                print(f"  🔢 Test functions: {test_stats.get('total_test_functions', 0)}")
                print(f"  📋 Test classes: {test_stats.get('test_classes', 0)}")
                print(f"  🔧 Fixtures: {test_stats.get('fixtures', 0)}")
            
            coverage_areas = test_preview.get('coverage_areas', [])
            if coverage_areas:
                print(f"  🎯 Coverage areas: {', '.join(coverage_areas)}")
        
        print(f"\n🎛️ Available options:")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            choice = input(f"\nYour choice ({'/'.join(options.keys())}): ").strip().lower()
            if choice in options:
                print(f"✅ You selected: {options[choice]}")
                return choice
            print(f"❌ Invalid choice. Please choose from: {list(options.keys())}")
    
    def _handle_human_test_review_decision(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle human test review decision"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        options = interrupt_data.get("options", {})
        test_analysis = interrupt_data.get("test_analysis", {})
        
        print(f"\n📋 {prompt}")
        
        if test_analysis:
            total_files = test_analysis.get('total_files', 0)
            statistics = test_analysis.get('statistics', {})
            coverage_areas = test_analysis.get('coverage_areas', [])
            
            print(f"\n🧪 Test Analysis Summary:")
            print(f"  📊 Total test files: {total_files}")
            
            if statistics:
                print(f"  🔢 Test functions: {statistics.get('total_test_functions', 0)}")
                print(f"  📋 Test classes: {statistics.get('test_classes', 0)}")
                print(f"  🔧 Fixtures: {statistics.get('fixtures', 0)}")
                print(f"  📊 Parametrized tests: {statistics.get('parametrized_tests', 0)}")
            
            if coverage_areas:
                print(f"  🎯 Coverage areas: {', '.join(coverage_areas)}")
            
            files = test_analysis.get('files', [])
            for file_info in files[:2]:  # Show first 2 test files
                filename = file_info.get('filename', 'Unknown')
                lines = file_info.get('lines', 0)
                test_functions = file_info.get('test_functions', 0)
                test_classes = file_info.get('test_classes', 0)
                
                print(f"\n📄 {filename} ({lines} lines)")
                print(f"   🔢 Test functions: {test_functions}, Test classes: {test_classes}")
                
                preview = file_info.get('preview', '')
                if preview:
                    print(f"   Preview: {preview[:200]}{'...' if len(preview) > 200 else ''}")
        
        print(f"\n❓ {question}")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            decision = input(f"\nYour decision ({'/'.join(options.keys())}): ").strip().lower()
            if decision in options:
                print(f"✅ You decided: {options[decision]}")
                return decision
            print(f"❌ Invalid decision. Please choose from: {list(options.keys())}")
    
    def _handle_human_test_review_feedback(self, interrupt_data: Dict[str, Any]) -> Dict[str, str]:
        """Handle test review feedback collection"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        
        print(f"\n💬 {prompt}")
        print(f"❓ {question}")
        
        feedback = input("\nYour detailed test feedback: ").strip()
        
        if not feedback:
            feedback = "No specific test feedback provided"
        
        print(f"✅ Test feedback recorded: {feedback[:100]}{'...' if len(feedback) > 100 else ''}")
        
        return {"feedback": feedback}
    
    def _handle_human_test_improvement_suggestions(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle test improvement suggestions collection"""
        
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
        
        suggestion = input("\nYour test improvement suggestion (or press Enter to skip): ").strip()
        
        if suggestion:
            print(f"✅ Test improvement suggestion recorded: {suggestion}")
        else:
            print("⏭️ No test improvement suggestion provided - skipping")
            suggestion = ""
    
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
    
    # ==================== NEW: CODE REVIEW INTERRUPT HANDLERS ====================
    
    def _handle_code_review_choice_interrupt(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle code review choice interrupt"""
        
        question = interrupt_data.get("question", "Choose code review method:")
        options = interrupt_data.get("options", {})
        context = interrupt_data.get("context", {})
        code_preview = interrupt_data.get("code_preview", {})
        
        print(f"\n❓ {question}")
        print(f"📊 Context: {context.get('code_files_count', 0)} code files, iteration {context.get('current_iteration', 0)}")
        
        if code_preview:
            print(f"\n💻 Code Files Preview:")
            files = code_preview.get('files', [])
            if files:
                print(f"  📁 Files: {', '.join(files)}")
            print(f"  📊 Total files: {code_preview.get('total_files', 0)}")
            
            file_sizes = code_preview.get('file_sizes', {})
            if file_sizes:
                print(f"  📏 File sizes:")
                for filename, size in file_sizes.items():
                    print(f"     {filename}: {size} characters")
        
        print(f"\n🎛️ Available options:")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            choice = input(f"\nYour choice ({'/'.join(options.keys())}): ").strip().lower()
            if choice in options:
                print(f"✅ You selected: {options[choice]}")
                return choice
            print(f"❌ Invalid choice. Please choose from: {list(options.keys())}")
    
    def _handle_human_code_review_decision(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle human code review decision"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        options = interrupt_data.get("options", {})
        code_files = interrupt_data.get("code_files", {})
        
        print(f"\n📋 {prompt}")
        
        if code_files:
            total_files = code_files.get('total_files', 0)
            print(f"\n💻 Code Review Summary: {total_files} files")
            
            files = code_files.get('files', [])
            for file_info in files:
                filename = file_info.get('filename', 'Unknown')
                lines = file_info.get('lines', 0)
                size = file_info.get('size_chars', 0)
                preview = file_info.get('preview', '')
                
                print(f"\n📄 {filename} ({lines} lines, {size} chars)")
                print(f"   Preview: {preview[:100]}{'...' if len(preview) > 100 else ''}")
        
        print(f"\n❓ {question}")
        for key, description in options.items():
            print(f"  {key}: {description}")
        
        while True:
            decision = input(f"\nYour decision ({'/'.join(options.keys())}): ").strip().lower()
            if decision in options:
                print(f"✅ You decided: {options[decision]}")
                return decision
            print(f"❌ Invalid decision. Please choose from: {list(options.keys())}")
    
    def _handle_human_code_review_feedback(self, interrupt_data: Dict[str, Any]) -> Dict[str, str]:
        """Handle code review feedback collection"""
        
        prompt = interrupt_data.get("prompt", "")
        question = interrupt_data.get("question", "")
        
        print(f"\n💬 {prompt}")
        print(f"❓ {question}")
        
        feedback = input("\nYour detailed code feedback: ").strip()
        
        if not feedback:
            feedback = "No specific code feedback provided"
        
        print(f"✅ Code feedback recorded: {feedback[:100]}{'...' if len(feedback) > 100 else ''}")
        
        return {"feedback": feedback}
    
    def _handle_human_code_review_suggestions(self, interrupt_data: Dict[str, Any]) -> str:
        """Handle code review suggestions collection"""
        
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
        
        suggestion = input("\nYour code suggestion (or press Enter to skip): ").strip()
        
        if suggestion:
            print(f"✅ Code suggestion recorded: {suggestion}")
        else:
            print("⏭️ No code suggestion provided - skipping")
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