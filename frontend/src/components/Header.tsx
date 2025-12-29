/**
 * Header Component
 * ----------------
 * Top navigation bar with title and user menu.
 */

'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';

export default function Header() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setShowMenu(false);
      }
    };

    if (showMenu) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showMenu]);

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <header className="bg-[#17a2b8] text-white h-16 flex items-center justify-between px-6 shadow-md sticky top-0 z-50">
      {/* Left - Brand Name Only (No Logo) */}
      <div className="flex items-center">
        <div className="text-xl font-bold">QUBEAI</div>
      </div>

      {/* Center - Title */}
      <div className="absolute left-1/2 transform -translate-x-1/2">
        <h1 className="text-xl font-semibold">QE Co-Pilot</h1>
      </div>

      {/* Right - User Menu (Show Admin Badge Only if Admin) */}
      <div className="relative" ref={menuRef}>
        <button
          onClick={() => setShowMenu(!showMenu)}
          className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-[#138496] transition-colors"
        >
          <div className="w-8 h-8 bg-white text-[#17a2b8] rounded-full flex items-center justify-center font-bold">
            {user?.username.charAt(0).toUpperCase()}
          </div>
          {/* Show ADMIN badge if user is admin */}
          {user?.is_admin && (
            <span className="px-2 py-0.5 bg-yellow-400 text-yellow-900 text-xs font-bold rounded">
              ADMIN
            </span>
          )}
        </button>

        {/* Dropdown Menu */}
        {showMenu && (
          <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg py-2 text-gray-700">
            <div className="px-4 py-3 border-b border-gray-200">
              <div className="font-semibold text-gray-900">{user?.username}</div>
              {user?.email && (
                <div className="text-sm text-gray-500">{user.email}</div>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors flex items-center gap-2"
            >
              <span className="text-lg">🚪</span>
              <span>Logout</span>
            </button>
          </div>
        )}
      </div>
    </header>
  );
}