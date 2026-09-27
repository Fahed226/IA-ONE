"""Ligne de commande : `python -m formation_studio …`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .exporters import EXPORTERS, slugify
from .generator import CourseGenerator
from .llm import DEFAULT_MODEL, ClaudeLLM
from .models import CourseBrief, Level
from .storage import CourseStore


def _generate(args: argparse.Namespace) -> int:
    brief = CourseBrief(
        topic=args.topic,
        audience=args.audience,
        level=Level(args.level),
        language=args.language,
        duration_hours=args.hours,
        modules_count=args.modules,
        lessons_per_module=args.lessons,
        goals=args.goals,
        constraints=args.constraints,
        include_video_scripts=args.video,
        include_slides=args.slides,
    )
    store = CourseStore(args.data_dir)

    def show(progress, course):
        print(f"[{progress.percent:3d} %] {progress.step} {progress.log[-1] if progress.log else ''}", flush=True)
        if course is not None:
            store.save(course)

    course = CourseGenerator(ClaudeLLM(model=args.model, effort=args.effort), max_workers=args.workers).generate_course(
        brief, show
    )
    store.save(course)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for fmt in args.formats:
        _, ext, export = EXPORTERS[fmt]
        path = out / f"{slugify(course.title)}.{ext}"
        path.write_bytes(export(course))
        print(f"→ {path}")
    print(f"Formation « {course.title} » : {course.status.value} (id {course.id})")
    return 0 if course.error is None else 1


def _export(args: argparse.Namespace) -> int:
    course = CourseStore(args.data_dir).get(args.course_id)
    _, ext, export = EXPORTERS[args.format]
    path = Path(args.out) / f"{slugify(course.title)}.{ext}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(export(course))
    print(f"→ {path}")
    return 0


def _serve(args: argparse.Namespace) -> int:
    import uvicorn

    from .app import create_app

    llm_factory = None
    if args.demo:
        from .demo import DemoLLM

        llm_factory = DemoLLM
        print("Mode démo : contenu factice, aucun appel à l'API Claude.")
    uvicorn.run(create_app(CourseStore(args.data_dir), llm_factory), host=args.host, port=args.port)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="formation_studio", description="Studio IA de création de formations en ligne")
    parser.add_argument("--data-dir", default=None, help="Dossier de stockage des formations")
    sub = parser.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("serve", help="Lancer l'interface web")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8000)
    s.add_argument("--demo", action="store_true", help="Contenu factice, sans clé API (pour tester l'interface)")
    s.set_defaults(func=_serve)

    g = sub.add_parser("generate", help="Générer une formation complète")
    g.add_argument("topic")
    g.add_argument("--audience", default="Grand public")
    g.add_argument("--level", default="débutant", choices=[lv.value for lv in Level])
    g.add_argument("--language", default="français")
    g.add_argument("--hours", type=float, default=10)
    g.add_argument("--modules", type=int, default=6)
    g.add_argument("--lessons", type=int, default=4)
    g.add_argument("--goals", default="")
    g.add_argument("--constraints", default="")
    g.add_argument("--video", action="store_true", help="Inclure des scripts vidéo")
    g.add_argument("--slides", action="store_true", help="Inclure des diapositives")
    g.add_argument("--model", default=DEFAULT_MODEL)
    g.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    g.add_argument("--workers", type=int, default=4)
    g.add_argument("--formats", nargs="+", default=["html", "markdown", "scorm"], choices=list(EXPORTERS))
    g.add_argument("--out", default="exports")
    g.set_defaults(func=_generate)

    e = sub.add_parser("export", help="Exporter une formation existante")
    e.add_argument("course_id")
    e.add_argument("--format", default="html", choices=list(EXPORTERS))
    e.add_argument("--out", default="exports")
    e.set_defaults(func=_export)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
