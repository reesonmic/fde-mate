import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    include: ['tests/**/*.{test,spec}.{js,ts}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@apis': path.resolve(__dirname, 'src/apis'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@stores': path.resolve(__dirname, 'src/stores'),
      '@types': path.resolve(__dirname, 'src/types'),
    },
  },
})