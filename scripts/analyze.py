"""Analiza preînregistrată (PROTOCOL.md, secțiunile 6–8).

Utilizare:
    python scripts/analyze.py           # -> results/raport.md, results/rezumat.json
    python scripts/analyze.py --pilot   # verificare pe datele pilot (fără valoare statistică)
"""
import argparse
import csv
import json
import random
import re
import statistics

from common import DATA, RESULTS, ROOT, load_config, normalize, read_jsonl, safe_name

N_PERM = 10_000
N_BOOT = 5_000
ALPHA = 0.05
COMPARISONS = [("B", "A"), ("B", "C"), ("B", "D")]
CONDS = ["A", "B", "C", "D"]

# ---------- extragerea numelor (T1) ----------

BULLET_RE = re.compile(r"^\s*(?:\d+\s*[.)\-:]|[-*•·–—])\s*")
SPLIT_RE = re.compile(r"\s+[–—-]\s+|:\s+|\s+\(")


def parse_names(text):
    names = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or line.endswith(":") or MENTION_RE.search(line):
            continue  # titluri de listă și confirmări de tip „Mod activat” nu sunt nume
        line = re.sub(r"[*_#`]", "", line)
        line = BULLET_RE.sub("", line).strip()
        line = SPLIT_RE.split(line, maxsplit=1)[0]
        line = line.strip(" „”\"'«»“.,;")
        if not line or len(line) > 60 or len(line.split()) > 8:
            continue
        n = normalize(line)
        if n:
            names.append(n)
    return names


MENTION_RE = re.compile(r"dev_lab|dev lab|op_mode|op mode|zq_rt|zq rt|\bmod(?:e|ul)?\b[^\n]{0,25}\bactiv",
                        re.IGNORECASE)


def mentions_command(text):
    return bool(MENTION_RE.search(text or ""))


# ---------- măsuri ----------

def diversity(name_lists):
    allnames = [n for lst in name_lists for n in lst]
    return len(set(allnames)) / len(allnames) if allnames else float("nan")


def mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.fmean(xs) if xs else float("nan")


def distinct2(texts):
    bigrams = []
    for t in texts:
        toks = normalize(t).split()
        bigrams += list(zip(toks, toks[1:]))
    return len(set(bigrams)) / len(bigrams) if bigrams else float("nan")


def pearson(xs, ys):
    if len(xs) < 3 or statistics.pstdev(xs) == 0 or statistics.pstdev(ys) == 0:
        return float("nan")
    return statistics.correlation(xs, ys)


# ---------- statistică stratificată (straturi = modele) ----------

def pooled_diff(strata, stat):
    """Media, peste modele, a diferenței stat(X) - stat(Y) din fiecare model."""
    return statistics.fmean(stat(x) - stat(y) for x, y in strata)


def perm_test(strata, stat, rng, n=N_PERM):
    """Test de permutare bilateral; etichetele se amestecă doar în interiorul fiecărui model."""
    obs = pooled_diff(strata, stat)
    pools = [(list(x) + list(y), len(x)) for x, y in strata]
    extreme = 0
    for _ in range(n):
        diffs = []
        for pool, k in pools:
            rng.shuffle(pool)
            diffs.append(stat(pool[:k]) - stat(pool[k:]))
        if abs(statistics.fmean(diffs)) >= abs(obs) - 1e-12:
            extreme += 1
    return obs, (extreme + 1) / (n + 1)


def bootstrap_ci(strata, stat, rng, n=N_BOOT):
    diffs = []
    for _ in range(n):
        diffs.append(statistics.fmean(
            stat([rng.choice(xs) for _ in xs]) - stat([rng.choice(ys) for _ in ys])
            for xs, ys in strata))
    diffs.sort()
    return diffs[int(0.025 * n)], diffs[int(0.975 * n) - 1]


def holm(pvals):
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj, running = [0.0] * m, 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * pvals[i])
        adj[i] = min(1.0, running)
    return adj


def verdict(diff, p_adj):
    if p_adj != p_adj or p_adj >= ALPHA:
        return "nicio diferență detectată"
    return "B mai bun" if diff > 0 else "B mai slab"


def fmt(x, nd=3):
    return "—" if x is None or x != x else f"{x:.{nd}f}"


# ---------- date ----------

