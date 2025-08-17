/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: 'none',
            color: '#374151',
            a: {
              color: '#2563eb',
              '&:hover': {
                color: '#1d4ed8',
              },
            },
            'h1, h2, h3, h4, h5, h6': {
              color: '#111827',
              fontWeight: '700',
              lineHeight: '1.25',
            },
            h1: {
              fontSize: '2.25rem',
              marginTop: '1rem',
              marginBottom: '0.5rem',
            },
            h2: {
              fontSize: '1.875rem',
              marginTop: '0.75rem',
              marginBottom: '0.375rem',
            },
            h3: {
              fontSize: '1.5rem',
              marginTop: '0.75rem',
              marginBottom: '0.375rem',
            },
            'p, ul, ol': {
              marginTop: '0.5rem',
              marginBottom: '0.5rem',
            },
            'ul, ol': {
              paddingLeft: '1.625rem',
            },
            li: {
              marginTop: '0.125rem',
              marginBottom: '0.125rem',
            },
            'li > p': {
              marginTop: '0.25rem',
              marginBottom: '0.25rem',
            },
            'li > ul, li > ol': {
              marginTop: '0.25rem',
              marginBottom: '0.25rem',
            },
            'li > pre': {
              marginTop: '0.25rem',
              marginBottom: '0.25rem',
              display: 'inline-block',
              width: '100%',
            },
            'li > code': {
              display: 'inline',
            },
            blockquote: {
              borderLeftColor: '#3b82f6',
              borderLeftWidth: '4px',
              paddingLeft: '1rem',
              fontStyle: 'italic',
              color: '#6b7280',
              backgroundColor: '#f8fafc',
              borderRadius: '0.375rem',
              padding: '1rem',
              margin: '0.75rem 0',
            },
            code: {
              color: '#1f2937',
              backgroundColor: '#f3f4f6',
              padding: '0.125rem 0.375rem',
              borderRadius: '0.375rem',
              fontSize: '0.875em',
              fontWeight: '500',
              border: '1px solid #e5e7eb',
            },
            'pre code': {
              backgroundColor: 'transparent',
              padding: '0',
              color: '#e5e7eb',
            },
            pre: {
              backgroundColor: '#1f2937',
              color: '#e5e7eb',
              padding: '1rem',
              borderRadius: '0.5rem',
              overflow: 'auto',
              fontSize: '0.875rem',
              lineHeight: '1.5',
              margin: '0.5rem 0',
            },
            'li pre': {
              margin: '0.25rem 0',
            },
            img: {
              borderRadius: '0.5rem',
              margin: '1rem auto',
            },
            table: {
              fontSize: '0.875rem',
              lineHeight: '1.25rem',
            },
            'thead th': {
              backgroundColor: '#f9fafb',
              borderBottom: '1px solid #e5e7eb',
              padding: '0.75rem',
              fontWeight: '600',
            },
            'tbody td': {
              borderBottom: '1px solid #f3f4f6',
              padding: '0.75rem',
            },
            hr: {
              borderColor: '#e5e7eb',
              margin: '1rem 0',
            },
          },
        },
        dark: {
          css: {
            color: '#d1d5db',
            a: {
              color: '#60a5fa',
              '&:hover': {
                color: '#93c5fd',
              },
            },
            'h1, h2, h3, h4, h5, h6': {
              color: '#f9fafb',
            },
            blockquote: {
              borderLeftColor: '#60a5fa',
              color: '#9ca3af',
              backgroundColor: '#1f2937',
            },
            code: {
              color: '#e5e7eb',
              backgroundColor: '#374151',
              border: '1px solid #4b5563',
            },
            pre: {
              backgroundColor: '#111827',
              color: '#e5e7eb',
            },
            'thead th': {
              backgroundColor: '#374151',
              borderBottom: '1px solid #4b5563',
            },
            'tbody td': {
              borderBottom: '1px solid #374151',
            },
            hr: {
              borderColor: '#374151',
            },
          },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
