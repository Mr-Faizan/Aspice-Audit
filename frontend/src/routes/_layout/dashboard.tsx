import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { BarChart3, ClipboardList, GraduationCap, Users } from "lucide-react"
import { Suspense } from "react"

import { StatisticsService } from "@/client"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import type { RecentAttemptPublic } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import type { ColumnDef } from "@tanstack/react-table"
import { Skeleton } from "@/components/ui/skeleton"

function getStatsQueryOptions() {
  return {
    queryFn: () => StatisticsService.getDashboardSummary(),
    queryKey: ["dashboard-stats"],
  }
}

export const Route = createFileRoute("/_layout/dashboard")({
  component: Dashboard,
  head: () => ({
    meta: [
      {
        title: "Dashboard - Aspice Audit",
      },
    ],
  }),
})

const columns: ColumnDef<RecentAttemptPublic>[] = [
  {
    accessorKey: "quiz_title",
    header: "Quiz",
    cell: ({ row }) => (
      <span className="font-medium text-foreground">
        {row.original.quiz_title}
      </span>
    ),
  },
  {
    accessorKey: "user_full_name",
    header: "User",
    cell: ({ row }) => (
      <div className="flex flex-col">
        <span className="text-sm">
          {row.original.user_full_name || "N/A"}
        </span>
        <span className="text-xs text-muted-foreground">
          {row.original.user_email}
        </span>
      </div>
    ),
  },
  {
    accessorKey: "score",
    header: "Score",
    cell: ({ row }) => (
      <span className="font-mono">{row.original.score}%</span>
    ),
  },
  {
    accessorKey: "passed",
    header: "Status",
    cell: ({ row }) => (
      <span
        className={
          row.original.passed
            ? "text-green-600 dark:text-green-400 font-semibold"
            : "text-red-600 dark:text-red-400 font-semibold"
        }
      >
        {row.original.passed ? "Passed" : "Failed"}
      </span>
    ),
  },
  {
    accessorKey: "completed_at",
    header: "Completed At",
    cell: ({ row }) =>
      row.original.completed_at
        ? new Date(row.original.completed_at).toLocaleString()
        : "N/A",
  },
]

function DashboardSkeleton() {
  return (
    <div className="flex flex-col gap-8">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Card key={i}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <Skeleton className="h-4 w-24" />
              <Skeleton className="h-4 w-4 rounded-full" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-8 w-16 mb-2" />
              <Skeleton className="h-3 w-32" />
            </CardContent>
          </Card>
        ))}
      </div>
      <div className="space-y-4">
        <div className="space-y-2">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-4 w-64" />
        </div>
        <div className="border rounded-md">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="flex items-center p-4 border-b last:border-0">
              <Skeleton className="h-4 w-full" />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function DashboardContent() {
  const { data: stats } = useSuspenseQuery(getStatsQueryOptions())

  return (
    <div className="flex flex-col gap-8">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium uppercase tracking-wider text-muted-foreground">Total Users</CardTitle>
            <Users className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold tracking-tight">{stats.total_users}</div>
            <p className="text-xs text-muted-foreground mt-1">
              <span className="text-green-600 font-medium">{stats.active_users}</span> active users currently
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium uppercase tracking-wider text-muted-foreground">Total Quizzes</CardTitle>
            <GraduationCap className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold tracking-tight">{stats.total_quizzes}</div>
            <p className="text-xs text-muted-foreground mt-1">
              <span className="font-medium">{stats.published_quizzes}</span> published quizzes
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium uppercase tracking-wider text-muted-foreground">Total Attempts</CardTitle>
            <ClipboardList className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold tracking-tight">{stats.total_attempts}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Across all available audits
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium uppercase tracking-wider text-muted-foreground">Avg Audit Score</CardTitle>
            <BarChart3 className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold tracking-tight">
              {stats.average_score.toFixed(1)}%
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              System-wide compliance level
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="flex flex-col gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-foreground">Recent Audit Attempts</h2>
          <p className="text-sm text-muted-foreground">
            Latest quiz results synchronization from all auditors
          </p>
        </div>
        <div className="rounded-xl border bg-card shadow-sm">
          <DataTable
            columns={columns}
            data={stats.recent_attempts || []}
          />
        </div>
      </div>
    </div>
  )
}

function Dashboard() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Auditor Dashboard</h1>
        <p className="text-muted-foreground text-lg">
          Overview and recent insights of the Aspice Audit system.
        </p>
      </div>
      <Suspense fallback={<DashboardSkeleton />}>
        <DashboardContent />
      </Suspense>
    </div>
  )
}
