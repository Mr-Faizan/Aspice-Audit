# Migration Plan: Quiz Features from Smarty-Quiz to Aspice-Audit

**Date:** March 10, 2026  
**Goal:** Port Dashboard, Quizzes, and Statistics admin/user pages from `smarty-quiz` into `Aspice-Audit`.

---

## 1. Project Comparison Summary

### Aspice-Audit (Target)
- **Frontend:** React 19 + TypeScript + TanStack Router + TanStack Query + Tailwind CSS + Radix UI
- **Backend:** FastAPI + SQLModel + Alembic + PostgreSQL
- **Auth:** JWT-based (own implementation, token in localStorage)
- **Folder:** `frontend/src/routes/` (file-based routing), `frontend/src/components/`
- **OpenAPI Client:** Auto-generated at `frontend/src/client/` via `@hey-api/openapi-ts`
- **Existing Quiz/Statistics:** Already has backend routes `/api/v1/quizzes` and `/api/v1/statistics` with fully implemented models and endpoints

### Smarty-Quiz (Source)
- **Frontend:** React 19 + TypeScript + React Router v7 + TanStack Query + Tailwind CSS + Material-UI
- **Backend:** Express.js + Drizzle ORM + PostgreSQL
- **Auth:** Better Auth
- **Folder:** `client/src/pages/`, `client/src/features/`, `client/src/layouts/`
- **API:** Manual fetch wrappers at `client/src/features/api/` calling Express routes
- **Structure:** Feature-based (`features/admin/`, `features/quiz/`) with page wrappers

---

## 2. Backend Compatibility Analysis

### ✅ What Already Exists in Aspice-Audit Backend

**`backend/app/api/routes/quizzes.py`**
- `GET /api/v1/quizzes/` — List all quizzes (admin only, with filters: search, category, difficulty)
- `POST /api/v1/quizzes/` — Create quiz + questions
- `PATCH /api/v1/quizzes/{id}` — Update quiz + replace questions
- `DELETE /api/v1/quizzes/{id}` — Delete quiz
- `PATCH /api/v1/quizzes/{id}/publish` — Toggle published/unpublished

**`backend/app/api/routes/statistics.py`**
- `GET /api/v1/statistics/` — Dashboard summary (total users, quizzes, attempts, avg score, recent attempts)
- `GET /api/v1/statistics/users` — User statistics
- `GET /api/v1/statistics/quizzes` — Quiz statistics (most popular quizzes, category/difficulty breakdowns)

**Models in `backend/app/models.py`**
- `Quiz`, `Question`, `QuizAttempt` — Full SQLModel schemas
- Enums: `DifficultyEnum`, `QuizStatusEnum`
- Pydantic: `QuizCreate`, `QuizUpdate`, `QuizPublic`, `QuizWithQuestions`, `StatisticsPublic`, `QuizStatisticsPublic`, `UserStatisticsPublic`

### 🔴 What's Missing (Must Add)

1. **User Quiz Endpoints** (in `smarty-quiz/server/src/routes/quiz.ts` but missing in Aspice):
   - `GET /api/v1/quizzes/published` — List published quizzes for users (not admin)
   - `GET /api/v1/quizzes/categories` — Get unique quiz categories
   - `GET /api/v1/quizzes/{id}` — Get quiz by ID (sanitized for users, without correct answers until submission)
   - `POST /api/v1/quizzes/{id}/start` — Start quiz session (time tracking)
   - `POST /api/v1/quizzes/{id}/submit` — Submit quiz attempt
   - `GET /api/v1/quizzes/attempts/user/{userId}` — List user attempts (history)
   - `GET /api/v1/quizzes/attempt/{attemptId}` — Get specific attempt result

2. **ActiveQuizSession Model** (optional, for time tracking)
   - Used by smarty-quiz to validate quiz timeouts
   - Can be added if the frontend timer is not sufficient

### Backend Contract Alignment

