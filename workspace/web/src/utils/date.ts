import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.locale('zh-cn')
dayjs.extend(relativeTime)

/**
 * Format date to standard format
 */
export function formatDate(date: string | Date, format: string = 'YYYY-MM-DD'): string {
  return dayjs(date).format(format)
}

/**
 * Format date with time
 */
export function formatDateTime(date: string | Date): string {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

/**
 * Get relative time (e.g., "3 days ago")
 */
export function formatRelativeTime(date: string | Date): string {
  return dayjs(date).fromNow()
}

/**
 * Check if date is today
 */
export function isToday(date: string | Date): boolean {
  return dayjs(date).isSame(dayjs(), 'day')
}

/**
 * Check if date is overdue
 */
export function isOverdue(date: string | Date): boolean {
  return dayjs(date).isBefore(dayjs(), 'day')
}

/**
 * Get days until deadline
 */
export function getDaysUntil(date: string | Date): number {
  return dayjs(date).diff(dayjs(), 'day')
}