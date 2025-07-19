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
    workflow.add_node("Input Requirements", ui_user_inputs_requirements)
    workflow.add_node("Auto Generate User Stories", auto_generate_user_stories)
    
    # Product Owner Review cycle
    workflow.add_node("Product Owner Review", product_owner_review_dynamic)
    workflow.add_node("Revise User Stories", revise_user_stories_dynamic)
    
    # Design phase
    workflow.add_node("Create Design Docs", create_design_documents)
    workflow.add_node("Design Review", design_review_dynamic)
    workflow.add_node("Revise Design Docs", revise_design_documents_dynamic)
    
    # Code generation and review cycle
    workflow.add_node("Generate Code", generate_code)
    workflow.add_node("Code Review", code_review_dynamic)
    workflow.add_node("Fix Code After Review", fix_code_after_review_dynamic)
    
    # Security review cycle
    workflow.add_node("Security Review", security_review_dynamic)
    workflow.add_node("Fix Code after Security", fix_code_after_security_dynamic)
    
    # Test cases cycle
    workflow.add_node("Generate Test Cases", generate_test_cases)
    workflow.add_node("Test Cases Review", test_cases_review_dynamic)
    workflow.add_node("Revise Test Cases", revise_test_cases_dynamic)
    
    # Deployment
    workflow.add_node("Deployment", deployment)
    
    # ===== SET ENTRY POINT =====
    workflow.set_entry_point("Input Requirements")
    
    # ===== DEFINE WORKFLOW EDGES =====
    
    # Initial flow: Requirements → User Stories → PO Review
    workflow.add_edge("Input Requirements", "Auto Generate User Stories")
    workflow.add_edge("Auto Generate User Stories", "Product Owner Review")
    
    # ===== PRODUCT OWNER REVIEW CYCLE =====
    workflow.add_conditional_edges(
        "Product Owner Review",
        route_after_po_review_dynamic,
        {
            "Create Design Docs": "Create Design Docs",  # Approved → Design phase
            "Revise User Stories": "Revise User Stories"  # Needs revision
        }
    )
    # Route back to PO review after user story revision
    workflow.add_edge("Revise User Stories", "Product Owner Review")
    
    # ===== DESIGN PHASE =====
    workflow.add_edge("Create Design Docs", "Design Review")
    
    # ===== DESIGN REVIEW CYCLE =====
    workflow.add_conditional_edges(
        "Design Review",
        route_after_design_review_dynamic,
        {
            "Generate Code": "Generate Code",  # Approved → Code generation
            "Revise Design Docs": "Revise Design Docs"  # Needs revision
        }
    )
    # Route back to design review after design revision
    workflow.add_edge("Revise Design Docs", "Design Review")
    
    # ===== CODE GENERATION AND REVIEW CYCLE =====
    workflow.add_edge("Generate Code", "Code Review")
    
    workflow.add_conditional_edges(
        "Code Review",
        route_after_code_review_dynamic,
        {
            "Security Review": "Security Review",  # Approved → Security review
            "Fix Code After Review": "Fix Code After Review"  # Needs fixes
        }
    )
    # Route back to code review after code fixes
    workflow.add_edge("Fix Code After Review", "Code Review")
    
    # ===== SECURITY REVIEW CYCLE =====
    workflow.add_conditional_edges(
        "Security Review",
        route_after_security_review_dynamic,
        {
            "Generate Test Cases": "Generate Test Cases",  # Approved → Test generation
            "Fix Code after Security": "Fix Code after Security"  # Needs security fixes
        }
    )
    # Route back to security review after security fixes
    workflow.add_edge("Fix Code after Security", "Security Review")
    
    # ===== TEST CASES CYCLE =====
    workflow.add_edge("Generate Test Cases", "Test Cases Review")
    
    workflow.add_conditional_edges(
        "Test Cases Review",
        route_after_test_review_dynamic,
        {
            "Deployment": "Deployment",  # Approved → Deployment
            "Revise Test Cases": "Revise Test Cases"  # Needs test improvements
        }
    )
    # Route back to test review after test revision
    workflow.add_edge("Revise Test Cases", "Test Cases Review")
    
    # ===== DEPLOYMENT (END) =====
    workflow.add_edge("Deployment", END)
    
    # ===== COMPILE WORKFLOW =====
    compiled_workflow = workflow.compile(
        checkpointer=MemorySaver()  # Only checkpointer needed for dynamic interrupts
    )
    
    # ===== WORKFLOW INFORMATION =====
    print("🔧 Complete SDLC Dynamic Interrupt Workflow Created")
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