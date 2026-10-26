import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { cpSync } from 'node:fs'
export default defineConfig({
  plugins: [react(), { name: 'copy-readme-assets', closeBundle() { cpSync('assets','dist/assets',{recursive:true}) } }],
  base: './', build: { outDir: 'dist', rollupOptions: { onwarn(warning, warn) {
    if (warning.code === 'MODULE_LEVEL_DIRECTIVE' || warning.code === 'SOURCEMAP_ERROR') return
    warn(warning)
  } } }
})
