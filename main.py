# ==================== MAIN APPLICATION - DYNAMIC INTERRUPTS ====================
# File: main_dynamic.py

import asyncio
import sys
from utils.dynamic_workflow_runner import DynamicWorkflowRunner
from utils.visualization_utils import WorkflowVisualizer
from workflow.dynamic_interrupt_workflow import create_dynamic_interrupt_workflow
from state.sdlc_state import SDLCState
from config.settings import settings

def display_dynamic_menu():
    """Display menu for dynamic interrupt workflow"""
    print("\n" + "="*70)
    print("🔥 DYNAMIC LANGGRAPH INTERRUPT WORKFLOW")
    print("="*70)
    print("⚡ Using interrupt() INSIDE nodes (Official Pattern)")
    print("🎯 Clean Command(resume=value) pattern")
    print("📖 Following LangGraph v0.4+ recommendations")
    print("-" * 70)
    print("1. 🚀 Run Dynamic Workflow")
    print("2. 🔄 Display Workflow Graph") 
    print("3. 📊 Show Implementation Comparison")
    print("4. 🧪 Test Interrupt Patterns")
    print("5. ❌ Exit")
    print("="*70)

async def run_dynamic_sdlc_workflow():
    """Run SDLC workflow using dynamic interrupt pattern"""
    
    print("\n🔥 Dynamic LangGraph Interrupt Workflow")
    print("=" * 50)
    print("⚡ This uses the OFFICIAL interrupt() pattern")
    print("🎯 interrupt() calls are INSIDE nodes")
    print("🔄 Resume with Command(resume=value)")
    
    # Get requirements
    print("\n📝 Enter your project requirements:")
    requirements = input("Requirements: ").strip()
    
    if not requirements:
        requirements = "Build a task management app with user authentication, project creation, and real-time notifications"
        print(f"🔄 Using default: {requirements}")
    
    try:
        print("\n⚡ Starting dynamic interrupt workflow...")
        
        # Create initial state
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
            project_id="DYNAMIC-001",
            timestamp="",
            stakeholders=["Product Owner", "Tech Lead", "QA Lead"],
            security_scan_results={},
            test_results={},
            deployment_status="",
            review_type="",
            human_review_requested=False
        )
        
        # Run using dynamic pattern
        runner = DynamicWorkflowRunner()
        result = await runner.run_workflow_with_dynamic_interrupts(initial_state)
        
        if result["success"]:
            await display_dynamic_results(result)
        else:
            print(f"\n❌ Workflow failed: {result['error']}")
            print(f"🔍 Error type: {result['error_type']}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return None

async def display_dynamic_results(result: dict):
    """Display results from dynamic workflow execution - Updated for Design Documents"""
    
    print("\n" + "="*70)
    print("🎉 DYNAMIC WORKFLOW EXECUTION RESULTS")
    print("="*70)
    
    final_state = result["final_state"]
    
    # Basic info with dynamic-specific metrics
    print(f"📊 Final Stage: {result['final_stage']}")
    print(f"📚 User Stories Generated: {result['user_stories_count']}")
    print(f"🎨 Design Documents Created: {'Yes' if result.get('design_docs_created') else 'No'}")
    print(f"🔄 Iterations Completed: {result['iterations']}")
    print(f"✅ Final Approval Status: {result['approval_status'].upper()}")
    print(f"🛑 Interrupts Handled: {result['interrupts_handled']}")
    print(f"⚡ Pattern Used: Dynamic interrupts (interrupt() inside nodes)")
    
    # Show user stories if any
    user_stories = final_state.get("user_stories", [])
    if user_stories:
        print(f"\n📖 Final User Stories:")
        for i, story in enumerate(user_stories, 1):
            story_id = story.get('id', f'US-{i:03d}')
            story_title = story.get('title', 'Untitled')
            priority = story.get('priority', 'Unknown')
            points = story.get('story_points', 'TBD')
            
            print(f"\n{i}. {story_id}: {story_title}")
            print(f"   🎯 Priority: {priority} | 📊 Points: {points}")
            
            # Show description preview
            description = story.get('description', '')
            if description:
                desc_preview = description[:100] + "..." if len(description) > 100 else description
                print(f"   📝 {desc_preview}")
            
            # Show acceptance criteria count
            criteria_count = len(story.get('acceptance_criteria', []))
            print(f"   ✅ {criteria_count} acceptance criteria defined")
    
    # Show design documents if created
    design_docs = final_state.get("design_docs", {})
    if design_docs:
        print(f"\n🎨 Design Documents Created:")
        
        # Show title and summary
        doc_title = design_docs.get("title", "Technical Design Document")
        doc_summary = design_docs.get("summary", "No summary available")
        print(f"   📄 {doc_title}")
        print(f"   📝 Summary: {doc_summary[:150]}{'...' if len(doc_summary) > 150 else ''}")
        
        # Show key sections with details
        sections_to_show = [
            ("system_architecture", "🏗️ System Architecture"),
            ("database_design", "🗄️ Database Design"),
            ("api_design", "🔌 API Design"),
            ("ui_design", "🎨 UI Design"),
            ("security_performance", "🔒 Security & Performance")
        ]
        
        print(f"\n   📋 Design Sections:")
        for section_key, section_name in sections_to_show:
            section_data = design_docs.get(section_key)
            if section_data and isinstance(section_data, dict):
                overview = section_data.get('overview', 'No overview available')
                print(f"      {section_name}: {overview[:80]}{'...' if len(overview) > 80 else ''}")
                
                # Show specific details for some sections
                if section_key == "system_architecture":
                    components = section_data.get('components', [])
                    if components:
                        print(f"         Components: {', '.join(components[:3])}{'...' if len(components) > 3 else ''}")
                
                elif section_key == "database_design":
                    entities = section_data.get('entities', [])
                    if entities:
                        print(f"         Entities: {', '.join(entities[:3])}{'...' if len(entities) > 3 else ''}")
                
                elif section_key == "api_design":
                    endpoints = section_data.get('core_endpoints', [])
                    if endpoints:
                        print(f"         Endpoints: {len(endpoints)} core endpoints defined")
        
        # Show implementation notes if available
        impl_notes = design_docs.get("implementation_notes", "")
        if impl_notes:
            notes_preview = impl_notes[:100] + "..." if len(impl_notes) > 100 else impl_notes
            print(f"\n   📌 Implementation Notes: {notes_preview}")
    
    # Show review history with enhanced info for both PO and Design reviews
    review_history = final_state.get("review_history", [])
    if review_history:
        print(f"\n📚 COMPLETE REVIEW HISTORY ({len(review_history)} reviews):")
        for i, review in enumerate(review_history, 1):
            iteration = review.get('iteration', i-1)
            reviewer = review.get('reviewer', 'Unknown')
            status = review.get('status', 'Unknown')
            stage = review.get('stage', 'unknown')
            method = review.get('review_method', 'unknown')
            feedback = review.get('feedback', 'No feedback')
            
            # Determine review type emoji
            stage_emoji = "👤" if stage == "product_owner_review" else "👨‍💻" if stage == "design_review" else "📋"
            stage_name = stage.replace('_', ' ').title()
            
            print(f"\n   {stage_emoji} Review {i} - {stage_name} (Iteration {iteration}):")
            print(f"      👤 Reviewer: {reviewer}")
            print(f"      ⚡ Method: {method}")
            print(f"      ✅ Status: {status.upper()}")
            print(f"      💬 Feedback: {feedback[:80]}{'...' if len(feedback) > 80 else ''}")
            
            # Show suggestions if any
            suggestions = review.get('suggestions', [])
            if suggestions:
                print(f"      💡 Suggestions: {len(suggestions)} provided")
            
            # Show scores based on review type
            if stage == "product_owner_review":
                bv_score = review.get('business_value_score')
                comp_score = review.get('completeness_score')
                if bv_score and comp_score:
                    print(f"      📊 Scores - Business Value: {bv_score}/10, Completeness: {comp_score}/10")
            elif stage == "design_review":
                tech_score = review.get('technical_score')
                comp_score = review.get('completeness_score')
                if tech_score and comp_score:
                    print(f"      📊 Scores - Technical: {tech_score}/10, Completeness: {comp_score}/10")
    
    print(f"\n🕒 Completed at: {result.get('timestamp', 'Unknown')}")
    print("✅ Dynamic interrupt workflow completed successfully!")

def show_implementation_comparison():
    """Show comparison between static and dynamic interrupt approaches"""
    
    print("\n📊 IMPLEMENTATION COMPARISON")
    print("="*60)
    
    print("\n🔴 OLD APPROACH (Static Interrupts):")
    print("  ❌ interrupt_before=['node_name'] in workflow.compile()")
    print("  ❌ Manual state management with aupdate_state()")
    print("  ❌ Resume with ainvoke(None, config)")
    print("  ❌ External interrupt handling logic")
    print("  ❌ Complex state coordination")
    
    print("\n🟢 NEW APPROACH (Dynamic Interrupts - Current):")
    print("  ✅ interrupt() calls INSIDE nodes")
    print("  ✅ Automatic interrupt detection via __interrupt__ key")
    print("  ✅ Resume with Command(resume=value)")
    print("  ✅ Self-contained node logic")
    print("  ✅ Rich interrupt payloads with context")
    print("  ✅ Multiple interrupts per node support")
    print("  ✅ Official LangGraph recommendation")
    
    print(f"\n⚙️ CONFIGURATION:")
    print(f"  • Max Stories: {settings.MAX_USER_STORIES}")
    print(f"  • Max Iterations: {settings.MAX_ITERATIONS}")
    print(f"  • Model: {settings.OPENAI_MODEL}")
    
    print(f"\n🔗 REFERENCES:")
    print("  📖 https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/")
    print("  📖 https://blog.langchain.com/interrupt/")

async def test_interrupt_patterns():
    """Test different interrupt patterns for demonstration"""
    
    print("\n🧪 INTERRUPT PATTERNS TEST")
    print("="*40)
    
    print("This would demonstrate:")
    print("1. Single interrupt with simple choice")
    print("2. Multiple interrupts in sequence")
    print("3. Conditional interrupts")
    print("4. Rich payload interrupts")
    print("\n💡 For now, use option 1 to see real interrupts in action!")

async def main():
    """Main application for dynamic LangGraph interrupt workflow"""
    
    print("🔥 Dynamic LangGraph Interrupt Workflow System")
    print("⚡ Using Official interrupt() Pattern")
    
    while True:
        display_dynamic_menu()
        
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                result = await run_dynamic_sdlc_workflow()
                input("\n📱 Press Enter to continue...")
                
            elif choice == '2':
                print("\n🔄 Displaying Dynamic Workflow Graph...")
                try:
                    workflow = create_dynamic_interrupt_workflow()
                    visualizer = WorkflowVisualizer(workflow)
                    visualizer.save_workflow_image("workflow_graph.png")
                    
                except Exception as e:
                    print(f"❌ Could not display graph: {e}")
                input("\n📱 Press Enter to continue...")
                
            elif choice == '3':
                show_implementation_comparison()
                input("\n📱 Press Enter to continue...")
                
            elif choice == '4':
                await test_interrupt_patterns()
                input("\n📱 Press Enter to continue...")
                
            elif choice == '5':
                print("\n👋 Thank you for using Dynamic LangGraph Workflow!")
                sys.exit(0)
                
            else:
                print("\n❌ Invalid option. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using Dynamic LangGraph Workflow!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("📱 Press Enter to continue...")

if __name__ == "__main__":
    print("🚀 Starting Dynamic LangGraph Interrupt System...")
    asyncio.run(main())