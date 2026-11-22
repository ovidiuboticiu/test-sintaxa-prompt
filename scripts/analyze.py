"""Analiza preînregistrată (PROTOCOL.md, secțiunile 6–8).

Utilizare:
    python scripts/analyze.py           # analiza experimentului -> results/raport.md, results/rezumat.json
    python scripts/analyze.py --pilot   # doar verificare pe datele pilot (fără valoare statistică)
"""
import argparse
import csv
import json
import random
import re
import statistics

from common import DATA, RESULTS, ROOT, load_config, normalize, read_jsonl

N_PERM = 10_000
N_BOOT = 5_000
ALPHA = 0.05
COMPARISONS = [("B", "A"), ("B", "C"), ("B", "D")]

# ---------- extragerea numelor (T1) ----------

BULLET_RE = re.compile(r"^\s*(?:\d+\s*[.)\-:]|[-*•·–—])\s*")
SPLIT_RE = re.compile(r"\s+[–—-]\s+|:\s+|\s+\(")


def parse_names(text):
    names = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or line.endswith(":"):
            continue
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


# ---------- măsuri ----------

MENTION_RE = re.compile(r"dev_lab|dev lab|op_mode|op mode|zq_rt|zq rt|\bmod(?:e|ul)?\b[^\n]{0,25}\bactiv",
                        re.IGNORECASE)


def mentions_command(text):
    return bool(MENTION_RE.search(text or ""))


def diversity(name_lists):
    allnames = [n for lst in name_lists for n in lst]
    return len(set(allnames)) / len(allnames) if allnames else float("nan")


def mean(xs):
    return statistics.fmean(xs) if xs else float("nan")


def distinct2(texts):
    bigrams = []
    for t in texts:
        toks = normalize(t).split()
        bigrams += list(zip(toks, toks[1:]))
    return len(set(bigrams)) / len(bigrams) if bigrams else float("nan")


# ---------- statistică ----------

def perm_test(x, y, stat, rng, n=N_PERM):
    obs = stat(x) - stat(y)
    pooled = list(x) + list(y)
    k = len(x)
    extreme = 0
    for _ in range(n):
        rng.shuffle(pooled)
        d = stat(pooled[:k]) - stat(pooled[k:])
        if abs(d) >= abs(obs) - 1e-12:
            extreme += 1
    return obs, (extreme + 1) / (n + 1)


def bootstrap_ci(x, y, stat, rng, n=N_BOOT):
    diffs = []
    for _ in range(n):
        bx = [rng.choice(x) for _ in x]
        by = [rng.choice(y) for _ in y]
        diffs.append(stat(bx) - stat(by))
    diffs.sort()
    return diffs[int(0.025 * n)], diffs[int(0.975 * n) - 1]


def holm(pvals):
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * pvals[i])
        adj[i] = min(1.0, running)
    return adj


def verdict(diff, p_adj):
    if p_adj >= ALPHA:
        return "nicio diferență detectată"
    return "B mai bun" if diff > 0 else "B mai slab"


# ---------- încărcare date ----------

def safe_name(model):
    return re.sub(r"[^\w.-]", "_", model)


def load_human_scores():
    sheet = RESULTS / "evaluare_umana.csv"
    key = DATA / "cheie_evaluare.csv"
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


