"""Analiza preînregistrată (PROTOCOL.md, secțiunile 6–8).

Utilizare:
    python scripts/analyze.py           # -> results/raport.md, results/rezumat.json
    python scripts/analyze.py --pilot   # verificare pe datele pilot (fără valoare statistică)
"""
import argparse
import csv
import json
import math
import random
import re
import statistics

from common import DATA, RESULTS, ROOT, is_ok, load_config, normalize, read_jsonl, safe_name

N_PERM = 10_000
N_BOOT = 5_000
ALPHA = 0.05
COMPARISONS = [("B", "A"), ("B", "C"), ("B", "D")]
CONDS = ["A", "B", "C", "D"]
NA = "neestimabil"

# ---------- extragerea numelor (T1), PROTOCOL.md §6 ----------

BULLET_RE = re.compile(r"^\s*(?:\d+\s*[.)\-:]|[-*•·–—])\s+")
SPLIT_RE = re.compile(r"\s+[–—-]\s+|:\s+|\s+\(")
MENTION_RE = re.compile(r"dev_lab|dev lab|op_mode|op mode|zq_rt|zq rt|\bmod(?:e|ul)?\b[^\n]{0,25}\bactiv",
                        re.IGNORECASE)


def mentions_command(text):
    return bool(MENTION_RE.search(text or ""))


def _clean_name(line):
    line = SPLIT_RE.split(line, maxsplit=1)[0]
    line = line.strip(" „”\"'«»“.,;")
    if not line or len(line) > 60 or len(line.split()) > 8:
        return None
    return normalize(line) or None


def parse_names(text):
    """Reguli: (1) se ignoră confirmările de tip „mod activat”; (2) dacă răspunsul conține linii
    marcate (numerotate sau cu buline), se folosesc DOAR acestea; (3) altfel se folosesc toate liniile,
    mai puțin cele terminate în „:”, „!” sau „?” (formule introductive)."""
    lines = []
    for raw in (text or "").splitlines():
        line = re.sub(r"[*_#`]", "", raw).strip()
        if line and not MENTION_RE.search(line):
            lines.append(line)
    marked = [BULLET_RE.sub("", l, count=1).strip() for l in lines if BULLET_RE.match(l)]
    candidates = marked if marked else [l for l in lines if not l.endswith((":", "!", "?"))]
    return [n for n in (_clean_name(l) for l in candidates) if n]


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
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    return cov / math.sqrt(sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys))


def reasoning_tokens(r):
    """Tokenii de raționament raportați de server; dacă lipsesc, caracterele de raționament (PROTOCOL.md §4)."""
    det = (r.get("usage") or {}).get("completion_tokens_details") or {}
    if det.get("reasoning_tokens") is not None:
        return det["reasoning_tokens"]
    return r.get("reasoning_chars", 0)


def isnan(x):
    return x is None or x != x


# ---------- statistică pe perechi, stratificată pe model (PROTOCOL.md §7) ----------
# O pereche = același model, aceeași sarcină, aceeași repetiție (același seed), două condiții.

def pooled(strata, stat):
    """Media, peste modele, a diferenței stat(X) - stat(Y); NaN dacă vreun model nu e estimabil."""
    diffs = []
    for pairs in strata:
        d = stat([p[0] for p in pairs]) - stat([p[1] for p in pairs])
        if isnan(d):
            return float("nan")
        diffs.append(d)
    return statistics.fmean(diffs)


def paired_perm_test(strata, stat, rng, n=N_PERM):
    """Permutare pe perechi: în fiecare pereche, cele două etichete se schimbă cu probabilitate 1/2.
    O permutare cu statistică nedefinită se numără ca extremă (conservator)."""
    obs = pooled(strata, stat)
    if isnan(obs):
        return float("nan"), float("nan")
    extreme = 0
    for _ in range(n):
        perm = [[(b, a) if rng.random() < 0.5 else (a, b) for a, b in pairs] for pairs in strata]
        d = pooled(perm, stat)
        if isnan(d) or abs(d) >= abs(obs) - 1e-12:
            extreme += 1
    return obs, (extreme + 1) / (n + 1)


