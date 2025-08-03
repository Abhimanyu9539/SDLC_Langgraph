import axios, { AxiosResponse } from 'axios'

const API_BASE_URL = '/api'

// Configure axios
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request/Response types
export interface StartWorkflowRequest {
  requirements: string
  project_name?: string
  stakeholders?: string[]
}

export interface StartWorkflowResponse {
  session_id: string
  status: string
}

export interface WorkflowStatusResponse {
  session_id: string
  status: string
  current_stage: string
  progress: number
  user_stories: any[]
  design_docs: Record<string, any>
  code_files: Record<string, any>
  test_cases: Record<string, any>
  review_history: any[]
  pending_interrupt: any | null
  error_message: string | null
}

export interface InterruptResponseRequest {
  response: string
  additional_data?: Record<string, any>
}

export interface SessionInfo {
  session_id: string
  status: string
  current_stage: string
  progress: number
  created_at: string
}

// API functions
export class WorkflowAPI {
  static async startWorkflow(request: StartWorkflowRequest): Promise<StartWorkflowResponse> {
    const response: AxiosResponse<StartWorkflowResponse> = await apiClient.post('/workflow/start', request)
    return response.data
  }

  static async getWorkflowStatus(sessionId: string): Promise<WorkflowStatusResponse> {
    const response: AxiosResponse<WorkflowStatusResponse> = await apiClient.get(`/workflow/${sessionId}/status`)
    return response.data
  }

  static async respondToInterrupt(sessionId: string, request: InterruptResponseRequest): Promise<{ status: string }> {
    const response: AxiosResponse<{ status: string }> = await apiClient.post(`/workflow/${sessionId}/respond`, request)
    return response.data
  }

  static async stopWorkflow(sessionId: string): Promise<{ status: string }> {
    const response: AxiosResponse<{ status: string }> = await apiClient.delete(`/workflow/${sessionId}`)
    return response.data
  }

  static async listSessions(): Promise<SessionInfo[]> {
    const response: AxiosResponse<SessionInfo[]> = await apiClient.get('/workflow/sessions')
    return response.data
  }

  static async healthCheck(): Promise<{ message: string; timestamp: string }> {
    const response = await apiClient.get('/')
    return response.data
  }
}

// Error handler
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 404) {
      throw new Error('Workflow session not found')
    } else if (error.response?.status === 500) {
      throw new Error(error.response?.data?.detail || 'Internal server error')
    } else if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout - please try again')
    } else if (!error.response) {
      throw new Error('Network error - please check your connection')
    }
    
    throw new Error(error.response?.data?.detail || error.message || 'An unexpected error occurred')
  }
)