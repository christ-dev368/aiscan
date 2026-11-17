#!/usr/bin/env python3
"""evaluer.py : compare le détecteur du scanner à TES verdicts (gold_set.json).

Usage : python evaluer.py [gold_set.json] [methode]     (methode : regex par défaut, plus tard : juge)
"""
import json, sys
from collections import defaultdict
from pathlib import Path

def matrice(items, cle):
    vp = sum(1 for g in items if g[cle] and g["humain"])          # vrai positif : scanner OUI, toi OUI
    fp = sum(1 for g in items if g[cle] and not g["humain"])      # faux positif : scanner OUI, toi NON
    fn = sum(1 for g in items if not g[cle] and g["humain"])      # faux négatif : scanner NON, toi OUI
    vn = sum(1 for g in items if not g[cle] and not g["humain"])  # vrai négatif : scanner NON, toi NON
    return vp, fp, fn, vn

def pct(a, b):
    return f"{a / b:.0%}" if b else "n/a"

def ligne(titre, items, cle):
    vp, fp, fn, vn = matrice(items, cle)
    print(f"{titre:<30} n={len(items):<3} VP={vp:<3} FP={fp:<3} FN={fn:<3} VN={vn:<3} "
          f"précision={pct(vp, vp + fp):<5} rappel={pct(vp, vp + fn):<5} exactitude={pct(vp + vn, len(items))}")

def main():
    chemin = Path(sys.argv[1] if len(sys.argv) > 1 else "gold_set.json")
    cle = sys.argv[2] if len(sys.argv) > 2 else "regex"
    gold = json.loads(chemin.read_text(encoding="utf-8"))
    print(f"Méthode évaluée : {cle} | {len(gold)} échanges étiquetés | tes 'oui' : {sum(g['humain'] for g in gold)}\n")
    ligne("TOTAL", gold, cle)
    print("-" * 100)
    par_cat = defaultdict(list)
    for g in gold:
        par_cat[g["categorie"]].append(g)
    for cat, items in par_cat.items():
        ligne(cat, items, cle)
    erreurs = [g for g in gold if g[cle] != g["humain"]]
    print(f"\n{len(erreurs)} désaccord(s) entre la méthode et toi (à relire) :")
    for g in erreurs:
        genre = "FAUX POSITIF" if g[cle] else "FAUX NÉGATIF"
        print(f"\n[{genre}] {g['categorie']}\n  Q : {g['prompt']}\n  R : {g['reponse'][:300]}")

main()
