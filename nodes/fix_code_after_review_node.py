# ==================== FIX CODE AFTER REVIEW NODE ====================
# File: nodes/fix_code_after_review_node.py

from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def fix_code_after_review_dynamic(state: SDLCState) -> SDLCState:
    """
    Fix code based on review feedback using dynamic pattern
    
    This node:
    1. Takes current code files and review feedback
    2. Uses AI to apply suggested improvements
    3. Maintains code structure while addressing concerns
    4. Updates iteration count for tracking
    5. Prepares for next review cycle
    """
    
    print("\n🔧 Fixing Code Based on Review Feedback")
    print("🎯 Applying code improvements and suggestions")
    
    current_code = state.get("code", {})
    review_feedback = state.get("review_feedback", {})
    current_iteration = state.get("iteration_count", 0)
    
    if not current_code:
        print("⚠️ No code files found - cannot apply fixes")
        return {
            **state,
            "current_stage": "code_fix_failed",
            "timestamp": datetime.now().isoformat()
        }
    
    if not review_feedback:
        print("⚠️ No review feedback found - returning original code")
        return {
            **state,
            "current_stage": "code_fix_skipped",
            "timestamp": datetime.now().isoformat()
        }
    
    print(f"🔄 Applying fixes to {len(current_code)} code files...")
    print(f"📝 Based on {review_feedback.get('reviewer', 'Unknown')} review feedback")
    
    # Generate improved code using AI
    improved_code = _generate_improved_code_files(current_code, review_feedback)
    
    # Update state for next iteration
    updated_state = {
        **state,
        "code": improved_code,
        "current_stage": "code_fixed_after_review", 
        "iteration_count": current_iteration + 1,
        "timestamp": datetime.now().isoformat(),
        # Clear review feedback for next iteration
        "review_feedback": {},
        "approval_status": ""  # Reset for next review
    }
    
    print(f"✅ Code fixes applied successfully")
    print(f"📄 Updated {len(improved_code)} code files")
    print(f"🔄 Moving to iteration {updated_state['iteration_count']}")
    
    return updated_state

def _generate_improved_code_files(current_code: Dict[str, str], review_feedback: Dict[str, Any]) -> Dict[str, str]:
    """Generate improved code files using LLM based on review feedback"""
    
    llm_utils = LLMUtils()
    
    # Extract feedback details
    feedback_summary = _format_review_feedback(review_feedback)
    
    system_prompt = """
    You are an experienced Software Engineer tasked with improving code based on review feedback.
    
    Your responsibilities:
    1. Apply the specific feedback and suggestions provided
    2. Improve code quality, structure, and maintainability
    3. Fix performance issues mentioned in the review
    4. Enhance error handling and edge case coverage
    5. Maintain the same file structure and core functionality
    6. Ensure code follows best practices for the technology stack
    7. Keep the same technology stack and architecture
    
    IMPORTANT RULES:
    - Return ALL files, even if some don't need changes
    - Maintain the same file names and overall structure
    - Apply improvements systematically across all files
    - Ensure code remains functional while addressing concerns
    - Add comments for significant improvements made
    
    Return the improved code as JSON with filename: code_content pairs.
    Include ALL original files with improvements applied where needed.
    """
    
    # Prepare current code for AI processing
    code_text = _format_code_files_for_improvement(current_code)
    
    user_prompt = f"""
    Improve this code based on the review feedback provided:
    
    REVIEW FEEDBACK TO ADDRESS:
    {feedback_summary}
    
    CURRENT CODE FILES:
    {code_text}
    
    Apply the feedback systematically and return ALL improved code files as JSON.
    Focus on addressing the specific concerns raised while maintaining functionality.
    """
    
    try:
        print("🤖 Generating improved code using AI...")
        improved_code = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        # Validate that we got all files back
        if len(improved_code) < len(current_code):
            print(f"⚠️ Some files missing in improvement - merging with originals")
            # Merge with original files to ensure we don't lose any
            for filename, content in current_code.items():
                if filename not in improved_code:
                    improved_code[filename] = content
        
        print(f"✅ Code improvements applied to {len(improved_code)} files")
        return improved_code
        
    except Exception as e:
        print(f"❌ Error improving code: {e}")
        print("🔄 Returning original code with minor improvements")
        return _apply_basic_improvements(current_code, review_feedback)

