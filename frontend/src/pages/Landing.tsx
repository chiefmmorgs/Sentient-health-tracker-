import { Link } from 'react-router-dom';
import { Brain, Heart, BarChart3, Zap } from 'lucide-react';

export function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-6">
            AI-Powered Multi-Agent Platform
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
            Experience the power of advanced AI systems with ROMA Meta-Agent Framework 
            and Sentient Health Tracker - your intelligent assistants for complex tasks 
            and personal wellness.
          </p>
        </div>

        {/* Systems Grid */}
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {/* ROMA System */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center mb-4">
              <Brain className="h-8 w-8 text-blue-600 mr-3" />
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                ROMA Meta-Agent
              </h2>
            </div>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              Advanced multi-agent framework featuring Atomizer → Planner → Executors → Aggregator 
              architecture for complex task decomposition and parallel execution.
            </p>
            <div className="space-y-2 mb-6">
              <div className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                <Zap className="h-4 w-4 mr-2 text-yellow-500" />
                Agent selection (General, Research, Financial)
              </div>
              <div className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                <BarChart3 className="h-4 w-4 mr-2 text-green-500" />
                Task complexity analysis & decomposition
              </div>
              <div className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                <Brain className="h-4 w-4 mr-2 text-blue-500" />
                Parallel execution & results aggregation
              </div>
            </div>
            <Link
              to="/roma"
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Launch ROMA Dashboard
            </Link>
          </div>

          {/* Health System */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center mb-4">
              <Heart className="h-8 w-8 text-red-600 mr-3" />
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Health Tracker
              </h2>
            </div>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              Intelligent health analysis system providing personalized insights, 
              weekly reports, and AI coaching for your wellness journey.
            </p>
            <div className="space-y-2 mb-6">
              <div className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                <BarChart3 className="h-4 w-4 mr-2 text-green-500" />
                Quick health metrics analysis
              </div>
              <div className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                <Brain className="h-4 w-4 mr-2 text-blue-500" />
                AI-powered coaching & recommendations
              </div>
              <div className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                <Heart className="h-4 w-4 mr-2 text-red-500" />
                Weekly reports & trend visualization
              </div>
            </div>
            <Link
              to="/health"
              className="inline-flex items-center px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Launch Health Dashboard
            </Link>
          </div>
        </div>

        {/* System Hub */}
        <div className="text-center">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 border border-gray-200 dark:border-gray-700 max-w-md mx-auto">
            <BarChart3 className="h-12 w-12 text-purple-600 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              System Hub
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              Monitor both systems, view performance metrics, and manage API connectivity 
              from a unified dashboard.
            </p>
            <Link
              to="/dashboard"
              className="inline-flex items-center px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              Open System Hub
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}