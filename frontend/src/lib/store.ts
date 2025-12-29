/**
 * Zustand Store
 * -------------
 * Global state management for authentication.
 * 
 * UPDATED: Added email and is_admin to user object.
 */

import { create } from 'zustand';

interface User {
  id: number;
  username: string;
  email?: string;
  is_admin?: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
  initializeAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  /**
   * Login user and store credentials
   */
  login: (token: string, user: User) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    set({ user, token, isAuthenticated: true });
  },

  /**
   * Logout user and clear credentials
   */
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({ user: null, token: null, isAuthenticated: false });
  },

  /**
   * Initialize auth state from localStorage
   */
  initializeAuth: () => {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    
    if (token && userStr) {
      try {
        const user = JSON.parse(userStr);
        set({ user, token, isAuthenticated: true });
      } catch (error) {
        console.error('Failed to parse user from localStorage:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
  },
}));