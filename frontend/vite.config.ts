import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// @ts-ignore
import Components from 'unplugin-vue-components/vite'
// @ts-ignore
import { BootstrapVue3Resolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({
      dts: true,
      extensions: ['vue'],
      resolvers: [BootstrapVue3Resolver()],
      include: [/\.vue$/, /\.vue\?vue/],
      exclude: [/[\\/]node_modules[\\/]/, /[\\/]\.git[\\/]/],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: { '^/api': { target: 'http://backend:8000' } },
    open: false,
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
        @import "@/assets/scss/_variables.scss";
        @import "bootstrap/scss/bootstrap.scss";
        `,
      },
    },
  },
})
