import { CheckCircle, XCircle } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import type { Answer, Question } from "@/types/quiz"

interface QuestionBreakdownProps {
  questions?: Question[]
  answers?: Answer[]
}

export function QuestionBreakdown({ questions, answers }: QuestionBreakdownProps) {
  return (
    <div className="rounded-xl border bg-card shadow-sm">
      <div className="p-6">
        <h3 className="text-base font-semibold text-foreground mb-1">Question Breakdown</h3>
        <Separator className="my-3" />

        <div className="space-y-4">
          {questions?.map((question, idx) => {
            const { id, correctAnswer, options, text, explanation } = question
            const userAnswer = answers?.find((a) => a.questionId === id)
            const isCorrect = userAnswer?.selectedAnswer === correctAnswer
            const selectedOption = options?.find((opt) => opt.id === userAnswer?.selectedAnswer)
            const correctOption = options?.find((opt) => opt.id === correctAnswer)

            return (
              <div
                key={id}
                className="rounded-lg border bg-muted/30 p-4"
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <p className="text-sm font-medium text-foreground">
                    Question {idx + 1}
                  </p>
                  <Badge
                    variant={isCorrect ? "default" : "destructive"}
                    className="flex items-center gap-1 shrink-0"
                  >
                    {isCorrect ? (
                      <CheckCircle className="h-3 w-3" />
                    ) : (
                      <XCircle className="h-3 w-3" />
                    )}
                    {isCorrect ? "Correct" : "Incorrect"}
                  </Badge>
                </div>

                <p className="text-sm text-foreground mb-3">{text}</p>

                <div className="space-y-1.5 text-sm">
                  <div>
                    <span className="text-muted-foreground">Your answer: </span>
                    <span className={isCorrect ? "text-green-600 dark:text-green-400 font-medium" : "text-red-600 dark:text-red-400 font-medium"}>
                      {selectedOption?.text ?? "Not answered"}
                    </span>
                  </div>

                  {!isCorrect && (
                    <div>
                      <span className="text-muted-foreground">Correct answer: </span>
                      <span className="text-green-600 dark:text-green-400 font-medium">
                        {correctOption?.text}
                      </span>
                    </div>
                  )}

                  {explanation && (
                    <div className="mt-2 rounded-md bg-muted px-3 py-2">
                      <span className="text-muted-foreground text-xs font-medium uppercase tracking-wide">
                        Explanation
                      </span>
                      <p className="text-sm text-foreground mt-0.5">{explanation}</p>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
