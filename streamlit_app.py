"""
Streamlit Frontend for LangGraph SDLC Workflow
Main Application Entry Point

This is the main Streamlit application that provides a web interface
for the LangGraph SDLC workflow with dynamic interrupts.
"""

import streamlit as st
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
import sys
import os

# Add the project root to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our LangGraph workflow components
from state.sdlc_state import SDLCState
from utils.dynamic_workflow_runner import DynamicWorkflowRunner
from workflow.dynamic_interrupt_workflow import create_dynamic_interrupt_workflow

# Streamlit page configuration
st.set_page_config(
    page_title="SDLC Workflow Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    
    # Workflow state tracking
    if 'workflow_started' not in st.session_state:
        st.session_state.workflow_started = False
    
    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = "requirements"
    
    if 'workflow_state' not in st.session_state:
        st.session_state.workflow_state = None
    
    if 'workflow_runner' not in st.session_state:
        st.session_state.workflow_runner = None
    
    # User inputs and data
    if 'requirements' not in st.session_state:
        st.session_state.requirements = ""
    
    if 'user_stories' not in st.session_state:
        st.session_state.user_stories = []
    
    if 'design_docs' not in st.session_state:
        st.session_state.design_docs = {}
    
    if 'code_files' not in st.session_state:
        st.session_state.code_files = {}
    
    if 'test_cases' not in st.session_state:
        st.session_state.test_cases = {}
    
    # Workflow progress tracking
    if 'completed_stages' not in st.session_state:
        st.session_state.completed_stages = []
    
    if 'review_history' not in st.session_state:
        st.session_state.review_history = []
    
    # Interrupt handling
    if 'pending_interrupt' not in st.session_state:
        st.session_state.pending_interrupt = None
    
    if 'interrupt_response' not in st.session_state:
        st.session_state.interrupt_response = None

def display_header():
    """Display the main application header"""
    
    st.title("🚀 SDLC Workflow Assistant")
    st.markdown("**Automated Software Development Lifecycle with LangGraph & AI**")
    
    # Display workflow progress
    display_workflow_progress()

def display_workflow_progress():
    """Display overall workflow progress"""
    
    # Define all workflow stages
    stages = [
        ("requirements", "📋 Requirements"),
        ("user_stories", "📖 User Stories"),
        ("po_review", "👤 PO Review"),
        ("design", "🎨 Design"),
        ("design_review", "👨‍💻 Design Review"),
        ("code", "💻 Code"),
        ("code_review", "🔍 Code Review"),
        ("security", "🔒 Security"),
        ("testing", "🧪 Testing"),
        ("deployment", "🚀 Deployment")
    ]
    
    completed_stages = st.session_state.completed_stages
    current_stage = st.session_state.current_stage
    
    # Create progress bar
    progress_value = len(completed_stages) / len(stages)
    st.progress(progress_value, text=f"Workflow Progress: {len(completed_stages)}/{len(stages)} stages completed")
    
    # Create stage indicators
    cols = st.columns(len(stages))
    
    for i, (stage_key, stage_name) in enumerate(stages):
        with cols[i]:
            if stage_key in completed_stages:
                st.success(f"✅ {stage_name}")
            elif stage_key == current_stage:
                st.info(f"🔄 {stage_name}")
            else:
                st.write(f"⏳ {stage_name}")

def display_sidebar():
    """Display the sidebar with workflow controls and status"""
    
    with st.sidebar:
        st.header("🎛️ Workflow Controls")
        
        # Workflow status
        if st.session_state.workflow_started:
            st.success("✅ Workflow Active")
            st.write(f"**Current Stage:** {st.session_state.current_stage}")
            
            if st.button("🔄 Reset Workflow", type="secondary"):
                reset_workflow()
                st.rerun()
        else:
            st.info("⏸️ Workflow Not Started")
        
        st.divider()
        
        # Quick navigation
        st.header("📍 Quick Navigation")
        
        nav_options = {
            "📋 Requirements": "requirements",
            "📖 User Stories": "user_stories", 
            "🎨 Design Documents": "design",
            "💻 Code Generation": "code",
            "🧪 Test Cases": "testing",
            "📊 Review History": "history"
        }
        
        for label, page in nav_options.items():
            if st.button(label, key=f"nav_{page}"):
                st.session_state.current_page = page
                st.rerun()
        
        st.divider()
        
        # Workflow statistics
        st.header("📊 Statistics")
        
        if st.session_state.user_stories:
            st.metric("User Stories", len(st.session_state.user_stories))
        
        if st.session_state.code_files:
            st.metric("Code Files", len(st.session_state.code_files))
        
        if st.session_state.test_cases:
            st.metric("Test Files", len(st.session_state.test_cases))
        
        if st.session_state.review_history:
            st.metric("Reviews Completed", len(st.session_state.review_history))

def display_requirements_section():
    """Display the requirements input section"""
    
    st.header("📋 Project Requirements")
    st.write("Enter your project requirements to start the SDLC workflow.")
    
    with st.form("requirements_form"):
        requirements = st.text_area(
            "Project Requirements",
            value=st.session_state.requirements,
            height=200,
            placeholder="Describe your project requirements here...\n\nExample: Build a task management app with user authentication, project creation, and real-time notifications",
            help="Provide detailed requirements for your software project. The AI will analyze and enhance these requirements."
        )
        
        submitted = st.form_submit_button("🚀 Start SDLC Workflow", type="primary")
        
        if submitted and (requirements or "").strip():
            st.session_state.requirements = requirements or ""
            start_workflow(requirements or "")
            st.rerun()
        elif submitted:
            st.error("Please enter project requirements before starting the workflow.")

def start_workflow(requirements: str):
    """Start the SDLC workflow with the provided requirements"""
    
    try:
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
            project_id=f"STREAMLIT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            stakeholders=["Product Owner", "Tech Lead", "QA Lead"],
            security_scan_results={},
            test_results={},
            deployment_status="",
            review_type="",
            human_review_requested=False,
            review_history=[]
        )
        
        # Initialize workflow runner
        st.session_state.workflow_runner = DynamicWorkflowRunner()
        st.session_state.workflow_state = initial_state
        st.session_state.workflow_started = True
        st.session_state.current_stage = "user_stories"
        
        st.success("✅ Workflow started successfully!")
        st.info("🔄 Generating user stories from requirements...")
        
    except Exception as e:
        st.error(f"❌ Error starting workflow: {e}")

