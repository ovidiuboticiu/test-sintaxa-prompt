# Raport — testul sintaxei de prompt

Rulări reușite: 800; eșuate definitiv: 0. Modele generatoare: `gemma-4-e4b-it`, `qwen3-4b-instruct-2507`, `ministral-3-8b-instruct-2512`, `granite-4.1-8b`, `microsoft_phi-4-mini-instruct`. Evaluatori: `qwen3.5-9b`, `gemma-4-12b-it`.

## Descriere pe model și condiție

| Model | Cond. | T1 diversitate nume | T1 exact 5 nume | T1 scor | T2 scor | T2 distinct-2 | Cuvinte T2 | Menționează comanda | Trunchiate | Eșuate |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma-4-e4b-it | A | 0.930 | 20/20 | 3.05 | 3.20 | 0.800 | 107.9 | 0 | 0 | 0 |
| gemma-4-e4b-it | B | 0.940 | 20/20 | 3.35 | 3.40 | 0.802 | 98.5 | 0 | 0 | 0 |
| gemma-4-e4b-it | C | 0.970 | 20/20 | 3.92 | 3.80 | 0.828 | 104.3 | 0 | 0 | 0 |
| gemma-4-e4b-it | D | 0.960 | 20/20 | 3.10 | 3.35 | 0.798 | 98.3 | 0 | 0 | 0 |
| qwen3-4b-instruct-2507 | A | 0.880 | 20/20 | 3.73 | 3.40 | 0.737 | 120.5 | 0 | 0 | 0 |
| qwen3-4b-instruct-2507 | B | 0.850 | 20/20 | 3.42 | 3.88 | 0.736 | 112.0 | 0 | 0 | 0 |
| qwen3-4b-instruct-2507 | C | 0.930 | 20/20 | 3.75 | 4.12 | 0.743 | 122.2 | 0 | 0 | 0 |
| qwen3-4b-instruct-2507 | D | 0.910 | 20/20 | 3.30 | 3.83 | 0.745 | 114.8 | 0 | 0 | 0 |
| ministral-3-8b-instruct-2512 | A | 0.980 | 20/20 | 3.35 | 3.17 | 0.826 | 125.5 | 0 | 0 | 0 |
| ministral-3-8b-instruct-2512 | B | 0.990 | 20/20 | 3.38 | 3.58 | 0.835 | 141.7 | 0 | 0 | 0 |
| ministral-3-8b-instruct-2512 | C | 1.000 | 20/20 | 3.80 | 4.03 | 0.834 | 146.7 | 0 | 0 | 0 |
| ministral-3-8b-instruct-2512 | D | 1.000 | 20/20 | 3.27 | 3.62 | 0.831 | 137.1 | 0 | 0 | 0 |
| granite-4.1-8b | A | 0.950 | 20/20 | 3.30 | 2.33 | 0.826 | 82.6 | 0 | 0 | 0 |
| granite-4.1-8b | B | 0.900 | 20/20 | 2.83 | 2.52 | 0.820 | 107.3 | 0 | 0 | 0 |
| granite-4.1-8b | C | 0.980 | 20/20 | 3.52 | 2.38 | 0.846 | 97.1 | 0 | 0 | 0 |
| granite-4.1-8b | D | 0.970 | 20/20 | 3.30 | 2.23 | 0.836 | 85.7 | 0 | 0 | 0 |
| microsoft_phi-4-mini-instruct | A | 0.952 | 19/20 | 2.12 | 1.20 | 0.584 | 584.1 | 0 | 9 | 0 |
| microsoft_phi-4-mini-instruct | B | 1.000 | 14/20 | 2.90 | 2.15 | 0.791 | 256.8 | 0 | 1 | 0 |
| microsoft_phi-4-mini-instruct | C | 1.000 | 19/20 | 3.38 | 2.48 | 0.777 | 283.8 | 0 | 0 | 0 |
| microsoft_phi-4-mini-instruct | D | 0.983 | 16/20 | 3.00 | 1.93 | 0.718 | 297.5 | 0 | 1 | 0 |

## Raționament intern (secundar)

Proporția răspunsurilor cu raționament / tokeni medii de raționament, pe ambele sarcini.

