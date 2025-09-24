import axios, { AxiosInstance } from 'axios';

// Environment configuration
const ROMA_API_URL = import.meta.env.VITE_ROMA_API_URL || 'http://localhost:5000';
const HEALTH_API_URL = import.meta.env.VITE_HEALTH_API_URL || 'http://localhost:5000';
const API_KEY = import.meta.env.VITE_API_KEY || 'demo-key-12345';

// Create axios instances for different services
export const romaApi: AxiosInstance = axios.create({
  baseURL: ROMA_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const healthApi: AxiosInstance = axios.create({
  baseURL: HEALTH_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
  },
});

// Request interceptors
romaApi.interceptors.request.use(
  (config) => {
    // Add any common headers or auth tokens here
    return config;
  },
  (error) => Promise.reject(error)
);

healthApi.interceptors.request.use(
  (config) => {
    // Ensure API key is always present for health API
    config.headers['X-API-Key'] = API_KEY;
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptors
romaApi.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('ROMA API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

healthApi.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Health API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export { API_KEY, ROMA_API_URL, HEALTH_API_URL };