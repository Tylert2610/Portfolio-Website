import React, { useState, useEffect } from 'react';
import { Button } from '../common';
import { apiService } from '../../services/api';
import { LoginForm } from './LoginForm';
import { ProjectForm } from './ProjectForm';
import { ExperienceForm } from './ExperienceForm';
import { BlogPostForm } from './BlogPostForm';
import type {
  AdminPanelProps,
  AdminTab,
  Project,
  Experience,
  BlogPost,
  ProjectFormData,
  ExperienceFormData,
  BlogPostFormData,
} from './types';

export const AdminPanel: React.FC<AdminPanelProps> = ({ className = '' }) => {
  const [activeTab, setActiveTab] = useState<AdminTab>('projects');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Projects state
  const [projects, setProjects] = useState<Project[]>([]);
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [projectForm, setProjectForm] = useState<ProjectFormData>({
    title: '',
    description: '',
    image: '',
    technologies: [],
    github_url: '',
    live_url: '',
    featured: false,
  });

  // Experience state
  const [experience, setExperience] = useState<Experience[]>([]);
  const [showExperienceForm, setShowExperienceForm] = useState(false);
  const [editingExperience, setEditingExperience] = useState<Experience | null>(
    null
  );
  const [experienceForm, setExperienceForm] = useState<ExperienceFormData>({
    title: '',
    company: '',
    location: '',
    period: '',
    start_date: '',
    end_date: '',
    description: '',
    technologies: [],
    achievements: [],
  });

  // Blog posts state
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([]);
  const [showBlogPostForm, setShowBlogPostForm] = useState(false);
  const [editingPost, setEditingPost] = useState<BlogPost | null>(null);
  const [blogPostForm, setBlogPostForm] = useState<BlogPostFormData>({
    title: '',
    slug: '',
    content: '',
    excerpt: '',
    read_time: '',
    category_id: undefined,
    published_at: undefined,
  });

  // Check for existing authentication on mount
  useEffect(() => {
    if (apiService.isAuthenticated()) {
      setIsAuthenticated(true);
    }
  }, []);

  // Load data
  useEffect(() => {
    if (isAuthenticated) {
      loadProjects();
      loadExperience();
      loadBlogPosts();
    }
  }, [isAuthenticated]);

  const loadProjects = async () => {
    setLoading(true);
    const response = await apiService.getProjects();
    if (response.error) {
      setError(`Failed to load projects: ${response.error}`);
    } else {
      setProjects(response.data || []);
    }
    setLoading(false);
  };

  const loadExperience = async () => {
    setLoading(true);
    const response = await apiService.getExperience();
    if (response.error) {
      setError(`Failed to load experience: ${response.error}`);
    } else {
      setExperience(response.data || []);
    }
    setLoading(false);
  };

  const loadBlogPosts = async () => {
    setLoading(true);
    const response = await apiService.getBlogPosts();
    if (response.error) {
      setError(`Failed to load blog posts: ${response.error}`);
    } else {
      setBlogPosts(response.data || []);
    }
    setLoading(false);
  };

  const handleLogin = async (username: string, password: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.login({ username, password });
      if (response.error) {
        setError(response.error);
      } else {
        setIsAuthenticated(true);
      }
    } catch {
      setError('Login failed');
    } finally {
      setLoading(false);
    }
  };

  // Project CRUD operations
  const handleProjectSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (editingProject) {
        // Update project
        const response = await apiService.updateProject(
          editingProject.id,
          projectForm
        );
        if (response.error) {
          setError(`Failed to update project: ${response.error}`);
        } else {
          await loadProjects();
          setShowProjectForm(false);
          setEditingProject(null);
          resetProjectForm();
        }
      } else {
        // Create project
        const response = await apiService.createProject(projectForm);
        if (response.error) {
          setError(`Failed to create project: ${response.error}`);
        } else {
          await loadProjects();
          setShowProjectForm(false);
          resetProjectForm();
        }
      }
    } catch {
      setError('Operation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleProjectEdit = (project: Project) => {
    setEditingProject(project);
    setProjectForm({
      title: project.title,
      description: project.description,
      image: project.image || '',
      technologies: project.technologies,
      github_url: project.github_url || '',
      live_url: project.live_url || '',
      featured: project.featured,
    });
    setShowProjectForm(true);
  };

  const handleProjectDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this project?')) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiService.deleteProject(id);
      if (response.error) {
        setError(`Failed to delete project: ${response.error}`);
      } else {
        await loadProjects();
      }
    } catch {
      setError('Delete failed');
    } finally {
      setLoading(false);
    }
  };

  const resetProjectForm = () => {
    setProjectForm({
      title: '',
      description: '',
      image: '',
      technologies: [],
      github_url: '',
      live_url: '',
      featured: false,
    });
  };

  // Experience CRUD operations
  const handleExperienceSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (editingExperience) {
        // Update experience
        const response = await apiService.updateExperience(
          editingExperience.id,
          experienceForm
        );
        if (response.error) {
          setError(`Failed to update experience: ${response.error}`);
        } else {
          await loadExperience();
          setShowExperienceForm(false);
          setEditingExperience(null);
          resetExperienceForm();
        }
      } else {
        // Create experience
        const response = await apiService.createExperience(experienceForm);
        if (response.error) {
          setError(`Failed to create experience: ${response.error}`);
        } else {
          await loadExperience();
          setShowExperienceForm(false);
          resetExperienceForm();
        }
      }
    } catch {
      setError('Operation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleExperienceEdit = (exp: Experience) => {
    setEditingExperience(exp);
    setExperienceForm({
      title: exp.title,
      company: exp.company,
      location: exp.location,
      period: exp.period,
      start_date: exp.start_date,
      end_date: exp.end_date || '',
      description: exp.description,
      technologies: exp.technologies,
      achievements: exp.achievements,
    });
    setShowExperienceForm(true);
  };

  const handleExperienceDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this experience entry?'))
      return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiService.deleteExperience(id);
      if (response.error) {
        setError(`Failed to delete experience: ${response.error}`);
      } else {
        await loadExperience();
      }
    } catch {
      setError('Delete failed');
    } finally {
      setLoading(false);
    }
  };

  const resetExperienceForm = () => {
    setExperienceForm({
      title: '',
      company: '',
      location: '',
      period: '',
      start_date: '',
      end_date: '',
      description: '',
      technologies: [],
      achievements: [],
    });
  };

  // Blog Post CRUD operations
  const handleBlogPostSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (editingPost) {
        // Update blog post
        const response = await apiService.updateBlogPost(
          editingPost.id,
          blogPostForm
        );
        if (response.error) {
          setError(`Failed to update blog post: ${response.error}`);
        } else {
          await loadBlogPosts();
          setShowBlogPostForm(false);
          setEditingPost(null);
          resetBlogPostForm();
        }
      } else {
        // Create blog post
        const response = await apiService.createBlogPost(blogPostForm);
        if (response.error) {
          setError(`Failed to create blog post: ${response.error}`);
        } else {
          await loadBlogPosts();
          setShowBlogPostForm(false);
          resetBlogPostForm();
        }
      }
    } catch {
      setError('Operation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleBlogPostEdit = (post: BlogPost) => {
    setEditingPost(post);
    setBlogPostForm({
      title: post.title,
      slug: post.slug,
      content: post.content,
      excerpt: post.excerpt || '',
      read_time: post.read_time || '',
      category_id: post.category_id || undefined,
      published_at: post.published_at || undefined,
    });
    setShowBlogPostForm(true);
  };

  const handleBlogPostDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this blog post?')) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiService.deleteBlogPost(id);
      if (response.error) {
        setError(`Failed to delete blog post: ${response.error}`);
      } else {
        await loadBlogPosts();
      }
    } catch {
      setError('Delete failed');
    } finally {
      setLoading(false);
    }
  };

  const handleBlogPostPublish = async (id: number) => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.publishBlogPost(id);
      if (response.error) {
        setError(`Failed to publish blog post: ${response.error}`);
      } else {
        await loadBlogPosts();
      }
    } catch {
      setError('Publish failed');
    } finally {
      setLoading(false);
    }
  };

  const resetBlogPostForm = () => {
    setBlogPostForm({
      title: '',
      slug: '',
      content: '',
      excerpt: '',
      read_time: '',
      category_id: undefined,
      published_at: undefined,
    });
  };

  if (!isAuthenticated) {
    return (
      <LoginForm
        onLogin={handleLogin}
        loading={loading}
        error={error}
        className={className}
      />
    );
  }

  return (
    <div
      className={`min-h-screen bg-gray-50 dark:bg-gray-900 py-12 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md">
          {/* Header */}
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Admin Panel
              </h1>
              <Button
                variant="outline"
                onClick={() => {
                  apiService.logout();
                  setIsAuthenticated(false);
                }}
                size="sm"
              >
                Logout
              </Button>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <nav className="flex space-x-8">
              <button
                onClick={() => setActiveTab('projects')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'projects'
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
              >
                Projects
              </button>
              <button
                onClick={() => setActiveTab('experience')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'experience'
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
              >
                Experience
              </button>
              <button
                onClick={() => setActiveTab('blog')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'blog'
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
              >
                Blog Posts
              </button>
            </nav>
          </div>

          {/* Error Display */}
          {error && (
            <div className="px-6 py-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300">
              {error}
              <button
                onClick={() => setError(null)}
                className="float-right text-red-500 hover:text-red-700"
              >
                ×
              </button>
            </div>
          )}

          {/* Content */}
          <div className="p-6">
            {activeTab === 'projects' && (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Manage Projects
                  </h2>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => {
                      setShowProjectForm(true);
                      setEditingProject(null);
                      resetProjectForm();
                    }}
                    disabled={loading}
                  >
                    Add New Project
                  </Button>
                </div>

                {showProjectForm && (
                  <ProjectForm
                    form={projectForm}
                    setForm={setProjectForm}
                    onSubmit={handleProjectSubmit}
                    onCancel={() => {
                      setShowProjectForm(false);
                      setEditingProject(null);
                      resetProjectForm();
                    }}
                    editingProject={editingProject}
                    loading={loading}
                  />
                )}

                {/* Projects List */}
                <div className="space-y-4">
                  {projects.map(project => (
                    <div
                      key={project.id}
                      className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                            {project.title}
                            {project.featured && (
                              <span className="ml-2 px-2 py-1 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 text-xs rounded-full">
                                Featured
                              </span>
                            )}
                          </h3>
                          <p className="text-gray-600 dark:text-gray-300 mt-1">
                            {project.description}
                          </p>
                          <div className="flex flex-wrap gap-1 mt-2">
                            {project.technologies.map((tech, index) => (
                              <span
                                key={index}
                                className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-xs"
                              >
                                {tech}
                              </span>
                            ))}
                          </div>
                        </div>
                        <div className="flex gap-2 ml-4">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleProjectEdit(project)}
                            disabled={loading}
                          >
                            Edit
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleProjectDelete(project.id)}
                            disabled={loading}
                            className="text-red-600 hover:text-red-700"
                          >
                            Delete
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'experience' && (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Manage Experience
                  </h2>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => {
                      setShowExperienceForm(true);
                      setEditingExperience(null);
                      resetExperienceForm();
                    }}
                    disabled={loading}
                  >
                    Add New Experience
                  </Button>
                </div>

                {showExperienceForm && (
                  <ExperienceForm
                    form={experienceForm}
                    setForm={setExperienceForm}
                    onSubmit={handleExperienceSubmit}
                    onCancel={() => {
                      setShowExperienceForm(false);
                      setEditingExperience(null);
                      resetExperienceForm();
                    }}
                    editingExperience={editingExperience}
                    loading={loading}
                  />
                )}

                {/* Experience List */}
                <div className="space-y-4">
                  {experience.map(exp => (
                    <div
                      key={exp.id}
                      className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                            {exp.title}
                          </h3>
                          <p className="text-blue-600 dark:text-blue-400 font-medium">
                            {exp.company}
                          </p>
                          <p className="text-gray-600 dark:text-gray-300 text-sm">
                            {exp.location}
                          </p>
                          <p className="text-gray-500 dark:text-gray-400 text-sm">
                            {exp.period}
                          </p>
                          <p className="text-gray-700 dark:text-gray-300 mt-2">
                            {exp.description}
                          </p>
                          <div className="flex flex-wrap gap-1 mt-2">
                            {exp.technologies.map((tech, index) => (
                              <span
                                key={index}
                                className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-xs"
                              >
                                {tech}
                              </span>
                            ))}
                          </div>
                        </div>
                        <div className="flex gap-2 ml-4">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleExperienceEdit(exp)}
                            disabled={loading}
                          >
                            Edit
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleExperienceDelete(exp.id)}
                            disabled={loading}
                            className="text-red-600 hover:text-red-700"
                          >
                            Delete
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'blog' && (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Manage Blog Posts
                  </h2>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => {
                      setShowBlogPostForm(true);
                      setEditingPost(null);
                      resetBlogPostForm();
                    }}
                    disabled={loading}
                  >
                    Add New Blog Post
                  </Button>
                </div>

                {showBlogPostForm && (
                  <BlogPostForm
                    form={blogPostForm}
                    setForm={setBlogPostForm}
                    onSubmit={handleBlogPostSubmit}
                    onCancel={() => {
                      setShowBlogPostForm(false);
                      setEditingPost(null);
                      resetBlogPostForm();
                    }}
                    editingPost={editingPost}
                    loading={loading}
                  />
                )}

                {/* Blog Posts List */}
                <div className="space-y-4">
                  {blogPosts.map(post => (
                    <div
                      key={post.id}
                      className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                            {post.title}
                            {post.published_at && (
                              <span className="ml-2 px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-xs rounded-full">
                                Published
                              </span>
                            )}
                          </h3>
                          <p className="text-gray-600 dark:text-gray-300 text-sm">
                            Slug: {post.slug}
                          </p>
                          {post.excerpt && (
                            <p className="text-gray-700 dark:text-gray-300 mt-2">
                              {post.excerpt}
                            </p>
                          )}
                          <div className="flex items-center gap-4 mt-2 text-sm text-gray-500 dark:text-gray-400">
                            {post.read_time && <span>{post.read_time}</span>}
                            {post.category && (
                              <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full">
                                {post.category.name}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="flex gap-2 ml-4">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleBlogPostEdit(post)}
                            disabled={loading}
                          >
                            Edit
                          </Button>
                          {!post.published_at && (
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleBlogPostPublish(post.id)}
                              disabled={loading}
                              className="text-green-600 hover:text-green-700"
                            >
                              Publish
                            </Button>
                          )}
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleBlogPostDelete(post.id)}
                            disabled={loading}
                            className="text-red-600 hover:text-red-700"
                          >
                            Delete
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
