# Test: are efect o „sintaxă” de tip comandă într-un prompt?

Un experiment mic, reproductibil, care verifică o afirmație întâlnită în discuții despre prompturi: că o linie de forma

```
//Dev_Lab_Op_Mode --creative
```

scrisă la începutul unei sesiuni noi, schimbă comportamentul unui model de limbaj mai bine decât o instrucțiune obișnuită, în cuvinte.

Experimentul compară patru variante ale aceleiași cereri: fără nimic, cu sintaxa testată, cu aceeași intenție scrisă în cuvinte și cu o sintaxă placebo (aceeași formă, dar un „mod” inventat). Testul se face pe cinci modele mici din familii diferite (Gemma, Qwen, Mistral, Granite, Phi), cu 800 de răspunsuri notate orb de doi evaluatori automați. Detaliile sunt în **[PROTOCOL.md](PROTOCOL.md)**.

## Rezultat

**Afirmația nu e susținută de acest experiment** (regulile preînregistrate din PROTOCOL.md §8). Față de lipsa oricărei instrucțiuni, linia a crescut notele de originalitate ale paragrafelor (+0,45 pe o scală 1–5, la toate cele 5 modele). Față de o linie placebo de aceeași formă, cu un „mod” inventat, nu s-a detectat însă o diferență semnificativă statistic (ceea ce nu dovedește că cele două sunt echivalente), iar instrucțiunea obișnuită „Răspunde cât mai creativ.” a dat rezultate mai bune atât la diversitatea numelor, cât și la originalitate.

- Raportul științific: **[raport/raport_test_sintaxa_prompt.pdf](raport/raport_test_sintaxa_prompt.pdf)** (versiunea 1.0.1, revizuită editorial; vezi `RELEASE_NOTES_v1.0.1.md`)
- Raportul generat automat de analiză, cu abaterile de la protocol: [results/raport.md](results/raport.md)

## Ce testează și ce nu testează

Experimentul verifică dacă linia `//Dev_Lab_Op_Mode --creative`, scrisă la începutul unei conversații, schimbă răspunsurile unor modele care nu au nicio configurare care să o definească, și dacă efectul diferă de cel al unei instrucțiuni obișnuite sau al unei linii placebo de aceeași formă.

Experimentul nu poate verifica dacă linia are o semnificație într-o aplicație anume sau în instrucțiuni personalizate care o definesc. Pentru această sintaxă nu am găsit o documentație publică.

Faptul că un text schimbă răspunsul unui model nu înseamnă că el activează un mod de funcționare diferit. Orice linie adăugată la un prompt poate schimba răspunsul; de aceea experimentul compară sintaxa cu o linie placebo de aceeași formă.