**Smarty-Quiz API Shape:**
```typescript
// Admin routes (/api/admin/...)
fetchAdminQuizzes(filters?: QuizListFilters): Promise<Quiz[]>
createQuiz(quiz: CreateQuizRequest): Promise<Quiz>
updateQuiz(quizId: string, quiz: UpdateQuizRequest): Promise<Quiz>
deleteQuiz(quizId: string): Promise<void>
togglePublishQuiz(quizId: string, isPublished: boolean): Promise<Quiz>
fetchDashboardStats(): Promise<DashboardStats>
fetchUserStats(): Promise<UserStats>
fetchQuizStats(): Promise<QuizStats>

// User routes (/api/quizzes/...)
fetchQuizzes(filters?: QuizListFilters): Promise<Quiz[]>
fetchQuizCategories(): Promise<string[]>
fetchQuizById(quizId: string): Promise<Quiz>
startQuizSession(quizId: string): Promise<{id, startedAt, expiresAt}>
submitQuiz(quizId: string, data: SubmitQuizRequest): Promise<QuizAttempt>
fetchUserQuizAttempts(userId: string): Promise<QuizAttempt[]>
fetchQuizAttemptById(attemptId: string): Promise<QuizAttempt>
```

**Aspice-Audit Current API Shape (from `frontend/src/client/sdk.gen.ts`):**
```typescript
// Admin routes
QuizzesService.readQuizzes(data: {skip?, limit?, search?, category?, difficulty?}): Promise<QuizzesPublic>
QuizzesService.createQuiz(data: {requestBody: QuizCreate}): Promise<QuizWithQuestions>
QuizzesService.updateQuiz(data: {id: string, requestBody: QuizUpdate}): Promise<QuizWithQuestions>
QuizzesService.deleteQuiz(data: {id: string}): Promise<Message>
QuizzesService.togglePublishQuiz(data: {id: string}): Promise<QuizPublic>

StatisticsService.getDashboardSummary(): Promise<StatisticsPublic>
StatisticsService.getUserStatistics(): Promise<UserStatisticsPublic>
StatisticsService.getQuizStatistics(): Promise<QuizStatisticsPublic>
```

**Compatibility Status:**
- Admin quiz management: ✅ Nearly identical (need to add category/difficulty filter support in togglePublish if needed)
- Statistics: ✅ Fully compatible
- User quiz flow: ❌ Missing entirely (must add 7 new endpoints)

---

## 3. Frontend Compatibility Analysis

### Component Library Differences

| Feature | Smarty-Quiz | Aspice-Audit | Migration Action |
|---------|-------------|--------------|------------------|
| UI Library | Material-UI (MUI) | Radix UI + custom | **Replace MUI components with Radix** |
| Box, Typography, Button, Card | `@mui/material` | Use Tailwind + Radix primitives | Rewrite JSX structure |
| Icons | `@mui/icons-material` | `lucide-react` | Replace icon imports |
| Charts | `@mui/x-charts` (PieChart, BarChart) | ❌ Not installed | **Install Recharts or keep MUI charts** |
| Modals | `@mui/material/Modal` | Custom `components/ui/dialog.tsx` | Adapt modal logic |
| Toasts/Notifications | `sonner` | `sonner` | ✅ Compatible |
| Forms | `react-hook-form` + `zod` | `react-hook-form` + `zod` | ✅ Compatible |

### Routing Differences

| Aspect | Smarty-Quiz | Aspice-Audit | Migration Action |
|--------|-------------|--------------|------------------|
| Library | React Router v7 | TanStack Router | **Replace all route hooks** |
| Navigation | `useNavigate()` from `react-router` | `useNavigate()` from `@tanstack/react-router` | Update imports |
| Route Structure | Centralized in `lib/router/index.tsx` | File-based in `src/routes/` | Create new route files |
| Lazy Loading | `lazy(() => import(...))` | TanStack auto-splitting | Remove manual lazy wrappers |
| Layout Wrapping | `<AdminLayout>`, `<UserLayout>` | `_layout.tsx` parent route | Nest routes under `_layout` |

### State Management & Data Fetching

| Aspect | Smarty-Quiz | Aspice-Audit | Compatibility |
|--------|-------------|--------------|---------------|
| Query Library | `@tanstack/react-query` | `@tanstack/react-query` | ✅ Compatible |
| API Client | Manual fetch in `features/api/` | Auto-generated `client/sdk.gen.ts` | Replace fetch calls with SDK |
| Auth Context | Better Auth hooks | Custom `useAuth()` hook | Adapt auth calls |

