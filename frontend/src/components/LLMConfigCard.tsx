/**
 * LLM Configuration Card Component
 * ---------------------------------
 * Displays a single LLM configuration with status, usage, and actions.
 * 
 * Features:
 * - Visual status indicators (health, test status)
 * - Token usage progress bars
 * - Quick actions (test, set default, edit, delete)
 * - Provider-specific icons
 * - Real-time usage updates
 */

'use client';

import { useState } from 'react';
import api from '@/lib/api';

interface LLMConfigCardProps {
  config: {
    id: number;
    name: string;
    model_name: string;
    provider: string;
    is_active: boolean;
    is_default: boolean;
    test_status: string;
    health_status: string;
    token_usage_today: number;
    token_usage_month: number;
    token_limit_daily: number;
    token_limit_monthly: number;
    daily_usage_percentage?: number;
    monthly_usage_percentage?: number;
    estimated_cost_today?: number;
    estimated_cost_month?: number;
    last_tested_at?: string;
    test_response_time_ms?: number;
  };
  onEdit: () => void;
  onDelete: () => void;
  onSetDefault: () => void;
}

export default function LLMConfigCard({ config, onEdit, onDelete, onSetDefault }: LLMConfigCardProps) {
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<string | null>(null);

  /**
   * Get provider icon based on provider type
   */
  const getProviderIcon = () => {
    switch (config.provider) {
      case 'ollama':
        return '🦙';
      case 'openai':
        return '🤖';
      case 'anthropic':
        return '🧠';
      case 'google':
        return '🔍';
      default:
        return '💬';
    }
  };

  /**
   * Get health status color
   */
  const getHealthColor = () => {
    switch (config.health_status) {
      case 'healthy':
        return 'bg-green-100 text-green-800';
      case 'degraded':
        return 'bg-yellow-100 text-yellow-800';
      case 'down':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  /**
   * Get usage bar color based on percentage
   */
  const getUsageColor = (percentage?: number) => {
    if (!percentage) return 'bg-gray-300';
    if (percentage >= 90) return 'bg-red-500';
    if (percentage >= 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  /**
   * Test the LLM configuration
   */
  const handleTest = async () => {
    setTesting(true);
    setTestResult(null);

    try {
      const response = await api.post(`/api/llm-configs/${config.id}/test`, {
        prompt: 'Hello! Please respond with a brief introduction to software testing.'
      });

      if (response.data.success) {
        setTestResult('✅ Test successful');
      } else {
        setTestResult('❌ Test failed: ' + response.data.error);
      }
    } catch (error: any) {
      setTestResult('❌ Test failed: ' + (error.response?.data?.detail || error.message));
    } finally {
      setTesting(false);
      
      // Clear result after 3 seconds
      setTimeout(() => setTestResult(null), 3000);
    }
  };

  return (
    <div className={`bg-white rounded-lg border-2 ${config.is_default ? 'border-[#17a2b8]' : 'border-gray-200'} hover:shadow-lg transition-shadow p-6`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="text-4xl">{getProviderIcon()}</div>
          <div>
            <h3 className="font-bold text-lg text-gray-900 flex items-center gap-2">
              {config.name}
              {config.is_default && (
                <span className="text-xs bg-[#17a2b8] text-white px-2 py-1 rounded">
                  DEFAULT
                </span>
              )}
            </h3>
            <p className="text-sm text-gray-600">{config.model_name}</p>
          </div>
        </div>

        {/* Status Badge */}
        <span className={`text-xs px-2 py-1 rounded ${getHealthColor()}`}>
          {config.health_status}
        </span>
      </div>

      {/* Provider Info */}
      <div className="mb-4 pb-4 border-b border-gray-100">
        <div className="text-sm text-gray-600">
          Provider: <span className="font-medium text-gray-900 capitalize">{config.provider}</span>
        </div>
        {config.last_tested_at && (
          <div className="text-xs text-gray-500 mt-1">
            Last tested: {new Date(config.last_tested_at).toLocaleString()}
            {config.test_response_time_ms && ` (${config.test_response_time_ms}ms)`}
          </div>
        )}
      </div>

      {/* Token Usage - Daily */}
      {config.token_limit_daily > 0 && (
        <div className="mb-3">
          <div className="flex justify-between text-xs text-gray-600 mb-1">
            <span>Daily Usage</span>
            <span>{config.token_usage_today.toLocaleString()} / {config.token_limit_daily.toLocaleString()}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${getUsageColor(config.daily_usage_percentage)}`}
              style={{ width: `${Math.min(config.daily_usage_percentage || 0, 100)}%` }}
            />
          </div>
          {config.daily_usage_percentage && config.daily_usage_percentage >= 90 && (
            <div className="text-xs text-red-600 mt-1">
              ⚠️ Approaching daily limit
            </div>
          )}
        </div>
      )}

      {/* Token Usage - Monthly */}
      {config.token_limit_monthly > 0 && (
        <div className="mb-4">
          <div className="flex justify-between text-xs text-gray-600 mb-1">
            <span>Monthly Usage</span>
            <span>{config.token_usage_month.toLocaleString()} / {config.token_limit_monthly.toLocaleString()}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${getUsageColor(config.monthly_usage_percentage)}`}
              style={{ width: `${Math.min(config.monthly_usage_percentage || 0, 100)}%` }}
            />
          </div>
        </div>
      )}

      {/* Cost Estimation */}
      {config.estimated_cost_month !== undefined && config.estimated_cost_month > 0 && (
        <div className="mb-4 p-3 bg-gray-50 rounded">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Est. Cost (Month):</span>
            <span className="font-bold text-gray-900">${config.estimated_cost_month.toFixed(4)}</span>
          </div>
        </div>
      )}

      {/* Test Result */}
      {testResult && (
        <div className={`mb-3 p-2 rounded text-sm ${testResult.includes('✅') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
          {testResult}
        </div>
      )}

      {/* Actions */}
      <div className="grid grid-cols-2 gap-2">
        <button
          onClick={handleTest}
          disabled={testing}
          className="px-3 py-2 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors disabled:opacity-50"
        >
          {testing ? 'Testing...' : 'Test'}
        </button>
        
        {!config.is_default && (
          <button
            onClick={onSetDefault}
            className="px-3 py-2 text-sm bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
          >
            Set Default
          </button>
        )}
        
        <button
          onClick={onEdit}
          className="px-3 py-2 text-sm bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
        >
          Edit
        </button>
        
        <button
          onClick={onDelete}
          className="px-3 py-2 text-sm bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
}