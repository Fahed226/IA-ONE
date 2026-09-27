import io
import json
import time
import zipfile

import pytest
from fastapi.testclient import TestClient

from formation_studio.app import create_app
from formation_studio.demo import DemoLLM
from formation_studio.exporters import to_html, to_markdown_zip, to_scorm_zip
from formation_studio.generator import CourseGenerator
from formation_studio.models import CourseBrief, CourseStatus
from formation_studio.storage import CourseStore


@pytest.fixture
def brief():
    return CourseBrief(topic="Gestion de projet agile", modules_count=3, lessons_per_module=2, include_slides=True)


def test_full_generation(brief):
    llm = DemoLLM()
    updates = []
    course = CourseGenerator(llm).generate_course(brief, lambda p, c: updates.append(p.percent))

    assert course.status == CourseStatus.ready
    assert len(course.modules) == 3
    assert all(len(m.lessons) == 2 for m in course.modules)
    assert all(lesson.content for m in course.modules for lesson in m.lessons)
    assert all(m.quiz for m in course.modules)
    assert course.final_exam and course.capstone and course.extras
    # 1 programme + 6 leçons + 3 quiz + examen + projet + extras
    assert len(llm.calls) == 13
    assert updates[-1] == 100
    assert course.modules[0].lessons[0].content.slides
    assert course.modules[0].lessons[0].content.video_script_markdown == ""


def test_options_disable_parts(brief):
    brief = brief.model_copy(
        update={"include_quizzes": False, "include_final_exam": False, "include_capstone": False, "include_exercises": False}
    )
    course = CourseGenerator(DemoLLM()).generate_course(brief)
    assert not any(m.quiz for m in course.modules)
    assert course.final_exam is None and course.capstone is None
    assert course.modules[0].lessons[0].content.exercises == []


class FlakyLLM(DemoLLM):
    def __init__(self):
        super().__init__()
        self.fail = True

    def generate(self, prompt, schema):
        if self.fail and schema.__name__ == "GenCapstone":
            raise RuntimeError("boom")
        return super().generate(prompt, schema)


def test_failure_then_resume(brief):
    llm = FlakyLLM()
    gen = CourseGenerator(llm)
    course = gen.generate_course(brief)
    assert course.status == CourseStatus.failed
    assert course.capstone is None and course.extras is not None

    llm.fail = False
    before = len(llm.calls)
    course = gen.generate_course(brief, course=course)
    assert course.status == CourseStatus.ready
    assert course.capstone is not None
    assert len(llm.calls) == before + 1  # seul l'élément manquant est régénéré


def test_exports(brief):
    course = CourseGenerator(DemoLLM()).generate_course(brief)

    page = to_html(course)
    assert "<section id=\"m1l1\">" in page and "form class=\"quiz\"" in page and "LMSInitialize" in page

    with zipfile.ZipFile(io.BytesIO(to_scorm_zip(course))) as z:
        assert set(z.namelist()) == {"imsmanifest.xml", "index.html"}
        assert "adlcp:scormtype=\"sco\"" in z.read("imsmanifest.xml").decode()

    with zipfile.ZipFile(io.BytesIO(to_markdown_zip(course))) as z:
        names = z.namelist()
        assert any(n.endswith("00-programme.md") for n in names)
        assert sum("/module-" in n for n in names) == 3 * (1 + 2 + 1)
        assert any(n.endswith("91-projet-final.md") for n in names)


def test_store_roundtrip(tmp_path, brief):
    store = CourseStore(tmp_path)
    course = CourseGenerator(DemoLLM()).generate_course(brief)
    store.save(course)
    assert store.get(course.id).title == course.title
    assert [c.id for c in store.list()] == [course.id]
    with pytest.raises(KeyError):
        store.get("../../etc/passwd")
    store.delete(course.id)
    assert store.list() == []


def test_api_flow(tmp_path):
    client = TestClient(create_app(CourseStore(tmp_path), DemoLLM))

    outline = client.post("/api/outline", json={"topic": "Photographie", "modules_count": 2, "lessons_per_module": 2})
    assert outline.status_code == 200
    course = outline.json()
    assert all(lesson["content"] is None for m in course["modules"] for lesson in m["lessons"])

    course["modules"][0]["title"] = "Titre modifié"
    assert client.put(f"/api/courses/{course['id']}", json=course).status_code == 200

    job_id = client.post(f"/api/courses/{course['id']}/generate").json()["job_id"]
    for _ in range(100):
        job = client.get(f"/api/jobs/{job_id}").json()
        if job["status"] != "en_cours":
            break
        time.sleep(0.05)
    assert job["status"] == "terminé", job

    full = client.get(f"/api/courses/{course['id']}").json()
    assert full["status"] == "prête"
    assert full["modules"][0]["title"] == "Titre modifié"

    lesson_id = full["modules"][0]["lessons"][0]["id"]
    r = client.post(f"/api/courses/{course['id']}/lessons/{lesson_id}/regenerate", json={"instructions": "plus simple"})
    assert r.status_code == 200

    for fmt in ["json", "markdown", "html", "scorm"]:
        r = client.get(f"/api/courses/{course['id']}/export/{fmt}")
        assert r.status_code == 200 and r.content, fmt
    assert json.loads(client.get(f"/api/courses/{course['id']}/export/json").content)["id"] == course["id"]

    assert len(client.get("/api/courses").json()) == 1
    assert client.get("/").status_code == 200
    assert client.delete(f"/api/courses/{course['id']}").status_code == 204
    assert client.get(f"/api/courses/{course['id']}").status_code == 404


def test_api_validation(tmp_path):
    client = TestClient(create_app(CourseStore(tmp_path), DemoLLM))
    assert client.post("/api/courses", json={"topic": "x"}).status_code == 422
    assert client.get("/api/courses/abcdefabcdef/export/pdf").status_code == 400
