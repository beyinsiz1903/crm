import {defineConfig, loadEnv} from 'vite';
import react from '@vitejs/plugin-react';
import tailwind from '@tailwindcss/vite';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
export default defineConfig(({mode}) => {
  const env = {...loadEnv(mode, root, ''), ...process.env};
  return {
    plugins: [react(), tailwind()],
    resolve: {alias: {'@': path.join(root, 'src')}},
    define: {'process.env.REACT_APP_BACKEND_URL': JSON.stringify(env.REACT_APP_BACKEND_URL || '')},
    server: {port: Number(env.PORT || 5000), strictPort: true, allowedHosts: (env.DEV_ALLOWED_HOSTS || '').split(',').filter(Boolean), proxy: {'/api': 'http://127.0.0.1:8000'}},
    build: {outDir: 'build', assetsDir: 'static', sourcemap: false},
    test: {environment: 'node', include: ['src/**/*.test.{js,jsx}']},
  };
});