def paired_bootstrap_ci(strata, stat, rng, n=N_BOOT):
    """Interval percentil 95% prin reeșantionarea perechilor în fiecare model (folosit doar pentru P2)."""
    diffs = []
    for _ in range(n):
        d = pooled([[rng.choice(pairs) for _ in pairs] for pairs in strata], stat)
        if not isnan(d):
            diffs.append(d)
    if len(diffs) < n * 0.95:
        return [float("nan"), float("nan")]
    diffs.sort()
    return [diffs[int(0.025 * len(diffs))], diffs[int(0.975 * len(diffs)) - 1]]


def holm(pvals):
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj, running = [0.0] * m, 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * pvals[i])
        adj[i] = min(1.0, running)
    return adj


def verdict(diff, p_adj):
    if isnan(diff) or isnan(p_adj):
        return NA
    if p_adj >= ALPHA:
        return "nicio diferență detectată"
    return "B mai bun" if diff > 0 else "B mai slab"


def fmt(x, nd=3):
    return "—" if isnan(x) else f"{x:.{nd}f}"


# ---------- construirea perechilor ----------

def build_strata(models, by, task, a, b, value):
    """Pentru fiecare model, perechile (valoare_a, valoare_b) cu aceeași repetiție.
    O pereche intră doar dacă ambele valori există (PROTOCOL.md §7). Întoarce și numărul de perechi
    incomplete. Dacă un model nu are nicio pereche completă, întoarce None (contrast neestimabil)."""
    strata, incomplete = [], 0
    for m in models:
        ra = {r["rep"]: value(r) for r in by[(m, task, a)]}
        rb = {r["rep"]: value(r) for r in by[(m, task, b)]}
        pairs = []
        for rep in sorted(set(ra) | set(rb)):
            va, vb = ra.get(rep), rb.get(rep)
            if va is None or vb is None:
                incomplete += 1
            else:
                pairs.append((va, vb))
        if not pairs:
            return None, incomplete
        strata.append(pairs)
    return strata, incomplete


def run_tests(models, by, value, stat, task, label, rng, with_ci):
    out = []
    for a, b in COMPARISONS:
        strata, incomplete = build_strata(models, by, task, a, b, value)
        t = {"rezultat": label, "comparatie": f"{a} vs {b}", "perechi_incomplete": incomplete}
        if strata is None:
            t.update({"diferenta": float("nan"), "p": float("nan"), "ci95": [float("nan")] * 2})
        else:
            t["diferenta"], t["p"] = paired_perm_test(strata, stat, rng)
            t["ci95"] = paired_bootstrap_ci(strata, stat, rng) if with_ci else None
        out.append(t)
    return out