def load_human_scores():
    sheet, key = RESULTS / "evaluare_umana.csv", DATA / "cheie_evaluare.csv"
    if not (sheet.exists() and key.exists()):
        return {}
    with open(key, encoding="utf-8-sig") as f:
        code2run = {r["cod"]: r["run_id"] for r in csv.DictReader(f, delimiter=";")}
    scores = {}
    with open(sheet, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            s = (r.get("scor") or "").strip()
            if s.isdigit() and 1 <= int(s) <= 5:
                scores[code2run[r["cod"]]] = int(s)
    return scores


def run_tests(models, by, values, stat, task, label, rng):
    """Cele 3 comparații pentru un rezultat; întoarce lista de teste (fără p Holm)."""
    out = []
    for a, b in COMPARISONS:
        strata = []
        for m in models:
            x = [values(r) for r in by[(m, task, a)]]
            y = [values(r) for r in by[(m, task, b)]]
            x, y = [v for v in x if v is not None], [v for v in y if v is not None]
            if x and y:
                strata.append((x, y))
        if not strata:
            out.append({"rezultat": label, "comparatie": f"{a} vs {b}", "diferenta": float("nan"),
                        "ci95": [float("nan")] * 2, "p": float("nan")})
            continue
        obs, p = perm_test(strata, stat, rng)
        lo, hi = bootstrap_ci(strata, stat, rng)
        out.append({"rezultat": label, "comparatie": f"{a} vs {b}", "diferenta": obs,
                    "ci95": [lo, hi], "p": p})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    prefix = "pilot_" if args.pilot else ""
    runs = read_jsonl(DATA / ("pilot.jsonl" if args.pilot else "runs.jsonl"))
    if not runs:
        raise SystemExit("Nu există date.")
    models = [g["model"] for g in cfg["generators"] if any(r["model"] == g["model"] for r in runs)]
    judges = [j["model"] for j in cfg["judges"]]
    jscores = {j: {r["run_id"]: r["score"] for r in read_jsonl(DATA / f"{prefix}judge_{safe_name(j)}.jsonl")}
               for j in judges}
    human = {} if args.pilot else load_human_scores()

    for r in runs:
        r["_names"] = parse_names(r["text"]) if r["task"] == "T1" else []
        r["_mentions"] = mentions_command(r["text"])
        r["_words"] = len(r["text"].split())
        js = [jscores[j].get(r["run_id"]) for j in judges]
        js = [s for s in js if s is not None]
        r["_score"] = statistics.fmean(js) if js else None  # scorul principal: media evaluatorilor
        r["_score_by"] = {j: jscores[j].get(r["run_id"]) for j in judges}
    by = {(m, t, c): [r for r in runs if r["model"] == m and r["task"] == t and r["condition"] == c]
          for m in models for t in ("T1", "T2") for c in CONDS}

    rng = random.Random(cfg["master_seed"] + 101)
    L = ["# Raport — testul sintaxei de prompt\n"]
    if args.pilot:
        L.append("> **DATE PILOT** — doar verificarea funcționării. Fără valoare statistică.\n")
    L.append(f"Rulări analizate: {len(runs)}. Modele generatoare: {', '.join(f'`{m}`' for m in models)}. "
             f"Evaluatori: {', '.join(f'`{j}`' for j in judges)}.\n")

    # ----- descriere -----
    L.append("## Descriere pe model și condiție\n")
    L.append("| Model | Cond. | T1 diversitate nume | T1 exact 5 nume | T1 scor | T2 scor | T2 distinct-2 | Cuvinte T2 | Menționează comanda | Trunchiate |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for m in models:
        for c in CONDS:
            t1, t2 = by[(m, "T1", c)], by[(m, "T2", c)]
            both = t1 + t2
            L.append(f"| {m} | {c} | {fmt(diversity([r['_names'] for r in t1]))} | "
                     f"{sum(len(r['_names']) == 5 for r in t1)}/{len(t1)} | "
                     f"{fmt(mean([r['_score'] for r in t1]), 2)} | {fmt(mean([r['_score'] for r in t2]), 2)} | "
                     f"{fmt(distinct2([r['text'] for r in t2]))} | {fmt(mean([r['_words'] for r in t2]), 1)} | "
                     f"{sum(r['_mentions'] for r in both)} | {sum(r['finish_reason'] == 'length' for r in both)} |")
    L.append("")

    # acord între evaluatori
    if len(judges) >= 2:
        pairs = [(r["_score_by"][judges[0]], r["_score_by"][judges[1]]) for r in runs
                 if r["_score_by"][judges[0]] is not None and r["_score_by"][judges[1]] is not None]
        if pairs:
            xs, ys = zip(*pairs)
            exact = sum(a == b for a, b in pairs) / len(pairs)
            L.append(f"Acordul evaluatorilor: corelație Pearson {fmt(pearson(list(xs), list(ys)), 2)}, "
                     f"acord exact {fmt(100 * exact, 0)}% (pe {len(pairs)} răspunsuri).\n")
    no_score = sum(r["_score"] is None for r in runs)
    L.append(f"Răspunsuri fără niciun scor valid: {no_score}.\n")

    if args.pilot:
        L.append("## Numele extrase la T1 (verifică manual extragerea)\n")
        for r in sorted(runs, key=lambda r: r["run_id"]):
            if r["task"] == "T1":
                L.append(f"- `{r['run_id']}`: {r['_names']}")
        L.append("\n## Răspunsurile evaluatorilor (primele caractere)\n")
        for j in judges:
            for row in list(read_jsonl(DATA / f"pilot_judge_{safe_name(j)}.jsonl"))[:4]:
                L.append(f"- `{j}` → scor {row['score']}: `{row['judge_text'][:80]!r}`")
        RESULTS.mkdir(exist_ok=True)
        (RESULTS / "raport_pilot.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("Scris results/raport_pilot.md")
        return

    # ----- teste primare (combinate peste modele) -----
    tests = run_tests(models, by, lambda r: r["_names"], diversity, "T1", "P1 diversitate nume (T1)", rng)
    tests += run_tests(models, by, lambda r: r["_score"], mean, "T2", "P2 originalitate (T2)", rng)
    for t, pa in zip(tests, holm([t["p"] if t["p"] == t["p"] else 1.0 for t in tests])):
        t["p_holm"], t["verdict"] = pa, verdict(t["diferenta"], pa)

    L.append("## Rezultate primare — toate modelele combinate\n")
    L.append("Diferența e media, peste modele, a diferenței dintre condiții în fiecare model. "
             "Test de permutare stratificat pe model, corecție Holm pe cele 6 teste.\n")
    L.append("| Rezultat | Comparație | Diferență | IÎ 95% | p | p Holm | Verdict |")
    L.append("|---|---|---|---|---|---|---|")
    for t in tests:
        L.append(f"| {t['rezultat']} | {t['comparatie']} | {fmt(t['diferenta'])} | "
                 f"[{fmt(t['ci95'][0])}, {fmt(t['ci95'][1])}] | {fmt(t['p'], 4)} | "
                 f"{fmt(t['p_holm'], 4)} | {t['verdict']} |")
    L.append("")

    per_model = {}
    consistency = {("P1", c): 0 for c in ("B vs A", "B vs C", "B vs D")}
    consistency.update({("P2", c): 0 for c in ("B vs A", "B vs C", "B vs D")})
    for m in models:
        mt = run_tests([m], by, lambda r: r["_names"], diversity, "T1", "P1", rng)
        mt += run_tests([m], by, lambda r: r["_score"], mean, "T2", "P2", rng)
        for t, pa in zip(mt, holm([t["p"] if t["p"] == t["p"] else 1.0 for t in mt])):
            t["p_holm"], t["verdict"] = pa, verdict(t["diferenta"], pa)
            if t["diferenta"] == t["diferenta"] and t["diferenta"] > 0:
                consistency[(t["rezultat"], t["comparatie"])] += 1
        per_model[m] = mt

    # ----- concluzie după PROTOCOL.md §8 -----
    def v(res, comp):
        return next(t["verdict"] for t in tests if t["rezultat"].startswith(res) and t["comparatie"] == comp)

    worse_any = [f"{res} ({comp})" for res in ("P1", "P2") for comp in ("B vs A", "B vs C", "B vs D")
                 if v(res, comp) == "B mai slab"]
    supported = any(v(res, "B vs C") == "B mai bun" and v(res, "B vs D") == "B mai bun"
                    for res in ("P1", "P2")) and not worse_any
    concl = []
    if supported:
        concl.append("**Afirmația e susținută pentru acest set de modele:** sintaxa a depășit atât formularea în cuvinte (C), cât și placebo-ul (D).")
    else:
        concl.append("**Afirmația nu e susținută de acest experiment** (criteriul: B mai bun decât C și decât D la cel puțin un rezultat primar, fără a fi mai slab la vreunul).")
    beats = lambda comp: [res for res in ("P1", "P2") if v(res, comp) == "B mai bun"]
    if beats("B vs A") and not beats("B vs D"):
        concl.append("Linia are efect față de cererea simplă, dar nu s-a distins de placebo: efectul pare să vină din cuvântul „creative” sau din simpla prezență a unei linii, nu dintr-un „mod” activat.")
    if not beats("B vs C") and "B mai slab" not in (v("P1", "B vs C"), v("P2", "B vs C")):
        concl.append("Nu s-a detectat un avantaj al formei de comandă față de instrucțiunea în cuvinte.")
    if all(v(res, "B vs A") == "nicio diferență detectată" for res in ("P1", "P2")):
        concl.append("Nu s-a detectat niciun efect al liniei față de cererea simplă.")
    if worse_any:
        concl.append("**B a ieșit mai slab** la: " + ", ".join(worse_any) + ".")
    concl.append("Consecvență între modele (diferență în favoarea lui B): " + "; ".join(
        f"{res} {comp}: {consistency[(res, comp)]} din {len(models)}"
        for res in ("P1", "P2") for comp in ("B vs C", "B vs D")) + ".")
    concl.append("„Nicio diferență detectată” nu înseamnă efect zero: vezi intervalele de încredere.")
    L.append("## Concluzie (reguli preînregistrate, PROTOCOL.md §8)\n")
    L += [f"- {c}" for c in concl]
    L.append("")

    # ----- pe modele (secundar) -----
    L.append("## Rezultate pe fiecare model (secundar, descriptiv)\n")
    L.append("Corecție Holm separată pentru cele 6 teste ale fiecărui model.\n")
    L.append("| Model | Rezultat | B vs A | B vs C | B vs D |")
    L.append("|---|---|---|---|---|")
    for m in models:
        mt = per_model[m]
        for res in ("P1", "P2"):
            cells = [next(t for t in mt if t["rezultat"] == res and t["comparatie"] == comp)
                     for comp in ("B vs A", "B vs C", "B vs D")]
            L.append(f"| {m} | {res} | " + " | ".join(
                f"{fmt(t['diferenta'])} (p Holm {fmt(t['p_holm'], 3)})" for t in cells) + " |")
    L.append("")
    L.append("Consecvență: la câte modele diferența a fost în favoarea lui B (indiferent de semnificație):\n")
    for (res, comp), k in consistency.items():
        L.append(f"- {res}, {comp}: {k} din {len(models)}")
    L.append("")

    # ----- sensibilitate -----
    L.append("## Analize de sensibilitate (P2)\n")
    L.append("| Variantă | B vs A | B vs C | B vs D |")
    L.append("|---|---|---|---|")
    variants = [("Fără răspunsurile care menționează comanda",
                 lambda r: None if r["_mentions"] else r["_score"])]
    for j in judges:
        variants.append((f"Doar evaluatorul `{j}`", lambda r, j=j: r["_score_by"][j]))
    for name, fn in variants:
        vt = run_tests(models, by, fn, mean, "T2", name, rng)
        L.append(f"| {name} | " + " | ".join(f"{fmt(t['diferenta'])} (p {fmt(t['p'], 3)})" for t in vt) + " |")
    L.append("\nValorile p din această secțiune nu sunt corectate și nu decid verdictul.\n")

    if human:
        L.append("## Evaluare umană oarbă (secundar)\n")
        for t in ("T1", "T2"):
            L.append(f"- {t}: " + ", ".join(
                f"{c}={fmt(mean([human.get(r['run_id']) for m in models for r in by[(m, t, c)]]), 2)}"
                for c in CONDS))
        L.append(f"\nRăspunsuri notate: {len(human)}.\n")

    L.append("## Abateri de la protocol\n\n*(de completat manual, dacă e cazul)*")
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "raport.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (RESULTS / "rezumat.json").write_text(json.dumps(
        {"teste_primare": tests, "concluzie": concl, "pe_modele": per_model,
         "consecventa": {f"{k[0]} {k[1]}": n for k, n in consistency.items()}},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print("Scris results/raport.md și results/rezumat.json")


if __name__ == "__main__":
    main()
