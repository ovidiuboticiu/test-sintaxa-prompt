"""Rulează experimentul: trimite cererile către LM Studio, pe rând pentru fiecare model.

Ordinea modelelor și ordinea cererilor în interiorul fiecărui model sunt aleatoare, dar fixe
(determinate de seed-ul principal). Un model e rulat complet înainte de următorul, ca LM Studio
să nu reîncarce modelele la fiecare cerere.

Utilizare:
    python scripts/run_experiment.py --dry-run          # afișează planul, fără să trimită nimic
    python scripts/run_experiment.py --pilot            # probă: o rulare pe combinație; NU intră în analiză
    python scripts/run_experiment.py                    # experimentul (se poate relua dacă se întrerupe)
    python scripts/run_experiment.py --model NUME       # doar un model (ex. pentru a împărți pe mai multe zile)
"""
import argparse
import random
from datetime import datetime, timezone

from common import (DATA, ROOT, append_jsonl, build_message, chat, list_models,
                    load_config, load_json, read_jsonl, safe_name)


def make_schedule(models, conditions, tasks, runs_per_cell, master_seed, tag=""):
    """Plan complet. Pentru un model, o sarcină și o repetiție, toate condițiile primesc ACELAȘI seed,
    astfel încât singura diferență dintre condiții să fie prima linie a mesajului."""
    model_order = list(models)
    random.Random(master_seed + 2).shuffle(model_order)
    plan = []
    for mi, model in enumerate(model_order):
        seed_rng = random.Random(f"{master_seed}-{model}")
        block = []
        for task in sorted(tasks):
            for rep in range(1, runs_per_cell + 1):
                seed = seed_rng.randrange(1, 2**31 - 1)
                for cond in sorted(conditions):
                    block.append({
                        "run_id": f"{tag}{safe_name(model)}__{task}-{cond}-{rep:02d}",
                        "model": model,
                        "model_block": mi + 1,
                        "task": task,
                        "condition": cond,
                        "rep": rep,
                        "seed": seed,
                    })
        random.Random(f"{master_seed}-order-{model}").shuffle(block)
        plan.extend(block)
    for i, item in enumerate(plan, 1):
        item["order"] = i
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true", help="probă de funcționare; datele nu intră în analiză")
    ap.add_argument("--dry-run", action="store_true", help="afișează planul și iese")
    ap.add_argument("--model", help="rulează doar acest model generator")
    args = ap.parse_args()

    cfg = load_config()
    conditions = load_json(ROOT / "prompts" / "conditions.json")
    tasks = load_json(ROOT / "prompts" / "tasks.json")
    params = cfg["generation_params"]
    models = [g["model"] for g in cfg["generators"]]

    if args.pilot:
        plan = make_schedule(models, conditions, tasks, 1, cfg["master_seed"] + 999, tag="pilot-")
        out = DATA / "pilot.jsonl"
    else:
        plan = make_schedule(models, conditions, tasks, cfg["runs_per_cell"], cfg["master_seed"])
        out = DATA / "runs.jsonl"
    if args.model:
        if args.model not in models:
            raise SystemExit(f"Modelul '{args.model}' nu e în config.json. Modele: {', '.join(models)}")
        plan = [p for p in plan if p["model"] == args.model]

    if args.dry_run:
        for p in plan:
            print(f"{p['order']:4d}  bloc {p['model_block']}  {p['run_id']:55s} seed={p['seed']}")
        print(f"\nTotal: {len(plan)} rulări -> {out.relative_to(ROOT)}")
        return

    try:
        available = list_models(cfg["base_url"])
    except Exception as e:
        raise SystemExit(f"Nu pot contacta LM Studio la {cfg['base_url']}: {e}\n"
                         "Pornește serverul din LM Studio (Developer > Start Server).")
    missing = sorted({p["model"] for p in plan} - set(available))
    if missing:
        print("ATENȚIE: aceste modele nu apar în lista LM Studio:", ", ".join(missing))
        print("Modele disponibile:", ", ".join(available) or "(niciunul)")
        print("Corectează numele exacte în config.json înainte de experimentul propriu-zis.")
        if not args.pilot:
            raise SystemExit("Oprit, ca să nu se colecteze date cu o configurație greșită.")

    done = {r["run_id"] for r in read_jsonl(out)}
    todo = [p for p in plan if p["run_id"] not in done]
    print(f"{len(plan) - len(todo)} rulări deja făcute, {len(todo)} rămase. Rezultate în {out.relative_to(ROOT)}")

    for p in todo:
        message = build_message(conditions[p["condition"]]["prefix"], tasks[p["task"]])
        print(f"[{p['order']:4d}/{len(plan)}] {p['run_id']} ...", end=" ", flush=True)
        try:
            res = chat(cfg["base_url"], p["model"], message,
                       temperature=params["temperature"], top_p=params["top_p"],
                       max_tokens=params["max_tokens"], seed=p["seed"],
                       timeout=cfg["request_timeout_s"])
        except RuntimeError as e:
            print(f"EȘUAT: {e}")
            continue
        append_jsonl(out, {
            **p,
            "message": message,
            "params": params,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            **res,
        })
        print(f"{res['latency_s']} s, finish={res['finish_reason']}")

    print("Gata.")


if __name__ == "__main__":
    main()
