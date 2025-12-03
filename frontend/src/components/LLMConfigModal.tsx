/**
 * LLM Configuration Modal Component
 * ----------------------------------
 * Modal for creating and editing LLM configurations.
 * 
 * Features:
 * - Provider selection with pre-filled defaults
 * - Model parameter customization
 * - Token limit configuration
 * - Test before save
 * - API key encryption
 * - Fallback configuration selection
 * - Cache settings
 * - Cost per token configuration
 */

'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface LLMConfigModalProps {
  projectId: number;
  config: any | null;
  onClose: (saved: boolean) => void;
}

interface ProviderDefaults {
  endpoint: string;
  model: string;
  requiresApiKey: boolean;
  defaultParams: any;
}

const PROVIDER_DEFAULTS: Record<string, ProviderDefaults> = {
  ollama: {
    endpoint: 'http://localhost:11434',
    model: 'llama3.1:8b',
    requiresApiKey: false,
    defaultParams: {
      temperature: 0.7,
      max_tokens: 2048,
      top_p: 0.9,
      frequency_penalty: 0.0,
      presence_penalty: 0.0
    }
  },
  openai: {
    endpoint: 'https://api.openai.com',
    model: 'gpt-4',
    requiresApiKey: true,
    defaultParams: {
      temperature: 0.7,
      max_tokens: 2048,
      top_p: 0.9,
      frequency_penalty: 0.0,
      presence_penalty: 0.0
    }
  },
  anthropic: {
    endpoint: 'https://api.anthropic.com',
    model: 'claude-3-5-sonnet-20241022',
    requiresApiKey: true,
    defaultParams: {
      temperature: 0.7,
      max_tokens: 2048,
      top_p: 0.9,
      frequency_penalty: 0.0,
      presence_penalty: 0.0
    }
  },
  google: {
    endpoint: 'https://generativelanguage.googleapis.com',
    model: 'gemini-pro',
    requiresApiKey: true,
    defaultParams: {
      temperature: 0.7,
      max_tokens: 2048,
      top_p: 0.9,
      frequency_penalty: 0.0,
      presence_penalty: 0.0
    }
  }
};

