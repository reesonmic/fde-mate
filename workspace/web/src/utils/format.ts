import { format } from 'date-fns'

/**
 * Format a number as currency
 */
export function formatCurrency(value: number, currency: string = 'CNY'): string {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency,
  }).format(value)
}

/**
 * Format a number with locale
 */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat('zh-CN').format(value)
}

/**
 * Format a percentage
 */
export function formatPercent(value: number): string {
  return `${Math.round(value)}%`
}

/**
 * Truncate text with ellipsis
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength - 3) + '...'
}