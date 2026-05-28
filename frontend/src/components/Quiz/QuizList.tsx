import { useState } from "react"
import { useNavigate } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { BookOpen, Clock, Play, Search } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Skeleton } from "@/components/ui/skeleton"
import { MaxAttemptsModal, StartQuizModal } from "@/components/Quiz/modals/QuizModals"
import useQuizAttempts from "@/hooks/Quiz/useQuizAttempts"
import { MOCK_QUIZZES } from "@/lib/quiz/mock-data"
import type { Difficulty, Quiz } from "@/types/quiz"

const DIFFICULTY_COLORS: Record<Difficulty, string> = {
  easy: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
  hard: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
}

function QuizCardSkeleton() {
  return (
    <Card>
      <CardContent className="pt-6 space-y-3">
        <div className="flex justify-between">
          <Skeleton className="h-5 w-24" />
          <Skeleton className="h-5 w-16" />
        </div>
        <Skeleton className="h-5 w-3/4" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-2/3" />
        <div className="flex gap-4 pt-2">
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-4 w-16" />
        </div>
      </CardContent>
      <CardFooter>
        <Skeleton className="h-9 w-full" />
      </CardFooter>
    </Card>
  )
}

export function QuizList() {
  const [search, setSearch] = useState("")
  const [selectedDifficulty, setSelectedDifficulty] = useState<Difficulty | "all">("all")
  const [startQuizInfo, setStartQuizInfo] = useState<Quiz | null>(null)
  const navigate = useNavigate()

  const { data: quizzes = [], isLoading } = useQuery({
    queryKey: ["quizzes", "list"],
    queryFn: async () => MOCK_QUIZZES,
    staleTime: 5 * 60 * 1000,
  })

  const { canAttempt, isMaxAttemptsReached, attemptsRemaining, attemptCount } =
    useQuizAttempts(startQuizInfo)

  const filtered = quizzes.filter((q) => {
    const matchesSearch =
      !search ||
      q.title.toLowerCase().includes(search.toLowerCase()) ||
      q.description.toLowerCase().includes(search.toLowerCase())
    const matchesDifficulty = selectedDifficulty === "all" || q.difficulty === selectedDifficulty
    return matchesSearch && matchesDifficulty
  })

  const handleStart = () => {
    if (startQuizInfo) {
      navigate({ to: "/quizzes/$quizId", params: { quizId: startQuizInfo.id } })
      setStartQuizInfo(null)
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">ASPICE Audits</h1>
        <p className="text-muted-foreground">
          Select a process area to begin your compliance assessment.
        </p>
      </div>

      {/* filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search audits..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
        <div className="flex gap-2 flex-wrap">
          {(["all", "easy", "medium", "hard"] as const).map((d) => (
            <button
              key={d}
              type="button"
              onClick={() => setSelectedDifficulty(d)}
              className={`px-3 py-1.5 rounded-md text-sm font-medium border transition-colors ${
                selectedDifficulty === d
                  ? "bg-primary text-primary-foreground border-primary"
                  : "border-border bg-background hover:bg-muted text-foreground"
              }`}
            >
              {d === "all" ? "All Levels" : d.charAt(0).toUpperCase() + d.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* grid */}
      {isLoading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => <QuizCardSkeleton key={i} />)}
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <BookOpen className="h-12 w-12 text-muted-foreground/40 mb-3" />
          <p className="text-muted-foreground">No audits found matching your filters.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((quiz) => (
            <Card
              key={quiz.id}
              className="flex flex-col transition-all duration-200 hover:-translate-y-1 hover:shadow-md"
            >
              <CardContent className="pt-6 flex-1">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide bg-muted px-2 py-0.5 rounded">
                    {quiz.category}
                  </span>
                  <span
                    className={`text-xs font-medium px-2 py-0.5 rounded capitalize ${DIFFICULTY_COLORS[quiz.difficulty]}`}
                  >
                    {quiz.difficulty}
                  </span>
                </div>

                <h3 className="font-semibold text-foreground mb-1.5 leading-snug">{quiz.title}</h3>
                <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
                  {quiz.description}
                </p>

                <div className="flex gap-4 text-sm text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <BookOpen className="h-3.5 w-3.5" />
                    {quiz.questions.length} questions
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="h-3.5 w-3.5" />
                    {quiz.timeLimit} min
                  </span>
                </div>

                {quiz.attemptCount != null && quiz.maxAttempts != null && (
                  <div className="mt-3">
                    <Badge
                      variant={quiz.attemptCount >= quiz.maxAttempts ? "destructive" : "secondary"}
                      className="text-xs"
                    >
                      {quiz.attemptCount}/{quiz.maxAttempts} attempts used
                    </Badge>
                  </div>
                )}
              </CardContent>

              <CardFooter className="pt-0">
                <Button
                  className="w-full gap-1.5"
                  onClick={() => setStartQuizInfo(quiz)}
                  disabled={quiz.attemptCount != null && quiz.maxAttempts != null && quiz.attemptCount >= quiz.maxAttempts}
                >
                  <Play className="h-4 w-4" />
                  Start Audit
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}

      <MaxAttemptsModal
        isOpen={isMaxAttemptsReached && !!startQuizInfo}
        attemptCount={attemptCount}
        onClose={() => setStartQuizInfo(null)}
      />
      <StartQuizModal
        isOpen={!!startQuizInfo && canAttempt}
        quizTitle={startQuizInfo?.title ?? ""}
        questionCount={startQuizInfo?.questions.length ?? 0}
        timeLimit={startQuizInfo?.timeLimit ?? 0}
        attemptsRemaining={attemptsRemaining}
        onClose={() => setStartQuizInfo(null)}
        onConfirm={handleStart}
      />
    </div>
  )
}
