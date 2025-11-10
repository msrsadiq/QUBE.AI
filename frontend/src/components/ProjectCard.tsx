/**
 * Project Card Component
 * ----------------------
 * Card displaying project summary information on the home page.
 * 
 * Features:
 * - Displays project ID, name, domain, and creation date
 * - Hover effect with shadow elevation
 * - Kebab menu (⋮) for edit/delete actions
 * - Click-through navigation to project dashboard
 * 
 * Props:
 * - project: Project data (id, name, domain, created_at)
 * - onDelete: Callback when delete is clicked
 * - onClick: Callback when card is clicked
 * 
 * Design:
 * - Teal border (#17A2B8)
 * - Responsive card layout
 * - Kebab menu positioned top-right
 * - Formatted date display
 * 
 * User Interactions:
 * - Click card → Navigate to project dashboard
 * - Click kebab menu → Show edit/delete options
 * - Click edit → Navigate to edit page
 * - Click delete → Show confirmation and delete
 */
'use client';

import { useState, useRef, useEffect } from 'react';

interface Project {
  id: number;
  name: string;
  domain: string;
  created_at: string;
}

interface ProjectCardProps {
  project: Project;
  onDelete: (id: number) => void;
  onEdit: () => void;
  onClick: () => void;
}

export default function ProjectCard({ project, onDelete, onEdit, onClick }: ProjectCardProps) {
  const menuRef = useRef<HTMLDivElement>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    };

    if (menuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [menuOpen]);

  const handleMenuClick = (e: React.MouseEvent, action: 'edit' | 'delete') => {
    e.stopPropagation();
    setMenuOpen(false); // Close menu immediately
    
    if (action === 'delete') {
      onDelete(project.id);
    } else if (action === 'edit') {
      onEdit();
    }
  };

  const toggleMenu = (e: React.MouseEvent) => {
    e.stopPropagation();
    setMenuOpen(!menuOpen);
  };

  return (
    <div
      onClick={onClick}
      className="bg-white border-2 border-primary-500 rounded-lg p-6 cursor-pointer hover:shadow-lg transition-shadow relative"
      role="button"
      tabIndex={0}
      onKeyPress={(e) => e.key === 'Enter' && onClick()}
      aria-label={`Open project ${project.name}`}
    >
      {/* Kebab Menu */}
      <div className="absolute top-4 right-4" ref={menuRef}>
        <button
          onClick={toggleMenu}
          className="text-gray-600 hover:text-gray-800 text-xl p-2 hover:bg-gray-100 rounded"
          aria-label="Project options"
          type="button"
        >
          ⋮
        </button>
        
        {menuOpen && (
          <div className="absolute right-0 mt-1 w-32 bg-white border border-gray-200 rounded shadow-lg z-10">
            <button
              onClick={(e) => handleMenuClick(e, 'edit')}
              className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 transition-colors"
              type="button"
            >
              Edit
            </button>
            <button
              onClick={(e) => handleMenuClick(e, 'delete')}
              className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 text-red-600 transition-colors"
              type="button"
            >
              Delete
            </button>
          </div>
        )}
      </div>

      <div className="mb-2">
        <span className="text-sm text-gray-500">ID: {project.id}</span>
      </div>
      
      <h3 className="text-xl font-bold text-gray-800 mb-2 pr-8">
        {project.name}
      </h3>
      
      <p className="text-gray-600 mb-4">{project.domain}</p>
      
      <div className="text-sm text-gray-500">
        Created: {formatDate(project.created_at)}
      </div>
    </div>
  );
}