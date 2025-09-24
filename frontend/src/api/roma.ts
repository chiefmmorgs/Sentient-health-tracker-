import { romaApi } from './client';

export interface RomaExecuteRequest {
  agent: 'general' | 'research' | 'financial';
  task: string;
  streaming?: boolean;
  options?: {
    complexity?: number;
    timeout?: number;
    [key: string]: any;
  };
}

export interface RomaExecuteResponse {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
  metadata?: {
    agent: string;
    task: string;
    decomposition?: any[];
    timeline?: any[];
  };
}

export interface RomaStatusResponse {
  status: string;
  agents: string[];
  version: string;
}

// ROMA API functions
export const romaApiFunctions = {
  // Execute task with specific agent
  execute: async (request: RomaExecuteRequest): Promise<RomaExecuteResponse> => {
    const response = await romaApi.post('/execute', request);
    return response.data;
  },

  // Get system status and available agents
  getStatus: async (): Promise<RomaStatusResponse> => {
    const response = await romaApi.get('/status');
    return response.data;
  },

  // Get system info
  getInfo: async () => {
    const response = await romaApi.get('/roma-info');
    return response.data;
  },

  // Get task history
  getHistory: async () => {
    const response = await romaApi.get('/history');
    return response.data;
  },
};