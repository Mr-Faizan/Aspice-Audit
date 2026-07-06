import { useState } from "react"
import { createFileRoute } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Plus, Pencil, PowerOff, ChevronDown, ChevronUp } from "lucide-react"
import { toast } from "sonner"
import { QuestionsService } from "@/client"
import type {
  AspiceLevelEnum,
  AuditOptionPublic,
  AuditQuestionPublic,
  ProcessEnum,
  StakeholderRoleEnum,
} from "@/client"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Skeleton } from "@/components/ui/skeleton"
import { Textarea } from "@/components/ui/textarea"

export const Route = createFileRoute("/_layout/admin-quizzes")({
  component: QuestionBankPage,
  head: () => ({ meta: [{ title: "Question Bank - Aspice Audit" }] }),
})

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const PROCESSES: ProcessEnum[] = ["SWE1", "SWE2", "SWE3", "SWE4", "SWE5", "SWE6"]
const LEVELS: AspiceLevelEnum[] = ["L1", "L2", "L3"]
const STAKEHOLDERS: StakeholderRoleEnum[] = [
  "software_developer", "software_architect", "project_manager",
  "qa_engineer", "test_engineer", "team_lead", "aspice_assessor",
]
const STAKEHOLDER_LABELS: Record<StakeholderRoleEnum, string> = {
  software_developer: "Developer",
  software_architect: "Architect",
  project_manager: "PM",
  qa_engineer: "QA",
  test_engineer: "Test Eng.",
  team_lead: "Team Lead",
  aspice_assessor: "Assessor",
}
const OPTION_LABELS = ["A", "B", "C", "D", "E"] as const

// ---------------------------------------------------------------------------
// Form state types
// ---------------------------------------------------------------------------

type OptionDraft = { label: string; option_text: string; weight: number }
type FormState = {
  question_code: string
  base_practice_id: string
  process: ProcessEnum
  level: AspiceLevelEnum
  stakeholders: StakeholderRoleEnum[]
  question_text: string
  recommendation_logic: string
  options: OptionDraft[]
}

function emptyForm(): FormState {
  return {
    question_code: "",
    base_practice_id: "",
    process: "SWE1",
    level: "L1",
    stakeholders: [],
    question_text: "",
    recommendation_logic: "",
    options: OPTION_LABELS.map((label, i) => ({
      label,
      option_text: "",
      weight: i,       // A=0 (best), E=4 (worst)
    })),
  }
}

function questionToForm(q: AuditQuestionPublic): FormState {
  const opts = [...(q.options ?? [])]
    .sort((a, b) => a.label.localeCompare(b.label))
  return {
    question_code: q.question_code,
    base_practice_id: q.base_practice_id,
    process: q.process,
    level: q.level,
    stakeholders: q.stakeholders as StakeholderRoleEnum[],
    question_text: q.question_text,
    recommendation_logic: q.recommendation_logic ?? "",
    options: OPTION_LABELS.map((label) => {
      const existing = opts.find((o) => o.label === label)
      return existing
        ? { label, option_text: existing.option_text, weight: existing.weight }
        : { label, option_text: "", weight: 0 }
    }),
  }
}

// ---------------------------------------------------------------------------
// Question form dialog
// ---------------------------------------------------------------------------

