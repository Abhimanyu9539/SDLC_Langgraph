"""
FastAPI Backend for LangGraph SDLC Workflow
Replaces Streamlit with REST API + WebSocket support
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import json
import uuid
from datetime import datetime
import logging
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import existing workflow components
from state.sdlc_state import SDLCState
from utils.dynamic_workflow_runner import DynamicWorkflowRunner
from workflow.dynamic_interrupt_workflow import create_dynamic_interrupt_workflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app instance
app = FastAPI(
    title="SDLC Workflow API",
    description="REST API for LangGraph-powered SDLC workflow automation",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for workflow sessions
workflow_sessions: Dict[str, Dict[str, Any]] = {}
websocket_connections: Dict[str, WebSocket] = {}

# Pydantic models for API
class WorkflowStartRequest(BaseModel):
    requirements: str
    project_name: Optional[str] = None
    stakeholders: Optional[List[str]] = None

class WorkflowStatusResponse(BaseModel):
    session_id: str
    status: str
    current_stage: str
    progress: float
    user_stories: List[Dict[str, Any]]
    design_docs: Dict[str, Any]
    code_files: Dict[str, Any]
    test_cases: Dict[str, Any]
    review_history: List[Dict[str, Any]]
    pending_interrupt: Optional[Dict[str, Any]]
    error_message: Optional[str]

class InterruptResponse(BaseModel):
    response: str
    additional_data: Optional[Dict[str, Any]] = None

# API Routes

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "SDLC Workflow API is running", "timestamp": datetime.now().isoformat()}

@app.post("/workflow/start")
async def start_workflow(request: WorkflowStartRequest) -> Dict[str, str]:
    """Start a new SDLC workflow"""
    
    session_id = str(uuid.uuid4())
    
    try:
        # Create initial state
        initial_state = SDLCState(
            requirements=request.requirements,
            user_stories=[],
            design_docs={},
            code={},
            test_cases=[],
            review_feedback={},
            approval_status="",
            current_stage="initial",
            iteration_count=0,
            project_id=session_id,
            timestamp=datetime.now().isoformat(),
            stakeholders=request.stakeholders or ["Product Owner", "Tech Lead", "QA Lead"],
            security_scan_results={},
            test_results={},
            deployment_status="",
            review_type="",
            human_review_requested=False,
            review_history=[]
        )
        
        # Initialize workflow runner
        workflow_runner = DynamicWorkflowRunner()
        
        # Store session data
        workflow_sessions[session_id] = {
            "state": initial_state,
            "runner": workflow_runner,
            "status": "started",
            "current_stage": "user_stories",
            "progress": 0.0,
            "error_message": None,
            "pending_interrupt": None,
            "created_at": datetime.now().isoformat()
        }
        
        # Start workflow in background
        asyncio.create_task(run_workflow_async(session_id))
        
        logger.info(f"Started workflow session {session_id}")
        return {"session_id": session_id, "status": "started"}
        
    except Exception as e:
        logger.error(f"Error starting workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start workflow: {str(e)}")

@app.get("/workflow/{session_id}/status")
async def get_workflow_status(session_id: str) -> WorkflowStatusResponse:
    """Get current workflow status"""
    
    if session_id not in workflow_sessions:
        raise HTTPException(status_code=404, detail="Workflow session not found")
    
    session = workflow_sessions[session_id]
    state = session["state"]
    
    return WorkflowStatusResponse(
        session_id=session_id,
        status=session["status"],
        current_stage=session["current_stage"],
        progress=session["progress"],
        user_stories=getattr(state, "user_stories", []),
        design_docs=getattr(state, "design_docs", {}),
        code_files=getattr(state, "code", {}),
        test_cases=getattr(state, "test_cases", {}),
        review_history=getattr(state, "review_history", []),
        pending_interrupt=session["pending_interrupt"],
        error_message=session["error_message"]
    )

@app.post("/workflow/{session_id}/respond")
async def respond_to_interrupt(session_id: str, response: InterruptResponse) -> Dict[str, str]:
    """Respond to a workflow interrupt"""
    
    if session_id not in workflow_sessions:
        raise HTTPException(status_code=404, detail="Workflow session not found")
    
    session = workflow_sessions[session_id]
    
    if not session["pending_interrupt"]:
        raise HTTPException(status_code=400, detail="No pending interrupt to respond to")
    
    try:
        # Store the response for the workflow to pick up
        session["interrupt_response"] = {
            "response": response.response,
            "additional_data": response.additional_data,
            "timestamp": datetime.now().isoformat()
        }
        session["pending_interrupt"] = None
        session["status"] = "running"
        
        # Notify via WebSocket if connected
        if session_id in websocket_connections:
            await websocket_connections[session_id].send_text(json.dumps({
                "type": "interrupt_response_received",
                "session_id": session_id,
                "response": response.response
            }))
        
        logger.info(f"Received interrupt response for session {session_id}")
        return {"status": "response_received"}
        
    except Exception as e:
        logger.error(f"Error handling interrupt response: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process response: {str(e)}")

@app.delete("/workflow/{session_id}")
async def stop_workflow(session_id: str) -> Dict[str, str]:
    """Stop and cleanup a workflow session"""
    
    if session_id not in workflow_sessions:
        raise HTTPException(status_code=404, detail="Workflow session not found")
    
    # Cleanup session
    del workflow_sessions[session_id]
    
    # Close WebSocket if connected
    if session_id in websocket_connections:
        await websocket_connections[session_id].close()
        del websocket_connections[session_id]
    
    logger.info(f"Stopped workflow session {session_id}")
    return {"status": "stopped"}

@app.get("/workflow/sessions")
async def list_sessions() -> List[Dict[str, Any]]:
    """List all active workflow sessions"""
    
    sessions = []
    for session_id, session in workflow_sessions.items():
        sessions.append({
            "session_id": session_id,
            "status": session["status"],
            "current_stage": session["current_stage"],
            "progress": session["progress"],
            "created_at": session["created_at"]
        })
    
    return sessions

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket connection for real-time workflow updates"""
    
    await websocket.accept()
    websocket_connections[session_id] = websocket
    
    logger.info(f"WebSocket connected for session {session_id}")
    
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle ping/pong for connection health
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
        if session_id in websocket_connections:
            del websocket_connections[session_id]
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        if session_id in websocket_connections:
            del websocket_connections[session_id]

