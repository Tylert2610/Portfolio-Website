import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import type { NavigationItem } from '../../types';

interface HeaderProps {
  navigationItems?: NavigationItem[];
}

const Header: React.FC<HeaderProps> = ({ navigationItems = [] }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const renderNavigationItem = (item: NavigationItem, isMobile = false) => {
    const baseClasses = isMobile
      ? 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors'
      : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors';

    // Check if it's an internal route (starts with / and doesn't contain #)
    const isInternalRoute =
      item.href.startsWith('/') && !item.href.includes('#');

    if (isInternalRoute) {
      return (
        <Link
          key={item.href}
          to={item.href}
          className={baseClasses}
          onClick={() => isMobile && setIsMobileMenuOpen(false)}
        >
          {item.label}
        </Link>
      );
    }

    return (
      <a
        key={item.href}
        href={item.href}
        className={baseClasses}
        target={item.external ? '_blank' : undefined}
        rel={item.external ? 'noopener noreferrer' : undefined}
        onClick={() => isMobile && setIsMobileMenuOpen(false)}
      >
        {item.label}
      </a>
    );
  };

  return (
    <header className="bg-white dark:bg-gray-900 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link
              to="/"
              className="text-xl font-bold text-gray-900 dark:text-white hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
            >
              Tyler Webb
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navigationItems.map(item => renderNavigationItem(item))}
            {/* Admin Link - Only visible in development */}
            {import.meta.env.DEV && (
              <Link
                to="/admin"
                className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Admin
              </Link>
            )}
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={toggleMobileMenu}
              className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white focus:outline-none focus:text-gray-900 dark:focus:text-white"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {isMobileMenuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navigationItems.map(item => renderNavigationItem(item, true))}
              {/* Admin Link - Only visible in development */}
              {import.meta.env.DEV && (
                <Link
                  to="/admin"
                  className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 block px-3 py-2 rounded-md text-base font-medium transition-colors"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Admin
                </Link>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
