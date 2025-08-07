import React, { useState } from 'react';
import Button from './Button';
import { apiService } from '../../services/api';
import { validateEmail } from '../../utils/validation';

interface NewsletterSignupProps {
  className?: string;
  title?: string;
  description?: string;
  placeholder?: string;
  buttonText?: string;
}

export const NewsletterSignup: React.FC<NewsletterSignupProps> = ({
  className = '',
  title = 'Stay Updated',
  description = 'Get notified when I publish new articles about web development, technology trends, and industry insights.',
  placeholder = 'Enter your email',
  buttonText = 'Subscribe',
}) => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{
    type: 'success' | 'error';
    text: string;
  } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email.trim()) {
      setMessage({ type: 'error', text: 'Please enter your email address.' });
      return;
    }

    if (!validateEmail(email)) {
      setMessage({
        type: 'error',
        text: 'Please enter a valid email address.',
      });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const response = await apiService.subscribeToNewsletter({
        email: email.trim(),
      });

      if (response.error) {
        setMessage({ type: 'error', text: response.error });
      } else {
        setMessage({
          type: 'success',
          text: 'Successfully subscribed! Check your email for confirmation.',
        });
        setEmail('');
      }
    } catch {
      setMessage({
        type: 'error',
        text: 'Failed to subscribe. Please try again.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`bg-white dark:bg-gray-700 rounded-lg p-8 text-center shadow-sm ${className}`}
    >
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        {title}
      </h3>
      <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-2xl mx-auto">
        {description}
      </p>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto"
      >
        <input
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          placeholder={placeholder}
          disabled={loading}
          className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <Button
          type="submit"
          variant="primary"
          disabled={loading}
          className="whitespace-nowrap"
        >
          {loading ? 'Subscribing...' : buttonText}
        </Button>
      </form>

      {message && (
        <div
          className={`mt-4 p-3 rounded-lg text-sm ${
            message.type === 'success'
              ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
              : 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
          }`}
        >
          {message.text}
        </div>
      )}
    </div>
  );
};
