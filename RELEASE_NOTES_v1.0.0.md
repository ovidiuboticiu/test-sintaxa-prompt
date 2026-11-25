# Versiunea 1.0.0 — 25 noiembrie 2026

Prima versiune publică a experimentului preînregistrat care testează linia de prompt `//Dev_Lab_Op_Mode --creative`.

## Rezultat

Conform regulilor preînregistrate, **afirmația nu este susținută de acest experiment**. Față de lipsa oricărei instrucțiuni, linia a crescut notele de originalitate (+0,45 pe o scală 1–5, la toate cele cinci modele), dar o linie placebo de aceeași formă nu s-a deosebit de ea, iar instrucțiunea obișnuită „Răspunde cât mai creativ.” a dat rezultate mai bune atât la diversitatea numelor, cât și la originalitate.

## Conținut

- Raportul științific: `raport/raport_test_sintaxa_prompt.pdf` (19 pagini, în română).
- Protocolul preînregistrat (`PROTOCOL.md`), fixat la eticheta `preinregistrare-v1` înainte de colectarea datelor.
- Datele complete: 800 de răspunsuri de la cinci modele locale și 1.600 de note ale celor doi evaluatori automați, plus datele pilot.
- Raportul generat automat de analiză, cu abaterile de la protocol (`results/raport.md`).
- Auditul pre-execuție (`AUDIT.md`, `AUDIT_RAPORT.md`, `AUDIT_RASPUNS.md`).
- Codul complet, utilizabil pe Windows, Linux și macOS, cu LM Studio și Python 3.10+.

## Modificări față de preînregistrare

Doar corectura unui defect cosmetic de afișare în `scripts/run_experiment.py`, făcută după încheierea experimentului (vezi README, „Modificări după experiment”). Abaterile din timpul experimentului sunt descrise în secțiunea 7 a raportului.

## Limite

Cinci modele mici (4–8 miliarde de parametri), două sarcini în limba română, creativitate măsurată prin evaluatori automați nevalidați față de evaluatori umani. Cercetare asistată de AI, fără evaluare inter pares umană.
