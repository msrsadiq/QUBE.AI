'use client';

import { useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import {
  Home,
  FileText,
  TestTube2,
  Bug,
  List,
  Settings,
  ChevronLeft,
  ChevronRight,
  FileCode,
  Bot,
  Zap
} from 'lucide-react';

interface SidebarProps {
  projectId?: string;
  isCollapsed?: boolean;
  onToggle?: () => void;
}

interface MenuItem {
  id: string;
  name: string;
  icon: any;
  path: string;
  disabled?: boolean;
  badge?: string;
}

export default function Sidebar({ projectId, isCollapsed = false, onToggle }: SidebarProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(!isCollapsed);

  const menuItems: MenuItem[] = [
    {
      id: 'home',
      name: 'Home',
      icon: Home,
      path: projectId ? `/projects/${projectId}` : '/home'
    },
    {
      id: 'requirement-analysis',
      name: 'Requirement Analyzer',
      icon: FileText,
      path: projectId ? `/projects/${projectId}/agents/requirement-analysis` : '#'
    },
    {
      id: 'testcase-generator',
      name: 'Testcase Generator',
      icon: TestTube2,
      path: projectId ? `/projects/${projectId}/agents/testcase-generator` : '#',
      disabled: true,
      badge: 'Soon'
    },
    {
      id: 'test-list',
      name: 'Test Case List',
      icon: List,
      path: projectId ? `/projects/${projectId}/agents/test-list` : '#',
      disabled: true,
      badge: 'Soon'
    },
    {
      id: 'bugs-manager',
      name: 'Bugs Manager',
      icon: Bug,
      path: projectId ? `/projects/${projectId}/agents/bugs-manager` : '#',
      disabled: true,
      badge: 'Soon'
    },
    {
      id: 'api-agent',
      name: 'API Agent',
      icon: FileCode,
      path: projectId ? `/projects/${projectId}/agents/api` : '#',
      disabled: true,
      badge: 'Soon'
    },
    {
      id: 'automation',
      name: 'Automation',
      icon: Bot,
      path: projectId ? `/projects/${projectId}/agents/automation` : '#',
      disabled: true,
      badge: 'Soon'
    },
  ];

  const handleToggleSidebar = () => {
    setIsOpen(!isOpen);
    if (onToggle) {
      onToggle();
    }
  };

  const handleNavigation = (item: MenuItem) => {
    if (!item.disabled && item.path !== '#') {
      router.push(item.path);
    }
  };

  const isActive = (path: string) => {
    return pathname === path;
  };

  return (
    <aside className={`${
      isOpen ? 'w-64' : 'w-20'
    } bg-white border-r border-gray-200 transition-all duration-300 ease-in-out flex flex-col h-full`}>
      
      {/* Sidebar Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className={`font-semibold text-gray-800 transition-opacity ${
            isOpen ? 'opacity-100' : 'opacity-0'
          }`}>
            MODULES
          </h2>
          <button
            onClick={handleToggleSidebar}
            className="p-1.5 rounded-lg hover:bg-gray-100 text-gray-600"
          >
            {isOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
          </button>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 p-4 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);
          
          return (
            <button
              key={item.id}
              onClick={() => handleNavigation(item)}
              disabled={item.disabled}
              className={`
                w-full flex items-center px-3 py-2.5 rounded-lg transition-all duration-200
                ${active 
                  ? 'bg-teal-50 text-teal-600 font-medium' 
                  : item.disabled
                  ? 'text-gray-400 cursor-not-allowed opacity-60'
                  : 'text-gray-700 hover:bg-gray-100'
                }
              `}
              title={!isOpen ? item.name : ''}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {isOpen && (
                <>
                  <span className="ml-3 flex-1 text-left text-sm">
                    {item.name}
                  </span>
                  {item.badge && (
                    <span className="ml-2 px-2 py-0.5 text-xs bg-gray-200 text-gray-600 rounded-full font-medium">
                      {item.badge}
                    </span>
                  )}
                </>
              )}
            </button>
          );
        })}
      </nav>

      {/* Settings Section */}
      <div className="p-4 border-t border-gray-200">
        <button
          onClick={() => router.push(projectId ? `/projects/${projectId}/settings` : '/settings')}
          className={`
            w-full flex items-center px-3 py-2.5 rounded-lg transition-all duration-200
            text-gray-700 hover:bg-gray-100
            ${isActive(`/projects/${projectId}/settings`) ? 'bg-teal-50 text-teal-600' : ''}
          `}
          title={!isOpen ? 'Settings' : ''}
        >
          <Settings className="w-5 h-5 flex-shrink-0" />
          {isOpen && (
            <span className="ml-3 flex-1 text-left text-sm">
              Settings
            </span>
          )}
        </button>
      </div>

      {/* Footer */}
      {isOpen && (
        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center space-x-2">
            <Zap className="w-4 h-4 text-teal-600" />
            <span className="text-xs text-gray-600">Powered by Qube.AI</span>
          </div>
        </div>
      )}
    </aside>
  );
}