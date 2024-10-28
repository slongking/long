
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
const app = createApp (App)
const pinia = createPinia()
app.use(router as any)
app.use(pinia)
app.use(ElementPlus as any)
app.mount("#app")


