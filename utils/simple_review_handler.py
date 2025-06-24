from typing import Dict, Any, List
from state.sdlc_state import SDLCState
from nodes.product_owner_review_node import _perform_po_review
from datetime import datetime

def ask_review_choice(stage_name: str, items_to_review) -> str:
    """Simple function to get user's review choice"""
    
    print(f"\n🛑 {stage_name} Review Required")
    print("="*50)
    
    # Show what needs review
    if isinstance(items_to_review, list) and items_to_review:
        print(f"📚 {len(items_to_review)} user stories to review:")
        for i, item in enumerate(items_to_review[:3], 1):
            title = item.get('title', 'Untitled')
            story_id = item.get('id', f'US-{i}')
            print(f"  {i}. {story_id}: {title}")
        if len(items_to_review) > 3:
            print(f"  ... and {len(items_to_review) - 3} more stories")
    else:
        print(f"📋 {stage_name} items ready for review")
    
    print(f"\n🤔 How would you like to handle this review?")
    print("1. 👤 I'll review it myself (Human Review)")
    print("2. 🤖 Let AI review it (AI Review)")  
    print("3. ⚡ Auto-approve and continue (Skip Review)")
    
    while True:
        choice = input("\nYour choice (1/2/3): ").strip()
        if choice == "1":
            print("✅ You chose: Human Review")
            return "human"
        elif choice == "2":
            print("✅ You chose: AI Review")
            return "ai"
        elif choice == "3":
            print("✅ You chose: Auto-approve")
            return "auto"
        else:
            print("❌ Please choose 1, 2, or 3")

def handle_review_choice(choice: str, stage_name: str, state: SDLCState) -> Dict[str, Any]:
    """Handle the user's review choice"""
    
    print(f"\n⚡ Processing {choice} review for {stage_name}...")
    
    if choice == "human":
        return handle_human_review(state)
    elif choice == "ai":
        return handle_ai_review(state)
    elif choice == "auto":
        return handle_auto_approve(state)
    else:
        # Fallback to auto-approve
        print("⚠️ Unknown choice, auto-approving...")
        return handle_auto_approve(state)

def handle_human_review(state: SDLCState) -> Dict[str, Any]:
    """Handle human review - collect user input"""
    
    print("👤 Starting Human Review")
    print("-" * 30)
    
    user_stories = state.get("user_stories", [])
    
    if not user_stories:
        return {"status": "approved", "feedback": "No stories to review", "reviewer": "Human"}
    
    # Show stories for review
    print("\n📖 Please review these user stories:\n")
    for i, story in enumerate(user_stories, 1):
        print(f"{i}. {story.get('id', 'N/A')}: {story.get('title', 'Untitled')}")
        print(f"   📝 {story.get('description', 'No description')}")
        print(f"   🎯 Priority: {story.get('priority', 'Unknown')} | Points: {story.get('story_points', 'TBD')}")
        
        # Show first 2 acceptance criteria
        criteria = story.get('acceptance_criteria', [])
        if criteria:
            print(f"   ✅ Acceptance Criteria:")
            for criterion in criteria[:2]:
                print(f"      • {criterion}")
            if len(criteria) > 2:
                print(f"      ... and {len(criteria) - 2} more")
        print()
    
    # Get user's overall decision
    print("🎯 Your overall assessment of these user stories:")
    print("1. ✅ Approve all - ready for next phase")
    print("2. ⚠️ Request changes - need improvements") 
    print("3. ❌ Reject all - start over")
    
    while True:
        decision = input("\nYour decision (1/2/3): ").strip()
        if decision in ['1', '2', '3']:
            break
        print("❌ Please choose 1, 2, or 3")
    
    # Get feedback if not approved
    feedback = ""
    if decision != '1':
        print(f"\n💬 Please provide feedback for your decision:")
        feedback = input("Your feedback: ").strip()
        if not feedback:
            feedback = "Human reviewer requested changes"
    
    # Map decision to status
    status_map = {
        '1': 'approved',
        '2': 'feedback', 
        '3': 'rejected'
    }
    
    status = status_map[decision]
    
    result = {
        "status": status,
        "feedback": feedback or f"Human review completed - {status}",
        "reviewer": "Human",
        "timestamp": datetime.now().isoformat(),
        "approval_status": status,
        "suggestions": [feedback] if feedback else [],
        "approved_stories": [s.get('id') for s in user_stories] if status == 'approved' else [],
        "rejected_stories": [s.get('id') for s in user_stories] if status == 'rejected' else [],
        "business_value_score": 8,
        "completeness_score": 8
    }
    
    print(f"✅ Human review completed with status: {status}")
    return result

def handle_ai_review(state: SDLCState) -> Dict[str, Any]:
    """Handle AI review - use existing AI review function"""
    
    print("🤖 Starting AI Review")
    print("-" * 25)
    
    try:
        # Use the existing AI review function
        result = _perform_po_review(
            state.get("user_stories", []), 
            state.get("requirements", "")
        )
        result["reviewer"] = "AI"
        print(f"✅ AI review completed with status: {result.get('status', 'unknown')}")
        return result
        
    except Exception as e:
        print(f"❌ AI review failed: {e}")
        print("🔄 Falling back to auto-approve...")
        return handle_auto_approve(state)

def handle_auto_approve(state: SDLCState) -> Dict[str, Any]:
    """Handle auto-approve - skip review entirely"""
    
    print("⚡ Auto-Approving")
    print("-" * 20)
    
    result = {
        "status": "approved",
        "feedback": "Auto-approved - review skipped by user choice",
        "reviewer": "Auto",
        "timestamp": datetime.now().isoformat(),
        "approval_status": "approved",
        "suggestions": [],
        "approved_stories": [s.get('id', f'US-{i}') for i, s in enumerate(state.get("user_stories", []), 1)],
        "rejected_stories": [],
        "business_value_score": 7,
        "completeness_score": 7
    }
    
    print("✅ Auto-approval completed")
    return result

def apply_review_result_and_continue(state: SDLCState, review_result: Dict[str, Any]) -> SDLCState:
    """Apply review result to state and prepare for continuation"""
    
    return {
        **state,
        "review_feedback": review_result,
        "approval_status": review_result.get("approval_status", review_result.get("status", "approved")),
        "current_stage": "product_owner_review_complete",
        "timestamp": datetime.now().isoformat(),
        # Add review to history
        "review_history": state.get("review_history", []) + [{
            "stage": "product_owner_review",
            "reviewer": review_result.get("reviewer", "Unknown"),
            "status": review_result.get("status", "approved"),
            "timestamp": review_result.get("timestamp", datetime.now().isoformat())
        }]
    }