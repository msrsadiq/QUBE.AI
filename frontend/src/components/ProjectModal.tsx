'use client';

import { useState, useEffect } from 'react';

interface Project {
  id?: number;
  name: string;
  brief: string;
  domain: string;
  tech_stack: string;
  figma_url: string;
  compliances: string;
}

interface ProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: Omit<Project, 'id'>) => Promise<void>;
  project?: Project | null;
  mode: 'create' | 'edit';
}

export default function ProjectModal({ 
  isOpen, 
  onClose, 
  onSubmit, 
  project, 
  mode 
}: ProjectModalProps) {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    brief: '',
    domain: '',
    tech_stack: '',
    figma_url: '',
    compliances: '',
  });

  useEffect(() => {
    if (project && mode === 'edit') {
      setFormData({
        name: project.name || '',
        brief: project.brief || '',
        domain: project.domain || '',
        tech_stack: project.tech_stack || '',
        figma_url: project.figma_url || '',
        compliances: project.compliances || '',
      });
    } else {
      setFormData({
        name: '',
        brief: '',
        domain: '',
        tech_stack: '',
        figma_url: '',
        compliances: '',
      });
    }
  }, [project, mode, isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await onSubmit(formData);
      onClose();
    } catch (error) {
      console.error('Failed to save project:', error);
      alert('Failed to save project. Please try again.');
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

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
          {/* Modal Header */}
          <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
            <h2 className="text-2xl font-bold text-primary-500">
              {mode === 'create' ? 'Add New Project' : 'Edit Project'}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-2xl"
            >
              ×
            </button>
          </div>

          {/* Modal Body */}
          <form onSubmit={handleSubmit} className="p-6">
            {/* Project Name */}
            <div className="mb-4">
              <label className="block text-gray-700 font-medium mb-2">
                Project Name *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                maxLength={255}
                placeholder="e.g., E-commerce Platform"
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Project Brief */}
            <div className="mb-4">
              <label className="block text-gray-700 font-medium mb-2">
                Project Brief *
              </label>
              <textarea
                name="brief"
                value={formData.brief}
                onChange={handleChange}
                required
                rows={3}
                placeholder="Detailed description of the project..."
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Domain Area */}
            <div className="mb-4">
              <label className="block text-gray-700 font-medium mb-2">
                Domain Area *
              </label>
              <input
                type="text"
                name="domain"
                value={formData.domain}
                onChange={handleChange}
                required
                maxLength={255}
                placeholder="e.g., E-commerce, Healthcare, FinTech"
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Tech Stack */}
            <div className="mb-4">
              <label className="block text-gray-700 font-medium mb-2">
                Tech Stack
              </label>
              <textarea
                name="tech_stack"
                value={formData.tech_stack}
                onChange={handleChange}
                rows={2}
                placeholder="e.g., React, Node.js, PostgreSQL"
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Figma URL */}
            <div className="mb-4">
              <label className="block text-gray-700 font-medium mb-2">
                Figma Prototype URL
              </label>
              <input
                type="url"
                name="figma_url"
                value={formData.figma_url}
                onChange={handleChange}
                placeholder="https://figma.com/file/..."
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Compliances */}
            <div className="mb-6">
              <label className="block text-gray-700 font-medium mb-2">
                Compliance Requirements
              </label>
              <textarea
                name="compliances"
                value={formData.compliances}
                onChange={handleChange}
                rows={2}
                placeholder="e.g., GDPR, HIPAA, SOC2"
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Modal Footer */}
            <div className="flex justify-end gap-4 pt-4 border-t border-gray-200">
              <button
                type="button"
                onClick={onClose}
                className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                disabled={loading}
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors disabled:opacity-50"
              >
                {loading ? 'Saving...' : mode === 'create' ? 'Create Project' : 'Update Project'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}