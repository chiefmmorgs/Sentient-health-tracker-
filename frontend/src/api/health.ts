import { healthApi } from './client';

export interface HealthData {
  data: Record<string, any>;
}

export interface ChatMessage {
  message: string;
  save?: boolean;
}

export interface HealthReport {
  id: number;
  created_at: string;
  kind: string;
  input: Record<string, any> | null;
  output_text: string | null;
  metrics: Record<string, any> | null;
}

export interface WeeklyReportResponse {
  status: string;
  report: string;
  metrics: Record<string, any>;
  data_analyzed: Record<string, any>;
  report_id: number | null;
}

export interface AnalysisResponse {
  status: string;
  analysis: string;
  report_id: number | null;
}

export interface ChatResponse {
  status: string;
  reply: string;
  report_id: number | null;
}

export interface HealthStatus {
  status: string;
  roma_available: boolean;
  timestamp: string;
}

// Health API functions
export const healthApiFunctions = {
  // Get system health status
  getHealth: async (): Promise<HealthStatus> => {
    const response = await healthApi.get('/health');
    return response.data;
  },

  // Get ROMA info
  getRomaInfo: async () => {
    const response = await healthApi.get('/roma-info');
    return response.data;
  },

  // Analyze health data
  analyze: async (data: HealthData, save?: boolean): Promise<AnalysisResponse> => {
    const params = save ? { save: 'true' } : {};
    const response = await healthApi.post('/analyze', data, { params });
    return response.data;
  },

  // Generate weekly report
  generateWeeklyReport: async (data: HealthData, save?: boolean): Promise<WeeklyReportResponse> => {
    const params = save ? { save: 'true' } : {};
    const response = await healthApi.post('/weekly-report', data, { params });
    return response.data;
  },

  // Chat with AI coach
  chat: async (message: ChatMessage, save?: boolean): Promise<ChatResponse> => {
    const params = save ? { save: 'true' } : {};
    const response = await healthApi.post('/chat', message, { params });
    return response.data;
  },

  // Get all reports
  getReports: async (limit = 20, offset = 0, kind?: string): Promise<HealthReport[]> => {
    const params: any = { limit, offset };
    if (kind) params.kind = kind;
    const response = await healthApi.get('/reports', { params });
    return response.data;
  },

  // Get specific report
  getReport: async (id: number): Promise<HealthReport> => {
    const response = await healthApi.get(`/reports/${id}`);
    return response.data;
  },

  // Delete report
  deleteReport: async (id: number): Promise<{ status: string; id: number }> => {
    const response = await healthApi.delete(`/reports/${id}`);
    return response.data;
  },
};