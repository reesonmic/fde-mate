/**
 * Local storage helper with type safety
 */

const PREFIX = 'fde_'

/**
 * Get item from localStorage
 */
export function getItem<T>(key: string): T | null {
  const fullKey = PREFIX + key
  const value = localStorage.getItem(fullKey)
  if (value === null) return null

  try {
    return JSON.parse(value) as T
  } catch {
    return value as unknown as T
  }
}

/**
 * Set item in localStorage
 */
export function setItem<T>(key: string, value: T): void {
  const fullKey = PREFIX + key
  const serialized = typeof value === 'string' ? value : JSON.stringify(value)
  localStorage.setItem(fullKey, serialized)
}

/**
 * Remove item from localStorage
 */
export function removeItem(key: string): void {
  const fullKey = PREFIX + key
  localStorage.removeItem(fullKey)
}

/**
 * Clear all items with prefix
 */
export function clearAll(): void {
  const keys = Object.keys(localStorage)
  keys.forEach((key) => {
    if (key.startsWith(PREFIX)) {
      localStorage.removeItem(key)
    }
  })
}

/**
 * Check if key exists
 */
export function hasItem(key: string): boolean {
  const fullKey = PREFIX + key
  return localStorage.getItem(fullKey) !== null
}