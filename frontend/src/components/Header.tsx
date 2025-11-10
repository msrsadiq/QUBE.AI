/**
 * Header Component
 * ----------------
 * Top navigation bar displayed across all pages.
 * 
 * Features:
 * - Hamburger menu button (left) - Opens sidebar navigation
 * - Logo and title (center) - Qube.AI branding
 * - User profile button (right) - Shows user menu dropdown
 * 
 * Props:
 * - onMenuClick: Callback to open/close sidebar
 * - title: Optional custom title (default: "Qube.AI")
 * 
 * User Menu (Future Enhancement):
 * - User profile information
 * - Settings link
 * - Logout option
 * 
 * Design:
 * - Uses Tarento color palette (#17A2B8)
 * - Sticky positioning (stays at top on scroll)
 * - Responsive design for mobile/desktop
 */

'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuthStore } from '@/lib/store';

interface HeaderProps {
  onMenuClick: () => void;
  title?: string;
}

export default function Header({ onMenuClick, title = 'Qube.AI' }: HeaderProps) {
  const { user } = useAuthStore();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setShowUserMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className="bg-primary-500 shadow-md sticky top-0 z-30">
      <div className="flex items-center justify-between px-6 py-4">
        {/* LEFT: Hamburger Menu */}
        <button
          onClick={onMenuClick}
          className="text-white hover:bg-primary-600 p-2 rounded-lg transition-colors"
          aria-label="Toggle menu"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>

        {/* CENTER: Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
            <span className="text-primary-500 font-bold text-xl">Q</span>
          </div>
          <h1 className="text-white text-2xl font-bold tracking-wide">
            {title}
          </h1>
        </div>

        {/* RIGHT: User Menu */}
        <div className="relative" ref={menuRef}>
          <button
            onClick={() => setShowUserMenu(!showUserMenu)}
            className="flex items-center gap-2 text-white hover:bg-primary-600 p-2 rounded-lg transition-colors"
            aria-label="User menu"
          >
            <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
              <span className="text-primary-500 font-semibold text-sm">
                {user?.username?.charAt(0).toUpperCase() || 'A'}
              </span>
            </div>
          </button>

          {/* User Dropdown Menu */}
          {showUserMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2">
              <div className="px-4 py-2 border-b border-gray-200">
                <p className="text-sm font-semibold text-gray-800">
                  {user?.username || 'Admin'}
                </p>
                <p className="text-xs text-gray-500">Administrator</p>
              </div>
              
              {/* Logout Button */}
              <button
                onClick={() => {
                  const { logout } = useAuthStore.getState();
                  logout();
                  window.location.href = '/';
                }}
                className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}