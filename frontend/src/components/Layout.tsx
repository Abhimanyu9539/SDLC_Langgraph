import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useWorkflowStore } from '../store/workflowStore'
import ProgressBar from './ProgressBar'
import StatusIndicator from './StatusIndicator'
import InterruptModal from './InterruptModal'
import {
  ClipboardDocumentListIcon,
  BookOpenIcon,
  PaintBrushIcon,
  CodeBracketIcon,
  BeakerIcon,
  ClockIcon,
  Squares2X2Icon
} from '@heroicons/react/24/outline'

interface LayoutProps {
  children: ReactNode
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: Squares2X2Icon },
  { name: 'Requirements', href: '/requirements', icon: ClipboardDocumentListIcon },
  { name: 'User Stories', href: '/user-stories', icon: BookOpenIcon },
  { name: 'Design', href: '/design', icon: PaintBrushIcon },
  { name: 'Code', href: '/code', icon: CodeBracketIcon },
  { name: 'Testing', href: '/testing', icon: BeakerIcon },
  { name: 'History', href: '/history', icon: ClockIcon },
]

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const { 
    sessionId, 
    status, 
    currentStage, 
    progress, 
    pendingInterrupt,
    isConnected,
    stopWorkflow 
  } = useWorkflowStore()

  const handleStopWorkflow = async () => {
    if (window.confirm('Are you sure you want to stop the current workflow?')) {
      await stopWorkflow()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-gray-900">
                🚀 SDLC Workflow Assistant
              </h1>
              <StatusIndicator />
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Connection status */}
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                <span className="text-sm text-gray-600">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              
              {/* Stop workflow button */}
              {sessionId && status !== 'idle' && (
                <button
                  onClick={handleStopWorkflow}
                  className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors"
                >
                  Stop Workflow
                </button>
              )}
            </div>
          </div>
          
          {/* Progress bar */}
          {sessionId && <ProgressBar />}
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <nav className="w-64 bg-white shadow-sm min-h-screen">
          <div className="p-4">
            <ul className="space-y-2">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href
                const Icon = item.icon
                
                return (
                  <li key={item.name}>
                    <Link
                      to={item.href}
                      className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-700'
                          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span className="font-medium">{item.name}</span>
                    </Link>
                  </li>
                )
              })}
            </ul>
          </div>
          
          {/* Workflow stats */}
          {sessionId && (
            <div className="border-t border-gray-200 p-4 mt-4">
              <h3 className="font-medium text-gray-900 mb-3">Workflow Stats</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Session ID:</span>
                  <span className="font-mono text-xs">{sessionId.slice(0, 8)}...</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Current Stage:</span>
                  <span className="capitalize">{currentStage.replace('_', ' ')}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Progress:</span>
                  <span>{Math.round(progress * 100)}%</span>
                </div>
              </div>
            </div>
          )}
        </nav>

        {/* Main content */}
        <main className="flex-1 p-6">
          <div className="max-w-6xl mx-auto">
            {children}
          </div>
        </main>
      </div>

      {/* Interrupt Modal */}
      {pendingInterrupt && <InterruptModal />}
    </div>
  )
}