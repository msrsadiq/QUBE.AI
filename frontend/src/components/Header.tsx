'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { LogOut, ChevronDown } from 'lucide-react';

export default function Header() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [showMenu, setShowMenu] = useState(false);

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <div className="bg-primary text-white py-4 px-6 flex items-center justify-between shadow-md relative">
      <div className="flex-1"></div>
      
      <h1 className="text-2xl font-bold absolute left-1/2 transform -translate-x-1/2">
        QE Co-pilot
      </h1>

      <div className="flex-1 flex justify-end">
        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="flex items-center space-x-2 px-4 py-2 hover:bg-primary-dark rounded-md transition-colors"
          >
            <span className="font-medium">{user?.username || 'User'}</span>
            <ChevronDown className="w-4 h-4" />
          </button>

          {showMenu && (
            <>
              <div
                className="fixed inset-0 z-10"
                onClick={() => setShowMenu(false)}
              ></div>
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-20">
                <button
                  onClick={handleLogout}
                  className="w-full px-4 py-2 text-left hover:bg-gray-50 text-secondary flex items-center space-x-2 rounded-md"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}