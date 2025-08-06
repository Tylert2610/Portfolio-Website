import React, { useState } from 'react';
import { Card, Button } from '../common';
import type { BaseComponentProps, Project } from '../../types';

export interface ProjectsProps extends BaseComponentProps {
  projects?: Project[];
}

export const Projects: React.FC<ProjectsProps> = ({
  className = '',
  projects = defaultProjects,
}) => {
  const [filter, setFilter] = useState<string>('all');
  const [showAll, setShowAll] = useState(false);

  const categories = ['all', 'frontend', 'fullstack', 'backend', 'design'];

  const filteredProjects = projects.filter(project => {
    if (filter === 'all') return true;
    return project.technologies.some(tech =>
      tech.toLowerCase().includes(filter)
    );
  });

  const displayedProjects = showAll
    ? filteredProjects
    : filteredProjects.slice(0, 6);

  return (
    <section
      id="projects"
      className={`py-20 bg-gray-50 dark:bg-gray-800 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Featured Projects
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            A showcase of my recent work and technical capabilities
          </p>
        </div>

        {/* Filter Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {categories.map(category => (
            <Button
              key={category}
              variant={filter === category ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setFilter(category)}
              className="capitalize"
            >
              {category}
            </Button>
          ))}
        </div>

        {/* Projects Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {displayedProjects.map(project => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>

        {/* Show More/Less Button */}
        {filteredProjects.length > 6 && (
          <div className="text-center">
            <Button
              variant="outline"
              onClick={() => setShowAll(!showAll)}
              className="px-8"
            >
              {showAll
                ? 'Show Less'
                : `Show ${filteredProjects.length - 6} More Projects`}
            </Button>
          </div>
        )}

        {/* Call to Action */}
        <div className="mt-20 text-center">
          <div className="bg-white dark:bg-gray-700 rounded-lg p-8 shadow-sm">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Have a project in mind?
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-2xl mx-auto">
              I'm always interested in new opportunities and exciting projects.
              Let's discuss how we can work together to bring your ideas to
              life.
            </p>
            <Button variant="primary" size="lg">
              Get In Touch
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

const ProjectCard: React.FC<{ project: Project }> = ({ project }) => {
  return (
    <Card
      title={project.title}
      description={project.description}
      image={project.image}
      link={project.liveUrl || undefined}
      className="group hover:shadow-lg transition-all duration-300"
    >
      <div className="space-y-4">
        {/* Technologies */}
        <div className="flex flex-wrap gap-2">
          {project.technologies.slice(0, 4).map(tech => (
            <span
              key={tech}
              className="px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full"
            >
              {tech}
            </span>
          ))}
          {project.technologies.length > 4 && (
            <span className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full">
              +{project.technologies.length - 4} more
            </span>
          )}
        </div>

        {/* Project Links */}
        <div className="flex gap-3 pt-4">
          {project.liveUrl && (
            <Button
              variant="primary"
              size="sm"
              onClick={() =>
                project.liveUrl && window.open(project.liveUrl, '_blank')
              }
              className="flex-1"
            >
              Live Demo
            </Button>
          )}
          {project.githubUrl && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => window.open(project.githubUrl, '_blank')}
              className="flex-1"
            >
              View Code
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
};

// Default projects data
const defaultProjects: Project[] = [
  {
    id: '1',
    title: 'E-Commerce Platform',
    description:
      'A full-stack e-commerce platform built with React, Node.js, and PostgreSQL. Features include user authentication, product management, shopping cart, and payment integration.',
    image: '/api/placeholder/400/250',
    technologies: ['React', 'TypeScript', 'Node.js', 'PostgreSQL', 'Stripe'],
    githubUrl: 'https://github.com/Tylert2610/ecommerce-platform',
    liveUrl: 'https://ecommerce-demo.vercel.app',
    featured: true,
  },
  {
    id: '2',
    title: 'Task Management App',
    description:
      'A collaborative task management application with real-time updates, drag-and-drop functionality, and team collaboration features.',
    image: '/api/placeholder/400/250',
    technologies: ['React', 'TypeScript', 'Socket.io', 'MongoDB', 'Express'],
    githubUrl: 'https://github.com/Tylert2610/task-manager',
    liveUrl: 'https://task-manager-demo.vercel.app',
    featured: true,
  },
  {
    id: '3',
    title: 'Weather Dashboard',
    description:
      'A beautiful weather dashboard that displays current weather and forecasts using OpenWeatherMap API with interactive charts and location-based features.',
    image: '/api/placeholder/400/250',
    technologies: ['React', 'TypeScript', 'Chart.js', 'OpenWeatherMap API'],
    githubUrl: 'https://github.com/Tylert2610/weather-dashboard',
    liveUrl: 'https://weather-dashboard-demo.vercel.app',
    featured: false,
  },
  {
    id: '4',
    title: 'Portfolio Website',
    description:
      'A modern, responsive portfolio website built with React and Tailwind CSS, featuring smooth animations and SEO optimization.',
    image: '/api/placeholder/400/250',
    technologies: ['React', 'TypeScript', 'Tailwind CSS', 'Vite'],
    githubUrl: 'https://github.com/Tylert2610/portfolio-website',
    liveUrl: 'https://portfolio.webbpulse.com',
    featured: true,
  },
  {
    id: '5',
    title: 'Blog Platform',
    description:
      'A content management system for blogs with markdown support, user authentication, and admin dashboard.',
    image: '/api/placeholder/400/250',
    technologies: ['Next.js', 'TypeScript', 'Prisma', 'PostgreSQL', 'Markdown'],
    githubUrl: 'https://github.com/Tylert2610/blog-platform',
    liveUrl: 'https://blog-platform-demo.vercel.app',
    featured: false,
  },
  {
    id: '6',
    title: 'API Gateway',
    description:
      'A microservices API gateway built with Node.js and Express, featuring rate limiting, authentication, and request routing.',
    image: '/api/placeholder/400/250',
    technologies: ['Node.js', 'Express', 'Redis', 'JWT', 'Docker'],
    githubUrl: 'https://github.com/Tylert2610/api-gateway',
    liveUrl: null,
    featured: false,
  },
  {
    id: '7',
    title: 'Social Media Dashboard',
    description:
      'A comprehensive dashboard for managing multiple social media accounts with analytics and scheduling features.',
    image: '/api/placeholder/400/250',
    technologies: ['React', 'TypeScript', 'Node.js', 'MongoDB', 'Social APIs'],
    githubUrl: 'https://github.com/Tylert2610/social-dashboard',
    liveUrl: 'https://social-dashboard-demo.vercel.app',
    featured: false,
  },
  {
    id: '8',
    title: 'Real-time Chat App',
    description:
      'A real-time chat application with private messaging, group chats, and file sharing capabilities.',
    image: '/api/placeholder/400/250',
    technologies: ['React', 'Socket.io', 'Node.js', 'MongoDB', 'AWS S3'],
    githubUrl: 'https://github.com/Tylert2610/chat-app',
    liveUrl: 'https://chat-app-demo.vercel.app',
    featured: false,
  },
];
