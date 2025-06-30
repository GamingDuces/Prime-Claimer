import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
// This Vite configuration sets up a React project with a development server
// running on port 5173. It also proxies API requests to a backend server running on port 8000.