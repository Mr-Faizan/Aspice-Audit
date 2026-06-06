import { z } from "zod"

const optionSchema = z.object({
  text: z.string().min(1, "Option text is required"),
})

export const questionFormSchema = z.object({
  questionText: z.string().min(1, "Question text is required"),
  options: z.array(optionSchema).min(2, "At least 2 options required"),
  correctAnswer: z.string().min(1, "Please select the correct answer"),
  explanation: z.string().optional(),
  points: z.number().min(1, "Points must be at least 1"),
})

export const quizFormSchema = z.object({
  title: z.string().min(1, "Title is required"),
  description: z.string().optional(),
  category: z.string().min(1, "Category is required"),
  difficulty: z.enum(["easy", "medium", "hard"]),
  timeLimit: z.number().min(1).optional(),
  passingScore: z.number().min(0).max(100),
  questions: z.array(questionFormSchema).min(1, "At least one question is required"),
})

export type QuizFormData = z.infer<typeof quizFormSchema>
export type QuestionFormData = z.infer<typeof questionFormSchema>

export const ASPICE_CATEGORIES = ["SWE", "SYS", "SUP", "MAN", "ACQ", "SPL"] as const

export const DEFAULT_QUESTION: QuestionFormData = {
  questionText: "",
  options: [{ text: "" }, { text: "" }],
  correctAnswer: "",
  explanation: "",
  points: 1,
}
