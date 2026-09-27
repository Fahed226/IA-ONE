"""Persistance des formations sur disque (un fichier JSON par formation)."""

from __future__ import annotations

import os
import re
import threading
from pathlib import Path
from typing import List

from .models import Course

_SAFE_ID = re.compile(r"^[a-f0-9]{12}$")


class CourseStore:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root or os.environ.get("FORMATION_DATA_DIR", "data/courses"))
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _path(self, course_id: str) -> Path:
        if not _SAFE_ID.match(course_id):
            raise KeyError(course_id)
        return self.root / f"{course_id}.json"

    def save(self, course: Course) -> None:
        course.touch()
        path = self._path(course.id)
        tmp = path.with_suffix(".tmp")
        with self._lock:
            tmp.write_text(course.model_dump_json(indent=2), encoding="utf-8")
            tmp.replace(path)

    def get(self, course_id: str) -> Course:
        path = self._path(course_id)
        if not path.exists():
            raise KeyError(course_id)
        return Course.model_validate_json(path.read_text(encoding="utf-8"))

    def list(self) -> List[Course]:
        courses = [Course.model_validate_json(p.read_text(encoding="utf-8")) for p in self.root.glob("*.json")]
        return sorted(courses, key=lambda c: c.updated_at, reverse=True)

    def delete(self, course_id: str) -> None:
        path = self._path(course_id)
        if not path.exists():
            raise KeyError(course_id)
        path.unlink()
