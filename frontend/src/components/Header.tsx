/**
 * Header component with top navigation bar.
 * 
 * Features:
 * - Logo on the left
 * - Application title in center
 * - User menu on the right (username + logout)
 * - Responsive design
 * 
 * Layout:
 * [Logo: Qube.AI] ---------- [QE Co-Pilot] ---------- [User: Admin ▼]
 */

'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { LogOut, User as UserIcon, ChevronDown } from 'lucide-react';
import { useAuthStore } from '@/lib/store';
import { authAPI } from '@/lib/api';

/**
 * Header component for authenticated pages.
 * 
 * Props: None (uses global auth store)
 * 
 * State:
 * - userMenuOpen: Controls visibility of user dropdown menu
 * 
 * User Menu:
 * - Displays current username
 * - Provides logout option
 * - Closes when clicking outside
 */
export default function Header() {
  const router = useRouter();
  const { user, logout: logoutStore } = useAuthStore();
  
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  /**
   * Close user menu when clicking outside.
   * 
   * Attaches event listener on mount, removes on unmount.
   * Checks if click target is outside the menu element.
   */
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setUserMenuOpen(false);
      }
    };

    if (userMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [userMenuOpen]);

  /**
   * Handle user logout.
   * 
   * Flow:
   * 1. Call backend logout endpoint (optional cleanup)
   * 2. Clear auth store and localStorage
   * 3. Redirect to login page
   * 
   * Note: Backend call may fail if token expired, but local logout still proceeds
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
   * Toggle user menu dropdown visibility.
   */
  const toggleUserMenu = () => {
    setUserMenuOpen(!userMenuOpen);
  };

  return (
    <header className="bg-primary-500 shadow-md sticky top-0 z-50">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Left: Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center shadow-sm">
              <span className="text-primary-600 font-bold text-xl">Q</span>
            </div>
            <span className="text-white font-semibold text-lg hidden sm:block">
              Qube.AI
            </span>
          </div>

          {/* Center: Application Title */}
          <div className="absolute left-1/2 transform -translate-x-1/2">
            <h1 className="text-white font-semibold text-xl hidden md:block">
              QE Co-Pilot
            </h1>
          </div>

          {/* Right: User Menu */}
          <div className="relative" ref={menuRef}>
            <button
              onClick={toggleUserMenu}
              className="flex items-center gap-2 bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg transition-all duration-200"
              aria-label="User menu"
              aria-expanded={userMenuOpen}
            >
              <UserIcon className="w-5 h-5" />
              <span className="font-medium hidden sm:block">
                {user?.username || 'User'}
              </span>
              <ChevronDown
                className={`w-4 h-4 transition-transform duration-200 ${
                  userMenuOpen ? 'rotate-180' : ''
                }`}
              />
            </button>

            {/* Dropdown Menu */}
            {userMenuOpen && (
              <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-200 py-2 animate-slide-in">
                {/* User Info */}
                <div className="px-4 py-3 border-b border-gray-200">
                  <p className="text-sm font-medium text-gray-900">
                    {user?.full_name || user?.username}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    @{user?.username}
                  </p>
                </div>

                {/* Logout Option */}
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center gap-3 px-4 py-3 text-left text-gray-700 hover:bg-gray-100 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="text-sm font-medium">Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}