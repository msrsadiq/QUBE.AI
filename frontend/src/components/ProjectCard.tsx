/**
 * Project Card Component
 * ----------------------
 * Compact project card with essential information.
 */

'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface ProjectCardProps {
  project: {
    id: number;
    project_code: string;
    name: string;
    domain: string;
    brief: string;
    created_at: string;
  };
  onDelete: () => void;
  onEdit: () => void;
}

export default function ProjectCard({ project, onDelete, onEdit }: ProjectCardProps) {
  const router = useRouter();
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

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const handleCardClick = () => {
    router.push(`/projects/${project.id}`);
  };

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowMenu(false);
    onEdit();
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowMenu(false);
    onDelete();
  };

  return (
    <div
      onClick={handleCardClick}
      className="bg-white rounded-lg border-2 border-[#17a2b8] hover:shadow-lg transition-shadow cursor-pointer p-4 relative h-32"
    >
      {/* Kebab Menu */}
      <div className="absolute top-2 right-2" ref={menuRef}>
        <button
          onClick={(e) => {
            e.stopPropagation();
            setShowMenu(!showMenu);
          }}
          className="text-gray-400 hover:text-gray-600 p-1"
        >
          <span className="text-xl">⋮</span>
        </button>

        {showMenu && (
          <div className="absolute right-0 mt-2 w-32 bg-white rounded-lg shadow-lg py-1 z-10 border border-gray-200">
            <button
              onClick={handleEdit}
              className="w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-gray-700"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-red-600"
            >
              Delete
            </button>
          </div>
        )}
      </div>

      {/* Project Info - Compact Layout */}
      <div className="flex flex-col h-full justify-between pr-8">
        <div>
          <h3 className="text-lg font-bold text-gray-900 mb-1 truncate">
            {project.name}
          </h3>
          
          <span className="inline-block px-2 py-0.5 bg-[#17a2b8] text-white text-xs rounded-full">
            {project.domain}
          </span>
        </div>

        {/* Footer with Code */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span className="font-mono font-semibold text-[#17a2b8]">
            #{project.project_code}
          </span>
          <span>{formatDate(project.created_at)}</span>
        </div>
      </div>
    </div>
  );
}