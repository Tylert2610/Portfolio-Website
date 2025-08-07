export interface AdminPanelProps {
  className?: string;
}

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

export interface ProjectFormData {
  title: string;
  description: string;
  image: string;
  technologies: string[];
  github_url: string;
  live_url: string;
  featured: boolean;
}

export interface ExperienceFormData {
  title: string;
  company: string;
  location: string;
  period: string;
  start_date: string;
  end_date: string;
  description: string;
  technologies: string[];
  achievements: string[];
}

export interface BlogPostFormData {
  title: string;
  slug: string;
  content: string;
  excerpt: string;
  read_time: string;
  category_id: number | undefined;
  published_at: string | undefined;
}

export interface BlogPost {
  id: number;
  title: string;
  slug: string;
  content: string;
  excerpt?: string;
  read_time?: string;
  published_at?: string;
  created_at: string;
  updated_at?: string;
  category_id?: number;
  category?: {
    id: number;
    name: string;
    slug: string;
  };
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
}

export interface CategoryFormData {
  name: string;
  slug: string;
  description: string;
}

export type AdminTab = 'projects' | 'experience' | 'blog' | 'categories';
