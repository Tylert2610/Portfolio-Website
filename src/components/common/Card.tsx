import React from 'react';
import type { CardProps } from '../../types';

const Card: React.FC<CardProps> = ({
  title,
  description,
  image,
  link,
  children,
  className = '',
}) => {
  const cardContent = (
    <div
      className={`bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden ${className}`}
    >
      {image && (
        <div className="aspect-video overflow-hidden">
          <img
            src={image}
            alt={title || 'Card image'}
            className="w-full h-full object-cover"
          />
        </div>
      )}
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
