import { useEffect, useState } from "react"

export function useDebounceValue<T>(
  initialValue: T,
  delay: number = 500,
): [T, T, (value: T) => void] {
  const [value, setValue] = useState<T>(initialValue)
  const [debouncedValue, setDebouncedValue] = useState<T>(initialValue)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return [value, debouncedValue, setValue]
}
