'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Menu, X, Search, Bell, User, LogOut } from 'lucide-react';

interface TopBarProps {
  user?: {
    username?: string;
    email?: string;
    display_name?: string;
  };
  onMenuClick?: () => void;
}

export default function TopBar({ user, onMenuClick }: TopBarProps) {
  const router = useRouter();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    // Clear any stored auth tokens
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    // Redirect to login
    router.push('/login');
  };

  const handleProfileClick = () => {
    setIsProfileOpen(!isProfileOpen);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
    if (onMenuClick) {
      onMenuClick();
    }
  };

  return (
    <header className="bg-gradient-to-r from-teal-500 to-teal-600 text-white shadow-lg sticky top-0 z-40">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Left Section - Menu & Logo */}
          <div className="flex items-center">
            {/* Mobile Menu Button */}
            <button
              onClick={toggleMobileMenu}
              className="lg:hidden p-2 rounded-md text-white hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-white"
              aria-label="Toggle menu"
            >
              {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            {/* Logo */}
            <div className="flex items-center space-x-3 ml-4 lg:ml-0">
              <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
                <span className="text-teal-600 font-bold text-lg">Q</span>
              </div>
              <h1 className="text-xl font-bold">Qube.AI</h1>
            </div>
          </div>

          {/* Right Section - Search, Notifications, User */}
          <div className="flex items-center space-x-4">
            {/* Search Button */}
            <button
              className="p-2 rounded-lg hover:bg-teal-600 transition-colors duration-200 hidden sm:block"
              aria-label="Search"
            >
              <Search size={20} />
            </button>

            {/* Notifications */}
            <button
              className="p-2 rounded-lg hover:bg-teal-600 transition-colors duration-200 relative"
              aria-label="Notifications"
            >
              <Bell size={20} />
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
            </button>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={handleProfileClick}
                className="flex items-center space-x-2 p-2 rounded-lg hover:bg-teal-600 transition-colors duration-200"
                aria-label="User menu"
              >
                <div className="w-8 h-8 bg-teal-300 rounded-full flex items-center justify-center">
                  <User size={16} />
                </div>
                <span className="hidden md:block text-sm font-medium">
                  {user?.display_name || user?.username || 'Admin'}
                </span>
              </button>

              {/* User Dropdown */}
              {isProfileOpen && (
                <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                  <div className="p-3 border-b border-gray-200">
                    <p className="text-sm font-medium text-gray-900">
                      {user?.username || 'Admin'}
                    </p>
                    <p className="text-xs text-gray-500">
                      {user?.email || 'admin@qube.ai'}
                    </p>
                  </div>
                  <div className="p-1">
                    <button
                      onClick={() => {
                        setIsProfileOpen(false);
                        router.push('/profile');
                      }}
                      className="w-full flex items-center space-x-2 px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 rounded-md"
                    >
                      <User size={16} />
                      <span>Profile</span>
                    </button>
                    <button
                      onClick={() => {
                        setIsProfileOpen(false);
                        router.push('/settings');
                      }}
                      className="w-full flex items-center space-x-2 px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 rounded-md"
                    >
                      <span>Settings</span>
                    </button>
                    <div className="border-t border-gray-200 mt-1 pt-1">
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center space-x-2 px-3 py-2 text-left text-sm text-red-600 hover:bg-red-50 rounded-md"
                      >
                        <LogOut size={16} />
                        <span>Logout</span>
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}