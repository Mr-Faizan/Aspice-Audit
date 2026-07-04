import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { BarChart3, Brain, ClipboardList, Users } from "lucide-react"
import { AnalyticsService } from "@/client"
import type { BanditArmStats, RoleStats } from "@/client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

export const Route = createFileRoute("/_layout/dashboard")({
  component: Dashboard,
  head: () => ({ meta: [{ title: "Dashboard - Aspice Audit" }] }),
})

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type Scores = Record<string, Record<string, number | null>>

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const PROCESSES = ["SWE1", "SWE2", "SWE3", "SWE4", "SWE5", "SWE6"] as const
const LEVELS = ["L1", "L2", "L3"] as const
const PROCESS_SHORT: Record<string, string> = {
  SWE1: "SWE.1", SWE2: "SWE.2", SWE3: "SWE.3",
  SWE4: "SWE.4", SWE5: "SWE.5", SWE6: "SWE.6",
}
const STAKEHOLDER_LABELS: Record<string, string> = {
  software_developer: "Developer",
  software_architect: "Architect",
  project_manager: "Project Manager",
  qa_engineer: "QA Engineer",
  test_engineer: "Test Engineer",
  team_lead: "Team Lead",
  aspice_assessor: "Assessor",
}

function scoreColor(score: number | null): string {
  if (score === null) return "bg-muted text-muted-foreground"
  if (score <= 0.25) return "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300"
  if (score <= 0.50) return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300"
  if (score <= 0.75) return "bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300"
  return "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300"
}

// ---------------------------------------------------------------------------
// Stat card
// ---------------------------------------------------------------------------

function StatCard({
  title,
  value,
  sub,
  icon: Icon,
}: {
  title: string
  value: string | number
  sub: string
  icon: React.ComponentType<{ className?: string }>
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
          {title}
        </CardTitle>
        <Icon className="h-4 w-4 text-primary" />
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold tracking-tight">{value}</div>
        <p className="text-xs text-muted-foreground mt-1">{sub}</p>
      </CardContent>
    </Card>
  )
}

// ---------------------------------------------------------------------------
// Weakness heatmap
// ---------------------------------------------------------------------------

