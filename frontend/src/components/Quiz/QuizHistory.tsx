import { useNavigate } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { CheckCircle, Eye, History, XCircle } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { MOCK_ATTEMPTS } from "@/lib/quiz/mock-data"

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

export function QuizHistory() {
  const navigate = useNavigate()

  const { data: attempts = [], isLoading } = useQuery({
    queryKey: ["quiz-attempts", "user"],
    queryFn: async () => MOCK_ATTEMPTS,
    staleTime: 2 * 60 * 1000,
  })

  if (isLoading) {
    return (
      <div className="flex flex-col gap-6">
        <div>
          <Skeleton className="h-8 w-48 mb-2" />
          <Skeleton className="h-4 w-72" />
        </div>
        {Array.from({ length: 3 }).map((_, i) => (
          <Skeleton key={i} className="h-24 w-full rounded-xl" />
        ))}
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Audit History</h1>
        <p className="text-muted-foreground">Review your past audit attempts and results.</p>
      </div>

      {attempts.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 gap-3 text-center">
          <History className="h-12 w-12 text-muted-foreground/40" />
          <p className="text-muted-foreground">You haven&apos;t taken any audits yet.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {attempts.map((attempt) => {
            const { id, score, quizId, completedAt, correctAnswers, totalQuestions, quiz } = attempt
            const passed = score >= 70

            return (
              <Card
                key={id}
                className="cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
                onClick={() =>
                  navigate({
                    to: "/quizzes/$quizId/result/$resultId",
                    params: { quizId, resultId: id },
                  })
                }
              >
                <CardContent className="pt-5">
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-foreground truncate">
                        {quiz?.title ?? "Untitled Audit"}
                      </h3>
                      <p className="text-sm text-muted-foreground mt-0.5">
                        Completed {formatDate(completedAt)}
                      </p>
                    </div>

                    <div className="flex items-center gap-4 flex-wrap">
                      {/* score pill */}
                      <div
                        className={`rounded-lg px-4 py-2 text-center min-w-[80px] ${
                          passed
                            ? "bg-green-100 dark:bg-green-900/30"
                            : "bg-red-100 dark:bg-red-900/30"
                        }`}
                      >
                        <p
                          className={`text-2xl font-bold ${
                            passed
                              ? "text-green-700 dark:text-green-400"
                              : "text-red-700 dark:text-red-400"
                          }`}
                        >
                          {score.toFixed(0)}%
                        </p>
                        <p className="text-xs text-muted-foreground">Score</p>
                      </div>

                      {/* status */}
                      <div className="flex flex-col items-center gap-1.5">
                        <Badge
                          variant={passed ? "default" : "destructive"}
                          className="flex items-center gap-1"
                        >
                          {passed ? (
                            <CheckCircle className="h-3 w-3" />
                          ) : (
                            <XCircle className="h-3 w-3" />
                          )}
                          {passed ? "Passed" : "Failed"}
                        </Badge>
                        <p className="text-xs text-muted-foreground">
                          {correctAnswers} / {totalQuestions} correct
                        </p>
                      </div>

                      <Badge variant="outline" className="gap-1">
                        <Eye className="h-3 w-3" />
                        View Details
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}
