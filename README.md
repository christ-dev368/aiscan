# aiscan : prototype V1 (scanner de chatbots)

Mini-démo locale : un faux chatbot volontairement vulnérable + un scanner qui l'attaque et génère un rapport.
Aucune dépendance : Python 3.8+ suffit, aucune clé d'API.

## Lancer la démo (2 terminaux)

Terminal 1 : le faux chatbot
    python fakebot.py --seed 42

Terminal 2 : le scanner
    python aiscan.py --cible http://localhost:8000/chat --repeat 5

Résultat : un tableau dans le terminal, `rapport_AAAA-MM-JJ.html` (preuves + correctifs)
et `resultats_AAAA-MM-JJ.json` (format de faille commun). Retire `--seed` pour voir les taux varier.

## Fichiers
- `fakebot.py`   : serveur HTTP local, cède aux attaques avec une probabilité (simule un LLM non déterministe)
- `attacks.json` : bibliothèque d'attaques (catégorie, prompts, motifs de détection, conseils)
- `aiscan.py`    : scanner, scoring, rapport HTML

## Limites (c'est un prototype)
- Le chatbot est simulé : les vrais LLM se comportent différemment.
- La détection repose sur des canary tokens et des motifs, sans juge LLM.
- Le scanner refuse toute cible hors `localhost` : ne l'utilise que sur des cibles autorisées.
