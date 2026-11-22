# Test: are efect o „sintaxă” de tip comandă într-un prompt?

Un experiment mic, reproductibil, care verifică o afirmație întâlnită în discuții despre prompturi: că o linie de forma

```
//Dev_Lab_Op_Mode --creative
```

scrisă la începutul unei sesiuni noi, schimbă comportamentul unui model de limbaj mai bine decât o instrucțiune obișnuită, în cuvinte.

Experimentul compară patru variante ale aceleiași cereri: fără nimic, cu sintaxa testată, cu aceeași intenție scrisă în cuvinte și cu o sintaxă placebo (aceeași formă, dar un „mod” inventat). Testul se face pe cinci modele mici din familii diferite (Gemma, Qwen, Mistral, Granite, Phi), cu 800 de răspunsuri notate orb de doi evaluatori automați. Detaliile sunt în **[PROTOCOL.md](PROTOCOL.md)**.

## De ce „preînregistrat”

Ipotezele, măsurătorile, testele statistice și regulile de interpretare au fost scrise **înainte** de a colecta datele și salvate în commit-ul cu eticheta `preinregistrare-v1`. Astfel, nimeni (nici autorul) nu poate potrivi concluziile după rezultate. Regulile sunt simetrice: un rezultat favorabil și unul nefavorabil sunt tratate cu același prag.

Verificare:

```
git show preinregistrare-v1 --stat
```

## Ce conține

| Cale | Conținut |
|---|---|
| `PROTOCOL.md` | Protocolul preînregistrat |
| `config.json` | Modelele și parametrii folosiți |
| `prompts/` | Textul exact al condițiilor, al sarcinilor și grila evaluatorului |
| `scripts/run_experiment.py` | Trimite cele 160 de cereri către LM Studio, în ordine aleatoare fixă |
| `scripts/judge.py` | Evaluarea oarbă automată a originalității |
| `scripts/make_blind_sheet.py` | Tabel pentru evaluare umană oarbă (opțional) |
| `scripts/analyze.py` | Analiza statistică preînregistrată și raportul |
| `scripts/status.py` | Progresul pe sesiuni și următoarea comandă |
| `EVALUARE_UMANA.md` | Instrucțiuni pentru evaluatorii umani (opțional) |
| `data/` | Datele brute (după experiment) |
| `results/` | Raportul final (după experiment) |

Scripturile folosesc doar biblioteca standard Python (3.9+); nu trebuie instalat nimic în plus.

## Cum reproduci experimentul

1. Instalează [LM Studio](https://lmstudio.ai) și descarcă modelele din `config.json`.
2. În LM Studio: **Developer → Start Server** (adresa implicită `http://localhost:1234`).
3. Verifică planul, fără să trimiți nimic:
   ```
   python scripts/run_experiment.py --dry-run
   ```
4. Rulare de probă (nu intră în analiză):
   ```
   python scripts/run_experiment.py --pilot
   python scripts/judge.py --pilot
   python scripts/analyze.py --pilot
   ```
   Deschide `results/raport_pilot.md` și verifică dacă numele din T1 au fost extrase corect.
5. Experimentul propriu-zis (dacă se întrerupe, comanda reluată continuă de unde a rămas):
   ```
   python scripts/run_experiment.py
   python scripts/judge.py
   python scripts/analyze.py
   ```
6. Rezultatul e în `results/raport.md`.

### Rulare pe sesiuni

Pe un laptop fără placă video dedicată, cele 800 de generări și cele 1.600 de evaluări pot dura între 10 și 15 ore. Nu trebuie făcute dintr-o dată. La începutul fiecărei sesiuni rulezi:

```
python scripts/status.py
```

Scriptul arată ce s-a terminat, cât a mai rămas (estimat din timpii de până atunci) și **comanda exactă de rulat în continuare**. O sesiune tipică acoperă un model generator (aprox. 1,5–3 ore) sau o parte dintr-un evaluator. Ordinea:

| Sesiune | Comandă |
|---|---|
| 1 | `python scripts/run_experiment.py --model microsoft_phi-4-mini-instruct` |
| 2 | `python scripts/run_experiment.py --model ministral-3-8b-instruct-2512` |
| 3 | `python scripts/run_experiment.py --model granite-4.1-8b` |
| 4 | `python scripts/run_experiment.py --model gemma-4-e4b-it` |
| 5 | `python scripts/run_experiment.py --model qwen3-4b-instruct-2507` |
| 6–7 | `python scripts/judge.py --judge qwen3.5-9b` |
| 8–9 | `python scripts/judge.py --judge gemma-4-12b-it` |
| final | `python scripts/analyze.py` |

Poți opri oricând cu **Ctrl+C**. Răspunsul aflat în lucru se pierde, iar la repornire se reface; tot ce era gata rămâne salvat.

Pe Windows, dacă `python` nu e recunoscut, folosește `py` în loc. În PowerShell, un clic în fereastră pune rularea pe pauză (QuickEdit); apasă o tastă ca să continue.

## Limite

Modele mici rulate local, o singură sintaxă testată, „creativitatea” măsurată indirect. Lista completă e în PROTOCOL.md, secțiunea 9.
