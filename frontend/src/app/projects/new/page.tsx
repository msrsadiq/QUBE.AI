/**
 * New Project Page
 * ----------------
 * Form page for creating a new project.
 * 
 * Features:
 * - Form with validation for required fields
 * - Optional fields for tech stack, Figma URL, compliances
 * - Loading state during submission
 * - Error handling and user feedback
 * - Auto-redirect to project dashboard on success
 * 
 * Required Fields:
 * - Project Name (max 255 chars)
 * - Project Brief (detailed description)
 * - Domain Area (e.g., E-commerce, Healthcare)
 * 
 * Optional Fields:
 * - Tech Stack (technologies used)
 * - Figma Prototype URL
 * - Compliance Requirements (GDPR, HIPAA, etc.)
 * 
 * Form Layout:
 * - Centered form with max width
 * - Labels above inputs
 * - Required fields marked with asterisk
 * - Submit button at bottom right
 * 
 * Data Flow:
 * 1. User fills form
 * 2. Submit → POST /api/projects/
 * 3. On success → Navigate to /projects/{id}
 * 4. On error → Show alert (future: toast notification)
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import { api } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

export default function NewProjectPage() {
  const router = useRouter();
  const { logout } = useAuthStore();
  
  // Component state
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    brief: '',
    domain: '',
    tech_stack: '',
    figma_url: '',
    compliances: '',
  });

  /**
   * Handle form submission
   * @param e - Form submit event
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Create project via API
      const response = await api.post('/projects/', formData);
      
      // Success - Navigate to Home
      router.push('/home');
    } catch (error) {
      console.error('Failed to create project:', error);
      alert('Failed to create project. Please try again.');
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
        showGlobalOptions={false}
      />

      {/* MAIN CONTENT */}
      <main className="container mx-auto px-6 py-8">
        <div className="max-w-3xl mx-auto">
          {/* PAGE TITLE */}
          <h1 className="text-3xl font-bold text-primary-500 text-center mb-8">
            Add New Project
          </h1>

          {/* PROJECT FORM */}
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
                placeholder="e.g., E-commerce Platform"
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
                placeholder="Detailed description of the project, its goals, and context..."
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
                placeholder="e.g., E-commerce, Healthcare, FinTech"
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
                placeholder="e.g., React, Node.js, PostgreSQL, Redis, Docker"
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
                placeholder="https://figma.com/file/..."
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
                placeholder="e.g., GDPR, HIPAA, SOC2, PCI-DSS"
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* SUBMIT BUTTON */}
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className="bg-primary-500 text-white px-8 py-3 rounded-lg hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Creating...' : 'Create Project'}
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