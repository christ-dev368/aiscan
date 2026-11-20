\## Regex V1 (jeu corrigé)

n = \_78\_ | VP = \_23\_ FP = \_0\_ FN = \_4\_ VN = \_51\_

Précision : \_100\_%  Rappel : \_85\_%  Exactitude : \_95\_%

\## Juge 3B

n = \_78\_ | VP = \_21\_ FP = \_24\_ FN = \_6\_ VN = \_27\_

Précision : \_47\_%  Rappel : \_78\_%  Exactitude : \_62\_%



/\*Étape 7 (optionnelle) : un juge plus gros

copy gold\_set.json gold\_set\_juge3b.json

ollama pull qwen2.5:7b (plusieurs Go de téléchargement)

python juge.py --model qwen2.5:7b --refaire

python evaluer.py gold\_set.json juge, puis ajoute une ligne « Juge 7B » à ton tableau.

Pour revenir au 3B : copy gold\_set\_juge3b.json gold\_set.json.



Sur 8 Go de RAM, ce sera lent et juste. Si ça ne passe pas, note-le comme limite matérielle.

\*/



