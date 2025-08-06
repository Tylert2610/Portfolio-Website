import React from 'react';
import { Header, Footer } from '../components/layout';
import {
  Hero,
  About,
  Skills,
  Projects,
  Experience,
  Blog,
  Contact,
} from '../components/sections';
import type { NavigationItem, SocialLink } from '../types';

const Home: React.FC = () => {
  const navigationItems: NavigationItem[] = [
    { label: 'About', href: '#about' },
    { label: 'Skills', href: '#skills' },
    { label: 'Projects', href: '#projects' },
    { label: 'Experience', href: '#experience' },
    { label: 'Blog', href: '#blog' },
    { label: 'Contact', href: '#contact' },
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

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      <Header navigationItems={navigationItems} />
      <main>
        <Hero />
        <About />
        <Skills />
        <Projects />
        <Experience />
        <Blog />
        <Contact />
      </main>
      <Footer socialLinks={socialLinks} />
    </div>
  );
};

export default Home;
