"""Pregătește evaluarea umană oarbă (opțională).

Creează:
  results/evaluare_umana.csv  — răspunsurile amestecate, fără condiție; completezi coloana „scor” (1–5)
  data/cheie_evaluare.csv     — legătura cod -> rulare. NU o deschide înainte de a termina notarea.

Fișierele se deschid direct în Excel (UTF-8 cu BOM, separator „;”).
"""
import argparse
import csv
import random

from common import DATA, RESULTS, ROOT, load_config, load_json, read_jsonl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0, help="doar un eșantion aleator de N răspunsuri (0 = toate)")
    args = ap.parse_args()
    cfg = load_config()
    tasks = load_json(ROOT / "prompts" / "tasks.json")
    runs = read_jsonl(DATA / "runs.jsonl")
    if not runs:
        raise SystemExit("Nu există răspunsuri. Rulează întâi run_experiment.py.")

    sheet = RESULTS / "evaluare_umana.csv"
    if sheet.exists():
        raise SystemExit(f"{sheet.name} există deja; nu îl suprascriu (ar putea conține note).")

    rows = list(runs)
    random.Random(cfg["master_seed"] + 13).shuffle(rows)
    if args.n:
        rows = rows[: args.n]
    RESULTS.mkdir(exist_ok=True)

    with open(sheet, "w", encoding="utf-8-sig", newline="") as f, \
         open(DATA / "cheie_evaluare.csv", "w", encoding="utf-8-sig", newline="") as k:
        ws = csv.writer(f, delimiter=";")
        wk = csv.writer(k, delimiter=";")
        ws.writerow(["cod", "cerere", "raspuns", "scor"])
        wk.writerow(["cod", "run_id"])
        for i, r in enumerate(rows, 1):
            code = f"R{i:03d}"
            ws.writerow([code, tasks[r["task"]], r["text"], ""])
            wk.writerow([code, r["run_id"]])
    print(f"Creat {sheet.relative_to(ROOT)} ({len(rows)} răspunsuri) și cheia în data/.")


if __name__ == "__main__":
    main()
