import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Layout } from './components/Layout';
import { Landing } from './pages/Landing';
import { RomaDashboard } from './pages/RomaDashboard';
import { HealthDashboard } from './pages/HealthDashboard';
import { SystemHub } from './pages/SystemHub';
import { queryClient } from './lib/react-query';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Landing />} />
            <Route path="roma" element={<RomaDashboard />} />
            <Route path="health" element={<HealthDashboard />} />
            <Route path="dashboard" element={<SystemHub />} />
          </Route>
        </Routes>
      </Router>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;
