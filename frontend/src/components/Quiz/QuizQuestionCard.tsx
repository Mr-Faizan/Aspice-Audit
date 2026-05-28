import { CheckCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { Answer, Question } from "@/types/quiz"
import { cn } from "@/lib/utils"

interface QuizQuestionCardProps {
  currentQuestion: Question
  currentAnswer: Answer | undefined
  isLastQuestion: boolean
  currentQuestionIndex: number
  totalQuestions: number
  isSubmitting: boolean
  onAnswerChange: (questionId: string, selectedAnswer: string) => void
  onPrevious: () => void
  onNext: () => void
  onSubmit: () => void
}

export function QuizQuestionCard({
  currentQuestion,
  currentAnswer,
  isLastQuestion,
  currentQuestionIndex,
  isSubmitting,
  onAnswerChange,
  onPrevious,
  onNext,
  onSubmit,
}: QuizQuestionCardProps) {
  const selected = currentAnswer?.selectedAnswer

  return (
    <div className="rounded-xl border bg-card p-6 shadow-sm">
      <p className="text-sm text-muted-foreground mb-1">
        {currentQuestion.points} {currentQuestion.points === 1 ? "point" : "points"}
      </p>
      <h3 className="text-base font-semibold text-foreground mb-5">
        {currentQuestion.questionText ?? currentQuestion.text}
      </h3>

      <div className="space-y-2.5">
        {currentQuestion.options.map((option) => {
          const isSelected = selected === option.id
          return (
            <button
              key={option.id}
              type="button"
              onClick={() => onAnswerChange(currentQuestion.id, option.id)}
              className={cn(
                "w-full text-left rounded-lg border px-4 py-3 text-sm transition-colors",
                isSelected
                  ? "border-primary bg-primary/10 text-foreground font-medium"
                  : "border-border bg-background hover:bg-muted text-foreground",
              )}
            >
              {option.text}
            </button>
          )
        })}
      </div>

      <div className="flex items-center justify-between mt-6">
        <div className="flex gap-2">
          <Button variant="outline" onClick={onPrevious} disabled={currentQuestionIndex === 0}>
            Previous
          </Button>
          {!isLastQuestion && (
            <Button onClick={onNext}>Next</Button>
          )}
        </div>
        {isLastQuestion && (
          <Button
            onClick={onSubmit}
            disabled={isSubmitting}
            className="gap-1.5"
          >
            <CheckCircle className="h-4 w-4" />
            {isSubmitting ? "Submitting..." : "Submit Quiz"}
          </Button>
        )}
      </div>
    </div>
  )
}
