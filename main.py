import asyncio
import sys
from state.sdlc_state import SDLCState
from workflow.sdlc_workflow import create_sdlc_workflow
from utils.visualization_utils import WorkflowVisualizer

def display_menu():
    """Display main menu options"""
    print("\n" + "="*60)
    print("🏗️  SDLC WORKFLOW SYSTEM")
    print("="*60)
    print("1. 🔄 Display Workflow Graph (LangGraph)")
    print("2. 💾 Save Workflow Image (PNG)")
    print("3. 🚀 Run SDLC Workflow")
    print("4. 📊 Show Implementation Status")
    print("5. ❌ Exit")
    print("="*60)

def show_implementation_status():
    """Show current implementation status with statistics"""
    
    visualizer = WorkflowVisualizer()
    visualizer.display_implementation_status()

# ==================== UPDATED run_sdlc_workflow FUNCTION ====================
# Add this to main.py (replace existing function)

async def run_sdlc_workflow():
    """Run the complete SDLC workflow"""
    
    print("\n🚀 Starting SDLC Workflow Execution...")
    
    # Get user input for requirements
    print("\n📝 Please enter your project requirements:")
    user_requirements = input("Requirements: ").strip()
    
    if not user_requirements:
        user_requirements = "Build a user authentication system with dashboard for managing customer data"
        print(f"Using default requirements: {user_requirements}")
    
    # Create the workflow
    workflow = create_sdlc_workflow()
    
    # Initial state
    initial_state = SDLCState(
        requirements=user_requirements,
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
    
    try:
        # Run the workflow
        print("\n⚡ Executing workflow...")
        result = await workflow.ainvoke(initial_state)
        
        # Display results with error handling
        print("\n" + "="*60)
        print("🎉 WORKFLOW EXECUTION RESULTS")
        print("="*60)
        print(f"📊 Current Stage: {result['current_stage']}")
        print(f"🕒 Timestamp: {result['timestamp']}")
        print(f"🔄 Iterations: {result['iteration_count']}")
        print(f"📚 User Stories Generated: {len(result['user_stories'])}")
        
        if result['user_stories']:
            print("\n📖 Generated User Stories:")
            for i, story in enumerate(result['user_stories'], 1):
                # Safe access to story fields with fallbacks
                story_id = story.get('id', f'US-{i:03d}')
                story_title = story.get('title', 'Untitled Story')
                story_priority = story.get('priority', 'Unknown')
                story_points = story.get('story_points', 'TBD')
                
                print(f"{i}. {story_id}: {story_title}")
                print(f"   Priority: {story_priority} | Points: {story_points}")
                
                # Show description if available
                if story.get('description'):
                    description = story['description']
                    if len(description) > 100:
                        description = description[:97] + "..."
                    print(f"   Description: {description}")
                
                # Show acceptance criteria count
                criteria_count = len(story.get('acceptance_criteria', []))
                print(f"   Acceptance Criteria: {criteria_count} criteria defined")
                print()
        
        # Show approval status
        approval_status = result.get('approval_status', 'Unknown')
        status_emoji = {"approved": "✅", "feedback": "⚠️", "rejected": "❌"}.get(approval_status, "❓")
        print(f"{status_emoji} Final Approval Status: {approval_status.upper()}")
        
        # Show review feedback if available
        if result.get('review_feedback'):
            feedback = result['review_feedback']
            if feedback.get('feedback'):
                print(f"\n💬 Latest Feedback: {feedback['feedback'][:200]}...")
        
        print("\n✅ Workflow completed successfully!")
        return result
        
    except Exception as e:
        print(f"\n❌ Error running workflow: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        
        # Try to show partial results if available
        try:
            if 'result' in locals() and result.get('user_stories'):
                print(f"\n📋 Partial Results Available:")
                print(f"   Stories generated: {len(result['user_stories'])}")
                print(f"   Current stage: {result.get('current_stage', 'unknown')}")
        except:
            pass
        
        return None
        
async def main():
    """Main application entry point"""
    
    # Create workflow first
    workflow = create_sdlc_workflow()
    visualizer = WorkflowVisualizer(workflow)
    
    while True:
        display_menu()
        
        try:
            choice = input("\nSelect an option (1-5): ").strip()
            
            if choice == '1':
                print("\n🔄 Displaying Workflow Graph...")
                visualizer.display_workflow_graph()
                input("\nPress Enter to continue...")
                
            elif choice == '2':
                print("\n💾 Saving Workflow Image...")
                filename = input("Enter filename (default: workflow.png): ").strip()
                if not filename:
                    filename = "workflow.png"
                if not filename.endswith('.png'):
                    filename += '.png'
                
                success = visualizer.save_workflow_image(filename)
                if success:
                    print(f"✅ Image saved successfully as {filename}")
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                result = await run_sdlc_workflow()
                if result:
                    input("\nPress Enter to continue...")
                
            elif choice == '4':
                show_implementation_status()
                input("\nPress Enter to continue...")
                
            elif choice == '5':
                print("\n👋 Goodbye! Thanks for using SDLC Workflow System!")
                sys.exit(0)
                
            else:
                print("\n❌ Invalid option. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using SDLC Workflow System!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    asyncio.run(main())