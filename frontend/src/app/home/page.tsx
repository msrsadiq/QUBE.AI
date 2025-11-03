/**
 * Home dashboard page (post-login).
 * 
 * Features:
 * - Welcome message with user name
 * - Project list grid (to be implemented in Phase 2)
 * - Add new project button (to be implemented in Phase 2)
 * - Search functionality (to be implemented in Phase 2)
 * 
 * Route: /home
 */

'use client';

import { useAuthStore } from '@/lib/store';
import { Plus, Search } from 'lucide-react';

/**
 * Home dashboard component.
 * 
 * Displays:
 * - Welcome message
 * - Search bar (placeholder for Phase 2)
 * - Add Project button (placeholder for Phase 2)
 * - Projects list (placeholder for Phase 2)
 * 
 * Future Phases:
 * - Phase 2: Project CRUD operations
 * - Phase 3: Project cards with metadata
 * - Phase 4: Search and filter functionality
 */
export default function HomePage() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome to Qube.AI.
          </h1>
          <p className="text-gray-600 mt-2">
            Hello, <span className="font-medium text-primary-600">{user?.full_name || user?.username}</span>! 
            Start by creating a project or exploring your existing projects.
          </p>
        </div>
      </div>

      {/* Search and Add Project Bar */}
      <div className="flex items-center gap-4">
        {/* Search Box (Placeholder) */}
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search all projects..."
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled
          />
        </div>

        {/* Add Project Button (Placeholder) */}
        <button
          className="btn-primary flex items-center gap-2 px-6 py-3 whitespace-nowrap"
          disabled
          title="Coming in Phase 2"
        >
          <Plus className="w-5 h-5" />
          <span>Add Project</span>
        </button>
      </div>

      {/* Projects Section */}
      <div>
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          Projects List
        </h2>

        {/* Empty State (Phase 1) */}
        <div className="bg-white rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
          <div className="max-w-md mx-auto">
            <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Plus className="w-10 h-10 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              No Projects Yet
            </h3>
            <p className="text-gray-500 mb-6">
              Get started by creating your first project. Projects help you organize your testing workflows and requirements.
            </p>
            <button
              className="btn-primary inline-flex items-center gap-2"
              disabled
              title="Coming in Phase 2"
            >
              <Plus className="w-5 h-5" />
              <span>Create Your First Project</span>
            </button>
            <p className="text-sm text-gray-400 mt-4">
              Phase 2 Feature - Coming Soon
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}