'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore, useProjectStore } from '@/lib/store';
import { projectsAPI } from '@/lib/api';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import ProjectCard from '@/components/ProjectCard';
import { PlusCircle } from 'lucide-react';

export default function HomePage() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const { projects, setProjects, deleteProject: removeProject } = useProjectStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/');
      return;
    }

    fetchProjects();
  }, [isAuthenticated, router]);

  const fetchProjects = async () => {
    try {
      const response = await projectsAPI.getAll();
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this project?')) return;

    try {
      await projectsAPI.delete(id);
      removeProject(id);
    } catch (error) {
      console.error('Error deleting project:', error);
      alert('Failed to delete project');
    }
  };

  const handleEdit = (id: number) => {
    router.push(`/projects/${id}/edit`);
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <div className="flex flex-1">
        <Sidebar />

        <main className="flex-1 p-8">
          <div className="max-w-7xl mx-auto">
            {/* Header Section */}
            <div className="mb-8">
              <div className="flex items-center justify-between">
                <h1 className="text-4xl font-bold text-primary mb-2">
                  Welcome to Qube.AI.
                </h1>

                {/* Add Project Button */}
                <button
                  onClick={() => router.push('/projects/new')}
                  className="flex items-center space-x-2 btn-primary"
                >
                  <PlusCircle className="w-5 h-5" />
                  <span>Add Project</span>
                </button>
              </div>
            </div>

            {/* Projects List */}
            <div>
              <h2 className="text-2xl font-bold text-primary mb-6">
                Projects List
              </h2>

              {loading ? (
                <div className="text-center py-12">
                  <p className="text-secondary-light">Loading projects...</p>
                </div>
              ) : projects.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-secondary-light mb-4">
                    No projects yet. Create your first project!
                  </p>
                  <button
                    onClick={() => router.push('/projects/new')}
                    className="btn-primary"
                  >
                    Add Project
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {projects.map((project) => (
                    <ProjectCard
                      key={project.id}
                      id={project.id}
                      name={project.name}
                      brief={project.brief}
                      created_at={project.created_at}
                      onDelete={() => handleDelete(project.id)}
                      onEdit={() => handleEdit(project.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        </main>
      </div>

      {/* Footer */}
      <div className="bg-primary py-4 text-center">
        <p className="text-white text-sm">Copywright</p>
      </div>
    </div>
  );
}