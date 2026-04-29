import type { Router } from 'vue-router'
import { useAuthStore } from '@stores/auth'

export function setupGuards(router: Router) {
  router.beforeEach((to, _from, next) => {
    const auth = useAuthStore()
    const requiresAuth = to.meta.requiresAuth !== false

    if (requiresAuth && !auth.isLoggedIn) {
      return next({ path: '/login', query: { redirect: to.fullPath } })
    }
    if (to.path === '/login' && auth.isLoggedIn) {
      return next('/dashboard')
    }

    const title = to.meta.title as string
    document.title = title ? `${title} · FDE 工作台` : 'FDE 工作台'

    next()
  })
}
