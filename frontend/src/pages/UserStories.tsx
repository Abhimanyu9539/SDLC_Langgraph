import { useWorkflowStore } from '../store/workflowStore'
import { Link } from 'react-router-dom'

export default function UserStories() {
  const { userStories, status, currentStage, sessionId } = useWorkflowStore()

  if (!sessionId) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📖</div>
        <h2 className="text-xl font-medium text-gray-900 mb-2">No Active Workflow</h2>
        <p className="text-gray-600 mb-6">
          Start a workflow to generate user stories from your requirements.
        </p>
        <Link to="/requirements" className="btn-primary">
          Start Workflow
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">User Stories</h1>
        <p className="text-gray-600 mt-2">
          AI-generated user stories from your project requirements
        </p>
      </div>

      {/* Status */}
      {currentStage === 'user_stories' && status === 'running' && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="w-4 h-4 border border-blue-600 border-t-transparent rounded-full animate-spin mr-3" />
            <span className="text-blue-800">Generating user stories from requirements...</span>
          </div>
        </div>
      )}

      {/* User Stories */}
      {userStories.length > 0 ? (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-900">
              Generated Stories ({userStories.length})
            </h2>
            <div className="text-sm text-gray-600">
              Total Story Points: {userStories.reduce((sum, story) => 
                sum + (typeof story.story_points === 'number' ? story.story_points : 0), 0)}
            </div>
          </div>

          <div className="grid gap-4">
            {userStories.map((story, index) => (
              <div key={story.id || index} className="card">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-lg font-medium text-gray-900">
                    {story.id || `US-${(index + 1).toString().padStart(3, '0')}`}: {story.title}
                  </h3>
                  <div className="flex items-center space-x-3 text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      story.priority === 'High' ? 'bg-red-100 text-red-800' :
                      story.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {story.priority || 'Medium'}
                    </span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                      {story.story_points || 'TBD'} points
                    </span>
                  </div>
                </div>

                <p className="text-gray-700 mb-4">{story.description}</p>

                {story.acceptance_criteria && story.acceptance_criteria.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Acceptance Criteria:</h4>
                    <ul className="space-y-1">
                      {story.acceptance_criteria.map((criteria, criteriaIndex) => (
                        <li key={criteriaIndex} className="flex items-start">
                          <span className="text-green-500 mr-2 mt-1">✓</span>
                          <span className="text-gray-700 text-sm">{criteria}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <div className="text-4xl mb-4">⏳</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            User Stories Not Generated Yet
          </h3>
          <p className="text-gray-600">
            {status === 'running' && currentStage === 'user_stories' 
              ? 'AI is currently generating user stories from your requirements...'
              : 'User stories will be generated after starting the workflow.'
            }
          </p>
        </div>
      )}
    </div>
  )
}