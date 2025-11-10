/**
 * Edit Project Page
 * -----------------
 * Form page for editing an existing project.
 * 
 * Features:
 * - Pre-populated form with existing project data
 * - All fields editable (including required fields)
 * - Loading state while fetching/updating
 * - Cancel button to go back
 * - Auto-redirect to project dashboard on success
 * 
 * Differences from New Project Page:
 * - Fetches existing project data on mount
 * - Uses PUT instead of POST for submission
 * - Pre-fills form fields with current values
 * - Includes Cancel button
 * 
 * Data Flow:
 * 1. Extract project ID from URL
 * 2. Fetch project details → Pre-fill form
 * 3. User edits fields
 * 4. Submit → PUT /api/projects/{id}
 * 5. On success → Navigate to /projects/{id}
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import { api } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

export default function EditProjectPage() {
  const router = useRouter();
  const params = useParams();
  const projectId = params.id as string;
  const { logout } = useAuthStore();
  
  // Component state
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    brief: '',
    domain: '',
    tech_stack: '',
    figma_url: '',
    compliances: '',
  });

  /**
   * Fetch project details on mount
   */
  useEffect(() => {
    fetchProject();
  }, [projectId]);

  /**
   * Fetch project details and pre-fill form
   */
  const fetchProject = async () => {
    try {
      const response = await api.get(`/projects/${projectId}`);
      const project = response.data;
      
      // Pre-fill form with existing data
      setFormData({
        name: project.name || '',
        brief: project.brief || '',
        domain: project.domain || '',
        tech_stack: project.tech_stack || '',
        figma_url: project.figma_url || '',
        compliances: project.compliances || '',
      });
    } catch (error) {
      console.error('Failed to fetch project:', error);
      alert('Failed to load project. Redirecting to home.');
      router.push('/home');
    } finally {
      setFetching(false);
    }
  };

  /**
   * Handle form submission
   * @param e - Form submit event
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Update project via API
      await api.put(`/projects/${projectId}`, formData);
      
      // Success - Navigate back to project dashboard
      router.push(`/projects/${projectId}`);
    } catch (error) {
      console.error('Failed to update project:', error);
      alert('Failed to update project. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle input field changes
   * @param e - Input change event
   */
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  /**
   * Handle cancel - go back to project dashboard
   */
  const handleCancel = () => {
    router.push(`/projects/${projectId}`);
  };

  // Loading state while fetching project
  if (fetching) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading project...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* HEADER */}
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      
      {/* SIDEBAR */}
      <Sidebar 
        isOpen={sidebarOpen} 
        onClose={() => setSidebarOpen(false)}
        onLogout={() => {
          logout();
          router.push('/login');
        }}
        projectId={projectId}
        showProjectOptions={true}
      />

      {/* MAIN CONTENT */}
      <main className="container mx-auto px-6 py-8">
        <div className="max-w-3xl mx-auto">
          {/* PAGE TITLE */}
          <h1 className="text-3xl font-bold text-primary-500 text-center mb-8">
            Edit Project
          </h1>

          {/* EDIT PROJECT FORM */}
          <form 
            onSubmit={handleSubmit} 
            className="bg-white p-8 rounded-lg border-2 border-gray-300"
          >
            {/* PROJECT NAME (Required) */}
            <div className="mb-6">
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
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* PROJECT BRIEF (Required) */}
            <div className="mb-6">
              <label className="block text-gray-700 font-medium mb-2">
                Project Brief *
              </label>
              <textarea
                name="brief"
                value={formData.brief}
                onChange={handleChange}
                required
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* DOMAIN AREA (Required) */}
            <div className="mb-6">
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
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* TECH STACK (Optional) */}
            <div className="mb-6">
              <label className="block text-gray-700 font-medium mb-2">
                Tech Stack
              </label>
              <textarea
                name="tech_stack"
                value={formData.tech_stack}
                onChange={handleChange}
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* FIGMA URL (Optional) */}
            <div className="mb-6">
              <label className="block text-gray-700 font-medium mb-2">
                Figma Prototype URL
              </label>
              <input
                type="url"
                name="figma_url"
                value={formData.figma_url}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* COMPLIANCES (Optional) */}
            <div className="mb-8">
              <label className="block text-gray-700 font-medium mb-2">
                Compliance Requirements
              </label>
              <textarea
                name="compliances"
                value={formData.compliances}
                onChange={handleChange}
                rows={2}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* ACTION BUTTONS */}
            <div className="flex justify-end gap-4">
              {/* Cancel Button */}
              <button
                type="button"
                onClick={handleCancel}
                className="bg-gray-300 text-gray-700 px-8 py-3 rounded-lg hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
              
              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="bg-primary-500 text-white px-8 py-3 rounded-lg hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Updating...' : 'Update Project'}
              </button>
            </div>
          </form>
        </div>
      </main>

      {/* FOOTER */}
      <footer className="fixed bottom-0 w-full bg-primary-500 text-center py-2 text-white text-sm">
        Copyright © 2025 Qube.AI. All rights reserved.
      </footer>
    </div>
  );
}