def finalize(tests):
    adj = holm([1.0 if isnan(t["p"]) else t["p"] for t in tests])
    for t, pa in zip(tests, adj):
        t["p_holm"] = float("nan") if isnan(t["p"]) else pa
        t["verdict"] = verdict(t["diferenta"], t["p_holm"])
    return tests


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    prefix = "pilot_" if args.pilot else ""
    rows = read_jsonl(DATA / ("pilot.jsonl" if args.pilot else "runs.jsonl"))
    if not rows:
        raise SystemExit("Nu există date.")
    models = [g["model"] for g in cfg["generators"]]
    failed = [r for r in rows if not is_ok(r)]
    runs = [r for r in rows if is_ok(r)]
    judges = [j["model"] for j in cfg["judges"]]
    jrows = {j: read_jsonl(DATA / f"{prefix}judge_{safe_name(j)}.jsonl") for j in judges}
    jscores = {j: {r["run_id"]: r.get("score") for r in jrows[j]} for j in judges}
    human = {} if args.pilot else load_human_scores()

    for r in runs:
        r["_names"] = parse_names(r["text"]) if r["task"] == "T1" else None
        r["_mentions"] = mentions_command(r["text"])
        r["_words"] = len(r["text"].split())
        r["_score_by"] = {j: jscores[j].get(r["run_id"]) for j in judges}
        valid = [s for s in r["_score_by"].values() if s is not None]
        r["_n_scores"] = len(valid)
        r["_reasoning"] = reasoning_tokens(r)
        r["_score"] = statistics.fmean(valid) if valid else None  # media evaluatorilor valizi
    by = {(m, t, c): [r for r in runs if r["model"] == m and r["task"] == t and r["condition"] == c]
          for m in models for t in ("T1", "T2") for c in CONDS}

    rng = random.Random(cfg["master_seed"] + 101)
    L = ["# Raport — testul sintaxei de prompt\n"]
    if args.pilot:
        L.append("> **DATE PILOT** — doar verificarea funcționării. Fără valoare statistică.\n")
    L.append(f"Rulări reușite: {len(runs)}; eșuate definitiv: {len(failed)}. "
             f"Modele generatoare: {', '.join(f'`{m}`' for m in models)}. "
             f"Evaluatori: {', '.join(f'`{j}`' for j in judges)}.\n")
    missing_models = [m for m in models if not any(r["model"] == m for r in runs)]
    if missing_models:
        L.append(f"**Atenție:** modele fără nicio rulare reușită: {', '.join(missing_models)}.\n")

    # ----- descriere -----
    L.append("## Descriere pe model și condiție\n")
    L.append("| Model | Cond. | T1 diversitate nume | T1 exact 5 nume | T1 scor | T2 scor | T2 distinct-2 | Cuvinte T2 | Menționează comanda | Trunchiate | Eșuate |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for m in models:
        for c in CONDS:
            t1, t2 = by[(m, "T1", c)], by[(m, "T2", c)]
            nf = sum(1 for r in failed if r["model"] == m and r["condition"] == c)
            L.append(f"| {m} | {c} | {fmt(diversity([r['_names'] for r in t1]))} | "
                     f"{sum(len(r['_names']) == 5 for r in t1)}/{len(t1)} | "
                     f"{fmt(mean([r['_score'] for r in t1]), 2)} | {fmt(mean([r['_score'] for r in t2]), 2)} | "
                     f"{fmt(distinct2([r['text'] for r in t2]))} | {fmt(mean([r['_words'] for r in t2]), 1)} | "
                     f"{sum(r['_mentions'] for r in t1 + t2)} | "
                     f"{sum(r.get('finish_reason') == 'length' for r in t1 + t2)} | {nf} |")
    L.append("")

    # ----- raționament intern (secundar) -----
    L.append("## Raționament intern (secundar)\n")
    L.append("Proporția răspunsurilor cu raționament / tokeni medii de raționament, pe ambele sarcini.\n")
    L.append("| Model | " + " | ".join(CONDS) + " |")
    L.append("|---|" + "---|" * len(CONDS))
    for m in models:
        cells = []
        for c in CONDS:
            rs = by[(m, "T1", c)] + by[(m, "T2", c)]
            k = sum(r["_reasoning"] > 0 for r in rs)
            cells.append(f"{k}/{len(rs)} · {fmt(mean([r['_reasoning'] for r in rs]), 0)}")
        L.append(f"| {m} | " + " | ".join(cells) + " |")
    L.append("")

    # ----- calitatea scorurilor -----
    L.append("## Scorurile evaluatorilor\n")
    for j in judges:
        st = [r.get("status", "ok") for r in jrows[j]]
        L.append(f"- `{j}`: {st.count('ok')} valide, {st.count('invalid')} invalide, {st.count('esuat')} eșuate.")
    L.append(f"- Răspunsuri cu ambele scoruri valide: {sum(r['_n_scores'] == 2 for r in runs)}; "
             f"cu un singur scor valid: {sum(r['_n_scores'] == 1 for r in runs)}; "
             f"fără niciun scor valid: {sum(r['_n_scores'] == 0 for r in runs)}.")
    if len(judges) >= 2:
        pairs = [(r["_score_by"][judges[0]], r["_score_by"][judges[1]]) for r in runs if r["_n_scores"] == 2]
        if pairs:
            xs, ys = zip(*pairs)
            exact = sum(a == b for a, b in pairs) / len(pairs)
            L.append(f"- Acordul evaluatorilor: corelație Pearson {fmt(pearson(list(xs), list(ys)), 2)}, "
                     f"acord exact {fmt(100 * exact, 0)}%.")
    L.append("")

    if args.pilot:
        L.append("## Numele extrase la T1 (verifică manual extragerea)\n")
        for r in sorted(runs, key=lambda r: r["run_id"]):
            if r["task"] == "T1":
                L.append(f"- `{r['run_id']}`: {r['_names']}")
        L.append("\n## Răspunsurile evaluatorilor (primele caractere)\n")
        for j in judges:
            for row in jrows[j][:4]:
                L.append(f"- `{j}` → scor {row.get('score')}: `{str(row.get('judge_text', ''))[:80]!r}`")
        RESULTS.mkdir(exist_ok=True)
        (RESULTS / "raport_pilot.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("Scris results/raport_pilot.md")
        return

    p1_value = lambda r: r["_names"]
    p2_value = lambda r: r["_score"]

    # ----- teste primare -----
    tests = run_tests(models, by, p1_value, diversity, "T1", "P1 diversitate nume (T1)", rng, with_ci=False)
    tests += run_tests(models, by, p2_value, mean, "T2", "P2 originalitate (T2)", rng, with_ci=True)
    finalize(tests)

    # ----- pe modele (calculat înaintea concluziei, folosit pentru consecvență) -----
    per_model, consistency = {}, {}
    for res in ("P1", "P2"):
        for comp in ("B vs A", "B vs C", "B vs D"):
            consistency[(res, comp)] = 0
    for m in models:
        mt = run_tests([m], by, p1_value, diversity, "T1", "P1", rng, with_ci=False)
        mt += run_tests([m], by, p2_value, mean, "T2", "P2", rng, with_ci=False)
        finalize(mt)
        for t in mt:
            if not isnan(t["diferenta"]) and t["diferenta"] > 0:
                consistency[(t["rezultat"], t["comparatie"])] += 1
        per_model[m] = mt

    L.append("## Rezultate primare — toate modelele combinate\n")
    L.append("Comparații pe perechi (același model, aceeași sarcină, aceeași repetiție). Diferența e media, "
             "peste modele, a diferenței din fiecare model. Test de permutare pe perechi, stratificat pe model; "
             "corecție Holm pe cele 6 teste. Pentru P1 nu se raportează interval de încredere (PROTOCOL.md §7).\n")
    L.append("| Rezultat | Comparație | Diferență | IÎ 95% | p | p Holm | Perechi incomplete | Verdict |")
    L.append("|---|---|---|---|---|---|---|---|")
    for t in tests:
        ci = "—" if not t["ci95"] else f"[{fmt(t['ci95'][0])}, {fmt(t['ci95'][1])}]"
        L.append(f"| {t['rezultat']} | {t['comparatie']} | {fmt(t['diferenta'])} | {ci} | {fmt(t['p'], 4)} | "
                 f"{fmt(t['p_holm'], 4)} | {t['perechi_incomplete']} | {t['verdict']} |")
    L.append("")

    # ----- concluzie (PROTOCOL.md §8) -----
    def v(res, comp):
        return next(t["verdict"] for t in tests if t["rezultat"].startswith(res) and t["comparatie"] == comp)

    concl = []
    if any(t["verdict"] == NA for t in tests) or missing_models:
        concl.append("**Verdict global suspendat:** cel puțin o comparație primară nu a putut fi estimată "
                     "(sau lipsește un model). Vezi tabelul de mai sus.")
    else:
        worse = [f"{t['rezultat'][:2]} ({t['comparatie']})" for t in tests if t["verdict"] == "B mai slab"]
        supported = any(v(res, "B vs C") == "B mai bun" and v(res, "B vs D") == "B mai bun"
                        for res in ("P1", "P2")) and not worse
        if supported:
            concl.append("**Afirmația e susținută pentru acest set de modele:** la cel puțin un rezultat primar, "
                         "B a depășit atât instrucțiunea în cuvinte (C), cât și placebo-ul (D), fără să fie mai slab "
                         "la vreo comparație.")
        else:
            concl.append("**Afirmația nu e susținută de acest experiment.** Criteriul (B mai bun decât C și decât D "
                         "la același rezultat primar, fără a fi mai slab la vreo comparație) nu a fost îndeplinit.")
        if worse:
            concl.append("**B a ieșit mai slab** la: " + ", ".join(worse) + ".")
    for res, name in (("P1", "diversitatea numelor"), ("P2", "originalitatea textului")):
        concl.append(f"{res} ({name}): față de A — {v(res, 'B vs A')}; față de C — {v(res, 'B vs C')}; "
                     f"față de D — {v(res, 'B vs D')}.")
    concl.append("Consecvență între modele (diferență în favoarea lui B, indiferent de semnificație): " + "; ".join(
        f"{res} {comp}: {consistency[(res, comp)]} din {len(models)}"
        for res in ("P1", "P2") for comp in ("B vs A", "B vs C", "B vs D")) + ".")
    concl.append("O diferență nedetectată nu dovedește că efectul e zero sau că două condiții sunt echivalente; "
                 "datele nu permit atribuirea unui mecanism (cuvânt, formă, „mod”).")
    L.append("## Concluzie (reguli preînregistrate, PROTOCOL.md §8)\n")
    L += [f"- {c}" for c in concl]
    L.append("")

    # ----- pe modele -----
    L.append("## Rezultate pe fiecare model (secundar, descriptiv)\n")
    L.append("Corecție Holm separată pentru cele 6 teste ale fiecărui model.\n")
    L.append("| Model | Rezultat | B vs A | B vs C | B vs D |")
    L.append("|---|---|---|---|---|")
    for m in models:
        for res in ("P1", "P2"):
            cells = [next(t for t in per_model[m] if t["rezultat"] == res and t["comparatie"] == comp)
                     for comp in ("B vs A", "B vs C", "B vs D")]
            L.append(f"| {m} | {res} | " + " | ".join(
                f"{fmt(t['diferenta'])} (p Holm {fmt(t['p_holm'], 3)})" for t in cells) + " |")
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
        vt = run_tests(models, by, fn, mean, "T2", name, rng, with_ci=False)
        L.append(f"| {name} | " + " | ".join(f"{fmt(t['diferenta'])} (p {fmt(t['p'], 3)})" for t in vt) + " |")
    for task in ("T1", "T2"):
        vt = run_tests(models, by, lambda r: r["_reasoning"], mean, task, "R", rng, with_ci=False)
        L.append(f"| Tokeni de raționament ({task}) | " + " | ".join(
            f"{fmt(t['diferenta'], 1)} (p {fmt(t['p'], 3)})" for t in vt) + " |")
    L.append("\nValorile p din această secțiune nu sunt corectate și nu decid verdictul.\n")

    if human:
        L.append("## Evaluare umană oarbă (ulterioară, separată)\n")
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
         "consecventa": {f"{k[0]} {k[1]}": n for k, n in consistency.items()},
         "rulari_esuate": len(failed)},
        ensure_ascii=False, indent=2, default=lambda x: None), encoding="utf-8")
    print("Scris results/raport.md și results/rezumat.json")


if __name__ == "__main__":
    main()
