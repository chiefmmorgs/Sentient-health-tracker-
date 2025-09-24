import { useState } from 'react';
import { Heart, TrendingUp, MessageSquare, FileText, Plus } from 'lucide-react';
import { useHealthStore } from '../store/health-store';

export function HealthDashboard() {
  const {
    healthData,
    setHealthData,
    isAnalyzing,
    isGeneratingReport,
    isChatting,
  } = useHealthStore();

  const [chatMessage, setChatMessage] = useState('');

  const handleQuickAnalysis = async () => {
    // This would normally make an API call
    console.log('Quick analysis for:', healthData);
  };

  const handleGenerateReport = async () => {
    // This would normally make an API call
    console.log('Generating weekly report for:', healthData);
  };

  const handleChat = async () => {
    if (!chatMessage.trim()) return;
    
    // This would normally make an API call
    console.log('Chat message:', chatMessage);
    setChatMessage('');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Health Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          AI-powered health analysis and personalized coaching
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Left Column - Forms */}
        <div className="lg:col-span-2 space-y-6">
          {/* Quick Analysis Form */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <TrendingUp className="h-6 w-6 mr-2 text-green-600" />
              Quick Health Analysis
            </h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Steps (weekly total)</label>
                <input
                  type="number"
                  value={healthData.steps || ''}
                  onChange={(e) => setHealthData({ steps: Number(e.target.value) })}
                  placeholder="70000"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Sleep Hours (weekly total)</label>
                <input
                  type="number"
                  value={healthData.sleep_hours || ''}
                  onChange={(e) => setHealthData({ sleep_hours: Number(e.target.value) })}
                  placeholder="49"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Workouts</label>
                <input
                  type="number"
                  value={healthData.workouts || ''}
                  onChange={(e) => setHealthData({ workouts: Number(e.target.value) })}
                  placeholder="4"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Water (liters/week)</label>
                <input
                  type="number"
                  value={healthData.water_liters || ''}
                  onChange={(e) => setHealthData({ water_liters: Number(e.target.value) })}
                  placeholder="14"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Resting Heart Rate</label>
                <input
                  type="number"
                  value={healthData.resting_hr || ''}
                  onChange={(e) => setHealthData({ resting_hr: Number(e.target.value) })}
                  placeholder="65"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">HRV</label>
                <input
                  type="number"
                  value={healthData.hrv || ''}
                  onChange={(e) => setHealthData({ hrv: Number(e.target.value) })}
                  placeholder="45"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>
            <div className="flex space-x-4 mt-6">
              <button
                onClick={handleQuickAnalysis}
                disabled={isAnalyzing}
                className="flex-1 flex items-center justify-center px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
              >
                <TrendingUp className="h-5 w-5 mr-2" />
                {isAnalyzing ? 'Analyzing...' : 'Quick Analysis'}
              </button>
              <button
                onClick={handleGenerateReport}
                disabled={isGeneratingReport}
                className="flex-1 flex items-center justify-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                <FileText className="h-5 w-5 mr-2" />
                {isGeneratingReport ? 'Generating...' : 'Weekly Report'}
              </button>
            </div>
          </div>

          {/* AI Coach Chat */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <MessageSquare className="h-6 w-6 mr-2 text-purple-600" />
              AI Health Coach
            </h2>
            <div className="space-y-4">
              <div className="h-64 bg-gray-50 dark:bg-gray-700 rounded-lg p-4 overflow-y-auto">
                <div className="text-center text-gray-500 dark:text-gray-400">
                  <MessageSquare className="h-8 w-8 mx-auto mb-2" />
                  <p>Start a conversation with your AI health coach</p>
                </div>
              </div>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  placeholder="Ask your health coach anything..."
                  className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  onKeyPress={(e) => e.key === 'Enter' && handleChat()}
                />
                <button
                  onClick={handleChat}
                  disabled={!chatMessage.trim() || isChatting}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column - Stats & Reports */}
        <div className="space-y-6">
          {/* System Status */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold mb-4">System Status</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm">Health API</span>
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                  Online
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">ROMA Available</span>
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                  Yes
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Total Reports</span>
                <span className="text-sm font-medium">0</span>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold mb-4">This Week</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm">Daily Steps Avg</span>
                <span className="text-lg font-bold text-blue-600">
                  {healthData.steps ? Math.round(healthData.steps / 7).toLocaleString() : '—'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Daily Sleep Avg</span>
                <span className="text-lg font-bold text-purple-600">
                  {healthData.sleep_hours ? Math.round((healthData.sleep_hours / 7) * 10) / 10 : '—'}h
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Workouts</span>
                <span className="text-lg font-bold text-green-600">
                  {healthData.workouts || '—'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Hydration</span>
                <span className="text-lg font-bold text-blue-600">
                  {healthData.water_liters || '—'}L
                </span>
              </div>
            </div>
          </div>

          {/* Recent Reports */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Recent Reports</h2>
              <button className="p-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
                <Plus className="h-5 w-5" />
              </button>
            </div>
            <div className="text-center py-8 text-gray-500 dark:text-gray-400">
              <FileText className="h-8 w-8 mx-auto mb-2" />
              <p>No reports yet</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}