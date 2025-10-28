import { create } from 'zustand';

interface User {
  id: number;
  username: string;
  role: string;
}

interface Project {
  id: number;
  name: string;
  domain: string;
  brief: string;
  tech_stack?: string;
  figma_url?: string;
  compliance?: string;
  created_at: string;
  updated_at?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
}

interface ProjectState {
  projects: Project[];
  currentProject: Project | null;
  setProjects: (projects: Project[]) => void;
  setCurrentProject: (project: Project | null) => void;
  addProject: (project: Project) => void;
  updateProject: (id: number, project: Partial<Project>) => void;
  deleteProject: (id: number) => void;
}

// Auth Store
export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: typeof window !== 'undefined' ? localStorage.getItem('token') : null,
  isAuthenticated: typeof window !== 'undefined' ? !!localStorage.getItem('token') : false,
  
  login: (token: string, user: User) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
    set({ token, user, isAuthenticated: true });
  },
  
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
    set({ token: null, user: null, isAuthenticated: false });
  },
}));

// Project Store
export const useProjectStore = create<ProjectState>((set) => ({
  projects: [],
  currentProject: null,
  
  setProjects: (projects: Project[]) => set({ projects }),
  
  setCurrentProject: (project: Project | null) => set({ currentProject: project }),
  
  addProject: (project: Project) =>
    set((state) => ({ projects: [...state.projects, project] })),
  
  updateProject: (id: number, updatedProject: Partial<Project>) =>
    set((state) => ({
      projects: state.projects.map((p) =>
        p.id === id ? { ...p, ...updatedProject } : p
      ),
      currentProject:
        state.currentProject?.id === id
          ? { ...state.currentProject, ...updatedProject }
          : state.currentProject,
    })),
  
  deleteProject: (id: number) =>
    set((state) => ({
      projects: state.projects.filter((p) => p.id !== id),
      currentProject: state.currentProject?.id === id ? null : state.currentProject,
    })),
}));