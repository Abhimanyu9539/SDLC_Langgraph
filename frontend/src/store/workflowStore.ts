import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { WorkflowAPI } from '../services/api'

export interface UserStory {
  id: string
  title: string
  description: string
  priority: string
  story_points: number | string
  acceptance_criteria: string[]
}

export interface DesignDocs {
  title?: string
  summary?: string
  system_architecture?: any
  database_design?: any
  api_design?: any
  ui_design?: any
  security_performance?: any
  implementation_notes?: string
}

export interface ReviewItem {
  iteration: number
  reviewer: string
  status: string
  stage: string
  review_method: string
  feedback: string
  suggestions?: string[]
  business_value_score?: number
  completeness_score?: number
  technical_score?: number
  timestamp?: string
}

export interface PendingInterrupt {
  type: string
  stage: string
  message: string
  options: string[]
  timestamp: string
}

export interface WorkflowState {
  // Session management
  sessionId: string | null
  isConnected: boolean
  
  // Workflow status
  status: 'idle' | 'starting' | 'running' | 'waiting_for_input' | 'completed' | 'error'
  currentStage: string
  progress: number
  errorMessage: string | null
  
  // Workflow data
  requirements: string
  userStories: UserStory[]
  designDocs: DesignDocs
  codeFiles: Record<string, any>
  testCases: Record<string, any>
  reviewHistory: ReviewItem[]
  
  // Interrupts
  pendingInterrupt: PendingInterrupt | null
  
  // Actions
  startWorkflow: (requirements: string, projectName?: string) => Promise<void>
  stopWorkflow: () => Promise<void>
  respondToInterrupt: (response: string, additionalData?: any) => Promise<void>
  fetchStatus: () => Promise<void>
  connectWebSocket: () => void
  disconnectWebSocket: () => void
  
  // Internal
  setSessionId: (id: string | null) => void
  setStatus: (status: WorkflowState['status']) => void
  setCurrentStage: (stage: string) => void
  setProgress: (progress: number) => void
  setErrorMessage: (message: string | null) => void
  setUserStories: (stories: UserStory[]) => void
  setDesignDocs: (docs: DesignDocs) => void
  setCodeFiles: (files: Record<string, any>) => void
  setTestCases: (cases: Record<string, any>) => void
  setReviewHistory: (history: ReviewItem[]) => void
  setPendingInterrupt: (interrupt: PendingInterrupt | null) => void
  setConnected: (connected: boolean) => void
}

let websocket: WebSocket | null = null

