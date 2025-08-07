// API service for communicating with the backend
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  technologies: string[];
  github_url?: string;
  live_url?: string;
  featured: boolean;
  created_at: string;
}

export interface Experience {
  id: number;
  title: string;
  company: string;
  location: string;
  period: string;
  start_date: string;
  end_date?: string;
  description: string;
  technologies: string[];
  achievements: string[];
  created_at: string;
}

export interface ApiResponse<T> {
  data: T;
  error?: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('API request failed:', error);
      return {
        data: null as T,
        error:
          error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  // Projects API
  async getProjects(
    featuredOnly: boolean = false
  ): Promise<ApiResponse<Project[]>> {
    const params = featuredOnly ? '?featured_only=true' : '';
    return this.request<Project[]>(`/projects/${params}`);
  }

  async getProject(id: number): Promise<ApiResponse<Project>> {
    return this.request<Project>(`/projects/${id}`);
  }

  // Experience API
  async getExperience(): Promise<ApiResponse<Experience[]>> {
    return this.request<Experience[]>('/experience/');
  }

  async getExperienceEntry(id: number): Promise<ApiResponse<Experience>> {
    return this.request<Experience>(`/experience/${id}`);
  }
}

// Create and export a singleton instance
export const apiService = new ApiService();

// Export types for use in components
export type { Project, Experience, ApiResponse };