function WeaknessHeatmap({ scores, sessionCount }: { scores: Scores; sessionCount: number }) {
  if (sessionCount === 0) {
    return (
      <p className="text-sm text-muted-foreground py-4 text-center">
        No completed sessions yet — heatmap will appear once data is available.
      </p>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr>
            <th className="text-left py-2 pr-4 font-medium text-muted-foreground w-20" />
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
              <td className="py-2 pr-4 font-medium text-xs">{PROCESS_SHORT[p]}</td>
              {LEVELS.map((lv) => {
                const score = scores[p]?.[lv] ?? null
                return (
                  <td key={lv} className="py-1.5 px-3 text-center">
                    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium min-w-[56px] ${scoreColor(score)}`}>
                      {score !== null ? `${(score * 100).toFixed(0)}%` : "—"}
                    </span>
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <p className="text-xs text-muted-foreground mt-3">
        Averaged across {sessionCount} completed session{sessionCount !== 1 ? "s" : ""}.
        Higher % = greater risk.
      </p>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Role participation table
// ---------------------------------------------------------------------------

function RoleTable({ roles }: { roles: RoleStats[] }) {
  const sorted = [...roles].sort((a, b) => b.sessions_started - a.sessions_started)
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-2 px-3 font-medium text-muted-foreground">Role</th>
            <th className="text-center py-2 px-3 font-medium text-muted-foreground">Users</th>
            <th className="text-center py-2 px-3 font-medium text-muted-foreground">Started</th>
            <th className="text-center py-2 px-3 font-medium text-muted-foreground">Completed</th>
            <th className="text-center py-2 px-3 font-medium text-muted-foreground">Completion %</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((r) => {
            const pct = r.sessions_started > 0
              ? Math.round((r.sessions_completed / r.sessions_started) * 100)
              : null
            return (
              <tr key={r.role} className="border-b border-border/50 hover:bg-muted/30">
                <td className="py-2 px-3 font-medium">
                  {STAKEHOLDER_LABELS[r.role] ?? r.role}
                </td>
                <td className="py-2 px-3 text-center tabular-nums">{r.total_users}</td>
                <td className="py-2 px-3 text-center tabular-nums">{r.sessions_started}</td>
                <td className="py-2 px-3 text-center tabular-nums">{r.sessions_completed}</td>
                <td className="py-2 px-3 text-center">
                  {pct !== null ? (
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                      pct >= 80 ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                        : pct >= 50 ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400"
                        : "bg-muted text-muted-foreground"
                    }`}>
                      {pct}%
                    </span>
                  ) : "—"}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

// ---------------------------------------------------------------------------
// CMAB arm table
// ---------------------------------------------------------------------------

function BanditTable({ arms }: { arms: BanditArmStats[] }) {
  const sorted = [...arms]
    .sort((a, b) => b.pull_count - a.pull_count)
    .slice(0, 15)

  if (sorted.length === 0) {
    return (
      <p className="text-sm text-muted-foreground py-4 text-center">
        No questions have been selected yet. Arm data will appear once sessions are run.
      </p>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-2 px-3 font-medium text-muted-foreground">Code</th>
            <th className="text-center py-2 px-3 font-medium text-muted-foreground">Process</th>
            <th className="text-center py-2 px-3 font-medium text-muted-foreground">Level</th>
            <th className="text-center py-2 px-3 font-medium text-muted-foreground">Pulls</th>
            <th className="text-center py-2 px-3 font-medium text-muted-foreground">Avg Reward</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((arm) => (
            <tr key={arm.question_id} className="border-b border-border/50 hover:bg-muted/30">
              <td className="py-2 px-3 font-mono text-xs">{arm.question_code}</td>
              <td className="py-2 px-3 text-center">
                <span className="text-xs bg-muted px-1.5 py-0.5 rounded">{arm.process}</span>
              </td>
              <td className="py-2 px-3 text-center">
                <span className="text-xs bg-muted px-1.5 py-0.5 rounded">{arm.level}</span>
              </td>
              <td className="py-2 px-3 text-center tabular-nums font-medium">{arm.pull_count}</td>
              <td className="py-2 px-3 text-center">
                {arm.avg_reward !== null ? (
                  <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${scoreColor(arm.avg_reward)}`}>
                    {(arm.avg_reward * 100).toFixed(0)}%
                  </span>
                ) : "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------

function Dashboard() {
  const weaknessQ = useQuery({
    queryKey: ["analytics", "weaknesses"],
    queryFn: () => AnalyticsService.aggregateWeaknesses(),
  })
  const usersQ = useQuery({
    queryKey: ["analytics", "users"],
    queryFn: () => AnalyticsService.userStats(),
  })
  const banditQ = useQuery({
    queryKey: ["analytics", "bandit"],
    queryFn: () => AnalyticsService.banditPerformance(),
  })

  const roles = usersQ.data?.roles ?? []
  const totalUsers = roles.reduce((s, r) => s + r.total_users, 0)
  const totalStarted = roles.reduce((s, r) => s + r.sessions_started, 0)
  const totalCompleted = roles.reduce((s, r) => s + r.sessions_completed, 0)
  const completionRate = totalStarted > 0
    ? `${Math.round((totalCompleted / totalStarted) * 100)}%`
    : "—"
  const totalArms = banditQ.data?.arms.length ?? 0

  const scores = weaknessQ.data?.scores as unknown as Scores ?? {}
  const sessionCount = weaknessQ.data?.session_count ?? 0

  const isLoading = weaknessQ.isLoading || usersQ.isLoading || banditQ.isLoading

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
        <p className="text-muted-foreground">
          ASPICE audit system analytics and CMAB performance.
        </p>
      </div>

      {/* Stat cards */}
      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Card key={i}>
              <CardHeader className="pb-2"><Skeleton className="h-4 w-28" /></CardHeader>
              <CardContent><Skeleton className="h-8 w-16" /></CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Active Users" value={totalUsers} sub="across all stakeholder roles" icon={Users} />
          <StatCard title="Sessions Started" value={totalStarted} sub={`${totalCompleted} completed`} icon={ClipboardList} />
          <StatCard title="Completion Rate" value={completionRate} sub="sessions finished vs started" icon={BarChart3} />
          <StatCard title="Questions in Bank" value={totalArms} sub="with active CMAB arms" icon={Brain} />
        </div>
      )}

      {/* Weakness heatmap */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Aggregate Weakness Heatmap</CardTitle>
        </CardHeader>
        <CardContent>
          {weaknessQ.isLoading ? (
            <Skeleton className="h-40 w-full" />
          ) : (
            <WeaknessHeatmap scores={scores} sessionCount={sessionCount} />
          )}
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Role participation */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Participation by Role</CardTitle>
          </CardHeader>
          <CardContent>
            {usersQ.isLoading ? (
              <Skeleton className="h-40 w-full" />
            ) : (
              <RoleTable roles={roles} />
            )}
          </CardContent>
        </Card>

        {/* CMAB arm performance */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">CMAB Arm Performance <span className="text-muted-foreground font-normal text-xs">(top 15 by pulls)</span></CardTitle>
          </CardHeader>
          <CardContent>
            {banditQ.isLoading ? (
              <Skeleton className="h-40 w-full" />
            ) : (
              <BanditTable arms={banditQ.data?.arms ?? []} />
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