### Custom Hooks

- `useDebounceValue()` (smarty-quiz) → Create in aspice-audit (missing)
- `useQuizAttempts()` → Will need to create
- `useQuizTimer()` → Will need to create

---

## 4. File-by-File Mapping

### **Source Files** (from `smarty-quiz/client/src/`)

#### **Admin Pages** (Thin Wrappers)
```
pages/admin/Dashboard.tsx       → routes/_layout/admin-dashboard.tsx
pages/admin/Quizzes.tsx         → routes/_layout/admin-quizzes.tsx
pages/admin/Statistics.tsx      → routes/_layout/admin-statistics.tsx
```

#### **User Pages**
```
pages/quiz/Quizzes.tsx          → routes/_layout/quizzes.tsx
pages/quiz/TakeQuiz.tsx         → routes/_layout/quiz.$id.tsx
pages/quiz/Result.tsx           → routes/_layout/quiz.$id.result.$resultId.tsx
pages/quiz/History.tsx          → routes/_layout/quiz-history.tsx
```

#### **Admin Feature Components** (Dashboard)
```
features/admin/components/dashboard/
  index.tsx                     → components/Quiz/Admin/Dashboard/index.tsx
  DashboardDetails.tsx          → components/Quiz/Admin/Dashboard/DashboardDetails.tsx
  StatisticCard.tsx             → components/Quiz/Admin/Dashboard/StatisticCard.tsx
  UserActivity.tsx              → components/Quiz/Admin/Dashboard/UserActivity.tsx
  QuizStatus.tsx                → components/Quiz/Admin/Dashboard/QuizStatus.tsx
```

#### **Admin Feature Components** (Quiz Management)
```
features/admin/components/quiz-management/
  index.tsx                     → components/Quiz/Admin/QuizManagement/index.tsx
  AdminQuizzes.tsx              → components/Quiz/Admin/QuizManagement/AdminQuizzes.tsx
  QuizModal.tsx                 → components/Quiz/Admin/QuizManagement/QuizModal.tsx
  Question.tsx                  → components/Quiz/Admin/QuizManagement/Question.tsx
  QuestionOptions.tsx           → components/Quiz/Admin/QuizManagement/QuestionOptions.tsx
```

#### **Admin Feature Components** (Statistics)
```
features/admin/components/statistics/
  index.tsx                     → components/Quiz/Admin/Statistics/index.tsx
  MostPopularQuizzes.tsx        → components/Quiz/Admin/Statistics/MostPopularQuizzes.tsx
```

#### **User Feature Components** (Quiz List)
```
features/quiz/components/quiz-list/
  index.tsx                     → components/Quiz/User/QuizList/index.tsx
  QuizList.tsx                  → components/Quiz/User/QuizList/QuizList.tsx
```

#### **User Feature Components** (Take Quiz)
```
features/quiz/components/take-quiz/
  index.tsx                     → components/Quiz/User/TakeQuiz/index.tsx
  QuizQuestionCard.tsx          → components/Quiz/User/TakeQuiz/QuizQuestionCard.tsx
  QuizQuestionProgress.tsx      → components/Quiz/User/TakeQuiz/QuizQuestionProgress.tsx
  QuizHeader.tsx                → components/Quiz/User/TakeQuiz/QuizHeader.tsx
  MaxAttemptsReachedPage.tsx    → components/Quiz/User/TakeQuiz/MaxAttemptsReachedPage.tsx
  NoActiveSessionPage.tsx       → components/Quiz/User/TakeQuiz/NoActiveSessionPage.tsx
```

#### **User Feature Components** (Result)
```
features/quiz/components/result/
  index.tsx                     → components/Quiz/User/Result/index.tsx
  QuestionBreakdown.tsx         → components/Quiz/User/Result/QuestionBreakdown.tsx
```

#### **User Feature Components** (History)
```
features/quiz/components/QuizHistory.tsx → components/Quiz/User/QuizHistory.tsx
```

#### **Shared Components**
```
features/shared/QuizFilters.tsx → components/Quiz/Shared/QuizFilters.tsx
```

#### **Modals**
```
features/quiz/components/modals/quiz.tsx → components/Quiz/Shared/Modals.tsx
```

