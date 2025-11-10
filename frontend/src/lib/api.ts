/**
 * API client configuration for backend communication.
 * 
 * Features:
 * - Centralized Axios instance with base URL
 * - Request interceptor: Attaches JWT token to all requests
 * - Response interceptor: Handles 401 errors and token expiration
 */

import axios, { AxiosError, AxiosResponse } from 'axios';

// Base API URL from environment variable (includes /api prefix)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

/**
 * Axios instance configured for Qube.AI backend.
 */
export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request interceptor: Attach JWT token to Authorization header.
 */
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('token');
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor: Handle authentication errors.
 */
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle 401 Unauthorized - token expired or invalid
    if (error.response?.status === 401) {
      // Clear authentication data
      localStorage.removeItem('token');
      
      // Redirect to login page
      if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// Export default for compatibility
export default api;