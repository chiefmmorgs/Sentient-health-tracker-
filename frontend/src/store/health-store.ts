import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { HealthReport } from '../api/health';

interface HealthData {
  steps?: number;
  sleep_hours?: number;
  workouts?: number;
  water_liters?: number;
  resting_hr?: number;
  hrv?: number;
  calories?: number;
  runs?: number;
  [key: string]: any;
}

interface ChatMessage {
  id: string;
  message: string;
  reply: string;
  timestamp: Date;
  saved?: boolean;
}

interface HealthStore {
  // State
  healthData: HealthData;
  reports: HealthReport[];
  chatHistory: ChatMessage[];
  isAnalyzing: boolean;
  isGeneratingReport: boolean;
  isChatting: boolean;
  selectedReportKind: string | null;
  
  // Actions
  setHealthData: (data: Partial<HealthData>) => void;
  setReports: (reports: HealthReport[]) => void;
  addReport: (report: HealthReport) => void;
  removeReport: (id: number) => void;
  addChatMessage: (message: ChatMessage) => void;
  clearChatHistory: () => void;
  setIsAnalyzing: (analyzing: boolean) => void;
  setIsGeneratingReport: (generating: boolean) => void;
  setIsChatting: (chatting: boolean) => void;
  setSelectedReportKind: (kind: string | null) => void;
  getReportsByKind: (kind?: string) => HealthReport[];
}

export const useHealthStore = create<HealthStore>()(
  devtools(
    (set, get) => ({
      // Initial state
      healthData: {},
      reports: [],
      chatHistory: [],
      isAnalyzing: false,
      isGeneratingReport: false,
      isChatting: false,
      selectedReportKind: null,

      // Actions
      setHealthData: (data) => set((state) => ({ 
        healthData: { ...state.healthData, ...data } 
      })),
      
      setReports: (reports) => set({ reports }),
      
      addReport: (report) => set((state) => ({ 
        reports: [report, ...state.reports] 
      })),
      
      removeReport: (id) => set((state) => ({
        reports: state.reports.filter(report => report.id !== id)
      })),
      
      addChatMessage: (message) => set((state) => ({ 
        chatHistory: [message, ...state.chatHistory].slice(0, 50) // Keep last 50 messages
      })),
      
      clearChatHistory: () => set({ chatHistory: [] }),
      setIsAnalyzing: (analyzing) => set({ isAnalyzing: analyzing }),
      setIsGeneratingReport: (generating) => set({ isGeneratingReport: generating }),
      setIsChatting: (chatting) => set({ isChatting: chatting }),
      setSelectedReportKind: (kind) => set({ selectedReportKind: kind }),
      
      getReportsByKind: (kind) => {
        const reports = get().reports;
        return kind ? reports.filter(report => report.kind === kind) : reports;
      },
    }),
    { name: 'health-store' }
  )
);