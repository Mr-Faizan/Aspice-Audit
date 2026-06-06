import { Trash2 } from "lucide-react"
import type { Control } from "react-hook-form"
import { Button } from "@/components/ui/button"
import {
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import type { QuizFormData } from "./schema"

interface OptionFieldProps {
  qIndex: number
  oIndex: number
  control: Control<QuizFormData>
  onRemove: () => void
  canRemove: boolean
}

export function OptionField({
  qIndex,
  oIndex,
  control,
  onRemove,
  canRemove,
}: OptionFieldProps) {
  const label = String.fromCharCode(65 + oIndex)

  return (
    <FormField
      control={control}
      name={`questions.${qIndex}.options.${oIndex}.text`}
      render={({ field }) => (
        <FormItem>
          <FormControl>
            <div className="flex items-center gap-2">
              <span className="w-5 shrink-0 text-sm text-muted-foreground">
                {label}.
              </span>
              <Input placeholder={`Option ${label}`} {...field} />
              {canRemove && (
                <Button
                  variant="ghost"
                  size="icon"
                  type="button"
                  onClick={onRemove}
                  className="h-8 w-8 shrink-0"
                >
                  <Trash2 className="h-3.5 w-3.5 text-muted-foreground" />
                </Button>
              )}
            </div>
          </FormControl>
          <FormMessage className="pl-7" />
        </FormItem>
      )}
    />
  )
}
