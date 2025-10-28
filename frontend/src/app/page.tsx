'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { authAPI } from '@/lib/api';
import { Sparkles } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const login = useAuthStore((state) => state.login);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(username, password);
      const { access_token } = response.data;

      // Decode token to get user info (simple decode, not validation)
      const payload = JSON.parse(atob(access_token.split('.')[1]));
      const user = {
        id: payload.user_id,
        username: payload.sub,
        role: payload.role,
      };

      login(access_token, user);
      router.push('/home');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-primary-light to-primary">
      {/* Header */}
      <div className="w-full bg-primary py-4 px-6 flex items-center">
        <Sparkles className="w-8 h-8 text-white mr-2" />
        <span className="text-white text-xl font-bold">Login</span>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center px-4">
        <div className="bg-white rounded-lg shadow-2xl p-8 w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-primary mb-2">
              Welcome to Qube.AI
            </h1>
            <p className="text-secondary-light text-lg">Login</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-secondary mb-2"
              >
                Username
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="john.doe"
                className="input-field"
                required
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-secondary mb-2"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="password123"
                className="input-field"
                required
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Logging in...' : 'Submit'}
            </button>
          </form>
        </div>
      </div>

    </div>
  );
}