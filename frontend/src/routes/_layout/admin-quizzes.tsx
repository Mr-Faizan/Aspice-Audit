import { createFileRoute } from "@tanstack/react-router"
import { AuditManagement } from "@/components/Admin/AuditManagement"

export const Route = createFileRoute("/_layout/admin-quizzes")({
  component: AdminQuizzes,
  head: () => ({
    meta: [
      {
        title: "Audit Management - Aspice Audit",
      },
    ],
  }),
})

function AdminQuizzes() {
  return <AuditManagement />
}
