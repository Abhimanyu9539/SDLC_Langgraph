import { useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { Fragment } from 'react'
import { useWorkflowStore } from '../store/workflowStore'
import toast from 'react-hot-toast'
import { XMarkIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

export default function InterruptModal() {
  const { pendingInterrupt, respondToInterrupt, setPendingInterrupt } = useWorkflowStore()
  const [selectedOption, setSelectedOption] = useState('')
  const [customResponse, setCustomResponse] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (!pendingInterrupt) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!selectedOption && !customResponse.trim()) {
      toast.error('Please select an option or provide a custom response')
      return
    }

    setIsSubmitting(true)

    try {
      const response = selectedOption || customResponse.trim()
      await respondToInterrupt(response, { timestamp: new Date().toISOString() })
      toast.success('Response submitted successfully')
    } catch (error: any) {
      toast.error(error.message || 'Failed to submit response')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCancel = () => {
    setPendingInterrupt(null)
    setSelectedOption('')
    setCustomResponse('')
  }

  return (
    <Transition appear show={!!pendingInterrupt} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={() => {}}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <ExclamationTriangleIcon className="w-6 h-6 text-yellow-600" />
                    <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-gray-900">
                      Review Required
                    </Dialog.Title>
                  </div>
                  <button
                    onClick={handleCancel}
                    className="text-gray-400 hover:text-gray-600"
                    disabled={isSubmitting}
                  >
                    <XMarkIcon className="w-5 h-5" />
                  </button>
                </div>

                {/* Content */}
                <div className="mb-6">
                  <div className="mb-4">
                    <p className="text-sm text-gray-600 mb-2">
                      <strong>Stage:</strong> {pendingInterrupt.stage.replace('_', ' ').toUpperCase()}
                    </p>
                    <p className="text-gray-800">{pendingInterrupt.message}</p>
                  </div>

                  <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Predefined options */}
                    {pendingInterrupt.options && pendingInterrupt.options.length > 0 && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Select an option:
                        </label>
                        <div className="space-y-2">
                          {pendingInterrupt.options.map((option) => (
                            <label key={option} className="flex items-center">
                              <input
                                type="radio"
                                name="interrupt-option"
                                value={option}
                                checked={selectedOption === option}
                                onChange={(e) => {
                                  setSelectedOption(e.target.value)
                                  setCustomResponse('')
                                }}
                                className="h-4 w-4 text-primary-600 border-gray-300 focus:ring-primary-500"
                              />
                              <span className="ml-2 text-sm text-gray-900 capitalize">
                                {option.replace('_', ' ')}
                              </span>
                            </label>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Custom response */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Or provide a custom response:
                      </label>
                      <textarea
                        value={customResponse}
                        onChange={(e) => {
                          setCustomResponse(e.target.value)
                          setSelectedOption('')
                        }}
                        className="textarea-field"
                        rows={3}
                        placeholder="Enter your custom response here..."
                      />
                    </div>

                    {/* Timestamp */}
                    <p className="text-xs text-gray-500">
                      Requested at: {new Date(pendingInterrupt.timestamp).toLocaleString()}
                    </p>

                    {/* Actions */}
                    <div className="flex justify-end space-x-3 pt-4">
                      <button
                        type="button"
                        onClick={handleCancel}
                        disabled={isSubmitting}
                        className="btn-secondary"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        disabled={isSubmitting || (!selectedOption && !customResponse.trim())}
                        className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isSubmitting ? (
                          <div className="flex items-center space-x-2">
                            <div className="w-4 h-4 border border-white border-t-transparent rounded-full animate-spin" />
                            <span>Submitting...</span>
                          </div>
                        ) : (
                          'Submit Response'
                        )}
                      </button>
                    </div>
                  </form>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  )
}