/**
 * Login Page
 * ----------
 * User authentication with JWT tokens.
 * 
 * Features:
 * - Username/password authentication
 * - Password visibility toggle
 * - JWT token storage
 * - Redirect on success
 * - Error handling
 */

'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff } from 'lucide-react';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';

export default function LoginPage() {
  const router = useRouter();
  const login = useAuthStore((state) => state.login);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  /**
   * Handle login form submission
   */
  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      console.log('Attempting login to:', api.defaults.baseURL);
      
      // Call login API
      const response = await api.post('/api/auth/login', {
        username,
        password,
      });

      console.log('Login successful:', response.data);

      // Store token and user info
      const { access_token, user } = response.data;
      login(access_token, user);

      // Redirect to home page
      router.push('/home');
    } catch (err: any) {
      console.error('Login error:', err);
      console.error('Error details:', {
        status: err.response?.status,
        data: err.response?.data,
        url: err.config?.url,
        baseURL: err.config?.baseURL,
      });
      
      setError(
        err.response?.data?.detail || 
        'Login failed. Please check your credentials.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-lg">
        {/* Logo and Title */}
        <div className="text-center">
          <div className="text-5xl mb-4">🎯</div>
          <h1 className="text-3xl font-bold text-[#17a2b8] mb-2">
            Welcome to Qube.AI
          </h1>
          <p className="text-gray-600">
            An Agentic AI for Quality Engineers
          </p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleLogin} className="mt-8 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
              placeholder="Enter username"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <div className="relative">
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent pr-10"
                placeholder="Enter password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-[#17a2b8] text-white rounded-lg hover:bg-[#138496] transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Logging in...' : 'Submit'}
          </button>
        </form>

        {/* Default Credentials Hint */}
        <div className="text-center text-sm text-gray-500">
          <p>Default credentials:</p>
          <p>Username: <span className="font-mono">Admin</span></p>
          <p>Password: <span className="font-mono">Admin</span></p>
        </div>
      </div>
    </div>
  );
}