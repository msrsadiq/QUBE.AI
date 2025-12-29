/**
 * Project Modal Component
 * -----------------------
 * Modal for creating and editing projects.
 */

'use client';

import { useState, useEffect, FormEvent } from 'react';
import api from '@/lib/api';

interface ProjectModalProps {
  project?: {
    id: number;
    name: string;
    domain: string;
    brief: string;
    tech_stack?: string;
    figma_url?: string;
    compliances?: string;
  } | null;
  onClose: (saved: boolean) => void;
}

export default function ProjectModal({ project, onClose }: ProjectModalProps) {
  const isEditMode = !!project;

  const [formData, setFormData] = useState({
    name: '',
    domain: '',
    brief: '',
    tech_stack: '',
    figma_url: '',
    compliances: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (project) {
      setFormData({
        name: project.name,
        domain: project.domain,
        brief: project.brief,
        tech_stack: project.tech_stack || '',
        figma_url: project.figma_url || '',
        compliances: project.compliances || '',
      });
    }
  }, [project]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isEditMode) {
        await api.put(`/api/projects/${project.id}`, formData);
      } else {
        await api.post('/api/projects/', formData);
      }
      onClose(true);
    } catch (err: any) {
      console.error('Failed to save project:', err);
      setError(err.response?.data?.detail || 'Failed to save project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">
            {isEditMode ? 'Edit Project' : 'Add New Project'}
          </h2>
          <button
            onClick={() => onClose(false)}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Project Name *
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
              placeholder="Enter project name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Domain Area *
            </label>
            <input
              type="text"
              value={formData.domain}
              onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
              placeholder="e.g., E-commerce, Healthcare, Finance"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Project Brief *
            </label>
            <textarea
              value={formData.brief}
              onChange={(e) => setFormData({ ...formData, brief: e.target.value })}
              required
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
              placeholder="Describe your project..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Tech Stack
            </label>
            <input
              type="text"
              value={formData.tech_stack}
              onChange={(e) => setFormData({ ...formData, tech_stack: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
              placeholder="e.g., React, Node.js, PostgreSQL"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Figma Prototype URL
            </label>
            <input
              type="url"
              value={formData.figma_url}
              onChange={(e) => setFormData({ ...formData, figma_url: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
              placeholder="https://figma.com/..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Compliance Requirements
            </label>
            <input
              type="text"
              value={formData.compliances}
              onChange={(e) => setFormData({ ...formData, compliances: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
              placeholder="e.g., HIPAA, GDPR, SOC 2"
            />
          </div>

          {/* Footer */}
          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={() => onClose(false)}
              className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-[#17a2b8] text-white rounded-lg hover:bg-[#138496] transition-colors disabled:opacity-50"
            >
              {loading ? 'Saving...' : isEditMode ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}