import { App } from 'vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

/**
 * Setup Ant Design Vue
 */
export function setupAntd(app: App) {
  app.use(Antd)
}