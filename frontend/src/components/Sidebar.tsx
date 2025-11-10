/**
 * Sidebar Navigation Component
 * ----------------------------
 * Collapsible side navigation menu with context-aware menu items.
 * 
 * Features:
 * - Slide-in animation from left
 * - Overlay backdrop (closes on click)
 * - Context-aware navigation items:
 *   - Global Options: Users, Prompts (on home page)
 *   - Project Options: LLM Settings, Requirements, Test Cases (in projects)
 * - Logout button at bottom
 * 
 * Props:
 * - isOpen: Controls sidebar visibility
 * - onClose: Callback to close sidebar
 * - onLogout: Callback to handle logout
 * - projectId: Current project ID (if in project context)
 * - showGlobalOptions: Show global navigation (home page)
 * - showProjectOptions: Show project navigation (project pages)
 * 
 * Navigation Structure:
 * - Home (always visible)
 * - Global Options (when on home page)
 *   - Users (future: user management)
 *   - Prompt Ops (prompt versioning)
 * - Project Options (when in a project)
 *   - LLM Settings
 *   - Requirements Home
 *   - Test Cases Home
 *   - Page Objects
 * - Logout (always at bottom)
 */

'use client';

import { useRouter } from 'next/navigation';

interface SidebarProps {
  /** Controls sidebar visibility (open/closed) */
  isOpen: boolean;
  /** Callback to close the sidebar */
  onClose: () => void;
  /** Callback to handle logout action */
  onLogout: () => void;
  /** Current project ID (optional, for project context) */
  projectId?: string;
  /** Show global navigation options (Users, Prompts) */
  showGlobalOptions?: boolean;
  /** Show project-specific navigation options */
  showProjectOptions?: boolean;
}

export default function Sidebar({
  isOpen,
  onClose,
  onLogout,
  projectId,
  showGlobalOptions = false,
  showProjectOptions = false
}: SidebarProps) {
  const router = useRouter();

  /**
   * Handle navigation and close sidebar
   * @param path - Navigation path (e.g., '/home', '/projects/1')
   */
  const handleNavigation = (path: string) => {
    router.push(path);
    onClose(); // Close sidebar after navigation
  };

  return (
    <>
      {/* Overlay Backdrop - Appears when sidebar is open */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Panel - Slides in from left */}
      <div
        className={`fixed left-0 top-0 h-full w-64 bg-white shadow-lg transform transition-transform duration-300 z-50 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        aria-label="Navigation sidebar"
      >
        <div className="flex flex-col h-full">
          {/* SIDEBAR HEADER */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-primary-500">Menu</h2>
              {/* Close Button */}
              <button
                onClick={onClose}
                className="text-gray-600 hover:text-gray-800 text-2xl leading-none"
                aria-label="Close menu"
              >
                ×
              </button>
            </div>
          </div>

          {/* SIDEBAR NAVIGATION - Scrollable content area */}
          <nav className="flex-1 overflow-y-auto p-4 space-y-1">
            {/* HOME - Always visible on all pages */}
            <button
              onClick={() => handleNavigation('/home')}
              className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors flex items-center gap-3 text-gray-700"
            >
              <span className="text-xl">🏠</span>
              <span className="font-medium">Home</span>
            </button>

            {/* GLOBAL OPTIONS - Shown on home page only */}
            {showGlobalOptions && (
              <>
                {/* Section Header */}
                <div className="pt-4 pb-2 px-4">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    Global Settings
                  </h3>
                </div>

                {/* Users Management (Future Phase) */}
                <button
                  onClick={() => handleNavigation('/users')}
                  className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors flex items-center gap-3 text-gray-700"
                  title="User management (Coming soon)"
                >
                  <span className="text-xl">👥</span>
                  <span className="font-medium">Users</span>
                </button>

                {/* Prompt Ops - Prompt Versioning */}
                <button
                  onClick={() => handleNavigation('/prompts')}
                  className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors flex items-center gap-3 text-gray-700"
                  title="Prompt versioning and management"
                >
                  <span className="text-xl">📝</span>
                  <span className="font-medium">Prompt Ops</span>
                </button>
              </>
            )}

            {/* PROJECT OPTIONS - Shown when in a project context */}
            {showProjectOptions && projectId && (
              <>
                {/* Section Header */}
                <div className="pt-4 pb-2 px-4">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    Project Settings
                  </h3>
                </div>

                {/* LLM Settings - Configure models for this project */}
                <button
                  onClick={() => handleNavigation(`/projects/${projectId}/llm-settings`)}
                  className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors flex items-center gap-3 text-gray-700"
                  title="Configure LLM models for this project"
                >
                  <span className="text-xl">⚙️</span>
                  <span className="font-medium">LLM Settings</span>
                </button>

                {/* Requirements Home - View all requirements */}
                <button
                  onClick={() => handleNavigation(`/projects/${projectId}/requirements`)}
                  className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors flex items-center gap-3 text-gray-700"
                  title="View and manage project requirements"
                >
                  <span className="text-xl">📋</span>
                  <span className="font-medium">Requirements Home</span>
                </button>

                {/* Test Cases Home - View all test cases */}
                <button
                  onClick={() => handleNavigation(`/projects/${projectId}/testcases`)}
                  className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors flex items-center gap-3 text-gray-700"
                  title="View and manage test cases"
                >
                  <span className="text-xl">🧪</span>
                  <span className="font-medium">Test Cases Home</span>
                </button>

                {/* Page Objects - View generated page objects */}
                <button
                  onClick={() => handleNavigation(`/projects/${projectId}/page-objects`)}
                  className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors flex items-center gap-3 text-gray-700"
                  title="View generated page object models"
                >
                  <span className="text-xl">📄</span>
                  <span className="font-medium">Page Objects</span>
                </button>
              </>
            )}
          </nav>

          {/* SIDEBAR FOOTER - Logout Button */}
          <div className="p-4 border-t border-gray-200">
            <button
              onClick={onLogout}
              className="w-full text-left px-4 py-3 rounded-lg hover:bg-red-50 transition-colors flex items-center gap-3 text-red-600 font-medium"
              title="Logout from Qube.AI"
            >
              <span className="text-xl">🚪</span>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </>
  );
}