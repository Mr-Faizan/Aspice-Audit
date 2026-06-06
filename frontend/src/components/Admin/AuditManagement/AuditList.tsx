import { useState } from "react"
import { Edit2, Globe, GlobeLock, Trash2 } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { LoadingButton } from "@/components/ui/loading-button"
import type { Quiz } from "@/types/quiz"

const DIFFICULTY_VARIANT: Record<
  string,
  "default" | "secondary" | "destructive"
> = {
  easy: "default",
  medium: "secondary",
  hard: "destructive",
}

const STATUS_LABEL: Record<string, string> = {
  draft: "Draft",
  published: "Published",
  unpublished: "Unpublished",
}

interface AuditListProps {
  quizzes: Quiz[]
  search: string
  category: string
  difficulty: string
  onEditQuiz: (quiz: Quiz) => void
  onDeleteQuiz: (id: string) => void
  onTogglePublish: (id: string) => void
}

export function AuditList({
  quizzes,
  search,
  category,
  difficulty,
  onEditQuiz,
  onDeleteQuiz,
  onTogglePublish,
}: AuditListProps) {
  const [quizToDelete, setQuizToDelete] = useState<Quiz | null>(null)

  const filtered = quizzes.filter((q) => {
    const matchesSearch =
      !search || q.title.toLowerCase().includes(search.toLowerCase())
    const matchesCategory = !category || category === "all" || q.category === category
    const matchesDifficulty =
      !difficulty || difficulty === "all" || q.difficulty === difficulty
    return matchesSearch && matchesCategory && matchesDifficulty
  })

  if (filtered.length === 0) {
    return (
      <div className="rounded-lg border border-dashed p-10 text-center">
        <p className="text-muted-foreground">
          {quizzes.length === 0
            ? "No quizzes yet. Create your first quiz to get started."
            : "No quizzes match the current filters."}
        </p>
      </div>
    )
  }

  return (
    <>
      <div className="grid gap-3">
        {filtered.map((quiz) => (
          <div
            key={quiz.id}
            className="flex items-start justify-between gap-4 rounded-lg border p-4"
          >
            <div className="min-w-0 flex-1">
              <div className="mb-1.5 flex flex-wrap gap-1.5">
                <Badge variant="outline">{quiz.category}</Badge>
                <Badge variant={DIFFICULTY_VARIANT[quiz.difficulty] ?? "secondary"}>
                  {quiz.difficulty.charAt(0).toUpperCase() + quiz.difficulty.slice(1)}
                </Badge>
                <Badge variant={quiz.isPublished ? "default" : "secondary"}>
                  {quiz.isPublished
                    ? "Published"
                    : (STATUS_LABEL[quiz.status ?? "draft"] ?? "Draft")}
                </Badge>
              </div>

              <h3 className="font-semibold leading-tight">{quiz.title}</h3>

              {quiz.description && (
                <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                  {quiz.description}
                </p>
              )}

              <p className="mt-2 text-xs text-muted-foreground">
                {quiz.questions.length} question{quiz.questions.length !== 1 ? "s" : ""}
                {quiz.timeLimit ? ` • ${quiz.timeLimit} min` : ""}
                {quiz.passingScore != null ? ` • ${quiz.passingScore}% to pass` : ""}
              </p>
            </div>

            <div className="flex shrink-0 items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                title={quiz.isPublished ? "Unpublish" : "Publish"}
                onClick={() => onTogglePublish(quiz.id)}
              >
                {quiz.isPublished ? (
                  <GlobeLock className="h-4 w-4" />
                ) : (
                  <Globe className="h-4 w-4" />
                )}
              </Button>

              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                title="Edit"
                onClick={() => onEditQuiz(quiz)}
              >
                <Edit2 className="h-4 w-4" />
              </Button>

              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-destructive hover:text-destructive"
                title="Delete"
                onClick={() => setQuizToDelete(quiz)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        ))}
      </div>

      <Dialog
        open={!!quizToDelete}
        onOpenChange={(v) => !v && setQuizToDelete(null)}
      >
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Delete Quiz</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete{" "}
              <strong>"{quizToDelete?.title}"</strong>? This action cannot be
              undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="mt-2">
            <DialogClose asChild>
              <Button variant="outline">Cancel</Button>
            </DialogClose>
            <LoadingButton
              variant="destructive"
              loading={false}
              onClick={() => {
                if (quizToDelete) {
                  onDeleteQuiz(quizToDelete.id)
                  setQuizToDelete(null)
                }
              }}
            >
              Delete
            </LoadingButton>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  )
}
