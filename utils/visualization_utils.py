from typing import Dict, List
from IPython.display import Image, display
import io
import base64

class WorkflowVisualizer:
    def __init__(self, workflow=None):
        self.workflow = workflow
        
    def display_workflow_graph(self):
        """Display the actual LangGraph workflow using built-in Mermaid visualization"""
        if not self.workflow:
            print("❌ Workflow not provided. Please create workflow first.")
            return
            
        try:
            # Use LangGraph's built-in Mermaid PNG generation
            print("\n🔄 Generating workflow visualization...")
            
            # For Jupyter/IPython environments
            try:
                from IPython.display import Image, display
                display(Image(self.workflow.get_graph().draw_mermaid_png()))
                print("✅ Workflow graph displayed successfully!")
            except ImportError:
                # Fallback for non-Jupyter environments
                print("📋 IPython not available. Generating Mermaid code instead...")
                self.display_workflow_mermaid_code()
                
        except Exception as e:
            print(f"❌ Error generating workflow graph: {e}")
            print("📋 Falling back to Mermaid code generation...")
            self.display_workflow_mermaid_code()
    
    def display_workflow_mermaid_code(self):
        """Display Mermaid code from the actual LangGraph workflow"""
        if not self.workflow:
            print("❌ Workflow not provided. Please create workflow first.")
            return
            
        try:
            # Get Mermaid code from LangGraph
            mermaid_code = self.workflow.get_graph().draw_mermaid()
            
            print("\n" + "="*80)
            print("🔄 ACTUAL WORKFLOW MERMAID DIAGRAM")
            print("="*80)
            print("Copy the following code to https://mermaid.live for visualization:")
            print("\n" + "-"*80)
            print(mermaid_code)
            print("-"*80)
            
        except Exception as e:
            print(f"❌ Error getting Mermaid code: {e}")
            self.display_fallback_mermaid()
    
    def display_fallback_mermaid(self):
        """Fallback Mermaid diagram showing current implementation"""
        mermaid_diagram = """
graph TD
    A[ui_user_inputs_requirements] --> B[auto_generate_user_stories]
    B --> END[End]
    
    %% Styling for current implementation
    classDef implemented fill:#90EE90,stroke:#006400,stroke-width:3px
    classDef endpoint fill:#FFB6C1,stroke:#FF1493,stroke-width:2px
    
    class A,B implemented
    class END endpoint
        """
        
        print("\n" + "="*80)
        print("🔄 CURRENT WORKFLOW STATE (Fallback)")
        print("="*80)
        print("Copy the following code to https://mermaid.live for visualization:")
        print("\n" + "-"*80)
        print(mermaid_diagram.strip())
        print("-"*80)
    
    def save_workflow_image(self, filename="workflow_graph.png"):
        """Save workflow graph as PNG image"""
        if not self.workflow:
            print("❌ Workflow not provided. Please create workflow first.")
            return False
            
        try:
            # Get PNG data from LangGraph
            png_data = self.workflow.get_graph().draw_mermaid_png()
            
            # Save to file
            with open(filename, "wb") as f:
                f.write(png_data)
            
            print(f"✅ Workflow graph saved as {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving workflow graph: {e}")
            return False
    
    def get_workflow_progress(self) -> Dict[str, int]:
        """Get current workflow progress statistics"""
        
        implemented_nodes = [
            "ui_user_inputs_requirements",
            "auto_generate_user_stories"
        ]
        
        planned_nodes = [
            "product_owner_review",
            "revise_user_stories", 
            "create_design_documents",
            "design_review",
            "generate_code",
            "code_review", 
            "fix_code_after_review",
            "security_review",
            "fix_code_after_security",
            "write_test_cases",
            "test_cases_review",
            "fix_test_cases",
            "qa_testing",
            "fix_code_after_qa",
            "deployment",
            "monitoring_and_feedback",
            "maintenance_and_updates"
        ]
        
        total_nodes = len(implemented_nodes) + len(planned_nodes)
        
        return {
            "implemented": len(implemented_nodes),
            "planned": len(planned_nodes),
            "total": total_nodes,
            "progress_percentage": round((len(implemented_nodes) / total_nodes) * 100, 1)
        }
    
    def display_implementation_status(self):
        """Display implementation status with current workflow nodes"""
        progress = self.get_workflow_progress()
        
        print("\n" + "="*80)
        print("📊 IMPLEMENTATION STATUS")
        print("="*80)
        
        print("\n✅ IMPLEMENTED NODES:")
        print("  • ui_user_inputs_requirements")
        print("  • auto_generate_user_stories")
        
        print("\n🔜 PLANNED NODES:")
        planned = [
            "product_owner_review", "revise_user_stories", "create_design_documents",
            "design_review", "generate_code", "code_review", "fix_code_after_review", 
            "security_review", "fix_code_after_security", "write_test_cases",
            "test_cases_review", "fix_test_cases", "qa_testing", "fix_code_after_qa",
            "deployment", "monitoring_and_feedback", "maintenance_and_updates"
        ]
        
        for i, node in enumerate(planned, 1):
            print(f"  {i:2d}. {node}")
        
        print(f"\n📊 PROGRESS STATISTICS:")
        print(f"  • Implemented: {progress['implemented']} nodes")
        print(f"  • Planned: {progress['planned']} nodes") 
        print(f"  • Total: {progress['total']} nodes")
        print(f"  • Completion: {progress['progress_percentage']}%")
        print("="*80)
    
    def display_implementation_status_mermaid(self):
        """Display implementation status as Mermaid diagram (for backward compatibility)"""
        self.display_implementation_status()
    
    def display_workflow_mermaid(self):
        """Display workflow as Mermaid code (for backward compatibility)"""
        self.display_workflow_mermaid_code()
