import { useWorkflowStore } from '../store/workflowStore'
import { Link } from 'react-router-dom'

export default function Testing() {
  const { testCases, status, currentStage, sessionId } = useWorkflowStore()

  if (!sessionId) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">🧪</div>
        <h2 className="text-xl font-medium text-gray-900 mb-2">No Active Workflow</h2>
        <p className="text-gray-600 mb-6">
          Start a workflow to generate test cases.
        </p>
        <Link to="/requirements" className="btn-primary">
          Start Workflow
        </Link>
      </div>
    )
  }

  const hasTestCases = testCases && Object.keys(testCases).length > 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Test Cases</h1>
        <p className="text-gray-600 mt-2">
          AI-generated test cases and testing strategies
        </p>
      </div>

      {/* Status */}
      {currentStage === 'testing' && status === 'running' && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="w-4 h-4 border border-blue-600 border-t-transparent rounded-full animate-spin mr-3" />
            <span className="text-blue-800">Generating test cases and testing strategies...</span>
          </div>
        </div>
      )}

      {/* Test Cases */}
      {hasTestCases ? (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-900">
              Test Suites ({Object.keys(testCases).length})
            </h2>
            <button className="btn-secondary text-sm">
              📊 Generate Test Report
            </button>
          </div>

          <div className="grid gap-6">
            {Object.entries(testCases).map(([testSuite, tests]) => (
              <div key={testSuite} className="card">
                <div className="flex items-center space-x-2 mb-4">
                  <span className="text-2xl">🧪</span>
                  <h3 className="text-lg font-medium text-gray-900 capitalize">
                    {testSuite.replace(/[_-]/g, ' ')} Tests
                  </h3>
                </div>

                {Array.isArray(tests) ? (
                  <div className="space-y-3">
                    {tests.map((test: any, index: number) => (
                      <div key={index} className="p-3 bg-gray-50 rounded-lg">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-medium text-gray-900">
                            {test.name || `Test Case ${index + 1}`}
                          </h4>
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            test.priority === 'High' ? 'bg-red-100 text-red-800' :
                            test.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {test.priority || 'Medium'}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2">
                          {test.description || 'No description available'}
                        </p>
                        {test.steps && (
                          <div className="text-sm">
                            <span className="font-medium text-gray-900">Steps: </span>
                            <span className="text-gray-600">{test.steps.length} steps defined</span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-sm text-gray-600">
                    <pre className="whitespace-pre-wrap bg-gray-50 p-3 rounded-lg">
                      {typeof tests === 'object' ? JSON.stringify(tests, null, 2) : tests}
                    </pre>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Testing Strategy */}
          <div className="card bg-blue-50 border-blue-200">
            <h3 className="text-lg font-medium text-blue-900 mb-3">
              📋 Testing Strategy
            </h3>
            <div className="text-sm text-blue-800 space-y-2">
              <p>• Unit tests for individual components and functions</p>
              <p>• Integration tests for API endpoints and database interactions</p>
              <p>• End-to-end tests for critical user workflows</p>
              <p>• Performance tests for scalability and load handling</p>
              <p>• Security tests for authentication and data protection</p>
            </div>
          </div>
        </div>
      ) : (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <div className="text-4xl mb-4">🔬</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Test Cases Not Generated Yet
          </h3>
          <p className="text-gray-600">
            {status === 'running' && currentStage === 'testing' 
              ? 'AI is currently generating test cases and testing strategies...'
              : 'Test cases will be generated after the code generation phase.'
            }
          </p>
        </div>
      )}
    </div>
  )
}