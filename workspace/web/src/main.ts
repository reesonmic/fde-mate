import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { setupAntd } from './plugins/antd'
import { setupAxiosInterceptors } from './apis/http'
import './styles/reset.css'
import './styles/theme.css'
import './styles/layout.css'
import './styles/copilot.css'
import './styles/pages.css'

async function bootstrap() {
  const app = createApp(App)
  const pinia = createPinia()
  app.use(pinia)
  app.use(router)
  setupAntd(app)
  setupAxiosInterceptors()
  app.mount('#app')
}

bootstrap()
