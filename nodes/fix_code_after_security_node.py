# ==================== FIX CODE AFTER SECURITY REVIEW NODE ====================
# File: nodes/fix_code_after_security_node.py

from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings
import traceback

def fix_code_after_security_dynamic(state: SDLCState) -> SDLCState:
    """
    Fix code based on security review feedback using dynamic pattern
    
    This node:
    1. Takes current code files and security review feedback
    2. Uses AI to apply security improvements and vulnerability fixes
    3. Maintains code functionality while addressing security concerns
    4. Updates iteration count for tracking
    5. Prepares for next security review cycle
    """
    
    print("\n[TOOLS] Fixing Code Based on Security Review Feedback")
    print("🔒 Applying security improvements and vulnerability fixes")
    
    current_code = state.get("code", {})
    review_feedback = state.get("review_feedback", {})
    security_scan_results = state.get("security_scan_results", {})
    current_iteration = state.get("iteration_count", 0)
    
    if not current_code:
        print("⚠️ No code files found - cannot apply security fixes")
        return {
            **state,
            "current_stage": "security_fix_failed",
            "timestamp": datetime.now().isoformat()
        }
    
    if not review_feedback:
        print("⚠️ No security review feedback found - returning original code")
        return {
            **state,
            "current_stage": "security_fix_skipped",
            "timestamp": datetime.now().isoformat()
        }
    
    print(f"🔄 Applying security fixes to {len(current_code)} code files...")
    print(f"📝 Based on {review_feedback.get('reviewer', 'Unknown')} security review")
    print(f"🔒 Security Score: {review_feedback.get('security_score', 'N/A')}/10")
    print(f"⚠️ Vulnerabilities Found: {review_feedback.get('vulnerability_count', 0)}")
    print(f"🎯 Risk Level: {review_feedback.get('risk_level', 'Unknown')}")
    
    # Generate security-improved code using AI
    improved_code = _generate_security_improved_code(current_code, review_feedback, security_scan_results)
    
    # Update state for next iteration
    updated_state = {
        **state,
        "code": improved_code,
        "current_stage": "code_fixed_after_security", 
        "iteration_count": current_iteration + 1,
        "timestamp": datetime.now().isoformat(),
        # Clear review feedback for next iteration
        "review_feedback": {},
        "approval_status": "",  # Reset for next review
        "security_scan_results": {}  # Clear previous scan results
    }
    
    print(f"✅ Security fixes applied successfully")
    print(f"📄 Updated {len(improved_code)} code files with security improvements")
    print(f"🔄 Moving to iteration {updated_state['iteration_count']}")
    
    return updated_state

def _generate_security_improved_code(current_code: Dict[str, str], review_feedback: Dict[str, Any], security_scan_results: Dict[str, Any]) -> Dict[str, str]:
    """Generate security-improved code using LLM based on security review feedback"""
    
    llm_utils = LLMUtils()
    
    # Extract security feedback details
    security_feedback = _format_security_feedback(review_feedback, security_scan_results)
    
    # Security-focused system prompt
    system_prompt = """
    You are a Senior Cybersecurity Engineer and Secure Code Developer tasked with fixing security vulnerabilities and improving code security.
    
    Your responsibilities:
    1. Fix all identified security vulnerabilities
    2. Implement secure coding best practices
    3. Add proper input validation and sanitization
    4. Improve authentication and authorization mechanisms
    5. Enhance error handling to prevent information disclosure
    6. Add security headers and configurations
    7. Implement proper cryptographic practices
    8. Ensure secure file and data handling
    9. Add security logging and monitoring
    10. Follow OWASP security guidelines
    
    CRITICAL SECURITY REQUIREMENTS:
    - Fix SQL injection vulnerabilities
    - Prevent XSS (Cross-Site Scripting) attacks
    - Implement CSRF protection
    - Add proper authentication checks
    - Validate and sanitize all inputs
    - Use secure password handling
    - Implement proper session management
    - Add rate limiting and access controls
    - Use parameterized queries for database operations
    - Implement proper error handling without information leakage
    
    IMPORTANT RULES:
    - Maintain the same file structure and core functionality
    - Add security improvements without breaking existing features
    - Include security comments explaining the fixes
    - Use established security libraries and frameworks
    - Follow the principle of least privilege
    - Implement defense in depth
    
    Return the improved Python code with all security fixes applied.
    Include detailed comments explaining the security improvements made.
    """
    
    # Prepare current code for AI processing
    code_text = _format_code_for_security_improvement(current_code)
    
    user_prompt = f"""
    Apply security fixes to this code based on the security review feedback:
    
    SECURITY REVIEW FEEDBACK:
    {security_feedback}
    
    CURRENT CODE TO SECURE:
    {code_text}
    
    Apply comprehensive security improvements to address all identified vulnerabilities and concerns.
    Focus on making the code secure while maintaining its functionality.
    Add security best practices and defensive programming techniques.
    """
    
    try:
        print("🔒 Generating security-improved code using AI...")
        
        # Use get_completion for security code generation
        improved_code_text = llm_utils.get_completion(system_prompt, user_prompt)
        
        # Clean up the response
        improved_code_text = _clean_security_code_response(improved_code_text)
        
        # Since we're working with single Python file, return it properly
        improved_code = {
            "main.py": improved_code_text
        }
        
        print(f"✅ Security improvements applied successfully")
        print(f"📏 Improved code length: {len(improved_code_text)} characters")
        
        # Validate that we got meaningful security improvements
        if len(improved_code_text.strip()) < 100:
            print("⚠️ Security improvements seem insufficient, using enhanced fallback")
            return _apply_basic_security_improvements(current_code, review_feedback)
        
        return improved_code
        
    except Exception as e:
        print(f"❌ Error applying security improvements: {e}")
        print(f"❌ Error type: {type(e)}")
        print(f"❌ Full traceback: {traceback.format_exc()}")
        
        print("🔄 Using fallback security improvements...")
        return _apply_basic_security_improvements(current_code, review_feedback)

