import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useMainStore } from '@/stores/main'
import { useStyleStore } from '@/stores/style'
import { darkModeKey, styleKey } from '@/styles/config'

import './css/main.css'

/* Init Pinia */
const pinia = createPinia()

/* Create Vue app */
createApp(App).use(router).use(pinia).mount('#app')

/* Init Pinia stoes */
const mainStore = useMainStore(pinia)
const styleStore = useStyleStore(pinia)

/* Fetch sample data */
mainStore.fetch('clients')
mainStore.fetch('history')

// /* App style */
styleStore.setStyle(localStorage[styleKey] ?? 'basic')

/* Dark mode */
if (
  (!localStorage[darkModeKey] &&
    window.matchMedia('(prefers-color-scheme: dark)').matches) ||
  localStorage[darkModeKey] === '1'
) {
  styleStore.setDarkMode(true)
}
