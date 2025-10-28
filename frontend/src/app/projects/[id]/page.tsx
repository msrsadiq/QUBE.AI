'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuthStore, useProjectStore } from '@/lib/store';
import { projectsAPI } from '@/lib/api';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import {
  FileText,
  Wrench,
  Bug,
  Search,
  Upload,
  MessageSquare,
} from 'lucide-react';

export default function ProjectHomePage() {
  const router = useRouter();
  const params = useParams();
  const projectId = parseInt(params.id as string);

  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const { currentProject, setCurrentProject } = useProjectStore();
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

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
      setCurrentProject(response.data);
    } catch (error) {
      console.error('Error fetching project:', error);
      router.push('/home');
    } finally {
      setLoading(false);
    }
  };

  const agentCards = [
    {
      title: 'Requirement Analyzer',
      description:
        'Efficiently analyze and refine project requirements with AI assistance, ensuring clarity and completeness for effective test case generation.',
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      onClick: () => alert('Requirement Analyzer - Coming Soon!'),
    },
    {
      title: 'Testcase Generator',
      description:
        'Generate comprehensive test cases automatically from LLM prompts and requirements, supporting various test types.',
      icon: Wrench,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      onClick: () => alert('Testcase Generator - Coming Soon!'),
    },
    {
      title: 'Bugs Manager',
      description:
        'Track, prioritize, and manage reported bugs across your projects, streamlining the defect lifecycle for faster resolution.',
      icon: Bug,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
      onClick: () => alert('Bugs Manager - Coming Soon!'),
    },
  ];

  const filteredCards = agentCards.filter((card) =>
    card.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

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

        <main className="flex-1 p-8">
          <div className="max-w-7xl mx-auto">
            {/* Header Section */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-secondary mb-2">
                Project Dashboard
              </h1>
              <p className="text-secondary-light text-lg">
                Welcome to {currentProject?.name}. Explore your project modules
                and streamline your software testing workflow.
              </p>

              <div className="flex items-center space-x-4 mt-6">
                {/* Search Bar */}
                <div className="relative flex-1 max-w-md">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search modules or test cases..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border-2 border-primary rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>

                {/* Action Buttons */}
                <button className="flex items-center space-x-2 px-6 py-2 bg-white border-2 border-primary text-primary rounded-md hover:bg-primary hover:text-white transition-colors">
                  <Upload className="w-5 h-5" />
                  <span>Upload</span>
                </button>

                <button className="flex items-center space-x-2 btn-primary">
                  <MessageSquare className="w-5 h-5" />
                  <span>Add New</span>
                </button>
              </div>
            </div>

            {/* Modules Section */}
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-secondary mb-1">
                MODULES
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                {filteredCards.map((card, index) => {
                  const Icon = card.icon;
                  return (
                    <div
                      key={index}
                      onClick={card.onClick}
                      className="card cursor-pointer hover:border-2 hover:border-primary transition-all group"
                    >
                      <div
                        className={`w-16 h-16 ${card.bgColor} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}
                      >
                        <Icon className={`w-8 h-8 ${card.color}`} />
                      </div>
                      <h3 className="text-xl font-bold text-secondary mb-2">
                        {card.title}
                      </h3>
                      <p className="text-secondary-light text-sm">
                        {card.description}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Footer */}
      <div className="bg-primary py-4 text-center flex items-center justify-between px-8">
        <div className="flex space-x-6 text-white text-sm">
          <span className="cursor-pointer hover:underline">Quick Links</span>
          <span className="cursor-pointer hover:underline">Legal</span>
        </div>
        <div className="flex space-x-4">
          <a
            href="#"
            className="text-white hover:text-gray-200 transition-colors"
          >
            <svg
              className="w-5 h-5"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z" />
            </svg>
          </a>
          <a
            href="#"
            className="text-white hover:text-gray-200 transition-colors"
          >
            <svg
              className="w-5 h-5"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
            </svg>
          </a>
        </div>
      </div>
    </div>
  );
}