Afirmații despre linii de tip comandă care ar activa „moduri” speciale ale modelelor (de exemplu `/DEV MODE` sau „Developer Mode”) circulă și în comunități online internaționale ([exemplu](https://www.reddit.com/r/ChatGPTPromptGenius/comments/1pg4b1v/)). Ele documentează existența afirmațiilor, nu validitatea lor; de aceea au nevoie de un test controlat.

## De ce „preînregistrat”

Ipotezele, măsurătorile, testele statistice și regulile de interpretare au fost scrise **înainte** de a colecta datele și salvate în commit-ul cu eticheta `preinregistrare-v1`. Asta reduce riscul ca concluziile să fie potrivite după rezultate și face analiza trasabilă. Limită: repozitoriul era privat la momentul preînregistrării și a devenit public după încheierea studiului, așa că eticheta și data release-ului permit inspectarea versiunii declarate, dar nu sunt o dovadă externă, independentă, a cronologiei. Regulile sunt simetrice: un rezultat favorabil și unul nefavorabil sunt tratate cu același prag.

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
| `scripts/run_experiment.py` | Trimite cele 800 de cereri (160 pe model) către LM Studio, în ordine aleatoare fixă |
| `scripts/model_fingerprints.py` | Înregistrează fișierele exacte ale modelelor și sumele SHA-256 în `MODELE.md` |
| `MODELE.md` | Fișierele GGUF folosite (după pilot) |
| `scripts/judge.py` | Evaluarea oarbă automată a originalității |
| `scripts/make_blind_sheet.py` | Tabel pentru evaluare umană oarbă (opțional) |
| `scripts/analyze.py` | Analiza statistică preînregistrată și raportul |
| `scripts/status.py` | Progresul pe sesiuni și următoarea comandă |
| `EVALUARE_UMANA.md` | Instrucțiuni pentru evaluatorii umani (opțional) |
| `AUDIT.md` | Auditul pre-execuție: întrebări și reguli de oprire |
| `AUDIT_RAPORT.md`, `AUDIT_RASPUNS.md` | Raportul auditorului și corecturile făcute |
| `data/` | Datele brute: 800 de răspunsuri, 1.600 de note ale evaluatorilor, datele pilot |
| `results/` | Raportul generat automat de analiză (`raport.md`, `rezumat.json`) |
| `raport/` | Raportul științific (PDF și sursa Markdown) și fișierele de construire |
| `RELEASE_NOTES_v1.0.0.md`, `RELEASE_NOTES_v1.0.1.md` | Ce conține fiecare versiune publică |
| `CITATION.cff`, `LICENSES.md` | Citare și licențe |
| `SHA256SUMS.txt` | Sumele de control ale datelor și ale raportului |

Scripturile folosesc doar biblioteca standard Python (3.10 sau mai nou); nu trebuie instalat nimic în plus.

## Cum reproduci experimentul

1. Instalează [LM Studio](https://lmstudio.ai) și descarcă **exact** fișierele de model din `MODELE.md` (sursa e indicată de cale; poți verifica suma SHA-256).
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
   Apoi înregistrează fișierele de model folosite (doar autorul experimentului, o singură dată):
   ```
   python scripts/model_fingerprints.py --models-dir "D:\LMStudio\Models"
   ```
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

### Linux și macOS

Scripturile folosesc doar biblioteca standard Python și funcționează la fel pe Windows, Linux și macOS. Diferențele țin doar de comenzi:

- LM Studio are versiune pentru Linux (AppImage) și pentru macOS; pașii de mai sus sunt aceiași.
- În loc de `python` se folosește de obicei `python3`.
- Dosarul de modele al LM Studio e de obicei `~/.lmstudio/models` (calea exactă apare în LM Studio, la *My Models*).
- Toate comenzile se rulează din dosarul repozitoriului; căile cu `/` merg pe toate sistemele.

**Alt server decât LM Studio.** Scripturile vorbesc cu orice server compatibil cu API-ul OpenAI (de exemplu Ollama sau `llama-server` din llama.cpp): se schimbă `base_url` și numele modelelor în `config.json`, folosind fișierele din `MODELE.md`. Rezultatul e atunci o **replicare** a experimentului, nu o repetare identică: alt motor de inferență, altă versiune sau alt procesor pot produce alte răspunsuri chiar cu aceleași fișiere de model și aceleași seed-uri. Orice astfel de schimbare trebuie raportată odată cu rezultatele.

### Windows

Dacă `python` nu e recunoscut, folosește `py` în loc. În PowerShell, un clic în fereastră pune rularea pe pauză (QuickEdit); apasă o tastă ca să continue.

## Contribuții și utilizarea AI

Cercetarea a fost realizată de autor, cu asistența unor instrumente AI:

- **Autorul:** întrebarea de cercetare, alegerea designului (condiția placebo, modelele, numărul de rulări), deciziile asupra protocolului, rularea experimentului și interpretarea rezultatelor.
- **Claude (Anthropic):** redactarea protocolului, a documentației și a codului, la cererea și sub controlul autorului. Commit-urile la care a contribuit sunt marcate cu `Co-Authored-By`.
- **Codex (OpenAI):** auditul pre-execuție, descris în `AUDIT.md`.

Modelele de limbaj testate și cele folosite ca evaluatori sunt instrumente de măsurare, nu autori.

## Limite

Modele mici rulate local, o singură sintaxă testată, „creativitatea” măsurată indirect. Lista completă e în PROTOCOL.md, secțiunea 9.

## Modificări după experiment

După încheierea colectării datelor s-a corectat un singur defect, cosmetic: contorul afișat de `scripts/run_experiment.py` la rularea cu `--model` arăta poziția globală raportată la totalul modelului (de exemplu `[161/160]`). Corectura nu schimbă nicio cerere trimisă modelelor și nicio dată. Versiunea exactă folosită în experiment rămâne disponibilă la eticheta `preinregistrare-v1`. Toate abaterile de la protocol sunt descrise în `results/raport.md` și în secțiunea 7 a raportului științific.

## Integritatea fișierelor

`SHA256SUMS.txt` conține sumele SHA-256 ale datelor, rezultatelor și raportului. Verificare:

```
sha256sum -c SHA256SUMS.txt
```

## Cum citezi

Boticiu, O. (2026). *Are o „sintaxă de comandă” vreun efect asupra creativității unui model de limbaj? Un experiment preînregistrat cu linia //Dev_Lab_Op_Mode --creative pe cinci modele locale.* Raport tehnic de cercetare. https://github.com/ovidiuboticiu/test-sintaxa-prompt

Datele de citare sunt și în `CITATION.cff`.

## Licență

Raportul, protocolul, documentația, prompturile și datele sunt publicate sub **CC BY 4.0**, iar codul Python din `scripts/` sub **MIT**. Detaliile sunt în [LICENSES.md](LICENSES.md).
