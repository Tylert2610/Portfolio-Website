import React, { useState, useEffect } from 'react';
import { Button } from '../common';
import { apiService } from '../../services/api';
import type { BlogPost, BlogPostFormData, Category } from './types';

interface BlogPostFormProps {
  form: BlogPostFormData;
  setForm: React.Dispatch<React.SetStateAction<BlogPostFormData>>;
  onSubmit: (e: React.FormEvent) => Promise<void>;
  onCancel: () => void;
  editingPost: BlogPost | null;
  loading: boolean;
}

export const BlogPostForm: React.FC<BlogPostFormProps> = ({
  form,
  setForm,
  onSubmit,
  onCancel,
  editingPost,
  loading,
}) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [categoriesLoading, setCategoriesLoading] = useState(false);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    setCategoriesLoading(true);
    const response = await apiService.getCategories();
    if (response.data) {
      setCategories(response.data);
    }
    setCategoriesLoading(false);
  };

  const generateSlug = () => {
    const slug = form.title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');
    setForm(prev => ({ ...prev, slug }));
  };

  return (
    <div className="mb-6 bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        {editingPost ? 'Edit Blog Post' : 'Add New Blog Post'}
      </h3>
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Title *
          </label>
          <input
            type="text"
            value={form.title}
            onChange={e =>
              setForm(prev => ({
                ...prev,
                title: e.target.value,
              }))
            }
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:text-white"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Slug *
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={form.slug}
              onChange={e =>
                setForm(prev => ({
                  ...prev,
                  slug: e.target.value,
                }))
              }
              className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:text-white"
              required
            />
            <Button
              type="button"
              variant="outline"
              onClick={generateSlug}
              disabled={!form.title}
            >
              Generate
            </Button>
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Category
          </label>
          <select
            value={form.category_id || ''}
            onChange={e =>
              setForm(prev => ({
                ...prev,
                category_id: e.target.value
                  ? Number(e.target.value)
                  : undefined,
              }))
            }
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:text-white"
            disabled={categoriesLoading}
          >
            <option value="">Select a category</option>
            {categories.map(category => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Excerpt
          </label>
          <textarea
            value={form.excerpt}
            onChange={e =>
              setForm(prev => ({
                ...prev,
                excerpt: e.target.value,
              }))
            }
            rows={3}
            placeholder="Brief summary of the post..."
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:text-white"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Read Time
          </label>
          <input
            type="text"
            value={form.read_time}
            onChange={e =>
              setForm(prev => ({
                ...prev,
                read_time: e.target.value,
              }))
            }
            placeholder="e.g., 5 min read"
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:text-white"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Content *
          </label>
          <textarea
            value={form.content}
            onChange={e =>
              setForm(prev => ({
                ...prev,
                content: e.target.value,
              }))
            }
            rows={15}
            placeholder="Write your blog post content here... (Markdown supported)"
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:text-white font-mono text-sm"
            required
          />
        </div>
        <div className="flex gap-2">
          <Button type="submit" variant="primary" disabled={loading}>
            {loading
              ? 'Saving...'
              : editingPost
                ? 'Update Post'
                : 'Create Post'}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </Button>
        </div>
      </form>
    </div>
  );
};
