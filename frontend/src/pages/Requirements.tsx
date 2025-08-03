import { useState } from 'react'
import { useWorkflowStore } from '../store/workflowStore'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

const exampleRequirements = [
  {
    title: "Task Management App",
    content: "Build a task management app with user authentication, project creation, task assignment, real-time notifications, and progress tracking. Include role-based access control and integration with calendar systems."
  },
  {
    title: "E-commerce Platform", 
    content: "Develop an e-commerce platform with product catalog, shopping cart, secure payment processing, user accounts, order management, and admin dashboard. Include inventory management and shipping integration."
  },
  {
    title: "Learning Management System",
    content: "Create an LMS with course creation tools, student enrollment, progress tracking, quiz/assessment features, discussion forums, and gradebook functionality. Support multimedia content and mobile access."
  }
]

export default function Requirements() {
  const navigate = useNavigate()
  const { 
    requirements: currentRequirements,
    sessionId, 
    status,
    startWorkflow 
  } = useWorkflowStore()
  
  const [requirements, setRequirements] = useState(currentRequirements || '')
  const [projectName, setProjectName] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!requirements.trim()) {
      toast.error('Please enter project requirements')
      return
    }

    setIsSubmitting(true)

    try {
      await startWorkflow(requirements.trim(), projectName.trim() || undefined)
      toast.success('Workflow started successfully!')
      navigate('/user-stories')
    } catch (error: any) {
      toast.error(error.message || 'Failed to start workflow')
    } finally {
      setIsSubmitting(false)
    }
  }

  const loadExample = (example: typeof exampleRequirements[0]) => {
    setRequirements(example.content)
    setProjectName(example.title)
  }

  const isWorkflowActive = sessionId && status !== 'idle'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Project Requirements</h1>
        <p className="text-gray-600 mt-2">
          Define your project requirements to start the automated SDLC workflow
        </p>
      </div>

      {/* Active workflow warning */}
      {isWorkflowActive && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <span className="text-yellow-400 text-xl">[WARNING]</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">
                Workflow Currently Active
              </h3>
              <div className="mt-2 text-sm text-yellow-700">
                <p>
                  You have an active workflow running. Starting a new workflow will stop the current one.
                  Current status: <span className="font-medium">{status}</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main form */}
        <div className="lg:col-span-2">
          <div className="card">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="project-name" className="block text-sm font-medium text-gray-700 mb-2">
                  Project Name (Optional)
                </label>
                <input
                  type="text"
                  id="project-name"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  className="input-field"
                  placeholder="e.g., Task Management System"
                />
              </div>

              <div>
                <label htmlFor="requirements" className="block text-sm font-medium text-gray-700 mb-2">
                  Project Requirements *
                </label>
                <textarea
                  id="requirements"
                  value={requirements}
                  onChange={(e) => setRequirements(e.target.value)}
                  className="textarea-field"
                  rows={12}
                  placeholder="Describe your project requirements in detail. Include features, functionality, target users, technical constraints, and any specific requirements..."
                  required
                />
                <p className="mt-2 text-sm text-gray-500">
                  Be as detailed as possible. The AI will analyze and enhance your requirements.
                </p>
              </div>

              <div className="flex justify-between">
                <div className="text-sm text-gray-500">
                  {requirements.length} characters
                </div>
                <button
                  type="submit"
                  disabled={isSubmitting || !requirements.trim()}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? (
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 border border-white border-t-transparent rounded-full animate-spin" />
                      <span>Starting Workflow...</span>
                    </div>
                  ) : (
                    '[START] Start SDLC Workflow'
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Examples sidebar */}
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Example Projects</h3>
            <div className="space-y-3">
              {exampleRequirements.map((example, index) => (
                <button
                  key={index}
                  onClick={() => loadExample(example)}
                  className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <h4 className="font-medium text-gray-900 text-sm">{example.title}</h4>
                  <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                    {example.content.substring(0, 100)}...
                  </p>
                </button>
              ))}
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Tips for Better Requirements</h3>
            <ul className="text-sm text-gray-600 space-y-2">
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Be specific about features and functionality
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Mention target users and use cases
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Include technical constraints or preferences
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Specify integration requirements
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Define success criteria
              </li>
            </ul>
          </div>

          <div className="card bg-blue-50 border-blue-200">
            <h3 className="text-lg font-medium text-blue-900 mb-2">How it works</h3>
            <div className="text-sm text-blue-800 space-y-2">
              <p>1. [EDIT] Enter your requirements</p>
              <p>2. [BOOK] AI generates user stories</p>
              <p>3. [USER] Product owner review</p>
              <p>4. [DESIGN] Technical design creation</p>
              <p>5. [CODE] Code generation</p>
              <p>6. [TEST] Test case creation</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}