/**
 * Root layout component for the entire application.
 * 
 * Responsibilities:
 * - Define HTML structure and metadata
 * - Load global styles
 * - Provide consistent layout wrapper
 * - Configure fonts and viewport
 * 
 * Note: This layout wraps ALL pages in the application
 */

import type { Metadata } from 'next';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: "Qube.AI - Agentic AI for Quality Engineers",
  description: "Multi-agent testing automation platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        {/* No header/footer here - pages handle their own */}
        {children}
      </body>
    </html>
  );
}