#### **Hooks**
```
hooks/useDebounce.ts            → hooks/useDebounce.ts (create new)
hooks/useMountEffect.ts         → hooks/useMountEffect.ts (create new)
hooks/useUnmountEffect.ts       → hooks/useUnmountEffect.ts (create new)
features/quiz/hooks/useQuizTimer.ts → hooks/Quiz/useQuizTimer.ts
features/quiz/hooks/useQuizAttempts.ts → hooks/Quiz/useQuizAttempts.ts
```

#### **Helpers**
```
features/admin/helpers/
  validator.ts                  → lib/quiz/validator.ts
  getStatisticsChartData.ts     → lib/quiz/getStatisticsChartData.ts
  index.ts (CATEGORIES, difficultyColors, getInitialQuizFormData)
                                → lib/quiz/helpers.ts
```

#### **Types**
```
types/Quiz.ts                   → types/quiz.ts (merge with existing client types)
types/User.ts (DashboardStats, UserStats, QuizStats)
                                → Already in client/types.gen.ts (check compatibility)
features/types/index.ts         → types/quiz-props.ts
```

#### **API Functions** (Replace with SDK)
```
features/api/admin.ts           → Use QuizzesService.* and StatisticsService.*
features/api/quiz.ts            → Use QuizzesService.* (after adding user endpoints)
```

#### **Layouts** (Not Needed)
```
layouts/admin/index.tsx         → Already exists via _layout.tsx
layouts/user/index.tsx          → Already exists via _layout.tsx
```

---

## 5. Migration Complexity Assessment

### ✅ **Can Copy Mostly As-Is**
- Type definitions (`types/Quiz.ts`, `features/types/`)
- Helper functions (`getStatisticsChartData`, `validator`, `CATEGORIES`)
- Custom hooks logic (`useDebounce`, `useQuizTimer`)

### 🟡 **Requires Moderate Adaptation**
- **All React components** — Replace MUI with Radix/Tailwind
- **API calls** — Replace `fetchJson()` calls with `QuizzesService.*` methods
- **Navigation** — Replace `react-router` hooks with `@tanstack/react-router`
- **Auth checks** — Use `useAuth()` from Aspice instead of Better Auth

### 🔴 **Requires Heavy Rewrite**
- **Charts** — MUI X Charts not installed; must either:
  1. Install `@mui/x-charts` (adds ~200KB)
  2. Replace with Recharts
  3. Use plain SVG/Canvas
- **Modal dialogs** — Replace MUI Dialogs with Radix Dialog
- **Form components** — Replace MUI TextField/Select with Shadcn/ui equivalents

### 📦 **New Dependencies Needed**
```json
{
  "@mui/material": "^7.3.6",         // If keeping MUI components (not recommended)
  "@mui/x-charts": "^8.19.0",        // For PieChart, BarChart (or use Recharts)
  "@emotion/react": "^11.14.0",      // Required by MUI
  "@emotion/styled": "^11.14.1"      // Required by MUI
}
```
**OR** (recommended):
```json
{
  "recharts": "^2.15.0"              // Alternative charting library
}
```

---

## 6. Step-by-Step Migration Plan

### **Phase 0: Preparation** ✅ (Current)
1. ✅ Document architecture differences
2. ✅ Identify missing backend endpoints
3. ✅ Map all source files to target locations
4. ⚠️ Decide on chart library (MUI X Charts vs Recharts)

### **Phase 1: Foundation** (Start Here)
**Goal:** Set up folder structure, install dependencies, create minimal stubs.

**Steps:**
1. Create folder structure in `Aspice-Audit/frontend/src/`:
   ```
   components/Quiz/
     Admin/
       Dashboard/
       QuizManagement/
       Statistics/
     User/
       QuizList/
       TakeQuiz/
       Result/
     Shared/
   hooks/Quiz/
   lib/quiz/
   types/quiz-props.ts
   ```

2. Install dependencies:
   ```bash
   cd frontend
   bun add recharts
   # OR if keeping MUI
   # bun add @mui/material @mui/x-charts @emotion/react @emotion/styled
   ```

3. Create utility hooks:
   - `hooks/useDebounce.ts`
   - `hooks/useMountEffect.ts`
   - `hooks/useUnmountEffect.ts`

