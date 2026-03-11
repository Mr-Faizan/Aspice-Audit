import type { DifficultyEnum, QuizPublic, QuizCreate } from "@/client"

export interface AdminQuizzesProps {
  searchQuery: string | null
  selectedDifficulty: DifficultyEnum | "" | null
  selectedCategory: string | null
  onEditQuiz?: (quiz: QuizPublic) => void
}

export interface StatisticCardProps {
  title: string
  value: number | string
  icon: React.ElementType
  color: string
  subtitle?: string
}

export interface DashboardDetailsProps {
  statistics: {
    activeUsers?: number
    totalUsers?: number
    totalQuizzes?: number
    publishedQuizzes?: number
    unpublishedQuizzes?: number
    totalAttempts?: number
    averageScore?: number
  }
}

export interface QuizFiltersProps {
  searchTerm: string
  setSearchTerm: (value: string) => void
  selectedDifficulty: DifficultyEnum | "" | null
  setSelectedDifficulty: (value: DifficultyEnum | "" | null) => void
  selectedCategory: string
  setSelectedCategory: (value: string) => void
}

export interface QuizModalProps {
  open: boolean
  quiz?: QuizPublic | null
  onClose: () => void
  onSave: (quiz: QuizCreate) => void
  isSubmitting?: boolean
}
