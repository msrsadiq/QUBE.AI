/**
 * Layout for authenticated pages (home and beyond).
 * 
 * Structure:
 * - Header (top bar)
 * - Sidebar (left navigation)
 * - Main content area
 * - Footer (copyright)
 * 
 * Protection:
 * - Redirects unauthenticated users to login
 * - Provides consistent layout for all authenticated pages
 */

'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import Footer from '@/components/Footer';
import { useAuthStore } from '@/lib/store';

/**
 * Authenticated layout component.
 * 
 * @param children - Page content to render
 * 
 * Features:
 * - Auth guard: Redirects if not authenticated
 * - Context-aware sidebar (home vs project)
 * - Responsive layout with flexbox
 */
export default function HomeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  /**
   * Authentication guard.
   * 
   * Checks if user is authenticated on mount.
   * Redirects to login page if not authenticated.
   */
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, router]);

  // Don't render layout until auth check is complete
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  /**
   * Determine sidebar context based on current path.
   * 
   * - /home: Home context (users, prompt ops)
   * - /projects/*: Project context (LLM, requirements, etc.)
   */
  const sidebarContext = pathname.startsWith('/projects') ? 'project' : 'home';

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Navigation Bar */}
      <Header />

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <Sidebar context={sidebarContext} />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto bg-background-secondary">
          <div className="container mx-auto px-6 py-8">
            {children}
          </div>
        </main>
      </div>

      {/* Footer */}
      <Footer />
    </div>
  );
}