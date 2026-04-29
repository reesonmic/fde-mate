import { http } from '../http'

export const authApi = {
  login: (data: { username: string; password: string }) =>
    http.post<unknown, { accessToken: string; refreshToken: string; expiresIn: number }>('/auth/login', data),

  logout: () => http.post('/auth/logout'),

  getMe: () => http.get<unknown, { id: number; name: string; email: string; avatar?: string; roles: string[]; level: string }>('/auth/me'),

  refresh: (refreshToken: string) =>
    http.post<unknown, { accessToken: string; refreshToken: string; expiresIn: number }>('/auth/refresh', { refreshToken }),
}