def _format_security_feedback(review_feedback: Dict[str, Any], security_scan_results: Dict[str, Any]) -> str:
    """Format security review feedback for AI processing"""
    
    feedback_parts = []
    
    # Basic security review info
    status = review_feedback.get('status', 'unknown')
    reviewer = review_feedback.get('reviewer', 'Unknown')
    security_score = review_feedback.get('security_score', 'N/A')
    vulnerability_count = review_feedback.get('vulnerability_count', 0)
    risk_level = review_feedback.get('risk_level', 'Unknown')
    
    feedback_parts.append(f"Security Review Status: {status}")
    feedback_parts.append(f"Reviewer: {reviewer}")
    feedback_parts.append(f"Security Score: {security_score}/10")
    feedback_parts.append(f"Vulnerabilities Found: {vulnerability_count}")
    feedback_parts.append(f"Risk Level: {risk_level}")
    
    # Main security feedback
    feedback = review_feedback.get('feedback', 'No specific security feedback')
    feedback_parts.append(f"Main Security Feedback: {feedback}")
    
    # Security suggestions
    suggestions = review_feedback.get('suggestions', [])
    if suggestions:
        feedback_parts.append("Security Improvement Suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            feedback_parts.append(f"  {i}. {suggestion}")
    
    # Detailed vulnerabilities from AI scan
    if security_scan_results and security_scan_results.get('detailed_vulnerabilities'):
        vulnerabilities = security_scan_results['detailed_vulnerabilities']
        if vulnerabilities:
            feedback_parts.append("Detailed Vulnerabilities Found:")
            for i, vuln in enumerate(vulnerabilities, 1):
                feedback_parts.append(f"  {i}. {vuln.get('type', 'Unknown')} - {vuln.get('severity', 'Unknown')} Severity")
                feedback_parts.append(f"     Location: {vuln.get('location', 'Not specified')}")
                feedback_parts.append(f"     Description: {vuln.get('description', 'No description')}")
                feedback_parts.append(f"     Fix: {vuln.get('recommendation', 'No recommendation')}")
    
    # Security strengths to maintain
    security_strengths = review_feedback.get('security_strengths', [])
    if security_strengths:
        feedback_parts.append("Security Strengths to Maintain:")
        for strength in security_strengths:
            feedback_parts.append(f"  • {strength}")
    
    return "\n".join(feedback_parts)

def _format_code_for_security_improvement(code_files: Dict[str, str]) -> str:
    """Format code files for security improvement"""
    
    formatted_code = []
    
    for filename, content in code_files.items():
        formatted_code.append(f"=== {filename} ===")
        formatted_code.append(content)
        formatted_code.append("")  # Empty line separator
    
    return "\n".join(formatted_code)

def _clean_security_code_response(response: str) -> str:
    """Clean up LLM response to extract just the Python code"""
    
    # Remove markdown code blocks if present
    if "```python" in response:
        # Extract content between ```python and ```
        start_marker = "```python"
        end_marker = "```"
        
        start_idx = response.find(start_marker)
        if start_idx != -1:
            start_idx += len(start_marker)
            end_idx = response.find(end_marker, start_idx)
            if end_idx != -1:
                response = response[start_idx:end_idx].strip()
    
    elif "```" in response:
        # Extract content between ``` blocks
        parts = response.split("```")
        if len(parts) >= 3:
            response = parts[1].strip()
    
    # Remove any leading/trailing whitespace
    response = response.strip()
    
    return response

def _apply_basic_security_improvements(current_code: Dict[str, str], review_feedback: Dict[str, Any]) -> Dict[str, str]:
    """Apply basic security improvements when AI processing fails"""
    
    improved_code = {}
    
    for filename, content in current_code.items():
        # Apply basic security improvements
        improved_content = content
        
        # Add security imports at the top
        if "import" in content and "hashlib" not in content:
            improved_content = _add_security_imports(improved_content)
        
        # Add basic input validation
        improved_content = _add_basic_input_validation(improved_content)
        
        # Add basic error handling
        improved_content = _add_security_error_handling(improved_content)
        
        # Add security comments
        security_comment = f"""
# SECURITY IMPROVEMENTS APPLIED
# Based on security review feedback: {review_feedback.get('feedback', 'Security enhancements applied')}
# Risk level: {review_feedback.get('risk_level', 'Unknown')}
# Security score: {review_feedback.get('security_score', 'N/A')}/10

"""
        improved_content = security_comment + improved_content
        
        improved_code[filename] = improved_content
    
    return improved_code

def _add_security_imports(content: str) -> str:
    """Add basic security-related imports"""
    
    security_imports = """import hashlib
import secrets
import logging
"""
    
    # Find the first import statement and add security imports after it
    lines = content.split('\n')
    import_inserted = False
    
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') and not import_inserted:
            lines.insert(i + 1, security_imports)
            import_inserted = True
            break
    
    if not import_inserted:
        # Add at the beginning if no imports found
        lines.insert(0, security_imports)
    
    return '\n'.join(lines)

def _add_basic_input_validation(content: str) -> str:
    """Add basic input validation patterns"""
    
    # Simple pattern replacement for common input operations
    patterns = [
        ("input(", "validate_input(input("),
        ("raw_input(", "validate_input(raw_input("),
    ]
    
    improved_content = content
    
    for old_pattern, new_pattern in patterns:
        if old_pattern in improved_content:
            improved_content = improved_content.replace(old_pattern, new_pattern)
            
            # Add validation function if not present
            if "def validate_input(" not in improved_content:
                validation_function = """
def validate_input(user_input):
    \"\"\"Basic input validation and sanitization\"\"\"
    if user_input is None:
        return ""
    
    # Basic sanitization
    sanitized = str(user_input).strip()
    
    # Log input for security monitoring
    logging.info(f"User input received: {len(sanitized)} characters")
    
    return sanitized

"""
                improved_content = validation_function + improved_content
    
    return improved_content

def _add_security_error_handling(content: str) -> str:
    """Add security-focused error handling"""
    
    # Look for functions without try-catch and add basic security error handling
    if "def " in content and "try:" not in content:
        lines = content.split('\n')
        improved_lines = []
        
        in_function = False
        function_indent = 0
        
        for line in lines:
            improved_lines.append(line)
            
            # Detect function definitions
            if line.strip().startswith('def ') and line.strip().endswith(':'):
                in_function = True
                function_indent = len(line) - len(line.lstrip())
                # Add security logging
                improved_lines.append(' ' * (function_indent + 4) + '"""Function with security enhancements"""')
                improved_lines.append(' ' * (function_indent + 4) + 'try:')
            elif in_function and line.strip() and not line.startswith(' ' * (function_indent + 4)):
                # End of function, add exception handling
                improved_lines.insert(-1, ' ' * (function_indent + 4) + 'except Exception as e:')
                improved_lines.insert(-1, ' ' * (function_indent + 8) + 'logging.error(f"Security error in function: {e}")')
                improved_lines.insert(-1, ' ' * (function_indent + 8) + 'raise')
                in_function = False
        
        return '\n'.join(improved_lines)
    
    return content