import React from 'react';
import { Header, Footer } from '../components/layout';
import { Hero } from '../components/sections';
import type { NavigationItem, SocialLink } from '../types';

const Home: React.FC = () => {
  const navigationItems: NavigationItem[] = [
    { label: 'About', href: '#about' },
    { label: 'Projects', href: '#projects' },
    { label: 'Skills', href: '#skills' },
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
        {/* Additional sections will be added here */}
        <section id="about" className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
              About Me
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 text-center max-w-3xl mx-auto">
              This section will contain information about Tyler Webb and his
              background.
            </p>
          </div>
        </section>
      </main>
      <Footer socialLinks={socialLinks} />
    </div>
  );
};

export default Home;
