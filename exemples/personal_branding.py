"""Formation « Personal branding » rédigée avec Formation Studio.

Exécuter : python exemples/personal_branding.py
Produit exemples/personal-branding.json et exemples/personal-branding.html
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from formation_studio.exporters import slugify, to_html  # noqa: E402
from formation_studio.models import (  # noqa: E402
    Course,
    CourseBrief,
    CourseStatus,
    GenCapstone,
    GenCourseExtras,
    GenExample,
    GenExercise,
    GenGlossaryEntry,
    GenLessonContent,
    GenLessonPlan,
    GenQuestion,
    GenQuiz,
    GenResource,
    GenRubricCriterion,
    GenSection,
    Lesson,
    Module,
    QuestionType,
)

U, M, VF = QuestionType.single, QuestionType.multiple, QuestionType.true_false


def lesson(title, summary, objectives, minutes, fmt, intro, sections, examples, takeaways, exercise, mistakes, resources):
    return Lesson(
        plan=GenLessonPlan(title=title, summary=summary, objectives=objectives, duration_minutes=minutes, format=fmt),
        content=GenLessonContent(
            introduction_markdown=intro,
            sections=[GenSection(heading=h, content_markdown=c) for h, c in sections],
            examples=[GenExample(title=t, content_markdown=c) for t, c in examples],
            key_takeaways=takeaways,
            exercises=[GenExercise(title=exercise[0], instructions_markdown=exercise[1], difficulty=exercise[2], estimated_minutes=exercise[3], solution_markdown=exercise[4])],
            common_mistakes=mistakes,
            resources=[GenResource(title=t, type=ty, description=d) for t, ty, d in resources],
            video_script_markdown="",
            slides=[],
        ),
    )


def quiz(title, questions, passing=70):
    return GenQuiz(
        title=title,
        instructions="Choisissez la ou les bonnes réponses, puis validez pour voir les explications.",
        passing_score_percent=passing,
        questions=[GenQuestion(question=q, type=t, options=o, correct_indexes=c, explanation=e, bloom_level=b) for q, t, o, c, e, b in questions],
    )


# =========================================================================== #
# MODULE 1 — Les fondations de sa marque personnelle
# =========================================================================== #

L1_1 = lesson(
    "Ce qu'est (vraiment) une marque personnelle",
    "Comprendre ce qu'est une marque personnelle et pourquoi elle devient un actif commercial.",
    ["Définir la marque personnelle avec ses propres mots", "Distinguer réputation, visibilité et marque", "Identifier ce que la marque apporte à son activité"],
    25, "vidéo + réflexion",
    "Votre marque personnelle existe déjà : c'est **ce que les gens disent de vous quand vous n'êtes pas dans la pièce**. La question n'est donc pas « faut-il avoir une marque ? » mais « est-ce que je la laisse au hasard ou est-ce que je la construis ? ». Dans cette leçon, on pose les bases qui serviront pendant toute la formation.",
    [
        ("Une définition simple et utilisable",
         "Une marque personnelle, c'est l'association durable entre **votre nom** et **une promesse** dans l'esprit d'un public précis.\n\n> *« Quand je pense à Sarah, je pense à : la personne qui aide les kinés à remplir leur agenda grâce à Instagram. »*\n\nTrois éléments doivent être présents :\n\n| Élément | Question | Exemple |\n|---|---|---|\n| **Pour qui** | Qui doit penser à vous ? | Les kinés installés en libéral |\n| **Quoi** | Pour quel résultat ? | Remplir leur agenda |\n| **Comment** | Avec quelle approche reconnaissable ? | Instagram, sans danser devant la caméra |"),
        ("Visibilité, réputation, marque : trois choses différentes",
         "- **La visibilité** : combien de personnes vous voient. On peut être très visible et oublié le lendemain.\n- **La réputation** : ce que les gens pensent de la qualité de votre travail.\n- **La marque** : l'idée claire et unique qu'ils associent à votre nom.\n\nUn compte à 100 000 abonnés sans positionnement clair a de la visibilité mais pas de marque. Une consultante à 3 000 abonnés que tout son secteur recommande a une marque forte. **La marque transforme l'attention en confiance, et la confiance en ventes.**"),
        ("Pourquoi c'est un actif commercial",
         "Une marque personnelle bien construite :\n\n1. **Réduit le coût d'acquisition** : les clients viennent à vous au lieu que vous alliez les chercher.\n2. **Permet de vendre plus cher** : on paie plus volontiers une personne identifiée comme la référence.\n3. **Raccourcit le cycle de vente** : le prospect vous connaît déjà avant le premier appel.\n4. **Vous appartient** : contrairement à un poste ou un client, elle vous suit partout.\n\nLes gens achètent à des personnes qu'ils **connaissent, apprécient et en qui ils ont confiance**. Tout le travail de personal branding consiste à faire avancer votre audience sur ces trois marches."),
        ("Authenticité : ni masque, ni journal intime",
         "Être authentique ne veut pas dire tout raconter. Pensez à une **version éditée de vous-même** : vraie, mais choisie.\n\n- ✅ Partager vos convictions, vos méthodes, vos coulisses de travail, vos échecs utiles.\n- ❌ Inventer un personnage que vous ne pourrez pas tenir dans la durée.\n- ❌ Exposer votre vie privée sans lien avec la promesse de votre marque.\n\nRègle pratique : **tout contenu personnel doit servir un message professionnel.**"),
    ],
    [
        ("Deux coachs sportifs, deux trajectoires",
         "Karim et Julie sont tous deux coachs sportifs. Karim publie des séances variées « pour tout le monde ». Julie publie uniquement sur **la remise en forme des mamans après la grossesse, en 20 minutes à la maison**.\n\nAprès un an, Karim a plus de vues ponctuelles, mais Julie a une liste d'attente : quand une maman cherche une solution, **c'est son nom qui revient**. La spécialisation a créé la marque."),
    ],
    ["Votre marque existe déjà : autant la construire volontairement", "Marque = nom + promesse + public précis", "La visibilité sans positionnement ne crée pas de marque", "Objectif : que votre audience vous connaisse, vous apprécie et vous fasse confiance", "Authentique ne veut pas dire tout montrer"],
    ("Votre marque aujourd'hui",
     "1. Envoyez ce message à 5 personnes qui vous connaissent professionnellement : *« En une phrase, pour quoi est-ce que tu me recommanderais ? »*\n2. Notez les réponses mot pour mot.\n3. Comparez-les avec l'image que **vous voulez** donner. Qu'est-ce qui revient ? Qu'est-ce qui manque ?",
     "facile", 20,
     "Il n'y a pas de bonne réponse unique. Ce qu'il faut observer :\n\n- **Si les réponses sont toutes différentes**, votre marque est floue : le module 1 est prioritaire.\n- **Si elles se ressemblent mais ne correspondent pas à votre cible**, votre marque est claire mais mal orientée : repositionnez-vous (leçon 1.2).\n- **Si elles correspondent à ce que vous voulez**, vous avez une base : il faut maintenant l'amplifier (modules 3 et 4).\n\nGardez ces réponses : vous referez l'exercice à la fin de la formation pour mesurer le chemin parcouru."),
    ["Confondre nombre d'abonnés et force de marque", "Vouloir plaire à tout le monde", "Copier le style d'un créateur connu au lieu de trouver le sien"],
    [("Montrez votre travail ! — Austin Kleon", "livre", "Court et très concret sur l'art de partager son travail pour se faire connaître."),
     ("Influence et manipulation — Robert Cialdini", "livre", "Les principes psychologiques (autorité, sympathie, preuve sociale) qui expliquent pourquoi une marque fait vendre.")],
)

L1_2 = lesson(
    "Trouver son positionnement unique",
    "Choisir sa niche et formuler une promesse claire qui vous différencie.",
    ["Choisir une niche à l'intersection de ses compétences, de ses envies et d'un marché", "Rédiger sa phrase de positionnement", "Identifier son angle différenciant"],
    35, "atelier",
    "Le positionnement est la décision la plus importante de votre marque. Un bon positionnement fait **qu'on vous choisit sans vous comparer**. Un mauvais vous condamne à être « un de plus ». Cette leçon vous fait passer de « je fais du marketing » à une promesse qui se retient.",
    [
        ("L'intersection gagnante",
         "Votre niche se trouve à l'intersection de trois cercles :\n\n1. **Ce que vous savez faire** (compétences, expérience, résultats obtenus)\n2. **Ce que vous aimez faire** (sinon vous ne tiendrez pas 2 ans de contenu)\n3. **Ce pour quoi des gens paient** (un problème urgent et coûteux)\n\nSi un cercle manque : sans compétence, vous perdez en crédibilité ; sans envie, vous abandonnez ; sans marché, vous avez un hobby."),
        ("Niche : assez étroite pour être la référence",
         "Se spécialiser fait peur car on a l'impression de perdre des clients. En réalité, **on gagne en mémorisation**.\n\n| Trop large | Mieux | Très bien |\n|---|---|---|\n| Coach business | Coach pour freelances | Coach pour graphistes freelances qui veulent dépasser 5 000 €/mois |\n| Nutritionniste | Nutrition sportive | Nutrition pour coureurs amateurs qui préparent un marathon |\n| Consultant LinkedIn | LinkedIn pour dirigeants | LinkedIn pour dirigeants de PME industrielles qui recrutent |\n\nVous pourrez élargir plus tard. **On se fait connaître par une porte étroite.**"),
        ("La phrase de positionnement",
         "Utilisez ce modèle :\n\n> **J'aide** [public précis] **à** [résultat désiré] **grâce à** [méthode / approche] **sans** [la contrainte qu'ils redoutent].\n\nExemples :\n- *J'aide les artisans du bâtiment à trouver des chantiers grâce à Facebook, sans y passer plus de 2 heures par semaine.*\n- *J'aide les jeunes diplômés en finance à décrocher leur premier CDI grâce à un LinkedIn qui attire les recruteurs, sans envoyer 200 candidatures.*\n\nCette phrase deviendra votre bio, votre accroche en réseau et le fil rouge de vos contenus."),
        ("Trouver son angle différenciant",
         "Dans une niche, d'autres existent déjà. Votre angle, c'est **ce qui vous rend reconnaissable**. Pistes :\n\n- **Votre parcours** : « ancien recruteur passé de l'autre côté », « infirmière devenue développeuse ».\n- **Votre méthode** : un nom, des étapes, un cadre propriétaire (ex. *la méthode 3P*).\n- **Votre conviction** : une idée forte, parfois à contre-courant (*« Arrêtez de poster tous les jours »*).\n- **Votre ton** : humour, franc-parler, pédagogie ultra-simple, esthétique.\n\nUn bon angle se résume en une expression que votre audience peut répéter."),
    ],
    [
        ("De « graphiste » à référence",
         "Léa se présentait comme « graphiste freelance ». Elle a combiné son expérience passée en restauration et son métier : **« Je crée l'identité visuelle des restaurants qui veulent remplir leur salle grâce à Instagram. »** Elle parle désormais le langage des restaurateurs, montre des cas concrets de restaurants, et ses clients se la recommandent entre eux."),
        ("Une conviction comme angle",
         "Un conseiller en investissement se démarque avec une conviction répétée dans tous ses contenus : *« La meilleure stratégie est ennuyeuse. »* Face à un secteur plein de promesses spectaculaires, cette phrase devient sa signature."),
    ],
    ["Niche = compétences ∩ envie ∩ marché qui paie", "Une niche étroite rend mémorable ; on élargit plus tard", "Phrase clé : J'aide [qui] à [résultat] grâce à [méthode] sans [contrainte]", "L'angle différenciant peut venir du parcours, de la méthode, d'une conviction ou du ton"],
    ("Rédiger votre positionnement",
     "1. Listez 5 compétences, 5 sujets qui vous passionnent et 5 problèmes pour lesquels des gens paient autour de vous.\n2. Entourez les combinaisons qui apparaissent dans les trois listes.\n3. Rédigez **3 versions** de votre phrase de positionnement avec le modèle *J'aide… à… grâce à… sans…*.\n4. Choisissez-en une et testez-la sur 3 personnes de votre cible : comprennent-elles en moins de 5 secondes ?",
     "moyen", 40,
     "**Exemple corrigé** (profil : ancienne commerciale, passionnée de psychologie, à l'aise sur LinkedIn) :\n\n- Version 1 : *J'aide les entreprises à mieux vendre.* → trop large, aucune différenciation.\n- Version 2 : *J'aide les commerciaux B2B à mieux prospecter grâce à LinkedIn.* → mieux, mais encore banal.\n- Version 3 : *J'aide les commerciaux B2B à décrocher des rendez-vous sur LinkedIn grâce à la psychologie de la persuasion, sans messages automatiques qui font fuir.* → public précis, résultat concret, méthode distinctive, objection traitée.\n\n**Critères de validation** : un inconnu de la cible doit pouvoir répondre à « c'est pour moi ? » en moins de 5 secondes, et vous devez pouvoir produire au moins 50 idées de contenus sur ce positionnement."),
    ["Choisir une niche uniquement parce qu'elle « marche » chez les autres", "Rédiger une promesse vague (« réussir », « s'épanouir »)", "Changer de positionnement tous les mois"],
    [("Building a StoryBrand — Donald Miller", "livre", "Méthode pour clarifier son message en plaçant le client au centre de l'histoire."),
     ("Positioning — Al Ries et Jack Trout", "livre", "Le classique sur la bataille pour une place dans l'esprit du public.")],
)

L1_3 = lesson(
    "Son histoire et son identité de marque",
    "Construire son récit, ses valeurs et une identité visuelle et verbale cohérente.",
    ["Structurer son histoire personnelle en récit de marque", "Définir 3 valeurs et un ton de voix", "Créer une identité visuelle simple et cohérente"],
    30, "atelier",
    "Les faits informent, les histoires font retenir. Votre histoire donne une raison de vous suivre **vous** plutôt qu'un autre expert aussi compétent. Associée à une identité cohérente (valeurs, ton, visuels), elle rend votre marque reconnaissable en un coup d'œil.",
    [
        ("Le récit de marque en 5 temps",
         "1. **Avant** : d'où vous partez (situation que votre audience vit aujourd'hui).\n2. **Le déclic** : l'événement, l'échec ou la rencontre qui a tout changé.\n3. **Le chemin** : ce que vous avez essayé, appris, construit.\n4. **Le résultat** : où vous en êtes aujourd'hui, preuves à l'appui.\n5. **La mission** : pourquoi vous aidez maintenant les autres à faire ce chemin.\n\nL'objectif n'est pas de vous mettre en valeur, mais de permettre à votre audience de **se reconnaître dans votre « avant »** et de désirer votre « après »."),
        ("Valeurs et ton de voix",
         "Choisissez **3 valeurs** qui guideront vos contenus et vos décisions (ex. : franchise, simplicité, exigence). Pour chacune, définissez ce qu'elle implique concrètement.\n\nPuis décrivez votre ton avec des paires « plutôt / plutôt pas » :\n\n| Plutôt | Plutôt pas |\n|---|---|\n| Direct | Agressif |\n| Pédagogue | Professoral |\n| Chaleureux | Familier |\n| Expert | Jargonneux |\n\nCe tableau vous servira aussi si vous déléguez un jour la rédaction."),
        ("Identité visuelle minimale",
         "Pas besoin d'un logo à 3 000 € pour démarrer. Il faut surtout de la **cohérence** :\n\n- **Une photo de profil** professionnelle : visage net, lumière naturelle, fond simple, regard caméra, la même partout.\n- **2 à 3 couleurs** et **1 à 2 polices** utilisées dans tous vos visuels.\n- **Des modèles réutilisables** (Canva ou équivalent) pour vos carrousels, citations et miniatures.\n- **Une bannière** (LinkedIn, YouTube, X) qui reprend votre phrase de positionnement.\n\nTest : si l'on cache votre nom, votre audience reconnaît-elle vos visuels dans son fil ?"),
    ],
    [
        ("L'histoire qui a lancé une marque",
         "Thomas, comptable, raconte : *« Pendant 8 ans, j'ai vu des indépendants brillants couler à cause de leur trésorerie, pas de leur talent. »* Il partage ensuite comment il a construit un tableau de suivi simple, puis son intention : que plus aucun freelance ne découvre un redressement de TVA par surprise. Son récit crée une connexion immédiate avec des indépendants qui ont peur de l'administratif."),
    ],
    ["L'histoire permet à l'audience de se reconnaître dans votre « avant »", "Structure : avant, déclic, chemin, résultat, mission", "3 valeurs + un ton de voix défini par des « plutôt / plutôt pas »", "Cohérence visuelle : même photo, mêmes couleurs, mêmes modèles partout"],
    ("Écrire votre histoire de marque",
     "Rédigez votre récit en 5 paragraphes courts (avant, déclic, chemin, résultat, mission), 200 à 300 mots maximum. Puis rédigez votre tableau de ton de voix (4 lignes « plutôt / plutôt pas »).",
     "moyen", 35,
     "**Points de contrôle** :\n\n- Le paragraphe « avant » décrit une situation que **votre cible vit aujourd'hui** (et non un détail biographique sans lien).\n- Le déclic est **concret** : une date, une scène, un chiffre, une phrase entendue.\n- Le résultat contient **au moins une preuve** (chiffre, client, réalisation).\n- La mission parle **de l'audience**, pas de vous.\n\nCe texte sera réutilisé : section « À propos » de LinkedIn, page de vente, premier post épinglé, présentation orale en 60 secondes."),
    ["Raconter sa vie sans lien avec le problème de l'audience", "Changer de couleurs et de style de visuels à chaque publication", "Utiliser une photo de profil différente sur chaque réseau"],
    [("Canva", "outil", "Création de modèles visuels cohérents (carrousels, bannières, miniatures)."),
     ("Coolors", "outil", "Générateur de palettes de couleurs pour définir sa charte.")],
)

# =========================================================================== #
# MODULE 2 — Connaître son audience
# =========================================================================== #

L2_1 = lesson(
    "Construire son persona",
    "Décrire précisément la personne idéale que vos contenus doivent attirer.",
    ["Construire un persona détaillé et réaliste", "Identifier les douleurs, désirs et objections de sa cible", "Utiliser le persona pour choisir ses sujets"],
    30, "atelier",
    "On ne crée pas du contenu « pour les réseaux », on le crée **pour une personne**. Plus vous la connaissez, plus vos contenus donnent l'impression de lire dans ses pensées. C'est ce sentiment qui fait s'abonner, commenter et acheter.",
    [
        ("Les 6 blocs d'un persona utile",
         "| Bloc | Questions |\n|---|---|\n| **Situation** | Âge, métier, contexte de vie et de travail |\n| **Douleurs** | Qu'est-ce qui l'empêche de dormir ? Qu'est-ce qui lui coûte du temps ou de l'argent ? |\n| **Désirs** | À quoi ressemble sa vie idéale dans 12 mois ? |\n| **Objections** | Pourquoi n'a-t-elle pas encore résolu le problème ? (prix, temps, doute, mauvaise expérience) |\n| **Habitudes** | Quels réseaux, à quel moment, quels comptes suit-elle ? |\n| **Vocabulaire** | Avec quels mots exacts décrit-elle son problème ? |\n\nLe dernier bloc est le plus sous-estimé : **utiliser les mots de votre audience** rend vos accroches immédiatement pertinentes."),
        ("Du persona aux sujets de contenu",
         "Chaque bloc devient une source de contenus :\n\n- **Douleurs** → contenus qui nomment le problème (*« Vous publiez tous les jours et personne ne réagit ? »*).\n- **Désirs** → contenus d'inspiration et de résultats clients.\n- **Objections** → contenus qui déconstruisent les croyances (*« Non, il ne faut pas 10 000 abonnés pour vendre »*).\n- **Vocabulaire** → titres et accroches."),
        ("Un persona vivant, pas une fiche oubliée",
         "Donnez-lui un prénom et une photo, affichez-le près de votre écran. Avant chaque publication, demandez-vous : **« Est-ce que [prénom] s'arrêterait sur ce contenu ? »** Mettez-le à jour tous les trimestres avec ce que vous apprenez en échangeant avec votre audience."),
    ],
    [
        ("Persona : « Claire, 38 ans »",
         "*Claire, 38 ans, responsable RH dans une PME de 80 salariés. Elle recrute seule, manque de temps, et voit ses offres ignorées sur les jobboards. **Douleur** : « Je passe mes soirées à trier des CV qui ne correspondent pas. » **Désir** : attirer des candidats qui viennent d'eux-mêmes. **Objection** : « LinkedIn, c'est pour les grandes entreprises avec un budget marque employeur. » **Habitudes** : LinkedIn le matin dans les transports. **Vocabulaire** : « galère de recrutement », « candidats fantômes ».*\n\nUn consultant qui cible Claire publiera : *« Candidats fantômes : 3 raisons pour lesquelles vos offres n'attirent personne (et ce n'est pas le salaire). »*"),
    ],
    ["On crée pour une personne, pas pour « tout le monde »", "Persona = situation, douleurs, désirs, objections, habitudes, vocabulaire", "Les mots exacts de l'audience font les meilleures accroches", "Chaque bloc du persona est une source de sujets"],
    ("Votre persona en une page",
     "Remplissez les 6 blocs pour votre client idéal. Donnez-lui un prénom. Puis déduisez-en **10 idées de contenus** : 3 sur ses douleurs, 3 sur ses désirs, 4 sur ses objections.",
     "moyen", 30,
     "**Grille d'autocorrection** :\n\n- Les douleurs sont **concrètes et vécues** (« je trie des CV le soir ») et pas abstraites (« manque d'efficacité »).\n- Au moins 3 expressions du bloc vocabulaire viennent de **vraies conversations** ou de commentaires lus, pas de votre imagination.\n- Chaque idée de contenu pourrait commencer par une phrase que votre persona dirait elle-même.\n\nSi vous bloquez sur le vocabulaire, passez directement à la leçon 2.2 : elle vous donne les méthodes pour le récolter."),
    ["Créer un persona trop large (« les entrepreneurs de 25 à 55 ans »)", "Inventer les douleurs au lieu de les vérifier", "Parler avec son jargon d'expert au lieu des mots de l'audience"],
    [("Méthode Jobs To Be Done — Clayton Christensen (« Competing Against Luck »)", "livre", "Comprendre le « travail » pour lequel un client « embauche » un produit.")],
)

L2_2 = lesson(
    "Écouter et étudier son audience",
    "Récolter les vrais problèmes et les vrais mots de sa cible, gratuitement.",
    ["Mener des entretiens d'audience efficaces", "Exploiter commentaires, groupes et outils de recherche", "Organiser ses découvertes dans une banque d'idées"],
    30, "atelier + outils",
    "Les meilleurs créateurs ne sont pas ceux qui ont le plus d'idées, mais ceux qui **écoutent le mieux**. Votre audience vous dit chaque jour ce qu'elle veut lire et acheter : il suffit de savoir où regarder.",
    [
        ("Les entretiens : la méthode la plus puissante",
         "Proposez 20 minutes d'échange à 5 à 10 personnes de votre cible. Posez des questions sur **leur passé réel**, pas sur des intentions :\n\n1. *« Raconte-moi la dernière fois que tu as rencontré [problème]. »*\n2. *« Qu'as-tu essayé ? Qu'est-ce qui n'a pas marché ? »*\n3. *« Qu'est-ce qui serait différent si c'était réglé ? »*\n4. *« Où cherches-tu des conseils sur ce sujet ? »*\n\nÉvitez : *« Est-ce que tu achèterais… ? »* Les gens répondent oui par politesse. Notez **les phrases exactes** : ce seront vos futures accroches."),
        ("Les mines d'or en ligne",
         "- **Commentaires** des comptes influents de votre niche : les questions qui reviennent sont des sujets de contenus.\n- **Groupes** Facebook, LinkedIn, Reddit, Discord : lisez les messages « J'ai besoin d'aide ».\n- **Avis clients** 1 à 3 étoiles de livres ou formations concurrentes : ils révèlent les attentes déçues.\n- **Suggestions de recherche** : Google, YouTube et TikTok complètent automatiquement les recherches fréquentes.\n- **Outils** : Google Trends (tendances), AnswerThePublic (questions posées)."),
        ("Votre banque d'idées",
         "Centralisez tout dans un seul outil (Notion, Google Sheets, application de notes) avec 4 colonnes :\n\n| Verbatim | Source | Type (douleur / désir / objection) | Idée de contenu |\n|---|---|---|---|\n| « Je n'ose pas me montrer en vidéo » | Entretien Marie | Objection | 5 formats pour percer sans montrer son visage |\n\nObjectif : ne plus jamais vous demander « sur quoi je publie aujourd'hui ? »."),
    ],
    [
        ("20 minutes qui changent une offre",
         "Une coach en organisation pensait que sa cible voulait « être plus productive ». En entretien, cinq mères entrepreneures ont toutes employé la même expression : **« J'ai l'impression de courir toute la journée et de ne rien avancer. »** Elle a réécrit sa bio et ses accroches avec cette phrase : ses messages privés ont nettement augmenté, car les lectrices se sont reconnues."),
    ],
    ["Les entretiens sur des situations passées valent mieux que les sondages", "Commentaires, groupes et avis négatifs sont des sources gratuites de sujets", "Notez les verbatims exacts", "Une banque d'idées supprime la panne d'inspiration"],
    ("Mission écoute",
     "En une semaine : réalisez **3 entretiens** avec des personnes de votre cible et collectez **20 verbatims** en ligne (commentaires, groupes, avis). Rangez-les dans votre banque d'idées et transformez les 5 meilleurs en titres de contenus.",
     "moyen", 120,
     "**Exemple de transformation verbatim → titre** :\n\n- « Je poste mais j'ai zéro commentaire » → *Zéro commentaire sur vos posts ? Le problème vient probablement de votre dernière ligne.*\n- « Je ne sais pas quoi raconter » → *47 idées de posts quand on pense n'avoir rien à dire.*\n- « Les gens trouvent ça trop cher » → *Si on vous dit « c'est trop cher », ce n'est (presque) jamais le prix.*\n\nUn bon titre reprend **les mots de l'audience** et promet une **réponse précise**."),
    ["Demander « est-ce que vous achèteriez ? » en entretien", "Ne consulter que les comptes à succès et jamais les commentaires", "Garder ses idées dans sa tête ou éparpillées"],
    [("Google Trends", "outil", "Visualiser l'évolution de l'intérêt pour un sujet."),
     ("AnswerThePublic", "outil", "Lister les questions que les internautes posent autour d'un mot-clé."),
     ("The Mom Test — Rob Fitzpatrick", "livre", "Comment interroger ses clients sans qu'ils vous mentent par politesse.")],
)

L2_3 = lesson(
    "Choisir ses plateformes",
    "Sélectionner 1 réseau principal et 1 secondaire en fonction de son audience et de ses forces.",
    ["Comparer les principaux réseaux sociaux", "Choisir un réseau principal et un secondaire", "Définir un rythme de publication tenable"],
    25, "texte + tableau comparatif",
    "Être partout, c'est souvent n'être bon nulle part. Mieux vaut **dominer un réseau** que survivre sur cinq. Cette leçon vous aide à choisir où concentrer votre énergie.",
    [
        ("Panorama des plateformes",
         "| Plateforme | Forces | Idéal pour |\n|---|---|---|\n| **LinkedIn** | Audience professionnelle, forte portée des posts texte et carrousels | B2B, consultants, recrutement, services aux entreprises |\n| **Instagram** | Visuel, Reels, stories pour la proximité | Lifestyle, bien-être, mode, food, créateurs, B2C |\n| **TikTok** | Découverte massive par l'algorithme, vidéos courtes | Croissance rapide, audiences jeunes et grand public |\n| **YouTube** | Contenu long, recherché, durable (effet moteur de recherche) | Expertise, tutoriels, confiance profonde |\n| **X (Twitter)** | Idées, actualité, conversations | Tech, finance, médias, réflexion |\n| **Newsletter** | Canal que vous possédez, relation directe | Tout le monde, en complément |\n\nLes algorithmes et usages évoluent vite : vérifiez régulièrement où se trouve réellement votre audience."),
        ("La règle 1 + 1 (+ 1)",
         "- **1 réseau principal** : là où se trouve votre persona et où votre format naturel (écrit, vidéo, image) est roi. 80 % de votre énergie.\n- **1 réseau secondaire** : où vous recyclez vos contenus. 20 %.\n- **+ 1 canal possédé** : newsletter ou liste e-mail. Vos abonnés sur un réseau peuvent disparaître si l'algorithme change ; votre liste e-mail vous appartient."),
        ("Un rythme tenable",
         "La régularité bat l'intensité. Mieux vaut **3 publications par semaine pendant 12 mois** que 2 par jour pendant 3 semaines.\n\nPoint de départ conseillé :\n- LinkedIn : 3 posts / semaine\n- Instagram : 3 à 4 publications + stories quasi quotidiennes\n- TikTok : 3 à 5 vidéos / semaine\n- YouTube : 1 vidéo / semaine ou toutes les 2 semaines\n- Newsletter : 1 / semaine ou 1 / 15 jours"),
    ],
    [
        ("Choix raisonné",
         "Une avocate en droit du travail qui cible les dirigeants de PME choisit **LinkedIn** en principal (ses clients y sont, elle écrit bien), **YouTube** en secondaire (des vidéos « Peut-on licencier pour… ? » très recherchées) et une **newsletter mensuelle** « L'actu sociale en 5 minutes »."),
    ],
    ["Mieux vaut dominer un réseau que survivre sur cinq", "Réseau principal = présence du persona + votre format naturel", "Construisez en parallèle un canal possédé (e-mail)", "Régularité > intensité"],
    ("Votre plan de présence",
     "Choisissez votre réseau principal, votre réseau secondaire et votre canal possédé. Justifiez chaque choix en 2 phrases (audience + format) et fixez un rythme hebdomadaire que vous êtes **sûr** de tenir pendant 3 mois.",
     "facile", 15,
     "**Contrôle** : votre choix est bon si (1) vous pouvez citer au moins 5 comptes suivis par votre persona sur ce réseau, (2) le format dominant du réseau correspond à celui où vous êtes le plus à l'aise ou prêt à progresser, (3) le rythme choisi représente moins de 5 heures par semaine au départ. Si un de ces points manque, revoyez le choix plutôt que de vous épuiser."),
    ["Ouvrir 5 comptes en même temps", "Choisir un réseau parce qu'il est à la mode et non parce que la cible y est", "Négliger la liste e-mail"],
    [("Substack / Brevo / Kit", "outil", "Plateformes pour démarrer une newsletter gratuitement.")],
)

# =========================================================================== #
# MODULE 3 — Créer du contenu qui marque
# =========================================================================== #

L3_1 = lesson(
    "Ses piliers de contenu et la stratégie éditoriale",
    "Définir 3 à 4 thématiques récurrentes et équilibrer les objectifs de ses contenus.",
    ["Définir ses piliers de contenu", "Équilibrer contenus de visibilité, de confiance et de conversion", "Construire un calendrier éditorial"],
    30, "atelier",
    "Sans stratégie éditoriale, on publie au gré de l'humeur et l'audience ne comprend pas pourquoi vous suivre. Les **piliers de contenu** donnent une colonne vertébrale à votre marque.",
    [
        ("Définir 3 à 4 piliers",
         "Un pilier est une **thématique récurrente** liée à votre positionnement. Exemple pour une coach LinkedIn pour dirigeants :\n\n1. **Écrire sur LinkedIn** (méthodes, structures de posts)\n2. **Leadership visible** (pourquoi et comment un dirigeant prend la parole)\n3. **Coulisses et résultats** (accompagnements, avant / après)\n4. **Convictions** (prises de position sur le secteur)\n\nChaque idée de votre banque d'idées doit pouvoir se ranger dans un pilier."),
        ("Les 3 objectifs d'un contenu",
         "| Objectif | Rôle | Exemples | Part conseillée |\n|---|---|---|---|\n| **Attirer** (visibilité) | Toucher de nouvelles personnes | Contenus larges, tendances, opinions fortes, listes | ~40 % |\n| **Nourrir** (confiance) | Prouver votre expertise, créer du lien | Tutoriels, méthodes, histoires, coulisses | ~40 % |\n| **Convertir** (vente) | Transformer en clients | Études de cas, témoignages, offres, appels à l'action | ~20 % |\n\nBeaucoup de créateurs ne font qu'attirer (beaucoup de vues, zéro vente) ou que vendre (audience qui se lasse)."),
        ("Le calendrier éditorial",
         "Sur un tableau simple, planifiez 4 semaines à l'avance :\n\n| Jour | Pilier | Objectif | Format | Sujet |\n|---|---|---|---|---|\n| Lundi | Méthode | Nourrir | Carrousel | 5 structures de posts qui marchent |\n| Mercredi | Conviction | Attirer | Texte | Pourquoi « poster tous les jours » est un mauvais conseil |\n| Vendredi | Résultats | Convertir | Étude de cas | Comment Marc a signé 3 clients en 2 mois |\n\nVous pouvez ainsi ajuster l'équilibre d'un coup d'œil."),
    ],
    [
        ("Un mois équilibré",
         "Une nutritionniste publie 12 contenus par mois : 5 pour attirer (*« 3 aliments « healthy » qui ne le sont pas »*), 5 pour nourrir (*recette express, explication de la satiété*), 2 pour convertir (*témoignage d'une cliente + ouverture des places de son programme*). Son audience grandit **et** ses places se remplissent."),
    ],
    ["3 à 4 piliers donnent une ligne éditoriale claire", "Chaque contenu a un objectif : attirer, nourrir ou convertir", "Repère : ~40 / 40 / 20", "Planifiez 4 semaines à l'avance"],
    ("Votre calendrier du mois",
     "Définissez vos 3 ou 4 piliers, puis remplissez un calendrier de 12 contenus sur 4 semaines en respectant l'équilibre attirer / nourrir / convertir.",
     "moyen", 45,
     "**Vérification** :\n\n- Chaque pilier apparaît au moins 2 fois dans le mois.\n- Vous avez 4 à 5 contenus « attirer », 4 à 5 « nourrir » et 2 à 3 « convertir ».\n- Les contenus « convertir » arrivent **après** des contenus « nourrir » sur le même thème (on prouve avant de vendre).\n- Au moins 3 sujets viennent directement de votre banque de verbatims (leçon 2.2)."),
    ["Ne publier que des contenus de visibilité sans jamais proposer son offre", "Avoir 10 piliers (plus de ligne claire)", "Planifier au jour le jour"],
    [("Notion", "outil", "Base de données pour gérer banque d'idées et calendrier éditorial."),
     ("Trello", "outil", "Tableau visuel idée → rédaction → programmé → publié.")],
)

L3_2 = lesson(
    "Écrire des accroches et des contenus qui retiennent",
    "Maîtriser les accroches, les structures de contenus et les appels à l'action.",
    ["Rédiger des accroches qui arrêtent le défilement", "Structurer un contenu avec des modèles éprouvés", "Terminer par un appel à l'action adapté"],
    40, "atelier d'écriture",
    "Sur les réseaux, vous avez **quelques secondes** pour convaincre quelqu'un d'arrêter de faire défiler. L'accroche décide si votre contenu sera lu ; la structure décide s'il sera retenu ; l'appel à l'action décide s'il sera utile à votre marque.",
    [
        ("7 types d'accroches",
         "| Type | Exemple |\n|---|---|\n| **Chiffre précis** | « J'ai analysé 100 profils LinkedIn de freelances. 83 font la même erreur. » |\n| **Contre-intuitif** | « Arrêtez de publier tous les jours. » |\n| **Question qui pique** | « Pourquoi vos concurrents moins bons que vous signent plus de clients ? » |\n| **Histoire** | « Il y a 2 ans, j'ai perdu mon plus gros client en une phrase. » |\n| **Promesse** | « La méthode en 3 étapes pour écrire un post en 20 minutes. » |\n| **Avant / après** | « De 0 à 5 rendez-vous par mois sans prospection à froid. » |\n| **Identification** | « Si vous avez déjà réécrit un post 6 fois avant de le supprimer, lisez ceci. » |\n\nRègle : la première ligne doit donner envie de lire la deuxième, et ainsi de suite."),
        ("3 structures qui fonctionnent",
         "**PAS (Problème – Agitation – Solution)**\n1. Nommer le problème. 2. Montrer ce qu'il coûte. 3. Apporter la solution.\n\n**L'histoire en 4 temps**\n1. Situation. 2. Obstacle. 3. Tournant. 4. Leçon pour le lecteur.\n\n**La liste actionnable**\n1. Promesse. 2. 3 à 7 points concrets, un par ligne. 3. Synthèse + question.\n\nMise en forme : phrases courtes, une idée par ligne, beaucoup d'espace, pas de pavé."),
        ("L'appel à l'action (CTA)",
         "Chaque contenu se termine par **une seule** action demandée, adaptée à son objectif :\n\n- **Attirer** → *« Quelle est la pire accroche que vous ayez lue ? »* (commentaires)\n- **Nourrir** → *« Enregistrez ce post pour votre prochaine rédaction. »* (sauvegardes)\n- **Convertir** → *« Écrivez-moi « AUDIT » en message privé pour recevoir l'analyse de votre profil. »*\n\nUn CTA flou (« N'hésitez pas à me suivre ») est rarement suivi d'effet."),
        ("La valeur avant tout",
         "Une accroche forte sur un contenu creux abîme votre marque. Test avant publication : **le lecteur apprend-il quelque chose, se sent-il compris, ou a-t-il envie d'agir ?** Si aucune des trois, retravaillez."),
    ],
    [
        ("Post LinkedIn réécrit",
         "**Avant** : *« Aujourd'hui je voulais vous parler de l'importance de la photo de profil sur LinkedIn. »*\n\n**Après** : *« Votre photo de profil vous fait perdre des clients avant même qu'ils lisent votre titre.*\n\n*3 erreurs que je vois chaque semaine :*\n*→ Photo de mariage recadrée*\n*→ Lunettes de soleil*\n*→ Visage minuscule sur un paysage*\n\n*La règle : visage net, regard caméra, fond neutre, 60 % du cadre.*\n\n*Quelle est votre photo actuelle : pro ou vacances ? »*"),
    ],
    ["L'accroche décide si le contenu est lu", "7 types d'accroches : chiffre, contre-intuitif, question, histoire, promesse, avant/après, identification", "Structures : PAS, histoire en 4 temps, liste actionnable", "Un seul appel à l'action, adapté à l'objectif"],
    ("Atelier d'accroches",
     "Prenez un sujet de votre calendrier. Écrivez **7 accroches**, une par type. Choisissez la meilleure, rédigez le contenu complet avec l'une des 3 structures et terminez par un CTA adapté à son objectif.",
     "moyen", 40,
     "**Exemple corrigé** (sujet : trouver des idées de contenus) :\n\n1. Chiffre : *« 47 idées de posts pour ceux qui pensent n'avoir rien à dire. »*\n2. Contre-intuitif : *« Vous n'avez pas un problème d'inspiration. Vous avez un problème d'écoute. »*\n3. Question : *« Pourquoi certains créateurs ne sont-ils jamais à court d'idées ? »*\n4. Histoire : *« Un lundi, j'ai fixé mon écran 40 minutes sans rien écrire. »*\n5. Promesse : *« La méthode pour ne plus jamais chercher quoi publier. »*\n6. Avant / après : *« Avant, je cherchais une idée par jour. Maintenant j'en ai 200 d'avance. »*\n7. Identification : *« Si vous ouvrez LinkedIn en vous disant « bon, je poste quoi ? », ce post est pour vous. »*\n\nLa n°2 est souvent la plus forte : elle surprend et amène naturellement la méthode (banque d'idées), puis un CTA « Enregistrez ce post »."),
    ["Commencer par « Aujourd'hui je voulais vous parler de… »", "Mettre 3 appels à l'action différents", "Accroche racoleuse qui ne tient pas sa promesse"],
    [("Contagious — Jonah Berger", "livre", "Pourquoi certaines idées se partagent et d'autres non."),
     ("Écrire pour convaincre (ressources de copywriting)", "article", "Cherchez les ressources sur les formules AIDA et PAS pour approfondir.")],
)

L3_3 = lesson(
    "Les formats et le système de production",
    "Maîtriser les formats clés et produire efficacement grâce au batching et au recyclage.",
    ["Choisir les bons formats pour chaque réseau", "Mettre en place un système de production par lots", "Recycler un contenu en plusieurs formats"],
    35, "démonstration + atelier",
    "La régularité ne dépend pas de la motivation, mais d'un **système**. Cette leçon vous donne une méthode pour produire un mois de contenus en quelques sessions, sans y passer vos soirées.",
    [
        ("Les formats incontournables",
         "- **Post texte** : rapide, idéal pour les opinions et les histoires (LinkedIn, X).\n- **Carrousel** : très sauvegardé, parfait pour les méthodes étape par étape (LinkedIn, Instagram).\n- **Vidéo courte (Reels, TikTok, Shorts)** : forte découverte ; accroche visuelle et orale dans les 2 premières secondes, sous-titres obligatoires (beaucoup regardent sans le son).\n- **Vidéo longue** : crée une confiance profonde et reste trouvable des années (YouTube).\n- **Stories / lives** : proximité, coulisses, questions-réponses.\n- **Newsletter** : relation directe, idéale pour vendre."),
        ("Le batching : produire par lots",
         "Regroupez les tâches semblables au lieu de tout faire chaque jour :\n\n| Session | Durée | Tâche |\n|---|---|---|\n| 1 | 1 h | Choisir 12 sujets dans la banque d'idées |\n| 2 | 2 h | Rédiger tous les textes et scripts |\n| 3 | 2 h | Tourner toutes les vidéos (même tenue, même lumière) |\n| 4 | 1 h 30 | Créer les visuels à partir de vos modèles |\n| 5 | 30 min | Programmer les publications |\n\nEnviron **7 heures par mois** pour 12 contenus, au lieu de 1 h de stress par jour."),
        ("Le recyclage : 1 idée, 5 contenus",
         "Une même idée peut devenir :\n\n1. Une **vidéo longue** ou un article (contenu « pilier »)\n2. Un **carrousel** avec les étapes clés\n3. Une **vidéo courte** avec le conseil le plus surprenant\n4. Un **post texte** racontant l'histoire derrière\n5. Une **newsletter** qui approfondit avec un exemple\n\nVotre audience ne voit pas tout : répéter une bonne idée sous une autre forme **n'est pas du radotage, c'est de la pédagogie**."),
    ],
    [
        ("Une idée, une semaine de contenus",
         "Un formateur en prise de parole enregistre une vidéo YouTube de 12 minutes « Comment ne plus trembler avant une présentation ». Il en tire : un carrousel « 5 techniques anti-trac », 3 Reels (respiration, première phrase, regard), un post LinkedIn racontant sa pire présentation et sa newsletter de la semaine. **Une seule session de réflexion, sept publications.**"),
    ],
    ["La régularité vient d'un système, pas de la motivation", "Le batching regroupe les tâches similaires", "Une idée pilier peut devenir 5 contenus", "Sous-titrez toujours vos vidéos"],
    ("Votre première session de batching",
     "Planifiez et réalisez une session de production : choisissez 1 idée pilier, puis déclinez-la en au moins 4 formats adaptés à vos réseaux. Chronométrez le temps passé sur chaque étape.",
     "difficile", 180,
     "**Déroulé attendu** :\n\n1. Idée pilier choisie dans la banque d'idées (≈ 10 min).\n2. Plan du contenu pilier en 5 points (≈ 20 min).\n3. Rédaction / tournage du contenu pilier (≈ 60 min).\n4. Déclinaisons : carrousel (≈ 30 min avec modèle), vidéo courte (≈ 20 min), post texte (≈ 15 min), newsletter (≈ 25 min).\n\n**Analyse** : repérez l'étape la plus longue. C'est souvent la création visuelle : investissez alors 1 h dans 3 modèles réutilisables, vous la diviserez par deux dès la session suivante."),
    ["Créer chaque contenu à la dernière minute", "Publier des vidéos sans sous-titres", "Penser qu'il faut toujours de nouvelles idées"],
    [("CapCut", "outil", "Montage vidéo mobile et ordinateur, sous-titres automatiques."),
     ("Buffer / Metricool", "outil", "Programmation des publications sur plusieurs réseaux.")],
)

# =========================================================================== #
# MODULE 4 — Exploser sur les réseaux
# =========================================================================== #

L4_1 = lesson(
    "Comprendre les algorithmes et optimiser son profil",
    "Savoir ce que récompensent les plateformes et transformer son profil en page d'accueil qui convertit.",
    ["Expliquer les signaux qui favorisent la diffusion d'un contenu", "Optimiser photo, titre, bio et lien de son profil", "Mettre en place un contenu épinglé stratégique"],
    30, "texte + audit",
    "Chaque plateforme a ses règles, qui changent souvent. Mais toutes cherchent la même chose : **garder les utilisateurs le plus longtemps possible**. Comprendre ce principe vaut mieux que courir après chaque « astuce algorithme ». Et quand un contenu vous amène un visiteur, c'est votre **profil** qui décide s'il s'abonne.",
    [
        ("Ce que les algorithmes récompensent",
         "De manière générale, un contenu est davantage diffusé quand il génère :\n\n- **Du temps passé** : vidéo regardée jusqu'au bout, carrousel parcouru, post lu en entier.\n- **Des interactions de qualité** : commentaires développés, partages, sauvegardes (plus précieux qu'un simple « j'aime »).\n- **Des réactions rapides** après la publication, qui signalent un intérêt.\n\nConséquences pratiques : soignez l'accroche (rétention), posez une vraie question (commentaires), apportez de la valeur réutilisable (sauvegardes), et **répondez aux commentaires** dans la première heure."),
        ("Le profil : votre vitrine",
         "Un visiteur décide en quelques secondes. Checklist :\n\n| Élément | Bonne pratique |\n|---|---|\n| **Photo** | Visage net, souriant, fond neutre, identique partout |\n| **Nom** | Votre nom (+ éventuellement votre spécialité sur certains réseaux) |\n| **Titre / bio** | Votre phrase de positionnement : pour qui, quel résultat |\n| **Preuve** | Un chiffre, une référence, un résultat client |\n| **Appel à l'action** | Ce que le visiteur doit faire : télécharger, s'abonner, réserver |\n| **Lien** | Une page claire (ressource gratuite ou prise de rendez-vous), pas 12 liens |"),
        ("Le contenu épinglé",
         "Épinglez en haut de votre profil 1 à 3 contenus qui répondent à : **Qui êtes-vous ? Que pouvez-vous m'apporter ? Comment travailler avec vous ?** Par exemple : votre histoire (leçon 1.3), votre meilleur contenu de méthode, un témoignage client."),
    ],
    [
        ("Bio avant / après",
         "**Avant** : *« Passionnée de marketing 🌸 | Maman | Café addict ☕ »*\n\n**Après** : *« J'aide les thérapeutes à remplir leur agenda avec Instagram 🌿 | +120 praticiens accompagnés | 👇 Mon guide gratuit : 30 idées de posts »*\n\nLa seconde dit **pour qui**, **quel résultat**, apporte **une preuve** et donne **une action**."),
    ],
    ["Les plateformes récompensent le temps passé et les interactions de qualité", "Commentaires, partages et sauvegardes valent plus que des « j'aime »", "Répondez aux commentaires rapidement", "Profil = photo + promesse + preuve + action + lien unique", "Épinglez vos 3 contenus les plus stratégiques"],
    ("Audit de profil",
     "Faites une capture de votre profil actuel. Notez chaque élément de la checklist sur 2 (0 = absent, 1 = moyen, 2 = excellent). Réécrivez tous les éléments notés sous 2, puis choisissez vos 3 contenus à épingler.",
     "facile", 30,
     "**Barème** : sur 12 points (6 éléments × 2).\n\n- **0 à 5** : votre profil fait fuir les visiteurs ; priorité absolue avant de chercher plus de visibilité.\n- **6 à 9** : correct, mais vous perdez des abonnés potentiels ; travaillez la preuve et l'appel à l'action.\n- **10 à 12** : excellent, concentrez-vous sur la création de contenu.\n\nL'erreur la plus fréquente : une bio qui parle de **vous** (passions, traits de caractère) au lieu de parler du **résultat pour le visiteur**."),
    ["Chercher des astuces pour « tromper » l'algorithme", "Bio centrée sur soi au lieu du bénéfice client", "Un lien vers une page d'accueil générique"],
    [("Centres d'aide officiels des plateformes (LinkedIn, Instagram, TikTok, YouTube)", "documentation", "Les plateformes publient elles-mêmes des conseils sur ce qui favorise la recommandation de contenus.")],
)

L4_2 = lesson(
    "Les leviers de croissance",
    "Accélérer sa croissance avec l'engagement, les collaborations et les contenus à fort potentiel de partage.",
    ["Pratiquer l'engagement stratégique", "Mettre en place des collaborations", "Créer des contenus conçus pour être partagés"],
    30, "texte + plan d'action",
    "Publier ne suffit pas au début : personne ne vous connaît encore. Pour accélérer, il faut **aller chercher l'attention là où elle se trouve déjà** et donner aux gens des raisons de partager vos contenus.",
    [
        ("L'engagement stratégique (la routine des 20 minutes)",
         "Chaque jour, 20 minutes :\n\n1. **Listez 20 à 30 comptes** suivis par votre persona (créateurs de la niche, médias, clients potentiels).\n2. **Laissez 5 à 10 commentaires qui apportent de la valeur** : un complément, un exemple, un avis argumenté. Jamais « Super post ! 👏 ».\n3. **Répondez à tous les commentaires** reçus sur vos propres contenus.\n\nUn commentaire pertinent sur un compte suivi par des milliers de personnes est un **mini-contenu vu par votre cible**."),
        ("Les collaborations",
         "Empruntez l'audience des autres, en échange de valeur :\n\n- **Interviews croisées** : vous recevez un expert, il vous reçoit.\n- **Lives à deux** sur Instagram, LinkedIn ou TikTok.\n- **Contenus co-signés** (collab Instagram, carrousel commun).\n- **Invité** dans des podcasts, newsletters, webinaires.\n\nCiblez des profils **complémentaires et non concurrents**, avec une audience proche de la vôtre (une nutritionniste et un coach sportif, par exemple). Commencez par des comptes de taille similaire."),
        ("Créer pour être partagé",
         "On partage un contenu quand il nous **fait bien paraître**, nous **est utile** ou **exprime ce qu'on pense**. Formats à fort potentiel :\n\n- Les **ressources de référence** (checklist, modèle, glossaire)\n- Les **opinions tranchées** sur un débat de la niche\n- Les **contenus d'identification** (« Les 7 étapes de tout freelance le lundi matin »)\n- Les **données originales** (votre propre mini-sondage ou analyse)"),
        ("Tendances : à utiliser avec discernement",
         "Surfer sur un son, un format ou une actualité peut apporter un pic de vues. Mais adaptez toujours la tendance **à votre positionnement** : une tendance sans lien avec votre expertise attire une audience qui n'achètera jamais."),
    ],
    [
        ("La routine qui fait décoller",
         "Un consultant en cybersécurité démarre LinkedIn avec quelques centaines de relations. Pendant 3 mois, il publie 3 posts par semaine **et** commente chaque matin les publications de 5 DSI et médias tech en ajoutant un vrai retour d'expérience. Plusieurs DSI commencent à le suivre après avoir lu ses commentaires, et deux l'invitent à intervenir dans leur podcast. Ses commentaires ont été sa meilleure source de visibilité les premiers mois."),
    ],
    ["Au début, commenter chez les autres est aussi important que publier", "Un commentaire doit apporter de la valeur, jamais « Super post »", "Collaborez avec des profils complémentaires", "On partage ce qui est utile, ce qui fait bien paraître ou ce qui exprime notre avis", "Les tendances doivent servir votre positionnement"],
    ("Plan de croissance de 30 jours",
     "1. Listez 25 comptes stratégiques où se trouve votre persona.\n2. Tenez la routine des 20 minutes pendant 30 jours (cochez chaque jour).\n3. Identifiez 5 partenaires de collaboration possibles et envoyez 2 propositions.\n4. Créez 1 contenu « à partager » (ressource, opinion ou donnée originale).",
     "difficile", 600,
     "**Modèle de proposition de collaboration** :\n\n*« Bonjour [prénom], je suis ton contenu sur [sujet] depuis quelques mois, en particulier ton post sur [exemple précis]. Je travaille avec [public] sur [sujet complémentaire]. Je pense que nos audiences se recoupent sans qu'on se fasse concurrence. Ça te dirait de faire un live de 30 minutes sur [sujet commun] ? Je m'occupe de préparer le déroulé. »*\n\nPourquoi ça marche : message personnalisé, bénéfice mutuel, proposition concrète et effort pris en charge.\n\n**Indicateurs à suivre au bout de 30 jours** : nombre de visites de profil, nouveaux abonnés venus de vos commentaires, réponses aux propositions."),
    ["Commentaires génériques ou auto-promotionnels", "Proposer une collaboration sans jamais avoir interagi avec la personne", "Suivre toutes les tendances même hors sujet"],
    [("Show Your Work! (Montrez votre travail) — Austin Kleon", "livre", "Chapitres sur l'art de partager et de construire un réseau."),
     ("Podcasts de votre niche", "outil", "Listez ceux qui reçoivent des invités : ce sont des opportunités de visibilité.")],
)

L4_3 = lesson(
    "Mesurer, analyser, ajuster",
    "Suivre les bons indicateurs et améliorer sa stratégie grâce aux données.",
    ["Distinguer indicateurs de vanité et indicateurs utiles", "Mettre en place un tableau de bord mensuel", "Tester et améliorer ses contenus de manière méthodique"],
    25, "texte + tableau de bord",
    "Ce qui ne se mesure pas ne s'améliore pas. Mais mesurer les mauvais chiffres est pire : on optimise des vues au lieu d'optimiser des ventes. Cette leçon vous apprend à lire vos statistiques comme un tableau de bord d'entreprise.",
    [
        ("Vanité contre utilité",
         "| Indicateur | Type | Ce qu'il dit |\n|---|---|---|\n| Nombre d'abonnés | Vanité (seul) | Taille, pas qualité |\n| Vues / impressions | Visibilité | Portée de l'accroche et du sujet |\n| Taux d'interaction | Utile | Pertinence du contenu |\n| Sauvegardes et partages | Très utile | Valeur perçue |\n| Visites de profil | Très utile | Curiosité envers **vous** |\n| Inscriptions e-mail | Business | Audience possédée |\n| Messages privés / rendez-vous | Business | Intention d'achat |\n| Clients et chiffre d'affaires | Business | Le vrai résultat |\n\nTaux d'interaction = (réactions + commentaires + partages + sauvegardes) ÷ vues × 100."),
        ("Le tableau de bord mensuel",
         "Une fois par mois, notez :\n\n1. Vos **3 meilleurs contenus** (par sauvegardes, commentaires ou prises de contact) et ce qu'ils ont en commun (sujet, format, accroche).\n2. Vos **3 moins bons** et une hypothèse pour chacun.\n3. Les chiffres business : inscrits, rendez-vous, ventes.\n4. **Une décision** pour le mois suivant (faire plus de…, arrêter…, tester…)."),
        ("Tester méthodiquement",
         "Changez **une seule variable à la fois** : l'accroche, le format, l'heure ou le sujet. Exemple : publier la même méthode en post texte une semaine, en carrousel la suivante. Comparez sur plusieurs contenus avant de conclure : un seul contenu qui fonctionne ou non peut être dû au hasard."),
    ],
    [
        ("La leçon des chiffres",
         "Une coach constate que ses Reels humoristiques font beaucoup de vues mais aucune prise de contact, alors que ses carrousels « méthode » font moins de vues mais génèrent l'essentiel de ses rendez-vous. Décision : elle garde 1 Reel humoristique par semaine pour attirer et double ses carrousels méthode, en ajoutant un CTA vers son appel découverte."),
    ],
    ["Les abonnés seuls sont un indicateur de vanité", "Suivez sauvegardes, visites de profil, inscrits, rendez-vous", "Bilan mensuel : top 3, flop 3, une décision", "Testez une variable à la fois, sur plusieurs contenus"],
    ("Votre premier bilan",
     "Exportez les statistiques de vos 10 derniers contenus. Calculez le taux d'interaction de chacun, identifiez le top 3 et le flop 3, trouvez un point commun à chaque groupe et formulez une décision pour le mois prochain.",
     "moyen", 40,
     "**Exemple d'analyse** :\n\n- Top 3 : trois carrousels « étape par étape », accroches avec un chiffre, publiés le mardi. Point commun : **méthode concrète et chiffrée**.\n- Flop 3 : trois posts d'humeur sans conseil actionnable. Point commun : **pas de bénéfice clair pour le lecteur**.\n- Décision : *« Ce mois-ci, 2 carrousels méthode par semaine, et je transforme mes posts d'humeur en histoires avec une leçon concrète. »*\n\nSi vous avez moins de 10 contenus, faites l'exercice quand même : l'habitude compte plus que la taille de l'échantillon."),
    ["Juger une stratégie sur un seul contenu", "Changer plusieurs choses à la fois", "Ne regarder que les vues"],
    [("Statistiques natives des plateformes", "outil", "LinkedIn, Instagram, TikTok et YouTube proposent des statistiques gratuites pour les comptes professionnels / créateurs."),
     ("Google Sheets", "outil", "Suffisant pour un tableau de bord mensuel simple.")],
)

# =========================================================================== #
# MODULE 5 — Vendre grâce à son image
# =========================================================================== #

L5_1 = lesson(
    "Construire une offre irrésistible",
    "Créer une offre claire qui prolonge naturellement votre marque et vos contenus.",
    ["Structurer une offre autour d'une transformation", "Construire une échelle d'offres", "Fixer un prix cohérent avec la valeur perçue"],
    35, "atelier",
    "Une audience sans offre, c'est de la notoriété qui ne paie pas les factures. Une offre bien construite est le **prolongement naturel** de ce que vous enseignez déjà dans vos contenus.",
    [
        ("Vendre une transformation, pas des heures",
         "Votre client n'achète pas « 6 séances de coaching » : il achète **le passage d'une situation A à une situation B**.\n\n| Mauvaise formulation | Bonne formulation |\n|---|---|\n| 6 séances d'1 h de coaching LinkedIn | En 6 semaines, un profil et une routine de publication qui vous amènent vos premiers rendez-vous clients |\n| Formation Canva de 4 h | Créez tous vos visuels du mois en 2 heures, sans graphiste |\n\nUne offre claire répond à : **pour qui, quel résultat, en combien de temps, comment, avec quelles garanties.**"),
        ("L'échelle d'offres",
         "Proposez plusieurs niveaux pour accompagner la montée en confiance :\n\n1. **Gratuit** : contenus, ressource téléchargeable (lead magnet) en échange d'un e-mail.\n2. **Petit prix** : guide, modèle, atelier (quelques dizaines d'euros). Transforme un abonné en client.\n3. **Offre principale** : programme, accompagnement, formation complète.\n4. **Premium** : accompagnement individuel, done-for-you, conseil.\n\nChaque niveau doit donner un vrai résultat **et** donner envie du suivant."),
        ("Augmenter la valeur perçue",
         "La valeur perçue dépend de 4 facteurs :\n\n- ⬆️ **Le résultat promis** (plus il est important et concret)\n- ⬆️ **La probabilité perçue de l'obtenir** (preuves, méthode, garanties)\n- ⬇️ **Le délai** avant résultat\n- ⬇️ **L'effort et les sacrifices** demandés\n\nAjoutez des éléments qui agissent sur ces leviers : modèles prêts à l'emploi (moins d'effort), suivi (plus de probabilité), bonus de démarrage rapide (délai réduit)."),
        ("Le prix",
         "Fixez-le par rapport à **la valeur du résultat** pour le client, pas à votre temps. Si votre accompagnement aide un freelance à signer un client à 3 000 €, un prix de 900 € reste un bon investissement pour lui. Votre marque personnelle vous permet de vous positionner au-dessus de la moyenne : **plus vous êtes perçu comme la référence, moins on vous compare sur le prix.**"),
    ],
    [
        ("Une échelle complète",
         "Une photographe culinaire construit : **gratuit** → guide « 10 réglages pour photographier vos plats au smartphone » ; **petit prix** → pack de préréglages à 29 € ; **offre principale** → formation en ligne « Photos de restaurant qui donnent faim » à 390 € ; **premium** → shooting sur place pour restaurants."),
    ],
    ["On vend une transformation : de A vers B", "Pour qui, quel résultat, quel délai, quelle méthode, quelles garanties", "Échelle : gratuit → petit prix → offre principale → premium", "Valeur perçue : résultat et probabilité ↑, délai et effort ↓", "Le prix se fixe sur la valeur du résultat"],
    ("Fiche offre",
     "Rédigez la fiche de votre offre principale : nom, promesse (A → B), public, durée, contenu, bonus, garantie, prix. Puis imaginez votre ressource gratuite et votre offre à petit prix.",
     "difficile", 60,
     "**Exemple corrigé** :\n\n- **Nom** : Le Programme Agenda Plein\n- **Promesse** : passer d'un agenda à moitié vide à 10 nouveaux patients par mois grâce à Instagram, en 90 jours.\n- **Public** : ostéopathes et kinés installés depuis moins de 5 ans.\n- **Contenu** : 6 modules vidéo, 30 modèles de publications, 1 appel de groupe par semaine.\n- **Bonus** : audit personnalisé du profil (augmente la probabilité perçue).\n- **Garantie** : si vous appliquez la méthode 60 jours sans résultat, accompagnement prolongé gratuitement.\n- **Prix** : 690 €.\n- **Gratuit** : checklist « Le profil Instagram qui remplit un cabinet ».\n- **Petit prix** : 30 modèles de posts à 27 €.\n\nVérifiez que votre promesse est **crédible** : ne promettez que des résultats que vous avez déjà obtenus pour vous ou pour des clients."),
    ["Vendre du temps au lieu d'un résultat", "N'avoir qu'une offre très chère sans étape intermédiaire", "Promettre des résultats qu'on ne peut pas prouver"],
    [("$100M Offers — Alex Hormozi", "livre", "Méthode détaillée pour construire une offre à forte valeur perçue (en anglais).")],
)

L5_2 = lesson(
    "Transformer son audience en clients",
    "Mettre en place le parcours qui mène de l'abonné au client : lead magnet, e-mail et messages privés.",
    ["Créer un lead magnet et une séquence e-mail", "Mener des conversations de vente en message privé sans être intrusif", "Réaliser un appel découverte qui convertit"],
    35, "atelier + scripts",
    "Vendre grâce à son image, ce n'est pas publier « achetez ma formation » en espérant que ça marche. C'est construire un **parcours** où chaque étape rapproche naturellement la personne de l'achat.",
    [
        ("Le parcours type",
         "1. **Contenu** (réseaux) → la personne vous découvre.\n2. **Profil** → elle comprend ce que vous faites.\n3. **Lead magnet** → elle vous donne son e-mail contre une ressource utile.\n4. **Séquence e-mail** → elle apprend à vous faire confiance.\n5. **Conversation / appel découverte** → vous vérifiez ensemble que l'offre lui convient.\n6. **Achat**."),
        ("Le lead magnet et la séquence de bienvenue",
         "Un bon lead magnet résout **un petit problème précis, rapidement** : checklist, modèle, mini-formation vidéo, quiz. Il doit être directement lié à votre offre payante.\n\nSéquence de bienvenue (5 e-mails sur 10 jours) :\n\n1. Livraison de la ressource + qui vous êtes\n2. Votre histoire (leçon 1.3)\n3. Une erreur fréquente et comment l'éviter\n4. Une étude de cas client\n5. Présentation de l'offre + invitation à un appel ou à l'achat"),
        ("La vente en message privé, sans forcer",
         "Principes :\n\n- **Répondez aux signaux**, ne démarchez pas à froid en masse : quelqu'un qui commente « c'est exactement mon problème », qui télécharge votre ressource, qui répond à une story.\n- **Commencez par une question**, pas par un lien : *« Merci pour ton commentaire ! C'est quoi ta situation actuelle avec [sujet] ? »*\n- **Écoutez**, reformulez, puis proposez **seulement si c'est pertinent** : *« Ce que tu décris, c'est exactement ce qu'on travaille dans [offre]. Tu veux qu'on en parle 20 minutes ? »*\n- Acceptez le « non » avec élégance : la relation vaut plus qu'une vente."),
        ("L'appel découverte en 5 étapes",
         "1. **Cadre** : « On a 30 minutes, je vais te poser des questions, et à la fin on voit si je peux t'aider. D'accord ? »\n2. **Situation actuelle** : où en es-tu ?\n3. **Objectif** : où veux-tu être dans 6 mois ? Pourquoi c'est important maintenant ?\n4. **Obstacles** : qu'est-ce qui t'en empêche ?\n5. **Proposition** : si c'est adapté, présentez l'offre comme le pont entre sa situation et son objectif, puis demandez clairement : « Est-ce que tu veux qu'on y aille ensemble ? »\n\nLe prospect doit parler environ **70 % du temps**."),
    ],
    [
        ("Un commentaire devenu client",
         "Sous un post sur la prise de parole, une manager commente : *« Je bloque complètement en réunion de direction. »* La formatrice lui écrit : *« Merci de l'avoir partagé, c'est très courant. Ça se passe comment concrètement ? »* Après quelques échanges, elle propose un appel ; la manager rejoint son programme. **Aucune relance insistante : de l'écoute et une proposition au bon moment.**"),
    ],
    ["Contenu → profil → lead magnet → e-mails → conversation → achat", "Le lead magnet résout vite un petit problème lié à l'offre", "En message privé : question d'abord, lien ensuite", "Appel découverte : cadre, situation, objectif, obstacles, proposition", "Le prospect parle 70 % du temps"],
    ("Votre parcours de vente",
     "1. Choisissez votre lead magnet et rédigez son titre.\n2. Écrivez le plan de votre séquence de 5 e-mails (objet + idée principale de chacun).\n3. Rédigez votre script de premier message privé en réponse à un commentaire.",
     "difficile", 60,
     "**Exemple d'objets d'e-mails** (thème : prise de parole) :\n\n1. *Ton guide « 5 minutes avant de parler » est là*\n2. *La réunion où j'ai perdu mes mots (et ce qu'elle m'a appris)*\n3. *L'erreur que font 9 managers sur 10 en début de réunion*\n4. *Comment Sophie a présenté son budget sans trembler*\n5. *Les inscriptions à « Voix de leader » sont ouvertes*\n\n**Script de message privé** :\n*« Merci pour ton commentaire [prénom] ! Tu parlais de [reprendre ses mots]. Ça se passe comment pour toi en ce moment ? »*\n\nÀ éviter : envoyer directement un lien de vente, copier-coller le même message à 50 personnes."),
    ["Envoyer des messages de vente automatiques à des inconnus", "Proposer l'offre sans avoir compris le besoin", "Parler plus que le prospect pendant l'appel"],
    [("Brevo / Kit / MailerLite", "outil", "Outils d'e-mailing pour lead magnet et séquences automatiques."),
     ("Calendly / Google Agenda (prise de rendez-vous)", "outil", "Permet aux prospects de réserver un appel découverte en un clic.")],
)

L5_3 = lesson(
    "Preuve sociale, réputation et durée",
    "Renforcer la confiance avec les témoignages, protéger sa réputation et installer sa marque dans le temps.",
    ["Collecter et utiliser des témoignages et études de cas", "Gérer les critiques et protéger son e-réputation", "Planifier sa marque sur 12 mois"],
    30, "texte + plan",
    "Ce que vous dites de vous est une promesse ; ce que vos clients disent de vous est une **preuve**. Une marque forte se construit sur des preuves accumulées, une réputation protégée et une présence qui dure.",
    [
        ("Collecter la preuve sociale",
         "- **Demandez systématiquement** un retour à la fin de chaque accompagnement, au moment où la satisfaction est la plus haute.\n- **Posez des questions guidées** : *Quelle était ta situation avant ? Qu'est-ce qui t'a fait hésiter ? Qu'est-ce qui a changé concrètement ? À qui recommanderais-tu cet accompagnement ?*\n- **Privilégiez les formats crédibles** : vidéo, capture de message avec accord, résultat chiffré, nom et photo réels (avec autorisation).\n- **Transformez les meilleurs en études de cas** : contexte, problème, solution, résultat chiffré."),
        ("Gérer les critiques",
         "Plus vous êtes visible, plus vous recevrez de critiques. Méthode :\n\n1. **Ne répondez jamais à chaud.**\n2. **Distinguez** critique constructive (à remercier et utiliser), désaccord d'opinion (à discuter avec respect) et attaque gratuite (à ignorer ou modérer).\n3. **Répondez publiquement avec calme** quand c'est utile : l'audience juge surtout votre réaction.\n4. **Réglez les problèmes clients en privé**, rapidement.\n\nVotre e-réputation, c'est aussi ce que l'on trouve en tapant votre nom sur un moteur de recherche : vérifiez-le régulièrement."),
        ("Tenir dans la durée",
         "La plupart des marques personnelles échouent par **abandon**, pas par manque de talent. Pour durer :\n\n- Un rythme réaliste (leçon 2.3) et un système de production (leçon 3.3).\n- Des **objectifs trimestriels** mesurables (inscrits, clients), pas seulement des abonnés.\n- Une **évolution progressive** : élargir sa niche, ajouter un format, lancer un produit, une fois les bases solides.\n- Des pauses **planifiées** plutôt que des disparitions : prévenez votre audience et programmez du contenu à l'avance."),
    ],
    [
        ("Étude de cas bien construite",
         "*« **Contexte** : Nadia, architecte d'intérieur, 3 ans d'activité, clients uniquement par bouche-à-oreille. **Problème** : des mois creux imprévisibles. **Solution** : positionnement sur les petites surfaces parisiennes, 3 carrousels « avant / après » par semaine, guide gratuit « Agrandir visuellement un studio ». **Résultat** : 340 inscrits à sa liste en 4 mois et 4 projets signés venant d'Instagram. »*\n\nCette structure permet au lecteur de se projeter : **« si elle y est arrivée dans ma situation, moi aussi. »**"),
    ],
    ["Ce que vos clients disent de vous vaut plus que ce que vous en dites", "Demandez les témoignages au moment de la satisfaction", "Étude de cas : contexte, problème, solution, résultat chiffré", "Ne répondez jamais à chaud aux critiques", "Les marques échouent surtout par abandon : planifiez la durée"],
    ("Plan de marque sur 12 mois",
     "Rédigez votre feuille de route sur 4 trimestres. Pour chacun : 1 objectif business mesurable, 1 objectif d'audience, 1 action de preuve sociale, 1 projet (nouveau format, collaboration, produit).",
     "moyen", 45,
     "**Exemple de feuille de route** :\n\n| Trimestre | Business | Audience | Preuve sociale | Projet |\n|---|---|---|---|---|\n| T1 | 3 clients offre principale | 300 inscrits e-mail | 3 témoignages écrits | Lead magnet + séquence e-mail |\n| T2 | 6 clients | 700 inscrits | 1 étude de cas vidéo | 4 collaborations en live |\n| T3 | Lancement offre petit prix : 50 ventes | 1 200 inscrits | Page témoignages | Réseau secondaire |\n| T4 | 10 clients + 1 premium | 2 000 inscrits | 5 études de cas | Programme de groupe |\n\nLes chiffres sont des exemples : fixez les vôtres selon votre point de départ, et révisez le plan à la fin de chaque trimestre avec votre bilan mensuel."),
    ["Publier des témoignages sans autorisation ou invérifiables", "Répondre aux critiques sous le coup de l'émotion", "Disparaître plusieurs semaines sans prévenir"],
    [("Google Alertes", "outil", "Recevoir une alerte quand votre nom ou votre marque est mentionné en ligne."),
     ("Senja / Testimonial.to", "outil", "Collecte et affichage de témoignages clients.")],
)

# =========================================================================== #
# Quiz, examen, projet, accompagnement
# =========================================================================== #

Q1 = quiz("Quiz — Les fondations de sa marque", [
    ("Quelle définition correspond le mieux à une marque personnelle ?", U, ["Le nombre d'abonnés sur ses réseaux", "L'association durable entre un nom, une promesse et un public précis", "Un logo et une charte graphique", "Le fait de publier tous les jours"], [1], "La marque est une idée claire dans l'esprit d'un public. Abonnés et logo n'en sont que des outils ou des conséquences.", "comprendre"),
    ("Un compte à 100 000 abonnés a forcément une marque personnelle forte.", VF, ["Vrai", "Faux"], [1], "Visibilité n'est pas marque : sans positionnement clair, le public ne retient rien de précis.", "comprendre"),
    ("Laquelle de ces phrases de positionnement est la plus efficace ?", U, ["J'aide les gens à réussir", "Coach business passionnée", "J'aide les graphistes freelances à dépasser 5 000 €/mois grâce à LinkedIn, sans prospection à froid", "Experte en marketing digital et réseaux sociaux"], [2], "Elle précise le public, le résultat, la méthode et l'objection traitée.", "évaluer"),
    ("Quelles sources peuvent constituer un angle différenciant ?", M, ["Votre parcours", "Votre méthode propriétaire", "Une conviction forte", "Copier le ton du créateur le plus suivi de la niche"], [0, 1, 2], "Parcours, méthode, conviction et ton personnel différencient. Copier un autre créateur fait de vous une copie.", "analyser"),
    ("Dans le récit de marque, à quoi sert l'étape « avant » ?", U, ["À raconter son enfance en détail", "À permettre à l'audience de se reconnaître dans votre situation passée", "À lister ses diplômes", "À présenter son offre"], [1], "L'« avant » crée l'identification : le lecteur se dit « c'est moi aujourd'hui ».", "comprendre"),
])
Q2 = quiz("Quiz — Connaître son audience", [
    ("Pourquoi noter les mots exacts de son audience ?", U, ["Pour les citer dans ses mentions légales", "Parce qu'ils rendent les accroches immédiatement parlantes pour la cible", "Pour améliorer son orthographe", "Ce n'est pas utile"], [1], "Utiliser le vocabulaire de la cible lui donne l'impression que vous lisez dans ses pensées.", "comprendre"),
    ("En entretien, quelle question est la plus fiable ?", U, ["Est-ce que tu achèterais ma formation ?", "Raconte-moi la dernière fois que tu as rencontré ce problème.", "Tu trouves mon idée bonne ?", "Combien tu serais prêt à payer ?"], [1], "Les questions sur des faits passés réels donnent des réponses fiables ; les questions hypothétiques entraînent des réponses polies.", "appliquer"),
    ("Quelles sont de bonnes sources pour découvrir les problèmes de votre audience ?", M, ["Les commentaires des comptes influents de la niche", "Les avis négatifs sur des produits concurrents", "Les groupes et forums de la niche", "Vos seules intuitions"], [0, 1, 2], "Les intuitions doivent être vérifiées ; les trois autres sources donnent des verbatims réels.", "analyser"),
    ("Il est recommandé de démarrer sur 5 réseaux sociaux en même temps pour maximiser ses chances.", VF, ["Vrai", "Faux"], [1], "Mieux vaut un réseau principal, un secondaire et un canal possédé (e-mail).", "comprendre"),
    ("Pourquoi construire une liste e-mail en parallèle des réseaux ?", U, ["Parce que les e-mails sont gratuits à envoyer", "Parce que c'est une audience que vous possédez, indépendante des algorithmes", "Parce que c'est obligatoire légalement", "Pour remplacer totalement les réseaux"], [1], "Vos abonnés sur un réseau dépendent de la plateforme ; votre liste vous appartient.", "comprendre"),
])
Q3 = quiz("Quiz — Créer du contenu qui marque", [
    ("Quel est l'équilibre de repère entre contenus attirer / nourrir / convertir ?", U, ["100 / 0 / 0", "40 / 40 / 20", "10 / 10 / 80", "33 / 33 / 33 en publiant uniquement des offres"], [1], "Environ 40 % pour attirer, 40 % pour créer la confiance et 20 % pour convertir.", "se souvenir"),
    ("Quelle accroche est de type « contre-intuitif » ?", U, ["Aujourd'hui je vais vous parler de LinkedIn", "Arrêtez de publier tous les jours", "Voici mon nouveau post", "Merci pour vos 1 000 abonnés"], [1], "Elle prend le contre-pied d'une idée reçue et crée la surprise.", "appliquer"),
    ("Combien d'appels à l'action faut-il idéalement à la fin d'un contenu ?", U, ["Aucun", "Un seul, adapté à l'objectif du contenu", "Trois pour multiplier les chances", "Autant que possible"], [1], "Plusieurs CTA dispersent l'attention ; un seul CTA clair est plus souvent suivi.", "comprendre"),
    ("Republier une bonne idée sous un autre format est une perte de temps pour l'audience.", VF, ["Vrai", "Faux"], [1], "Votre audience ne voit pas tout ; la répétition sous d'autres formes renforce le message.", "évaluer"),
    ("Quels sont les avantages du batching ?", M, ["Gain de temps grâce au regroupement des tâches", "Régularité de publication", "Moins de stress quotidien", "Il rend inutile toute planification"], [0, 1, 2], "Le batching repose justement sur la planification.", "analyser"),
])
Q4 = quiz("Quiz — Exploser sur les réseaux", [
    ("Quels signaux favorisent généralement la diffusion d'un contenu ?", M, ["Le temps passé sur le contenu", "Les commentaires et partages", "Les sauvegardes", "Le nombre de hashtags, plus il y en a mieux c'est"], [0, 1, 2], "Les plateformes privilégient ce qui retient et engage les utilisateurs ; accumuler des hashtags n'est pas un levier fiable.", "comprendre"),
    ("Quelle bio est la plus efficace ?", U, ["Passionnée | Maman | Café addict", "J'aide les thérapeutes à remplir leur agenda avec Instagram | +120 praticiens accompagnés | Guide gratuit ci-dessous", "Bienvenue sur mon compte", "Entrepreneur – Visionnaire – Leader"], [1], "Elle indique pour qui, quel résultat, une preuve et une action.", "évaluer"),
    ("Un bon commentaire stratégique sur le post d'un autre créateur, c'est :", U, ["« Super post ! »", "Un lien vers votre offre", "Un complément argumenté ou un exemple concret qui apporte de la valeur", "Un emoji"], [2], "Un commentaire utile est un mini-contenu vu par la cible.", "appliquer"),
    ("Pour tester l'effet du format, on change en même temps l'accroche, l'heure et le sujet.", VF, ["Vrai", "Faux"], [1], "On change une seule variable à la fois pour savoir ce qui a produit l'effet.", "analyser"),
    ("Quel indicateur est le plus proche du résultat business ?", U, ["Nombre d'abonnés", "Impressions", "Rendez-vous et messages privés qualifiés", "Nombre de « j'aime »"], [2], "Les conversations et rendez-vous traduisent une intention d'achat.", "évaluer"),
])
Q5 = quiz("Quiz — Vendre grâce à son image", [
    ("Quelle formulation d'offre est la plus convaincante ?", U, ["6 séances d'une heure", "Un accompagnement personnalisé de qualité", "En 6 semaines, un profil et une routine qui vous amènent vos premiers rendez-vous clients", "Coaching à 90 € de l'heure"], [2], "Elle vend une transformation concrète dans un délai donné.", "évaluer"),
    ("Quels facteurs augmentent la valeur perçue d'une offre ?", M, ["Un résultat promis important et concret", "Des preuves qui augmentent la probabilité de réussite", "Un délai plus court avant résultat", "Plus d'efforts demandés au client"], [0, 1, 2], "Plus d'effort demandé diminue la valeur perçue.", "analyser"),
    ("En message privé, que faire en premier après un commentaire intéressé ?", U, ["Envoyer le lien de paiement", "Poser une question sur sa situation", "Envoyer une plaquette de 20 pages", "Ne rien faire"], [1], "On commence par comprendre le besoin avant de proposer quoi que ce soit.", "appliquer"),
    ("Pendant un appel découverte, le vendeur doit parler la majorité du temps pour présenter son offre.", VF, ["Vrai", "Faux"], [1], "Le prospect doit parler environ 70 % du temps : c'est en l'écoutant qu'on sait si l'offre lui convient.", "comprendre"),
    ("Face à une critique publique virulente, la première règle est :", U, ["Répondre immédiatement pour se défendre", "Ne jamais répondre à chaud", "Supprimer son compte", "Répondre par une attaque"], [1], "Prendre du recul permet de distinguer critique utile, désaccord et attaque, et de répondre avec calme.", "appliquer"),
])

EXAM = quiz("Examen final — Personal branding", [
    ("Julie publie sur la nutrition, le sport, le voyage et la déco. Elle a beaucoup de vues mais aucune demande de clients. Quelle est la cause la plus probable ?", U, ["Elle ne publie pas assez", "Son positionnement est flou : personne ne sait pour quoi la recommander", "Son algorithme est bloqué", "Elle devrait acheter des abonnés"], [1], "Sans positionnement clair, la visibilité ne se transforme pas en marque ni en ventes.", "analyser"),
    ("Complétez le modèle de positionnement : « J'aide [qui] à [résultat] grâce à [méthode] sans [...] ».", U, ["la contrainte redoutée par la cible", "mon diplôme", "mon prix", "mes concurrents"], [0], "Nommer la contrainte redoutée lève une objection dès la première phrase.", "se souvenir"),
    ("Quel est l'ordre du récit de marque ?", U, ["Mission, avant, résultat, déclic, chemin", "Avant, déclic, chemin, résultat, mission", "Résultat, mission, avant, chemin, déclic", "Déclic, mission, avant, résultat, chemin"], [1], "Avant → déclic → chemin → résultat → mission.", "se souvenir"),
    ("Un créateur veut connaître les vrais problèmes de sa cible. Quelles actions sont pertinentes ?", M, ["Mener 5 entretiens sur des situations vécues", "Lire les avis négatifs de produits concurrents", "Lire les questions dans les groupes de la niche", "Demander « tu achèterais ? » à ses amis"], [0, 1, 2], "La dernière question produit des réponses de politesse.", "appliquer"),
    ("Une avocate en droit du travail cible les dirigeants de PME. Quel réseau principal est le plus cohérent ?", U, ["TikTok avec des danses", "LinkedIn", "Pinterest", "Twitch"], [1], "Son audience professionnelle y est présente et le format écrit/expertise y fonctionne bien.", "appliquer"),
    ("Sur 12 contenus mensuels, combien devraient environ viser directement la conversion ?", U, ["0", "2 à 3", "8", "12"], [1], "Environ 20 % : 2 à 3 contenus sur 12.", "appliquer"),
    ("Quelle accroche utilise un chiffre précis ?", U, ["Voici mes conseils", "J'ai analysé 100 profils de freelances : 83 font la même erreur", "Parlons de LinkedIn", "Un post important"], [1], "Le chiffre précis rend la promesse concrète et crédible.", "comprendre"),
    ("Le recyclage consiste à décliner une idée pilier en plusieurs formats adaptés à chaque réseau.", VF, ["Vrai", "Faux"], [0], "Une idée peut devenir vidéo, carrousel, post, vidéo courte et newsletter.", "comprendre"),
    ("Quels éléments doit contenir un profil qui convertit ?", M, ["Une promesse claire pour la cible", "Une preuve (chiffre, résultat)", "Un appel à l'action et un lien unique", "La liste de tous ses loisirs"], [0, 1, 2], "Le profil doit parler du bénéfice pour le visiteur.", "analyser"),
    ("Un créateur débute avec peu d'abonnés. Quelle routine accélère le plus sa visibilité au départ ?", U, ["Publier 5 fois par jour", "Commenter chaque jour avec valeur chez des comptes suivis par sa cible, en plus de publier", "Acheter de la publicité dès le premier jour", "Attendre que l'algorithme le découvre"], [1], "Les commentaires utiles exposent son expertise à une audience déjà constituée.", "évaluer"),
    ("Ses Reels humoristiques font beaucoup de vues mais aucun rendez-vous, ses carrousels méthode moins de vues mais la plupart des rendez-vous. Quelle décision est la plus pertinente ?", U, ["Ne faire que des Reels humoristiques", "Arrêter les réseaux", "Garder un peu d'humour pour attirer et renforcer les carrousels méthode avec un appel à l'action", "Supprimer les carrousels"], [2], "On optimise d'après les indicateurs business, pas seulement les vues.", "évaluer"),
    ("Dans une échelle d'offres, à quoi sert l'offre à petit prix ?", U, ["À remplacer l'offre principale", "À transformer un abonné en client et créer la confiance pour la suite", "À rien", "À baisser la valeur de la marque"], [1], "Le premier achat est le plus difficile ; un petit prix facilite ce passage.", "comprendre"),
    ("Quel message privé est le plus adapté après le commentaire « C'est exactement mon problème » ?", U, ["Voici le lien pour acheter ma formation à 690 €", "Merci pour ton commentaire ! Ça se passe comment pour toi en ce moment ?", "Abonne-toi à mon compte", "Tu devrais lire mes 50 derniers posts"], [1], "Commencer par une question ouvre la conversation et permet de comprendre le besoin.", "appliquer"),
    ("Quels éléments rendent une étude de cas convaincante ?", M, ["Un contexte proche de la cible", "Le problème initial", "La solution appliquée", "Un résultat chiffré"], [0, 1, 2, 3], "Les quatre éléments permettent au lecteur de se projeter.", "analyser"),
    ("Selon la formation, pourquoi la plupart des marques personnelles échouent-elles ?", U, ["Par manque de talent", "Par abandon faute de système et de rythme tenable", "À cause des algorithmes", "Parce qu'il est trop tard pour commencer"], [1], "Régularité, système de production et objectifs trimestriels permettent de durer.", "comprendre"),
], passing=75)

CAPSTONE = GenCapstone(
    title="Lancer sa marque personnelle en 30 jours",
    context_markdown="Vous allez appliquer l'ensemble de la formation à **votre propre marque**. À l'issue du projet, vous disposez d'un positionnement validé, d'un profil optimisé, d'un mois de contenus publiés, d'une première ressource gratuite et d'un parcours de vente prêt à fonctionner.\n\nSi vous n'avez pas encore d'activité, choisissez un projet réaliste que vous pourriez lancer, et construisez la marque autour de lui.",
    deliverables=[
        "Une fiche marque d'une page : positionnement, angle, persona, 3 valeurs, ton de voix",
        "Captures du profil optimisé (avant / après) sur le réseau principal",
        "Le calendrier éditorial de 30 jours et au moins 10 contenus publiés",
        "Un lead magnet et le plan de la séquence e-mail de 5 messages",
        "La fiche de l'offre principale",
        "Un bilan chiffré à J+30 avec 3 décisions pour le mois suivant",
    ],
    steps=[
        "Jours 1-3 : rédiger positionnement, histoire, valeurs et ton ; valider la phrase de positionnement auprès de 3 personnes de la cible",
        "Jours 4-6 : réaliser 3 entretiens d'audience et construire le persona et la banque d'idées (30 idées minimum)",
        "Jour 7 : optimiser le profil (photo, bio, bannière, lien, contenus épinglés)",
        "Jours 8-9 : définir les piliers et remplir le calendrier de 30 jours ; première session de batching",
        "Jours 10-30 : publier selon le calendrier et tenir la routine d'engagement de 20 minutes par jour",
        "Jours 15-20 : créer le lead magnet, la page d'inscription et la séquence e-mail",
        "Jours 20-25 : rédiger la fiche offre et proposer 2 collaborations",
        "Jour 30 : réaliser le bilan chiffré et fixer 3 décisions",
    ],
    rubric=[
        GenRubricCriterion(criterion="Positionnement", description="Public précis, résultat concret, angle différenciant, validé auprès de la cible", points=20),
        GenRubricCriterion(criterion="Connaissance de l'audience", description="Persona fondé sur de vrais verbatims, banque d'idées exploitable", points=15),
        GenRubricCriterion(criterion="Profil", description="Photo, promesse, preuve, appel à l'action et lien unique cohérents", points=10),
        GenRubricCriterion(criterion="Contenus", description="Équilibre attirer / nourrir / convertir, accroches travaillées, régularité tenue", points=25),
        GenRubricCriterion(criterion="Parcours de vente", description="Lead magnet lié à l'offre, séquence e-mail logique, offre claire et crédible", points=20),
        GenRubricCriterion(criterion="Analyse", description="Bilan chiffré honnête et décisions justifiées par les données", points=10),
    ],
    estimated_hours=25,
)

EXTRAS = GenCourseExtras(
    welcome_message_markdown="Bienvenue dans cette formation ! 🎉\n\nVous êtes ici parce que vous savez que votre expertise mérite d'être **vue, reconnue et choisie**. Dans les prochaines semaines, vous allez passer de « je publie de temps en temps sans vraiment savoir pourquoi » à une **marque personnelle claire, une audience qualifiée et des clients qui viennent à vous**.\n\nPas de recette miracle ici : une méthode, des exercices concrets et un projet final qui vous fait avancer pour de vrai.",
    how_to_follow_markdown="- **Rythme conseillé** : 2 à 3 leçons par semaine, soit environ 5 semaines, puis 30 jours pour le projet final.\n- **Faites les exercices** : c'est là que la marque se construit. Chaque exercice sert au projet final.\n- **Gardez un seul document** (Notion, Google Docs) où vous rassemblez vos exercices : ce sera votre « bible de marque ».\n- **Publiez dès le module 3**, même si ce n'est pas parfait : la pratique vaut plus que la préparation.\n- **Refaites l'exercice de la leçon 1.1** à la fin pour mesurer votre progression.",
    glossary=[
        GenGlossaryEntry(term="Marque personnelle", definition="Association durable entre votre nom, une promesse et un public précis."),
        GenGlossaryEntry(term="Positionnement", definition="Place que vous choisissez d'occuper dans l'esprit de votre cible : pour qui, quel résultat, comment."),
        GenGlossaryEntry(term="Niche", definition="Segment précis de marché sur lequel vous vous spécialisez."),
        GenGlossaryEntry(term="Persona", definition="Portrait détaillé et réaliste de votre client idéal."),
        GenGlossaryEntry(term="Verbatim", definition="Phrase exacte prononcée ou écrite par un membre de votre audience."),
        GenGlossaryEntry(term="Pilier de contenu", definition="Thématique récurrente de votre ligne éditoriale."),
        GenGlossaryEntry(term="Accroche (hook)", definition="Première ligne ou premières secondes d'un contenu, qui donnent envie de continuer."),
        GenGlossaryEntry(term="CTA (appel à l'action)", definition="Action précise demandée au lecteur à la fin d'un contenu."),
        GenGlossaryEntry(term="Carrousel", definition="Publication composée de plusieurs images ou diapositives à faire défiler."),
        GenGlossaryEntry(term="Batching", definition="Production de contenus par lots, en regroupant les tâches similaires."),
        GenGlossaryEntry(term="Taux d'interaction", definition="(Réactions + commentaires + partages + sauvegardes) ÷ vues × 100."),
        GenGlossaryEntry(term="Lead magnet", definition="Ressource gratuite offerte en échange d'une adresse e-mail."),
        GenGlossaryEntry(term="Séquence e-mail", definition="Série d'e-mails envoyés automatiquement après une inscription."),
        GenGlossaryEntry(term="Appel découverte", definition="Échange avec un prospect pour comprendre son besoin et vérifier que l'offre lui convient."),
        GenGlossaryEntry(term="Échelle d'offres", definition="Ensemble d'offres de valeur et de prix croissants, du gratuit au premium."),
        GenGlossaryEntry(term="Preuve sociale", definition="Témoignages, résultats et recommandations qui prouvent la valeur de votre travail."),
        GenGlossaryEntry(term="E-réputation", definition="Image de vous qui ressort des recherches et conversations en ligne."),
        GenGlossaryEntry(term="Canal possédé", definition="Canal que vous contrôlez (liste e-mail, site), indépendant des algorithmes."),
    ],
    faq=[
        GenExample(title="Faut-il beaucoup d'abonnés pour vendre ?", content_markdown="Non. Une audience **petite mais très ciblée** peut suffire à remplir un accompagnement. Ce qui compte : un positionnement clair, de la confiance et un parcours de vente."),
        GenExample(title="Je n'ose pas me montrer en vidéo. Est-ce bloquant ?", content_markdown="Non. Les posts texte, carrousels, newsletters et vidéos sans visage (écran, mains, voix off) fonctionnent. Commencez par ce qui vous met à l'aise, puis testez progressivement la vidéo."),
        GenExample(title="Combien de temps faut-il par semaine ?", content_markdown="Comptez 3 à 5 heures par semaine au démarrage avec la méthode de batching (création + engagement)."),
        GenExample(title="Au bout de combien de temps voit-on des résultats ?", content_markdown="Cela dépend de votre niche, de votre point de départ et de votre régularité. En général, les premiers signaux (interactions, messages) apparaissent en quelques semaines, et une marque solide se construit sur plusieurs mois de publication régulière."),
        GenExample(title="Et si je change de positionnement plus tard ?", content_markdown="C'est normal d'évoluer. Faites-le progressivement, en expliquant l'évolution à votre audience, plutôt que de repartir de zéro tous les mois."),
        GenExample(title="Faut-il être sur tous les réseaux ?", content_markdown="Non : un réseau principal, un secondaire et une liste e-mail. Dominez-en un avant d'en ouvrir d'autres."),
        GenExample(title="L'intelligence artificielle peut-elle écrire mes contenus ?", content_markdown="Elle peut aider à trouver des idées, structurer ou corriger. Mais votre histoire, vos exemples, vos convictions et votre ton sont ce qui fait votre marque : gardez-les au cœur de chaque contenu."),
    ],
    certification_criteria=[
        "Avoir suivi les 15 leçons",
        "Obtenir au moins 70 % à chacun des 5 quiz de module",
        "Obtenir au moins 75 % à l'examen final",
        "Remettre le projet final et obtenir au moins 60 / 100 selon la grille d'évaluation",
    ],
    conclusion_markdown="Félicitations ! Vous avez maintenant tout ce qu'il faut pour construire une marque personnelle qui attire et qui vend : un positionnement clair, une connaissance fine de votre audience, un système de création de contenu, des leviers de croissance et un parcours de vente.\n\n**Prochaines étapes** :\n1. Terminez votre projet de 30 jours.\n2. Faites votre bilan mensuel chaque mois.\n3. Révisez votre feuille de route chaque trimestre.\n\nLa différence entre ceux qui réussissent et les autres n'est pas le talent : c'est **la régularité**. À vous de jouer !",
    marketing_pitch="Vous avez l'expertise, mais personne ne le sait encore ? Cette formation vous guide pas à pas pour construire une marque personnelle claire, créer des contenus qui marquent, faire grandir une audience qualifiée et transformer votre image en clients, avec une méthode concrète, des exercices corrigés et un plan d'action de 30 jours.",
    sales_page_bullets=[
        "Trouvez un positionnement qui vous rend unique et mémorable",
        "Découvrez exactement ce que votre audience veut lire et acheter",
        "Écrivez des accroches et des contenus qui arrêtent le défilement",
        "Produisez un mois de contenus en quelques heures grâce au batching",
        "Faites grandir votre audience avec l'engagement et les collaborations",
        "Construisez une offre à forte valeur perçue et un parcours de vente",
        "Vendez en message privé sans forcer ni spammer",
        "Repartez avec votre marque lancée grâce au projet de 30 jours",
    ],
)

MODULES = [
    Module(title="Les fondations de sa marque personnelle", summary="Comprendre ce qu'est une marque personnelle, trouver son positionnement unique et construire son histoire et son identité.", objectives=["Définir sa marque personnelle", "Rédiger son positionnement", "Construire son récit et son identité"], lessons=[L1_1, L1_2, L1_3], quiz=Q1),
    Module(title="Connaître son audience", summary="Construire son persona, récolter les vrais mots de sa cible et choisir les bonnes plateformes.", objectives=["Construire un persona fondé sur des faits", "Collecter des verbatims", "Choisir ses réseaux"], lessons=[L2_1, L2_2, L2_3], quiz=Q2),
    Module(title="Créer du contenu qui marque", summary="Définir sa ligne éditoriale, écrire des contenus qui retiennent et produire efficacement.", objectives=["Construire un calendrier éditorial équilibré", "Rédiger accroches et CTA", "Mettre en place un système de production"], lessons=[L3_1, L3_2, L3_3], quiz=Q3),
    Module(title="Exploser sur les réseaux", summary="Comprendre les algorithmes, optimiser son profil, activer les leviers de croissance et piloter par les chiffres.", objectives=["Optimiser son profil", "Accélérer sa croissance", "Mesurer et ajuster"], lessons=[L4_1, L4_2, L4_3], quiz=Q4),
    Module(title="Vendre grâce à son image", summary="Construire son offre, transformer son audience en clients et installer sa réputation dans la durée.", objectives=["Créer une offre à forte valeur perçue", "Mettre en place un parcours de vente", "Utiliser la preuve sociale et durer"], lessons=[L5_1, L5_2, L5_3], quiz=Q5),
]

COURSE = Course(
    brief=CourseBrief(
        topic="Personal branding : créer sa marque personnelle, créer du contenu, exploser sur les réseaux, connaître son audience et vendre grâce à son image",
        audience="Entrepreneurs, freelances, indépendants et créateurs",
        level="débutant",
        duration_hours=8,
        modules_count=5,
        lessons_per_module=3,
        tone="concret, motivant et direct",
    ),
    status=CourseStatus.ready,
    title="Personal Branding : de l'invisible à la référence",
    subtitle="Construisez votre marque, faites grandir votre audience et vendez grâce à votre image",
    description="Une formation complète et pratique pour construire une marque personnelle forte : trouver son positionnement, connaître son audience, créer des contenus qui marquent, grandir sur les réseaux sociaux et transformer son image en clients. Chaque leçon se termine par un exercice corrigé, chaque module par un quiz, et la formation par un projet de lancement en 30 jours.",
    target_audience="Entrepreneurs, freelances, indépendants, consultants et créateurs qui veulent se faire connaître et vendre grâce à leur image",
    prerequisites=["Avoir une activité, une expertise ou un projet à faire connaître", "Avoir un compte sur au moins un réseau social", "Aucune compétence technique ou marketing requise"],
    learning_outcomes=[
        "Formuler un positionnement clair et différenciant",
        "Construire un persona fondé sur les vrais mots de son audience",
        "Planifier et produire un mois de contenus équilibrés",
        "Rédiger des accroches et des appels à l'action efficaces",
        "Optimiser son profil et activer les leviers de croissance",
        "Analyser ses statistiques et ajuster sa stratégie",
        "Construire une offre et un parcours qui transforment l'audience en clients",
    ],
    skills=["Positionnement", "Storytelling", "Stratégie éditoriale", "Copywriting", "Croissance sur les réseaux", "Analyse de données", "Vente"],
    pedagogical_approach="Chaque leçon combine explications, exemples réels, points clés et un exercice pratique corrigé. Les exercices s'enchaînent pour construire votre propre marque pas à pas, jusqu'au projet final de 30 jours.",
    modules=MODULES,
    final_exam=EXAM,
    capstone=CAPSTONE,
    extras=EXTRAS,
)

if __name__ == "__main__":
    out = Path(__file__).parent
    (out / "personal-branding.json").write_text(COURSE.model_dump_json(indent=2), encoding="utf-8")
    (out / "personal-branding.html").write_text(to_html(COURSE), encoding="utf-8")
    print(f"{COURSE.title} : {len(COURSE.modules)} modules, {COURSE.lessons_count} leçons, {COURSE.total_minutes} min → {slugify(COURSE.title)}")
