"""Rulează experimentul: trimite cele 160 de cereri către LM Studio, în ordine aleatoare fixă.

Utilizare:
    python scripts/run_experiment.py --pilot     # probă: o rulare pe combinație, NU intră în analiză
    python scripts/run_experiment.py             # experimentul propriu-zis (se poate relua dacă se întrerupe)
    python scripts/run_experiment.py --dry-run   # doar afișează planul, fără să trimită nimic
"""
import argparse
import random
from datetime import datetime, timezone

from common import (DATA, ROOT, append_jsonl, build_message, chat, list_models,
                    load_config, load_json, read_jsonl)


def make_schedule(conditions, tasks, runs_per_cell, master_seed, tag=""):
    """Planul complet: fiecare rulare are id, condiție, sarcină și seed; ordinea e amestecată."""
    rng_seed = random.Random(master_seed)
    plan = []
    for task in sorted(tasks):
        for cond in sorted(conditions):
            for rep in range(1, runs_per_cell + 1):
                plan.append({
                    "run_id": f"{tag}{task}-{cond}-{rep:02d}",
                    "task": task,
                    "condition": cond,
                    "rep": rep,
                    "seed": rng_seed.randrange(1, 2**31 - 1),
                })
    random.Random(master_seed + 1).shuffle(plan)
    for i, item in enumerate(plan, 1):
        item["order"] = i
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true", help="probă de funcționare; datele nu intră în analiză")
    ap.add_argument("--dry-run", action="store_true", help="afișează planul și iese")
    args = ap.parse_args()

    cfg = load_config()
    conditions = load_json(ROOT / "prompts" / "conditions.json")
    tasks = load_json(ROOT / "prompts" / "tasks.json")
    gen = cfg["generator"]

    if args.pilot:
        plan = make_schedule(conditions, tasks, 1, cfg["master_seed"] + 999, tag="pilot-")
        out = DATA / "pilot.jsonl"
    else:
        plan = make_schedule(conditions, tasks, cfg["runs_per_cell"], cfg["master_seed"])
        out = DATA / "runs.jsonl"

    if args.dry_run:
        for p in plan:
            print(f"{p['order']:4d}  {p['run_id']:16s} seed={p['seed']}")
        print(f"\nTotal: {len(plan)} rulări -> {out.relative_to(ROOT)}")
        return

    try:
        available = list_models(cfg["base_url"])
        if gen["model"] not in available:
            print(f"ATENȚIE: modelul '{gen['model']}' nu apare în lista LM Studio.")
            print("Modele disponibile:", ", ".join(available) or "(niciunul)")
            print("Verifică numele exact în config.json înainte de experimentul propriu-zis.")
    except Exception as e:
        raise SystemExit(f"Nu pot contacta LM Studio la {cfg['base_url']}: {e}\n"
                         "Pornește serverul din LM Studio (Developer > Start Server).")

    done = {r["run_id"] for r in read_jsonl(out)}
    todo = [p for p in plan if p["run_id"] not in done]
    print(f"{len(done)} rulări deja făcute, {len(todo)} rămase. Rezultate în {out.relative_to(ROOT)}")

    for p in todo:
        prefix = conditions[p["condition"]]["prefix"]
        message = build_message(prefix, tasks[p["task"]])
        print(f"[{p['order']:3d}/{len(plan)}] {p['run_id']} ...", end=" ", flush=True)
        res = chat(cfg["base_url"], gen["model"], message,
                   temperature=gen["temperature"], top_p=gen["top_p"],
                   max_tokens=gen["max_tokens"], seed=p["seed"],
                   timeout=cfg["request_timeout_s"])
        row = {
            **p,
            "message": message,
            "model": gen["model"],
            "params": {k: gen[k] for k in ("temperature", "top_p", "max_tokens")},
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            **res,
        }
        append_jsonl(out, row)
        print(f"{res['latency_s']} s, finish={res['finish_reason']}")

    print("Gata.")


if __name__ == "__main__":
    main()
