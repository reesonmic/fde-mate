import { App } from 'vue'
import {
  DashboardOutlined,
  ProjectOutlined,
  TeamOutlined,
  FileOutlined,
  BookOutlined,
  MessageOutlined,
  SettingOutlined,
  SearchOutlined,
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  CheckOutlined,
  CloseOutlined,
  MoreOutlined,
  UserOutlined,
  CalendarOutlined,
  BellOutlined,
} from '@ant-design/icons-vue'

/**
 * Setup Ant Design Icons
 */
export function setupIcons(app: App) {
  // Register icons globally
  app.component('DashboardOutlined', DashboardOutlined)
  app.component('ProjectOutlined', ProjectOutlined)
  app.component('TeamOutlined', TeamOutlined)
  app.component('FileOutlined', FileOutlined)
  app.component('BookOutlined', BookOutlined)
  app.component('MessageOutlined', MessageOutlined)
  app.component('SettingOutlined', SettingOutlined)
  app.component('SearchOutlined', SearchOutlined)
  app.component('PlusOutlined', PlusOutlined)
  app.component('EditOutlined', EditOutlined)
  app.component('DeleteOutlined', DeleteOutlined)
  app.component('CheckOutlined', CheckOutlined)
  app.component('CloseOutlined', CloseOutlined)
  app.component('MoreOutlined', MoreOutlined)
  app.component('UserOutlined', UserOutlined)
  app.component('CalendarOutlined', CalendarOutlined)
  app.component('BellOutlined', BellOutlined)
}