/**
 * Login page component.
 * 
 * Features:
 * - Username and password authentication
 * - Password visibility toggle
 * - Form validation
 * - Loading state during authentication
 * - Error message display
 * - Redirect to home on successful login
 * 
 * Route: / (root)
 */

'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

/**
 * Login page component.
 */
export default function LoginPage() {
  const router = useRouter();
  const login = useAuthStore((state) => state.login);

  // Form state
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  /**
   * Handle login form submission.
   */
  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!username.trim() || !password.trim()) {
      setError('Please enter both username and password');
      return;
    }

    setLoading(true);

    try {
      // Authenticate with backend
      const response = await api.post('/auth/login', {
        username,
        password,
      });

      // Extract data from response
      const { access_token, username: responseUsername } = response.data;

      // Store authentication data
      login(
        {
          username: responseUsername,
        },
        access_token
      );

      // Redirect to home page
      router.push('/home');
    } catch (err: any) {
      // Handle authentication errors
      console.error('Login error:', err);
      const errorMessage = err.response?.data?.detail || 'Login failed. Please check your credentials.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Toggle password visibility.
   */
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-primary-50 to-primary-100">
      {/* Top Bar */}
      <header className="bg-primary-500 py-4 px-6 shadow-md">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Logo Placeholder */}
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
              <span className="text-primary-600 font-bold text-xl">Q</span>
            </div>
            <span className="text-white font-semibold text-lg">Qube.AI</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">
          {/* Welcome Section */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-primary-700 mb-3">
              Welcome to Qube.AI
            </h1>
            <p className="text-primary-600 text-lg">
              An Agentic AI for Quality Engineers
            </p>
          </div>

          {/* Login Form Card */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
              Login
            </h2>

            <form onSubmit={handleLogin} className="space-y-5">
              {/* Username Field */}
              <div>
                <label
                  htmlFor="username"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Username
                </label>
                <input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter your username"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  disabled={loading}
                  autoComplete="username"
                />
              </div>

              {/* Password Field */}
              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Password
                </label>
                <div className="relative">
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="w-full px-4 py-2 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    disabled={loading}
                    autoComplete="current-password"
                  />
                  {/* Password Visibility Toggle */}
                  <button
                    type="button"
                    onClick={togglePasswordVisibility}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
                    disabled={loading}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? (
                      <EyeOff className="w-5 h-5" />
                    ) : (
                      <Eye className="w-5 h-5" />
                    )}
                  </button>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-primary-500 text-white py-3 text-lg font-semibold rounded-lg hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Signing in...</span>
                  </>
                ) : (
                  'Submit'
                )}
              </button>
            </form>

            {/* Default Credentials Info */}
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-800 font-medium mb-1">
                Default Credentials (Phase 1)
              </p>
              <p className="text-xs text-blue-600">
                Username: <span className="font-mono font-semibold">Admin</span>
              </p>
              <p className="text-xs text-blue-600">
                Password: <span className="font-mono font-semibold">Admin</span>
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-primary-500 py-4 text-center text-white text-sm">
        <p>&copy; {new Date().getFullYear()} Qube.AI. All rights reserved.</p>
      </footer>
    </div>
  );
}
