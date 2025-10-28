'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuthStore, useProjectStore } from '@/lib/store';
import { projectsAPI } from '@/lib/api';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import { Edit } from 'lucide-react';

export default function EditProjectPage() {
  const router = useRouter();
  const params = useParams();
  const projectId = parseInt(params.id as string);

  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const updateProject = useProjectStore((state) => state.updateProject);

  const [formData, setFormData] = useState({
    name: '',
    domain: '',
    brief: '',
    tech_stack: '',
    figma_url: '',
    compliance: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/');
      return;
    }

    fetchProject();
  }, [isAuthenticated, projectId, router]);

  const fetchProject = async () => {
    try {
      const response = await projectsAPI.getById(projectId);
      const project = response.data;
      setFormData({
        name: project.name,
        domain: project.domain,
        brief: project.brief,
        tech_stack: project.tech_stack || '',
        figma_url: project.figma_url || '',
        compliance: project.compliance || '',
      });
    } catch (error) {
      console.error('Error fetching project:', error);
      router.push('/home');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSaving(true);

    try {
      const response = await projectsAPI.update(projectId, formData);
      updateProject(projectId, response.data);
      router.push('/home');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update project');
    } finally {
      setSaving(false);
    }
  };

  if (!isAuthenticated || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-secondary-light">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <div className="flex flex-1">
        <Sidebar />

        <main className="flex-1 p-8 bg-gray-50">
          <div className="max-w-3xl mx-auto">
            <div className="bg-white rounded-lg shadow-md p-8">
              <div className="flex items-center mb-6">
                <Edit className="w-8 h-8 text-primary mr-3" />
                <h1 className="text-3xl font-bold text-primary">
                  Edit Project
                </h1>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-secondary mb-2">
                    Project Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-secondary mb-2">
                    Project Brief <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    name="brief"
                    value={formData.brief}
                    onChange={handleChange}
                    rows={4}
                    className="textarea-field"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-secondary mb-2">
                    Domain Area <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="domain"
                    value={formData.domain}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-secondary mb-2">
                    Teck Stack
                  </label>
                  <textarea
                    name="tech_stack"
                    value={formData.tech_stack}
                    onChange={handleChange}
                    rows={3}
                    className="textarea-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-secondary mb-2">
                    Figma Prototype URL
                  </label>
                  <input
                    type="url"
                    name="figma_url"
                    value={formData.figma_url}
                    onChange={handleChange}
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-secondary mb-2">
                    Compliance Requirements
                  </label>
                  <textarea
                    name="compliance"
                    value={formData.compliance}
                    onChange={handleChange}
                    rows={3}
                    className="textarea-field"
                  />
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
                    {error}
                  </div>
                )}

                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => router.push('/home')}
                    className="flex-1 btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={saving}
                    className="flex-1 btn-primary disabled:opacity-50"
                  >
                    {saving ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </main>
      </div>

      <div className="bg-primary py-4 text-center">
        <p className="text-white text-sm">
          Company &nbsp;&nbsp; Resources &nbsp;&nbsp; Legal
        </p>
      </div>
    </div>
  );
}