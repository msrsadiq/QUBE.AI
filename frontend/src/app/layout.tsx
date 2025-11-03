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
import { Inter } from 'next/font/google';
import '@/styles/globals.css';

/**
 * Configure Inter font with Latin subset.
 * Optimized font loading via Next.js font optimization.
 */
const inter = Inter({ subsets: ['latin'] });

/**
 * Application metadata for SEO and browser tabs.
 * 
 * Includes:
 * - Page title with template
 * - Meta description
 * - Viewport configuration
 */
export const metadata: Metadata = {
  title: {
    default: 'Qube.AI - Agentic AI for Quality Engineers',
    template: '%s | Qube.AI',
  },
  description: 'An Agentic AI platform for autonomous testing and quality engineering',
  viewport: 'width=device-width, initial-scale=1',
};

/**
 * Root layout component.
 * 
 * @param children - Page content to be rendered
 * @returns HTML document structure with global layout
 * 
 * Structure:
 * - html: Root element with language attribute
 * - body: Content wrapper with font family
 * - children: Dynamic page content
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}