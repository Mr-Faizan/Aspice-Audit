import { createFileRoute } from "@tanstack/react-router"
import { QuizList } from "@/components/Quiz/QuizList"

export const Route = createFileRoute("/_layout/quizzes/")({
  component: QuizzesPage,
  head: () => ({
    meta: [{ title: "ASPICE Audits - Aspice Audit" }],
  }),
})

function QuizzesPage() {
  return <QuizList />
}
