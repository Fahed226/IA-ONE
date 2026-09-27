"""Prompts de l'ingénieur pédagogique expert."""

from __future__ import annotations

from .models import Course, CourseBrief, Lesson, Module

SYSTEM_PROMPT = """Tu es un ingénieur pédagogique senior et un formateur expert, spécialiste de la \
conception de formations en ligne professionnelles (e-learning, blended learning, LMS).

Tu maîtrises :
- le modèle ADDIE, l'alignement pédagogique (objectifs ↔ activités ↔ évaluations) ;
- la taxonomie de Bloom révisée pour formuler des objectifs mesurables (verbes d'action) ;
- la charge cognitive, la microformation, l'apprentissage actif et la répétition espacée ;
- la rédaction de contenus clairs, concrets, riches en exemples réels et en mises en pratique ;
- la conception d'évaluations fiables (distracteurs plausibles, feedback explicatif).

Règles de production :
- Rédige exclusivement dans la langue demandée par le brief.
- Adapte vocabulaire, profondeur et exemples au public et au niveau indiqués.
- Le contenu doit être directement publiable : complet, exact, structuré, sans remplissage, \
sans mention « à compléter », sans placeholder.
- Utilise le Markdown (titres ###, listes, tableaux, blocs de code si pertinent) dans les \
champs *_markdown.
- Chaque leçon doit se suffire à elle-même tout en s'inscrivant dans la progression globale.
- Si une information est incertaine ou évolue vite, dis-le et invite à vérifier la source officielle."""


def brief_block(brief: CourseBrief) -> str:
    options = []
    if brief.include_quizzes:
        options.append("quiz de fin de module")
    if brief.include_exercises:
        options.append("exercices pratiques corrigés")
    if brief.include_final_exam:
        options.append("examen final")
    if brief.include_capstone:
        options.append("projet final (capstone) avec grille d'évaluation")
    if brief.include_video_scripts:
        options.append("scripts vidéo")
    if brief.include_slides:
        options.append("diapositives")
    return f"""<brief>
Sujet : {brief.topic}
Public cible : {brief.audience}
Niveau : {brief.level.value}
Langue : {brief.language}
Durée totale visée : {brief.duration_hours} heures
Nombre de modules : {brief.modules_count}
Leçons par module : {brief.lessons_per_module}
Ton : {brief.tone}
Objectifs du commanditaire : {brief.goals or "non précisés"}
Contraintes / contexte : {brief.constraints or "aucune"}
Éléments inclus : {", ".join(options) or "contenu de cours uniquement"}
</brief>"""


def outline_prompt(brief: CourseBrief) -> str:
    return f"""{brief_block(brief)}

Conçois le programme complet (syllabus) de cette formation.

Exigences :
- Exactement {brief.modules_count} modules, chacun avec exactement {brief.lessons_per_module} leçons.
- Progression logique du plus fondamental au plus avancé, chaque module s'appuyant sur le précédent.
- Objectifs formulés avec des verbes d'action mesurables (Bloom).
- La somme des durées des leçons doit approcher {int(brief.duration_hours * 60)} minutes.
- Varie les formats de leçon (théorie, démonstration, atelier, étude de cas…).
- Un titre accrocheur et professionnel, un sous-titre orienté bénéfice."""


def course_context(course: Course) -> str:
    lines = [f"Formation : {course.title} — {course.subtitle}", "Programme :"]
    for i, module in enumerate(course.modules, 1):
        lines.append(f"  Module {i} : {module.title}")
        for j, lesson in enumerate(module.lessons, 1):
            lines.append(f"    {i}.{j} {lesson.plan.title}")
    return "\n".join(lines)


