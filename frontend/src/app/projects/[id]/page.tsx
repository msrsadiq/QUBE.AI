/**
 * Project Dashboard Page
 * ----------------------
 * Main dashboard for a specific project - displays all agent modules.
 * 
 * Features:
 * - Project name in page title
 * - Welcome message and description
 * - Search bar for filtering agents
 * - Upload and Add New buttons (future functionality)
 * - Agent cards organized by category
 * - Project-specific sidebar navigation
 * 
 * Agent Categories:
 * 1. QE Agents
 *    - Requirement Analyzer
 *    - Testcase Generator
 *    - Bugs Manager
 * 
 * 2. Automation Agents
 *    - Page Object Generator
 *    - Framework Agent
 *    - API Agent
 * 
 * Layout:
 * - Header with project context
 * - Sidebar with project-specific options
 * - Agent cards in responsive grid
 * - Footer with quick links
 * 
 * Data Flow:
 * 1. Extract project ID from URL
 * 2. Fetch project details from API
 * 3. Display agent modules
 * 4. Handle navigation to agent pages
 */
'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import AgentCard from '@/components/AgentCard';
import { api } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

interface Project {
  id: number;
  name: string;
  domain: string;
  brief: string;
}

export default function ProjectHomePage() {
  const router = useRouter();
  const params = useParams();
  const projectId = params.id as string;
  const { logout } = useAuthStore();
  
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    fetchProject();
  }, [projectId]);

  const fetchProject = async () => {
    try {
      const response = await api.get(`/projects/${projectId}`);
      setProject(response.data);
    } catch (error) {
      console.error('Failed to fetch project:', error);
      router.push('/home');
    } finally {
      setLoading(false);
    }
  };

  const agentModules = [
    {
      category: 'Manual Testing',
      agents: [
        {
          id: 'requirement-analyzer',
          name: 'Requirement Analyzer',
          icon: '📋',
          description: 'Efficiently analyze and refine project requirements with AI assistance, ensuring clarity and completeness for effective test case generation.',
          route: `/projects/${projectId}/requirement-analyzer`
        },
        {
          id: 'testcase-generator',
          name: 'Testcase Generator',
          icon: '🧪',
          description: 'Generate comprehensive test cases automatically from LLM prompts and requirements, supporting various test types.',
          route: `/projects/${projectId}/testcase-generator`
        },
        {
          id: 'bugs-manager',
          name: 'Bugs Manager',
          icon: '🐛',
          description: 'Track, prioritize, and manage reported bugs across your projects, streamlining the defect lifecycle for faster resolution.',
          route: `/projects/${projectId}/bugs-manager`
        }
      ]
    },
    {
      category: 'Automation Testing',
      agents: [
        {
          id: 'page-object-generator',
          name: 'Page Object Generator',
          icon: '📄',
          description: 'Automatically generate page object models for web automation frameworks.',
          route: `/projects/${projectId}/page-object-generator`
        },
        {
          id: 'framework-agent',
          name: 'Framework Agent',
          icon: '🏗️',
          description: 'Bootstrap automation frameworks with best practices and structure.',
          route: `/projects/${projectId}/framework-agent`
        },
        {
          id: 'api-agent',
          name: 'API Agent',
          icon: '🔌',
          description: 'Generate API test automation scripts for REST and GraphQL APIs.',
          route: `/projects/${projectId}/api-agent`
        }
      ]
    }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    );
  }

  if (!project) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      
      <Sidebar 
        isOpen={sidebarOpen} 
        onClose={() => setSidebarOpen(false)}
        onLogout={() => {
          logout();
          router.push('/');
        }}
        projectId={projectId}
        showProjectOptions={true}
      />

      <main className="flex-1 container mx-auto px-6 py-8">
        {/* Project Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            {project.name} Dashboard
          </h1>
          <p className="text-gray-600">
            Welcome to QE-CoPilot. An Agentic AI for software testing needs
          </p>
        </div>

        {/* Agent Modules - Horizontal Sections */}
        {agentModules.map((category, idx) => (
          <div key={idx} className="mb-12">
            <h2 className="text-2xl font-bold text-gray-700 mb-6">
              {category.category}
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {category.agents.map((agent) => (
                <AgentCard
                  key={agent.id}
                  agent={agent}
                  onClick={() => router.push(agent.route)}
                />
              ))}
            </div>
          </div>
        ))}
      </main>

      {/* Simple Footer */}
      <footer className="bg-primary-500 text-center py-4 text-white text-sm">
        Copyright © 2025 Qube.AI. All rights reserved.
      </footer>
    </div>
  );
}