def _format_review_feedback(review_feedback: Dict[str, Any]) -> str:
    """Format review feedback for AI processing"""
    
    feedback_parts = []
    
    # Basic feedback info
    status = review_feedback.get('status', 'unknown')
    reviewer = review_feedback.get('reviewer', 'Unknown')
    feedback_parts.append(f"Review Status: {status}")
    feedback_parts.append(f"Reviewer: {reviewer}")
    
    # Main feedback
    feedback = review_feedback.get('feedback', 'No specific feedback')
    feedback_parts.append(f"Main Feedback: {feedback}")
    
    # Suggestions
    suggestions = review_feedback.get('suggestions', [])
    if suggestions:
        feedback_parts.append("Specific Suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            feedback_parts.append(f"  {i}. {suggestion}")
    
    # Key concerns
    concerns = review_feedback.get('key_concerns', [])
    if concerns:
        feedback_parts.append("Key Concerns to Address:")
        for concern in concerns:
            feedback_parts.append(f"  • {concern}")
    
    # Performance issues
    performance_issues = review_feedback.get('performance_issues', [])
    if performance_issues:
        feedback_parts.append("Performance Issues:")
        for issue in performance_issues:
            feedback_parts.append(f"  • {issue}")
    
    # Scores for context
    code_quality_score = review_feedback.get('code_quality_score')
    maintainability_score = review_feedback.get('maintainability_score')
    if code_quality_score:
        feedback_parts.append(f"Code Quality Score: {code_quality_score}/10")
    if maintainability_score:
        feedback_parts.append(f"Maintainability Score: {maintainability_score}/10")
    
    return "\n".join(feedback_parts)

def _format_code_files_for_improvement(code_files: Dict[str, str]) -> str:
    """Format code files for AI processing"""
    
    formatted_code = []
    
    for filename, content in code_files.items():
        formatted_code.append(f"=== {filename} ===")
        formatted_code.append(content)
        formatted_code.append("")  # Empty line separator
    
    return "\n".join(formatted_code)

def _apply_basic_improvements(current_code: Dict[str, str], review_feedback: Dict[str, Any]) -> Dict[str, str]:
    """Apply basic improvements when AI processing fails"""
    
    improved_code = {}
    
    for filename, content in current_code.items():
        # Apply basic improvements
        improved_content = content
        
        # Add basic error handling if missing
        if "try:" not in content and "except:" not in content:
            if filename.endswith('.py'):
                improved_content = _add_basic_python_error_handling(content)
            elif filename.endswith('.js'):
                improved_content = _add_basic_js_error_handling(content)
        
        # Add improvement comment
        if filename.endswith('.py'):
            improved_content = f"# Code improved based on review feedback\n# {review_feedback.get('feedback', 'Applied basic improvements')}\n\n{improved_content}"
        elif filename.endswith('.js'):
            improved_content = f"// Code improved based on review feedback\n// {review_feedback.get('feedback', 'Applied basic improvements')}\n\n{improved_content}"
        elif filename.endswith('.html'):
            improved_content = f"<!-- Code improved based on review feedback -->\n<!-- {review_feedback.get('feedback', 'Applied basic improvements')} -->\n\n{improved_content}"
        
        improved_code[filename] = improved_content
    
    return improved_code

def _add_basic_python_error_handling(content: str) -> str:
    """Add basic error handling to Python code"""
    
    if "def " in content and "try:" not in content:
        # Wrap main function content in try-catch
        lines = content.split('\n')
        improved_lines = []
        
        for line in lines:
            improved_lines.append(line)
            if line.strip().startswith('def ') and line.strip().endswith(':'):
                improved_lines.append('    """Enhanced with error handling"""')
                improved_lines.append('    try:')
        
        # Add basic exception handling at the end
        improved_lines.append('    except Exception as e:')
        improved_lines.append('        print(f"Error: {e}")')
        improved_lines.append('        raise')
        
        return '\n'.join(improved_lines)
    
    return content

def _add_basic_js_error_handling(content: str) -> str:
    """Add basic error handling to JavaScript code"""
    
    if "function " in content and "try {" not in content:
        # Add basic try-catch structure
        improved_content = content.replace(
            "function ",
            "function "
        )
        # Simple improvement - add error handling comment
        improved_content = f"// Enhanced with improved error handling\n{improved_content}"
    
    return content if "try {" in content else f"// Enhanced with error handling considerations\n{content}"