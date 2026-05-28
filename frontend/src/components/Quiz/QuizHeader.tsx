import { Timer } from "lucide-react"
import { Badge } from "@/components/ui/badge"

interface QuizHeaderProps {
  title: string
  formattedTime: string
  timeRemaining: number
  currentQuestionIndex: number
  totalQuestions: number
  progress: number
}

export function QuizHeader({
  title,
  formattedTime,
  timeRemaining,
  currentQuestionIndex,
  totalQuestions,
  progress,
}: QuizHeaderProps) {
  return (
    <div className="rounded-xl border bg-card p-4 mb-4 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-semibold text-foreground truncate pr-4">{title}</h2>
        <Badge
          variant={timeRemaining < 60 ? "destructive" : "default"}
          className="flex items-center gap-1 shrink-0 text-sm px-3 py-1"
        >
          <Timer className="h-3.5 w-3.5" />
          {formattedTime}
        </Badge>
      </div>

      {/* progress bar */}
      <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
        <div
          className="h-full rounded-full bg-primary transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="text-xs text-muted-foreground mt-1.5">
        Question {currentQuestionIndex + 1} of {totalQuestions}
      </p>
    </div>
  )
}
