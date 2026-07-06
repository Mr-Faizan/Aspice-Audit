import { cn } from "@/lib/utils"
import type { Answer, Question } from "@/types/quiz"

interface QuizQuestionProgressProps {
  questions: Question[]
  answers: Answer[]
  currentQuestionIndex: number
  setCurrentQuestionIndex: (idx: number) => void
}

export function QuizQuestionProgress({
  questions,
  answers,
  currentQuestionIndex,
  setCurrentQuestionIndex,
}: QuizQuestionProgressProps) {
  return (
    <div className="rounded-xl border bg-card p-4 mt-4 shadow-sm">
      <p className="text-xs text-muted-foreground mb-2">Question Progress</p>
      <div className="flex flex-wrap gap-1.5">
        {questions.map((q, idx) => {
          const isAnswered = answers.some((a) => a.questionId === q.id)
          const isCurrent = idx === currentQuestionIndex

          return (
            <button
              key={q.id}
              type="button"
              onClick={() => setCurrentQuestionIndex(idx)}
              className={cn(
                "h-8 w-8 rounded-md text-xs font-medium border transition-colors",
                isCurrent && "bg-primary text-primary-foreground border-primary",
                !isCurrent && isAnswered && "bg-primary/20 border-primary/40 text-primary",
                !isCurrent && !isAnswered && "bg-muted border-border text-muted-foreground hover:bg-accent",
              )}
            >
              {idx + 1}
            </button>
          )
        })}
      </div>
    </div>
  )
}
