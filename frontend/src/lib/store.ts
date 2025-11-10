/**
 * Global state management using Zustand.
 * 
 * Manages:
 * - Authentication state (user, token)
 * - Persistent storage via localStorage
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

/**
 * User state interface
 */
interface User {
  username: string;
  email?: string;
}

/**
 * Authentication store interface
 */
interface AuthState {
  // State
  user: User | null;
  token: string | null;
  
  // Actions
  login: (user: User, token: string) => void;
  logout: () => void;
  setUser: (user: User) => void;
}

/**
 * Authentication store with persistent storage.
 */
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // Initial State
      user: null,
      token: null,

      /**
       * Handle successful login.
       * 
       * @param user - User profile data
       * @param token - JWT access token
       */
      login: (user: User, token: string) => {
        localStorage.setItem('token', token);
        set({ user, token });
      },

      /**
       * Handle user logout.
       * 
       * Clears all authentication data.
       */
      logout: () => {
        localStorage.removeItem('token');
        set({ user: null, token: null });
      },

      /**
       * Update user profile data.
       * 
       * @param user - Updated user data
       */
      setUser: (user: User) => {
        set({ user });
      },
    }),
    {
      name: 'qubeai-auth-storage',
    }
  )
);