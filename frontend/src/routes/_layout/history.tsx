import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { History, RefreshCw, BarChart2, Clock } from "lucide-react"
import { AuditService } from "@/client"
import type { AuditSessionPublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"

export const Route = createFileRoute("/_layout/history")({
  component: AuditHistoryPage,
  head: () => ({ meta: [{ title: "Audit History - Aspice Audit" }] }),
})

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

const STATUS_LABEL: Record<string, string> = {
  in_progress: "In Progress",
  completed: "Completed",
  abandoned: "Abandoned",
}

function statusVariant(status: string): "default" | "secondary" | "outline" {
  if (status === "completed") return "default"
  if (status === "in_progress") return "secondary"
  return "outline"
}

// ---------------------------------------------------------------------------
// Table row
// ---------------------------------------------------------------------------

function SessionRow({ session }: { session: AuditSessionPublic }) {
  const navigate = useNavigate()
  const answered = session.questions_asked.length
  const total = session.max_questions

  return (
    <tr className="border-b border-border/60 hover:bg-muted/40 transition-colors">
      {/* Date */}
      <td className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap">
        {formatDate(session.started_at)}
      </td>

      {/* Status */}
      <td className="py-3 px-4">
        <Badge variant={statusVariant(session.status)}>
          {STATUS_LABEL[session.status] ?? session.status}
        </Badge>
      </td>

      {/* Progress */}
      <td className="py-3 px-4 text-sm">
        <div className="flex items-center gap-2">
          <span className="tabular-nums">
            {answered} / {total}
          </span>
          <div className="w-20 bg-muted rounded-full h-1.5 hidden sm:block">
            <div
              className="bg-primary h-1.5 rounded-full"
              style={{ width: `${(answered / total) * 100}%` }}
            />
          </div>
        </div>
      </td>

      {/* Completed at */}
      <td className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap">
        {session.completed_at ? formatDate(session.completed_at) : "—"}
      </td>

      {/* Actions */}
      <td className="py-3 px-4 text-right">
        {session.status === "completed" ? (
          <Button
            size="sm"
            variant="outline"
            className="gap-1.5"
            onClick={() =>
              navigate({
                to: "/audit/$sessionId/results",
                params: { sessionId: session.id },
              })
            }
          >
            <BarChart2 className="h-3.5 w-3.5" />
            View Results
          </Button>
        ) : session.status === "in_progress" ? (
          <Button
            size="sm"
            className="gap-1.5"
            onClick={() =>
              navigate({
                to: "/audit/$sessionId",
                params: { sessionId: session.id },
              })
            }
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Continue
          </Button>
        ) : (
          <span className="text-xs text-muted-foreground">—</span>
        )}
      </td>
    </tr>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------

function AuditHistoryPage() {
  const { data: sessions = [], isLoading } = useQuery({
    queryKey: ["audit", "sessions"],
    queryFn: () => AuditService.listSessions({ limit: 100 }),
  })

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-bold tracking-tight">Audit History</h1>
        <p className="text-muted-foreground">
          All your ASPICE assessment sessions, newest first.
        </p>
      </div>

      {isLoading ? (
        <div className="flex flex-col gap-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-14 w-full rounded-lg" />
          ))}
        </div>
      ) : sessions.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 gap-3 text-center">
          <History className="h-12 w-12 text-muted-foreground/40" />
          <p className="text-lg font-medium">No sessions yet</p>
          <p className="text-sm text-muted-foreground">
            Start an audit from the Audits page to see your history here.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-border">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-muted/50 border-b border-border">
                <th className="py-3 px-4 text-left font-medium text-muted-foreground">
                  <span className="flex items-center gap-1.5">
                    <Clock className="h-3.5 w-3.5" /> Started
                  </span>
                </th>
                <th className="py-3 px-4 text-left font-medium text-muted-foreground">Status</th>
                <th className="py-3 px-4 text-left font-medium text-muted-foreground">Progress</th>
                <th className="py-3 px-4 text-left font-medium text-muted-foreground">Completed</th>
                <th className="py-3 px-4 text-right font-medium text-muted-foreground">Action</th>
              </tr>
            </thead>
            <tbody>
              {sessions.map((session) => (
                <SessionRow key={session.id} session={session} />
              ))}
            </tbody>
          </table>
        </div>
      )}

      <p className="text-xs text-muted-foreground text-center">
        Showing {sessions.length} session{sessions.length !== 1 ? "s" : ""}
      </p>
    </div>
  )
}
