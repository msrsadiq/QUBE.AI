'use client';

import Link from 'next/link';
import { MoreVertical, Trash2, Edit } from 'lucide-react';
import { useState } from 'react';

interface ProjectCardProps {
  id: number;
  name: string;
  brief: string;
  created_at: string;
  onDelete: () => void;
  onEdit: () => void;
}

export default function ProjectCard({
  id,
  name,
  brief,
  created_at,
  onDelete,
  onEdit,
}: ProjectCardProps) {
  const [showMenu, setShowMenu] = useState(false);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="card relative border-2 border-primary">
      {/* Menu Button */}
      <div className="absolute top-4 right-4">
        <button
          onClick={() => setShowMenu(!showMenu)}
          className="p-2 hover:bg-gray-100 rounded-full transition-colors"
        >
          <MoreVertical className="w-5 h-5 text-secondary" />
        </button>

        {showMenu && (
          <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-10">
            <button
              onClick={() => {
                setShowMenu(false);
                onEdit();
              }}
              className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center space-x-2"
            >
              <Edit className="w-4 h-4" />
              <span>Edit</span>
            </button>
            <button
              onClick={() => {
                setShowMenu(false);
                onDelete();
              }}
              className="w-full px-4 py-2 text-left hover:bg-red-50 text-red-600 flex items-center space-x-2"
            >
              <Trash2 className="w-4 h-4" />
              <span>Delete</span>
            </button>
          </div>
        )}
      </div>

      {/* Card Content */}
      <Link href={`/projects/${id}`}>
        <div className="cursor-pointer">
          <h3 className="text-xl font-bold text-secondary mb-2 pr-8">{name}</h3>
          <p className="text-secondary-light text-sm mb-4 line-clamp-2">
            {brief}
          </p>
          <p className="text-xs text-gray-500">
            Created: {formatDate(created_at)}
          </p>
        </div>
      </Link>
    </div>
  );
}