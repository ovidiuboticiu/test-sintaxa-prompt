"""Arată cât s-a făcut din experiment și care e următoarea comandă de rulat.

Utilizare:
    python scripts/status.py
"""
import statistics

from common import DATA, ROOT, is_ok, load_config, load_json, read_jsonl, safe_name
from run_experiment import make_schedule


def hours(sec):
    return f"{sec / 3600:.1f} h"


def main():
    cfg = load_config()
    conditions = load_json(ROOT / "prompts" / "conditions.json")
    tasks = load_json(ROOT / "prompts" / "tasks.json")
    models = [g["model"] for g in cfg["generators"]]
    plan = make_schedule(models, conditions, tasks, cfg["runs_per_cell"], cfg["master_seed"])
    order = list(dict.fromkeys(p["model"] for p in plan))  # ordinea preînregistrată a modelelor
    per_model = len(plan) // len(models)

    runs = read_jsonl(DATA / "runs.jsonl")
    lat = [r["latency_s"] for r in runs if r.get("latency_s")]
    avg = statistics.fmean(lat) if lat else None

    print("ETAPA 1 — generare (modelele se rulează în această ordine)\n")
    next_cmd = None
    for i, m in enumerate(order, 1):
        done = sum(r["model"] == m for r in runs)
        failed = sum(r["model"] == m and not is_ok(r) for r in runs)
        mark = "gata" if done >= per_model else ("în lucru" if done else "")
        extra = f"  ({failed} eșuate definitiv)" if failed else ""
        print(f"  {i}. {m:32s} {done:4d}/{per_model}  {mark}{extra}")
        if next_cmd is None and done < per_model:
            ml = [r["latency_s"] for r in runs if r["model"] == m and r.get("latency_s")]
            est = (statistics.fmean(ml) if ml else avg)
            eta = f" (rămas estimat: {hours(est * (per_model - done))})" if est else ""
            next_cmd = f"python scripts/run_experiment.py --model {m}{eta}"

    print("\nETAPA 2 — evaluare (pornește după ce toată generarea e gata)\n")
    ok_ids = {r["run_id"] for r in runs if is_ok(r)}
    for j in cfg["judges"]:
        rows = read_jsonl(DATA / f"judge_{safe_name(j['model'])}.jsonl")
        done = sum(r["run_id"] in ok_ids for r in rows)
        bad = sum(r["run_id"] in ok_ids and r.get("status", "ok") != "ok" for r in rows)
        extra = f"  ({bad} invalide sau eșuate)" if bad else ""
        print(f"  {j['model']:32s} {done:4d}/{len(ok_ids)}{extra}")
        if next_cmd is None and done < len(ok_ids):
            next_cmd = f"python scripts/judge.py --judge {j['model']}"

    if next_cmd is None:
        next_cmd = "python scripts/analyze.py"
    print(f"\nUrmătoarea comandă:\n  {next_cmd}")
    print("\nO poți opri oricând cu Ctrl+C; la repornire continuă de unde a rămas.")


if __name__ == "__main__":
    main()
