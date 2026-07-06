import { useCallback, useEffect, useRef, useState } from "react"

interface UseQuizTimerProps {
  timeLimitInMinutes: number
}

interface UseQuizTimerReturn {
  timeRemaining: number
  formattedTime: string
  startTimer: () => void
  isRunning: boolean
  isTimeUp: boolean
}

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`
}

const useQuizTimer = ({ timeLimitInMinutes }: UseQuizTimerProps): UseQuizTimerReturn => {
  const [timeRemaining, setTimeRemaining] = useState(timeLimitInMinutes * 60)
  const [isRunning, setIsRunning] = useState(false)
  const [isTimeUp, setIsTimeUp] = useState(false)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const startTimer = useCallback(() => {
    if (isRunning || timeRemaining <= 0) return
    setIsRunning(true)
  }, [isRunning, timeRemaining])

  useEffect(() => {
    if (!isRunning) return

    intervalRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(intervalRef.current!)
          setIsRunning(false)
          setIsTimeUp(true)
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(intervalRef.current!)
  }, [isRunning])

  return {
    timeRemaining,
    formattedTime: formatTime(timeRemaining),
    startTimer,
    isRunning,
    isTimeUp,
  }
}

export default useQuizTimer
