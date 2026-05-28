import { useEffect, useRef, useState } from "react"
import { useNavigate } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { AlertTriangle, ArrowLeft } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { QuizHeader } from "@/components/Quiz/QuizHeader"
import { QuizQuestionCard } from "@/components/Quiz/QuizQuestionCard"
import { QuizQuestionProgress } from "@/components/Quiz/QuizQuestionProgress"
import useQuizAttempts from "@/hooks/Quiz/useQuizAttempts"
import useQuizTimer from "@/hooks/Quiz/useQuizTimer"
import { getQuizById } from "@/lib/quiz/mock-data"
import type { Answer, QuizResult } from "@/types/quiz"

interface TakeQuizProps {
  quizId: string
}

function LoadingState() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-24 w-full rounded-xl" />
      <Skeleton className="h-64 w-full rounded-xl" />
      <Skeleton className="h-16 w-full rounded-xl" />
    </div>
  )
}

function ErrorState({ message, onBack }: { message: string; onBack: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4 text-center">
      <AlertTriangle className="h-10 w-10 text-destructive" />
      <p className="text-muted-foreground">{message}</p>
      <Button variant="outline" onClick={onBack} className="gap-1.5">
        <ArrowLeft className="h-4 w-4" /> Back to Audits
      </Button>
    </div>
  )
}

export function TakeQuiz({ quizId }: TakeQuizProps) {
  const navigate = useNavigate()
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Answer[]>([])
  const [startedAt] = useState(new Date().toISOString())
  const isSubmittingRef = useRef(false)

  const { data: quiz, isLoading } = useQuery({
    queryKey: ["quizzes", "detail", quizId],
    queryFn: async () => getQuizById(quizId) ?? null,
    enabled: !!quizId,
  })

  const { isMaxAttemptsReached, attemptCount } = useQuizAttempts(quiz)

  const { timeRemaining, formattedTime, startTimer, isRunning, isTimeUp } = useQuizTimer({
    timeLimitInMinutes: quiz?.timeLimit ?? 10,
  })

  const questions = quiz?.questions ?? []

  // start timer once quiz loads
  useEffect(() => {
    if (quiz && !isRunning && !isTimeUp) {
      startTimer()
    }
  }, [quiz, isRunning, isTimeUp, startTimer])

  const handleSubmit = () => {
    if (isSubmittingRef.current) return
    isSubmittingRef.current = true

    // simulate submitting: calculate score and navigate to result with a mock attempt id
    const correctCount = answers.filter((a) => {
      const q = questions.find((q) => q.id === a.questionId)
      return q?.correctAnswer === a.selectedAnswer
    }).length

    const score = questions.length > 0 ? (correctCount / questions.length) * 100 : 0
    const passed = score >= (quiz?.passingScore ?? 70)

    // create a transient mock result and store it in memory for the result page
    const resultId = `result-${Date.now()}`
    sessionStorage.setItem(
      resultId,
      JSON.stringify({
        id: resultId,
        userId: "current-user",
        quizId: quizId,
        answers,
        score,
        totalQuestions: questions.length,
        correctAnswers: correctCount,
        passed,
        startedAt,
        completedAt: new Date().toISOString(),
        quiz: quiz!,
        percentage: score,
      } satisfies QuizResult),
    )

    navigate({
      to: "/quizzes/$quizId/result/$resultId",
      params: { quizId, resultId },
    })
  }

  // auto-submit when time is up
  useEffect(() => {
    if (isTimeUp && !isSubmittingRef.current) {
      handleSubmit()
    }
  }, [isTimeUp])

  const handleAnswerChange = (questionId: string, selectedAnswer: string) => {
    setAnswers((prev) => {
      const existing = prev.findIndex((a) => a.questionId === questionId)
      if (existing >= 0) {
        const updated = [...prev]
        updated[existing] = { questionId, selectedAnswer }
        return updated
      }
      return [...prev, { questionId, selectedAnswer }]
    })
  }

  if (isLoading) return <LoadingState />

  if (!quiz) {
    return (
      <ErrorState
        message="Quiz not found. It may have been removed or is unavailable."
        onBack={() => navigate({ to: "/quizzes" })}
      />
    )
  }

  if (isMaxAttemptsReached) {
    return (
      <div className="flex flex-col items-center justify-center py-16 gap-4 text-center">
        <AlertTriangle className="h-10 w-10 text-destructive" />
        <div>
          <p className="font-semibold text-foreground">Maximum Attempts Reached</p>
          <p className="text-sm text-muted-foreground mt-1">
            You have used all {attemptCount} attempts for this quiz.
          </p>
        </div>
        <Button variant="outline" onClick={() => navigate({ to: "/quizzes" })} className="gap-1.5">
          <ArrowLeft className="h-4 w-4" /> Back to Audits
        </Button>
      </div>
    )
  }

  const isLastQuestion = currentQuestionIndex === questions.length - 1
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100
  const currentQuestion = questions[currentQuestionIndex]
  const currentAnswer = answers.find((a) => a.questionId === currentQuestion?.id)

  return (
    <div className="max-w-3xl mx-auto">
      <QuizHeader
        title={quiz.title}
        formattedTime={formattedTime}
        timeRemaining={timeRemaining}
        currentQuestionIndex={currentQuestionIndex}
        totalQuestions={questions.length}
        progress={progress}
      />

      {currentQuestion && (
        <QuizQuestionCard
          currentQuestion={currentQuestion}
          currentAnswer={currentAnswer}
          isLastQuestion={isLastQuestion}
          currentQuestionIndex={currentQuestionIndex}
          totalQuestions={questions.length}
          isSubmitting={false}
          onAnswerChange={handleAnswerChange}
          onPrevious={() => setCurrentQuestionIndex((p) => Math.max(0, p - 1))}
          onNext={() => setCurrentQuestionIndex((p) => Math.min(questions.length - 1, p + 1))}
          onSubmit={handleSubmit}
        />
      )}

      <QuizQuestionProgress
        questions={questions}
        answers={answers}
        currentQuestionIndex={currentQuestionIndex}
        setCurrentQuestionIndex={setCurrentQuestionIndex}
      />
    </div>
  )
}
