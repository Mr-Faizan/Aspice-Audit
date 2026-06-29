import enum
import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import DateTime, JSON
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


class StakeholderRoleEnum(str, enum.Enum):
    software_developer = "software_developer"
    software_architect = "software_architect"
    project_manager = "project_manager"
    qa_engineer = "qa_engineer"
    test_engineer = "test_engineer"
    team_lead = "team_lead"
    aspice_assessor = "aspice_assessor"


class ProcessEnum(str, enum.Enum):
    SWE1 = "SWE1"
    SWE2 = "SWE2"
    SWE3 = "SWE3"
    SWE4 = "SWE4"
    SWE5 = "SWE5"
    SWE6 = "SWE6"


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    stakeholder_role: StakeholderRoleEnum = Field(default=StakeholderRoleEnum.software_developer)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)
    stakeholder_role: StakeholderRoleEnum = Field(default=StakeholderRoleEnum.software_developer)


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
    id: int | None = Field(default=None, primary_key=True)
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
    audit_sessions: list["AuditSession"] = Relationship(back_populates="user", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int
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
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: int = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int
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
# ASPICE Audit — Question & Option Models
# ===========================================================================

class AspiceLevelEnum(str, enum.Enum):
    L1 = "L1"  # Performed
    L2 = "L2"  # Managed
    L3 = "L3"  # Established


class AuditQuestion(SQLModel, table=True):
    """One assessment question for a specific ASPICE process & level."""
    __tablename__ = "auditquestion"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    # Human-readable code, e.g. "SWE1_L1_01"
    question_code: str = Field(max_length=50, unique=True, index=True)
    base_practice_id: str = Field(max_length=50)  # e.g. "SWE.1.BP1"

    process: ProcessEnum                           # SWE1 … SWE6
    level: AspiceLevelEnum                         # L1 / L2 / L3
    # Stored as JSON array of StakeholderRoleEnum values
    stakeholders: list = Field(default=[], sa_type=JSON)
    question_text: str = Field(max_length=2048)
    recommendation_logic: str | None = Field(default=None, max_length=2048)
    is_active: bool = Field(default=True)

    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    options: list["AuditOption"] = Relationship(back_populates="question", cascade_delete=True)


class AuditOption(SQLModel, table=True):
    """One answer option for an AuditQuestion, carrying a risk weight 0–4."""
    __tablename__ = "auditoption"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(
        foreign_key="auditquestion.id", nullable=False, ondelete="CASCADE"
    )
    label: str = Field(max_length=5)              # "A" | "B" | "C" | "D" | "E"
    option_text: str = Field(max_length=1000)
    # 0 = best / lowest risk, 4 = worst / highest risk; reward = weight / 4.0
    weight: int = Field(default=0, ge=0, le=4)

    question: AuditQuestion | None = Relationship(back_populates="options")


# ---------------------------------------------------------------------------
# Pydantic schemas — AuditQuestion / AuditOption
# ---------------------------------------------------------------------------

class AuditOptionPublic(SQLModel):
    id: int
    label: str
    option_text: str
    weight: int


class AuditQuestionPublic(SQLModel):
    id: int
    question_code: str
    base_practice_id: str
    process: ProcessEnum
    level: AspiceLevelEnum
    stakeholders: list[StakeholderRoleEnum]
    question_text: str
    recommendation_logic: str | None = None
    is_active: bool
    options: list[AuditOptionPublic] = []


# ===========================================================================
# Audit Session Models
# ===========================================================================

class SessionStatusEnum(str, enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class AuditSession(SQLModel, table=True):
    __tablename__ = "auditsession"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    status: SessionStatusEnum = Field(default=SessionStatusEnum.in_progress)
    # Ordered list of AuditQuestion IDs (integers) already presented in this session
    questions_asked: list = Field(default=[], sa_type=JSON)
    max_questions: int = Field(default=12)
    started_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    completed_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    user: User | None = Relationship(back_populates="audit_sessions")
    responses: list["AuditResponse"] = Relationship(back_populates="session", cascade_delete=True)
    weakness_result: Optional["WeaknessResult"] = Relationship(back_populates="session")


# ---------------------------------------------------------------------------
# Pydantic schemas — AuditSession
# ---------------------------------------------------------------------------

class AuditSessionPublic(SQLModel):
    id: uuid.UUID
    user_id: int
    status: SessionStatusEnum
    questions_asked: list[int]
    max_questions: int
    started_at: datetime
    completed_at: datetime | None = None


# ===========================================================================
# Audit Response Model
# ===========================================================================

class AuditResponse(SQLModel, table=True):
    __tablename__ = "auditresponse"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(foreign_key="auditsession.id", nullable=False, ondelete="CASCADE")
    question_id: int = Field(foreign_key="auditquestion.id", nullable=False)
    option_id: int = Field(foreign_key="auditoption.id", nullable=False)
    answered_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    session: AuditSession | None = Relationship(back_populates="responses")
    question: AuditQuestion | None = Relationship()
    option: AuditOption | None = Relationship()


# ---------------------------------------------------------------------------
# Pydantic schemas — AuditResponse
# ---------------------------------------------------------------------------

class AuditResponsePublic(SQLModel):
    id: uuid.UUID
    session_id: uuid.UUID
    question_id: int
    option_id: int
    answered_at: datetime


# ===========================================================================
# Weakness Result Model
# ===========================================================================

class WeaknessResult(SQLModel, table=True):
    __tablename__ = "weaknessresult"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(
        foreign_key="auditsession.id", nullable=False, unique=True, ondelete="CASCADE"
    )
    # {"SWE1": {"L1": 0.75, "L2": null}, ...}
    scores: dict = Field(default={}, sa_type=JSON)
    # e.g. ["SWE3-L2", "SWE1-L1"]
    top_weaknesses: list = Field(default=[], sa_type=JSON)
    computed_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    session: AuditSession | None = Relationship(back_populates="weakness_result")


# ---------------------------------------------------------------------------
# Pydantic schemas — WeaknessResult
# ---------------------------------------------------------------------------

class WeaknessResultPublic(SQLModel):
    id: uuid.UUID
    session_id: uuid.UUID
    scores: dict
    top_weaknesses: list[str]
    computed_at: datetime


# ===========================================================================
# Bandit Arm State Model
# ===========================================================================

class BanditArmState(SQLModel, table=True):
    __tablename__ = "banditarmstate"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    question_id: int = Field(
        foreign_key="auditquestion.id", nullable=False, unique=True
    )
    # LinUCB matrices — stored as nested lists [[...], ...]
    A_matrix: list = Field(default=[], sa_type=JSON)
    b_vector: list = Field(default=[], sa_type=JSON)
    pull_count: int = Field(default=0)
    total_reward: float = Field(default=0.0)
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationship
    question: AuditQuestion | None = Relationship()


# ---------------------------------------------------------------------------
# Pydantic schemas — BanditArmState
# ---------------------------------------------------------------------------

class BanditArmStatePublic(SQLModel):
    id: uuid.UUID
    question_id: int
    pull_count: int
    total_reward: float
    updated_at: datetime


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
    creator_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")

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
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
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
