import { zodResolver } from "@hookform/resolvers/zod"
import { Plus } from "lucide-react"
import { useEffect } from "react"
import { useFieldArray, useForm } from "react-hook-form"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { LoadingButton } from "@/components/ui/loading-button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet"
import { Textarea } from "@/components/ui/textarea"
import type { Quiz } from "@/types/quiz"
import { QuestionField } from "./QuestionField"
import {
  ASPICE_CATEGORIES,
  DEFAULT_QUESTION,
  quizFormSchema,
  type QuizFormData,
} from "./schema"

interface AuditModalProps {
  open: boolean
  quiz: Quiz | null
  onClose: () => void
  onSave: (data: Quiz) => void
  isSaving?: boolean
}

const EMPTY_FORM: QuizFormData = {
  title: "",
  description: "",
  category: "",
  difficulty: "medium",
  timeLimit: undefined,
  passingScore: 70,
  questions: [DEFAULT_QUESTION],
}

function quizToFormData(quiz: Quiz | null): QuizFormData {
  if (!quiz) return EMPTY_FORM
  return {
    title: quiz.title,
    description: quiz.description ?? "",
    category: quiz.category,
    difficulty: quiz.difficulty,
    timeLimit: quiz.timeLimit ?? undefined,
    passingScore: quiz.passingScore ?? 70,
    questions: quiz.questions.map((q) => ({
      questionText: q.questionText ?? q.text,
      options: q.options.map((o) => ({ text: o.text })),
      correctAnswer: q.correctAnswer,
      explanation: q.explanation ?? "",
      points: q.points,
    })),
  }
}

export function AuditModal({
  open,
  quiz,
  onClose,
  onSave,
  isSaving = false,
}: AuditModalProps) {
  const isEditing = !!quiz

  const form = useForm<QuizFormData>({
    resolver: zodResolver(quizFormSchema) as any,
    mode: "onBlur",
    defaultValues: EMPTY_FORM,
  })

  const { fields: questionFields, append, remove } = useFieldArray({
    control: form.control,
    name: "questions",
  })

  useEffect(() => {
    if (open) {
      form.reset(quizToFormData(quiz))
    }
  }, [open, quiz])

  const onSubmit = (data: QuizFormData) => {
    const now = new Date().toISOString()
    const result: Quiz = {
      id: quiz?.id ?? crypto.randomUUID(),
      title: data.title,
      description: data.description ?? "",
      category: data.category,
      difficulty: data.difficulty,
      timeLimit: data.timeLimit ?? 30,
      passingScore: data.passingScore,
      isPublished: quiz?.isPublished ?? false,
      status: quiz?.status ?? "draft",
      createdBy: quiz?.createdBy ?? "admin",
      createdAt: quiz?.createdAt ?? now,
      updatedAt: now,
      activeSession: quiz?.activeSession ?? null,
      attemptCount: quiz?.attemptCount ?? 0,
      maxAttempts: quiz?.maxAttempts ?? 3,
      questions: data.questions.map((q, qi) => ({
        id: quiz?.questions[qi]?.id ?? crypto.randomUUID(),
        quizId: quiz?.id ?? "",
        type: "multiple-choice" as const,
        text: q.questionText,
        questionText: q.questionText,
        options: q.options.map((o, oi) => ({
          id: String.fromCharCode(97 + oi),
          text: o.text,
        })),
        correctAnswer: q.correctAnswer,
        explanation: q.explanation,
        points: q.points,
      })),
    }
    onSave(result)
  }

  return (
    <Sheet open={open} onOpenChange={(v) => !v && onClose()}>
      <SheetContent
        side="right"
        className="flex w-full flex-col sm:max-w-2xl"
      >
        <SheetHeader className="shrink-0">
          <SheetTitle>
            {isEditing ? "Edit Quiz" : "Create New Quiz"}
          </SheetTitle>
          <SheetDescription>
            {isEditing
              ? "Update the quiz details and questions."
              : "Fill in the details to create a new ASPICE audit quiz."}
          </SheetDescription>
        </SheetHeader>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="flex flex-1 flex-col overflow-hidden"
          >
            <div className="flex-1 overflow-y-auto px-1 py-4">
              <div className="grid gap-5">
                <FormField
                  control={form.control}
                  name="title"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        Title <span className="text-destructive">*</span>
                      </FormLabel>
                      <FormControl>
                        <Input placeholder="e.g. SWE.1 Requirements Analysis" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="description"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Description</FormLabel>
                      <FormControl>
                        <Textarea
                          placeholder="Brief description of this quiz..."
                          rows={2}
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="category"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>
                          Category <span className="text-destructive">*</span>
                        </FormLabel>
                        <Select onValueChange={field.onChange} value={field.value}>
                          <FormControl>
                            <SelectTrigger className="w-full">
                              <SelectValue placeholder="Select category" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {ASPICE_CATEGORIES.map((cat) => (
                              <SelectItem key={cat} value={cat}>
                                {cat}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="difficulty"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>
                          Difficulty <span className="text-destructive">*</span>
                        </FormLabel>
                        <Select onValueChange={field.onChange} value={field.value}>
                          <FormControl>
                            <SelectTrigger className="w-full">
                              <SelectValue placeholder="Select difficulty" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="easy">Easy</SelectItem>
                            <SelectItem value="medium">Medium</SelectItem>
                            <SelectItem value="hard">Hard</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="timeLimit"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Time Limit (minutes)</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min={1}
                            placeholder="e.g. 30"
                            value={field.value ?? ""}
                            onChange={(e) =>
                              field.onChange(
                                e.target.value === ""
                                  ? undefined
                                  : Number(e.target.value),
                              )
                            }
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="passingScore"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Passing Score (%)</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min={0}
                            max={100}
                            {...field}
                            onChange={(e) =>
                              field.onChange(Number(e.target.value))
                            }
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div>
                  <div className="mb-3 flex items-center justify-between">
                    <div>
                      <h3 className="text-sm font-semibold">
                        Questions <span className="text-destructive">*</span>
                      </h3>
                      {form.formState.errors.questions &&
                        !Array.isArray(form.formState.errors.questions) && (
                          <p className="mt-0.5 text-xs text-destructive">
                            {form.formState.errors.questions.message}
                          </p>
                        )}
                    </div>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => append(DEFAULT_QUESTION)}
                    >
                      <Plus className="mr-1 h-3.5 w-3.5" />
                      Add Question
                    </Button>
                  </div>

                  <div className="grid gap-4">
                    {questionFields.map((qField, qIndex) => (
                      <QuestionField
                        key={qField.id}
                        qIndex={qIndex}
                        control={form.control}
                        onRemove={() => remove(qIndex)}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <SheetFooter className="shrink-0 border-t pt-4">
              <SheetClose asChild>
                <Button type="button" variant="outline" disabled={isSaving}>
                  Cancel
                </Button>
              </SheetClose>
              <LoadingButton type="submit" loading={isSaving}>
                {isEditing ? "Save Changes" : "Create Quiz"}
              </LoadingButton>
            </SheetFooter>
          </form>
        </Form>
      </SheetContent>
    </Sheet>
  )
}
