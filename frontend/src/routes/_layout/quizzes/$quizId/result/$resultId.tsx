import { createFileRoute } from "@tanstack/react-router"
import { QuizResult } from "@/components/Quiz/QuizResult"

export const Route = createFileRoute("/_layout/quizzes/$quizId/result/$resultId")({
  component: QuizResultPage,
  head: () => ({
    meta: [{ title: "Audit Result - Aspice Audit" }],
  }),
})

function QuizResultPage() {
  const { quizId, resultId } = Route.useParams()
  return <QuizResult quizId={quizId} resultId={resultId} />
}
