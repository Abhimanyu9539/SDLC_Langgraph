import { useWorkflowStore } from '../store/workflowStore'
import { Link } from 'react-router-dom'

export default function Design() {
  const { designDocs, status, currentStage, sessionId } = useWorkflowStore()

  if (!sessionId) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">[DESIGN]</div>
        <h2 className="text-xl font-medium text-gray-900 mb-2">No Active Workflow</h2>
        <p className="text-gray-600 mb-6">
          Start a workflow to generate design documents.
        </p>
        <Link to="/requirements" className="btn-primary">
          Start Workflow
        </Link>
      </div>
    )
  }

  const hasDesignDocs = designDocs && Object.keys(designDocs).length > 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Design Documents</h1>
        <p className="text-gray-600 mt-2">
          Technical design and system architecture documentation
        </p>
      </div>

      {/* Status */}
      {currentStage === 'design' && status === 'running' && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="w-4 h-4 border border-blue-600 border-t-transparent rounded-full animate-spin mr-3" />
            <span className="text-blue-800">Generating technical design documents...</span>
          </div>
        </div>
      )}

      {/* Design Documents */}
      {hasDesignDocs ? (
        <div className="space-y-6">
          {/* Document Overview */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {designDocs.title || 'Technical Design Document'}
            </h2>
            {designDocs.summary && (
              <p className="text-gray-700 mb-4">{designDocs.summary}</p>
            )}
          </div>

          {/* Design Sections */}
          <div className="grid gap-6">
            {/* System Architecture */}
            {designDocs.system_architecture && (
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                  <span className="text-2xl mr-2">[ARCH]</span>
                  System Architecture
                </h3>
                <div className="space-y-3">
                  <p className="text-gray-700">
                    {designDocs.system_architecture.overview || 'Architecture overview not available'}
                  </p>
                  {designDocs.system_architecture.components && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Components:</h4>
                      <ul className="grid grid-cols-2 gap-2">
                        {designDocs.system_architecture.components.map((component: string, index: number) => (
                          <li key={index} className="flex items-center text-sm text-gray-700">
                            <span className="w-2 h-2 bg-blue-500 rounded-full mr-2" />
                            {component}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Database Design */}
            {designDocs.database_design && (
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                  <span className="text-2xl mr-2">[DB]</span>
                  Database Design
                </h3>
                <div className="space-y-3">
                  <p className="text-gray-700">
                    {designDocs.database_design.overview || 'Database design overview not available'}
                  </p>
                  {designDocs.database_design.entities && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Entities:</h4>
                      <ul className="grid grid-cols-2 gap-2">
                        {designDocs.database_design.entities.map((entity: string, index: number) => (
                          <li key={index} className="flex items-center text-sm text-gray-700">
                            <span className="w-2 h-2 bg-green-500 rounded-full mr-2" />
                            {entity}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* API Design */}
            {designDocs.api_design && (
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                  <span className="text-2xl mr-2">🔌</span>
                  API Design
                </h3>
                <div className="space-y-3">
                  <p className="text-gray-700">
                    {designDocs.api_design.overview || 'API design overview not available'}
                  </p>
                  {designDocs.api_design.core_endpoints && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Core Endpoints:</h4>
                      <div className="text-sm text-gray-600">
                        {designDocs.api_design.core_endpoints.length} endpoints defined
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* UI Design */}
            {designDocs.ui_design && (
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                  <span className="text-2xl mr-2">🎨</span>
                  UI Design
                </h3>
                <p className="text-gray-700">
                  {designDocs.ui_design.overview || 'UI design overview not available'}
                </p>
              </div>
            )}

            {/* Security & Performance */}
            {designDocs.security_performance && (
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                  <span className="text-2xl mr-2">🔒</span>
                  Security & Performance
                </h3>
                <p className="text-gray-700">
                  {designDocs.security_performance.overview || 'Security and performance considerations not available'}
                </p>
              </div>
            )}
          </div>

          {/* Implementation Notes */}
          {designDocs.implementation_notes && (
            <div className="card bg-yellow-50 border-yellow-200">
              <h3 className="text-lg font-medium text-yellow-900 mb-3">
                [NOTES] Implementation Notes
              </h3>
              <p className="text-yellow-800">{designDocs.implementation_notes}</p>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <div className="text-4xl mb-4">[RULER]</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Design Documents Not Generated Yet
          </h3>
          <p className="text-gray-600">
            {status === 'running' && currentStage === 'design' 
              ? 'AI is currently generating technical design documents...'
              : 'Design documents will be generated after user stories are approved.'
            }
          </p>
        </div>
      )}
    </div>
  )
}