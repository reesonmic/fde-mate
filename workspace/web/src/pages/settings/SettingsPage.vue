<script setup lang="ts">
import { reactive } from 'vue'
import { Form, Input, Switch, Select, message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const formState = reactive({
  language: userStore.preferences.language,
  theme: userStore.settings.theme,
  notifications: { ...userStore.preferences.notifications },
})

const handleSave = () => {
  userStore.updatePreferences({
    language: formState.language,
    notifications: formState.notifications,
  })
  userStore.updateSettings({ theme: formState.theme })
  message.success('设置已保存')
}
</script>

<template>
  <div class="settings-page">
    <h2>系统设置</h2>

    <Form :model="formState" @finish="handleSave">
      <Form.Item label="语言">
        <Select v-model:value="formState.language">
          <Select.Option value="zh-CN">中文</Select.Option>
          <Select.Option value="en-US">English</Select.Option>
        </Select>
      </Form.Item>

      <Form.Item label="主题">
        <Select v-model:value="formState.theme">
          <Select.Option value="light">浅色</Select.Option>
          <Select.Option value="dark">深色</Select.Option>
        </Select>
      </Form.Item>

      <Form.Item label="邮件通知">
        <Switch v-model:checked="formState.notifications.email" />
      </Form.Item>

      <Form.Item label="短信通知">
        <Switch v-model:checked="formState.notifications.sms" />
      </Form.Item>

      <Form.Item label="推送通知">
        <Switch v-model:checked="formState.notifications.push" />
      </Form.Item>

      <Form.Item :wrapper-col="{ offset: 4 }">
        <Switch type="primary" @click="handleSave">保存设置</Switch>
      </Form.Item>
    </Form>
  </div>
</template>

<style scoped>
.settings-page h2 {
  margin-bottom: 24px;
}
</style>