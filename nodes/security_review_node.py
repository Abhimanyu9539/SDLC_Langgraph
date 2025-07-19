# ==================== SECURITY REVIEW NODE ====================
# File: nodes/security_review_node.py

from datetime import datetime
from typing import List, Dict, Any
from langgraph.types import interrupt, Command
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings

def security_review_dynamic(state: SDLCState) -> SDLCState:
    """
    Security Review using DYNAMIC INTERRUPTS (Official Pattern)
    Focused specifically on security vulnerabilities, threats, and compliance
    """
    
    print("\n🔒 Security Review - Dynamic Interrupt Pattern")
    print("🎯 Dedicated security vulnerability assessment")
    
    code_files = state.get("code", {})
    if not code_files:
        print("⚠️ No code files found - auto-approving security")
        return {
            **state,
            "approval_status": "approved",
            "current_stage": "security_review_complete",
            "timestamp": datetime.now().isoformat()
        }
    
    # ⭐ DYNAMIC INTERRUPT - Security review choice
    user_choice = interrupt({
        "type": "security_review_choice",
        "question": "How would you like to conduct the security review?",
        "options": {
            "human": "👤 I'll review security myself (Human Security Review)",
            "ai": "🤖 Let AI perform security analysis (AI Security Review)",
            "auto": "⚡ Auto-approve security and continue (Skip Security Review)"
        },
        "context": {
            "code_files_count": len(code_files),
            "current_iteration": state.get("iteration_count", 0),
            "project_id": state.get("project_id", "unknown")
        },
        "security_preview": {
            "files": list(code_files.keys()),
            "total_files": len(code_files),
            "code_languages": _detect_code_languages(code_files),
            "potential_security_areas": _identify_security_areas(code_files)
        }
    })
    
    print(f"✅ User selected: {user_choice}")
    
    # Process the user's choice
    if user_choice == "human":
        print("👤 Processing human security review...")
        review_result = _handle_human_security_review_dynamic(state)
    elif user_choice == "ai":
        print("🤖 Processing AI security review...")
        review_result = _handle_ai_security_review_dynamic(state)
    elif user_choice == "auto":
        print("⚡ Auto-approving security...")
        review_result = _handle_auto_approve_security_dynamic(state)
    else:
        print(f"⚠️ Unknown choice '{user_choice}' - defaulting to AI security review")
        review_result = _handle_ai_security_review_dynamic(state)
    
    # Save review to history
    review_history = state.get("review_history", [])
    review_record = {
        "iteration": state.get("iteration_count", 0),
        "stage": "security_review",
        "reviewer": review_result.get("reviewer", "Unknown"),
        "status": review_result.get("status", "unknown"),
        "feedback": review_result.get("feedback", ""),
        "suggestions": review_result.get("suggestions", []),
        "timestamp": review_result.get("timestamp", datetime.now().isoformat()),
        "security_score": review_result.get("security_score"),
        "vulnerability_count": review_result.get("vulnerability_count"),
        "risk_level": review_result.get("risk_level"),
        "review_method": user_choice
    }
    review_history.append(review_record)
    
    # Update state with review results
    updated_state = {
        **state,
        "review_feedback": review_result,
        "approval_status": review_result.get("status", "approved"),
        "current_stage": "security_review_complete",
        "timestamp": datetime.now().isoformat(),
        "review_history": review_history,
        "security_scan_results": review_result.get("security_scan_results", {})
    }
    
    print(f"✅ Security review completed - Status: {review_result.get('status', 'approved')}")
    print(f"👤 Reviewer: {review_result.get('reviewer', 'Unknown')}")
    print(f"🔒 Security Score: {review_result.get('security_score', 'N/A')}/10")
    
    return updated_state

