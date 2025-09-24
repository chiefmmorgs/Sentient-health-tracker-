import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface RomaTask {
  id: string;
  agent: 'general' | 'research' | 'financial';
  task: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
  timestamp: Date;
  decomposition?: any[];
  timeline?: any[];
}

interface RomaStore {
  // State
  selectedAgent: 'general' | 'research' | 'financial';
  currentTask: string;
  complexity: number;
  isExecuting: boolean;
  tasks: RomaTask[];
  
  // Actions
  setSelectedAgent: (agent: 'general' | 'research' | 'financial') => void;
  setCurrentTask: (task: string) => void;
  setComplexity: (complexity: number) => void;
  setIsExecuting: (executing: boolean) => void;
  addTask: (task: RomaTask) => void;
  updateTask: (id: string, updates: Partial<RomaTask>) => void;
  clearTasks: () => void;
  getTasksByAgent: (agent: string) => RomaTask[];
}

export const useRomaStore = create<RomaStore>()(
  devtools(
    (set, get) => ({
      // Initial state
      selectedAgent: 'general',
      currentTask: '',
      complexity: 50,
      isExecuting: false,
      tasks: [],

      // Actions
      setSelectedAgent: (agent) => set({ selectedAgent: agent }),
      setCurrentTask: (task) => set({ currentTask: task }),
      setComplexity: (complexity) => set({ complexity }),
      setIsExecuting: (executing) => set({ isExecuting: executing }),
      
      addTask: (task) => set((state) => ({ 
        tasks: [task, ...state.tasks].slice(0, 100) // Keep last 100 tasks
      })),
      
      updateTask: (id, updates) => set((state) => ({
        tasks: state.tasks.map(task => 
          task.id === id ? { ...task, ...updates } : task
        )
      })),
      
      clearTasks: () => set({ tasks: [] }),
      
      getTasksByAgent: (agent) => get().tasks.filter(task => task.agent === agent),
    }),
    { name: 'roma-store' }
  )
);