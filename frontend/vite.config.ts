import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  server: {
    port: 5173,
    host: true, // Allow external connections
    proxy:
      mode === 'development'
        ? {
            // Proxy API requests to local backend during development mode only
            '/api': {
              target: 'http://localhost:8000',
              changeOrigin: true,
              secure: false,
            },
          }
        : undefined, // No proxy in production mode - use direct API calls
  },
}));
