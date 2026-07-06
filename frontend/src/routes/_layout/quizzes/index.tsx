import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { CheckCircle, Clock, ClipboardList, Play, RefreshCw } from "lucide-react"
import { toast } from "sonner"
import { AuditService } from "@/client"
import type { AuditSessionPublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

export const Route = createFileRoute("/_layout/quizzes/")({
  component: AuditsPage,
  head: () => ({ meta: [{ title: "ASPICE Audits - Aspice Audit" }] }),
})

const STATUS_LABELS: Record<string, string> = {
  in_progress: "In Progress",
  completed: "Completed",
  abandoned: "Abandoned",
}

function statusBadgeVariant(status: string) {
  if (status === "completed") return "default"
  if (status === "in_progress") return "secondary"
  return "outline"
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  })
}

function SessionCardSkeleton() {
  return (
    <Card>
      <CardContent className="pt-6 space-y-3">
        <Skeleton className="h-5 w-24" />
        <Skeleton className="h-4 w-40" />
        <Skeleton className="h-4 w-32" />
      </CardContent>
      <CardFooter>
        <Skeleton className="h-9 w-full" />
      </CardFooter>
    </Card>
  )
}

function SessionCard({ session }: { session: AuditSessionPublic }) {
  const navigate = useNavigate()
  const answered = session.questions_asked.length
  const total = session.max_questions

  return (
    <Card className="flex flex-col transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md">
      <CardContent className="pt-6 flex-1 space-y-2">
        <div className="flex items-center justify-between">
          <Badge variant={statusBadgeVariant(session.status)}>
            {STATUS_LABELS[session.status] ?? session.status}
          </Badge>
          <span className="text-xs text-muted-foreground">{formatDate(session.started_at)}</span>
        </div>

        <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
          <ClipboardList className="h-3.5 w-3.5" />
          <span>{answered} / {total} questions answered</span>
        </div>

        {session.status === "in_progress" && (
          <div className="w-full bg-muted rounded-full h-1.5 mt-2">
            <div
              className="bg-primary h-1.5 rounded-full transition-all"
              style={{ width: `${(answered / total) * 100}%` }}
            />
          </div>
        )}

        {session.completed_at && (
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <CheckCircle className="h-3.5 w-3.5 text-green-500" />
            <span>Completed {formatDate(session.completed_at)}</span>
          </div>
        )}
      </CardContent>

      <CardFooter className="pt-0">
        {session.status === "completed" ? (
          <Button
            className="w-full"
            variant="outline"
            onClick={() =>
              navigate({ to: "/audit/$sessionId/results", params: { sessionId: session.id } })
            }
          >
            View Results
          </Button>
        ) : session.status === "in_progress" ? (
          <Button
            className="w-full gap-1.5"
            onClick={() =>
              navigate({ to: "/audit/$sessionId", params: { sessionId: session.id } })
            }
          >
            <RefreshCw className="h-4 w-4" />
            Continue
          </Button>
        ) : null}
      </CardFooter>
    </Card>
  )
}

function AuditsPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { data: sessions = [], isLoading } = useQuery({
    queryKey: ["audit", "sessions"],
    queryFn: () => AuditService.listSessions({ limit: 50 }),
  })

  const startMutation = useMutation({
    mutationFn: () => AuditService.startSession(),
    onSuccess: (data) => {
      // Persist the first question in sessionStorage so the session page can read it
      sessionStorage.setItem(
        `audit_question_${data.session.id}`,
        JSON.stringify({
          question: data.first_question,
          questionsAnswered: 0,
          questionsTotal: data.session.max_questions,
        }),
      )
      queryClient.invalidateQueries({ queryKey: ["audit", "sessions"] })
      navigate({ to: "/audit/$sessionId", params: { sessionId: data.session.id } })
    },
    onError: () => {
      toast.error("Could not start audit. Please try again.")
    },
  })

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-start justify-between">
        <div className="flex flex-col gap-1">
          <h1 className="text-3xl font-bold tracking-tight">ASPICE Audits</h1>
          <p className="text-muted-foreground">
            Start a new assessment or continue a session in progress.
          </p>
        </div>
        <Button
          className="gap-2"
          onClick={() => startMutation.mutate()}
          disabled={startMutation.isPending}
        >
          <Play className="h-4 w-4" />
          {startMutation.isPending ? "Starting…" : "Start New Audit"}
        </Button>
      </div>

      {isLoading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => <SessionCardSkeleton key={i} />)}
        </div>
      ) : sessions.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <Clock className="h-12 w-12 text-muted-foreground/40 mb-4" />
          <p className="text-lg font-medium">No audits yet</p>
          <p className="text-sm text-muted-foreground mt-1">
            Click "Start New Audit" to begin your first ASPICE assessment.
          </p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {sessions.map((session) => (
            <SessionCard key={session.id} session={session} />
          ))}
        </div>
      )}
    </div>
  )
}
