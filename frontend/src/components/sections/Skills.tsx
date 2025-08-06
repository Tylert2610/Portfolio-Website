import React from 'react';
import type { BaseComponentProps, Skill } from '../../types';

export interface SkillsProps extends BaseComponentProps {
  skills?: Skill[];
}

export const Skills: React.FC<SkillsProps> = ({
  className = '',
  skills = defaultSkills,
}) => {
  const skillCategories = [
    { name: 'Frontend', color: 'blue' },
    { name: 'Backend', color: 'green' },
    { name: 'DevOps & Infrastructure', color: 'purple' },
    { name: 'Networking & Security', color: 'red' },
    { name: 'Other', color: 'orange' },
  ];

  const getSkillsByCategory = (category: string) => {
    return skills.filter(skill => skill.category === category);
  };

  return (
    <section
      id="skills"
      className={`py-20 bg-white dark:bg-gray-900 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Skills & Technologies
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            A comprehensive overview of my technical expertise and tools I work
            with
          </p>
        </div>

        {/* Skills Grid */}
        <div className="space-y-12">
          {skillCategories.map(category => {
            const categorySkills = getSkillsByCategory(
              category.name.toLowerCase()
            );
            if (categorySkills.length === 0) return null;

            return (
              <div key={category.name} className="space-y-6">
                <h3 className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {category.name}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {categorySkills.map(skill => (
                    <SkillCard key={skill.name} skill={skill} />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

const SkillCard: React.FC<{ skill: Skill }> = ({ skill }) => {
  const getCategoryColor = (category: string) => {
    const colorMap: Record<string, string> = {
      frontend: 'blue',
      backend: 'green',
      devops: 'purple',
      design: 'pink',
      other: 'orange',
    };
    return colorMap[category] || 'gray';
  };

  return (
    <div className="group relative p-4 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200">
      <div className="flex items-center space-x-3">
        <div
          className={`w-10 h-10 bg-${getCategoryColor(skill.category)}-100 dark:bg-${getCategoryColor(skill.category)}-900 rounded-lg flex items-center justify-center`}
        >
          <span className="text-lg">{skill.icon || '💻'}</span>
        </div>
        <div>
          <h4 className="font-medium text-gray-900 dark:text-white">
            {skill.name}
          </h4>
          <div className="flex items-center space-x-1">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className={`w-1 h-1 rounded-full ${
                  i < Math.floor(skill.proficiency / 20)
                    ? `bg-${getCategoryColor(skill.category)}-500`
                    : 'bg-gray-300 dark:bg-gray-600'
                }`}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Default skills data
const defaultSkills: Skill[] = [
  // Frontend
  { name: 'React', category: 'frontend', proficiency: 85, icon: '⚛️' },
  { name: 'TypeScript', category: 'frontend', proficiency: 80, icon: '📘' },
  { name: 'JavaScript', category: 'frontend', proficiency: 85, icon: '🟨' },
  { name: 'HTML/CSS', category: 'frontend', proficiency: 80, icon: '🎨' },
  { name: 'Tailwind CSS', category: 'frontend', proficiency: 75, icon: '🎯' },
  { name: 'Flutter/Dart', category: 'frontend', proficiency: 70, icon: '📱' },

  // Backend
  { name: 'Python', category: 'backend', proficiency: 90, icon: '🐍' },
  { name: 'FastAPI', category: 'backend', proficiency: 80, icon: '⚡' },
  { name: 'PostgreSQL', category: 'backend', proficiency: 75, icon: '🐘' },
  { name: 'SQL', category: 'backend', proficiency: 85, icon: '🗄️' },
  { name: 'Firebase', category: 'backend', proficiency: 70, icon: '🔥' },

  // DevOps & Infrastructure
  { name: 'AWS', category: 'devops', proficiency: 80, icon: '☁️' },
  { name: 'Docker', category: 'devops', proficiency: 75, icon: '🐳' },
  { name: 'Kubernetes', category: 'devops', proficiency: 65, icon: '⚓' },
  { name: 'Git', category: 'devops', proficiency: 90, icon: '📚' },
  { name: 'Bash', category: 'devops', proficiency: 85, icon: '💻' },
  { name: 'Datadog', category: 'devops', proficiency: 80, icon: '📊' },

  // Networking & Security
  {
    name: 'Network Troubleshooting',
    category: 'other',
    proficiency: 85,
    icon: '🌐',
  },
  { name: 'Wireshark', category: 'other', proficiency: 75, icon: '🔍' },
  { name: 'Active Directory', category: 'other', proficiency: 80, icon: '🏢' },
  { name: 'Azure', category: 'other', proficiency: 75, icon: '🔵' },
  { name: 'GCP', category: 'other', proficiency: 70, icon: '☁️' },

  // Other
  { name: 'Problem Solving', category: 'other', proficiency: 95, icon: '🧩' },
  {
    name: 'Technical Documentation',
    category: 'other',
    proficiency: 85,
    icon: '📝',
  },
  { name: 'Automation', category: 'other', proficiency: 90, icon: '🤖' },
];
