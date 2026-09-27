# IA-ONE — Formation Studio 🎓

Outil expert de création de **formations en ligne complètes**, propulsé par Claude.
À partir d'un simple brief (sujet, public, niveau, durée…), il conçoit et rédige
une formation prête à publier :

| Élément | Contenu généré |
|---|---|
| **Programme** | titre, sous-titre, description, public, prérequis, objectifs mesurables (Bloom), compétences, approche pédagogique |
| **Modules** | résumé, objectifs, N leçons chacun |
| **Leçons** | introduction, sections développées, exemples / études de cas, points clés, erreurs fréquentes, ressources |
| **Exercices** | exercices pratiques progressifs avec solutions détaillées |
| **Quiz** | un quiz par module (choix unique, multiple, vrai/faux) avec explications |
| **Examen final** | questions de mise en situation couvrant toute la formation |
| **Projet final** | cas réaliste, livrables, étapes, grille d'évaluation sur 100 points |
| **Accompagnement** | message de bienvenue, guide de suivi, glossaire, FAQ, critères de certification, conclusion |
| **Vente** | pitch marketing + arguments pour la page de vente |
| **Options** | scripts vidéo, diapositives avec notes du présentateur |

## Exports

- **Site HTML autonome** : lecteur de formation interactif (sommaire, progression, quiz corrigés automatiquement) — un seul fichier, fonctionne hors ligne.
- **SCORM 1.2** : paquet `.zip` à importer dans un LMS (Moodle, 360Learning, TalentLMS…) ; progression et score de l'examen remontés au LMS.
- **Markdown** : une arborescence module / leçon (`.zip`), idéale pour Notion, GitBook, Docusaurus…
- **JSON** : la structure complète, pour intégrer dans vos propres outils.

## Installation

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Utilisation

### Interface web

```bash
python -m formation_studio serve          # http://127.0.0.1:8000
python -m formation_studio serve --demo   # essai sans clé API (contenu factice)
```

Deux modes de travail :
1. **Générer le programme (à valider)** : l'IA propose le syllabus ; vous modifiez titres,
   résumés et durées, puis cliquez sur *Rédiger tout le contenu manquant*.
2. **Générer la formation complète** : tout est produit d'un coup, avec suivi en temps réel.

Ensuite, chaque leçon peut être **régénérée avec des consignes** (« plus d'exemples »,
« plus simple », « ajouter un cas pratique dans le BTP »…), chaque quiz régénéré, et la
formation exportée dans tous les formats.

### Ligne de commande

```bash
python -m formation_studio generate "Excel pour l'analyse de données commerciales" \
  --audience "commerciaux B2B" --level intermédiaire --hours 12 \
  --modules 6 --lessons 4 --video --slides --formats html scorm markdown --out exports/

python -m formation_studio export <id> --format scorm
```

## Configuration

| Variable | Défaut | Rôle |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Clé API Claude |
| `FORMATION_MODEL` | `claude-opus-5` | Modèle utilisé |
| `FORMATION_EFFORT` | `high` | Niveau d'effort (`low` … `max`) |
| `FORMATION_DATA_DIR` | `data/courses` | Dossier de stockage des formations |

Les requêtes activent le repli automatique côté serveur (`fallbacks: "default"`) : si un
filtre de sécurité refuse une requête, l'API la rejoue sur un modèle de repli.

## Architecture

```
formation_studio/
├── models.py      # schémas Pydantic (brief, programme, leçons, quiz, projet…)
├── prompts.py     # prompts de l'ingénieur pédagogique (ADDIE, Bloom, alignement)
├── llm.py         # client Claude : streaming + sorties JSON structurées validées
├── generator.py   # pipeline : programme → leçons (en parallèle) → quiz → examen → projet → extras
├── exporters.py   # HTML interactif, SCORM 1.2, Markdown, JSON
├── storage.py     # persistance JSON
├── app.py         # API REST FastAPI + tâches de fond
├── cli.py         # ligne de commande
├── demo.py        # LLM factice (démo et tests)
└── static/        # interface web (marked + DOMPurify embarqués, aucun CDN)
```

Si une étape échoue (réseau, limite de débit…), les autres continuent ; relancer la
génération ne refait que les éléments manquants.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```