def display_user_stories_section():
    """Display user stories section"""
    
    st.header("📖 User Stories")
    
    if not st.session_state.workflow_started:
        st.warning("Please start the workflow by entering requirements first.")
        return
    
    if st.session_state.user_stories:
        st.success(f"✅ Generated {len(st.session_state.user_stories)} user stories")
        
        # Display user stories
        for i, story in enumerate(st.session_state.user_stories, 1):
            with st.expander(f"📖 {story.get('id', f'US-{i:03d}')}: {story.get('title', 'Untitled')}"):
                st.write(f"**Description:** {story.get('description', 'No description')}")
                st.write(f"**Priority:** {story.get('priority', 'Unknown')} | **Story Points:** {story.get('story_points', 'TBD')}")
                
                criteria = story.get('acceptance_criteria', [])
                if criteria:
                    st.write("**Acceptance Criteria:**")
                    for j, criterion in enumerate(criteria, 1):
                        st.write(f"  {j}. {criterion}")
        
        # Review section (this will be enhanced later)
        if st.button("👤 Review User Stories", type="primary"):
            st.session_state.current_stage = "po_review"
            st.rerun()
            
    else:
        if st.button("🔄 Generate User Stories", type="primary"):
            with st.spinner("Generating user stories..."):
                # This will be implemented with async workflow execution
                st.info("User story generation will be implemented in the next step")

def display_main_content():
    """Display the main content area based on current stage"""
    
    current_stage = st.session_state.current_stage
    current_page = st.session_state.get('current_page', current_stage)
    
    if current_page == "requirements" or not st.session_state.workflow_started:
        display_requirements_section()
    elif current_page == "user_stories":
        display_user_stories_section()
    elif current_page == "design":
        st.header("🎨 Design Documents")
        st.info("Design documents section - Coming in next iteration")
    elif current_page == "code":
        st.header("💻 Code Generation")
        st.info("Code generation section - Coming in next iteration")
    elif current_page == "testing":
        st.header("🧪 Test Cases")
        st.info("Test cases section - Coming in next iteration")
    elif current_page == "history":
        display_review_history()
    else:
        display_requirements_section()

def display_review_history():
    """Display review history"""
    
    st.header("📚 Review History")
    
    if not st.session_state.review_history:
        st.info("No reviews completed yet.")
        return
    
    for i, review in enumerate(st.session_state.review_history, 1):
        with st.expander(f"Review {i}: {review.get('stage', 'Unknown')} - {review.get('status', 'Unknown')}"):
            st.write(f"**Reviewer:** {review.get('reviewer', 'Unknown')}")
            st.write(f"**Status:** {review.get('status', 'Unknown')}")
            st.write(f"**Timestamp:** {review.get('timestamp', 'Unknown')}")
            st.write(f"**Feedback:** {review.get('feedback', 'No feedback')}")

def reset_workflow():
    """Reset the workflow to initial state"""
    
    # Reset all session state variables
    st.session_state.workflow_started = False
    st.session_state.current_stage = "requirements"
    st.session_state.workflow_state = None
    st.session_state.workflow_runner = None
    st.session_state.user_stories = []
    st.session_state.design_docs = {}
    st.session_state.code_files = {}
    st.session_state.test_cases = {}
    st.session_state.completed_stages = []
    st.session_state.review_history = []
    st.session_state.pending_interrupt = None
    st.session_state.interrupt_response = None
    
    # Keep requirements for convenience
    # st.session_state.requirements = ""

def main():
    """Main Streamlit application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Display main content
    display_main_content()
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8em;'>
        🚀 SDLC Workflow Assistant powered by LangGraph & Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()