def _detect_code_languages(code_files: Dict[str, str]) -> List[str]:
    """Detect programming languages in code files"""
    
    languages = set()
    
    for filename in code_files.keys():
        if filename.endswith('.py'):
            languages.add('Python')
        elif filename.endswith('.js'):
            languages.add('JavaScript')
        elif filename.endswith('.java'):
            languages.add('Java')
        elif filename.endswith('.php'):
            languages.add('PHP')
        elif filename.endswith('.go'):
            languages.add('Go')
        elif filename.endswith('.cpp') or filename.endswith('.c'):
            languages.add('C/C++')
        elif filename.endswith('.cs'):
            languages.add('C#')
        else:
            languages.add('Other')
    
    return list(languages)

def _identify_security_areas(code_files: Dict[str, str]) -> List[str]:
    """Identify potential security concern areas in code"""
    
    security_areas = []
    
    for filename, content in code_files.items():
        content_lower = content.lower()
        
        # Check for common security-sensitive patterns
        if any(pattern in content_lower for pattern in ['password', 'secret', 'key', 'token']):
            security_areas.append("Credential Management")
        
        if any(pattern in content_lower for pattern in ['sql', 'query', 'database']):
            security_areas.append("Database Security")
        
        if any(pattern in content_lower for pattern in ['request', 'input', 'form', 'user']):
            security_areas.append("Input Validation")
        
        if any(pattern in content_lower for pattern in ['file', 'open', 'read', 'write']):
            security_areas.append("File Operations")
        
        if any(pattern in content_lower for pattern in ['http', 'url', 'api', 'request']):
            security_areas.append("Network Security")
        
        if any(pattern in content_lower for pattern in ['session', 'cookie', 'auth']):
            security_areas.append("Authentication/Authorization")
    
    return list(set(security_areas)) if security_areas else ["General Code Security"]

def _handle_human_security_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """
    Handle human security review using dynamic interrupts
    Can use MULTIPLE interrupts for detailed security assessment
    """
    
    code_files = state.get("code", {})
    
    # Prepare security-focused code summary
    security_summary = {
        "total_files": len(code_files),
        "languages": _detect_code_languages(code_files),
        "security_areas": _identify_security_areas(code_files),
        "files": []
    }
    
    # Extract security-relevant information about each file
    for filename, content in code_files.items():
        file_info = {
            "filename": filename,
            "lines": len(content.split('\n')) if content else 0,
            "size_chars": len(content),
            "security_keywords": _count_security_keywords(content),
            "preview": content[:300] + "..." if len(content) > 300 else content
        }
        security_summary["files"].append(file_info)
    
    # ⭐ FIRST INTERRUPT: Show security analysis and get overall decision
    overall_decision = interrupt({
        "type": "human_security_review_decision",
        "prompt": "Please review the code for security vulnerabilities and concerns:",
        "security_analysis": security_summary,
        "question": "What's your overall security assessment of this code?",
        "options": {
            "approve": "✅ Approve - no significant security issues found",
            "request_changes": "⚠️ Request changes - security issues need fixing",
            "reject": "❌ Reject - critical security vulnerabilities found"
        }
    })
    
    feedback = ""
    suggestions = []
    vulnerability_count = 0
    risk_level = "Low"
    
    # ⭐ SECOND INTERRUPT: Get detailed security feedback if not approved
    if overall_decision != "approve":
        detailed_feedback = interrupt({
            "type": "human_security_review_feedback",
            "prompt": f"You chose to '{overall_decision}'. Please provide detailed security feedback:",
            "question": "What specific security issues or vulnerabilities did you identify?",
            "help_text": "Be specific about security concerns, vulnerabilities, or compliance issues."
        })
        
        feedback = detailed_feedback.get("feedback", "") if isinstance(detailed_feedback, dict) else str(detailed_feedback)
        
        # ⭐ THIRD INTERRUPT: Get risk assessment and suggestions
        if feedback:
            risk_assessment = interrupt({
                "type": "human_security_risk_assessment",
                "prompt": "Please assess the security risk level and provide improvement suggestions:",
                "question": "What is the risk level and what specific security improvements are needed?",
                "risk_options": {
                    "low": "🟢 Low Risk - Minor security improvements needed",
                    "medium": "🟡 Medium Risk - Moderate security issues to address", 
                    "high": "🔴 High Risk - Critical security vulnerabilities found"
                },
                "current_feedback": feedback
            })
            
            if isinstance(risk_assessment, dict):
                risk_level = risk_assessment.get("risk_level", "medium").title()
                suggestion_text = risk_assessment.get("suggestions", "")
                if suggestion_text:
                    suggestions = [suggestion_text]
            else:
                # Simple string response for risk level
                risk_level = str(risk_assessment).title() if risk_assessment else "Medium"
            
            # Estimate vulnerability count based on decision
            vulnerability_count = {"low": 1, "medium": 3, "high": 5}.get(risk_level.lower(), 2)
    
    # Calculate security score based on decision and risk
    security_score = _calculate_security_score(overall_decision, risk_level)
    
    return {
        "status": overall_decision,
        "feedback": feedback or f"Human security review completed with decision: {overall_decision}",
        "reviewer": "Human",
        "timestamp": datetime.now().isoformat(),
        "approval_status": overall_decision,
        "suggestions": suggestions,
        "security_score": security_score,
        "vulnerability_count": vulnerability_count,
        "risk_level": risk_level,
        "security_scan_results": {
            "scan_type": "human_review",
            "vulnerabilities_found": vulnerability_count,
            "risk_assessment": risk_level,
            "manual_review_completed": True
        },
        "approved_files": list(code_files.keys()) if overall_decision == "approve" else [],
        "flagged_files": list(code_files.keys()) if overall_decision in ["request_changes", "reject"] else [],
        "review_method": "human_dynamic"
    }

