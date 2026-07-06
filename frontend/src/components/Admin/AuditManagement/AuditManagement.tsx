import { Plus } from "lucide-react"
import { useState } from "react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { MOCK_QUIZZES } from "@/lib/quiz/mock-data"
import type { Quiz } from "@/types/quiz"
import { AuditFilters } from "./AuditFilters"
import { AuditList } from "./AuditList"
import { AuditModal } from "./AuditModal"

export function AuditManagement() {
  const [quizzes, setQuizzes] = useState<Quiz[]>(MOCK_QUIZZES)
  const [search, setSearch] = useState("")
  const [category, setCategory] = useState("all")
  const [difficulty, setDifficulty] = useState("all")
  const [isSheetOpen, setIsSheetOpen] = useState(false)
  const [editingQuiz, setEditingQuiz] = useState<Quiz | null>(null)

  const handleAddQuiz = () => {
    setEditingQuiz(null)
    setIsSheetOpen(true)
  }

  const handleEditQuiz = (quiz: Quiz) => {
    setEditingQuiz(quiz)
    setIsSheetOpen(true)
  }

  const handleSheetClose = () => {
    setIsSheetOpen(false)
    setEditingQuiz(null)
  }

  const handleSaveQuiz = (quiz: Quiz) => {
    const isEditing = quizzes.some((q) => q.id === quiz.id)
    if (isEditing) {
      setQuizzes((prev) => prev.map((q) => (q.id === quiz.id ? quiz : q)))
      toast.success("Quiz updated successfully")
    } else {
      setQuizzes((prev) => [quiz, ...prev])
      toast.success("Quiz created successfully")
    }
    handleSheetClose()
  }

  const handleDeleteQuiz = (id: string) => {
    setQuizzes((prev) => prev.filter((q) => q.id !== id))
    toast.success("Quiz deleted successfully")
  }

  const handleTogglePublish = (id: string) => {
    setQuizzes((prev) =>
      prev.map((q) => {
        if (q.id !== id) return q
        const nowPublished = !q.isPublished
        return {
          ...q,
          isPublished: nowPublished,
          status: nowPublished ? "published" : "unpublished",
          updatedAt: new Date().toISOString(),
        }
      }),
    )
  }

  const publishedCount = quizzes.filter((q) => q.isPublished).length

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Audit Management</h1>
          <p className="text-muted-foreground">
            {quizzes.length} quiz{quizzes.length !== 1 ? "zes" : ""} total •{" "}
            {publishedCount} published
          </p>
        </div>
        <Button onClick={handleAddQuiz}>
          <Plus className="mr-2 h-4 w-4" />
          New Quiz
        </Button>
      </div>

      <AuditFilters
        search={search}
        category={category}
        difficulty={difficulty}
        onSearchChange={setSearch}
        onCategoryChange={setCategory}
        onDifficultyChange={setDifficulty}
      />

      <AuditList
        quizzes={quizzes}
        search={search}
        category={category}
        difficulty={difficulty}
        onEditQuiz={handleEditQuiz}
        onDeleteQuiz={handleDeleteQuiz}
        onTogglePublish={handleTogglePublish}
      />

      <AuditModal
        open={isSheetOpen}
        quiz={editingQuiz}
        onClose={handleSheetClose}
        onSave={handleSaveQuiz}
      />
    </div>
  )
}
