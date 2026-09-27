"""Exports d'une formation : JSON, Markdown (zip), site HTML autonome, paquet SCORM 1.2."""

from __future__ import annotations

import html
import io
import json
import re
import unicodedata
import zipfile
from typing import Iterable, List

import markdown as md

from .models import Course, GenQuiz, Lesson, Module

# --------------------------------------------------------------------------- #
# Utilitaires
# --------------------------------------------------------------------------- #


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:max_len].strip("-") or "formation"


def _md(text: str) -> str:
    return md.markdown(text or "", extensions=["tables", "fenced_code", "sane_lists"])


def _e(text: object) -> str:
    return html.escape(str(text))


def _bullets(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _fmt_minutes(minutes: int) -> str:
    h, m = divmod(minutes, 60)
    return f"{h} h {m:02d}" if h else f"{m} min"


# --------------------------------------------------------------------------- #
# JSON
# --------------------------------------------------------------------------- #


def to_json(course: Course) -> str:
    return course.model_dump_json(indent=2)


# --------------------------------------------------------------------------- #
# Markdown
# --------------------------------------------------------------------------- #


def quiz_to_markdown(quiz: GenQuiz, with_answers: bool = True) -> str:
    out = [f"## {quiz.title}", "", quiz.instructions, "", f"*Seuil de réussite : {quiz.passing_score_percent} %*", ""]
    for i, q in enumerate(quiz.questions, 1):
        out.append(f"**{i}. {q.question}** _({q.type.value})_")
        out.append("")
        for j, option in enumerate(q.options):
            mark = "x" if with_answers and j in q.correct_indexes else " "
            out.append(f"- [{mark}] {option}")
        if with_answers:
            out += ["", f"> {q.explanation}"]
        out.append("")
    return "\n".join(out)


def lesson_to_markdown(course: Course, module: Module, lesson: Lesson) -> str:
    m_idx = course.modules.index(module) + 1
    l_idx = module.lessons.index(lesson) + 1
    p = lesson.plan
    out = [
        f"# Leçon {m_idx}.{l_idx} — {p.title}",
        "",
        f"*Durée : {_fmt_minutes(p.duration_minutes)} · Format : {p.format}*",
        "",
        "### Objectifs",
        _bullets(p.objectives),
        "",
    ]
    c = lesson.content
    if c is None:
        out += ["> Contenu non encore généré.", ""]
        return "\n".join(out)
    out += [c.introduction_markdown, ""]
    for section in c.sections:
        out += [f"## {section.heading}", "", section.content_markdown, ""]
    if c.examples:
        out += ["## Exemples et études de cas", ""]
        for ex in c.examples:
            out += [f"### {ex.title}", "", ex.content_markdown, ""]
    out += ["## À retenir", _bullets(c.key_takeaways), ""]
    if c.common_mistakes:
        out += ["## Erreurs fréquentes", _bullets(c.common_mistakes), ""]
    if c.exercises:
        out += ["## Exercices pratiques", ""]
        for ex in c.exercises:
            out += [
                f"### {ex.title} ({ex.difficulty}, ~{ex.estimated_minutes} min)",
                "",
                ex.instructions_markdown,
                "",
                "<details><summary>Voir la solution</summary>",
                "",
                ex.solution_markdown,
                "",
                "</details>",
                "",
            ]
    if c.resources:
        out += ["## Pour aller plus loin", ""]
        out += [f"- **{r.title}** ({r.type}) — {r.description}" for r in c.resources]
        out.append("")
    if c.video_script_markdown.strip():
        out += ["## Script vidéo", "", c.video_script_markdown, ""]
    if c.slides:
        out += ["## Diapositives", ""]
        for i, slide in enumerate(c.slides, 1):
            out += [f"### Diapo {i} — {slide.title}", _bullets(slide.bullets), "", f"*Notes : {slide.speaker_notes}*", ""]
    return "\n".join(out)


def syllabus_markdown(course: Course) -> str:
    out = [
        f"# {course.title}",
        f"### {course.subtitle}",
        "",
        course.description,
        "",
        f"**Public :** {course.target_audience}  ",
        f"**Niveau :** {course.brief.level.value}  ",
        f"**Durée :** {_fmt_minutes(course.total_minutes)} · {len(course.modules)} modules · {course.lessons_count} leçons",
        "",
        "## Prérequis",
        _bullets(course.prerequisites),
        "",
        "## Ce que vous saurez faire",
        _bullets(course.learning_outcomes),
        "",
        "## Compétences développées",
        _bullets(course.skills),
        "",
        "## Approche pédagogique",
        course.pedagogical_approach,
        "",
        "## Programme",
    ]
    for i, module in enumerate(course.modules, 1):
        out += ["", f"### Module {i} — {module.title}", module.summary, ""]
        for j, lesson in enumerate(module.lessons, 1):
            out.append(f"- {i}.{j} {lesson.plan.title} ({_fmt_minutes(lesson.plan.duration_minutes)})")
    return "\n".join(out) + "\n"


def to_markdown_zip(course: Course) -> bytes:
    buf = io.BytesIO()
    root = slugify(course.title)
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{root}/00-programme.md", syllabus_markdown(course))
        if course.extras:
            x = course.extras
            z.writestr(
                f"{root}/01-bienvenue.md",
                f"# Bienvenue\n\n{x.welcome_message_markdown}\n\n# Comment suivre cette formation\n\n{x.how_to_follow_markdown}\n",
            )
        for i, module in enumerate(course.modules, 1):
            mdir = f"{root}/module-{i:02d}-{slugify(module.title, 40)}"
            z.writestr(
                f"{mdir}/00-presentation.md",
                f"# Module {i} — {module.title}\n\n{module.summary}\n\n## Objectifs\n{_bullets(module.objectives)}\n",
            )
            for j, lesson in enumerate(module.lessons, 1):
                z.writestr(
                    f"{mdir}/{j:02d}-{slugify(lesson.plan.title, 40)}.md", lesson_to_markdown(course, module, lesson)
                )
            if module.quiz:
                z.writestr(f"{mdir}/99-quiz.md", quiz_to_markdown(module.quiz))
        if course.final_exam:
            z.writestr(f"{root}/90-examen-final.md", quiz_to_markdown(course.final_exam))
        if course.capstone:
            cp = course.capstone
            rubric = "\n".join(f"| {r.criterion} | {r.description} | {r.points} |" for r in cp.rubric)
            z.writestr(
                f"{root}/91-projet-final.md",
                f"# Projet final — {cp.title}\n\n*Durée estimée : {cp.estimated_hours} h*\n\n{cp.context_markdown}\n\n"
                f"## Livrables\n{_bullets(cp.deliverables)}\n\n## Étapes\n"
                + "\n".join(f"{k}. {s}" for k, s in enumerate(cp.steps, 1))
                + f"\n\n## Grille d'évaluation\n\n| Critère | Description | Points |\n|---|---|---|\n{rubric}\n",
            )
        if course.extras:
            x = course.extras
            glossary = "\n".join(f"- **{g.term}** : {g.definition}" for g in x.glossary)
            faq = "\n\n".join(f"### {f.title}\n\n{f.content_markdown}" for f in x.faq)
            z.writestr(f"{root}/92-glossaire.md", f"# Glossaire\n\n{glossary}\n")
            z.writestr(f"{root}/93-faq.md", f"# FAQ\n\n{faq}\n")
            z.writestr(
                f"{root}/94-certification-et-conclusion.md",
                f"# Certification\n\n{_bullets(x.certification_criteria)}\n\n# Conclusion\n\n{x.conclusion_markdown}\n",
            )
            z.writestr(
                f"{root}/95-page-de-vente.md",
                f"# {course.title}\n\n{x.marketing_pitch}\n\n{_bullets(x.sales_page_bullets)}\n",
            )
    return buf.getvalue()


# --------------------------------------------------------------------------- #
# Site HTML autonome (lecteur de formation interactif)
# --------------------------------------------------------------------------- #


def _quiz_html(quiz: GenQuiz, quiz_id: str) -> str:
    parts = [
        f'<form class="quiz" data-quiz="{_e(quiz_id)}" data-pass="{quiz.passing_score_percent}">',
        f"<p>{_e(quiz.instructions)}</p>",
        f'<p class="muted">Seuil de réussite : {quiz.passing_score_percent} %</p>',
    ]
    for i, q in enumerate(quiz.questions):
        kind = "checkbox" if len(q.correct_indexes) > 1 else "radio"
        correct = ",".join(str(c) for c in q.correct_indexes)
        parts.append(f'<fieldset class="question" data-correct="{correct}"><legend>{i + 1}. {_e(q.question)}</legend>')
        if kind == "checkbox":
            parts.append('<p class="muted">Plusieurs réponses possibles.</p>')
        for j, option in enumerate(q.options):
            parts.append(f'<label><input type="{kind}" name="q{i}" value="{j}"> {_e(option)}</label>')
        parts.append(f'<p class="explanation" hidden>{_e(q.explanation)}</p></fieldset>')
    parts.append('<button type="submit">Valider mes réponses</button><p class="result" aria-live="polite"></p></form>')
    return "\n".join(parts)


def _pages(course: Course) -> List[tuple[str, str, str]]:
    """Retourne la liste (id, titre de navigation, html) des pages du lecteur."""
    pages: List[tuple[str, str, str]] = []
    intro = _md(syllabus_markdown(course))
    if course.extras:
        intro = (
            f"<h1>{_e(course.title)}</h1>{_md(course.extras.welcome_message_markdown)}"
            f"<h2>Comment suivre cette formation</h2>{_md(course.extras.how_to_follow_markdown)}<hr>" + intro
        )
    pages.append(("accueil", "Accueil & programme", intro))
    for i, module in enumerate(course.modules, 1):
        pages.append(
            (
                f"m{i}",
                f"Module {i} — {module.title}",
                f"<h1>Module {i} — {_e(module.title)}</h1>{_md(module.summary)}"
                f"<h2>Objectifs</h2>{_md(_bullets(module.objectives))}",
            )
        )
        for j, lesson in enumerate(module.lessons, 1):
            pages.append((f"m{i}l{j}", f"{i}.{j} {lesson.plan.title}", _md(lesson_to_markdown(course, module, lesson))))
        if module.quiz:
            pages.append(
                (
                    f"m{i}q",
                    f"Quiz du module {i}",
                    f"<h1>{_e(module.quiz.title)}</h1>{_quiz_html(module.quiz, f'm{i}q')}",
                )
            )
    if course.capstone:
        cp = course.capstone
        rubric = "\n".join(f"| {r.criterion} | {r.description} | {r.points} |" for r in cp.rubric)
        body = (
            f"# Projet final — {cp.title}\n\n*Durée estimée : {cp.estimated_hours} h*\n\n{cp.context_markdown}\n\n"
            f"## Livrables\n{_bullets(cp.deliverables)}\n\n## Étapes\n"
            + "\n".join(f"{k}. {s}" for k, s in enumerate(cp.steps, 1))
            + f"\n\n## Grille d'évaluation\n\n| Critère | Description | Points |\n|---|---|---|\n{rubric}\n"
        )
        pages.append(("projet", "Projet final", _md(body)))
    if course.final_exam:
        pages.append(
            ("examen", "Examen final", f"<h1>{_e(course.final_exam.title)}</h1>{_quiz_html(course.final_exam, 'examen')}")
        )
    if course.extras:
        x = course.extras
        glossary = "\n".join(f"- **{g.term}** : {g.definition}" for g in x.glossary)
        faq = "\n\n".join(f"### {f.title}\n\n{f.content_markdown}" for f in x.faq)
        pages.append(("glossaire", "Glossaire", _md(f"# Glossaire\n\n{glossary}")))
        pages.append(("faq", "FAQ", _md(f"# Questions fréquentes\n\n{faq}")))
        pages.append(
            (
                "conclusion",
                "Conclusion & certificat",
                _md(
                    f"# Conclusion\n\n{x.conclusion_markdown}\n\n## Obtenir le certificat\n\n"
                    f"{_bullets(x.certification_criteria)}"
                ),
            )
        )
    return pages


PLAYER_CSS = """
:root{--bg:#f7f7fb;--panel:#fff;--text:#1d1d27;--muted:#6b6b7b;--accent:#4f46e5;--ok:#15803d;--ko:#b91c1c;--border:#e4e4ee}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#12121a;--panel:#1b1b26;--text:#ececf3;--muted:#9a9aae;--accent:#8b85ff;--ok:#4ade80;--ko:#f87171;--border:#2c2c3a}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#12121a;--panel:#1b1b26;--text:#ececf3;--muted:#9a9aae;--accent:#8b85ff;--ok:#4ade80;--ko:#f87171;--border:#2c2c3a}
*{box-sizing:border-box}body{margin:0;font:16px/1.65 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text)}
.layout{display:grid;grid-template-columns:300px 1fr;min-height:100vh}
nav{background:var(--panel);border-right:1px solid var(--border);padding:16px;position:sticky;top:env(safe-area-inset-top,0px);height:100vh;overflow:auto}
nav h2{font-size:15px;margin:0 0 4px}.bar{height:6px;background:var(--border);border-radius:3px;margin:8px 0 16px}.bar>i{display:block;height:100%;background:var(--accent);border-radius:3px;width:0}
nav a{display:block;padding:6px 8px;border-radius:6px;color:var(--text);text-decoration:none;font-size:14px}nav a.module{font-weight:600;margin-top:8px}
nav a.active{background:var(--accent);color:#fff}nav a.seen:not(.active)::after{content:" ✓";color:var(--ok)}
main{padding:32px clamp(16px,5vw,64px);max-width:900px}section[hidden]{display:none}
table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}td,th{border:1px solid var(--border);padding:6px 10px}
pre{background:var(--panel);border:1px solid var(--border);padding:12px;border-radius:8px;overflow:auto}code{font-size:.92em}
blockquote{border-left:4px solid var(--accent);margin:0;padding:4px 16px;color:var(--muted)}
details{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:8px 12px;margin:8px 0}
.question{border:1px solid var(--border);border-radius:8px;margin:12px 0;padding:12px;background:var(--panel)}
.question label{display:block;padding:4px 0;cursor:pointer}.question.ok{border-color:var(--ok)}.question.ko{border-color:var(--ko)}
.muted{color:var(--muted);font-size:14px}.explanation{font-size:14px;color:var(--muted)}
button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:10px 18px;font-size:15px;cursor:pointer}
.pager{display:flex;justify-content:space-between;margin-top:40px;gap:12px}
.menu{display:none}
@media (max-width:800px){.layout{grid-template-columns:1fr}nav{position:fixed;inset:0 20% 0 0;z-index:10;transform:translateX(-100%);transition:.2s}
nav.open{transform:none}.menu{display:inline-block;position:sticky;top:8px;margin:8px 16px;z-index:11}main{padding:16px}}
"""

PLAYER_JS = """
(function(){
  var KEY='formation-'+document.body.dataset.course;
  var state={seen:{},scores:{}};
  try{state=JSON.parse(localStorage.getItem(KEY))||state}catch(e){}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}}
  // SCORM 1.2 (si la formation est lancée depuis un LMS)
  function findAPI(w){for(var i=0;w&&i<10;i++){if(w.API)return w.API;if(w.parent===w)break;w=w.parent}return null}
  var api=findAPI(window)||(window.opener&&findAPI(window.opener));
  if(api){try{api.LMSInitialize('')}catch(e){api=null}}
  var sections=[].slice.call(document.querySelectorAll('main section'));
  var links=[].slice.call(document.querySelectorAll('nav a[data-page]'));
  function progress(){
    var n=sections.filter(function(s){return state.seen[s.id]}).length;
    var pct=Math.round(100*n/sections.length);
    document.querySelector('.bar>i').style.width=pct+'%';
    document.getElementById('pct').textContent=pct+' %';
    if(api){
      var exam=state.scores.examen, done=n===sections.length;
      api.LMSSetValue('cmi.core.lesson_location',location.hash.slice(1));
      if(exam!==undefined)api.LMSSetValue('cmi.core.score.raw',String(exam.score));
      var status=exam!==undefined?(exam.passed?'passed':'failed'):(done?'completed':'incomplete');
      api.LMSSetValue('cmi.core.lesson_status',status);api.LMSCommit('');
    }
  }
  function show(id){
    var target=document.getElementById(id)||sections[0];
    sections.forEach(function(s){s.hidden=s!==target});
    links.forEach(function(a){a.classList.toggle('active',a.dataset.page===target.id);a.classList.toggle('seen',!!state.seen[a.dataset.page])});
    state.seen[target.id]=true;save();progress();
    document.querySelector('nav').classList.remove('open');window.scrollTo(0,0);
  }
  window.addEventListener('hashchange',function(){show(location.hash.slice(1))});
  document.querySelector('.menu').addEventListener('click',function(){document.querySelector('nav').classList.toggle('open')});
  document.querySelectorAll('form.quiz').forEach(function(form){
    form.addEventListener('submit',function(ev){
      ev.preventDefault();var good=0,qs=form.querySelectorAll('.question');
      qs.forEach(function(q){
        var expected=q.dataset.correct.split(',').sort().join(',');
        var given=[].slice.call(q.querySelectorAll('input:checked')).map(function(i){return i.value}).sort().join(',');
        var ok=expected===given;if(ok)good++;
        q.classList.toggle('ok',ok);q.classList.toggle('ko',!ok);q.querySelector('.explanation').hidden=false;
      });
      var score=Math.round(100*good/qs.length),passed=score>=Number(form.dataset.pass);
      state.scores[form.dataset.quiz]={score:score,passed:passed};save();progress();
      form.querySelector('.result').textContent='Score : '+score+' % — '+(passed?'Réussi 🎉':'Pas encore, relisez les explications et réessayez.');
    });
  });
  window.addEventListener('beforeunload',function(){if(api){try{api.LMSFinish('')}catch(e){}}});
  show(location.hash.slice(1)||(api&&api.LMSGetValue('cmi.core.lesson_location'))||sections[0].id);
})();
"""


def to_html(course: Course) -> str:
    pages = _pages(course)
    nav = []
    for idx, (pid, label, _) in enumerate(pages):
        cls = ' class="module"' if re.fullmatch(r"m\d+", pid) else ""
        nav.append(f'<a href="#{pid}" data-page="{pid}"{cls}>{_e(label)}</a>')
    sections = []
    for idx, (pid, _, body) in enumerate(pages):
        prev_link = f'<a href="#{pages[idx - 1][0]}">← {_e(pages[idx - 1][1])}</a>' if idx > 0 else "<span></span>"
        next_link = f'<a href="#{pages[idx + 1][0]}">{_e(pages[idx + 1][1])} →</a>' if idx < len(pages) - 1 else ""
        sections.append(f'<section id="{pid}" hidden>{body}<div class="pager">{prev_link}{next_link}</div></section>')
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_e(course.title)}</title><style>{PLAYER_CSS}</style></head>
<body data-course="{_e(course.id)}"><button class="menu" type="button">☰ Sommaire</button>
<div class="layout"><nav><h2>{_e(course.title)}</h2><span class="muted">Progression : <b id="pct">0 %</b></span>
<div class="bar"><i></i></div>{"".join(nav)}</nav>
<main>{"".join(sections)}</main></div><script>{PLAYER_JS}</script></body></html>"""


# --------------------------------------------------------------------------- #
# SCORM 1.2
# --------------------------------------------------------------------------- #


def to_scorm_zip(course: Course) -> bytes:
    title = _e(course.title)
    manifest = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="formation-{course.id}" version="1.0"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata><schema>ADL SCORM</schema><schemaversion>1.2</schemaversion></metadata>
  <organizations default="org-{course.id}">
    <organization identifier="org-{course.id}">
      <title>{title}</title>
      <item identifier="item-1" identifierref="res-1"><title>{title}</title>
        <adlcp:masteryscore>{course.final_exam.passing_score_percent if course.final_exam else 70}</adlcp:masteryscore>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="res-1" type="webcontent" adlcp:scormtype="sco" href="index.html"><file href="index.html"/></resource>
  </resources>
</manifest>"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("imsmanifest.xml", manifest)
        z.writestr("index.html", to_html(course))
    return buf.getvalue()


EXPORTERS = {
    "json": ("application/json", "json", lambda c: to_json(c).encode("utf-8")),
    "markdown": ("application/zip", "md.zip", to_markdown_zip),
    "html": ("text/html; charset=utf-8", "html", lambda c: to_html(c).encode("utf-8")),
    "scorm": ("application/zip", "scorm12.zip", to_scorm_zip),
}
