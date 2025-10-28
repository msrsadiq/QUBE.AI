'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Settings, ChevronLeft, ChevronRight } from 'lucide-react';

export default function Sidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const menuItems = [
    { name: 'Home', href: '/home', icon: Home },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  return (
    <div
      className={`bg-white border-r border-gray-200 min-h-screen transition-all duration-300 ${
        isCollapsed ? 'w-16' : 'w-64'
      }`}
    >
      {/* Toggle Button */}
      <div className="p-4 flex justify-end">
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-2 hover:bg-gray-100 rounded-md transition-colors"
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? (
            <ChevronRight className="w-5 h-5 text-secondary" />
          ) : (
            <ChevronLeft className="w-5 h-5 text-secondary" />
          )}
        </button>
      </div>

      {/* Menu Items */}
      <div className="px-4">
        {!isCollapsed && (
          <h2 className="text-secondary font-semibold mb-4">MODULES</h2>
        )}
        <nav className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center px-4 py-3 rounded-md transition-colors ${
                  isActive
                    ? 'bg-gray-100 text-primary'
                    : 'text-secondary-light hover:bg-gray-50'
                }`}
                title={isCollapsed ? item.name : ''}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {!isCollapsed && <span className="ml-3">{item.name}</span>}
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
}