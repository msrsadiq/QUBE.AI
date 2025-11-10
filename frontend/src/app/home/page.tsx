/**
 * Home Page
 * ----------
 * Main landing page after login - displays all projects.
 * 
 * Features:
 * - Project list in card grid layout
 * - Search bar for filtering projects
 * - Add Project button (top right)
 * - Empty state with call-to-action
 * - Project CRUD operations (view, edit, delete)
 * 
 * Layout:
 * - Header with menu button
 * - Collapsible sidebar with global options
 * - Project cards in responsive grid (1-3 columns)
 * - Footer with copyright
 * 
 * Data Flow:
 * 1. Check authentication (redirect to login if not authenticated)
 * 2. Fetch all projects from API
 * 3. Display projects sorted by creation date (newest first)
 * 4. Handle search, delete operations
 * 
 * User Actions:
 * - Click "Add Project" → Navigate to /projects/new
 * - Click project card → Navigate to project dashboard
 * - Search projects → Filter by name/domain
 * - Delete project → Confirm and remove from list
 */

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import ProjectCard from '@/components/ProjectCard';
import ProjectModal from '@/components/ProjectModal';
import { api } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

interface ProjectListItem {
  id: number;
  name: string;
  domain: string;
  created_at: string;
}

interface ProjectFull {
  id: number;
  name: string;
  domain: string;
  brief: string;
  tech_stack: string;
  figma_url: string;
  compliances: string;
  created_at: string;
}

export default function HomePage() {
  const router = useRouter();
  const { token, logout } = useAuthStore();
  
  const [projects, setProjects] = useState<ProjectListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<ProjectFull | null>(null);
  const [loadingProject, setLoadingProject] = useState(false);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (!storedToken && !token) {
      router.replace('/');
      return;
    }
    fetchProjects();
  }, [token]);

  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects/');
      setProjects(response.data);
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (term: string) => {
    setSearchTerm(term);
    if (term.trim()) {
      try {
        const response = await api.get(`/projects/search?q=${term}`);
        setProjects(response.data);
      } catch (error) {
        console.error('Search failed:', error);
      }
    } else {
      fetchProjects();
    }
  };

  const handleCreateProject = async (data: Omit<ProjectFull, 'id' | 'created_at'>) => {
    try {
      await api.post('/projects/', data);
      await fetchProjects();
    } catch (error) {
      console.error('Failed to create project:', error);
      throw error;
    }
  };

  const handleUpdateProject = async (data: Omit<ProjectFull, 'id' | 'created_at'>) => {
    if (!editingProject) return;
    try {
      await api.put(`/projects/${editingProject.id}`, data);
      await fetchProjects();
      setEditingProject(null);
    } catch (error) {
      console.error('Failed to update project:', error);
      throw error;
    }
  };

  const handleDeleteProject = async (projectId: number) => {
    if (!confirm('Are you sure you want to delete this project?')) {
      return;
    }
    
    try {
      await api.delete(`/projects/${projectId}`);
      setProjects(projects.filter(p => p.id !== projectId));
    } catch (error) {
      console.error('Failed to delete project:', error);
      alert('Failed to delete project. Please try again.');
    }
  };

  const handleEditClick = async (projectId: number) => {
    setLoadingProject(true);
    try {
      // Fetch FULL project data including all fields
      const response = await api.get(`/projects/${projectId}`);
      setEditingProject(response.data);
      setModalOpen(true);
    } catch (error) {
      console.error('Failed to fetch project details:', error);
      alert('Failed to load project details. Please try again.');
    } finally {
      setLoadingProject(false);
    }
  };

  const handleModalClose = () => {
    setModalOpen(false);
    setEditingProject(null);
  };

  const handleLogout = () => {
    logout();
    router.replace('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      
      <Sidebar 
        isOpen={sidebarOpen} 
        onClose={() => setSidebarOpen(false)}
        onLogout={handleLogout}
        showGlobalOptions={true}
      />

      <main className="flex-1 container mx-auto px-6 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">
            QUBEAI - Projects List
          </h1>
          <button
            onClick={() => {
              setEditingProject(null);
              setModalOpen(true);
            }}
            className="bg-primary-500 text-white px-6 py-3 rounded-lg hover:bg-primary-600 transition-colors flex items-center gap-2"
          >
            <span className="text-xl">⊕</span>
            Add Project
          </button>
        </div>

        <div className="mb-6">
          <input
            type="text"
            placeholder="Search all projects..."
            value={searchTerm}
            onChange={(e) => handleSearch(e.target.value)}
            className="w-full max-w-md px-4 py-2 border border-primary-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {projects.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-xl text-gray-600 mb-6">
              No Projects Available
            </p>
            <button
              onClick={() => {
                setEditingProject(null);
                setModalOpen(true);
              }}
              className="bg-primary-500 text-white px-8 py-3 rounded-lg hover:bg-primary-600 transition-colors"
            >
              Add Project
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                onDelete={handleDeleteProject}
                onEdit={() => handleEditClick(project.id)}
                onClick={() => router.push(`/projects/${project.id}`)}
              />
            ))}
          </div>
        )}
      </main>

      <footer className="bg-primary-500 text-center py-4 text-white text-sm">
        Copyright © 2025 Qube.AI. All rights reserved.
      </footer>

      {/* Loading Overlay */}
      {loadingProject && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6">
            <div className="text-center">
              <div className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-gray-600">Loading project details...</p>
            </div>
          </div>
        </div>
      )}

      {/* Project Modal */}
      <ProjectModal
        isOpen={modalOpen}
        onClose={handleModalClose}
        onSubmit={editingProject ? handleUpdateProject : handleCreateProject}
        project={editingProject}
        mode={editingProject ? 'edit' : 'create'}
      />
    </div>
  );
}