import json, sys
i, val = int(sys.argv[1]), sys.argv[2].lower() in ("o", "oui", "true")
p = "gold_set.json"
gold = json.load(open(p, encoding="utf-8"))
print("Avant :", gold[i]["humain"], "|", gold[i]["prompt"])
gold[i]["humain"] = val
json.dump(gold, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("Après :", val)