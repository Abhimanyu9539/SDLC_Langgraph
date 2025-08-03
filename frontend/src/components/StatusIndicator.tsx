import { useWorkflowStore } from '../store/workflowStore'
import { motion } from 'framer-motion'

export default function StatusIndicator() {
  const { status, currentStage } = useWorkflowStore()
  
  const getStatusConfig = () => {
    switch (status) {
      case 'idle':
        return {
          text: 'Ready to Start',
          color: 'text-gray-600',
          bgColor: 'bg-gray-100',
          icon: '[PAUSE]'
        }
      case 'starting':
        return {
          text: 'Starting Workflow...',
          color: 'text-blue-600',
          bgColor: 'bg-blue-100',
          icon: '[START]'
        }
      case 'running':
        return {
          text: `Processing ${currentStage.replace('_', ' ')}...`,
          color: 'text-blue-600',
          bgColor: 'bg-blue-100',
          icon: '[RUN]'
        }
      case 'waiting_for_input':
        return {
          text: 'Waiting for Review',
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-100',
          icon: '[WAIT]'
        }
      case 'completed':
        return {
          text: 'Workflow Completed',
          color: 'text-green-600',
          bgColor: 'bg-green-100',
          icon: '[DONE]'
        }
      case 'error':
        return {
          text: 'Error Occurred',
          color: 'text-red-600',
          bgColor: 'bg-red-100',
          icon: '[ERROR]'
        }
      default:
        return {
          text: 'Unknown Status',
          color: 'text-gray-600',
          bgColor: 'bg-gray-100',
          icon: '[UNKNOWN]'
        }
    }
  }
  
  const config = getStatusConfig()
  
  return (
    <motion.div
      initial={{ scale: 0.95, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className={`flex items-center space-x-2 px-3 py-1 rounded-full ${config.bgColor}`}
    >
      <span className="text-lg">{config.icon}</span>
      <span className={`text-sm font-medium ${config.color}`}>
        {config.text}
      </span>
      {(status === 'running' || status === 'starting') && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="w-3 h-3 border border-blue-600 border-t-transparent rounded-full"
        />
      )}
    </motion.div>
  )
}