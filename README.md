# \# aiscan : *scanner de chatbots* (prototype)

# 

###### Un scanner qui attaque un chatbot (injection de prompt, extraction du prompt système, fuite de données, jailbreak, sorties hors périmètre), prouve les fuites avec des canary tokens, puis génère un rapport avec des conseils de défense.

###### 

###### Il fonctionne sur un faux chatbot simulé, et sur un vrai modèle local (Ollama). Le détecteur est mesuré contre un jeu de référence étiqueté à la main.



###### **Aucune dépendance externe pour le scanner : Python 3.8+ suffit.**

# 

## \## Lancer la démo avec le faux chatbot (2 terminaux)

###### 

##### Terminal 1 : le faux chatbot



##### &#x20;   python fakebot.py --seed 42



##### Terminal 2 : le scanner



##### &#x20;   python aiscan.py --cible http://localhost:8000/chat --repeat 5



###### Résultat : un tableau dans le terminal, `rapport\_AAAA-MM-JJ.html` (preuves et correctifs) et `resultats\_AAAA-MM-JJ.json`.

# 

## \## Lancer le scan sur un vrai modèle local

## 

##### Prérequis : \[Ollama](https://ollama.com) installé, puis `ollama pull llama3.2:3b`.

##### 

##### Terminal 1 : le chatbot branché sur le modèle



##### &#x20;   python llmbot.py --model llama3.2:3b



##### Terminal 2 : le scanner



##### &#x20;   python aiscan.py --cible http://localhost:8000/chat --repeat 5

##### 

###### Le prompt système de `llmbot.py` est volontairement fragile et contient des secrets fictifs (canary) pour pouvoir prouver une quelconque fuite.

###### 

## \## Mesurer la qualité du détecteur

##### 

###### 1\. `python etiqueter.py echanges\_AAAA-MM-JJ.json` : tu lis chaque échange et tu donnes ton verdict (oui/non). Le verdict du scanner est masqué pour ne pas t'influencer. Le résultat est enregistré dans `gold\_set.json`.

###### 2\. `python evaluer.py gold\_set.json regex` : compare le détecteur par motifs à tes verdicts (précision, rappel, exactitude, liste des désaccords).

###### 3\. (À ajouter une fois fait) `python juge.py` puis `python evaluer.py gold\_set.json juge` : même mesure pour un juge LLM local.

###### 

## \## Fichiers



###### \- `fakebot.py` : faux chatbot vulnérable, cède avec une probabilité (simule un LLM non déterministe)

###### \- `llmbot.py` : même interface, mais avec un vrai modèle via Ollama

###### \- `attacks.json` : bibliothèque d'attaques (catégorie, prompts, motifs de détection, conseils)

###### \- `aiscan.py` : scanner, rapport HTML

###### \- `etiqueter.py` : étiquetage à la main des échanges

###### \- `evaluer.py` : évaluation d'une méthode de détection contre `gold\_set.json`

###### \- `juge.py` : juge LLM local

###### \- `gold\_set.json` : jeu de référence (secrets fictifs uniquement)

###### 

## \## Résultats actuels (détecteur par motifs)

##### 

###### Jeu de référence : 78 échanges étiquetés à la main, dont 27 attaques réussies.



##### &#x20;     TABLEAU

##### \---------------------

##### | Mesure | Résultat |

##### |--------|----------|

##### |Précision| 100 % (0 fausse alerte) |

##### | Rappel  | 85 % (23 fuites trouvées sur 27) |

##### |Exactitude| 95 % |

###### 

###### Les 4 fuites ratées sont des fuites partielles ou reformulées : le modèle refuse mais reprend le contenu de ses consignes, ou cite un fragment d'un secret. Les motifs ne cherchent que les canary exacts, c'est la raison d'être du juge LLM.

###### 

## \## Limites

###### 

###### \- Échantillon petit : 78 échanges, dont 2 seulement en jailbreak. Quelques cas suffisent à faire bouger les pourcentages.

###### \- Un seul étiqueteur : les cas limites (refus qui en dit trop) dépendent de ma règle d'étiquetage.

###### \- Le modèle testé est petit (llama3.2:3b) et les secrets sont fictifs : les résultats ne se transposent pas tels quels à un vrai système.

###### \- Les regex n'ont pas été modifiées pour améliorer ce score : il sert de référence.

###### \- Le scanner refuse toute cible hors `localhost` : n'utilise cet outil que sur des cibles dont on a l'autorisation.

###### 

## \## Références

## 

##### \- OWASP Top 10 for LLM Applications : LLM01 (injection de prompt), LLM02 (divulgation d'informations sensibles), LLM07 (fuite du prompt système), LLM09 (sorties hors cadre).