export default function LLMConfigModal({ projectId, config, onClose }: LLMConfigModalProps) {
  const isEditMode = !!config;

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    provider: 'ollama',
    model_name: '',
    api_endpoint: '',
    api_key: '',
    temperature: 0.7,
    max_tokens: 2048,
    top_p: 0.9,
    frequency_penalty: 0.0,
    presence_penalty: 0.0,
    token_limit_daily: 0,
    token_limit_monthly: 0,
    is_active: true,
    is_default: false,
    cache_enabled: true,
    cache_ttl_seconds: 3600,
    cost_per_1k_tokens: 0.0,
    fallback_config_id: null as number | null
  });

  const [availableConfigs, setAvailableConfigs] = useState<any[]>([]);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // Initialize form data
  useEffect(() => {
    if (config) {
      setFormData({
        name: config.name,
        provider: config.provider,
        model_name: config.model_name,
        api_endpoint: config.api_endpoint,
        api_key: '', // Don't populate for security
        temperature: config.model_parameters?.temperature || 0.7,
        max_tokens: config.model_parameters?.max_tokens || 2048,
        top_p: config.model_parameters?.top_p || 0.9,
        frequency_penalty: config.model_parameters?.frequency_penalty || 0.0,
        presence_penalty: config.model_parameters?.presence_penalty || 0.0,
        token_limit_daily: config.token_limit_daily || 0,
        token_limit_monthly: config.token_limit_monthly || 0,
        is_active: config.is_active,
        is_default: config.is_default,
        cache_enabled: config.cache_enabled,
        cache_ttl_seconds: config.cache_ttl_seconds || 3600,
        cost_per_1k_tokens: config.cost_per_1k_tokens || 0.0,
        fallback_config_id: config.fallback_config_id || null
      });
    } else {
      // Set defaults for new config
      const defaults = PROVIDER_DEFAULTS.ollama;
      setFormData(prev => ({
        ...prev,
        model_name: defaults.model,
        api_endpoint: defaults.endpoint
      }));
    }

    // Fetch available configs for fallback selection
    fetchAvailableConfigs();
  }, [config]);

  const fetchAvailableConfigs = async () => {
    try {
      const response = await api.get(`/api/llm-configs/project/${projectId}`);
      setAvailableConfigs(response.data.filter((c: any) => c.id !== config?.id));
    } catch (error) {
      console.error('Failed to fetch configs:', error);
    }
  };

  /**
   * Handle provider change and update defaults
   */
  const handleProviderChange = (provider: string) => {
    const defaults = PROVIDER_DEFAULTS[provider];
    setFormData(prev => ({
      ...prev,
      provider,
      model_name: defaults.model,
      api_endpoint: defaults.endpoint,
      temperature: defaults.defaultParams.temperature,
      max_tokens: defaults.defaultParams.max_tokens,
      top_p: defaults.defaultParams.top_p
    }));
  };

  /**
   * Test the configuration before saving
   */
  const handleTest = async () => {
    setTesting(true);
    setTestResult(null);

    try {
      // Create temporary config for testing
      const testPayload = {
        project_id: projectId,
        name: formData.name || 'Test Config',
        model_name: formData.model_name,
        provider: formData.provider,
        api_endpoint: formData.api_endpoint,
        api_key: formData.api_key || null,
        model_parameters: {
          temperature: formData.temperature,
          max_tokens: formData.max_tokens,
          top_p: formData.top_p,
          frequency_penalty: formData.frequency_penalty,
          presence_penalty: formData.presence_penalty
        },
        is_active: true,
        is_default: false,
        cache_enabled: formData.cache_enabled,
        cache_ttl_seconds: formData.cache_ttl_seconds,
        cost_per_1k_tokens: formData.cost_per_1k_tokens,
        token_limit_daily: 0,
        token_limit_monthly: 0
      };

      // Create a temporary config
      const createResponse = await api.post('/api/llm-configs/', testPayload);
      const tempConfigId = createResponse.data.id;

      // Test it
      const testResponse = await api.post(`/api/llm-configs/${tempConfigId}/test`, {
        prompt: 'Hello! Please respond with "OK" to confirm you are working.'
      });

      // Delete temporary config
      await api.delete(`/api/llm-configs/${tempConfigId}`);

      if (testResponse.data.success) {
        setTestResult(`✅ Success! Response time: ${testResponse.data.response_time_ms}ms`);
      } else {
        setTestResult(`❌ Test failed: ${testResponse.data.error}`);
      }
    } catch (error: any) {
      setTestResult(`❌ Test failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setTesting(false);
    }
  };

  /**
   * Save the configuration
   */
  const handleSave = async () => {
    // Validation
    if (!formData.name.trim()) {
      alert('Please enter a configuration name');
      return;
    }
    if (!formData.model_name.trim()) {
      alert('Please enter a model name');
      return;
    }
    if (!formData.api_endpoint.trim()) {
      alert('Please enter an API endpoint');
      return;
    }

    const provider = PROVIDER_DEFAULTS[formData.provider];
    if (provider.requiresApiKey && !formData.api_key.trim() && !isEditMode) {
      alert('This provider requires an API key');
      return;
    }

    setSaving(true);

    try {
      const payload = {
        project_id: projectId,
        name: formData.name,
        model_name: formData.model_name,
        provider: formData.provider,
        api_endpoint: formData.api_endpoint,
        api_key: formData.api_key || null,
        model_parameters: {
          temperature: formData.temperature,
          max_tokens: formData.max_tokens,
          top_p: formData.top_p,
          frequency_penalty: formData.frequency_penalty,
          presence_penalty: formData.presence_penalty
        },
        token_limit_daily: formData.token_limit_daily,
        token_limit_monthly: formData.token_limit_monthly,
        is_active: formData.is_active,
        is_default: formData.is_default,
        cache_enabled: formData.cache_enabled,
        cache_ttl_seconds: formData.cache_ttl_seconds,
        cost_per_1k_tokens: formData.cost_per_1k_tokens,
        fallback_config_id: formData.fallback_config_id
      };

      if (isEditMode) {
        await api.put(`/api/llm-configs/${config.id}`, payload);
      } else {
        await api.post('/api/llm-configs/', payload);
      }

      onClose(true);
    } catch (error: any) {
      console.error('Failed to save config:', error);
      alert(`Failed to save: ${error.response?.data?.detail || error.message}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">
            {isEditMode ? 'Edit LLM Configuration' : 'Add LLM Configuration'}
          </h2>
          <button
            onClick={() => onClose(false)}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Form */}
        <div className="p-6 space-y-6">
          {/* Basic Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Basic Information</h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Configuration Name *
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                placeholder="e.g., Production Llama, Testing GPT-4"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Provider *
                </label>
                <select
                  value={formData.provider}
                  onChange={(e) => handleProviderChange(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                >
                  <option value="ollama">Ollama (Local)</option>
                  <option value="openai">OpenAI</option>
                  <option value="anthropic">Anthropic (Claude)</option>
                  <option value="google">Google (Gemini)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Model Name *
                </label>
                <input
                  type="text"
                  value={formData.model_name}
                  onChange={(e) => setFormData({ ...formData, model_name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                  placeholder="e.g., llama3.1:8b, gpt-4"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                API Endpoint *
              </label>
              <input
                type="text"
                value={formData.api_endpoint}
                onChange={(e) => setFormData({ ...formData, api_endpoint: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                placeholder="e.g., http://localhost:11434"
              />
            </div>

            {PROVIDER_DEFAULTS[formData.provider].requiresApiKey && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  API Key {isEditMode ? '' : '*'}
                </label>
                <input
                  type="password"
                  value={formData.api_key}
                  onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                  placeholder={isEditMode ? 'Leave blank to keep existing key' : 'Enter API key'}
                />
              </div>
            )}
          </div>

          {/* Model Parameters */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Model Parameters</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Temperature (0-2)
                </label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="2"
                  value={formData.temperature}
                  onChange={(e) => setFormData({ ...formData, temperature: parseFloat(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">Higher = more creative, Lower = more focused</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Max Tokens
                </label>
                <input
                  type="number"
                  step="1"
                  min="1"
                  value={formData.max_tokens}
                  onChange={(e) => setFormData({ ...formData, max_tokens: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Top P (0-1)
                </label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="1"
                  value={formData.top_p}
                  onChange={(e) => setFormData({ ...formData, top_p: parseFloat(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Frequency Penalty (-2 to 2)
                </label>
                <input
                  type="number"
                  step="0.1"
                  min="-2"
                  max="2"
                  value={formData.frequency_penalty}
                  onChange={(e) => setFormData({ ...formData, frequency_penalty: parseFloat(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                />
              </div>
            </div>
          </div>

          {/* Token Limits */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Token Limits</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Daily Token Limit (0 = unlimited)
                </label>
                <input
                  type="number"
                  min="0"
                  value={formData.token_limit_daily}
                  onChange={(e) => setFormData({ ...formData, token_limit_daily: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Monthly Token Limit (0 = unlimited)
                </label>
                <input
                  type="number"
                  min="0"
                  value={formData.token_limit_monthly}
                  onChange={(e) => setFormData({ ...formData, token_limit_monthly: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Cost per 1K Tokens (USD)
              </label>
              <input
                type="number"
                step="0.0001"
                min="0"
                value={formData.cost_per_1k_tokens}
                onChange={(e) => setFormData({ ...formData, cost_per_1k_tokens: parseFloat(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">For cost estimation and tracking</p>
            </div>
          </div>

          {/* Advanced Settings */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Advanced Settings</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Fallback Configuration
                </label>
                <select
                  value={formData.fallback_config_id || ''}
                  onChange={(e) => setFormData({ ...formData, fallback_config_id: e.target.value ? parseInt(e.target.value) : null })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                >
                  <option value="">None</option>
                  {availableConfigs.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
                <p className="text-xs text-gray-500 mt-1">Use this config if primary fails</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cache TTL (seconds)
                </label>
                <input
                  type="number"
                  min="0"
                  value={formData.cache_ttl_seconds}
                  onChange={(e) => setFormData({ ...formData, cache_ttl_seconds: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
                  disabled={!formData.cache_enabled}
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  className="w-4 h-4 text-[#17a2b8] border-gray-300 rounded focus:ring-[#17a2b8]"
                />
                <span className="text-sm text-gray-700">Active</span>
              </label>

              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.is_default}
                  onChange={(e) => setFormData({ ...formData, is_default: e.target.checked })}
                  className="w-4 h-4 text-[#17a2b8] border-gray-300 rounded focus:ring-[#17a2b8]"
                />
                <span className="text-sm text-gray-700">Set as Default</span>
              </label>

              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.cache_enabled}
                  onChange={(e) => setFormData({ ...formData, cache_enabled: e.target.checked })}
                  className="w-4 h-4 text-[#17a2b8] border-gray-300 rounded focus:ring-[#17a2b8]"
                />
                <span className="text-sm text-gray-700">Enable Response Caching</span>
              </label>
            </div>
          </div>

          {/* Test Result */}
          {testResult && (
            <div className={`p-4 rounded-lg ${testResult.includes('✅') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
              {testResult}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 flex items-center justify-between">
          <button
            onClick={handleTest}
            disabled={testing}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50"
          >
            {testing ? 'Testing...' : 'Test Configuration'}
          </button>

          <div className="flex gap-3">
            <button
              onClick={() => onClose(false)}
              className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saving}
              className="px-6 py-2 bg-[#17a2b8] text-white rounded-lg hover:bg-[#138496] transition-colors disabled:opacity-50"
            >
              {saving ? 'Saving...' : isEditMode ? 'Update' : 'Create'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}