export const useWorkflowStore = create<WorkflowState>()(
  devtools(
    (set, get) => ({
      // Initial state
      sessionId: null,
      isConnected: false,
      status: 'idle',
      currentStage: 'requirements',
      progress: 0,
      errorMessage: null,
      requirements: '',
      userStories: [],
      designDocs: {},
      codeFiles: {},
      testCases: {},
      reviewHistory: [],
      pendingInterrupt: null,

      // Actions
      startWorkflow: async (requirements: string, projectName?: string) => {
        set({ status: 'starting', requirements, errorMessage: null })
        
        try {
          const response = await WorkflowAPI.startWorkflow({ requirements, project_name: projectName })
          
          set({ 
            sessionId: response.session_id, 
            status: 'running',
            currentStage: 'user_stories',
            progress: 0.1
          })
          
          // Connect to WebSocket for real-time updates
          get().connectWebSocket()
          
          // Start polling for status updates
          const pollStatus = () => {
            if (get().sessionId && get().status !== 'completed' && get().status !== 'error') {
              get().fetchStatus()
              setTimeout(pollStatus, 2000) // Poll every 2 seconds
            }
          }
          pollStatus()
          
        } catch (error: any) {
          set({ 
            status: 'error', 
            errorMessage: error.message || 'Failed to start workflow' 
          })
        }
      },

      stopWorkflow: async () => {
        const { sessionId } = get()
        if (!sessionId) return
        
        try {
          await WorkflowAPI.stopWorkflow(sessionId)
          set({
            sessionId: null,
            status: 'idle',
            currentStage: 'requirements',
            progress: 0,
            pendingInterrupt: null
          })
          
          get().disconnectWebSocket()
        } catch (error: any) {
          set({ errorMessage: error.message || 'Failed to stop workflow' })
        }
      },

      respondToInterrupt: async (response: string, additionalData?: any) => {
        const { sessionId } = get()
        if (!sessionId) return
        
        try {
          await WorkflowAPI.respondToInterrupt(sessionId, { response, additional_data: additionalData })
          set({ pendingInterrupt: null, status: 'running' })
        } catch (error: any) {
          set({ errorMessage: error.message || 'Failed to respond to interrupt' })
        }
      },

      fetchStatus: async () => {
        const { sessionId } = get()
        if (!sessionId) return
        
        try {
          const status = await WorkflowAPI.getWorkflowStatus(sessionId)
          
          set({
            status: status.status as WorkflowState['status'],
            currentStage: status.current_stage,
            progress: status.progress,
            userStories: status.user_stories,
            designDocs: status.design_docs,
            codeFiles: status.code_files,
            testCases: status.test_cases,
            reviewHistory: status.review_history,
            pendingInterrupt: status.pending_interrupt,
            errorMessage: status.error_message
          })
        } catch (error: any) {
          set({ errorMessage: error.message || 'Failed to fetch status' })
        }
      },

      connectWebSocket: () => {
        const { sessionId } = get()
        if (!sessionId || websocket) return
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const wsUrl = `${protocol}//${window.location.host}/ws/${sessionId}`
        
        websocket = new WebSocket(wsUrl)
        
        websocket.onopen = () => {
          set({ isConnected: true })
          console.log('WebSocket connected')
        }
        
        websocket.onclose = () => {
          set({ isConnected: false })
          websocket = null
          console.log('WebSocket disconnected')
        }
        
        websocket.onerror = (error) => {
          console.error('WebSocket error:', error)
          set({ isConnected: false })
        }
        
        websocket.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data)
            
            switch (message.type) {
              case 'status_update':
                set({ status: message.status, currentStage: message.current_stage })
                break
                
              case 'progress_update':
                set({ currentStage: message.current_stage, progress: message.progress })
                break
                
              case 'interrupt_required':
                set({ pendingInterrupt: message.interrupt, status: 'waiting_for_input' })
                break
                
              case 'workflow_completed':
                set({ status: 'completed', progress: 1.0 })
                break
                
              case 'workflow_error':
                set({ status: 'error', errorMessage: message.error })
                break
                
              default:
                console.log('Unknown WebSocket message:', message)
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error)
          }
        }
        
        // Keep connection alive
        const keepAlive = setInterval(() => {
          if (websocket?.readyState === WebSocket.OPEN) {
            websocket.send(JSON.stringify({ type: 'ping' }))
          } else {
            clearInterval(keepAlive)
          }
        }, 30000)
      },

      disconnectWebSocket: () => {
        if (websocket) {
          websocket.close()
          websocket = null
          set({ isConnected: false })
        }
      },

      // Setters
      setSessionId: (id) => set({ sessionId: id }),
      setStatus: (status) => set({ status }),
      setCurrentStage: (stage) => set({ currentStage: stage }),
      setProgress: (progress) => set({ progress }),
      setErrorMessage: (message) => set({ errorMessage: message }),
      setUserStories: (stories) => set({ userStories: stories }),
      setDesignDocs: (docs) => set({ designDocs: docs }),
      setCodeFiles: (files) => set({ codeFiles: files }),
      setTestCases: (cases) => set({ testCases: cases }),
      setReviewHistory: (history) => set({ reviewHistory: history }),
      setPendingInterrupt: (interrupt) => set({ pendingInterrupt: interrupt }),
      setConnected: (connected) => set({ isConnected: connected }),
    }),
    {
      name: 'workflow-store',
    }
  )
)