'use client';

import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import axios from 'axios';
import Sidebar from '@/components/layout/Sidebar';
import TopBar from '@/components/layout/TopBar';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, Zap, Bug, Code, Lock } from 'lucide-react';

interface Project {
  id: number;
  name: string;
  brief: string;
  domain: string;
  tech_stack: string;
}

const AGENTS = [
  {
    id: 'requirement_analysis',
    title: 'Requirement Analyzer',
    description:
      'Efficiently analyze and refine project requirements with AI assistance, ensuring clarity and completeness for effective test case generation.',
    icon: FileText,
    enabled: true,
    path: '/agents/requirement-analysis',
  },
  {
    id: 'api_testing',
    title: 'API Agent',
    description:
      'Generate comprehensive API test cases and automation scripts with intelligent test scenario generation.',
    icon: Zap,
    enabled: false,
    path: '/agents/api-testing',
  },
  {
    id: 'bugs_manager',
    title: 'Bugs Manager',
    description:
      'Track, prioritize, and manage reported bugs across your projects, streamlining the defect lifecycle for faster resolution.',
    icon: Bug,
    enabled: false,
    path: '/agents/bugs-manager',
  },
  {
    id: 'automation',
    title: 'Automation',
    description:
      'Build and execute automated test scenarios across web, API, and mobile applications with intelligent automation strategies.',
    icon: Code,
    enabled: false,
    path: '/agents/automation',
  },
];

export default function ProjectDashboard() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;

  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProject = async () => {
      try {
        const response = await axios.get(`/api/v1/projects/${projectId}`);
        setProject(response.data);
      } catch (error) {
        console.error('Failed to fetch project:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [projectId]);

  if (loading) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar projectId={projectId} />
        <div className="flex-1 flex flex-col">
          <TopBar />
          <main className="flex-1 flex items-center justify-center">
            <p className="text-gray-500">Loading...</p>
          </main>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar projectId={projectId} />

      <div className="flex-1 flex flex-col">
        <TopBar />

        <main className="flex-1 overflow-auto p-8">
          <div className="max-w-7xl mx-auto">
            {/* Page Header */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-gray-900">
                {project?.name} Dashboard
              </h1>
              <p className="text-gray-600 mt-2">
                {project?.brief || 'Welcome to your project dashboard'}
              </p>
            </div>

            {/* Agents Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {AGENTS.map((agent) => {
                const Icon = agent.icon;
                
                return (
                  <Card
                    key={agent.id}
                    className={`overflow-hidden transition-all ${
                      agent.enabled
                        ? 'hover:shadow-lg cursor-pointer border-teal-200'
                        : 'opacity-60 cursor-not-allowed'
                    }`}
                    onClick={() => {
                      if (agent.enabled) {
                        router.push(`/projects/${projectId}${agent.path}`);
                      }
                    }}
                  >
                    <CardHeader className="pb-4">
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3">
                          <div className="p-2 bg-teal-50 rounded-lg">
                            <Icon className="w-6 h-6 text-teal-600" />
                          </div>
                          <div className="flex-1">
                            <CardTitle className="text-lg">{agent.title}</CardTitle>
                          </div>
                        </div>
                        {!agent.enabled && (
                          <span className="px-3 py-1 bg-yellow-100 text-yellow-700 text-xs font-semibold rounded-full flex items-center gap-1">
                            <Lock className="w-3 h-3" />
                            Coming Soon
                          </span>
                        )}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-base text-gray-700">
                        {agent.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}