import { createApp } from 'vue'
import { createPinia } from 'pinia'
import BootstrapVue3 from 'bootstrap-vue-3'
import VueApexCharts from 'vue3-apexcharts'

import App from './App.vue'
import router from './router'

import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
// import 'bootstrap/dist/css/bootstrap.css'
import '@/assets/scss/_bootswatch.scss'
import 'bootstrap-icons/font/bootstrap-icons.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(BootstrapVue3)
app.use(VueApexCharts)

app.mount('#app')