4. Copy type definitions:
   - `types/quiz.ts` (merge with existing `client/types.gen.ts`)
   - `types/quiz-props.ts` (component prop types)

5. Copy helpers:
   - `lib/quiz/validator.ts`
   - `lib/quiz/helpers.ts` (CATEGORIES, difficultyColors)
   - `lib/quiz/getStatisticsChartData.ts`

6. Create placeholder route files (empty components):
   - `routes/_layout/admin-dashboard.tsx`
   - `routes/_layout/admin-quizzes.tsx`
   - `routes/_layout/admin-statistics.tsx`
   - `routes/_layout/quizzes.tsx`

---

### **Phase 2: Backend User Endpoints**
**Goal:** Add missing user quiz endpoints so frontend can consume them.

**New Routes (`backend/app/api/routes/quizzes.py`):**
1. `GET /quizzes/published` — List published quizzes (non-admin)
2. `GET /quizzes/categories` — Categories list
3. `GET /quizzes/{id}/detail` — Quiz detail for user (sanitized)
4. `POST /quizzes/{id}/start` — Start session
5. `POST /quizzes/{id}/submit` — Submit attempt
6. `GET /attempts/user/{userId}` — User history
7. `GET /attempts/{attemptId}` — Attempt detail

**Models to Add:**
- `ActiveQuizSession` (optional table for timeout tracking)
- `QuizAttemptPublic` (already exists ✅)

**After Adding:**
1. Run Alembic migration: `alembic revision --autogenerate -m "Add user quiz endpoints"`
2. Regenerate frontend client: `bash scripts/generate-client.sh`

---

### **Phase 3: Admin Dashboard**
**Goal:** Migrate admin Dashboard page with stat cards.

**Components to Port:**
1. `components/Quiz/Admin/Dashboard/index.tsx` (main)
2. `components/Quiz/Admin/Dashboard/DashboardDetails.tsx`
3. `components/Quiz/Admin/Dashboard/StatisticCard.tsx`
4. `components/Quiz/Admin/Dashboard/UserActivity.tsx`
5. `components/Quiz/Admin/Dashboard/QuizStatus.tsx`

**API Calls:**
- Replace `fetchDashboardStats()` with `StatisticsService.getDashboardSummary()`

**UI Changes:**
- Replace `<Box>`, `<Card>`, `<Typography>` with Tailwind classes + `<div>`
- Replace MUI `<Chip>` with custom badge component
- Replace `@mui/icons-material/TrendingUp` with `lucide-react` icons

**Route:**
- `routes/_layout/admin-dashboard.tsx`

---

### **Phase 4: Admin Quizzes (CRUD)**
**Goal:** Migrate Quiz Management (list, create, edit, delete, publish).

**Components to Port:**
1. `components/Quiz/Admin/QuizManagement/index.tsx` (main)
2. `components/Quiz/Admin/QuizManagement/AdminQuizzes.tsx` (list view)
3. `components/Quiz/Admin/QuizManagement/QuizModal.tsx` (create/edit modal)
4. `components/Quiz/Admin/QuizManagement/Question.tsx` (question editor)
5. `components/Quiz/Admin/QuizManagement/QuestionOptions.tsx` (option editor)
6. `components/Quiz/Shared/QuizFilters.tsx` (search/filter bar)

**API Calls:**
- Replace `fetchAdminQuizzes()` with `QuizzesService.readQuizzes()`
- Replace `createQuiz()` with `QuizzesService.createQuiz()`
- Replace `updateQuiz()` with `QuizzesService.updateQuiz()`
- Replace `deleteQuiz()` with `QuizzesService.deleteQuiz()`
- Replace `togglePublishQuiz()` with `QuizzesService.togglePublishQuiz()`

**UI Changes:**
- Replace MUI Modal with Radix Dialog
- Replace MUI TextField with Shadcn Input
- Replace MUI Select with Shadcn Select
- Replace MUI Button with Shadcn Button
- Replace MUI IconButton with custom icon wrapper

**Route:**
- `routes/_layout/admin-quizzes.tsx`

---

### **Phase 5: Admin Statistics**
**Goal:** Migrate Statistics page with charts.

**Components to Port:**
1. `components/Quiz/Admin/Statistics/index.tsx` (main)
2. `components/Quiz/Admin/Statistics/MostPopularQuizzes.tsx` (table)

