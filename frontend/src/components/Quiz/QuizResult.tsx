import { useNavigate } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { ArrowLeft, CheckCircle, RefreshCw, XCircle } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"
import { QuestionBreakdown } from "@/components/Quiz/QuestionBreakdown"
import { getAttemptById } from "@/lib/quiz/mock-data"
import type { QuizResult as QuizResultType } from "@/types/quiz"

interface QuizResultProps {
  quizId: string
  resultId: string
}

export function QuizResult({ quizId, resultId }: QuizResultProps) {
  const navigate = useNavigate()

  const { data: result, isLoading } = useQuery({
    queryKey: ["quiz-results", resultId],
    queryFn: async (): Promise<QuizResultType | null> => {
      // check session storage first (fresh result from current session)
      const stored = sessionStorage.getItem(resultId)
      if (stored) return JSON.parse(stored) as QuizResultType

      // fall back to mock history attempts
      const attempt = getAttemptById(resultId)
      if (!attempt || !attempt.quiz) return null
      return { ...attempt, quiz: attempt.quiz, percentage: attempt.score } as QuizResultType
    },
    enabled: !!resultId,
  })

  if (isLoading) {
    return (
      <div className="max-w-3xl mx-auto space-y-4">
        <Skeleton className="h-40 w-full rounded-xl" />
        <Skeleton className="h-32 w-full rounded-xl" />
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    )
  }

  if (!result) {
    return (
      <div className="flex flex-col items-center justify-center py-16 gap-4 text-center">
        <XCircle className="h-10 w-10 text-destructive" />
        <p className="text-muted-foreground">Result not found.</p>
        <Button variant="outline" onClick={() => navigate({ to: "/quizzes" })}>
          Back to Audits
        </Button>
      </div>
    )
  }

  const { percentage, passed, quiz, correctAnswers, totalQuestions, answers } = result

  return (
    <div className="max-w-3xl mx-auto flex flex-col gap-5">
      {/* hero banner */}
      <div
        className={`rounded-xl p-8 text-center text-white ${
          passed
            ? "bg-gradient-to-br from-indigo-500 to-purple-600"
            : "bg-gradient-to-br from-pink-500 to-red-500"
        }`}
      >
        {passed ? (
          <CheckCircle className="h-16 w-16 mx-auto mb-3 opacity-90" />
        ) : (
          <XCircle className="h-16 w-16 mx-auto mb-3 opacity-90" />
        )}
        <h1 className="text-3xl font-bold mb-1">
          {passed ? "Congratulations!" : "Better Luck Next Time"}
        </h1>
        <p className="text-white/80 text-base">
          {passed ? "You passed the audit!" : "You did not meet the passing threshold."}
        </p>
      </div>

      {/* stats card */}
      <Card>
        <CardContent className="pt-6">
          <h2 className="text-lg font-semibold text-foreground mb-1">{quiz?.title}</h2>
          <Separator className="my-3" />
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">Score</p>
              <p className="text-3xl font-bold text-primary">{percentage?.toFixed(0)}%</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">
                Correct
              </p>
              <p className="text-3xl font-bold text-foreground">
                {correctAnswers}{" "}
                <span className="text-lg text-muted-foreground">/ {totalQuestions}</span>
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">
                Questions
              </p>
              <p className="text-3xl font-bold text-foreground">{quiz?.questions.length}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Status</p>
              <Badge variant={passed ? "default" : "destructive"} className="text-sm px-3 py-0.5">
                {passed ? "Passed" : "Failed"}
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* question breakdown */}
      <QuestionBreakdown questions={quiz?.questions} answers={answers} />

      {/* action buttons */}
      <div className="flex flex-col sm:flex-row gap-3">
        <Button variant="outline" onClick={() => navigate({ to: "/quizzes" })} className="gap-1.5">
          <ArrowLeft className="h-4 w-4" />
          Back to Audits
        </Button>
        <Button
          onClick={() => navigate({ to: "/quizzes/$quizId", params: { quizId } })}
          className="gap-1.5"
        >
          <RefreshCw className="h-4 w-4" />
          Retake Audit
        </Button>
      </div>
    </div>
  )
}