| Model | A | B | C | D |
|---|---|---|---|---|
| gemma-4-e4b-it | 29/40 · 351 | 39/40 · 534 | 40/40 · 562 | 39/40 · 547 |
| qwen3-4b-instruct-2507 | 0/40 · 0 | 0/40 · 0 | 0/40 · 0 | 0/40 · 0 |
| ministral-3-8b-instruct-2512 | 0/40 · 0 | 0/40 · 0 | 0/40 · 0 | 0/40 · 0 |
| granite-4.1-8b | 0/40 · 0 | 0/40 · 0 | 0/40 · 0 | 0/40 · 0 |
| microsoft_phi-4-mini-instruct | 0/40 · 0 | 0/40 · 0 | 0/40 · 0 | 0/40 · 0 |

## Scorurile evaluatorilor

- `qwen3.5-9b`: 800 valide, 0 invalide, 0 eșuate.
- `gemma-4-12b-it`: 800 valide, 0 invalide, 0 eșuate.
- Răspunsuri cu ambele scoruri valide: 800; cu un singur scor valid: 0; fără niciun scor valid: 0.
- Acordul evaluatorilor: corelație Pearson 0.48, acord exact 50%.

## Rezultate primare — toate modelele combinate

Comparații pe perechi (același model, aceeași sarcină, aceeași repetiție). Diferența e media, peste modele, a diferenței din fiecare model. Test de permutare pe perechi, stratificat pe model; corecție Holm pe cele 6 teste. Pentru P1 nu se raportează interval de încredere (PROTOCOL.md §7).

| Rezultat | Comparație | Diferență | IÎ 95% | p | p Holm | Perechi incomplete | Verdict |
|---|---|---|---|---|---|---|---|
| P1 diversitate nume (T1) | B vs A | -0.002 | — | 0.8566 | 0.8566 | 0 | nicio diferență detectată |
| P1 diversitate nume (T1) | B vs C | -0.040 | — | 0.0001 | 0.0006 | 0 | B mai slab |
| P1 diversitate nume (T1) | B vs D | -0.029 | — | 0.0276 | 0.0828 | 0 | nicio diferență detectată |
| P2 originalitate (T2) | B vs A | 0.445 | [0.325, 0.565] | 0.0001 | 0.0006 | 0 | B mai bun |
| P2 originalitate (T2) | B vs C | -0.255 | [-0.385, -0.120] | 0.0008 | 0.0032 | 0 | B mai slab |
| P2 originalitate (T2) | B vs D | 0.115 | [-0.015, 0.245] | 0.1120 | 0.2240 | 0 | nicio diferență detectată |

## Concluzie (reguli preînregistrate, PROTOCOL.md §8)

- **Afirmația nu e susținută de acest experiment.** Criteriul (B mai bun decât C și decât D la același rezultat primar, fără a fi mai slab la vreo comparație) nu a fost îndeplinit.
- **B a ieșit mai slab** la: P1 (B vs C), P2 (B vs C).
- P1 (diversitatea numelor): față de A — nicio diferență detectată; față de C — B mai slab; față de D — nicio diferență detectată.
- P2 (originalitatea textului): față de A — B mai bun; față de C — B mai slab; față de D — nicio diferență detectată.
- Consecvență între modele (diferență în favoarea lui B, indiferent de semnificație): P1 B vs A: 3 din 5; P1 B vs C: 0 din 5; P1 B vs D: 1 din 5; P2 B vs A: 5 din 5; P2 B vs C: 1 din 5; P2 B vs D: 4 din 5.
- O diferență nedetectată nu dovedește că efectul e zero sau că două condiții sunt echivalente; datele nu permit atribuirea unui mecanism (cuvânt, formă, „mod”).

## Rezultate pe fiecare model (secundar, descriptiv)

Corecție Holm separată pentru cele 6 teste ale fiecărui model.

