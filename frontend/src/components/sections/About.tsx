import React from 'react';
import { Card } from '../common';
import type { BaseComponentProps } from '../../types';
import { defaultProjects } from '../../data/projects';
import { calculateYearsOfExperience } from '../../data/experience';

export type AboutProps = BaseComponentProps;

export const About: React.FC<AboutProps> = ({ className = '' }) => {
  const projectCount = defaultProjects.length;
  const yearsOfExperience = calculateYearsOfExperience();

  return (
    <section
      id="about"
      className={`py-20 bg-gray-50 dark:bg-gray-800 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            About Me
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Full-stack developer passionate about creating innovative web
            solutions
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Profile Content */}
          <div className="space-y-6">
            <div className="prose prose-lg dark:prose-invert max-w-none">
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed">
                Hi, I'm Tyler Webb! I'm a passionate full-stack developer with a
                love for creating elegant, user-friendly web applications. With
                expertise in modern technologies like React, TypeScript, and
                Node.js, I enjoy turning complex problems into simple, beautiful
                solutions.
              </p>

              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed">
                When I'm not coding, you can find me exploring new technologies,
                contributing to open-source projects, or sharing knowledge with
                the developer community. I believe in writing clean,
                maintainable code and creating experiences that users love.
              </p>
            </div>

            {/* Key Highlights */}
            <div className="grid grid-cols-2 gap-4 mt-8">
              <div className="text-center p-4 bg-white dark:bg-gray-700 rounded-lg shadow-sm">
                <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {yearsOfExperience}+
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300">
                  Years Experience
                </div>
              </div>
              <div className="text-center p-4 bg-white dark:bg-gray-700 rounded-lg shadow-sm">
                <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {projectCount}+
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300">
                  Projects Completed
                </div>
              </div>
            </div>
          </div>

          {/* Profile Image/Illustration */}
          <div className="flex justify-center lg:justify-end">
            <div className="relative">
              <div className="w-80 h-80 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <div className="text-white text-6xl font-bold">TW</div>
              </div>
              <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-green-500 rounded-full flex items-center justify-center">
                <span className="text-white text-2xl">🚀</span>
              </div>
            </div>
          </div>
        </div>

        {/* Values/Philosophy */}
        <div className="mt-20">
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white text-center mb-12">
            What I Value
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <Card
              title="Clean Code"
              description="Writing maintainable, well-documented code that others can easily understand and build upon."
              placeholderType="value"
              className="text-center"
            />
            <Card
              title="User Experience"
              description="Creating intuitive, accessible interfaces that provide delightful user experiences."
              placeholderType="value"
              className="text-center"
            />
            <Card
              title="Continuous Learning"
              description="Staying up-to-date with the latest technologies and best practices in web development."
              placeholderType="value"
              className="text-center"
            />
          </div>
        </div>
      </div>
    </section>
  );
};
