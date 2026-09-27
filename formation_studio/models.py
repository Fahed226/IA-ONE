"""Modèles de données d'une formation complète.

Deux familles de modèles :
- les schémas « Gen* » envoyés à Claude comme format de sortie structuré
  (ils ne contiennent que ce que le modèle doit produire) ;
- les modèles « Course* » qui représentent la formation assemblée et persistée.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------- #
# Brief : ce que l'utilisateur demande
# --------------------------------------------------------------------------- #


class Level(str, Enum):
    debutant = "débutant"
    intermediaire = "intermédiaire"
    avance = "avancé"
    expert = "expert"


class CourseBrief(BaseModel):
    topic: str = Field(..., min_length=3, description="Sujet de la formation")
    audience: str = Field("Grand public", description="Public cible")
    level: Level = Level.debutant
    language: str = "français"
    duration_hours: float = Field(10, gt=0, le=500, description="Durée totale visée")
    modules_count: int = Field(6, ge=1, le=30)
    lessons_per_module: int = Field(4, ge=1, le=15)
    tone: str = "pédagogique, clair et motivant"
    goals: str = Field("", description="Objectifs ou résultats attendus par le client")
    constraints: str = Field("", description="Contraintes, outils imposés, contexte métier")
    include_quizzes: bool = True
    include_exercises: bool = True
    include_final_exam: bool = True
    include_capstone: bool = True
    include_video_scripts: bool = False
    include_slides: bool = False


# --------------------------------------------------------------------------- #
# Schémas de sortie structurée (générés par Claude)
# --------------------------------------------------------------------------- #


class GenLessonPlan(BaseModel):
    title: str
    summary: str
    objectives: List[str]
    duration_minutes: int
    format: str = Field(description="texte, vidéo, atelier pratique, étude de cas…")


class GenModulePlan(BaseModel):
    title: str
    summary: str
    objectives: List[str]
    lessons: List[GenLessonPlan]


class GenOutline(BaseModel):
    title: str
    subtitle: str
    description: str
    target_audience: str
    prerequisites: List[str]
    learning_outcomes: List[str]
    skills: List[str]
    pedagogical_approach: str
    modules: List[GenModulePlan]


class GenSection(BaseModel):
    heading: str
    content_markdown: str


class GenExample(BaseModel):
    title: str
    content_markdown: str


class GenExercise(BaseModel):
    title: str
    instructions_markdown: str
    difficulty: str
    estimated_minutes: int
    solution_markdown: str


class GenResource(BaseModel):
    title: str
    type: str = Field(description="livre, article, outil, vidéo, documentation…")
    description: str


class GenSlide(BaseModel):
    title: str
    bullets: List[str]
    speaker_notes: str


class GenLessonContent(BaseModel):
    introduction_markdown: str
    sections: List[GenSection]
    examples: List[GenExample]
    key_takeaways: List[str]
    exercises: List[GenExercise]
    common_mistakes: List[str]
    resources: List[GenResource]
    video_script_markdown: str = Field(description="Script vidéo ou chaîne vide si non demandé")
    slides: List[GenSlide] = Field(description="Diapositives ou liste vide si non demandé")


class QuestionType(str, Enum):
    single = "choix_unique"
    multiple = "choix_multiple"
    true_false = "vrai_faux"


class GenQuestion(BaseModel):
    question: str
    type: QuestionType
    options: List[str]
    correct_indexes: List[int]
    explanation: str
    bloom_level: str = Field(description="Niveau de la taxonomie de Bloom visé")


class GenQuiz(BaseModel):
    title: str
    instructions: str
    passing_score_percent: int
    questions: List[GenQuestion]


class GenRubricCriterion(BaseModel):
    criterion: str
    description: str
    points: int


class GenCapstone(BaseModel):
    title: str
    context_markdown: str
    deliverables: List[str]
    steps: List[str]
    rubric: List[GenRubricCriterion]
    estimated_hours: float


class GenGlossaryEntry(BaseModel):
    term: str
    definition: str


class GenCourseExtras(BaseModel):
    welcome_message_markdown: str
    how_to_follow_markdown: str
    glossary: List[GenGlossaryEntry]
    faq: List[GenExample]
    certification_criteria: List[str]
    conclusion_markdown: str
    marketing_pitch: str
    sales_page_bullets: List[str]


# --------------------------------------------------------------------------- #
# Formation assemblée
# --------------------------------------------------------------------------- #


def _id() -> str:
    return uuid4().hex[:12]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Lesson(BaseModel):
    id: str = Field(default_factory=_id)
    plan: GenLessonPlan
    content: Optional[GenLessonContent] = None


class Module(BaseModel):
    id: str = Field(default_factory=_id)
    title: str
    summary: str
    objectives: List[str]
    lessons: List[Lesson]
    quiz: Optional[GenQuiz] = None


class CourseStatus(str, Enum):
    draft = "brouillon"
    generating = "en_generation"
    ready = "prête"
    failed = "échec"


class Course(BaseModel):
    id: str = Field(default_factory=_id)
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)
    status: CourseStatus = CourseStatus.draft
    error: Optional[str] = None
    brief: CourseBrief
    title: str
    subtitle: str
    description: str
    target_audience: str
    prerequisites: List[str]
    learning_outcomes: List[str]
    skills: List[str]
    pedagogical_approach: str
    modules: List[Module]
    final_exam: Optional[GenQuiz] = None
    capstone: Optional[GenCapstone] = None
    extras: Optional[GenCourseExtras] = None

    def touch(self) -> None:
        self.updated_at = _now()

    @property
    def lessons_count(self) -> int:
        return sum(len(m.lessons) for m in self.modules)

    @property
    def total_minutes(self) -> int:
        return sum(lesson.plan.duration_minutes for m in self.modules for lesson in m.lessons)

    def find_lesson(self, lesson_id: str) -> tuple[Module, Lesson]:
        for module in self.modules:
            for lesson in module.lessons:
                if lesson.id == lesson_id:
                    return module, lesson
        raise KeyError(lesson_id)

    def find_module(self, module_id: str) -> Module:
        for module in self.modules:
            if module.id == module_id:
                return module
        raise KeyError(module_id)

    @classmethod
    def from_outline(cls, brief: CourseBrief, outline: GenOutline) -> "Course":
        return cls(
            brief=brief,
            title=outline.title,
            subtitle=outline.subtitle,
            description=outline.description,
            target_audience=outline.target_audience,
            prerequisites=outline.prerequisites,
            learning_outcomes=outline.learning_outcomes,
            skills=outline.skills,
            pedagogical_approach=outline.pedagogical_approach,
            modules=[
                Module(
                    title=m.title,
                    summary=m.summary,
                    objectives=m.objectives,
                    lessons=[Lesson(plan=lp) for lp in m.lessons],
                )
                for m in outline.modules
            ],
        )
