"""Funcții comune: căi, citire/scriere fișiere, apel către API-ul LM Studio."""
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"

# Consola Windows nu afișează mereu corect diacriticele fără asta.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_config():
    return load_json(ROOT / "config.json")


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                # O linie incompletă (oprire bruscă în timpul scrierii) e ignorată; rularea se reface.
                print(f"  ! linia {n} din {path.name} e incompletă și a fost ignorată")
    return rows


def append_jsonl(path, row):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_newline = False
    if path.exists() and path.stat().st_size > 0:
        with open(path, "rb") as f:
            f.seek(-1, 2)
            needs_newline = f.read(1) != b"\n"  # după o oprire bruscă, ultima linie poate fi neterminată
    with open(path, "a", encoding="utf-8") as f:
        if needs_newline:
            f.write("\n")
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()


def build_message(prefix, task_text):
    """Mesajul trimis modelului: prima linie (dacă există), apoi cererea."""
    return f"{prefix}\n\n{task_text}" if prefix else task_text


THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def strip_thinking(text):
    """Elimină raționamentul intern (<think>...</think>), dacă modelul îl pune în text."""
    text = THINK_RE.sub("", text or "")
    # Raționament neînchis (trunchiat): păstrăm doar ce e după el, dacă există.
    if "<think>" in text.lower():
        text = text[: text.lower().index("<think>")]
    return text.strip()


def chat(base_url, model, message, temperature, top_p=None, max_tokens=1500,
         seed=None, timeout=900, retries=3):
    """Trimite o conversație nouă, cu un singur mesaj de utilizator, fără system prompt."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    if top_p is not None:
        payload["top_p"] = top_p
    if seed is not None:
        payload["seed"] = seed
    data = json.dumps(payload).encode("utf-8")
    last_err = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(
            base_url.rstrip("/") + "/chat/completions",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            choice = body["choices"][0]
            raw = choice["message"].get("content") or ""
            return {
                "raw_text": raw,
                "text": strip_thinking(raw),
                "finish_reason": choice.get("finish_reason"),
                "usage": body.get("usage"),
                "model_reported": body.get("model"),
                "latency_s": round(time.time() - t0, 2),
            }
        except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError) as e:
            last_err = e
            print(f"  ! eroare (încercarea {attempt}/{retries}): {e}")
            time.sleep(5 * attempt)
    raise RuntimeError(f"Cererea a eșuat de {retries} ori: {last_err}")


def list_models(base_url):
    with urllib.request.urlopen(base_url.rstrip("/") + "/models", timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return [m.get("id") for m in body.get("data", [])]


def safe_name(model):
    """Numele modelului, sigur pentru fișiere și identificatori."""
    return re.sub(r"[^\w.-]", "_", model)


def normalize(s):
    """Litere mici, fără diacritice, fără punctuație, spații simple."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()
