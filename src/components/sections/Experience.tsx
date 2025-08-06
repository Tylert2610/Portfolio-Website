import React from 'react';
import type { BaseComponentProps } from '../../types';

export type ExperienceProps = BaseComponentProps;

interface ExperienceItem {
  id: string;
  title: string;
  company: string;
  location: string;
  period: string;
  description: string;
  technologies: string[];
  achievements: string[];
}

export const Experience: React.FC<ExperienceProps> = ({ className = '' }) => {
  return (
    <section
      id="experience"
      className={`py-20 bg-white dark:bg-gray-900 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Experience
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            My professional journey and the impact I've made along the way
          </p>
        </div>

        {/* Timeline */}
        <div className="relative">
          {/* Timeline Line */}
          <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 h-full w-0.5 bg-gray-200 dark:bg-gray-700"></div>

          {/* Experience Items */}
          <div className="space-y-12">
            {experienceData.map((item, index) => (
              <ExperienceItem key={item.id} item={item} index={index} />
            ))}
          </div>
        </div>

        {/* Education Section */}
        <div className="mt-20">
          <h3 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
            Education
          </h3>
          <div className="grid md:grid-cols-2 gap-8">
            {educationData.map(education => (
              <div
                key={education.id}
                className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 hover:shadow-md transition-shadow duration-200"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h4 className="text-xl font-semibold text-gray-900 dark:text-white">
                      {education.degree}
                    </h4>
                    <p className="text-gray-600 dark:text-gray-300">
                      {education.institution}
                    </p>
                  </div>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {education.period}
                  </span>
                </div>
                <p className="text-gray-700 dark:text-gray-300 mb-3">
                  {education.description}
                </p>
                {education.gpa && (
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    GPA: {education.gpa}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Certifications */}
        <div className="mt-20">
          <h3 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
            Certifications
          </h3>
          <div className="grid md:grid-cols-3 gap-6">
            {certificationsData.map(cert => (
              <div
                key={cert.id}
                className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 text-center hover:shadow-md transition-shadow duration-200"
              >
                <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🏆</span>
                </div>
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {cert.name}
                </h4>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-3">
                  {cert.issuer}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {cert.date}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

const ExperienceItem: React.FC<{ item: ExperienceItem; index: number }> = ({
  item,
  index,
}) => {
  const isEven = index % 2 === 0;

  return (
    <div
      className={`relative flex items-center ${isEven ? 'md:flex-row' : 'md:flex-row-reverse'}`}
    >
      {/* Timeline Dot */}
      <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 w-4 h-4 bg-blue-500 rounded-full border-4 border-white dark:border-gray-900"></div>

      {/* Content */}
      <div
        className={`ml-12 md:ml-0 md:w-5/12 ${isEven ? 'md:mr-auto md:pr-8' : 'md:ml-auto md:pl-8'}`}
      >
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 hover:shadow-md transition-shadow duration-200">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                {item.title}
              </h3>
              <p className="text-blue-600 dark:text-blue-400 font-medium">
                {item.company}
              </p>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                {item.location}
              </p>
            </div>
            <span className="text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap">
              {item.period}
            </span>
          </div>

          <p className="text-gray-700 dark:text-gray-300 mb-4">
            {item.description}
          </p>

          {/* Technologies */}
          <div className="flex flex-wrap gap-2 mb-4">
            {item.technologies.map(tech => (
              <span
                key={tech}
                className="px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full"
              >
                {tech}
              </span>
            ))}
          </div>

          {/* Achievements */}
          <ul className="space-y-2">
            {item.achievements.map((achievement, idx) => (
              <li
                key={idx}
                className="text-sm text-gray-600 dark:text-gray-300 flex items-start"
              >
                <span className="text-blue-500 mr-2 mt-1">•</span>
                {achievement}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

// Experience data
const experienceData: ExperienceItem[] = [
  {
    id: '1',
    title: 'Senior Full-Stack Developer',
    company: 'TechCorp Solutions',
    location: 'San Francisco, CA',
    period: '2022 - Present',
    description:
      'Leading development of enterprise web applications and mentoring junior developers.',
    technologies: ['React', 'TypeScript', 'Node.js', 'PostgreSQL', 'AWS'],
    achievements: [
      'Led a team of 5 developers to deliver a major e-commerce platform',
      'Improved application performance by 40% through optimization',
      'Implemented CI/CD pipeline reducing deployment time by 60%',
      'Mentored 3 junior developers and conducted code reviews',
    ],
  },
  {
    id: '2',
    title: 'Full-Stack Developer',
    company: 'InnovateWeb',
    location: 'Remote',
    period: '2021 - 2022',
    description:
      'Developed and maintained multiple client websites and web applications.',
    technologies: ['React', 'JavaScript', 'Express.js', 'MongoDB', 'Heroku'],
    achievements: [
      'Built 15+ client websites with 100% client satisfaction',
      'Reduced bug reports by 50% through improved testing practices',
      'Collaborated with design team to implement responsive designs',
      'Optimized database queries improving load times by 30%',
    ],
  },
  {
    id: '3',
    title: 'Frontend Developer',
    company: 'StartupHub',
    location: 'Austin, TX',
    period: '2020 - 2021',
    description:
      'Focused on creating responsive and accessible user interfaces.',
    technologies: ['React', 'JavaScript', 'CSS3', 'HTML5', 'Git'],
    achievements: [
      'Developed 10+ reusable React components',
      'Improved website accessibility score to 95%',
      'Reduced bundle size by 25% through code optimization',
      'Participated in agile development process with 2-week sprints',
    ],
  },
];

// Education data
const educationData = [
  {
    id: '1',
    degree: 'Bachelor of Science in Computer Science',
    institution: 'University of Texas at Austin',
    period: '2016 - 2020',
    description:
      'Focused on software engineering, algorithms, and web development. Completed capstone project on machine learning applications.',
    gpa: '3.8/4.0',
  },
  {
    id: '2',
    degree: 'Web Development Bootcamp',
    institution: 'Coding Academy',
    period: '2020',
    description:
      'Intensive 12-week program covering full-stack web development with modern technologies.',
    gpa: null,
  },
];

// Certifications data
const certificationsData = [
  {
    id: '1',
    name: 'AWS Certified Developer',
    issuer: 'Amazon Web Services',
    date: '2023',
  },
  {
    id: '2',
    name: 'React Developer Certification',
    issuer: 'Meta',
    date: '2022',
  },
  {
    id: '3',
    name: 'TypeScript Professional',
    issuer: 'Microsoft',
    date: '2021',
  },
];
