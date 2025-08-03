import { useWorkflowStore } from '../store/workflowStore'

const stages = [
  { key: 'requirements', name: '📋 Requirements' },
  { key: 'user_stories', name: '📖 User Stories' },
  { key: 'po_review', name: '👤 PO Review' },
  { key: 'design', name: '🎨 Design' },
  { key: 'design_review', name: '👨‍💻 Design Review' },
  { key: 'code', name: '💻 Code' },
  { key: 'code_review', name: '🔍 Code Review' },
  { key: 'security', name: '🔒 Security' },
  { key: 'testing', name: '🧪 Testing' },
  { key: 'deployment', name: '🚀 Deployment' }
]

export default function ProgressBar() {
  const { currentStage, progress, status } = useWorkflowStore()
  
  const currentStageIndex = stages.findIndex(stage => stage.key === currentStage)
  
  return (
    <div className="pb-4">
      {/* Overall progress */}
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-700">
          Workflow Progress
        </span>
        <span className="text-sm text-gray-500">
          {Math.round(progress * 100)}% Complete
        </span>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
        <div
          className="bg-primary-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${progress * 100}%` }}
        />
      </div>
      
      {/* Stage indicators */}
      <div className="flex justify-between items-center text-xs">
        {stages.map((stage, index) => {
          const isCompleted = index < currentStageIndex
          const isCurrent = stage.key === currentStage
          const isFuture = index > currentStageIndex
          
          let statusClass = 'text-gray-400'
          if (isCompleted) {
            statusClass = 'text-green-600'
          } else if (isCurrent) {
            statusClass = 'text-primary-600 font-medium'
          }
          
          return (
            <div key={stage.key} className="flex flex-col items-center">
              <div
                className={`w-3 h-3 rounded-full mb-1 ${
                  isCompleted
                    ? 'bg-green-600'
                    : isCurrent
                    ? 'bg-primary-600'
                    : 'bg-gray-300'
                }`}
              />
              <span className={`${statusClass} text-center max-w-16 leading-tight`}>
                {stage.name}
              </span>
              {isCurrent && status === 'waiting_for_input' && (
                <div className="mt-1">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse" />
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}