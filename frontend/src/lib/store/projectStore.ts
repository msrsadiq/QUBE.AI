import { create } from 'zustand';

interface Project {
  id: number;
  name: string;
  domain: string;
  brief: string;
  tech_stack?: string;
  figma_url?: string;
  compliances?: string;
  created_at: string;
  updated_at: string;
}

interface LLMConfig {
  id: number;
  config_name: string;
  provider: string;
  model_name: string;
  is_validated: boolean;
  is_default: boolean;
  validation_status: string;
}

interface ProjectStore {
  projects: Project[];
  currentProject: Project | null;
  llmConfigs: LLMConfig[];
  currentLLMConfig: LLMConfig | null;

  setProjects: (projects: Project[]) => void;
  setCurrentProject: (project: Project) => void;
  addProject: (project: Project) => void;
  updateProject: (project: Project) => void;
  deleteProject: (projectId: number) => void;

  setLLMConfigs: (configs: LLMConfig[]) => void;
  setCurrentLLMConfig: (config: LLMConfig) => void;
  addLLMConfig: (config: LLMConfig) => void;
  updateLLMConfig: (config: LLMConfig) => void;
  deleteLLMConfig: (configId: number) => void;
}

export const useProjectStore = create<ProjectStore>((set) => ({
  projects: [],
  currentProject: null,
  llmConfigs: [],
  currentLLMConfig: null,

  setProjects: (projects) => set({ projects }),
  setCurrentProject: (project) => set({ currentProject: project }),
  addProject: (project) =>
    set((state) => ({ projects: [...state.projects, project] })),
  updateProject: (project) =>
    set((state) => ({
      projects: state.projects.map((p) => (p.id === project.id ? project : p)),
      currentProject:
        state.currentProject?.id === project.id ? project : state.currentProject,
    })),
  deleteProject: (projectId) =>
    set((state) => ({
      projects: state.projects.filter((p) => p.id !== projectId),
      currentProject:
        state.currentProject?.id === projectId ? null : state.currentProject,
    })),

  setLLMConfigs: (configs) => set({ llmConfigs: configs }),
  setCurrentLLMConfig: (config) => set({ currentLLMConfig: config }),
  addLLMConfig: (config) =>
    set((state) => ({ llmConfigs: [...state.llmConfigs, config] })),
  updateLLMConfig: (config) =>
    set((state) => ({
      llmConfigs: state.llmConfigs.map((c) =>
        c.id === config.id ? config : c
      ),
      currentLLMConfig:
        state.currentLLMConfig?.id === config.id ? config : state.currentLLMConfig,
    })),
  deleteLLMConfig: (configId) =>
    set((state) => ({
      llmConfigs: state.llmConfigs.filter((c) => c.id !== configId),
      currentLLMConfig:
        state.currentLLMConfig?.id === configId ? null : state.currentLLMConfig,
    })),
}));