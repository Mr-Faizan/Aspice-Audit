import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { AlertTriangle, ArrowLeft, CheckCircle, Home } from "lucide-react"
import { AuditService } from "@/client"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

// The OpenAPI generator types `scores` as `{ [key: string]: unknown }`.
// This alias gives us proper access throughout this file.
type Scores = Record<string, Record<string, number | null>>

export const Route = createFileRoute("/_layout/audit/$sessionId/results")({
  component: AuditResultsPage,
  head: () => ({ meta: [{ title: "Audit Results - Aspice Audit" }] }),
})

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const PROCESSES = ["SWE1", "SWE2", "SWE3", "SWE4", "SWE5", "SWE6"] as const
const LEVELS = ["L1", "L2", "L3"] as const

const PROCESS_SHORT: Record<string, string> = {
  SWE1: "SWE.1", SWE2: "SWE.2", SWE3: "SWE.3",
  SWE4: "SWE.4", SWE5: "SWE.5", SWE6: "SWE.6",
}

const PROCESS_FULL: Record<string, string> = {
  SWE1: "Software Requirements Analysis",
  SWE2: "Software Architectural Design",
  SWE3: "Software Detailed Design",
  SWE4: "Software Unit Verification",
  SWE5: "Software Integration Test",
  SWE6: "Software Qualification Test",
}

