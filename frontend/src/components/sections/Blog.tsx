import React from 'react';
import { Card, Button } from '../common';
import type { BaseComponentProps } from '../../types';

export type BlogProps = BaseComponentProps;

interface BlogPost {
  id: string;
  title: string;
  excerpt: string;
  date: string;
  readTime: string;
  category: string;
  image: string;
  slug: string;
}

export const Blog: React.FC<BlogProps> = ({ className = '' }) => {
  return (
    <section
      id="blog"
      className={`py-20 bg-gray-50 dark:bg-gray-800 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Blog & Articles
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Thoughts on web development, technology trends, and best practices
          </p>
        </div>

        {/* Featured Post */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">
            Featured Article
          </h3>
          <div className="bg-white dark:bg-gray-700 rounded-lg overflow-hidden shadow-lg">
            <div className="md:flex">
              <div className="md:w-1/2">
                <div className="h-64 md:h-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                  <span className="text-white text-6xl">📝</span>
                </div>
              </div>
              <div className="md:w-1/2 p-8">
                <div className="flex items-center space-x-4 mb-4">
                  <span className="px-3 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full">
                    Web Development
                  </span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    5 min read
                  </span>
                </div>
                <h4 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  Building Modern Web Applications with React and TypeScript
                </h4>
                <p className="text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
                  Explore the benefits of using TypeScript with React for
                  building scalable, maintainable web applications. Learn best
                  practices, common patterns, and how to avoid common pitfalls
                  in modern web development.
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    January 15, 2024
                  </span>
                  <Button variant="primary" size="sm">
                    Read More
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Posts Grid */}
        <div className="mb-12">
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">
            Recent Posts
          </h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {blogPosts.slice(0, 6).map(post => (
              <BlogPostCard key={post.id} post={post} />
            ))}
          </div>
        </div>

        {/* Newsletter Signup */}
        <div className="bg-white dark:bg-gray-700 rounded-lg p-8 text-center shadow-sm">
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Stay Updated
          </h3>
          <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-2xl mx-auto">
            Get notified when I publish new articles about web development,
            technology trends, and industry insights.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
            />
            <Button variant="primary">Subscribe</Button>
          </div>
        </div>

        {/* View All Posts Button */}
        <div className="text-center mt-12">
          <Button variant="outline" size="lg">
            View All Posts
          </Button>
        </div>
      </div>
    </section>
  );
};

const BlogPostCard: React.FC<{ post: BlogPost }> = ({ post }) => {
  return (
    <Card
      title={post.title}
      description={post.excerpt}
      image={post.image}
      category={post.category}
      placeholderType="blog"
      className="h-full hover:shadow-lg transition-shadow duration-300"
    >
      <div className="space-y-4">
        <div className="flex items-center justify-between text-sm">
          <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full">
            {post.category}
          </span>
          <span className="text-gray-500 dark:text-gray-400">
            {post.readTime}
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {post.date}
          </span>
          <Button variant="ghost" size="sm">
            Read More →
          </Button>
        </div>
      </div>
    </Card>
  );
};

// Sample blog posts data
const blogPosts: BlogPost[] = [
  {
    id: '1',
    title: 'The Future of Web Development: What to Expect in 2024',
    excerpt:
      'Exploring emerging technologies and trends that will shape the web development landscape in the coming year.',
    date: 'January 10, 2024',
    readTime: '4 min read',
    category: 'Technology',
    image: '',
    slug: 'future-web-development-2024',
  },
  {
    id: '2',
    title: 'Optimizing React Performance: Best Practices and Tools',
    excerpt:
      'Learn how to identify and fix performance bottlenecks in your React applications using modern tools and techniques.',
    date: 'January 8, 2024',
    readTime: '6 min read',
    category: 'React',
    image: '',
    slug: 'optimizing-react-performance',
  },
  {
    id: '3',
    title: 'TypeScript vs JavaScript: When to Use Each',
    excerpt:
      'A comprehensive comparison of TypeScript and JavaScript, helping you decide which to use for your next project.',
    date: 'January 5, 2024',
    readTime: '5 min read',
    category: 'TypeScript',
    image: '',
    slug: 'typescript-vs-javascript',
  },
  {
    id: '4',
    title: 'Building Accessible Web Applications',
    excerpt:
      'Essential guidelines and techniques for creating web applications that work for everyone, including users with disabilities.',
    date: 'January 3, 2024',
    readTime: '7 min read',
    category: 'Accessibility',
    image: '',
    slug: 'building-accessible-web-applications',
  },
  {
    id: '5',
    title: 'Deploying to AWS: A Step-by-Step Guide',
    excerpt:
      'Complete walkthrough of deploying a React application to AWS using S3, CloudFront, and Route 53.',
    date: 'December 30, 2023',
    readTime: '8 min read',
    category: 'DevOps',
    image: '',
    slug: 'deploying-to-aws-guide',
  },
  {
    id: '6',
    title: 'State Management in React: Context vs Redux',
    excerpt:
      'Comparing different state management solutions in React and when to use each approach.',
    date: 'December 28, 2023',
    readTime: '6 min read',
    category: 'React',
    image: '',
    slug: 'state-management-react-context-redux',
  },
];
