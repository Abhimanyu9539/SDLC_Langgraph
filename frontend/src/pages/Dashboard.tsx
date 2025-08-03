import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useWorkflowStore } from '../store/workflowStore'
import { 
  ClipboardDocumentListIcon,
  BookOpenIcon,
  PaintBrushIcon,
  CodeBracketIcon,
  BeakerIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

const quickActions = [
  {
    name: 'Start New Workflow',
    description: 'Begin with project requirements',
    href: '/requirements',
    icon: ClipboardDocumentListIcon,
    color: 'bg-blue-500'
  },
  {
    name: 'View User Stories',
    description: 'Review generated user stories',
    href: '/user-stories',
    icon: BookOpenIcon,
    color: 'bg-green-500'
  },
  {
    name: 'Design Documents',
    description: 'Technical design and architecture',
    href: '/design',
    icon: PaintBrushIcon,
    color: 'bg-purple-500'
  },
  {
    name: 'Generated Code',
    description: 'View and download code files',
    href: '/code',
    icon: CodeBracketIcon,
    color: 'bg-yellow-500'
  },
  {
    name: 'Test Cases',
    description: 'Review testing strategies',
    href: '/testing',
    icon: BeakerIcon,
    color: 'bg-red-500'
  },
  {
    name: 'Review History',
    description: 'Track workflow progress',
    href: '/history',
    icon: ClockIcon,
    color: 'bg-gray-500'
  }
]

export default function Dashboard() {
  const { 
    sessionId, 
    status, 
    currentStage, 
    progress,
    userStories,
    reviewHistory,
    fetchStatus
  } = useWorkflowStore()

  useEffect(() => {
    if (sessionId) {
      fetchStatus()
    }
  }, [sessionId, fetchStatus])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Manage your SDLC workflow with AI-powered automation
        </p>
      </div>

      {/* Current Workflow Status */}
      {sessionId && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Current Workflow</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">
                {Math.round(progress * 100)}%
              </div>
              <div className="text-sm text-gray-600">Progress</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {userStories.length}
              </div>
              <div className="text-sm text-gray-600">User Stories</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {reviewHistory.length}
              </div>
              <div className="text-sm text-gray-600">Reviews</div>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex justify-between items-center">
              <div>
                <span className="text-sm text-gray-600">Current Stage:</span>
                <span className="ml-2 font-medium capitalize">
                  {currentStage.replace('_', ' ')}
                </span>
              </div>
              <div>
                <span className="text-sm text-gray-600">Status:</span>
                <span className={`ml-2 px-2 py-1 text-xs rounded-full ${
                  status === 'completed' ? 'bg-green-100 text-green-800' :
                  status === 'error' ? 'bg-red-100 text-red-800' :
                  status === 'waiting_for_input' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-blue-100 text-blue-800'
                }`}>
                  {status.replace('_', ' ').toUpperCase()}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map((action) => {
            const Icon = action.icon
            return (
              <Link
                key={action.name}
                to={action.href}
                className="card hover:shadow-md transition-shadow duration-200 block"
              >
                <div className="flex items-start space-x-3">
                  <div className={`p-2 rounded-lg ${action.color}`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">{action.name}</h3>
                    <p className="text-sm text-gray-600 mt-1">{action.description}</p>
                  </div>
                </div>
              </Link>
            )
          })}
        </div>
      </div>

      {/* Recent Activity */}
      {reviewHistory.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
          <div className="space-y-3">
            {reviewHistory.slice(-3).reverse().map((review, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="flex-shrink-0">
                  <div className={`w-2 h-2 rounded-full ${
                    review.status === 'approved' ? 'bg-green-500' :
                    review.status === 'rejected' ? 'bg-red-500' :
                    'bg-yellow-500'
                  }`} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {review.stage.replace('_', ' ').toUpperCase()} Review
                  </p>
                  <p className="text-sm text-gray-600 truncate">
                    {review.feedback}
                  </p>
                </div>
                <div className="flex-shrink-0 text-xs text-gray-500">
                  {review.timestamp && new Date(review.timestamp).toLocaleDateString()}
                </div>
              </div>
            ))}
            
            {reviewHistory.length > 3 && (
              <div className="text-center">
                <Link 
                  to="/history" 
                  className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                >
                  View all {reviewHistory.length} reviews →
                </Link>
              </div>
            )}
          </div>
        </div>
      )}

      {/* No Active Workflow */}
      {!sessionId && (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">[ROCKET]</div>
          <h3 className="text-xl font-medium text-gray-900 mb-2">
            No Active Workflow
          </h3>
          <p className="text-gray-600 mb-6">
            Start by defining your project requirements to begin the automated SDLC workflow.
          </p>
          <Link to="/requirements" className="btn-primary">
            Start New Workflow
          </Link>
        </div>
      )}
    </div>
  )
}