import React, { useState } from 'react';
import { Card, Button } from '../common';
import type { BaseComponentProps, Project } from '../../types';
import { defaultProjects } from '../../data/projects';

export interface ProjectsProps extends BaseComponentProps {
  projects?: Project[];
}

export const Projects: React.FC<ProjectsProps> = ({
  className = '',
  projects = defaultProjects,
}) => {
  const [filter, setFilter] = useState<string>('all');
  const [showAll, setShowAll] = useState(false);

  const categories = ['all', 'frontend', 'backend', 'automation'];

  // Define technology mappings for each category
  const categoryTechnologies = {
    frontend: [
      'react',
      'typescript',
      'javascript',
      'html',
      'css',
      'tailwind',
      'vite',
      'flutter',
      'dart',
    ],
    backend: [
      'fastapi',
      'postgresql',
      'sqlalchemy',
      'pydantic',
      'firebase',
      'nosql',
    ],
    automation: ['web scraping', 'automation', 'data processing', 'bash'],
  };

  const filteredProjects = projects.filter(project => {
    if (filter === 'all') return true;

    const projectTechs = project.technologies.map(tech => tech.toLowerCase());
    const categoryTechs =
      categoryTechnologies[filter as keyof typeof categoryTechnologies] || [];

    return categoryTechs.some(categoryTech =>
      projectTechs.some(projectTech => projectTech.includes(categoryTech))
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
  // Determine the primary category based on technologies
  const getProjectCategory = (technologies: string[]): string => {
    const techs = technologies.map(tech => tech.toLowerCase());

    if (techs.some(tech => ['flutter', 'dart'].includes(tech)))
      return 'flutter';
    if (
      techs.some(tech => ['react', 'typescript', 'javascript'].includes(tech))
    )
      return 'react';
    if (techs.some(tech => ['python', 'fastapi'].includes(tech)))
      return 'python';
    if (techs.some(tech => ['web scraping', 'automation'].includes(tech)))
      return 'automation';

    return 'technology';
  };

  const category = getProjectCategory(project.technologies);

  return (
    <Card
      title={project.title}
      description={project.description}
      image={project.image}
      link={project.liveUrl || undefined}
      category={category}
      placeholderType="project"
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
