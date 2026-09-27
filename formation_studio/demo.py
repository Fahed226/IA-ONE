"""LLM de démonstration : produit un contenu factice sans appel API.

Utile pour essayer l'interface (`serve --demo`) et pour les tests.
"""

from __future__ import annotations

import re
import threading
from typing import TypeVar

from pydantic import BaseModel

from .models import (
    GenCapstone,
    GenCourseExtras,
    GenExample,
    GenExercise,
    GenGlossaryEntry,
    GenLessonContent,
    GenLessonPlan,
    GenModulePlan,
    GenOutline,
    GenQuestion,
    GenQuiz,
    GenResource,
    GenRubricCriterion,
    GenSection,
    GenSlide,
    QuestionType,
)

T = TypeVar("T", bound=BaseModel)


def _int(pattern: str, text: str, default: int) -> int:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else default


class DemoLLM:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []
        self._lock = threading.Lock()

    def generate(self, prompt: str, schema: type[T]) -> T:
        with self._lock:
            self.calls.append((schema.__name__, prompt))
        topic = re.search(r"Sujet : (.+)", prompt)
        topic = topic.group(1).strip() if topic else "Formation"
        builder = getattr(self, f"_{schema.__name__}")
        return builder(prompt, topic)

    def _GenOutline(self, prompt: str, topic: str) -> GenOutline:
        n_mod = _int(r"Exactement (\d+) modules", prompt, 3)
        n_les = _int(r"exactement (\d+) leçons", prompt, 3)
        return GenOutline(
            title=f"{topic} : la formation complète",
            subtitle="Passez de la théorie à la pratique pas à pas",
            description=f"Une formation structurée pour maîtriser {topic}.",
            target_audience="Apprenants motivés",
            prerequisites=["Aucun prérequis technique"],
            learning_outcomes=[f"Appliquer les fondamentaux de {topic}", "Mener un projet de bout en bout"],
            skills=["Analyse", "Mise en pratique", "Esprit critique"],
            pedagogical_approach="Alternance d'apports, de démonstrations et d'exercices.",
            modules=[
                GenModulePlan(
                    title=f"Module {i + 1} : étape {i + 1}",
                    summary=f"Résumé du module {i + 1}.",
                    objectives=[f"Objectif {i + 1}.1", f"Objectif {i + 1}.2"],
                    lessons=[
                        GenLessonPlan(
                            title=f"Leçon {i + 1}.{j + 1}",
                            summary="Résumé de la leçon.",
                            objectives=["Identifier", "Appliquer"],
                            duration_minutes=30,
                            format="texte + atelier",
                        )
                        for j in range(n_les)
                    ],
                )
                for i in range(n_mod)
            ],
        )

    def _GenLessonContent(self, prompt: str, topic: str) -> GenLessonContent:
        wants_video = "script vidéo complet" in prompt
        wants_slides = "diapositives avec notes" in prompt
        return GenLessonContent(
            introduction_markdown=f"Bienvenue dans cette leçon sur **{topic}**.",
            sections=[
                GenSection(heading="Les notions clés", content_markdown="- Notion A\n- Notion B\n\n| Terme | Sens |\n|---|---|\n| A | B |"),
                GenSection(heading="Mise en œuvre", content_markdown="1. Étape 1\n2. Étape 2\n\n```python\nprint('ok')\n```"),
            ],
            examples=[GenExample(title="Cas pratique", content_markdown="Une entreprise fictive applique la méthode.")],
            key_takeaways=["Point clé 1", "Point clé 2"],
            exercises=[
                GenExercise(
                    title="Exercice 1",
                    instructions_markdown="Réalisez l'étape 1.",
                    difficulty="facile",
                    estimated_minutes=10,
                    solution_markdown="Voici la solution.",
                )
            ]
            if "exercices pratiques progressifs" in prompt
            else [],
            common_mistakes=["Aller trop vite"],
            resources=[GenResource(title="Documentation officielle", type="documentation", description="Référence.")],
            video_script_markdown="**[0:00]** Accroche…" if wants_video else "",
            slides=[GenSlide(title="Titre", bullets=["Idée 1"], speaker_notes="Notes.")] if wants_slides else [],
        )

    def _GenQuiz(self, prompt: str, topic: str) -> GenQuiz:
        return GenQuiz(
            title="Quiz d'évaluation",
            instructions="Répondez à toutes les questions.",
            passing_score_percent=75,
            questions=[
                GenQuestion(
                    question=f"Question sur {topic} ?",
                    type=QuestionType.single,
                    options=["Réponse A", "Réponse B", "Réponse C"],
                    correct_indexes=[1],
                    explanation="B est correct car…",
                    bloom_level="comprendre",
                ),
                GenQuestion(
                    question="Cette affirmation est-elle vraie ?",
                    type=QuestionType.true_false,
                    options=["Vrai", "Faux"],
                    correct_indexes=[0],
                    explanation="C'est vrai.",
                    bloom_level="se souvenir",
                ),
                GenQuestion(
                    question="Sélectionnez les bonnes pratiques.",
                    type=QuestionType.multiple,
                    options=["Pratique 1", "Pratique 2", "Anti-pratique"],
                    correct_indexes=[0, 1],
                    explanation="Les deux premières sont recommandées.",
                    bloom_level="appliquer",
                ),
            ],
        )

    def _GenCapstone(self, prompt: str, topic: str) -> GenCapstone:
        return GenCapstone(
            title=f"Projet de synthèse {topic}",
            context_markdown="Vous êtes consultant pour une entreprise fictive.",
            deliverables=["Rapport", "Présentation"],
            steps=["Analyser", "Concevoir", "Présenter"],
            rubric=[
                GenRubricCriterion(criterion="Analyse", description="Pertinence", points=50),
                GenRubricCriterion(criterion="Livrables", description="Qualité", points=50),
            ],
            estimated_hours=4,
        )

    def _GenCourseExtras(self, prompt: str, topic: str) -> GenCourseExtras:
        return GenCourseExtras(
            welcome_message_markdown="Bienvenue !",
            how_to_follow_markdown="Suivez une leçon par jour.",
            glossary=[GenGlossaryEntry(term="Terme", definition="Définition")],
            faq=[GenExample(title="Combien de temps ?", content_markdown="Environ 10 heures.")],
            certification_criteria=["Réussir l'examen final à 75 %"],
            conclusion_markdown="Bravo !",
            marketing_pitch=f"La formation de référence sur {topic}.",
            sales_page_bullets=["Contenu complet", "Exercices corrigés"],
        )
