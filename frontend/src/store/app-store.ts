import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface AppStore {
  // UI State
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  
  // System Status
  romaStatus: 'online' | 'offline' | 'unknown';
  healthStatus: 'online' | 'offline' | 'unknown';
  
  // Actions
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setRomaStatus: (status: 'online' | 'offline' | 'unknown') => void;
  setHealthStatus: (status: 'online' | 'offline' | 'unknown') => void;
}

export const useAppStore = create<AppStore>()(
  devtools(
    (set) => ({
      // Initial state
      theme: 'dark',
      sidebarOpen: false,
      romaStatus: 'unknown',
      healthStatus: 'unknown',

      // Actions
      toggleTheme: () => set((state) => ({ 
        theme: state.theme === 'light' ? 'dark' : 'light' 
      })),
      
      setTheme: (theme) => set({ theme }),
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      setRomaStatus: (status) => set({ romaStatus: status }),
      setHealthStatus: (status) => set({ healthStatus: status }),
    }),
    { name: 'app-store' }
  )
);