const LEVEL_FULL: Record<string, string> = {
  L1: "Level 1 — Performed",
  L2: "Level 2 — Managed",
  L3: "Level 3 — Established",
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function scoreColor(score: number | null): string {
  if (score === null) return "bg-muted text-muted-foreground"
  if (score <= 0.25) return "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300"
  if (score <= 0.50) return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300"
  if (score <= 0.75) return "bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300"
  return "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300"
}

function scoreLabel(score: number | null): string {
  if (score === null) return "—"
  if (score <= 0.25) return "Compliant"
  if (score <= 0.50) return "Minor"
  if (score <= 0.75) return "Significant"
  return "Critical"
}

function processAvgScore(scores: Scores, process: string): number | null {
  const levels = scores[process]
  if (!levels) return null
  const values = Object.values(levels).filter((v) => v !== null) as number[]
  return values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : null
}

// ---------------------------------------------------------------------------
// 9.3.1 — Radar chart (pure SVG)
// ---------------------------------------------------------------------------

function RadarChart({ scores }: { scores: Scores }) {
  const cx = 150
  const cy = 150
  const r = 110
  const n = PROCESSES.length
  const levels = 4

  // Compute angles (start from top, go clockwise)
  const angle = (i: number) => (Math.PI * 2 * i) / n - Math.PI / 2
  const pt = (i: number, radius: number) => ({
    x: cx + radius * Math.cos(angle(i)),
    y: cy + radius * Math.sin(angle(i)),
  })

  // Grid circles
  const gridCircles = Array.from({ length: levels }, (_, i) => (i + 1) / levels)

  // Data polygon — score 0=compliant (small area), 1=critical (full radius)
  const dataPoints = PROCESSES.map((p, i) => {
    const avg = processAvgScore(scores, p)
    const radius = avg !== null ? avg * r : 0
    return pt(i, radius)
  })
  const dataPath =
    dataPoints.map((p, i) => `${i === 0 ? "M" : "L"}${p.x},${p.y}`).join(" ") + " Z"

  // Axis spokes
  const spokes = PROCESSES.map((_, i) => ({ from: { x: cx, y: cy }, to: pt(i, r) }))

  return (
    <svg viewBox="0 0 300 300" className="w-full max-w-xs mx-auto">
      {/* Grid rings */}
      {gridCircles.map((frac, i) => (
        <circle
          key={i}
          cx={cx}
          cy={cy}
          r={frac * r}
          fill="none"
          stroke="currentColor"
          strokeOpacity={0.12}
          strokeWidth={1}
        />
      ))}

      {/* Axis spokes */}
      {spokes.map((s, i) => (
        <line
          key={i}
          x1={s.from.x}
          y1={s.from.y}
          x2={s.to.x}
          y2={s.to.y}
          stroke="currentColor"
          strokeOpacity={0.2}
          strokeWidth={1}
        />
      ))}

      {/* Data polygon */}
      <path
        d={dataPath}
        fill="rgb(239 68 68)"
        fillOpacity={0.25}
        stroke="rgb(239 68 68)"
        strokeWidth={2}
        strokeLinejoin="round"
      />

      {/* Data points */}
      {PROCESSES.map((p, i) => {
        const avg = processAvgScore(scores, p)
        const radius = avg !== null ? avg * r : 0
        const { x, y } = pt(i, radius)
        return avg !== null ? (
          <circle key={p} cx={x} cy={y} r={4} fill="rgb(239 68 68)" />
        ) : null
      })}

      {/* Labels */}
      {PROCESSES.map((p, i) => {
        const labelR = r + 20
        const { x, y } = pt(i, labelR)
        return (
          <text
            key={p}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            fontSize={10}
            fill="currentColor"
            className="font-medium"
          >
            {PROCESS_SHORT[p]}
          </text>
        )
      })}
    </svg>
  )
}

// ---------------------------------------------------------------------------
// 9.3.2 — Heatmap table
// ---------------------------------------------------------------------------

function HeatmapTable({ scores }: { scores: Scores }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr>
            <th className="text-left py-2 pr-4 font-medium text-muted-foreground w-24">Process</th>
            {LEVELS.map((lv) => (
              <th key={lv} className="text-center py-2 px-3 font-medium text-muted-foreground">
                {lv}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {PROCESSES.map((p) => (
            <tr key={p} className="border-t border-border/50">
              <td className="py-2 pr-4 font-medium">{PROCESS_SHORT[p]}</td>
              {LEVELS.map((lv) => {
                const score = scores[p]?.[lv] ?? null
                return (
                  <td key={lv} className="py-2 px-3 text-center">
                    <span
                      className={`inline-block px-2 py-0.5 rounded text-xs font-medium min-w-[72px] ${scoreColor(score)}`}
                    >
                      {score !== null ? `${(score * 100).toFixed(0)}% — ${scoreLabel(score)}` : "—"}
                    </span>
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>

      {/* Legend */}
      <div className="flex flex-wrap gap-3 mt-4 text-xs">
        {[
          { label: "Compliant (0–25%)", cls: "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300" },
          { label: "Minor weakness (25–50%)", cls: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300" },
          { label: "Significant gap (50–75%)", cls: "bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300" },
          { label: "Critical gap (75–100%)", cls: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300" },
        ].map(({ label, cls }) => (
          <span key={label} className={`px-2 py-0.5 rounded font-medium ${cls}`}>
            {label}
          </span>
        ))}
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// 9.3.3 — Top weaknesses list
// ---------------------------------------------------------------------------

function TopWeaknesses({ top, scores }: { top: string[]; scores: Scores }) {
  if (top.length === 0) {
    return (
      <div className="flex items-center gap-2 text-muted-foreground text-sm py-4">
        <CheckCircle className="h-4 w-4 text-green-500" />
        No significant weaknesses detected.
      </div>
    )
  }

  return (
    <ol className="flex flex-col gap-3">
      {top.map((key, idx) => {
        const [process, level] = key.split("-")
        const score = scores[process]?.[level] ?? null
        return (
          <li
            key={key}
            className="flex items-start gap-3 rounded-lg border border-border p-4"
          >
            <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-destructive/10 text-destructive font-bold text-sm">
              {idx + 1}
            </span>
            <div className="flex-1">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="font-semibold">{PROCESS_SHORT[process]}</span>
                <span className="text-xs text-muted-foreground">{LEVEL_FULL[level]}</span>
                {score !== null && (
                  <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${scoreColor(score)}`}>
                    {(score * 100).toFixed(0)}% risk
                  </span>
                )}
              </div>
              <p className="text-sm text-muted-foreground mt-0.5">
                {PROCESS_FULL[process]}
              </p>
            </div>
            <AlertTriangle className="h-4 w-4 shrink-0 text-destructive mt-0.5" />
          </li>
        )
      })}
    </ol>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------

function AuditResultsPage() {
  const { sessionId } = Route.useParams()
  const navigate = useNavigate()

  const { data: result, isLoading, isError } = useQuery({
    queryKey: ["audit", "results", sessionId],
    queryFn: () => AuditService.getResults({ sessionId }),
  })

  if (isLoading) {
    return (
      <div className="max-w-3xl mx-auto flex flex-col gap-6">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-64 w-full" />
        <Skeleton className="h-48 w-full" />
      </div>
    )
  }

  if (isError || !result) {
    return (
      <div className="flex flex-col items-center justify-center py-20 gap-4 text-center">
        <AlertTriangle className="h-10 w-10 text-muted-foreground/50" />
        <p className="text-lg font-medium">Results not available</p>
        <Button variant="outline" onClick={() => navigate({ to: "/quizzes" })}>
          Back to Audits
        </Button>
      </div>
    )
  }

  const scores = result.scores as unknown as Scores
  const { top_weaknesses } = result

  return (
    <div className="max-w-3xl mx-auto flex flex-col gap-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Audit Results</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            ASPICE process assessment — weakness summary
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-1.5"
            onClick={() => navigate({ to: "/quizzes" })}
          >
            <Home className="h-4 w-4" />
            All Audits
          </Button>
        </div>
      </div>

      {/* Top weaknesses */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Top Identified Weaknesses</CardTitle>
        </CardHeader>
        <CardContent>
          <TopWeaknesses top={top_weaknesses} scores={scores} />
        </CardContent>
      </Card>

      {/* Radar + Heatmap side by side on wide, stacked on narrow */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Risk Profile</CardTitle>
          </CardHeader>
          <CardContent className="flex items-center justify-center pb-6">
            <RadarChart scores={scores} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Process × Level Heatmap</CardTitle>
          </CardHeader>
          <CardContent>
            <HeatmapTable scores={scores} />
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-center">
        <Button
          variant="outline"
          className="gap-2"
          onClick={() => navigate({ to: "/quizzes" })}
        >
          <ArrowLeft className="h-4 w-4" />
          Start Another Audit
        </Button>
      </div>
    </div>
  )
}
