/**
 * LLM Configuration Page
 * ----------------------
 * Project-specific LLM configuration management.
 * 
 * Features:
 * - Display all LLM configs as cards
 * - Create new configurations
 * - Edit existing configurations
 * - Test models before saving
 * - Monitor token usage in real-time
 * - Set default configuration
 * - Delete configurations
 * 
 * This page is accessed from project settings sidebar.
 */

'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import api from '@/lib/api';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import Footer from '@/components/Footer';
import LLMConfigCard from '@/components/LLMConfigCard';
import LLMConfigModal from '@/components/LLMConfigModal';

interface LLMConfig {
  id: number;
  name: string;
  model_name: string;
  provider: string;
  api_endpoint: string;
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
}

interface Project {
  id: number;
  name: string;
}

export default function LLMConfigPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = parseInt(params.id as string);

  const [project, setProject] = useState<Project | null>(null);
  const [configs, setConfigs] = useState<LLMConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingConfig, setEditingConfig] = useState<LLMConfig | null>(null);
  const [usageSummary, setUsageSummary] = useState<any>(null);

  // Fetch project details
  useEffect(() => {
    const fetchProject = async () => {
      try {
        const response = await api.get(`/api/projects/${projectId}`);
        setProject(response.data);
      } catch (error) {
        console.error('Failed to fetch project:', error);
      }
    };

    fetchProject();
  }, [projectId]);

  // Fetch LLM configurations
  const fetchConfigs = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/api/llm-configs/project/${projectId}`);
      setConfigs(response.data);
    } catch (error) {
      console.error('Failed to fetch configs:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch usage summary
  const fetchUsageSummary = async () => {
    try {
      const response = await api.get(`/api/llm-configs/project/${projectId}/usage`);
      setUsageSummary(response.data);
    } catch (error) {
      console.error('Failed to fetch usage summary:', error);
    }
  };

  useEffect(() => {
    fetchConfigs();
    fetchUsageSummary();
    
    // Refresh every 30 seconds
    const interval = setInterval(() => {
      fetchConfigs();
      fetchUsageSummary();
    }, 30000);

    return () => clearInterval(interval);
  }, [projectId]);

  const handleCreate = () => {
    setEditingConfig(null);
    setShowModal(true);
  };

  const handleEdit = (config: LLMConfig) => {
    setEditingConfig(config);
    setShowModal(true);
  };

  const handleDelete = async (configId: number) => {
    if (!confirm('Are you sure you want to delete this configuration?')) {
      return;
    }

    try {
      await api.delete(`/api/llm-configs/${configId}`);
      fetchConfigs();
      fetchUsageSummary();
    } catch (error) {
      console.error('Failed to delete config:', error);
      alert('Failed to delete configuration');
    }
  };

  const handleSetDefault = async (configId: number) => {
    try {
      await api.put(`/api/llm-configs/${configId}`, { is_default: true });
      fetchConfigs();
    } catch (error) {
      console.error('Failed to set default:', error);
      alert('Failed to set default configuration');
    }
  };

  const handleModalClose = (saved: boolean) => {
    setShowModal(false);
    setEditingConfig(null);
    
    if (saved) {
      fetchConfigs();
      fetchUsageSummary();
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      
      <div className="flex flex-1">
        <Sidebar context="project" projectId={projectId} />
        
        <main className="flex-1 p-8">
          {/* Page Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  LLM Configuration
                </h1>
                <p className="text-gray-600 mt-1">
                  {project?.name} - Manage LLM models and monitor usage
                </p>
              </div>
              
              <button
                onClick={handleCreate}
                className="px-6 py-3 bg-[#17a2b8] text-white rounded-lg hover:bg-[#138496] transition-colors font-medium flex items-center gap-2"
              >
                <span className="text-xl">+</span>
                Add LLM Config
              </button>
            </div>

            {/* Usage Summary */}
            {usageSummary && (
              <div className="mt-6 grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white p-4 rounded-lg border border-gray-200">
                  <div className="text-sm text-gray-600">Total Configs</div>
                  <div className="text-2xl font-bold text-gray-900 mt-1">
                    {usageSummary.total_configs}
                  </div>
                </div>
                
                <div className="bg-white p-4 rounded-lg border border-gray-200">
                  <div className="text-sm text-gray-600">Tokens Today</div>
                  <div className="text-2xl font-bold text-gray-900 mt-1">
                    {usageSummary.total_tokens_today.toLocaleString()}
                  </div>
                </div>
                
                <div className="bg-white p-4 rounded-lg border border-gray-200">
                  <div className="text-sm text-gray-600">Tokens This Month</div>
                  <div className="text-2xl font-bold text-gray-900 mt-1">
                    {usageSummary.total_tokens_month.toLocaleString()}
                  </div>
                </div>
                
                <div className="bg-white p-4 rounded-lg border border-gray-200">
                  <div className="text-sm text-gray-600">Estimated Cost (Month)</div>
                  <div className="text-2xl font-bold text-gray-900 mt-1">
                    ${usageSummary.estimated_cost_month.toFixed(2)}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Config Cards */}
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="text-gray-500">Loading configurations...</div>
            </div>
          ) : configs.length === 0 ? (
            <div className="text-center py-16">
              <div className="text-gray-400 text-5xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold text-gray-700 mb-2">
                No LLM Configurations Yet
              </h3>
              <p className="text-gray-500 mb-6">
                Add your first LLM configuration to start using AI agents
              </p>
              <button
                onClick={handleCreate}
                className="px-6 py-3 bg-[#17a2b8] text-white rounded-lg hover:bg-[#138496] transition-colors font-medium"
              >
                Add LLM Config
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {configs.map((config) => (
                <LLMConfigCard
                  key={config.id}
                  config={config}
                  onEdit={() => handleEdit(config)}
                  onDelete={() => handleDelete(config.id)}
                  onSetDefault={() => handleSetDefault(config.id)}
                />
              ))}
            </div>
          )}
        </main>
      </div>

      <Footer />

      {/* Modal for Create/Edit */}
      {showModal && (
        <LLMConfigModal
          projectId={projectId}
          config={editingConfig}
          onClose={handleModalClose}
        />
      )}
    </div>
  );
}