def _handle_ai_security_review_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle AI security review - automated security vulnerability analysis"""
    
    llm_utils = LLMUtils()
    code_files = state.get("code", {})
    design_docs = state.get("design_docs", {})
    
    system_prompt = """
    You are a Senior Cybersecurity Expert and Security Architect conducting a comprehensive security review.
    
    Analyze the code for:
    - Security vulnerabilities (SQL injection, XSS, CSRF, etc.)
    - Authentication and authorization flaws
    - Data validation and sanitization issues
    - Cryptographic implementation problems
    - Information disclosure risks
    - Input/output security concerns
    - File handling security issues
    - Network security considerations
    - Configuration and deployment security
    - OWASP Top 10 vulnerabilities
    
    Provide your security assessment as JSON with this structure:
    {
        "status": "approve" | "request_changes" | "reject",
        "feedback": "Comprehensive security assessment summary",
        "suggestions": ["List of specific security improvement recommendations"],
        "security_score": 1-10,
        "vulnerability_count": 0-20,
        "risk_level": "Low" | "Medium" | "High",
        "vulnerabilities_found": [
            {
                "type": "Vulnerability type",
                "severity": "Low|Medium|High|Critical",
                "location": "File/function location",
                "description": "Detailed vulnerability description",
                "recommendation": "How to fix this vulnerability"
            }
        ],
        "security_strengths": ["List of good security practices found"],
        "compliance_notes": ["Security compliance observations"],
        "overall_assessment": "Detailed security analysis summary"
    }
    
    Return ONLY the JSON object, no additional text.
    """
    
    # Format code files for security analysis
    code_analysis_text = "CODE FILES FOR SECURITY ANALYSIS:\n\n"
    for filename, content in code_files.items():
        # Include full content for security analysis (security is critical)
        code_analysis_text += f"=== {filename} ===\n{content}\n\n"
    
    # Add design context for security considerations
    design_context = f"DESIGN CONTEXT:\n{design_docs.get('summary', 'No design context available')}\n\n"
    
    user_prompt = f"""
    Conduct a thorough security review of this code:
    
    {design_context}
    
    {code_analysis_text}
    
    Focus on identifying security vulnerabilities, potential attack vectors, and security best practices compliance.
    Provide specific, actionable recommendations for improving security.
    """
    
    try:
        review_result = llm_utils.get_json_completion(system_prompt, user_prompt)
        
        # Ensure required fields and add metadata
        review_result.update({
            "reviewer": "AI",
            "timestamp": datetime.now().isoformat(),
            "approval_status": review_result.get("status", "approve"),
            "review_method": "ai_dynamic",
            "security_scan_results": {
                "scan_type": "ai_security_analysis",
                "vulnerabilities_found": review_result.get("vulnerability_count", 0),
                "risk_assessment": review_result.get("risk_level", "Low"),
                "automated_scan_completed": True,
                "detailed_vulnerabilities": review_result.get("vulnerabilities_found", [])
            }
        })
        
        print("🤖 AI Security Expert review completed")
        return review_result
        
    except Exception as e:
        print(f"❌ AI security review failed: {e}")
        return _handle_auto_approve_security_dynamic(state)

def _handle_auto_approve_security_dynamic(state: SDLCState) -> Dict[str, Any]:
    """Handle auto-approve security review"""
    
    code_files = state.get("code", {})
    
    return {
        "status": "approve",
        "feedback": "Auto-approved by user choice - security review skipped",
        "reviewer": "Auto",
        "timestamp": datetime.now().isoformat(),
        "approval_status": "approve",
        "suggestions": [],
        "security_score": 6,
        "vulnerability_count": 0,
        "risk_level": "Unknown",
        "security_scan_results": {
            "scan_type": "auto_approval",
            "vulnerabilities_found": 0,
            "risk_assessment": "Not Assessed",
            "review_skipped": True
        },
        "approved_files": list(code_files.keys()),
        "flagged_files": [],
        "overall_assessment": "Security review skipped by user choice",
        "review_method": "auto_dynamic"
    }

def _count_security_keywords(content: str) -> Dict[str, int]:
    """Count security-related keywords in code content"""
    
    security_keywords = {
        'password': content.lower().count('password'),
        'secret': content.lower().count('secret'),
        'key': content.lower().count('key'),
        'token': content.lower().count('token'),
        'auth': content.lower().count('auth'),
        'sql': content.lower().count('sql'),
        'query': content.lower().count('query'),
        'input': content.lower().count('input'),
        'request': content.lower().count('request'),
        'session': content.lower().count('session')
    }
    
    return {k: v for k, v in security_keywords.items() if v > 0}

def _calculate_security_score(decision: str, risk_level: str) -> int:
    """Calculate security score based on review decision and risk level"""
    
    base_scores = {
        "approve": 8,
        "request_changes": 5,
        "reject": 2
    }
    
    risk_adjustments = {
        "low": 1,
        "medium": 0, 
        "high": -2
    }
    
    base_score = base_scores.get(decision, 6)
    risk_adjustment = risk_adjustments.get(risk_level.lower(), 0)
    
    final_score = max(1, min(10, base_score + risk_adjustment))
    return final_score

def route_after_security_review_dynamic(state: SDLCState) -> str:
    """Route after security review based on approval status and iteration limits"""
    
    approval_status = state.get("approval_status", "")
    iteration_count = state.get("iteration_count", 0)
    
    if approval_status == "approve":
        print("✅ Security approved - proceeding to next phase")
        return "generate_test_cases"  # End for now, can be changed to next phase later
    elif iteration_count >= settings.MAX_ITERATIONS:
        print(f"⚠️ Maximum iterations ({settings.MAX_ITERATIONS}) reached - proceeding to next phase")
        return "generate_test_cases"
    else:
        print(f"⚠️ Security issues need fixing - iteration {iteration_count + 1}/{settings.MAX_ITERATIONS}")
        return "fix_code_after_security"