/**
 * Root Layout
 * -----------
 * Main application layout with providers and global styles.
 */

'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import '../styles/globals.css'; // FIXED: Changed from './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const initializeAuth = useAuthStore((state) => state.initializeAuth);

  /**
   * Initialize authentication state from localStorage on mount
   */
  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  return (
    <html lang="en">
      <head>
        <title>Qube.AI - QE Co-Pilot</title>
        <meta name="description" content="Agentic AI Platform for Quality Engineering" />
      </head>
      <body className="min-h-screen bg-gray-50">
        {children}
      </body>
    </html>
  );
}