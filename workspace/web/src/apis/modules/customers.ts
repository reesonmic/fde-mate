import { http } from '../http'
import type { Customer } from '@types/business'

export const customersApi = {
  list: (params = {}) => http.get<unknown, { items: Customer[]; total: number }>('/customers', { params }),
  get: (id: number) => http.get<unknown, Customer>(`/customers/${id}`),
  create: (data: any) => http.post<unknown, Customer>('/customers', data),
  update: (id: number, data: any) => http.put<unknown, Customer>(`/customers/${id}`, data),
  delete: (id: number) => http.delete<unknown, void>(`/customers/${id}`),
  getContacts: (id: number) => http.get<unknown, any[]>(`/customers/${id}/contacts`),
  addContact: (id: number, data: any) => http.post<unknown, any>(`/customers/${id}/contacts`, data),
  getOpportunities: (id: number) => http.get<unknown, any[]>(`/customers/${id}/opportunities`),
}
