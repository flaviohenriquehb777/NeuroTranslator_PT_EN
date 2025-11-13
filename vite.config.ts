import { defineConfig } from 'vite'

export default defineConfig({
  root: 'web',
  build: {
    outDir: 'assets/js',
    emptyOutDir: false,
    lib: {
      entry: 'assets/ts/script-optimized.ts',
      name: 'NeuroTranslator',
      formats: ['iife'],
      fileName: () => 'script-optimized.js'
    },
    rollupOptions: {
      output: {
        inlineDynamicImports: true
      }
    }
  }
})