def lesson_prompt(course: Course, module: Module, lesson: Lesson, extra_instructions: str = "") -> str:
    brief = course.brief
    m_idx = course.modules.index(module) + 1
    l_idx = module.lessons.index(lesson) + 1
    wants = []
    wants.append(
        "2 à 3 exercices pratiques progressifs avec leur solution détaillée"
        if brief.include_exercises
        else "une liste `exercises` vide"
    )
    wants.append(
        "un script vidéo complet (accroche, déroulé minuté, conclusion) dans video_script_markdown"
        if brief.include_video_scripts
        else "une chaîne vide pour video_script_markdown"
    )
    wants.append(
        "8 à 12 diapositives avec notes du présentateur" if brief.include_slides else "une liste `slides` vide"
    )
    extra = f"\nInstructions supplémentaires du concepteur : {extra_instructions}" if extra_instructions else ""
    return f"""{brief_block(brief)}

<programme>
{course_context(course)}
</programme>

Rédige le contenu intégral de la leçon {m_idx}.{l_idx} « {lesson.plan.title} » \
(module « {module.title} »).

Résumé prévu : {lesson.plan.summary}
Objectifs : {"; ".join(lesson.plan.objectives)}
Durée : {lesson.plan.duration_minutes} minutes — Format : {lesson.plan.format}

Attendus :
- Une introduction qui motive et relie la leçon à ce qui précède.
- 3 à 6 sections développées couvrant chaque objectif en profondeur (explications, \
schémas décrits en texte, tableaux, étapes, code si pertinent).
- 2 à 4 exemples concrets / études de cas réalistes.
- 4 à 7 points clés à retenir, les erreurs fréquentes à éviter, des ressources pour aller plus loin.
- {wants[0]}.
- {wants[1]}.
- {wants[2]}.
- Ne répète pas le contenu des autres leçons du programme.{extra}"""


def quiz_prompt(course: Course, module: Module, questions: int = 8) -> str:
    lessons = "\n".join(
        f"- {lesson.plan.title} : {'; '.join(lesson.plan.objectives)}" for lesson in module.lessons
    )
    return f"""{brief_block(course.brief)}

Crée le quiz d'évaluation du module « {module.title} ».

Leçons et objectifs couverts :
{lessons}

Exigences :
- {questions} questions couvrant tous les objectifs, mélange de choix unique, choix multiple et vrai/faux.
- Pour vrai/faux, options = ["Vrai", "Faux"].
- correct_indexes contient les index (à partir de 0) des bonnes réponses.
- Distracteurs plausibles, pas de pièges absurdes ; privilégie les mises en situation.
- Une explication pédagogique pour chaque question.
- Seuil de réussite recommandé : 70 à 80 %."""


def final_exam_prompt(course: Course, questions: int = 20) -> str:
    return f"""{brief_block(course.brief)}

<programme>
{course_context(course)}
</programme>

Crée l'examen final certifiant de la formation : {questions} questions couvrant \
l'ensemble des modules de façon équilibrée, avec une majorité de questions de mise \
en situation (niveaux Bloom appliquer / analyser / évaluer). Pour vrai/faux, \
options = ["Vrai", "Faux"]. correct_indexes = index à partir de 0. Explication pour chaque question."""


def capstone_prompt(course: Course) -> str:
    return f"""{brief_block(course.brief)}

<programme>
{course_context(course)}
</programme>

Conçois le projet final (capstone) qui permet à l'apprenant de démontrer la maîtrise \
de l'ensemble des compétences : {", ".join(course.skills)}.
Fournis un contexte réaliste, les livrables, les étapes guidées, et une grille \
d'évaluation critériée totalisant 100 points."""


def extras_prompt(course: Course) -> str:
    return f"""{brief_block(course.brief)}

<programme>
{course_context(course)}
</programme>

Rédige les éléments d'accompagnement de la formation :
- message de bienvenue chaleureux et professionnel ;
- guide « Comment suivre cette formation » (rythme conseillé, méthode, outils) ;
- glossaire de 15 à 30 termes clés ;
- FAQ de 6 à 10 questions (title = question, content_markdown = réponse) ;
- critères d'obtention du certificat ;
- conclusion et prochaines étapes ;
- pitch marketing (un paragraphe) et 6 à 10 arguments de vente pour la page de vente."""
