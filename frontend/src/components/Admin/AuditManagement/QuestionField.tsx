import { Plus, Trash2 } from "lucide-react"
import { useFieldArray, useWatch, type Control } from "react-hook-form"
import { Button } from "@/components/ui/button"
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import type { QuizFormData } from "./schema"
import { OptionField } from "./OptionField"

interface QuestionFieldProps {
  qIndex: number
  control: Control<QuizFormData>
  onRemove: () => void
}

export function QuestionField({ qIndex, control, onRemove }: QuestionFieldProps) {
  const {
    fields: optionFields,
    append,
    remove,
  } = useFieldArray({
    control,
    name: `questions.${qIndex}.options`,
  })

  const watchedOptions = useWatch({
    control,
    name: `questions.${qIndex}.options`,
  })

  return (
    <div className="grid gap-4 rounded-lg border p-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold">Question {qIndex + 1}</span>
        <Button
          variant="ghost"
          size="icon"
          type="button"
          onClick={onRemove}
          className="h-8 w-8 text-destructive hover:text-destructive"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>

      <FormField
        control={control}
        name={`questions.${qIndex}.questionText`}
        render={({ field }) => (
          <FormItem>
            <FormLabel>
              Question <span className="text-destructive">*</span>
            </FormLabel>
            <FormControl>
              <Textarea
                placeholder="Enter the question text..."
                rows={2}
                {...field}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <div>
        <FormLabel>
          Options <span className="text-destructive">*</span>
        </FormLabel>
        <div className="mt-2 grid gap-2">
          {optionFields.map((opt, oIndex) => (
            <OptionField
              key={opt.id}
              qIndex={qIndex}
              oIndex={oIndex}
              control={control}
              onRemove={() => remove(oIndex)}
              canRemove={optionFields.length > 2}
            />
          ))}
        </div>
        {optionFields.length < 6 && (
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="mt-2 h-8 text-xs text-muted-foreground"
            onClick={() => append({ text: "" })}
          >
            <Plus className="mr-1 h-3 w-3" />
            Add Option
          </Button>
        )}
      </div>

      <FormField
        control={control}
        name={`questions.${qIndex}.correctAnswer`}
        render={({ field }) => (
          <FormItem>
            <FormLabel>
              Correct Answer <span className="text-destructive">*</span>
            </FormLabel>
            <Select onValueChange={field.onChange} value={field.value}>
              <FormControl>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select the correct answer" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                {watchedOptions?.map((opt, i) =>
                  opt.text ? (
                    <SelectItem
                      key={i}
                      value={String.fromCharCode(97 + i)}
                    >
                      {String.fromCharCode(65 + i)}. {opt.text}
                    </SelectItem>
                  ) : null,
                )}
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        )}
      />

      <div className="grid grid-cols-2 gap-4">
        <FormField
          control={control}
          name={`questions.${qIndex}.explanation`}
          render={({ field }) => (
            <FormItem>
              <FormLabel>Explanation (optional)</FormLabel>
              <FormControl>
                <Input
                  placeholder="Explain why this answer is correct..."
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={control}
          name={`questions.${qIndex}.points`}
          render={({ field }) => (
            <FormItem>
              <FormLabel>Points</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  min={1}
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </div>
    </div>
  )
}
