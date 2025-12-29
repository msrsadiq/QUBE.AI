/**
 * Home Page
 * ---------
 * Project list and management dashboard.
 */

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import Footer from '@/components/Footer';
import ProjectCard from '@/components/ProjectCard';
import ProjectModal from '@/components/ProjectModal';

interface Project {
  id: number;
  project_code: string;  // Added
  name: string;
  domain: string;
  brief: string;
  tech_stack?: string;
  created_at: string;
}

export default function HomePage() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchProjects();
    }
  }, [isAuthenticated]);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/projects/');
      console.log('Fetched projects:', response.data); // DEBUG LOG
      setProjects(response.data);
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (projectId: number) => {
    if (!confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
      return;
    }

    try {
      await api.delete(`/api/projects/${projectId}`);
      fetchProjects();
    } catch (error) {
      console.error('Failed to delete project:', error);
      alert('Failed to delete project. Please try again.');
    }
  };

  const handleEdit = (project: Project) => {
    setEditingProject(project);
    setShowProjectModal(true);
  };

  const handleModalClose = (saved: boolean) => {
    setShowProjectModal(false);
    setEditingProject(null);
    if (saved) {
      fetchProjects();
    }
  };

  const filteredProjects = projects.filter((project) =>
    project.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    project.domain.toLowerCase().includes(searchQuery.toLowerCase()) ||
    project.brief.toLowerCase().includes(searchQuery.toLowerCase()) ||
    project.project_code.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      
      <div className="flex flex-1">
        <Sidebar context="home" />
        
        <main className="flex-1 p-8">
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Welcome to Qube.AI
                </h1>
                <p className="text-gray-600 mt-1">
                  Manage your projects
                </p>
              </div>
              
              <button
                onClick={() => setShowProjectModal(true)}
                className="px-6 py-3 bg-[#17a2b8] text-white rounded-lg hover:bg-[#138496] transition-colors font-medium flex items-center gap-2"
              >
                <span className="text-xl">⊕</span>
                Add Project
              </button>
            </div>

            <div className="mt-6">
              <input
                type="text"
                placeholder="Search all projects..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#17a2b8] focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-[#17a2b8] mb-6">
              Projects List
            </h2>

            {loading ? (
              <div className="flex justify-center items-center h-64">
                <div className="text-gray-500 flex items-center gap-3">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#17a2b8]"></div>
                  <span>Loading projects...</span>
                </div>
              </div>
            ) : filteredProjects.length === 0 ? (
              <div className="text-center py-16">
                <div className="text-gray-400 text-6xl mb-4">📁</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  {searchQuery ? 'No projects found' : 'No Projects Available'}
                </h3>
                <p className="text-gray-500 mb-6">
                  {searchQuery 
                    ? 'Try adjusting your search terms' 
                    : 'Get started by creating your first project'}
                </p>
                {!searchQuery && (
                  <button
                    onClick={() => setShowProjectModal(true)}
                    className="px-6 py-3 bg-[#17a2b8] text-white rounded-lg hover:bg-[#138496] transition-colors font-medium"
                  >
                    Create Your First Project
                  </button>
                )}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {filteredProjects.map((project) => (
                  <ProjectCard
                    key={project.id}
                    project={project}
                    onDelete={() => handleDelete(project.id)}
                    onEdit={() => handleEdit(project)}
                  />
                ))}
              </div>
            )}

            {!loading && filteredProjects.length > 0 && (
              <div className="mt-6 text-sm text-gray-600">
                Showing {filteredProjects.length} of {projects.length} project{projects.length !== 1 ? 's' : ''}
              </div>
            )}
          </div>
        </main>
      </div>

      <Footer />

      {showProjectModal && (
        <ProjectModal
          project={editingProject}
          onClose={handleModalClose}
        />
      )}
    </div>
  );
}