export interface ExperienceItem {
  id: string;
  title: string;
  company: string;
  location: string;
  period: string;
  startDate: string; // ISO date string for calculations
  endDate?: string; // Optional for current positions
  description: string;
  technologies: string[];
  achievements: string[];
}

// Experience data
export const experienceData: ExperienceItem[] = [
  {
    id: '1',
    title: 'Escalations Engineer',
    company: 'Verkada',
    location: 'San Mateo, CA',
    period: 'Jul 2024 - Present',
    startDate: '2024-07-01',
    description:
      'Leading critical incident resolution and technical troubleshooting while developing internal tools and automation solutions to improve team efficiency.',
    technologies: [
      'Python',
      'SQL',
      'Bash',
      'Datadog',
      'AWS',
      'GCP',
      'Azure',
      'Docker',
    ],
    achievements: [
      'Developed and deployed internal tools using Python and SQL to automate repetitive tasks',
      'Built custom monitoring solutions and dashboards to improve incident response times',
      'Collaborated with development teams to identify and resolve complex system issues',
      'Mentored junior engineers on technical troubleshooting and automation best practices',
      'Proactively identified system vulnerabilities and implemented performance optimizations',
    ],
  },
  {
    id: '2',
    title: 'Senior Technical Support Engineer',
    company: 'Verkada',
    location: 'San Mateo, CA',
    period: 'Jul 2022 - Jul 2024',
    startDate: '2022-07-01',
    endDate: '2024-07-01',
    description:
      'Provided technical support for enterprise customers while developing automation scripts and tools to streamline support processes.',
    technologies: [
      'Python',
      'SQL',
      'Bash',
      'Wireshark',
      'Active Directory',
      'Salesforce',
    ],
    achievements: [
      'Built automation scripts in Python to reduce manual troubleshooting time by 60%',
      'Developed internal tools for inventory management and device tracking',
      'Submitted detailed bug reports and collaborated with engineering teams on solutions',
      'Handled escalated accounts for Fortune 500 companies and strategic customers',
      'Created comprehensive documentation for complex technical procedures',
    ],
  },
];

// Utility function to calculate total years of experience
export const calculateYearsOfExperience = (): number => {
  const now = new Date();
  let totalYears = 0;

  experienceData.forEach(experience => {
    const startDate = new Date(experience.startDate);
    const endDate = experience.endDate ? new Date(experience.endDate) : now;

    const years =
      (endDate.getTime() - startDate.getTime()) /
      (1000 * 60 * 60 * 24 * 365.25);
    totalYears += years;
  });

  return Math.round(totalYears);
};
