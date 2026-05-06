import { http } from '../http'
import type { CustomerDTO } from '@types/business'

export interface ContactDTO {
  id: number
  customer_id: number
  name: string
  title: string
  phone: string
  email: string
  gmt_create: string
}

export interface OpportunityDTO {
  id: number
  customer_id: number
  title: string
  stage: string
  amount: number
  close_at: string
  gmt_create: string
}

export const customersApi = {
  list: (params = {}) => http.get<unknown, { items: CustomerDTO[]; total: number }>('/customers', { params }),
  get: (id: number) => http.get<unknown, CustomerDTO>(`/customers/${id}`),
  create: (data: { name: string; industry?: string; scale?: string }) => http.post<unknown, CustomerDTO>('/customers', data),
  update: (id: number, data: { name?: string; industry?: string; scale?: string }) => http.put<unknown, CustomerDTO>(`/customers/${id}`, data),
  delete: (id: number) => http.delete<unknown, void>(`/customers/${id}`),
  getContacts: (id: number) => http.get<unknown, ContactDTO[]>(`/customers/${id}/contacts`),
  addContact: (id: number, data: { name: string; title?: string; phone?: string; email?: string }) => http.post<unknown, ContactDTO>(`/customers/${id}/contacts`, data),
  getOpportunities: (id: number) => http.get<unknown, OpportunityDTO[]>(`/customers/${id}/opportunities`),
}
