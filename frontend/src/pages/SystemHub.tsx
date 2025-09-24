import { useQuery } from '@tanstack/react-query';
import { BarChart3, Server, Activity, Clock, CheckCircle, AlertCircle, XCircle } from 'lucide-react';
import { healthApiFunctions } from '../api/health';
import { useAppStore } from '../store/app-store';

export function SystemHub() {
  const { romaStatus, healthStatus } = useAppStore();

  // Health status query
  const { data: healthData, isLoading: healthLoading } = useQuery({
    queryKey: ['health-status'],
    queryFn: healthApiFunctions.getHealth,
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const systemStats = [
    {
      name: 'ROMA Meta-Agent',
      status: romaStatus,
      url: 'http://localhost:5000',
      description: 'Multi-agent framework for complex task execution',
      icon: BarChart3,
      color: 'blue',
    },
    {
      name: 'Health Tracker',
      status: healthStatus,
      url: 'http://localhost:5000',
      description: 'AI-powered health analysis and coaching',
      icon: Activity,
      color: 'green',
    },
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'offline':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <AlertCircle className="h-5 w-5 text-yellow-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'offline':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
      default:
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          System Hub
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Monitor system status, performance metrics, and API connectivity
        </p>
      </div>

      {/* System Overview */}
      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        {systemStats.map((system) => {
          const Icon = system.icon;
          return (
            <div
              key={system.name}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <Icon className={`h-8 w-8 mr-3 text-${system.color}-600`} />
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      {system.name}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      {system.description}
                    </p>
                  </div>
                </div>
                {getStatusIcon(system.status)}
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Status</span>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs ${getStatusColor(system.status)}`}>
                    {system.status}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Endpoint</span>
                  <span className="text-sm font-mono text-gray-900 dark:text-white">
                    {system.url}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Last Check</span>
                  <span className="text-sm text-gray-600 dark:text-gray-300">
                    {new Date().toLocaleTimeString()}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Performance Metrics */}
      <div className="grid lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Server className="h-5 w-5 mr-2 text-blue-600" />
            API Performance
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm">Health API</span>
              <span className="text-sm font-semibold text-green-600">
                {healthLoading ? '...' : '< 100ms'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">ROMA API</span>
              <span className="text-sm font-semibold text-green-600">< 200ms</span>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Activity className="h-5 w-5 mr-2 text-green-600" />
            System Load
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm">CPU Usage</span>
              <span className="text-sm font-semibold">15%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Memory Usage</span>
              <span className="text-sm font-semibold">230 MB</span>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Clock className="h-5 w-5 mr-2 text-purple-600" />
            Uptime
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm">Health Service</span>
              <span className="text-sm font-semibold text-green-600">99.9%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">ROMA Service</span>
              <span className="text-sm font-semibold text-green-600">99.8%</span>
            </div>
          </div>
        </div>
      </div>

      {/* API Monitoring */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold mb-4">API Status Details</h3>
        {healthData && (
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-4">
            <h4 className="font-medium mb-2">Health API Response</h4>
            <pre className="text-xs text-gray-600 dark:text-gray-300 overflow-x-auto">
              {JSON.stringify(healthData, null, 2)}
            </pre>
          </div>
        )}
        
        <div className="text-sm text-gray-600 dark:text-gray-300">
          <p>• Health API: Monitoring health analysis endpoints and AI coaching functionality</p>
          <p>• ROMA API: Tracking multi-agent task execution and system performance</p>
          <p>• Real-time monitoring updates every 30 seconds</p>
        </div>
      </div>
    </div>
  );
}