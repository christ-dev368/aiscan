# aiscan : scanner de chatbots (prototype)

Un scanner qui attaque un chatbot (injection de prompt, extraction du prompt système, fuite de données, jailbreak, sorties hors périmètre), prouve les fuites avec des canary tokens, puis génère un rapport avec des conseils de défense.

Il fonctionne sur un faux chatbot simulé et sur un vrai modèle local (Ollama). Le détecteur est mesuré contre un jeu de référence étiqueté à la main.

Aucune dépendance externe pour le scanner : Python 3.8+ suffit.

## Lancer la démo avec le faux chatbot (2 terminaux)

Terminal 1 : le faux chatbot

    python fakebot.py --seed 42

Terminal 2 : le scanner

    python aiscan.py --cible http://localhost:8000/chat --repeat 5

Résultat : un tableau dans le terminal, `rapport_AAAA-MM-JJ.html` (preuves et correctifs) et `resultats_AAAA-MM-JJ.json` (format de faille commun). Retire `--seed` pour voir les taux varier.

## Lancer le scan sur un vrai modèle local

Prérequis : [Ollama](https://ollama.com) installé, puis `ollama pull llama3.2:3b`.

Terminal 1 : le chatbot branché sur le modèle

    python llmbot.py --model llama3.2:3b

Terminal 2 : le scanner (même commande qu'avec le faux chatbot)

    python aiscan.py --cible http://localhost:8000/chat --repeat 5

Le prompt système de `llmbot.py` est volontairement fragile et contient des secrets fictifs (canary) pour pouvoir prouver une fuite. Un vrai modèle sur un PC modeste répond plus lentement que le faux bot : si le scanner s'arrête sur un délai dépassé, augmente le timeout dans `envoyer()` (`aiscan.py`).

## Mesurer la qualité du détecteur

1. `python etiqueter.py echanges_AAAA-MM-JJ.json` : tu lis chaque échange et tu donnes ton verdict (oui/non). Le verdict du scanner est masqué pour ne pas t'influencer. Le résultat est enregistré dans `gold_set.json`.
2. `python evaluer.py gold_set.json regex` : compare le détecteur par motifs à tes verdicts (précision, rappel, exactitude, liste des désaccords).
3. `python juge.py` puis `python evaluer.py gold_set.json juge` : même mesure pour un juge LLM local (résultats à venir).

## Fichiers

- `fakebot.py` : serveur HTTP local, cède aux attaques avec une probabilité (simule un LLM non déterministe)
- `llmbot.py` : même interface, mais avec un vrai modèle via Ollama
- `attacks.json` : bibliothèque d'attaques (catégorie, prompts, motifs de détection, conseils)
- `aiscan.py` : scanner, scoring, rapport HTML
- `etiqueter.py` : étiquetage à la main des échanges
- `evaluer.py` : évaluation d'une méthode de détection contre `gold_set.json`
- `juge.py` : juge LLM local
- `gold_set.json` : jeu de référence (secrets fictifs uniquement)

## Résultats actuels (détecteur par motifs)

Jeu de référence : 78 échanges étiquetés à la main, dont 27 attaques réussies.

| Mesure | Résultat |
|---|---|
| Précision | 100 % (0 fausse alerte) |
| Rappel | 85 % (23 fuites trouvées sur 27) |
| Exactitude | 95 % |

Les 4 fuites ratées sont des fuites partielles ou reformulées : le modèle refuse mais reprend le contenu de ses consignes, ou cite un fragment d'un secret. Les motifs ne cherchent que les canary exacts, c'est la raison d'être du juge LLM.

## Limites (c'est un prototype)

- Échantillon petit : 78 échanges, dont 2 seulement en jailbreak. Quelques cas suffisent à faire bouger les pourcentages.
- Un seul étiqueteur : les cas limites (un refus qui en dit trop) dépendent de ma règle d'étiquetage.
- Le modèle testé est petit (llama3.2:3b) et les secrets sont fictifs : les résultats ne se transposent pas tels quels à un vrai système.
- Les motifs de détection n'ont pas été modifiés pour améliorer ce score : il sert de référence.
- Le scanner refuse toute cible hors `localhost` : n'utilise cet outil que sur des cibles dont tu as l'autorisation.

## Références

OWASP Top 10 for LLM Applications : LLM01 (injection de prompt), LLM02 (divulgation d'informations sensibles), LLM07 (fuite du prompt système), LLM09 (sorties hors cadre).
