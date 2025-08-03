# ==================== COMPLETE SDLC DYNAMIC INTERRUPT WORKFLOW ====================
# File: workflow/dynamic_interrupt_workflow.py

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state.sdlc_state import SDLCState

# Core workflow nodes
from nodes.requirements_node import ui_user_inputs_requirements
from nodes.user_stories_node import auto_generate_user_stories

# Product Owner Review cycle
from nodes.dynamic_review_node import (
    product_owner_review_dynamic, 
    revise_user_stories_dynamic, 
    route_after_po_review_dynamic
)

# Design phase
from nodes.design_documents_node import create_design_documents
from nodes.design_review_node import (
    design_review_dynamic,
    revise_design_documents_dynamic,
    route_after_design_review_dynamic
)

# Code generation phase
from nodes.generate_code_node import generate_code

# Code review cycle
from nodes.code_review_node import (
    code_review_dynamic,
    route_after_code_review_dynamic
)
from nodes.fix_code_after_review_node import fix_code_after_review_dynamic

# Security review cycle
from nodes.security_review_node import (
    security_review_dynamic,
    route_after_security_review_dynamic
)
from nodes.fix_code_after_security_node import fix_code_after_security_dynamic

# Test cases cycle
from nodes.test_cases_generation_node import generate_test_cases
from nodes.test_cases_review_node import (
    test_cases_review_dynamic,
    route_after_test_review_dynamic
)
from nodes.revise_test_cases_node import revise_test_cases_dynamic

# Deployment
from nodes.deployment_node import deployment

