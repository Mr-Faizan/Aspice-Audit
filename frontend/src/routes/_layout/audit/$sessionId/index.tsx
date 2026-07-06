import { useEffect, useState } from "react"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useMutation } from "@tanstack/react-query"
import { AlertCircle, ChevronRight } from "lucide-react"
import { AuditService } from "@/client"
import type { AuditOptionPublic, AuditQuestionPublic } from "@/client"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { toast } from "sonner"

export const Route = createFileRoute("/_layout/audit/$sessionId/")({
  component: AuditSessionPage,
  head: () => ({ meta: [{ title: "Audit Session - Aspice Audit" }] }),
})

type StoredState = {
  question: AuditQuestionPublic
  questionsAnswered: number
  questionsTotal: number
}

const PROCESS_LABELS: Record<string, string> = {
  SWE1: "SWE.1 Software Requirements Analysis",
  SWE2: "SWE.2 Software Architectural Design",
  SWE3: "SWE.3 Software Detailed Design",
  SWE4: "SWE.4 Software Unit Verification",
  SWE5: "SWE.5 Software Integration Test",
  SWE6: "SWE.6 Software Qualification Test",
}

const LEVEL_LABELS: Record<string, string> = {
  L1: "Level 1 — Performed",
  L2: "Level 2 — Managed",
  L3: "Level 3 — Established",
}

function OptionCard({
  option,
  selected,
  onSelect,
  disabled,
}: {
  option: AuditOptionPublic
  selected: boolean
  onSelect: () => void
  disabled: boolean
}) {
  return (
    <button
      type="button"
      onClick={onSelect}
      disabled={disabled}
      className={`w-full text-left rounded-lg border p-4 transition-all duration-150 ${
        selected
          ? "border-primary bg-primary/5 ring-1 ring-primary"
          : "border-border bg-background hover:border-primary/50 hover:bg-muted/40"
      } disabled:opacity-50 disabled:cursor-not-allowed`}
    >
      <div className="flex gap-3 items-start">
        <span
          className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-xs font-semibold ${
            selected ? "border-primary bg-primary text-primary-foreground" : "border-muted-foreground text-muted-foreground"
          }`}
        >
          {option.label}
        </span>
        <span className="text-sm leading-relaxed">{option.option_text}</span>
      </div>
    </button>
  )
}

function AuditSessionPage() {
  const { sessionId } = Route.useParams()
  const navigate = useNavigate()


  const [state, setState] = useState<StoredState | null>(null)
  const [selected, setSelected] = useState<AuditOptionPublic | null>(null)
  const [notFound, setNotFound] = useState(false)

  // Load current question from sessionStorage on mount
  useEffect(() => {
    const raw = sessionStorage.getItem(`audit_question_${sessionId}`)
    if (raw) {
      try {
        setState(JSON.parse(raw))
      } catch {
        setNotFound(true)
      }
    } else {
      setNotFound(true)
    }
  }, [sessionId])

  const submitMutation = useMutation({
    mutationFn: () =>
      AuditService.submitAnswer({
        sessionId,
        requestBody: {
          question_id: state!.question.id,
          option_id: selected!.id,
        },
      }),
    onSuccess: (result) => {
      setSelected(null)
      if (result.status === "in_progress") {
        const next: StoredState = {
          question: result.next_question,
          questionsAnswered: result.questions_answered,
          questionsTotal: result.questions_total,
        }
        sessionStorage.setItem(`audit_question_${sessionId}`, JSON.stringify(next))
        setState(next)
      } else {
        sessionStorage.removeItem(`audit_question_${sessionId}`)
        navigate({ to: "/audit/$sessionId/results", params: { sessionId } })
      }
    },
    onError: () => {
      toast.error("Submission failed. Please try again.")
    },
  })

  if (notFound) {
    return (
      <div className="flex flex-col items-center justify-center py-20 gap-4 text-center">
        <AlertCircle className="h-10 w-10 text-muted-foreground/50" />
        <p className="text-lg font-medium">Question not available</p>
        <p className="text-sm text-muted-foreground">
          This session may have already been completed or is not accessible from here.
        </p>
        <Button variant="outline" onClick={() => navigate({ to: "/quizzes" })}>
          Back to Audits
        </Button>
      </div>
    )
  }

  if (!state) return null

  const { question, questionsAnswered, questionsTotal } = state
  const progress = Math.round((questionsAnswered / questionsTotal) * 100)
  const processLabel = PROCESS_LABELS[question.process] ?? question.process
  const levelLabel = LEVEL_LABELS[question.level] ?? question.level

  return (
    <div className="max-w-2xl mx-auto flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-col gap-1">
        <div className="flex items-center justify-between text-sm text-muted-foreground">
          <span>
            Question {questionsAnswered + 1} of {questionsTotal}
          </span>
          <span>{progress}% complete</span>
        </div>
        <div className="w-full bg-muted rounded-full h-2">
          <div
            className="bg-primary h-2 rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question card */}
      <Card>
        <CardContent className="pt-6 flex flex-col gap-5">
          {/* Tags */}
          <div className="flex flex-wrap gap-2">
            <span className="text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 px-2 py-0.5 rounded">
              {processLabel}
            </span>
            <span className="text-xs font-medium bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400 px-2 py-0.5 rounded">
              {levelLabel}
            </span>
            <span className="text-xs font-medium text-muted-foreground bg-muted px-2 py-0.5 rounded">
              {question.base_practice_id}
            </span>
          </div>

          {/* Question text */}
          <p className="text-base font-medium leading-relaxed">{question.question_text}</p>

          {/* Options */}
          <div className="flex flex-col gap-2.5">
            {(question.options ?? []).map((opt) => (
              <OptionCard
                key={opt.id}
                option={opt}
                selected={selected?.id === opt.id}
                onSelect={() => setSelected(opt)}
                disabled={submitMutation.isPending}
              />
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Submit */}
      <div className="flex justify-end">
        <Button
          size="lg"
          className="gap-2 min-w-36"
          disabled={!selected || submitMutation.isPending}
          onClick={() => submitMutation.mutate()}
        >
          {submitMutation.isPending ? "Submitting…" : "Next"}
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
