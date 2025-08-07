import type { Project } from '../types';

// Default projects data
export const defaultProjects: Project[] = [
  {
    id: '1',
    title: 'Car Modification Planning Tool',
    description:
      'Full-stack web application enabling automotive enthusiasts to manage vehicle modification projects. Features user authentication, detailed build lists, part tracking with specifications, and responsive design.',
    image: '',
    technologies: [
      'Python',
      'TypeScript',
      'Tailwind CSS',
      'FastAPI',
      'React',
      'PostgreSQL',
      'Docker',
    ],
    githubUrl: 'https://github.com/Tylert2610/CarModPicker-Frontend',
    liveUrl: undefined,
    featured: true,
  },
  {
    id: '1-backend',
    title: 'Car Modification Planning Tool - Backend',
    description:
      'Python FastAPI backend providing RESTful APIs for the car modification planning tool. Features PostgreSQL database, authentication, and comprehensive API endpoints.',
    image: '',
    technologies: [
      'Python',
      'FastAPI',
      'PostgreSQL',
      'Docker',
      'SQLAlchemy',
      'Pydantic',
    ],
    githubUrl: 'https://github.com/Tylert2610/CarModPicker-Backend',
    liveUrl: undefined,
    featured: false,
  },
  {
    id: '2',
    title: 'Inventory Tracking System',
    description:
      'Full-stack application for tracking lab device checkout status across multiple platforms. Built for Verkada tech support team with web, Android, and iOS support.',
    image: '',
    technologies: ['Dart', 'Flutter', 'Firebase', 'Python', 'Git', 'NoSQL'],
    githubUrl: 'https://github.com/Tylert2610/WebbPulse-Inventory-Management',
    liveUrl: 'webbpulse.com',
    featured: true,
  },
  {
    id: '3',
    title: 'Portfolio Website',
    description:
      'Modern, responsive portfolio website built with React and TypeScript, featuring smooth animations, dark theme, and SEO optimization.',
    image: '',
    technologies: ['React', 'TypeScript', 'Tailwind CSS', 'Vite'],
    githubUrl: 'https://github.com/Tylert2610/Portfolio-Website',
    liveUrl: undefined,
    featured: true,
  },
  {
    id: '4',
    title: 'Internal Automation Tools',
    description:
      'Collection of Python scripts and tools developed for Verkada support team to automate repetitive tasks and improve efficiency.',
    image: '',
    technologies: ['Python', 'SQL', 'Bash', 'Datadog', 'AWS'],
    githubUrl: undefined,
    liveUrl: undefined,
    featured: false,
  },
  {
    id: '5',
    title: 'Custom Monitoring & Analytics Dashboards',
    description:
      'Engineered comprehensive monitoring solutions and analytics dashboards for engineering operations teams. Built performance metrics tracking, and real-time visibility tools to streamline incident response and improve system reliability.',
    image: '',
    technologies: ['Datadog', 'SQL', 'Metabase', 'AWS'],
    githubUrl: undefined,
    liveUrl: undefined,
    featured: false,
  },
  {
    id: '6',
    title: 'HelpVerkada Web Crawler',
    description:
      'Python-based web crawler designed to automate data collection and analysis for Verkada support operations. Streamlines information gathering processes.',
    image: '',
    technologies: ['Python', 'Web Scraping', 'Automation', 'Data Processing'],
    githubUrl: 'https://github.com/Tylert2610/HelpVerkadaWebCrawler',
    liveUrl: undefined,
    featured: false,
  },
];
