'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { AlertCircle, Check, X, Plus, Eye, EyeOff, Trash2, RefreshCw } from 'lucide-react';
import Sidebar from '@/components/layout/Sidebar';
import TopBar from '@/components/layout/TopBar';

const LLM_PROVIDERS = [
  { value: 'ollama', label: 'Ollama (Local)' },
  { value: 'openai', label: 'OpenAI' },
  { value: 'anthropic', label: 'Anthropic' },
  { value: 'huggingface', label: 'HuggingFace' },
];

interface LLMConfig {
  id: number;
  config_name: string;
  provider: string;
  model_name: string;
  api_base_url?: string;
  api_key?: string;
  temperature: string;
  max_tokens: number;
  top_p: string;
  is_active: boolean;
  is_validated: boolean;
  validation_status: string;
  validation_message?: string;
  last_validated_at?: string;
  is_default: boolean;
}

interface AgentMapping {
  agent_type: string;
  llm_config_id: number;
}

export default function ProjectSettingsPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;

  const [configs, setConfigs] = useState<LLMConfig[]>([]);
  const [agentMappings, setAgentMappings] = useState<AgentMapping[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    config_name: '',
    provider: 'ollama',
    model_name: '',
    api_base_url: 'http://localhost:11434',
    api_key: '',
    temperature: '0.7',
    max_tokens: 2048,
    top_p: '1.0',
    is_default: false,
  });

  const [showApiKey, setShowApiKey] = useState(false);
  const [validating, setValidating] = useState(false);
  const [validationResult, setValidationResult] = useState<any>(null);

  useEffect(() => {
    fetchLLMConfigs();
    fetchAgentMappings();
  }, []);

  const fetchLLMConfigs = async () => {
    try {
      const response = await axios.get(`/api/v1/projects/${projectId}/llm-configs`);
      setConfigs(response.data);
    } catch (err) {
      setError('Failed to fetch LLM configurations');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAgentMappings = async () => {
    try {
      const response = await axios.get(`/api/v1/projects/${projectId}/llm-configs/agents`);
      setAgentMappings(response.data);
    } catch (err) {
      console.error('Failed to fetch agent mappings', err);
    }
  };

  const handleValidateConfig = async () => {
    setValidating(true);
    setValidationResult(null);

    try {
      const response = await axios.post(`/api/v1/projects/${projectId}/llm-configs/validate`, {
        provider: formData.provider,
        model_name: formData.model_name,
        api_base_url: formData.api_base_url || undefined,
        api_key: formData.api_key || undefined,
        temperature: formData.temperature,
        max_tokens: formData.max_tokens,
      });

      setValidationResult(response.data);
    } catch (err: any) {
      setValidationResult({
        is_valid: false,
        status: 'failed',
        message: err.response?.data?.detail || 'Validation failed',
      });
    } finally {
      setValidating(false);
    }
  };

  const handleSaveConfig = async () => {
    try {
      const payload = {
        ...formData,
        temperature: formData.temperature.toString(),
        max_tokens: parseInt(formData.max_tokens.toString()),
        top_p: formData.top_p.toString(),
      };

      const response = await axios.post(
        `/api/v1/projects/${projectId}/llm-configs`,
        payload
      );

      setConfigs([...configs, response.data]);
      resetForm();
      setValidationResult(null);
      
      alert('LLM configuration saved successfully!');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save configuration');
    }
  };

  const handleDeleteConfig = async (configId: number) => {
    if (!confirm('Are you sure you want to delete this configuration?')) return;

    try {
      await axios.delete(`/api/v1/projects/${projectId}/llm-configs/${configId}`);
      setConfigs(configs.filter(c => c.id !== configId));
      alert('Configuration deleted successfully');
    } catch (err) {
      setError('Failed to delete configuration');
    }
  };

  const handleSetDefault = async (configId: number) => {
    try {
      await axios.put(`/api/v1/projects/${projectId}/llm-configs/${configId}`, {
        is_default: true,
      });
      fetchLLMConfigs();
    } catch (err) {
      setError('Failed to set default configuration');
    }
  };

  const handleRevalidate = async (configId: number) => {
    setValidating(true);
    try {
      const response = await axios.post(
        `/api/v1/projects/${projectId}/llm-configs/${configId}/validate`
      );
      setValidationResult(response.data);
      fetchLLMConfigs();
    } catch (err) {
      setError('Failed to revalidate configuration');
    } finally {
      setValidating(false);
    }
  };

  const resetForm = () => {
    setFormData({
      config_name: '',
      provider: 'ollama',
      model_name: '',
      api_base_url: 'http://localhost:11434',
      api_key: '',
      temperature: '0.7',
      max_tokens: 2048,
      top_p: '1.0',
      is_default: false,
    });
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar projectId={projectId} />
      
      <div className="flex-1 flex flex-col">
        <TopBar />
        
        <main className="flex-1 overflow-auto p-6">
          <div className="max-w-6xl mx-auto">
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900">Project Settings</h1>
              <p className="text-gray-600 mt-2">Configure LLM models for your project</p>
            </div>

            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-red-700">{error}</div>
              </div>
            )}

            <Tabs defaultValue="add-config" className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-6">
                <TabsTrigger value="add-config">Add LLM Configuration</TabsTrigger>
                <TabsTrigger value="manage-configs">Manage Configurations</TabsTrigger>
              </TabsList>

              {/* Add Configuration Tab */}
              <TabsContent value="add-config" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Add New LLM Configuration</CardTitle>
                    <CardDescription>
                      Configure a new Language Model for your project.
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Configuration Name */}
                    <div className="space-y-2">
                      <Label htmlFor="config_name">Configuration Name *</Label>
                      <Input
                        id="config_name"
                        placeholder="e.g., Ollama Local, OpenAI GPT-4"
                        value={formData.config_name}
                        onChange={(e) => setFormData({ ...formData, config_name: e.target.value })}
                      />
                    </div>

                    {/* Provider Selection */}
                    <div className="space-y-2">
                      <Label htmlFor="provider">LLM Provider *</Label>
                      <Select value={formData.provider} onValueChange={(value) =>
                        setFormData({ 
                          ...formData, 
                          provider: value,
                          api_base_url: value === 'ollama' ? 'http://localhost:11434' : '',
                        })
                      }>
                        <SelectTrigger id="provider">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {LLM_PROVIDERS.map((p) => (
                            <SelectItem key={p.value} value={p.value}>
                              {p.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    {/* Model Name */}
                    <div className="space-y-2">
                      <Label htmlFor="model_name">Model Name *</Label>
                      <Input
                        id="model_name"
                        placeholder="e.g., mistral, gpt-4"
                        value={formData.model_name}
                        onChange={(e) => setFormData({ ...formData, model_name: e.target.value })}
                      />
                    </div>

                    {/* API Base URL */}
                    {formData.provider === 'ollama' && (
                      <div className="space-y-2">
                        <Label htmlFor="api_base_url">API Base URL</Label>
                        <Input
                          id="api_base_url"
                          placeholder="http://localhost:11434"
                          value={formData.api_base_url}
                          onChange={(e) => setFormData({ ...formData, api_base_url: e.target.value })}
                        />
                      </div>
                    )}

                    {/* API Key */}
                    {formData.provider !== 'ollama' && (
                      <div className="space-y-2">
                        <Label htmlFor="api_key">API Key *</Label>
                        <div className="relative">
                          <Input
                            id="api_key"
                            type={showApiKey ? 'text' : 'password'}
                            placeholder="Enter your API key"
                            value={formData.api_key}
                            onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
                          />
                          <button
                            type="button"
                            onClick={() => setShowApiKey(!showApiKey)}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                          >
                            {showApiKey ? <EyeOff size={18} /> : <Eye size={18} />}
                          </button>
                        </div>
                      </div>
                    )}

                    {/* Advanced Parameters */}
                    <div className="bg-gray-50 p-4 rounded-lg space-y-4">
                      <h3 className="font-semibold text-gray-900">Advanced Parameters</h3>
                      
                      <div className="grid grid-cols-3 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="temperature">Temperature</Label>
                          <Input
                            id="temperature"
                            type="number"
                            step="0.1"
                            value={formData.temperature}
                            onChange={(e) => setFormData({ ...formData, temperature: e.target.value })}
                          />
                        </div>

                        <div className="space-y-2">
                          <Label htmlFor="top_p">Top P</Label>
                          <Input
                            id="top_p"
                            type="number"
                            step="0.1"
                            value={formData.top_p}
                            onChange={(e) => setFormData({ ...formData, top_p: e.target.value })}
                          />
                        </div>

                        <div className="space-y-2">
                          <Label htmlFor="max_tokens">Max Tokens</Label>
                          <Input
                            id="max_tokens"
                            type="number"
                            value={formData.max_tokens}
                            onChange={(e) => setFormData({ ...formData, max_tokens: parseInt(e.target.value) })}
                          />
                        </div>
                      </div>
                    </div>

                    {/* Validation Result */}
                    {validationResult && (
                      <div className={`p-4 rounded-lg border ${
                        validationResult.is_valid
                          ? 'bg-green-50 border-green-200'
                          : 'bg-yellow-50 border-yellow-200'
                      }`}>
                        <div className="flex items-start gap-3">
                          {validationResult.is_valid ? (
                            <Check className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                          ) : (
                            <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                          )}
                          <div>
                            <p className={`font-semibold ${validationResult.is_valid ? 'text-green-900' : 'text-yellow-900'}`}>
                              {validationResult.is_valid ? 'Validation Successful' : 'Validation Failed'}
                            </p>
                            <p className={`text-sm mt-1 ${validationResult.is_valid ? 'text-green-700' : 'text-yellow-700'}`}>
                              {validationResult.message}
                            </p>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex gap-3 pt-4">
                      <Button
                        onClick={handleValidateConfig}
                        variant="outline"
                        disabled={validating || !formData.config_name || !formData.model_name}
                      >
                        {validating && <div className="animate-spin h-4 w-4 border-2 border-gray-600 rounded-full border-t-transparent mr-2" />}
                        Test Connection
                      </Button>
                      <Button
                        onClick={handleSaveConfig}
                        disabled={!formData.config_name || !formData.model_name}
                        className="bg-teal-600 hover:bg-teal-700 text-white"
                      >
                        <Plus className="w-4 h-4 mr-2" />
                        Save Configuration
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Manage Configurations Tab */}
              <TabsContent value="manage-configs" className="space-y-6">
                {configs.length === 0 ? (
                  <Card>
                    <CardContent className="pt-6">
                      <p className="text-center text-gray-500 py-8">
                        No LLM configurations yet. Create one in the "Add LLM Configuration" tab.
                      </p>
                    </CardContent>
                  </Card>
                ) : (
                  <div className="space-y-4">
                    {configs.map((config) => (
                      <Card key={config.id} className="border-l-4 border-l-teal-500">
                        <CardContent className="pt-6">
                          <div className="space-y-4">
                            <div className="flex justify-between items-start">
                              <div className="flex-1">
                                <h3 className="font-semibold text-lg text-gray-900">
                                  {config.config_name}
                                </h3>
                                <p className="text-sm text-gray-600">
                                  {config.provider.toUpperCase()} • {config.model_name}
                                </p>
                              </div>
                              <div className="flex items-center gap-2">
                                {config.is_default && (
                                  <span className="px-2 py-1 bg-teal-100 text-teal-700 text-xs rounded-full font-semibold">
                                    Default
                                  </span>
                                )}
                                {config.is_validated ? (
                                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full flex items-center gap-1">
                                    <Check className="w-3 h-3" />
                                    Valid
                                  </span>
                                ) : (
                                  <span className="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded-full flex items-center gap-1">
                                    <AlertCircle className="w-3 h-3" />
                                    Not Validated
                                  </span>
                                )}
                              </div>
                            </div>

                            <div className="flex gap-2 pt-4 border-t">
                              {!config.is_default && (
                                <Button
                                  variant="outline"
                                  size="sm"
                                  onClick={() => handleSetDefault(config.id)}
                                >
                                  Set as Default
                                </Button>
                              )}
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleRevalidate(config.id)}
                                disabled={validating}
                              >
                                <RefreshCw className="w-4 h-4 mr-2" />
                                Revalidate
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleDeleteConfig(config.id)}
                                className="text-red-600 hover:text-red-700 hover:bg-red-50"
                              >
                                <Trash2 className="w-4 h-4" />
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </div>
  );
}