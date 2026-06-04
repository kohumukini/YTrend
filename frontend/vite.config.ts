import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  define: {
    global: "globalThis",
  }, 
  optimizeDeps: {
    include: ['react-plotly.js', 'plotly.js']
  }, 
  ssr: {
    noExternal: ['plotly.js', 'react-plotly.js' ]
  }
})