function QuestionFormDialog({
  open,
  editing,
  onClose,
}: {
  open: boolean
  editing: AuditQuestionPublic | null
  onClose: () => void
}) {
  const qc = useQueryClient()
  const [form, setForm] = useState<FormState>(() =>
    editing ? questionToForm(editing) : emptyForm(),
  )

  // Reset when editing target changes
  useState(() => {
    setForm(editing ? questionToForm(editing) : emptyForm())
  })

  const set = (patch: Partial<FormState>) => setForm((f) => ({ ...f, ...patch }))
  const setOption = (idx: number, patch: Partial<OptionDraft>) =>
    setForm((f) => {
      const options = [...f.options]
      options[idx] = { ...options[idx], ...patch }
      return { ...f, options }
    })

  const createMut = useMutation({
    mutationFn: () =>
      QuestionsService.createQuestion({
        requestBody: {
          ...form,
          recommendation_logic: form.recommendation_logic || undefined,
        },
      }),
    onSuccess: () => {
      toast.success("Question created")
      qc.invalidateQueries({ queryKey: ["questions"] })
      onClose()
    },
    onError: () => toast.error("Failed to create question"),
  })

  const updateMut = useMutation({
    mutationFn: () =>
      QuestionsService.updateQuestion({
        questionId: editing!.id,
        requestBody: {
          process: form.process,
          level: form.level,
          stakeholders: form.stakeholders,
          question_text: form.question_text,
          recommendation_logic: form.recommendation_logic || undefined,
          options: form.options,
        },
      }),
    onSuccess: () => {
      toast.success("Question updated")
      qc.invalidateQueries({ queryKey: ["questions"] })
      onClose()
    },
    onError: () => toast.error("Failed to update question"),
  })

  const isPending = createMut.isPending || updateMut.isPending
  const handleSave = () => editing ? updateMut.mutate() : createMut.mutate()

  const toggleStakeholder = (role: StakeholderRoleEnum) => {
    set({
      stakeholders: form.stakeholders.includes(role)
        ? form.stakeholders.filter((r) => r !== role)
        : [...form.stakeholders, role],
    })
  }

  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{editing ? "Edit Question" : "Add Question"}</DialogTitle>
        </DialogHeader>

        <div className="grid gap-4 py-2">
          {/* Code + BP */}
          <div className="grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-1.5">
              <Label>Question Code</Label>
              <Input
                placeholder="SWE1_L1_01"
                value={form.question_code}
                onChange={(e) => set({ question_code: e.target.value })}
                disabled={!!editing}
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label>Base Practice ID</Label>
              <Input
                placeholder="SWE.1.BP1"
                value={form.base_practice_id}
                onChange={(e) => set({ base_practice_id: e.target.value })}
              />
            </div>
          </div>

          {/* Process + Level */}
          <div className="grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-1.5">
              <Label>Process</Label>
              <Select value={form.process} onValueChange={(v) => set({ process: v as ProcessEnum })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  {PROCESSES.map((p) => <SelectItem key={p} value={p}>{p}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div className="flex flex-col gap-1.5">
              <Label>Level</Label>
              <Select value={form.level} onValueChange={(v) => set({ level: v as AspiceLevelEnum })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  {LEVELS.map((l) => <SelectItem key={l} value={l}>{l}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Stakeholders */}
          <div className="flex flex-col gap-1.5">
            <Label>Stakeholders</Label>
            <div className="flex flex-wrap gap-2">
              {STAKEHOLDERS.map((role) => (
                <button
                  key={role}
                  type="button"
                  onClick={() => toggleStakeholder(role)}
                  className={`px-2.5 py-1 rounded-md text-xs font-medium border transition-colors ${
                    form.stakeholders.includes(role)
                      ? "bg-primary text-primary-foreground border-primary"
                      : "border-border bg-background hover:bg-muted"
                  }`}
                >
                  {STAKEHOLDER_LABELS[role]}
                </button>
              ))}
            </div>
          </div>

          {/* Question text */}
          <div className="flex flex-col gap-1.5">
            <Label>Question Text</Label>
            <Textarea
              rows={3}
              placeholder="Enter the assessment question…"
              value={form.question_text}
              onChange={(e) => set({ question_text: e.target.value })}
            />
          </div>

          {/* Recommendation logic */}
          <div className="flex flex-col gap-1.5">
            <Label>Recommendation Logic <span className="text-muted-foreground text-xs">(optional)</span></Label>
            <Textarea
              rows={2}
              placeholder="What should be recommended if this area is weak?"
              value={form.recommendation_logic}
              onChange={(e) => set({ recommendation_logic: e.target.value })}
            />
          </div>

          {/* Options */}
          <div className="flex flex-col gap-2">
            <Label>Answer Options <span className="text-muted-foreground text-xs">(A = best / weight 0, E = worst / weight 4)</span></Label>
            {form.options.map((opt, idx) => (
              <div key={opt.label} className="flex gap-2 items-start">
                <span className="mt-2.5 w-5 text-xs font-bold text-muted-foreground shrink-0">
                  {opt.label}
                </span>
                <Input
                  className="flex-1"
                  placeholder={`Option ${opt.label}`}
                  value={opt.option_text}
                  onChange={(e) => setOption(idx, { option_text: e.target.value })}
                />
                <Select
                  value={String(opt.weight)}
                  onValueChange={(v) => setOption(idx, { weight: Number(v) })}
                >
                  <SelectTrigger className="w-20">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[0, 1, 2, 3, 4].map((w) => (
                      <SelectItem key={w} value={String(w)}>{w}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            ))}
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={isPending}>Cancel</Button>
          <Button onClick={handleSave} disabled={isPending}>
            {isPending ? "Saving…" : "Save Question"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

// ---------------------------------------------------------------------------
// Question table row
// ---------------------------------------------------------------------------

function QuestionRow({
  question,
  onEdit,
}: {
  question: AuditQuestionPublic
  onEdit: (q: AuditQuestionPublic) => void
}) {
  const qc = useQueryClient()
  const [expanded, setExpanded] = useState(false)

  const deactivateMut = useMutation({
    mutationFn: () => QuestionsService.deactivateQuestion({ questionId: question.id }),
    onSuccess: () => {
      toast.success(`Question ${question.question_code} deactivated`)
      qc.invalidateQueries({ queryKey: ["questions"] })
    },
    onError: () => toast.error("Failed to deactivate"),
  })

  return (
    <>
      <tr className="border-b border-border/60 hover:bg-muted/30 transition-colors">
        <td className="py-3 px-4 font-mono text-xs">{question.question_code}</td>
        <td className="py-3 px-4">
          <Badge variant="outline">{question.process}</Badge>
        </td>
        <td className="py-3 px-4">
          <Badge variant="secondary">{question.level}</Badge>
        </td>
        <td className="py-3 px-4 text-xs text-muted-foreground max-w-xs truncate">
          {question.question_text}
        </td>
        <td className="py-3 px-4">
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
            question.is_active
              ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
              : "bg-muted text-muted-foreground"
          }`}>
            {question.is_active ? "Active" : "Inactive"}
          </span>
        </td>
        <td className="py-3 px-4">
          <div className="flex items-center gap-1 justify-end">
            <Button
              size="icon"
              variant="ghost"
              className="h-7 w-7"
              onClick={() => setExpanded((e) => !e)}
              title="Toggle options"
            >
              {expanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
            </Button>
            <Button
              size="icon"
              variant="ghost"
              className="h-7 w-7"
              onClick={() => onEdit(question)}
              title="Edit"
            >
              <Pencil className="h-3.5 w-3.5" />
            </Button>
            {question.is_active && (
              <Button
                size="icon"
                variant="ghost"
                className="h-7 w-7 text-destructive hover:text-destructive"
                onClick={() => deactivateMut.mutate()}
                disabled={deactivateMut.isPending}
                title="Deactivate"
              >
                <PowerOff className="h-3.5 w-3.5" />
              </Button>
            )}
          </div>
        </td>
      </tr>
      {expanded && (
        <tr className="bg-muted/20">
          <td colSpan={6} className="px-6 py-3">
            <div className="flex flex-col gap-1">
              {(question.options ?? [])
                .sort((a: AuditOptionPublic, b: AuditOptionPublic) => a.label.localeCompare(b.label))
                .map((opt: AuditOptionPublic) => (
                  <div key={opt.id} className="flex gap-3 text-xs">
                    <span className="font-bold w-4 shrink-0">{opt.label}</span>
                    <span className="flex-1 text-muted-foreground">{opt.option_text}</span>
                    <span className="text-muted-foreground">weight {opt.weight}</span>
                  </div>
                ))}
            </div>
          </td>
        </tr>
      )}
    </>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------

function QuestionBankPage() {
  const [filterProcess, setFilterProcess] = useState<ProcessEnum | "all">("all")
  const [filterLevel, setFilterLevel] = useState<AspiceLevelEnum | "all">("all")
  const [filterActive, setFilterActive] = useState<"all" | "active" | "inactive">("active")
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingQuestion, setEditingQuestion] = useState<AuditQuestionPublic | null>(null)

  const { data: questions = [], isLoading } = useQuery({
    queryKey: ["questions", filterProcess, filterLevel, filterActive],
    queryFn: () =>
      QuestionsService.listQuestions({
        process: filterProcess !== "all" ? filterProcess : undefined,
        level: filterLevel !== "all" ? filterLevel : undefined,
        isActive: filterActive === "all" ? undefined : filterActive === "active",
        limit: 200,
      }),
  })

  const openAdd = () => {
    setEditingQuestion(null)
    setDialogOpen(true)
  }

  const openEdit = (q: AuditQuestionPublic) => {
    setEditingQuestion(q)
    setDialogOpen(true)
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex flex-col gap-1">
          <h1 className="text-2xl font-bold tracking-tight">Question Bank</h1>
          <p className="text-muted-foreground">
            Manage ASPICE assessment questions. Deactivated questions are excluded from new sessions.
          </p>
        </div>
        <Button onClick={openAdd} className="gap-2">
          <Plus className="h-4 w-4" />
          Add Question
        </Button>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <Select
          value={filterProcess}
          onValueChange={(v) => setFilterProcess(v as ProcessEnum | "all")}
        >
          <SelectTrigger className="w-36">
            <SelectValue placeholder="Process" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All processes</SelectItem>
            {PROCESSES.map((p) => <SelectItem key={p} value={p}>{p}</SelectItem>)}
          </SelectContent>
        </Select>

        <Select
          value={filterLevel}
          onValueChange={(v) => setFilterLevel(v as AspiceLevelEnum | "all")}
        >
          <SelectTrigger className="w-32">
            <SelectValue placeholder="Level" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All levels</SelectItem>
            {LEVELS.map((l) => <SelectItem key={l} value={l}>{l}</SelectItem>)}
          </SelectContent>
        </Select>

        <Select value={filterActive} onValueChange={(v) => setFilterActive(v as typeof filterActive)}>
          <SelectTrigger className="w-32">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All status</SelectItem>
            <SelectItem value="active">Active only</SelectItem>
            <SelectItem value="inactive">Inactive only</SelectItem>
          </SelectContent>
        </Select>

        <span className="text-sm text-muted-foreground self-center ml-auto">
          {questions.length} question{questions.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* Table */}
      {isLoading ? (
        <div className="flex flex-col gap-2">
          {Array.from({ length: 6 }).map((_, i) => <Skeleton key={i} className="h-12 w-full" />)}
        </div>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-border">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-muted/50 border-b border-border">
                <th className="py-3 px-4 text-left font-medium text-muted-foreground">Code</th>
                <th className="py-3 px-4 text-left font-medium text-muted-foreground">Process</th>
                <th className="py-3 px-4 text-left font-medium text-muted-foreground">Level</th>
                <th className="py-3 px-4 text-left font-medium text-muted-foreground">Question</th>
                <th className="py-3 px-4 text-left font-medium text-muted-foreground">Status</th>
                <th className="py-3 px-4 text-right font-medium text-muted-foreground">Actions</th>
              </tr>
            </thead>
            <tbody>
              {questions.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-muted-foreground">
                    No questions match the current filters.
                  </td>
                </tr>
              ) : (
                questions.map((q) => (
                  <QuestionRow key={q.id} question={q} onEdit={openEdit} />
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      <QuestionFormDialog
        open={dialogOpen}
        editing={editingQuestion}
        onClose={() => {
          setDialogOpen(false)
          setEditingQuestion(null)
        }}
      />
    </div>
  )
}