**API Calls:**
- Replace `fetchQuizStats()` with `StatisticsService.getQuizStatistics()`
- Replace `fetchUserStats()` with `StatisticsService.getUserStatistics()`

**Charts:**
- Replace `<PieChart>` from `@mui/x-charts` with Recharts `<PieChart>` (or keep MUI if installed)
- Replace `<BarChart>` from `@mui/x-charts` with Recharts `<BarChart>`

**Helper:**
- Use `lib/quiz/getStatisticsChartData.ts` to transform data

**Route:**
- `routes/_layout/admin-statistics.tsx`

---

### **Phase 6: User Quiz List**
**Goal:** Allow users to browse and start quizzes.

**Components to Port:**
1. `components/Quiz/User/QuizList/index.tsx` (main wrapper)
2. `components/Quiz/User/QuizList/QuizList.tsx` (card grid)
3. `components/Quiz/Shared/QuizFilters.tsx` (reuse from Phase 4)
4. `components/Quiz/Shared/Modals.tsx` (start quiz modal, max attempts)

**Hooks:**
- `hooks/Quiz/useQuizAttempts.ts`

**API Calls:**
- Replace `fetchQuizzes()` with `QuizzesService.readQuizzes()` (after adding `/published` endpoint)
- Replace `startQuizSession()` with new SDK method

**Route:**
- `routes/_layout/quizzes.tsx`

---

### **Phase 7: Take Quiz (Timer + Submit)**
**Goal:** Allow users to take a quiz with timer and submit answers.

**Components to Port:**
1. `components/Quiz/User/TakeQuiz/index.tsx` (main)
2. `components/Quiz/User/TakeQuiz/QuizQuestionCard.tsx` (question display)
3. `components/Quiz/User/TakeQuiz/QuizQuestionProgress.tsx` (progress bar)
4. `components/Quiz/User/TakeQuiz/QuizHeader.tsx` (timer display)
5. `components/Quiz/User/TakeQuiz/MaxAttemptsReachedPage.tsx`
6. `components/Quiz/User/TakeQuiz/NoActiveSessionPage.tsx`

**Hooks:**
- `hooks/Quiz/useQuizTimer.ts`

**API Calls:**
- Replace `fetchQuizById()` with new SDK method
- Replace `submitQuiz()` with new SDK method

**Route:**
- `routes/_layout/quiz.$id.tsx`

---

### **Phase 8: Quiz Result**
**Goal:** Show quiz result with breakdown.

**Components to Port:**
1. `components/Quiz/User/Result/index.tsx` (main)
2. `components/Quiz/User/Result/QuestionBreakdown.tsx` (show correct/incorrect)

**API Calls:**
- Replace `fetchQuizAttemptById()` with new SDK method

**Route:**
- `routes/_layout/quiz.$id.result.$resultId.tsx`

---

### **Phase 9: Quiz History**
**Goal:** Show user's past quiz attempts.

**Components to Port:**
1. `components/Quiz/User/QuizHistory.tsx`

**API Calls:**
- Replace `fetchUserQuizAttempts()` with new SDK method

**Route:**
- `routes/_layout/quiz-history.tsx`

---

### **Phase 10: Integration & Testing**
**Goal:** Wire up navigation, update sidebar, test end-to-end.

**Steps:**
1. Update `components/Sidebar/AppSidebar.tsx`:
   - Add "Quizzes" menu item for all users
   - Add "Quiz Admin" submenu for superusers (Dashboard, Manage Quizzes, Statistics)

2. Update `routes/_layout.tsx` to include new routes

3. Add protection middleware:
   - Admin routes: `beforeLoad: checkSuperuser`
   - User routes: `beforeLoad: checkAuthenticated`

4. Manual testing:
   - Admin creates quiz → publishes → user takes quiz → sees result → checks history
   - Admin sees dashboard stats update
   - Admin sees statistics charts

---

## 7. First Implementation Step (Minimal Risk)

**Goal:** Establish foundation without breaking existing functionality.

