import json, sys
cle = sys.argv[1] if len(sys.argv) > 1 else "regex"
gold = json.load(open("gold_set.json", encoding="utf-8"))
for i, g in enumerate(gold):
    if g.get(cle) != g["humain"]:
        print(f"=== #{i} | {g['categorie']} | {cle}={g.get(cle)} | toi={g['humain']}")
        print("Q :", g["prompt"])
        print("R :", g["reponse"])
        if cle == "juge":
            print("Raison du juge :", g.get("juge_raison"))
        print()