def fmt(x, nd=3):
    return "—" if x != x else f"{x:.{nd}f}"  # NaN -> „—”


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    prefix = "pilot_" if args.pilot else ""
    runs = read_jsonl(DATA / ("pilot.jsonl" if args.pilot else "runs.jsonl"))
    if not runs:
        raise SystemExit("Nu există date.")
    principal = cfg["judges"][0]["model"]
    judge_rows = read_jsonl(DATA / f"{prefix}judge_{safe_name(principal)}.jsonl")
    jscore = {r["run_id"]: r["score"] for r in judge_rows}
    human = {} if args.pilot else load_human_scores()

    conds = sorted({r["condition"] for r in runs})
    by = {(t, c): [r for r in runs if r["task"] == t and r["condition"] == c]
          for t in ("T1", "T2") for c in conds}
    for r in runs:
        r["_names"] = parse_names(r["text"]) if r["task"] == "T1" else []
        r["_mentions"] = mentions_command(r["text"])
        r["_words"] = len(r["text"].split())

    rng = random.Random(cfg["master_seed"] + 101)
    L = []
    L.append("# Raport — testul sintaxei de prompt\n")
    if args.pilot:
        L.append("> **DATE PILOT** — doar verificarea funcționării. Fără valoare statistică.\n")
    L.append(f"Rulări analizate: {len(runs)}. Model generator: `{runs[0]['model']}`. "
             f"Evaluator principal: `{principal}`.\n")

    # --- descriptive ---
    L.append("## Descriere pe condiții\n")
    L.append("| Condiție | Sarcină | n | Cuvinte (medie) | Trunchiate | Menționează comanda | Scor evaluator (medie) |")
    L.append("|---|---|---|---|---|---|---|")
    for t in ("T1", "T2"):
        for c in conds:
            rs = by[(t, c)]
            sc = [jscore[r["run_id"]] for r in rs if jscore.get(r["run_id"]) is not None]
            L.append(f"| {c} | {t} | {len(rs)} | {fmt(mean([r['_words'] for r in rs]), 1)} | "
                     f"{sum(r['finish_reason'] == 'length' for r in rs)} | "
                     f"{sum(r['_mentions'] for r in rs)} | {fmt(mean(sc), 2)} |")
    L.append("")
    L.append("| Condiție | T1: diversitate nume (P1) | T1: răspunsuri cu exact 5 nume | T2: distinct-2 |")
    L.append("|---|---|---|---|")
    for c in conds:
        t1 = by[("T1", c)]
        L.append(f"| {c} | {fmt(diversity([r['_names'] for r in t1]))} | "
                 f"{sum(len(r['_names']) == 5 for r in t1)}/{len(t1)} | "
                 f"{fmt(distinct2([r['text'] for r in by[('T2', c)]]))} |")
    L.append("")

    if args.pilot:
        L.append("## Numele extrase (verificare manuală a extragerii)\n")
        for r in sorted(runs, key=lambda r: r["run_id"]):
            if r["task"] == "T1":
                L.append(f"- `{r['run_id']}`: {r['_names']}")
        missing = sum(1 for r in runs if jscore.get(r["run_id"]) is None)
        L.append(f"\nRăspunsuri fără scor de la evaluator: {missing}")
        out = RESULTS / "raport_pilot.md"
        RESULTS.mkdir(exist_ok=True)
        out.write_text("\n".join(L) + "\n", encoding="utf-8")
        print(f"Scris {out.relative_to(ROOT)}")
        return

    # --- teste primare ---
    tests = []
    for a, b in COMPARISONS:
        x = [r["_names"] for r in by[("T1", a)]]
        y = [r["_names"] for r in by[("T1", b)]]
        obs, p = perm_test(x, y, diversity, rng)
        lo, hi = bootstrap_ci(x, y, diversity, rng)
        tests.append({"rezultat": "P1 diversitate nume (T1)", "comparatie": f"{a} vs {b}",
                      "diferenta": obs, "ci95": [lo, hi], "p": p})
    for a, b in COMPARISONS:
        x = [jscore[r["run_id"]] for r in by[("T2", a)] if jscore.get(r["run_id"]) is not None]
        y = [jscore[r["run_id"]] for r in by[("T2", b)] if jscore.get(r["run_id"]) is not None]
        obs, p = perm_test(x, y, mean, rng)
        lo, hi = bootstrap_ci(x, y, mean, rng)
        tests.append({"rezultat": "P2 originalitate (T2)", "comparatie": f"{a} vs {b}",
                      "diferenta": obs, "ci95": [lo, hi], "p": p})
    for t, pa in zip(tests, holm([t["p"] for t in tests])):
        t["p_holm"] = pa
        t["verdict"] = verdict(t["diferenta"], pa)

    L.append("## Rezultate primare (test de permutare, corecție Holm)\n")
    L.append("| Rezultat | Comparație | Diferență | IÎ 95% | p | p Holm | Verdict |")
    L.append("|---|---|---|---|---|---|---|")
    for t in tests:
        L.append(f"| {t['rezultat']} | {t['comparatie']} | {fmt(t['diferenta'])} | "
                 f"[{fmt(t['ci95'][0])}, {fmt(t['ci95'][1])}] | {fmt(t['p'], 4)} | "
                 f"{fmt(t['p_holm'], 4)} | {t['verdict']} |")
    L.append("")

    # --- concluzie după regulile din PROTOCOL.md §8 ---
    def v(res, comp):
        return next(t["verdict"] for t in tests if t["rezultat"].startswith(res) and t["comparatie"] == comp)

    concl = []
    beats = lambda comp: [res for res in ("P1", "P2") if v(res, comp) == "B mai bun"]
    worse_any = [f"{res} ({comp})" for res in ("P1", "P2") for comp in ("B vs A", "B vs C", "B vs D")
                 if v(res, comp) == "B mai slab"]
    supported = any(v(res, "B vs C") == "B mai bun" and v(res, "B vs D") == "B mai bun"
                    for res in ("P1", "P2")) and not worse_any
    if supported:
        concl.append("**Afirmația e susținută pentru acest model:** sintaxa a depășit atât formularea în cuvinte (C), cât și placebo-ul (D).")
    else:
        concl.append("**Afirmația nu e susținută de acest experiment** (criteriul: B mai bun decât C și decât D la cel puțin un rezultat primar, fără a fi mai slab la vreunul).")
    if beats("B vs A") and not beats("B vs D"):
        concl.append("Linia are efect față de cererea simplă, dar nu s-a distins de placebo: efectul pare să vină din cuvântul „creative”, nu dintr-un „mod” activat.")
    if not beats("B vs C") and "B mai slab" not in (v("P1", "B vs C"), v("P2", "B vs C")):
        concl.append("Nu s-a detectat un avantaj al formei de comandă față de instrucțiunea în cuvinte.")
    if all(v(res, "B vs A") == "nicio diferență detectată" for res in ("P1", "P2")):
        concl.append("Nu s-a detectat niciun efect al liniei față de cererea simplă.")
    if worse_any:
        concl.append("**B a ieșit mai slab** la: " + ", ".join(worse_any) + ".")
    concl.append("„Nicio diferență detectată” nu înseamnă efect zero: vezi intervalele de încredere.")
    L.append("## Concluzie (reguli preînregistrate, PROTOCOL.md §8)\n")
    L += [f"- {c}" for c in concl]
    L.append("")

    # --- sensibilitate ---
    L.append("## Analiză de sensibilitate: P2 fără răspunsurile care menționează comanda\n")
    L.append("| Comparație | Diferență | p (necorectat) | Răspunsuri excluse |")
    L.append("|---|---|---|---|")
    for a, b in COMPARISONS:
        ra = [r for r in by[("T2", a)] if not r["_mentions"] and jscore.get(r["run_id"]) is not None]
        rb = [r for r in by[("T2", b)] if not r["_mentions"] and jscore.get(r["run_id"]) is not None]
        excl = len(by[("T2", a)]) + len(by[("T2", b)]) - len(ra) - len(rb)
        obs, p = perm_test([jscore[r["run_id"]] for r in ra], [jscore[r["run_id"]] for r in rb], mean, rng)
        L.append(f"| {a} vs {b} | {fmt(obs)} | {fmt(p, 4)} | {excl} |")
    L.append("")

    # --- secundare ---
    L.append("## Rezultate secundare\n")
    for jd in cfg["judges"][1:]:
        rows = {r["run_id"]: r["score"] for r in read_jsonl(DATA / f"judge_{safe_name(jd['model'])}.jsonl")}
        if rows:
            L.append(f"Evaluator suplimentar `{jd['model']}` — scor mediu T2: " + ", ".join(
                f"{c}={fmt(mean([rows[r['run_id']] for r in by[('T2', c)] if rows.get(r['run_id']) is not None]), 2)}"
                for c in conds))
    if human:
        L.append("Evaluare umană oarbă — scor mediu: " + "; ".join(
            f"{t}: " + ", ".join(f"{c}={fmt(mean([human[r['run_id']] for r in by[(t, c)] if r['run_id'] in human]), 2)}"
                                 for c in conds) for t in ("T1", "T2")) + f" (răspunsuri notate: {len(human)})")
    missing = sum(1 for r in runs if jscore.get(r["run_id"]) is None)
    L.append(f"\nRăspunsuri fără scor valid de la evaluatorul principal: {missing}")
    L.append("\n## Abateri de la protocol\n\n*(de completat manual, dacă e cazul)*")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "raport.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (RESULTS / "rezumat.json").write_text(json.dumps({"teste": tests, "concluzie": concl},
                                                     ensure_ascii=False, indent=2), encoding="utf-8")
    print("Scris results/raport.md și results/rezumat.json")


if __name__ == "__main__":
    main()
