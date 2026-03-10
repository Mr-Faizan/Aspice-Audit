import enum
import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy import DateTime, JSON
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    last_login_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    quizzes: list["Quiz"] = Relationship(back_populates="creator", cascade_delete=True)
    quiz_attempts: list["QuizAttempt"] = Relationship(back_populates="user", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None
    last_login_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# ===========================================================================
# Quiz Models
# ===========================================================================

class DifficultyEnum(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class QuizStatusEnum(str, enum.Enum):
    draft = "draft"
    published = "published"
    unpublished = "unpublished"


# ---------------------------------------------------------------------------
# Quiz — DB table
# ---------------------------------------------------------------------------

class Quiz(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1024)
    difficulty: DifficultyEnum = Field(default=DifficultyEnum.medium)
    category: str = Field(max_length=100)
    time_limit: int | None = Field(default=None)          # minutes
    passing_score: int = Field(default=70)                 # percentage
    status: QuizStatusEnum = Field(default=QuizStatusEnum.draft)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    creator_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")

    # Relationships
    creator: User | None = Relationship(back_populates="quizzes")
    questions: list["Question"] = Relationship(back_populates="quiz", cascade_delete=True)
    attempts: list["QuizAttempt"] = Relationship(back_populates="quiz", cascade_delete=True)


# ---------------------------------------------------------------------------
# Question — DB table
# ---------------------------------------------------------------------------

class Question(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    quiz_id: uuid.UUID = Field(foreign_key="quiz.id", nullable=False, ondelete="CASCADE")
    question_text: str = Field(max_length=2048)
    options: list = Field(default=[], sa_type=JSON)        # stored as JSON array
    correct_answer: str = Field(max_length=500)
    explanation: str | None = Field(default=None, max_length=2048)
    points: int = Field(default=1)
    order: int = Field(default=0)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    quiz: Quiz | None = Relationship(back_populates="questions")


# ---------------------------------------------------------------------------
# QuizAttempt — DB table
# ---------------------------------------------------------------------------

class QuizAttempt(SQLModel, table=True):
    __tablename__ = "quizattempt"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    quiz_id: uuid.UUID = Field(foreign_key="quiz.id", nullable=False, ondelete="CASCADE")
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    answers: dict = Field(default={}, sa_type=JSON)        # stored as JSON object
    score: int = Field(default=0)
    total_questions: int = Field(default=0)
    correct_answers: int = Field(default=0)
    passed: bool = Field(default=False)
    started_at: datetime = Field(sa_type=DateTime(timezone=True))  # type: ignore
    completed_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    quiz: Quiz | None = Relationship(back_populates="attempts")
    user: User | None = Relationship(back_populates="quiz_attempts")


# ---------------------------------------------------------------------------
# Pydantic schemas — Question
# ---------------------------------------------------------------------------

class QuestionCreate(SQLModel):
    question_text: str = Field(max_length=2048)
    options: list[str]
    correct_answer: str = Field(max_length=500)
    explanation: str | None = None
    points: int = Field(default=1)


class QuestionPublic(SQLModel):
    id: uuid.UUID
    quiz_id: uuid.UUID
    question_text: str
    options: list[str]
    correct_answer: str
    explanation: str | None = None
    points: int
    order: int


# ---------------------------------------------------------------------------
# Pydantic schemas — Quiz
# ---------------------------------------------------------------------------

class QuizBase(SQLModel):
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1024)
    difficulty: DifficultyEnum = DifficultyEnum.medium
    category: str = Field(max_length=100)
    time_limit: int | None = None
    passing_score: int = 70


class QuizCreate(QuizBase):
    questions: list[QuestionCreate] = []


class QuizUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1024)
    difficulty: DifficultyEnum | None = None
    category: str | None = Field(default=None, max_length=100)
    time_limit: int | None = None
    passing_score: int | None = None
    status: QuizStatusEnum | None = None
    questions: list[QuestionCreate] | None = None


class QuizPublic(QuizBase):
    id: uuid.UUID
    status: QuizStatusEnum
    creator_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
    question_count: int = 0


class QuizWithQuestions(QuizPublic):
    questions: list[QuestionPublic] = []


class QuizzesPublic(SQLModel):
    data: list[QuizPublic]
    count: int


# ---------------------------------------------------------------------------
# Pydantic schemas — QuizAttempt
# ---------------------------------------------------------------------------

class QuizAttemptPublic(SQLModel):
    id: uuid.UUID
    quiz_id: uuid.UUID
    user_id: uuid.UUID
    score: int
    total_questions: int
    correct_answers: int
    passed: bool
    started_at: datetime
    completed_at: datetime | None = None


# ---------------------------------------------------------------------------
# Statistics response schemas
# ---------------------------------------------------------------------------

class RecentAttemptPublic(SQLModel):
    id: uuid.UUID
    quiz_id: uuid.UUID
    quiz_title: str
    user_id: uuid.UUID
    user_full_name: str | None = None
    user_email: str
    score: int
    passed: bool
    completed_at: datetime | None = None


class StatisticsPublic(SQLModel):
    total_users: int
    active_users: int
    total_quizzes: int
    published_quizzes: int
    unpublished_quizzes: int
    total_attempts: int
    average_score: float
    recent_attempts: list[RecentAttemptPublic] = []


class UserStatisticsPublic(SQLModel):
    total_users: int
    active_users: int
    new_users_this_month: int
    admin_users: int
    regular_users: int


class PopularQuizPublic(SQLModel):
    id: uuid.UUID
    title: str
    attempts: int


class QuizStatisticsPublic(SQLModel):
    total_quizzes: int
    published_quizzes: int
    unpublished_quizzes: int
    quizzes_by_category: dict[str, int]
    quizzes_by_difficulty: dict[str, int]
    average_attempts_per_quiz: float
    most_popular_quizzes: list[PopularQuizPublic]
