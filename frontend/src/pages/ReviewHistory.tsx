import { useWorkflowStore } from '../store/workflowStore'
import { Link } from 'react-router-dom'

export default function ReviewHistory() {
  const { reviewHistory, sessionId } = useWorkflowStore()

  if (!sessionId) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📚</div>
        <h2 className="text-xl font-medium text-gray-900 mb-2">No Active Workflow</h2>
        <p className="text-gray-600 mb-6">
          Start a workflow to track review history.
        </p>
        <Link to="/requirements" className="btn-primary">
          Start Workflow
        </Link>
      </div>
    )
  }

  if (reviewHistory.length === 0) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Review History</h1>
          <p className="text-gray-600 mt-2">
            Track all reviews and feedback throughout the workflow
          </p>
        </div>

        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <div className="text-4xl mb-4">📝</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No Reviews Yet
          </h3>
          <p className="text-gray-600">
            Review history will appear here as the workflow progresses and reviews are completed.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Review History</h1>
        <p className="text-gray-600 mt-2">
          Complete history of all reviews and feedback ({reviewHistory.length} reviews)
        </p>
      </div>

      {/* Timeline */}
      <div className="space-y-6">
        {reviewHistory.map((review, index) => {
          const isLast = index === reviewHistory.length - 1
          const stageEmoji = review.stage === 'product_owner_review' ? '👤' : 
                           review.stage === 'design_review' ? '👨‍💻' : 
                           review.stage === 'code_review' ? '🔍' : 
                           review.stage === 'security_review' ? '🔒' : '📋'
          
          return (
            <div key={index} className="relative">
              {/* Timeline line */}
              {!isLast && (
                <div className="absolute left-6 top-16 w-0.5 h-full bg-gray-200" />
              )}
              
              <div className="flex items-start space-x-4">
                {/* Timeline dot */}
                <div className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center ${
                  review.status === 'approved' ? 'bg-green-100' :
                  review.status === 'rejected' ? 'bg-red-100' :
                  'bg-yellow-100'
                }`}>
                  <span className="text-xl">{stageEmoji}</span>
                </div>
                
                {/* Review content */}
                <div className="flex-1 card">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">
                        {review.stage.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </h3>
                      <p className="text-sm text-gray-600">
                        Iteration {review.iteration} • Reviewed by {review.reviewer}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                        review.status === 'approved' ? 'bg-green-100 text-green-800' :
                        review.status === 'rejected' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {review.status.toUpperCase()}
                      </span>
                      {review.timestamp && (
                        <span className="text-xs text-gray-500">
                          {new Date(review.timestamp).toLocaleString()}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="space-y-3">
                    {/* Feedback */}
                    <div>
                      <h4 className="font-medium text-gray-900 mb-1">Feedback:</h4>
                      <p className="text-gray-700">{review.feedback}</p>
                    </div>

                    {/* Suggestions */}
                    {review.suggestions && review.suggestions.length > 0 && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Suggestions:</h4>
                        <ul className="space-y-1">
                          {review.suggestions.map((suggestion, suggestionIndex) => (
                            <li key={suggestionIndex} className="flex items-start">
                              <span className="text-blue-500 mr-2">💡</span>
                              <span className="text-gray-700 text-sm">{suggestion}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Scores */}
                    <div className="flex space-x-6 pt-2 border-t border-gray-100">
                      {review.business_value_score && (
                        <div className="text-sm">
                          <span className="text-gray-600">Business Value:</span>
                          <span className="ml-1 font-medium">{review.business_value_score}/10</span>
                        </div>
                      )}
                      {review.technical_score && (
                        <div className="text-sm">
                          <span className="text-gray-600">Technical:</span>
                          <span className="ml-1 font-medium">{review.technical_score}/10</span>
                        </div>
                      )}
                      {review.completeness_score && (
                        <div className="text-sm">
                          <span className="text-gray-600">Completeness:</span>
                          <span className="ml-1 font-medium">{review.completeness_score}/10</span>
                        </div>
                      )}
                      <div className="text-sm">
                        <span className="text-gray-600">Method:</span>
                        <span className="ml-1 font-medium capitalize">{review.review_method}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Summary Statistics */}
      <div className="card bg-gray-50">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Review Statistics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {reviewHistory.filter(r => r.status === 'approved').length}
            </div>
            <div className="text-sm text-gray-600">Approved</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">
              {reviewHistory.filter(r => r.status === 'rejected').length}
            </div>
            <div className="text-sm text-gray-600">Rejected</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {reviewHistory.filter(r => r.status === 'needs_revision').length}
            </div>
            <div className="text-sm text-gray-600">Needs Revision</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {Math.max(...reviewHistory.map(r => r.iteration), 0)}
            </div>
            <div className="text-sm text-gray-600">Max Iterations</div>
          </div>
        </div>
      </div>
    </div>
  )
}