| Model | Rezultat | B vs A | B vs C | B vs D |
|---|---|---|---|---|
| gemma-4-e4b-it | P1 | 0.010 (p Holm 1.000) | -0.030 (p Holm 1.000) | -0.020 (p Holm 1.000) |
| gemma-4-e4b-it | P2 | 0.200 (p Holm 0.776) | -0.400 (p Holm 0.100) | 0.050 (p Holm 1.000) |
| qwen3-4b-instruct-2507 | P1 | -0.030 (p Holm 1.000) | -0.080 (p Holm 0.026) | -0.060 (p Holm 0.505) |
| qwen3-4b-instruct-2507 | P2 | 0.475 (p Holm 0.002) | -0.250 (p Holm 0.126) | 0.050 (p Holm 1.000) |
| ministral-3-8b-instruct-2512 | P1 | 0.010 (p Holm 1.000) | -0.010 (p Holm 1.000) | -0.010 (p Holm 1.000) |
| ministral-3-8b-instruct-2512 | P2 | 0.400 (p Holm 0.052) | -0.450 (p Holm 0.004) | -0.050 (p Holm 1.000) |
| granite-4.1-8b | P1 | -0.050 (p Holm 0.901) | -0.080 (p Holm 0.022) | -0.070 (p Holm 0.274) |
| granite-4.1-8b | P2 | 0.200 (p Holm 0.901) | 0.150 (p Holm 0.901) | 0.300 (p Holm 0.901) |
| microsoft_phi-4-mini-instruct | P1 | 0.048 (p Holm 0.027) | 0.000 (p Holm 1.000) | 0.017 (p Holm 0.828) |
| microsoft_phi-4-mini-instruct | P2 | 0.950 (p Holm 0.003) | -0.325 (p Holm 0.828) | 0.225 (p Holm 0.828) |

## Analize de sensibilitate (P2)

| Variantă | B vs A | B vs C | B vs D |
|---|---|---|---|
| Fără răspunsurile care menționează comanda | 0.445 (p 0.000) | -0.255 (p 0.001) | 0.115 (p 0.109) |
| Doar evaluatorul `qwen3.5-9b` | 0.260 (p 0.002) | -0.050 (p 0.619) | 0.170 (p 0.019) |
| Doar evaluatorul `gemma-4-12b-it` | 0.630 (p 0.000) | -0.460 (p 0.000) | 0.060 (p 0.613) |
| Tokeni de raționament (T1) | 66.8 (p 0.001) | -18.1 (p 0.014) | -2.5 (p 0.531) |
| Tokeni de raționament (T2) | 6.2 (p 0.065) | 6.8 (p 0.356) | -2.7 (p 0.421) |

Valorile p din această secțiune nu sunt corectate și nu decid verdictul.

## Abateri de la protocol

1. **Evaluarea s-a făcut cu o versiune mai veche a `scripts/judge.py`.** Pe calculatorul pe care s-a rulat experimentul, `judge.py` nu conținea verificarea din versiunea preînregistrată care oprește evaluarea dacă evaluatorul produce raționament intern (commit 7b2d5c5). Fișierele de evaluare nu înregistrează tokenii de raționament ai evaluatorilor, deci absența raționamentului nu poate fi dovedită direct. Indicii indirecte: toate cele 1.600 de scoruri sunt o singură cifră, toate cu `finish_reason = stop` (în pilot, raționamentul evaluatorului ducea la trunchiere și la scor gol), iar opțiunea „Enable Thinking” a fost verificată ca dezactivată în LM Studio pentru ambii evaluatori înainte de rulare. Restul codului de evaluare (rubrica, parametrii, parsarea scorului) este identic cu versiunea preînregistrată.
2. **Analiza a fost rulată inițial cu o versiune incompletă a `scripts/analyze.py`**, căreia îi lipsea secțiunea secundară despre raționamentul intern. Acest raport provine din versiunea preînregistrată (`preinregistrare-v1`), rulată pe aceleași date; toate rezultatele primare și verdictul sunt identice cifră cu cifră între cele două rulări.
3. Fișierele care produc datele (`run_experiment.py`, `common.py`, `config.json`, `prompts/`) au fost verificate ca identice cu versiunea preînregistrată.
4. La evaluatorul `gemma-4-12b-it`, opțiunea „Enable Thinking” nu se păstra la reîncărcarea modelului; a fost dezactivată manual după încărcare. Modelul a rulat cu 4 sloturi paralele (`Parallel 4`); cererile au fost trimise strict secvențial, câte una.
5. Generarea s-a făcut în cinci sesiuni, câte una pe model, între 22 și 24 noiembrie 2026, fără modificarea setărilor LM Studio în timpul unei sesiuni.
6. Defect cosmetic de afișare în `run_experiment.py` cu `--model`: contorul arăta poziția globală raportată la totalul modelului (de ex. `[161/160]`). Nu afectează datele; a fost lăsat necorectat în timpul experimentului.
