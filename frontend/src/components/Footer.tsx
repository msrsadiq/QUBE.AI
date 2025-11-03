/**
 * Footer component with copyright information.
 * 
 * Features:
 * - Copyright notice with dynamic year
 * - Consistent branding
 * - Sticky bottom positioning
 */

'use client';

/**
 * Footer component for all authenticated pages.
 * 
 * Displays:
 * - Copyright symbol and year
 * - Application name
 * - Rights statement
 * 
 * Styling:
 * - Primary brand color background
 * - White text for contrast
 * - Centered content
 */
export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-primary-500 py-4 mt-auto">
      <div className="container mx-auto px-6">
        <p className="text-center text-white text-sm">
          &copy; {currentYear} Qube.AI. All rights reserved.
        </p>
      </div>
    </footer>
  );
}