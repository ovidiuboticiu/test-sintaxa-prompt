"""Evaluare oarbă automată: un alt model notează originalitatea fiecărui răspuns (1–5).

Evaluatorul vede DOAR cererea (identică în toate condițiile) și răspunsul.
Nu vede prima linie a mesajului și nici codul condiției.

Utilizare:
    python scripts/judge.py            # toți evaluatorii din config.json
    python scripts/judge.py --pilot    # evaluează datele pilot (pentru verificare)
"""
import argparse
import random
import re

from common import (DATA, ROOT, append_jsonl, chat, load_config, load_json,
                    read_jsonl)

SCORE_RE = re.compile(r"(?<!\d)([1-5])(?!\d)")


def parse_score(text):
    m = SCORE_RE.search(text or "")
    return int(m.group(1)) if m else None


def safe_name(model):
    return re.sub(r"[^\w.-]", "_", model)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    tasks = load_json(ROOT / "prompts" / "tasks.json")
    rubric = (ROOT / "prompts" / "judge_rubric.txt").read_text(encoding="utf-8")

    runs = read_jsonl(DATA / ("pilot.jsonl" if args.pilot else "runs.jsonl"))
    if not runs:
        raise SystemExit("Nu există răspunsuri de evaluat. Rulează întâi run_experiment.py.")

    for judge in cfg["judges"]:
        out = DATA / f"{'pilot_' if args.pilot else ''}judge_{safe_name(judge['model'])}.jsonl"
        done = {r["run_id"] for r in read_jsonl(out)}
        todo = [r for r in runs if r["run_id"] not in done]
        random.Random(cfg["master_seed"] + 7).shuffle(todo)  # ordine amestecată, fixă
        print(f"Evaluator {judge['model']}: {len(done)} făcute, {len(todo)} rămase -> {out.name}")

        for i, r in enumerate(todo, 1):
            prompt = rubric.replace("{task}", tasks[r["task"]]).replace("{response}", r["text"])
            res = chat(cfg["base_url"], judge["model"], prompt,
                       temperature=judge["temperature"], max_tokens=judge["max_tokens"],
                       seed=0, timeout=cfg["request_timeout_s"])
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