### **Step 0.1: Create Folder Structure**
```bash
mkdir -p frontend/src/components/Quiz/{Admin/{Dashboard,QuizManagement,Statistics},User/{QuizList,TakeQuiz,Result},Shared}
mkdir -p frontend/src/hooks/Quiz
mkdir -p frontend/src/lib/quiz
```

### **Step 0.2: Copy Utility Hooks**
**File:** `frontend/src/hooks/useDebounce.ts`
```typescript
import { useEffect, useState } from "react"

export function useDebounceValue<T>(initialValue: T, delay: number = 500): [T, T, (value: T) => void] {
  const [value, setValue] = useState<T>(initialValue)
  const [debouncedValue, setDebouncedValue] = useState<T>(initialValue)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return [value, debouncedValue, setValue]
}
```

### **Step 0.3: Copy Type Definitions**
**File:** `frontend/src/types/quiz-props.ts`
```typescript
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
```

### **Step 0.4: Create Placeholder Admin Route**
**File:** `frontend/src/routes/_layout/admin-quizzes.tsx`
```tsx
import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/admin-quizzes")({
  component: AdminQuizzes,
  head: () => ({
    meta: [
      {
        title: "Quiz Management - Aspice Audit",
      },
    ],
  }),
})

function AdminQuizzes() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Quiz Management</h1>
        <p className="text-muted-foreground text-lg">
          Create, edit, and manage ASPICE audit quizzes
        </p>
      </div>
      <div className="rounded-lg border border-dashed p-8 text-center">
        <p className="text-muted-foreground">
          Coming soon: Admin quiz management interface
        </p>
      </div>
    </div>
  )
}
```

### **Step 0.5: Update Sidebar to Include Placeholder Link**
**File:** `frontend/src/components/Sidebar/AppSidebar.tsx`

Add import:
```tsx
import { GraduationCap } from "lucide-react"
```

Update `baseItems`:
```tsx
const baseItems: Item[] = [
  { icon: Home, title: "Dashboard", path: "/dashboard" },
  { icon: Briefcase, title: "Items", path: "/items" },
  { icon: GraduationCap, title: "Quiz Admin", path: "/admin-quizzes" }, // NEW
]
```

### **Step 0.6: Verify Changes**
```bash
cd frontend
bun run dev
```

**Expected Result:**
- Sidebar shows "Quiz Admin" link
- Clicking it opens `/admin-quizzes` route with placeholder message
- No errors in console
- Existing routes (Dashboard, Items, Admin) still work

**This completes Phase 0 ("Foundation - Minimal Risk").**

---

## 8. Summary

### ✅ Frontend Components Reusable With Adaptation
- All React components can be migrated with MUI → Radix/Tailwind conversion
- TanStack Query code is 100% compatible
- react-hook-form + zod validation logic is reusable

### 🔴 Backend Requires New Endpoints
- Must add 7 user quiz endpoints before user pages can function
- Admin endpoints are already complete ✅

### 📦 Dependencies Decision Required
- **Option A:** Install MUI X Charts (~200KB, faster migration)
- **Option B:** Use Recharts (~150KB, more flexible, better Tailwind integration)
- **Recommendation:** Use Recharts for consistency with Aspice's Tailwind/Radix stack

### 🛠️ Migration Effort Estimate
- **Phase 1 (Foundation):** 2 hours
- **Phase 2 (Backend Endpoints):** 4 hours
- **Phase 3 (Admin Dashboard):** 3 hours
- **Phase 4 (Admin Quizzes CRUD):** 6 hours
- **Phase 5 (Admin Statistics):** 4 hours
- **Phase 6 (User Quiz List):** 4 hours
- **Phase 7 (Take Quiz):** 5 hours
- **Phase 8 (Quiz Result):** 3 hours
- **Phase 9 (Quiz History):** 2 hours
- **Phase 10 (Integration & Testing):** 4 hours
- **Total:** ~37 hours (5 working days)

---

## 9. Next Steps

1. ✅ Review this migration plan
2. ✅ Execute Phase 1 Step 0.1-0.6 (DONE in this session)
3. ⏭️ Decide on chart library (MUI X Charts vs Recharts)
4. ⏭️ Implement Phase 2 (Backend User Endpoints)
5. ⏭️ Continue with Phase 3-10 incrementally

**Current Implementation Status:** Phase 1 (Step 0.6) — Foundation placeholders created ✅
