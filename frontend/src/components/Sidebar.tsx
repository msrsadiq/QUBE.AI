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

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';

interface SidebarProps {
  context: 'home' | 'project';
  projectId?: number;
}

export default function Sidebar({ context, projectId }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const logout = useAuthStore((state) => state.logout);

  /**
   * Check if a menu item is active based on current path
   */
  const isActive = (path: string) => pathname === path;

  /**
   * Handle logout
   */
  const handleLogout = () => {
    logout();
    router.push('/');
  };

  /**
   * Home page menu items
   */
  const homeMenuItems = [
    { path: '/home', label: 'Home', icon: '🏠' },
    { path: '/home/prompts', label: 'Prompt Ops', icon: '📝' },
    // { path: '/home/users', label: 'Users', icon: '👥' }, // Future phase
  ];

  /**
   * Project page menu items
   */
  const projectMenuItems = projectId
    ? [
        { path: `/projects/${projectId}`, label: 'Home', icon: '🏠' },
        { path: `/projects/${projectId}/llm-config`, label: 'LLM Settings', icon: '🤖' },
        { path: `/projects/${projectId}/requirements`, label: 'Requirements', icon: '📋' },
        { path: `/projects/${projectId}/test-cases`, label: 'Test Cases', icon: '✅' },
        { path: `/projects/${projectId}/bugs`, label: 'Bugs Manager', icon: '🐛' },
      ]
    : [];

  const menuItems = context === 'home' ? homeMenuItems : projectMenuItems;

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Menu Items */}
      <nav className="flex-1 px-4 py-6 space-y-1">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            href={item.path}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
              isActive(item.path)
                ? 'bg-[#17a2b8] text-white'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span className="font-medium">{item.label}</span>
          </Link>
        ))}
      </nav>

      {/* Logout Button */}
      <div className="px-4 py-4 border-t border-gray-200">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-red-50 hover:text-red-600 transition-colors"
        >
          <span className="text-xl">🚪</span>
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </aside>
  );
}