def create_dynamic_interrupt_workflow():
    """
    Create Complete SDLC workflow using DYNAMIC INTERRUPTS (Official LangGraph Pattern)
    
    Complete workflow flow:
    Requirements → User Stories → PO Review → Design Documents → Design Review → 
    Code Generation → Code Review → Security Review → Test Generation → Test Review → Deployment
    
    Key features:
    - Dynamic interrupts with interrupt() calls INSIDE nodes
    - Complete review cycles with iteration support
    - Comprehensive SDLC coverage from requirements to deployment
    - Human/AI/Auto review options for all review phases
    """
    
    # Initialize the graph
    workflow = StateGraph(SDLCState)
    
    # ===== ADD ALL NODES TO THE GRAPH =====
    
    # Core workflow nodes
    workflow.add_node("ui_user_inputs_requirements", ui_user_inputs_requirements)
    workflow.add_node("auto_generate_user_stories", auto_generate_user_stories)
    
    # Product Owner Review cycle
    workflow.add_node("product_owner_review", product_owner_review_dynamic)
    workflow.add_node("revise_user_stories", revise_user_stories_dynamic)
    
    # Design phase
    workflow.add_node("create_design_documents", create_design_documents)
    workflow.add_node("design_review", design_review_dynamic)
    workflow.add_node("revise_design_documents", revise_design_documents_dynamic)
    
    # Code generation and review cycle
    workflow.add_node("generate_code", generate_code)
    workflow.add_node("code_review", code_review_dynamic)
    workflow.add_node("fix_code_after_review", fix_code_after_review_dynamic)
    
    # Security review cycle
    workflow.add_node("security_review", security_review_dynamic)
    workflow.add_node("fix_code_after_security", fix_code_after_security_dynamic)
    
    # Test cases cycle
    workflow.add_node("generate_test_cases", generate_test_cases)
    workflow.add_node("test_cases_review", test_cases_review_dynamic)
    workflow.add_node("revise_test_cases", revise_test_cases_dynamic)
    
    # Deployment
    workflow.add_node("deployment", deployment)
    
    # ===== SET ENTRY POINT =====
    workflow.set_entry_point("ui_user_inputs_requirements")
    
    # ===== DEFINE WORKFLOW EDGES =====
    
    # Initial flow: Requirements → User Stories → PO Review
    workflow.add_edge("ui_user_inputs_requirements", "auto_generate_user_stories")
    workflow.add_edge("auto_generate_user_stories", "product_owner_review")
    
    # ===== PRODUCT OWNER REVIEW CYCLE =====
    workflow.add_conditional_edges(
        "product_owner_review",
        route_after_po_review_dynamic,
        {
            "create_design_documents": "create_design_documents",  # Approved → Design phase
            "revise_user_stories": "revise_user_stories"  # Needs revision
        }
    )
    # Route back to PO review after user story revision
    workflow.add_edge("revise_user_stories", "product_owner_review")
    
    # ===== DESIGN PHASE =====
    workflow.add_edge("create_design_documents", "design_review")
    
    # ===== DESIGN REVIEW CYCLE =====
    workflow.add_conditional_edges(
        "design_review",
        route_after_design_review_dynamic,
        {
            "generate_code": "generate_code",  # Approved → Code generation
            "revise_design_documents": "revise_design_documents"  # Needs revision
        }
    )
    # Route back to design review after design revision
    workflow.add_edge("revise_design_documents", "design_review")
    
    # ===== CODE GENERATION AND REVIEW CYCLE =====
    workflow.add_edge("generate_code", "code_review")
    
    workflow.add_conditional_edges(
        "code_review",
        route_after_code_review_dynamic,
        {
            "security_review": "security_review",  # Approved → Security review
            "fix_code_after_review": "fix_code_after_review"  # Needs fixes
        }
    )
    # Route back to code review after code fixes
    workflow.add_edge("fix_code_after_review", "code_review")
    
    # ===== SECURITY REVIEW CYCLE =====
    workflow.add_conditional_edges(
        "security_review",
        route_after_security_review_dynamic,
        {
            "generate_test_cases": "generate_test_cases",  # Approved → Test generation
            "fix_code_after_security": "fix_code_after_security"  # Needs security fixes
        }
    )
    # Route back to security review after security fixes
    workflow.add_edge("fix_code_after_security", "security_review")
    
    # ===== TEST CASES CYCLE =====
    workflow.add_edge("generate_test_cases", "test_cases_review")
    
    workflow.add_conditional_edges(
        "test_cases_review",
        route_after_test_review_dynamic,
        {
            "deployment": "deployment",  # Approved → Deployment
            "revise_test_cases": "revise_test_cases"  # Needs test improvements
        }
    )
    # Route back to test review after test revision
    workflow.add_edge("revise_test_cases", "test_cases_review")
    
    # ===== DEPLOYMENT (END) =====
    workflow.add_edge("deployment", END)
    
    # ===== COMPILE WORKFLOW =====
    compiled_workflow = workflow.compile(
        checkpointer=MemorySaver()  # Only checkpointer needed for dynamic interrupts
    )
    
    # ===== WORKFLOW INFORMATION =====
    print("[TOOLS] Complete SDLC Dynamic Interrupt Workflow Created")
    print("🎯 Uses interrupt() INSIDE nodes (official LangGraph pattern)")
    print("⚡ Resume with Command(resume=value)")
    print("\n🆕 Complete SDLC Coverage:")
    print("   📋 Requirements Capture & Enhancement")
    print("   📖 User Stories Generation")
    print("   👤 Product Owner Review (with interrupts & iteration)")
    print("   🎨 Design Documents Creation")
    print("   👨‍💻 Design Review (with interrupts & iteration)")
    print("   💻 Code Generation (Python)")
    print("   🔍 Code Review (with interrupts & iteration)")
    print("   🔒 Security Review (with interrupts & iteration)")
    print("   🧪 Test Cases Generation")
    print("   📊 Test Cases Review (with interrupts & iteration)")
    print("   🚀 Deployment Readiness")
    print("\n🔄 Complete Iteration Support:")
    print("   • User Stories ↔ Product Owner Review")
    print("   • Design Documents ↔ Design Review")
    print("   • Code ↔ Code Review")
    print("   • Code ↔ Security Review")
    print("   • Test Cases ↔ Test Cases Review")
    print("\n🛑 Dynamic Interrupts for:")
    print("   • Product Owner Review (human/AI/auto)")
    print("   • Design Review (human/AI/auto)")
    print("   • Code Review (human/AI/auto)")
    print("   • Security Review (human/AI/auto)")
    print("   • Test Cases Review (human/AI/auto)")
    
    return compiled_workflow