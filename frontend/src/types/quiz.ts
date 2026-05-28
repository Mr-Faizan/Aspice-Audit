export type QuestionType = "multiple-choice" | "true-false"
export type Difficulty = "easy" | "medium" | "hard"

export interface Option {
  id: string
  text: string
}

export interface Question {
  id: string
  quizId: string
  type: QuestionType
  text: string
  questionText?: string
  options: Option[]
  correctAnswer: string
  points: number
  explanation?: string
}

export interface Quiz {
  id: string
  title: string
  description: string
  category: string
  difficulty: Difficulty
  timeLimit: number
  passingScore?: number
  status?: string
  questions: Question[]
  createdBy: string
  createdAt: string
  updatedAt: string
  isPublished: boolean
  activeSession?: {
    id: string
    startedAt: string
    expiresAt: string
  } | null
  attemptCount?: number
  maxAttempts?: number
}

export interface Answer {
  questionId: string
  selectedAnswer: string
}

export interface QuizAttempt {
  id: string
  userId: string
  quizId: string
  answers: Answer[]
  score: number
  totalQuestions: number
  correctAnswers: number
  passed: boolean
  startedAt: string
  completedAt: string
  quiz?: Quiz
}

export interface QuizResult extends QuizAttempt {
  quiz: Quiz
  percentage: number
  passed: boolean
}

export interface SubmitQuizRequest {
  answers: Answer[]
  startedAt: string
}

export interface QuizListFilters {
  category?: string
  difficulty?: Difficulty
  search?: string
}
