<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Form, Input, Button, message } from 'ant-design-vue'
import { useAuthStore } from '@stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const formState = ref({ username: '', password: '' })
const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true
  try {
    await auth.login(formState.value.username, formState.value.password)
    message.success('登录成功')
    const redirect = (route.query.redirect as string) || '/dashboard'
    router.push(redirect)
  } catch {
    message.error('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>FDE 工作台</h1>
        <p>Forward Deployed Engineer Workbench</p>
      </div>
      <Form @submit.prevent="handleSubmit">
        <Form.Item>
          <Input v-model:value="formState.username" placeholder="用户名" size="large" />
        </Form.Item>
        <Form.Item>
          <Input.Password v-model:value="formState.password" placeholder="密码" size="large" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" size="large" block :loading="loading" html-type="submit">
            登录
          </Button>
        </Form.Item>
      </Form>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-container {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.login-header {
  text-align: center;
  margin-bottom: 32px;
}
.login-header h1 {
  font-size: 24px;
  margin-bottom: 8px;
}
.login-header p {
  font-size: 14px;
  color: #666;
}
</style>
