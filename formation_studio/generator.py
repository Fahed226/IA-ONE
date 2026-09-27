"""Pipeline de génération d'une formation complète.

Étapes :
1. Programme (syllabus) : modules, leçons, objectifs.
2. Contenu de chaque leçon (en parallèle).
3. Quiz de chaque module.
4. Examen final, projet capstone, éléments d'accompagnement.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Callable, Optional

from . import prompts
from .llm import StructuredLLM
from .models import (
    Course,
    CourseBrief,
    CourseStatus,
    GenCapstone,
    GenCourseExtras,
    GenLessonContent,
    GenOutline,
    GenQuiz,
)


@dataclass
class Progress:
    total: int = 0
    done: int = 0
    step: str = ""
    log: list[str] = field(default_factory=list)

    @property
    def percent(self) -> int:
        return int(100 * self.done / self.total) if self.total else 0


ProgressCallback = Callable[[Progress, Optional[Course]], None]


class CourseGenerator:
    def __init__(self, llm: StructuredLLM, max_workers: int = 4) -> None:
        self.llm = llm
        self.max_workers = max_workers

    # -- étapes unitaires ---------------------------------------------------- #

    def generate_outline(self, brief: CourseBrief) -> Course:
        outline = self.llm.generate(prompts.outline_prompt(brief), GenOutline)
        return Course.from_outline(brief, outline)

    def generate_lesson(self, course: Course, lesson_id: str, extra_instructions: str = "") -> None:
        module, lesson = course.find_lesson(lesson_id)
        lesson.content = self.llm.generate(
            prompts.lesson_prompt(course, module, lesson, extra_instructions), GenLessonContent
        )

    def generate_module_quiz(self, course: Course, module_id: str) -> None:
        module = course.find_module(module_id)
        module.quiz = self.llm.generate(prompts.quiz_prompt(course, module), GenQuiz)

    def generate_final_exam(self, course: Course) -> None:
        course.final_exam = self.llm.generate(prompts.final_exam_prompt(course), GenQuiz)

    def generate_capstone(self, course: Course) -> None:
        course.capstone = self.llm.generate(prompts.capstone_prompt(course), GenCapstone)

    def generate_extras(self, course: Course) -> None:
        course.extras = self.llm.generate(prompts.extras_prompt(course), GenCourseExtras)

    # -- pipeline complet ---------------------------------------------------- #

    def build_tasks(self, course: Course) -> list[tuple[str, Callable[[], None]]]:
        brief = course.brief
        tasks: list[tuple[str, Callable[[], None]]] = []
        for module in course.modules:
            for lesson in module.lessons:
                if lesson.content is None:
                    tasks.append(
                        (f"Leçon « {lesson.plan.title} »", lambda lid=lesson.id: self.generate_lesson(course, lid))
                    )
            if brief.include_quizzes and module.quiz is None:
                tasks.append(
                    (f"Quiz « {module.title} »", lambda mid=module.id: self.generate_module_quiz(course, mid))
                )
        if brief.include_final_exam and course.final_exam is None:
            tasks.append(("Examen final", lambda: self.generate_final_exam(course)))
        if brief.include_capstone and course.capstone is None:
            tasks.append(("Projet final", lambda: self.generate_capstone(course)))
        if course.extras is None:
            tasks.append(("Bienvenue, glossaire, FAQ, marketing", lambda: self.generate_extras(course)))
        return tasks

    def generate_course(
        self,
        brief: CourseBrief,
        on_progress: ProgressCallback | None = None,
        course: Course | None = None,
    ) -> Course:
        """Génère (ou reprend) une formation complète. `course` permet de reprendre après un échec."""
        progress = Progress(step="Conception du programme")
        notify = on_progress or (lambda p, c: None)

        if course is None:
            progress.total = 1
            notify(progress, None)
            course = self.generate_outline(brief)
            progress.log.append(f"Programme conçu : {len(course.modules)} modules, {course.lessons_count} leçons")

        course.status = CourseStatus.generating
        course.error = None
        tasks = self.build_tasks(course)
        progress.total = len(tasks) + 1
        progress.done = 1
        progress.step = "Rédaction des contenus"
        notify(progress, course)

        errors: list[str] = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {pool.submit(fn): label for label, fn in tasks}
            for future in as_completed(futures):
                label = futures[future]
                progress.done += 1
                try:
                    future.result()
                    progress.log.append(f"✓ {label}")
                except Exception as exc:  # une tâche en échec n'arrête pas les autres
                    errors.append(f"{label} : {exc}")
                    progress.log.append(f"✗ {label} : {exc}")
                notify(progress, course)

        if errors:
            course.status = CourseStatus.failed
            course.error = f"{len(errors)} élément(s) en échec — relancez la génération pour compléter."
        else:
            course.status = CourseStatus.ready
        progress.step = "Terminé"
        notify(progress, course)
        return course
