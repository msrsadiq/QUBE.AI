/**
 * Collapsible sidebar navigation component.
 * 
 * Features:
 * - Context-aware menu items (Home vs Project pages)
 * - Collapsible behavior with toggle button
 * - Active route highlighting
 * - Icon-based navigation
 * - Responsive design
 * 
 * Menu Contexts:
 * 1. Home Context: Users, Prompt Ops, Logout
 * 2. Project Context: Home, LLM, Requirement Analyzer, Test Case Generator, Page Object Generator
 */

'use client';

import { usePathname, useRouter } from 'next/navigation';
import {
  Home,
  Settings,
  Users,
  FileCode,
  LogOut,
  Menu,
  ChevronLeft,
  Sparkles,
  FileText,
  TestTube,
  Code2,
} from 'lucide-react';
import { useUIStore, useAuthStore } from '@/lib/store';
import { authAPI } from '@/lib/api';

/**
 * Navigation menu item interface.
 */
interface NavItem {
  label: string;
  icon: React.ReactNode;
  path?: string;
  onClick?: () => void;
  comingSoon?: boolean;
}

/**
 * Sidebar navigation component.
 * 
 * @param context - Menu context: 'home' | 'project'
 * 
 * Behavior:
 * - Displays different menu items based on context
 * - Highlights active route
 * - Collapses to icon-only mode
 * - Handles logout action
 */
export default function Sidebar({ context = 'home' }: { context?: 'home' | 'project' }) {
  const pathname = usePathname();
  const router = useRouter();
  const { sidebarCollapsed, toggleSidebar } = useUIStore();
  const { logout: logoutStore } = useAuthStore();

  /**
   * Handle user logout from sidebar.
   * 
   * Same flow as Header logout for consistency.
   */
  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      logoutStore();
      router.push('/');
    }
  };

  /**
   * Home context menu items.
   * 
   * Available on: /home page
   * Items: Home, Users (future), Prompt Ops (future), Logout
   */
  const homeMenuItems: NavItem[] = [
    {
      label: 'Home',
      icon: <Home className="w-5 h-5" />,
      path: '/home',
    },
    {
      label: 'Users',
      icon: <Users className="w-5 h-5" />,
      path: '/users',
      comingSoon: true,
    },
    {
      label: 'Prompt Ops',
      icon: <FileCode className="w-5 h-5" />,
      path: '/prompt-ops',
      comingSoon: true,
    },
    {
      label: 'Logout',
      icon: <LogOut className="w-5 h-5" />,
      onClick: handleLogout,
    },
  ];

  /**
   * Project context menu items.
   * 
   * Available on: /projects/[id]/* pages
   * Items: Home, LLM Config, Requirement Analyzer, Test Case Generator, Page Object Generator
   */
  const projectMenuItems: NavItem[] = [
    {
      label: 'Home',
      icon: <Home className="w-5 h-5" />,
      path: '/home',
    },
    {
      label: 'LLM',
      icon: <Sparkles className="w-5 h-5" />,
      path: '/projects/[id]/llm',
      comingSoon: true,
    },
    {
      label: 'Requirement Analyzer',
      icon: <FileText className="w-5 h-5" />,
      path: '/projects/[id]/requirements',
      comingSoon: true,
    },
    {
      label: 'Test Case Generator',
      icon: <TestTube className="w-5 h-5" />,
      path: '/projects/[id]/testcases',
      comingSoon: true,
    },
    {
      label: 'Page Object Generator',
      icon: <Code2 className="w-5 h-5" />,
      path: '/projects/[id]/page-objects',
      comingSoon: true,
    },
  ];

  // Select menu items based on context
  const menuItems = context === 'home' ? homeMenuItems : projectMenuItems;

  /**
   * Navigate to a menu item path.
   * 
   * @param path - Target route path
   */
  const handleNavigation = (path: string) => {
    router.push(path);
  };

  /**
   * Check if a menu item is currently active.
   * 
   * @param path - Menu item path
   * @returns Boolean indicating if path matches current route
   */
  const isActive = (path?: string) => {
    if (!path) return false;
    return pathname === path;
  };

  return (
    <aside
      className={`bg-sidebar border-r border-gray-200 flex flex-col transition-all duration-300 ${
        sidebarCollapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* Sidebar Header with Toggle */}
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        {!sidebarCollapsed && (
          <h2 className="font-semibold text-gray-700">MODULES</h2>
        )}
        <button
          onClick={toggleSidebar}
          className="p-2 hover:bg-sidebar-hover rounded-lg transition-colors"
          aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {sidebarCollapsed ? (
            <Menu className="w-5 h-5 text-gray-600" />
          ) : (
            <ChevronLeft className="w-5 h-5 text-gray-600" />
          )}
        </button>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 overflow-y-auto py-4 px-3">
        <ul className="space-y-2">
          {menuItems.map((item, index) => (
            <li key={index}>
              <button
                onClick={() => {
                  if (item.onClick) {
                    item.onClick();
                  } else if (item.path && !item.comingSoon) {
                    handleNavigation(item.path);
                  }
                }}
                disabled={item.comingSoon}
                className={`sidebar-link w-full ${
                  isActive(item.path) ? 'active' : ''
                } ${
                  item.comingSoon
                    ? 'opacity-50 cursor-not-allowed'
                    : 'cursor-pointer'
                }`}
                title={sidebarCollapsed ? item.label : undefined}
              >
                {item.icon}
                {!sidebarCollapsed && (
                  <span className="flex-1 text-left">
                    {item.label}
                    {item.comingSoon && (
                      <span className="ml-2 text-xs text-gray-500">(Soon)</span>
                    )}
                  </span>
                )}
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}