# Background task to run workflows
async def run_workflow_async(session_id: str):
    """Run the workflow asynchronously and handle interrupts"""
    
    session = workflow_sessions[session_id]
    
    try:
        session["status"] = "running"
        
        # Notify WebSocket of status change
        if session_id in websocket_connections:
            await websocket_connections[session_id].send_text(json.dumps({
                "type": "status_update",
                "session_id": session_id,
                "status": "running",
                "current_stage": "user_stories"
            }))
        
        # Run the workflow (this is a simplified version - needs integration with actual workflow)
        runner = session["runner"]
        state = session["state"]
        
        # This would integrate with your existing DynamicWorkflowRunner
        # For now, simulate workflow execution
        stages = ["user_stories", "po_review", "design", "design_review", "code", "testing", "deployment"]
        
        for i, stage in enumerate(stages):
            session["current_stage"] = stage
            session["progress"] = (i + 1) / len(stages)
            
            # Simulate some work
            await asyncio.sleep(2)
            
            # Simulate interrupt on PO review
            if stage == "po_review" and not session.get("interrupt_response"):
                session["pending_interrupt"] = {
                    "type": "review_required",
                    "stage": stage,
                    "message": "Product Owner review required for user stories",
                    "options": ["approve", "request_changes", "reject"],
                    "timestamp": datetime.now().isoformat()
                }
                session["status"] = "waiting_for_input"
                
                # Notify via WebSocket
                if session_id in websocket_connections:
                    await websocket_connections[session_id].send_text(json.dumps({
                        "type": "interrupt_required",
                        "session_id": session_id,
                        "interrupt": session["pending_interrupt"]
                    }))
                
                # Wait for response
                while not session.get("interrupt_response") and session_id in workflow_sessions:
                    await asyncio.sleep(1)
                
                if session.get("interrupt_response"):
                    logger.info(f"Received response: {session['interrupt_response']['response']}")
                    session["interrupt_response"] = None
                    session["status"] = "running"
            
            # Notify progress
            if session_id in websocket_connections:
                await websocket_connections[session_id].send_text(json.dumps({
                    "type": "progress_update",
                    "session_id": session_id,
                    "current_stage": stage,
                    "progress": session["progress"]
                }))
        
        # Complete workflow
        session["status"] = "completed"
        session["progress"] = 1.0
        
        if session_id in websocket_connections:
            await websocket_connections[session_id].send_text(json.dumps({
                "type": "workflow_completed",
                "session_id": session_id,
                "status": "completed"
            }))
        
        logger.info(f"Workflow completed for session {session_id}")
        
    except Exception as e:
        logger.error(f"Workflow error for session {session_id}: {e}")
        session["status"] = "error"
        session["error_message"] = str(e)
        
        if session_id in websocket_connections:
            await websocket_connections[session_id].send_text(json.dumps({
                "type": "workflow_error",
                "session_id": session_id,
                "error": str(e)
            }))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)