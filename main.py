import asyncio
import sys
from utils.proper_workflow_runner import run_proper_workflow, ProperWorkflowRunner
from utils.visualization_utils import WorkflowVisualizer
from workflow.proper_interrupt_workflow import create_proper_interrupt_workflow
from config.settings import settings

def display_proper_menu():
    """Display menu for proper LangGraph interrupt workflow"""
    print("\n" + "="*70)
    print("🏗️  PROPER LANGGRAPH INTERRUPT WORKFLOW")
    print("="*70)
    print("📖 Following Official LangGraph Documentation")
    print("🔗 https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/")
    print("-" * 70)
    print("1. 🚀 Run Workflow (Proper Interrupts)")
    print("2. 🔄 Display Workflow Graph") 
    print("3. 📊 Show Implementation Status")
    print("4. 🧪 Debug Workflow State")
    print("5. ❌ Exit")
    print("="*70)

async def run_proper_sdlc_workflow():
    """Run SDLC workflow using proper LangGraph interrupt pattern"""
    
    print("\n🚀 Proper LangGraph Interrupt Workflow")
    print("=" * 50)
    print("✨ This follows the official LangGraph documentation")
    print("🛑 Workflow will pause BEFORE product_owner_review node")
    print("🎛️ You choose how to handle the review, then workflow continues")
    
    # Get requirements
    print("\n📝 Enter your project requirements:")
    requirements = input("Requirements: ").strip()
    
    if not requirements:
        requirements = "Build a task management app with user authentication"
        print(f"🔄 Using default: {requirements}")
    
    try:
        print("\n⚡ Starting proper interrupt workflow...")
        
        # Run using proper LangGraph pattern
        result = await run_proper_workflow(requirements)
        
        if result["success"]:
            await display_proper_results(result)
        else:
            print(f"\n❌ Workflow failed: {result['error']}")
            print(f"🔍 Error type: {result['error_type']}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return None

async def display_proper_results(result: dict):
    """Display results from proper workflow execution"""
    
    print("\n" + "="*70)
    print("🎉 PROPER WORKFLOW EXECUTION RESULTS")
    print("="*70)
    
    final_state = result["final_state"]
    
    # Basic info
    print(f"📊 Final Stage: {result['final_stage']}")
    print(f"📚 User Stories: {result['user_stories_count']}")
    print(f"🔄 Iterations: {result['iterations']}")
    print(f"✅ Approval Status: {result['approval_status'].upper()}")
    print(f"🎛️ Review Type Used: {result.get('review_type', 'Unknown').upper()}")
    
    # Show user stories if any
    user_stories = final_state.get("user_stories", [])
    if user_stories:
        print(f"\n📖 Generated User Stories:")
        for i, story in enumerate(user_stories, 1):
            story_id = story.get('id', f'US-{i:03d}')
            story_title = story.get('title', 'Untitled')
            priority = story.get('priority', 'Unknown')
            points = story.get('story_points', 'TBD')
            
            print(f"\n{i}. {story_id}: {story_title}")
            print(f"   🎯 Priority: {priority} | 📊 Points: {points}")
            
            # Show description
            description = story.get('description', '')
            if description:
                desc_preview = description[:100] + "..." if len(description) > 100 else description
                print(f"   📝 {desc_preview}")
            
            # Show acceptance criteria count
            criteria_count = len(story.get('acceptance_criteria', []))
            print(f"   ✅ {criteria_count} acceptance criteria defined")
    
    # ⭐ Show complete review history
    review_history = final_state.get("review_history", [])
    if review_history:
        print(f"\n📚 COMPLETE REVIEW HISTORY ({len(review_history)} reviews):")
        for i, review in enumerate(review_history, 1):
            iteration = review.get('iteration', i-1)
            reviewer = review.get('reviewer', 'Unknown')
            status = review.get('status', 'Unknown')
            feedback = review.get('feedback', 'No feedback')
            
            print(f"\n   📋 Review {i} (Iteration {iteration}):")
            print(f"      👤 Reviewer: {reviewer}")
            print(f"      ✅ Status: {status.upper()}")
            print(f"      💬 Feedback: {feedback[:80]}{'...' if len(feedback) > 80 else ''}")
            
            # Show suggestions if any
            suggestions = review.get('suggestions', [])
            if suggestions:
                print(f"      💡 Suggestions: {len(suggestions)} provided")
            
            # Show scores if available
            bv_score = review.get('business_value_score')
            comp_score = review.get('completeness_score')
            if bv_score and comp_score:
                print(f"      📊 Scores - Business Value: {bv_score}/10, Completeness: {comp_score}/10")
    
    # Show current/latest review feedback if different from history
    review_feedback = final_state.get("review_feedback", {})
    if review_feedback and review_feedback.get("feedback"):
        reviewer = review_feedback.get("reviewer", "Unknown")
        feedback = review_feedback.get("feedback", "")
        print(f"\n💬 Latest Review by {reviewer}:")
        if feedback:
            feedback_preview = feedback[:150] + "..." if len(feedback) > 150 else feedback
            print(f"   {feedback_preview}")
        
        # Show scores if available
        bv_score = review_feedback.get("business_value_score")
        comp_score = review_feedback.get("completeness_score")
        if bv_score and comp_score:
            print(f"   📊 Scores - Business Value: {bv_score}/10, Completeness: {comp_score}/10")
    
    print(f"\n🕒 Completed at: {result.get('timestamp', 'Unknown')}")
    print("✅ Proper LangGraph interrupt workflow completed!")

async def debug_workflow_state():
    """Debug current workflow state for development"""
    
    print("\n🧪 WORKFLOW STATE DEBUGGER")
    print("=" * 40)
    
    try:
        # Create runner to access workflow state
        runner = ProperWorkflowRunner()
        state_info = await runner.get_workflow_state()
        
        print("📊 Current Workflow State:")
        print(f"   Values: {state_info.get('values', 'None')}")
        print(f"   Next steps: {state_info.get('next', 'None')}")
        print(f"   Metadata: {state_info.get('metadata', 'None')}")
        
    except Exception as e:
        print(f"❌ Error accessing workflow state: {e}")
        print("💡 Run a workflow first to generate state")

def show_proper_implementation_status():
    """Show implementation status for proper approach"""
    
    print("\n📊 PROPER LANGGRAPH IMPLEMENTATION STATUS")
    print("="*55)
    
    print("\n✅ IMPLEMENTED - PROPER PATTERN:")
    features = [
        "✅ Official LangGraph interrupt pattern",
        "✅ Proper workflow.compile(interrupt_before=...)",
        "✅ State-based choice handling",
        "✅ Actual workflow nodes (not replacement)",
        "✅ Thread-based state management",
        "✅ Enhanced PO review with choice detection",
        "✅ Human/AI/Auto review modes",
        "✅ Proper workflow continuation after interrupt"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print(f"\n🎯 TECHNICAL DETAILS:")
    print(f"  • Uses: workflow.ainvoke() + interrupt_before")
    print(f"  • State: Thread-based with config={{thread_id: '1'}}")
    print(f"  • Choice: Modifies state, lets actual nodes run")
    print(f"  • Pattern: Official LangGraph documentation")
    
    print(f"\n⚙️ CONFIGURATION:")
    print(f"  • Max Stories: {settings.MAX_USER_STORIES}")
    print(f"  • Max Iterations: {settings.MAX_ITERATIONS}")
    print(f"  • Model: {settings.OPENAI_MODEL}")
    
    print(f"\n🔗 REFERENCE:")
    print("  📖 https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/")

async def main():
    """Main application for proper LangGraph interrupt workflow"""
    
    print("🏗️ Proper LangGraph Interrupt Workflow System")
    print("📖 Following Official Documentation")
    
    while True:
        display_proper_menu()
        
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                result = await run_proper_sdlc_workflow()
                input("\n📱 Press Enter to continue...")
                
            elif choice == '2':
                print("\n🔄 Displaying Workflow Graph...")
                try:
                    workflow = create_proper_interrupt_workflow()
                    visualizer = WorkflowVisualizer(workflow)
                    visualizer.save_workflow_image("workflow_graph.png")
                    
                except Exception as e:
                    print(f"❌ Could not display graph: {e}")
                input("\n📱 Press Enter to continue...")
                
            elif choice == '3':
                show_proper_implementation_status()
                input("\n📱 Press Enter to continue...")
                
            elif choice == '4':
                await debug_workflow_state()
                input("\n📱 Press Enter to continue...")
                
            elif choice == '5':
                print("\n👋 Thank you for using Proper LangGraph Workflow!")
                sys.exit(0)
                
            else:
                print("\n❌ Invalid option. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using Proper LangGraph Workflow!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("📱 Press Enter to continue...")

if __name__ == "__main__":
    print("🚀 Starting Proper LangGraph Interrupt System...")
    asyncio.run(main())