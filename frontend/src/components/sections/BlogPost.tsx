import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Header, Footer } from '../layout';
import { Button } from '../common';
import { apiService } from '../../services/api';
import type { BlogPost as BlogPostType } from '../../services/api';
import type { NavigationItem, SocialLink } from '../../types';
import { processMarkdown, extractHeadings } from '../../utils/markdown';

export const BlogPost: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [post, setPost] = useState<BlogPostType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [readingProgress, setReadingProgress] = useState(0);
  const [showTableOfContents, setShowTableOfContents] = useState(false);

  const navigationItems: NavigationItem[] = [
    { label: 'Home', href: '/' },
    { label: 'About', href: '/#about' },
    { label: 'Skills', href: '/#skills' },
    { label: 'Projects', href: '/#projects' },
    { label: 'Experience', href: '/#experience' },
    { label: 'Blog', href: '/blog' },
    { label: 'Contact', href: '/#contact' },
  ];

  const socialLinks: SocialLink[] = [
    {
      platform: 'GitHub',
      url: 'https://github.com/Tylert2610',
      icon: 'github',
    },
    {
      platform: 'LinkedIn',
      url: 'https://www.linkedin.com/in/tylert2610/',
      icon: 'linkedin',
    },
  ];

  useEffect(() => {
    const fetchPost = async () => {
      if (!slug) return;

      setLoading(true);
      setError(null);

      try {
        const response = await apiService.getBlogPostBySlug(slug);
        if (response.error) {
          setError(response.error);
        } else {
          setPost(response.data);
        }
      } catch {
        setError('Failed to load blog post');
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [slug]);

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = (scrollTop / docHeight) * 100;
      setReadingProgress(Math.min(scrollPercent, 100));
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const processContent = (content: string) => {
    // Process markdown content to HTML with styling
    return processMarkdown(content);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900">
        <Header navigationItems={navigationItems} />
        <main className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">Loading...</p>
          </div>
        </main>
        <Footer socialLinks={socialLinks} />
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900">
        <Header navigationItems={navigationItems} />
        <main className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Blog Post Not Found
            </h1>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              {error || 'The blog post you are looking for does not exist.'}
            </p>
            <Link to="/">
              <Button variant="primary">Back to Home</Button>
            </Link>
          </div>
        </main>
        <Footer socialLinks={socialLinks} />
      </div>
    );
  }

  const headings = extractHeadings(post.content);
  const processedContent = processContent(post.content);

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      {/* Reading Progress Bar */}
      <div className="fixed top-0 left-0 w-full h-1 bg-gray-200 dark:bg-gray-700 z-50">
        <div
          className="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-300 ease-out"
          style={{ width: `${readingProgress}%` }}
        />
      </div>

      <Header navigationItems={navigationItems} />
      <main className="py-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Main Content */}
            <article className="lg:col-span-3">
              {/* Header */}
              <header className="mb-12">
                <div className="flex items-center space-x-4 mb-6">
                  {post.category && (
                    <span className="px-3 py-1 text-sm bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full font-medium">
                      {post.category.name}
                    </span>
                  )}
                  {post.read_time && (
                    <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center">
                      <svg
                        className="w-4 h-4 mr-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      {post.read_time}
                    </span>
                  )}
                </div>

                <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
                  {post.title}
                </h1>

                {post.excerpt && (
                  <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed font-light">
                    {post.excerpt}
                  </p>
                )}

                <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-700 pt-6">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                        <span className="text-white text-sm font-medium">
                          TW
                        </span>
                      </div>
                      <span>Tyler Webb</span>
                    </div>
                    <span>•</span>
                    <span>
                      {post.published_at &&
                        new Date(post.published_at).toLocaleDateString(
                          'en-US',
                          {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                          }
                        )}
                    </span>
                  </div>
                  <Link to="/#blog">
                    <Button variant="outline" size="sm">
                      ← Back to Blog
                    </Button>
                  </Link>
                </div>
              </header>

              {/* Content */}
              <div className="prose prose-lg dark:prose-invert max-w-none">
                <div
                  className="text-gray-700 dark:text-gray-300 leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: processedContent }}
                />
              </div>

              {/* Footer */}
              <footer className="mt-16 pt-8 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    <p>Written by Tyler Webb</p>
                    {post.updated_at && post.updated_at !== post.created_at && (
                      <p>
                        Last updated:{' '}
                        {new Date(post.updated_at).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                  <Link to="/#blog">
                    <Button variant="outline">View All Posts</Button>
                  </Link>
                </div>
              </footer>
            </article>

            {/* Sidebar */}
            <aside className="lg:col-span-1">
              <div className="sticky top-24 space-y-6">
                {/* Table of Contents */}
                {headings.length > 0 && (
                  <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Table of Contents
                      </h3>
                      <button
                        onClick={() =>
                          setShowTableOfContents(!showTableOfContents)
                        }
                        className="lg:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                      >
                        <svg
                          className="w-5 h-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 9l-7 7-7-7"
                          />
                        </svg>
                      </button>
                    </div>
                    <nav
                      className={`${showTableOfContents ? 'block' : 'hidden lg:block'}`}
                    >
                      <ul className="space-y-2">
                        {headings.map((heading, index) => (
                          <li key={index}>
                            <a
                              href={`#${heading.id}`}
                              className={`block text-sm hover:text-blue-600 dark:hover:text-blue-400 transition-colors ${
                                heading.level === 2
                                  ? 'text-gray-700 dark:text-gray-300 font-medium'
                                  : 'text-gray-600 dark:text-gray-400 ml-4'
                              }`}
                            >
                              {heading.text}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </nav>
                  </div>
                )}

                {/* Share Section */}
                <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Share this post
                  </h3>
                  <div className="flex space-x-3">
                    <button
                      onClick={() => {
                        navigator.share?.({
                          title: post.title,
                          url: window.location.href,
                        });
                      }}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                    >
                      Share
                    </button>
                    <button
                      onClick={() =>
                        navigator.clipboard.writeText(window.location.href)
                      }
                      className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                    >
                      Copy Link
                    </button>
                  </div>
                </div>

                {/* Author Info */}
                <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-6">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-white text-xl font-bold">TW</span>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      Tyler Webb
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
                      Escalations Engineer at Verkada
                    </p>
                    <div className="flex justify-center space-x-3">
                      <a
                        href="https://github.com/Tylert2610"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors"
                      >
                        <svg
                          className="w-5 h-5"
                          fill="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                        </svg>
                      </a>
                      <a
                        href="https://www.linkedin.com/in/tylert2610/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors"
                      >
                        <svg
                          className="w-5 h-5"
                          fill="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
                        </svg>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </main>
      <Footer socialLinks={socialLinks} />
    </div>
  );
};
