import React from 'react';
import type { CardProps } from '../../types';

const Card: React.FC<CardProps> = ({
  title,
  description,
  image,
  link,
  placeholderType = 'default',
  children,
  className = '',
}) => {
  const renderPlaceholder = () => {
    const baseClasses = 'w-full h-full flex items-center justify-center';

    switch (placeholderType) {
      case 'project':
        return (
          <div
            className={`${baseClasses} bg-gradient-to-br from-blue-500 to-purple-600`}
          >
            <div className="text-center text-white">
              <div className="text-4xl mb-2">💻</div>
              <div className="text-sm font-medium">Project Image</div>
            </div>
          </div>
        );

      case 'blog':
        return (
          <div
            className={`${baseClasses} bg-gradient-to-br from-green-500 to-teal-600`}
          >
            <div className="text-center text-white">
              <div className="text-4xl mb-2">📝</div>
              <div className="text-sm font-medium">Blog Post</div>
            </div>
          </div>
        );

      case 'value':
        return (
          <div
            className={`${baseClasses} bg-gradient-to-br from-orange-500 to-red-600`}
          >
            <div className="text-center text-white">
              <div className="text-4xl mb-2">⭐</div>
              <div className="text-sm font-medium">Core Value</div>
            </div>
          </div>
        );

      default:
        return (
          <div
            className={`${baseClasses} bg-gradient-to-br from-gray-500 to-gray-600`}
          >
            <div className="text-center text-white">
              <div className="text-4xl mb-2">📄</div>
              <div className="text-sm font-medium">Content</div>
            </div>
          </div>
        );
    }
  };

  const cardContent = (
    <div
      className={`bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden ${className}`}
    >
      <div className="aspect-video overflow-hidden">
        {image ? (
          <img
            src={image}
            alt={title || 'Card image'}
            className="w-full h-full object-cover"
            loading="lazy"
          />
        ) : (
          renderPlaceholder()
        )}
      </div>
      <div className="p-6">
        {title && (
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {title}
          </h3>
        )}
        {description && (
          <p className="text-gray-600 dark:text-gray-300 mb-4">{description}</p>
        )}
        {children}
      </div>
    </div>
  );

  if (link) {
    return (
      <a
        href={link}
        className="block hover:transform hover:scale-105 transition-transform duration-200"
      >
        {cardContent}
      </a>
    );
  }

  return cardContent;
};

export default Card;
