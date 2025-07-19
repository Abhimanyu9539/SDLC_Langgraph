import streamlit as st

st.set_page_config(page_title="SDLC LangGraph", layout="wide")

st.title("SDLC LangGraph Workflow App")
st.write("Welcome to the SDLC LangGraph Streamlit App! Select a workflow to begin.")

# Sidebar for workflow selection
workflow_options = [
    "Dynamic Interrupt Workflow",
    "Proper Interrupt Workflow",
    "SDLC Workflow"
]
selected_workflow = st.sidebar.selectbox("Choose a workflow", workflow_options)

st.sidebar.markdown("---")
st.sidebar.write("Project: SDLC_Langgraph")

# Main area
st.header(f"Selected Workflow: {selected_workflow}")

# Placeholder for workflow visualization or interaction
st.info("Workflow visualization and controls will appear here.")

# You can later import and run your workflow logic based on `selected_workflow`
# For example:
# if selected_workflow == "Dynamic Interrupt Workflow":
#     from workflow.dynamic_interrupt_workflow import run_dynamic_workflow
#     run_dynamic_workflow()
