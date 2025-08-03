# SDLC Workflow React Frontend

This document explains how to run the new React frontend with the FastAPI backend.

## Architecture

### Backend (FastAPI)
- **Location**: `api/main.py`
- **Features**: REST API + WebSocket support for real-time updates
- **Port**: 8000

### Frontend (React + TypeScript)
- **Location**: `frontend/`
- **Features**: Modern React with TypeScript, Tailwind CSS, Zustand state management
- **Port**: 3000

## Setup Instructions

### 1. Install Backend Dependencies

```bash
# Install FastAPI requirements
pip install -r api_requirements.txt
```

### 2. Install Frontend Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### 3. Running the Application

#### Start Backend Server
```bash
# From project root directory
python api/main.py

# Or using uvicorn directly
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend Development Server
```bash
# From frontend directory
cd frontend
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Key Features

### ✅ Implemented Features

1. **FastAPI Backend**
   - REST API endpoints for workflow management
   - WebSocket support for real-time updates
   - Session management and interrupt handling
   - CORS support for React frontend

2. **React Frontend**
   - Modern React 18 with TypeScript
   - Tailwind CSS for styling
   - Zustand for state management
   - React Router for navigation
   - Real-time updates via WebSocket
   - Responsive design

3. **Core Components**
   - Dashboard with workflow overview
   - Requirements input form
   - User stories display
   - Design documents viewer
   - Code viewer with syntax highlighting
   - Test cases display
   - Review history timeline
   - Real-time progress tracking
   - Interrupt modal for user input

4. **Real-time Features**
   - Live workflow progress updates
   - WebSocket connection status indicator
   - Interrupt handling with modal dialogs
   - Automatic status polling

### 🚧 Integration Needed

The current implementation includes:
- Complete React frontend structure
- FastAPI backend with all endpoints
- WebSocket integration
- State management

**Still needed for full functionality:**
- Integration with existing `DynamicWorkflowRunner` (currently simulated)
- Connection to actual LangGraph workflow execution
- Real data flow from workflow nodes to API responses

## File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout.tsx           # Main layout with navigation
│   │   ├── ProgressBar.tsx      # Workflow progress indicator
│   │   ├── StatusIndicator.tsx  # Current status display
│   │   └── InterruptModal.tsx   # Modal for interrupt responses
│   ├── pages/
│   │   ├── Dashboard.tsx        # Main dashboard
│   │   ├── Requirements.tsx     # Requirements input
│   │   ├── UserStories.tsx      # User stories display
│   │   ├── Design.tsx           # Design documents
│   │   ├── Code.tsx             # Generated code viewer
│   │   ├── Testing.tsx          # Test cases
│   │   └── ReviewHistory.tsx    # Review timeline
│   ├── services/
│   │   └── api.ts               # API service layer
│   ├── store/
│   │   └── workflowStore.ts     # Zustand state management
│   ├── App.tsx                  # Main app component
│   └── main.tsx                 # App entry point
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json

api/
├── main.py                      # FastAPI application
└── __init__.py
```

## API Endpoints

### REST Endpoints
- `POST /workflow/start` - Start a new workflow
- `GET /workflow/{session_id}/status` - Get workflow status
- `POST /workflow/{session_id}/respond` - Respond to interrupts
- `DELETE /workflow/{session_id}` - Stop workflow
- `GET /workflow/sessions` - List active sessions

### WebSocket
- `GET /ws/{session_id}` - Real-time workflow updates

## Development

### Frontend Development
```bash
cd frontend
npm run dev      # Start development server
npm run build    # Build for production
npm run lint     # Run ESLint
```

### Backend Development
```bash
# Run with auto-reload
uvicorn api.main:app --reload

# Or using Python directly
python api/main.py
```

## Next Steps

1. **Complete Integration**: Connect the FastAPI backend to the existing LangGraph workflow
2. **Authentication**: Add user authentication and session security
3. **File Management**: Implement code file download and export features
4. **Error Handling**: Enhance error handling and user feedback
5. **Testing**: Add comprehensive tests for both frontend and backend
6. **Deployment**: Set up production deployment configuration

## Migration from Streamlit

The React frontend provides several advantages over Streamlit:
- **Better UX**: Modern, responsive interface with real-time updates
- **Scalability**: Separate frontend/backend architecture
- **Customization**: Full control over UI components and styling
- **Mobile Support**: Responsive design works on all devices
- **Real-time**: WebSocket support for live updates and interrupts
- **Maintainability**: Structured codebase with TypeScript support