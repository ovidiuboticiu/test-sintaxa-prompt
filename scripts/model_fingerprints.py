"""Identifică exact fișierele de model folosite (PROTOCOL.md §4): calea în LM Studio și suma SHA-256.

Se rulează o dată, după pilot și înainte de eticheta `preinregistrare-v1`. Scrie MODELE.md.
Calcularea sumelor pentru câteva fișiere de câțiva GB durează câteva minute.

Utilizare (Windows):
    python scripts/model_fingerprints.py --models-dir "D:\\LMStudio\\Models"
"""
import argparse
import hashlib
import re
from pathlib import Path

from common import ROOT, load_config


def key(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8 * 1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models-dir", required=True, help="dosarul de modele din LM Studio")
    args = ap.parse_args()
    base = Path(args.models_dir)
    if not base.is_dir():
        raise SystemExit(f"Dosarul {base} nu există.")

    cfg = load_config()
    wanted = [(g["model"], "generator") for g in cfg["generators"]] + [(j["model"], "evaluator") for j in cfg["judges"]]
    ggufs = [p for p in base.rglob("*.gguf") if "mmproj" not in p.name.lower()]

    rows, problems = [], []
    for model, role in wanted:
        k = key(model.split("/")[-1])
        hits = [p for p in ggufs if k in key(str(p.relative_to(base)))]
        if len(hits) != 1:
            problems.append((model, hits))
            continue
        p = hits[0]
        rel = p.relative_to(base).as_posix()
        print(f"Calculez SHA-256 pentru {rel} ...", flush=True)
        rows.append((model, role, rel, p.stat().st_size, sha256(p)))

    L = ["# Fișierele de model folosite\n",
         "Generat de `scripts/model_fingerprints.py`. Calea e relativă la dosarul de modele din LM Studio; "
         "primele două niveluri indică de obicei sursa (autorul și depozitul de pe Hugging Face).\n",
         "| Model (API) | Rol | Fișier | Mărime (octeți) | SHA-256 |", "|---|---|---|---|---|"]
    L += [f"| `{m}` | {r} | `{rel}` | {size} | `{h}` |" for m, r, rel, size, h in rows]
    if problems:
        L.append("\n## De rezolvat manual\n")
        for m, hits in problems:
            found = ", ".join(f"`{h.relative_to(base).as_posix()}`" for h in hits) or "niciun fișier găsit"
            L.append(f"- `{m}`: {found}")
    (ROOT / "MODELE.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Scris MODELE.md ({len(rows)} identificate, {len(problems)} de rezolvat manual).")


if __name__ == "__main__":
    main()
