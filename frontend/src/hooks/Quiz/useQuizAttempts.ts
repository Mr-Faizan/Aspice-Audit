import type { Quiz } from "@/types/quiz"

const MAX_ATTEMPTS = 3

interface UseQuizAttemptsReturn {
  attemptCount: number
  maxAttempts: number
  canAttempt: boolean
  attemptsRemaining: number
  isMaxAttemptsReached: boolean
}

const useQuizAttempts = (quiz?: Quiz | null): UseQuizAttemptsReturn => {
  const attemptCount = quiz?.attemptCount ?? 0
  const maxAttempts = quiz?.maxAttempts ?? MAX_ATTEMPTS
  const canAttempt = attemptCount < maxAttempts
  const attemptsRemaining = Math.max(0, maxAttempts - attemptCount)
  const isMaxAttemptsReached = attemptCount >= maxAttempts

  return { attemptCount, maxAttempts, canAttempt, attemptsRemaining, isMaxAttemptsReached }
}

export default useQuizAttempts
