import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/admin-quizzes")({
  component: AdminQuizzes,
  head: () => ({
    meta: [
      {
        title: "Quiz Management - Aspice Audit",
      },
    ],
  }),
})

function AdminQuizzes() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Quiz Management</h1>
        <p className="text-muted-foreground text-lg">
          Create, edit, and manage ASPICE audit quizzes.
        </p>
      </div>
      <div className="rounded-lg border border-dashed p-8 text-center">
        <p className="text-muted-foreground">
          Coming soon: Admin quiz management interface
        </p>
      </div>
    </div>
  )
}
