import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

interface MaxAttemptsModalProps {
  isOpen: boolean
  attemptCount: number
  onClose: () => void
}

export function MaxAttemptsModal({ isOpen, attemptCount, onClose }: MaxAttemptsModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Maximum Attempts Reached</DialogTitle>
          <DialogDescription>
            You have already attempted this quiz {attemptCount} time
            {attemptCount !== 1 ? "s" : ""}. You cannot take this quiz anymore.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button onClick={onClose}>OK</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

interface StartQuizModalProps {
  isOpen: boolean
  quizTitle: string
  questionCount: number
  timeLimit: number
  attemptsRemaining: number
  isLoading?: boolean
  onClose: () => void
  onConfirm: () => void
}

export function StartQuizModal({
  isOpen,
  quizTitle,
  questionCount,
  timeLimit,
  attemptsRemaining,
  isLoading = false,
  onClose,
  onConfirm,
}: StartQuizModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Start Audit: {quizTitle}</DialogTitle>
          <DialogDescription asChild>
            <div className="space-y-2 pt-1 text-sm text-muted-foreground">
              <p>
                This quiz contains <strong className="text-foreground">{questionCount}</strong>{" "}
                questions with a time limit of{" "}
                <strong className="text-foreground">{timeLimit} minutes</strong>.
              </p>
              <p>
                You have{" "}
                <strong className="text-foreground">
                  {attemptsRemaining} {attemptsRemaining === 1 ? "attempt" : "attempts"}
                </strong>{" "}
                remaining.
              </p>
              <p>Once you start, the timer will begin and cannot be paused. Are you ready?</p>
            </div>
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button onClick={onConfirm} disabled={isLoading}>
            {isLoading ? "Starting..." : "Start Audit"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
