import { createFileRoute } from "@tanstack/react-router"
import { QuizHistory } from "@/components/Quiz/QuizHistory"

export const Route = createFileRoute("/_layout/history")({
  component: HistoryPage,
  head: () => ({
    meta: [{ title: "Audit History - Aspice Audit" }],
  }),
})

function HistoryPage() {
  return <QuizHistory />
}
