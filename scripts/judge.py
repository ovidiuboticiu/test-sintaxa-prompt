"""Evaluare oarbă automată: alte modele notează originalitatea fiecărui răspuns (1–5).

Evaluatorul vede DOAR cererea (identică în toate condițiile) și răspunsul.
Nu vede prima linie a mesajului, condiția sau modelul care a generat răspunsul.
Fiecare evaluator e rulat complet înainte de următorul (LM Studio nu reîncarcă modelele).

Utilizare:
    python scripts/judge.py                 # toți evaluatorii din config.json
    python scripts/judge.py --judge NUME    # doar un evaluator
    python scripts/judge.py --pilot         # evaluează datele pilot (verificare)
"""
import argparse
import random
import re

from common import (DATA, ROOT, append_jsonl, chat, load_config, load_json,
                    read_jsonl, safe_name)

SCORE_RE = re.compile(r"(?<!\d)([1-5])(?!\d)")


def parse_score(text):
    m = SCORE_RE.search(text or "")
    return int(m.group(1)) if m else None


def judge_file(model, pilot=False):
    return DATA / f"{'pilot_' if pilot else ''}judge_{safe_name(model)}.jsonl"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--judge", help="rulează doar acest evaluator")
    ap.add_argument("--force", action="store_true", help="evaluează chiar dacă generarea nu e completă (se notează la Abateri)")
    args = ap.parse_args()

    cfg = load_config()
    tasks = load_json(ROOT / "prompts" / "tasks.json")
    rubric = (ROOT / "prompts" / "judge_rubric.txt").read_text(encoding="utf-8")

    runs = read_jsonl(DATA / ("pilot.jsonl" if args.pilot else "runs.jsonl"))
    if not runs:
        raise SystemExit("Nu există răspunsuri de evaluat. Rulează întâi run_experiment.py.")
    expected = len(cfg["generators"]) * 4 * 2 * cfg["runs_per_cell"]
    if not args.pilot and not args.force and len(runs) < expected:
        raise SystemExit(f"Generarea nu e completă ({len(runs)}/{expected}). Conform protocolului, "
                         "evaluarea începe după ce toate răspunsurile sunt generate. Vezi scripts/status.py.")

    judges = [j for j in cfg["judges"] if not args.judge or j["model"] == args.judge]
    if not judges:
        raise SystemExit(f"Evaluatorul '{args.judge}' nu e în config.json.")

    for judge in judges:
        out = judge_file(judge["model"], args.pilot)
        done = {r["run_id"] for r in read_jsonl(out)}
        todo = [r for r in runs if r["run_id"] not in done]
        random.Random(f"{cfg['master_seed']}-judge-{judge['model']}").shuffle(todo)
        print(f"Evaluator {judge['model']}: {len(done)} făcute, {len(todo)} rămase -> {out.name}")

        for i, r in enumerate(todo, 1):
            prompt = rubric.replace("{task}", tasks[r["task"]]).replace("{response}", r["text"])
            try:
                res = chat(cfg["base_url"], judge["model"], prompt,
                           temperature=judge["temperature"], max_tokens=judge["max_tokens"],
                           seed=0, timeout=cfg["request_timeout_s"])
            except RuntimeError as e:
                print(f"  [{i}/{len(todo)}] EȘUAT: {e}")
                continue
            score = parse_score(res["text"])
            append_jsonl(out, {
                "run_id": r["run_id"],
                "judge_model": judge["model"],
                "score": score,
                "judge_text": res["text"][:200],
                "finish_reason": res["finish_reason"],
            })
            print(f"  [{i}/{len(todo)}] scor={score}")
    print("Gata.")


if __name__ == "__main__":
    main()
