import { useWorkflowStore } from '../store/workflowStore'
import { Link } from 'react-router-dom'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism'

export default function Code() {
  const { codeFiles, status, currentStage, sessionId } = useWorkflowStore()

  if (!sessionId) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">[CODE]</div>
        <h2 className="text-xl font-medium text-gray-900 mb-2">No Active Workflow</h2>
        <p className="text-gray-600 mb-6">
          Start a workflow to generate code files.
        </p>
        <Link to="/requirements" className="btn-primary">
          Start Workflow
        </Link>
      </div>
    )
  }

  const hasCodeFiles = codeFiles && Object.keys(codeFiles).length > 0

  const getLanguageFromFilename = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase()
    const langMap: { [key: string]: string } = {
      'js': 'javascript',
      'jsx': 'jsx',
      'ts': 'typescript',
      'tsx': 'tsx',
      'py': 'python',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c',
      'cs': 'csharp',
      'php': 'php',
      'rb': 'ruby',
      'go': 'go',
      'rs': 'rust',
      'html': 'html',
      'css': 'css',
      'json': 'json',
      'xml': 'xml',
      'sql': 'sql',
      'md': 'markdown',
      'yml': 'yaml',
      'yaml': 'yaml'
    }
    return langMap[ext || ''] || 'text'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Generated Code</h1>
        <p className="text-gray-600 mt-2">
          AI-generated code files based on your design documents
        </p>
      </div>

      {/* Status */}
      {currentStage === 'code' && status === 'running' && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="w-4 h-4 border border-blue-600 border-t-transparent rounded-full animate-spin mr-3" />
            <span className="text-blue-800">Generating code from design documents...</span>
          </div>
        </div>
      )}

      {/* Code Files */}
      {hasCodeFiles ? (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-900">
              Code Files ({Object.keys(codeFiles).length})
            </h2>
            <button className="btn-secondary text-sm">
              [PACKAGE] Download All Files
            </button>
          </div>

          <div className="grid gap-6">
            {Object.entries(codeFiles).map(([filename, content]) => (
              <div key={filename} className="card p-0 overflow-hidden">
                <div className="flex justify-between items-center p-4 bg-gray-50 border-b">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">[FILE]</span>
                    <h3 className="font-mono text-sm font-medium text-gray-900">
                      {filename}
                    </h3>
                  </div>
                  <div className="flex space-x-2">
                    <button className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200">
                      Copy
                    </button>
                    <button className="px-2 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200">
                      Download
                    </button>
                  </div>
                </div>
                
                <div className="max-h-96 overflow-auto">
                  <SyntaxHighlighter
                    language={getLanguageFromFilename(filename)}
                    style={tomorrow}
                    showLineNumbers
                    customStyle={{
                      margin: 0,
                      padding: '1rem',
                      background: '#fafafa'
                    }}
                  >
                    {typeof content === 'string' ? content : JSON.stringify(content, null, 2)}
                  </SyntaxHighlighter>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <div className="text-4xl mb-4">[SETUP]</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Code Not Generated Yet
          </h3>
          <p className="text-gray-600">
            {status === 'running' && currentStage === 'code' 
              ? 'AI is currently generating code from your design documents...'
              : 'Code files will be generated after the design phase is completed.'
            }
          </p>
        </div>
      )}
    </div>
  )
}