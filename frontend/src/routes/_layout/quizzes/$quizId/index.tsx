import { createFileRoute } from "@tanstack/react-router"
import { TakeQuiz } from "@/components/Quiz/TakeQuiz"

export const Route = createFileRoute("/_layout/quizzes/$quizId/")({
  component: TakeQuizPage,
  head: () => ({
    meta: [{ title: "Take Audit - Aspice Audit" }],
  }),
})

function TakeQuizPage() {
  const { quizId } = Route.useParams()
  return <TakeQuiz quizId={quizId} />
}
