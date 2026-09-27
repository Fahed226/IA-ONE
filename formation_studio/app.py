"""API web + interface du studio de formation."""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .exporters import EXPORTERS, slugify
from .generator import CourseGenerator, Progress
from .llm import ClaudeLLM, StructuredLLM
from .models import Course, CourseBrief, CourseStatus
from .storage import CourseStore

STATIC_DIR = Path(__file__).parent / "static"


@dataclass
class Job:
    id: str
    status: str = "en_cours"  # en_cours | terminé | échec
    course_id: Optional[str] = None
    percent: int = 0
    step: str = "En attente"
    log: list[str] = field(default_factory=list)
    error: Optional[str] = None


class JobManager:
    def __init__(self) -> None:
        self.jobs: Dict[str, Job] = {}
        self._lock = threading.Lock()

    def start(self, work: Callable[[Job], None]) -> Job:
        job = Job(id=uuid.uuid4().hex[:12])
        with self._lock:
            self.jobs[job.id] = job

        def run() -> None:
            try:
                work(job)
                job.status = "terminé"
            except Exception as exc:
                job.status = "échec"
                job.error = str(exc)

        threading.Thread(target=run, daemon=True).start()
        return job

    def get(self, job_id: str) -> Job:
        with self._lock:
            if job_id not in self.jobs:
                raise KeyError(job_id)
            return self.jobs[job_id]


class RegenerateLessonRequest(BaseModel):
    instructions: str = ""


class CourseSummary(BaseModel):
    id: str
    title: str
    subtitle: str
    status: CourseStatus
    modules: int
    lessons: int
    minutes: int
    updated_at: str


def create_app(
    store: CourseStore | None = None,
    llm_factory: Callable[[], StructuredLLM] | None = None,
) -> FastAPI:
    store = store or CourseStore()
    llm_factory = llm_factory or ClaudeLLM
    jobs = JobManager()
    app = FastAPI(title="Formation Studio", version="1.0.0")

    def generator() -> CourseGenerator:
        return CourseGenerator(llm_factory())

    def load(course_id: str) -> Course:
        try:
            return store.get(course_id)
        except KeyError:
            raise HTTPException(404, "Formation introuvable") from None

    def progress_updater(job: Job):
        def update(p: Progress, course: Course | None) -> None:
            job.percent, job.step, job.log = p.percent, p.step, list(p.log[-50:])
            if course is not None:
                job.course_id = course.id
                store.save(course)

        return update

    # -- formations ---------------------------------------------------------- #

    @app.get("/api/courses", response_model=list[CourseSummary])
    def list_courses():
        return [
            CourseSummary(
                id=c.id,
                title=c.title,
                subtitle=c.subtitle,
                status=c.status,
                modules=len(c.modules),
                lessons=c.lessons_count,
                minutes=c.total_minutes,
                updated_at=c.updated_at,
            )
            for c in store.list()
        ]

    @app.post("/api/courses", status_code=202)
    def create_course(brief: CourseBrief):
        """Lance la génération complète d'une formation (tâche de fond)."""

        def work(job: Job) -> None:
            course = generator().generate_course(brief, progress_updater(job))
            store.save(course)
            if course.status == CourseStatus.failed:
                raise RuntimeError(course.error)

        return {"job_id": jobs.start(work).id}

    @app.post("/api/outline")
    def create_outline(brief: CourseBrief):
        """Génère uniquement le programme (pour validation avant rédaction)."""
        course = generator().generate_outline(brief)
        store.save(course)
        return course

    @app.get("/api/courses/{course_id}")
    def get_course(course_id: str):
        return load(course_id)

    @app.put("/api/courses/{course_id}")
    def update_course(course_id: str, course: Course):
        """Enregistre les modifications manuelles faites dans l'éditeur."""
        load(course_id)
        if course.id != course_id:
            raise HTTPException(400, "Identifiant incohérent")
        store.save(course)
        return course

    @app.delete("/api/courses/{course_id}", status_code=204)
    def delete_course(course_id: str):
        load(course_id)
        store.delete(course_id)

    @app.post("/api/courses/{course_id}/generate", status_code=202)
    def resume_course(course_id: str):
        """Complète tout ce qui manque (leçons, quiz, examen…) — utile après validation du programme ou un échec."""
        course = load(course_id)

        def work(job: Job) -> None:
            result = generator().generate_course(course.brief, progress_updater(job), course=course)
            store.save(result)
            if result.status == CourseStatus.failed:
                raise RuntimeError(result.error)

        return {"job_id": jobs.start(work).id}

    @app.post("/api/courses/{course_id}/lessons/{lesson_id}/regenerate")
    def regenerate_lesson(course_id: str, lesson_id: str, body: RegenerateLessonRequest):
        course = load(course_id)
        try:
            generator().generate_lesson(course, lesson_id, body.instructions)
        except KeyError:
            raise HTTPException(404, "Leçon introuvable") from None
        store.save(course)
        return course

    @app.post("/api/courses/{course_id}/modules/{module_id}/quiz")
    def regenerate_quiz(course_id: str, module_id: str):
        course = load(course_id)
        try:
            generator().generate_module_quiz(course, module_id)
        except KeyError:
            raise HTTPException(404, "Module introuvable") from None
        store.save(course)
        return course

    @app.get("/api/courses/{course_id}/export/{fmt}")
    def export_course(course_id: str, fmt: str):
        if fmt not in EXPORTERS:
            raise HTTPException(400, f"Format inconnu. Formats : {', '.join(EXPORTERS)}")
        course = load(course_id)
        media_type, ext, export = EXPORTERS[fmt]
        filename = f"{slugify(course.title)}.{ext}"
        return Response(
            export(course),
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    # -- tâches -------------------------------------------------------------- #

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str):
        try:
            return jobs.get(job_id)
        except KeyError:
            raise HTTPException(404, "Tâche introuvable") from None

    # -- interface ----------------------------------------------------------- #

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(STATIC_DIR / "index.html")

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    return app
