import { useState } from 'react';
import { Brain, Loader2, Play, AlertCircle } from 'lucide-react';
import { useRomaStore } from '../store/roma-store';

export function RomaDashboard() {
  const {
    selectedAgent,
    currentTask,
    complexity,
    isExecuting,
    tasks,
    setSelectedAgent,
    setCurrentTask,
    setComplexity,
  } = useRomaStore();

  const [streaming, setStreaming] = useState(false);

  const agents = [
    { id: 'general' as const, name: 'General Agent', description: 'General purpose task execution' },
    { id: 'research' as const, name: 'Research Agent', description: 'Research and analysis tasks' },
    { id: 'financial' as const, name: 'Financial Agent', description: 'Financial analysis and planning' },
  ];

  const handleExecuteTask = async () => {
    if (!currentTask.trim()) return;
    
    // This would normally make an API call
    console.log('Executing task:', {
      agent: selectedAgent,
      task: currentTask,
      complexity,
      streaming,
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          ROMA Meta-Agent Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Advanced multi-agent framework for complex task decomposition and execution
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Control Panel */}
        <div className="lg:col-span-2 space-y-6">
          {/* Agent Selection */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Brain className="h-6 w-6 mr-2 text-blue-600" />
              Agent Selection
            </h2>
            <div className="grid md:grid-cols-3 gap-4">
              {agents.map((agent) => (
                <button
                  key={agent.id}
                  onClick={() => setSelectedAgent(agent.id)}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    selectedAgent === agent.id
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                      : 'border-gray-200 dark:border-gray-600 hover:border-gray-300'
                  }`}
                >
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                    {agent.name}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    {agent.description}
                  </p>
                </button>
              ))}
            </div>
          </div>

          {/* Task Input */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold mb-4">Task Input</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Task Description</label>
                <textarea
                  value={currentTask}
                  onChange={(e) => setCurrentTask(e.target.value)}
                  placeholder="Describe the task you want the agent to execute..."
                  className="w-full h-32 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">
                  Complexity Level: {complexity}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={complexity}
                  onChange={(e) => setComplexity(Number(e.target.value))}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Simple</span>
                  <span>Complex</span>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={streaming}
                    onChange={(e) => setStreaming(e.target.checked)}
                    className="mr-2"
                  />
                  Enable Streaming
                </label>
              </div>

              <button
                onClick={handleExecuteTask}
                disabled={!currentTask.trim() || isExecuting}
                className="w-full flex items-center justify-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isExecuting ? (
                  <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                ) : (
                  <Play className="h-5 w-5 mr-2" />
                )}
                {isExecuting ? 'Executing...' : 'Execute Task'}
              </button>
            </div>
          </div>
        </div>

        {/* Results Panel */}
        <div className="space-y-6">
          {/* System Status */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold mb-4">System Status</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm">ROMA Service</span>
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                  Online
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Available Agents</span>
                <span className="text-sm font-medium">3</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Active Tasks</span>
                <span className="text-sm font-medium">{tasks.filter(t => t.status === 'running').length}</span>
              </div>
            </div>
          </div>

          {/* Recent Tasks */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold mb-4">Recent Tasks</h2>
            {tasks.length === 0 ? (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                <AlertCircle className="h-8 w-8 mx-auto mb-2" />
                <p>No tasks executed yet</p>
              </div>
            ) : (
              <div className="space-y-3">
                {tasks.slice(0, 5).map((task) => (
                  <div
                    key={task.id}
                    className="p-3 border border-gray-200 dark:border-gray-600 rounded-lg"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium capitalize">{task.agent}</span>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        task.status === 'completed' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' :
                        task.status === 'failed' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300' :
                        task.status === 'running' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300' :
                        'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
                      }`}>
                        {task.status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-300 truncate">
                      {task.task}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}