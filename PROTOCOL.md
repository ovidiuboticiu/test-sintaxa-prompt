# Protocol preînregistrat — v1

Acest protocol a fost scris și salvat în repozitoriu **înainte** de colectarea datelor experimentului. Singura excepție permisă e rularea pilot (secțiunea 4), folosită doar pentru a verifica funcționarea scripturilor; datele ei nu intră în analiză și sunt păstrate separat, în `data/pilot.jsonl`. Commit-ul care îl conține are eticheta git `preinregistrare-v1`; data etichetei poate fi verificată cu `git show preinregistrare-v1`. Orice abatere de la protocol va fi trecută în secțiunea „Abateri” din raportul final, cu motivul ei.

## 1. Întrebarea

În discuții despre prompturi apare afirmația că anumite „sintaxe” de tip comandă, de exemplu

```
//Dev_Lab_Op_Mode --creative
```

scrise la începutul unei sesiuni noi, controlează comportamentul unui model de limbaj mai bine decât un prompt formulat obișnuit, în cuvinte.

Întrebarea testată: **produce această linie un efect asupra răspunsurilor, și dacă da, efectul vine din forma de comandă sau doar din cuvântul pe care îl conține?**

Testul privește **doar exemplul de mai sus**, așa cum a fost dat public. Nu poate spune nimic despre alte „sintaxe” nepublicate.

## 2. Condiții

Fiecare cerere e trimisă într-o conversație nouă, fără system prompt. Condițiile diferă doar prin prima linie a mesajului:

| Cod | Prima linie | Rolul condiției |
|---|---|---|
| A | *(nimic)* | Referință: cererea simplă |
| B | `//Dev_Lab_Op_Mode --creative` | Sintaxa testată |
| C | `Răspunde cât mai creativ.` | Aceeași intenție, în cuvinte obișnuite |
| D | `//Zq_Rt_Op_Mode --creative` | Placebo: aceeași formă și același cuvânt, dar un „mod” inventat pentru acest test |

Logica: dacă există un „mod” real activat de B, atunci B trebuie să difere de D (care nu activează niciun mod cunoscut). Dacă B și D se comportă la fel, efectul vine din cuvântul „creative”. Dacă B și C se comportă la fel, forma de comandă nu aduce nimic în plus față de limbajul obișnuit.

Textul exact al condițiilor e în `prompts/conditions.json`.

## 3. Sarcini

- **T1 (listă):** „Propune 5 nume pentru o cafenea dintr-un oraș mic din România. Scrie doar lista, câte un nume pe rând.”
- **T2 (text liber):** „Scrie primul paragraf, de cel mult 120 de cuvinte, al unei povești despre un far părăsit.”

Textul exact e în `prompts/tasks.json`.

## 4. Model și setări

- **Model generator:** `gemma-4-e4b-it`, cuantizare Q4_K_M, rulat local în LM Studio, prin API-ul compatibil OpenAI.
- **Parametri de generare:** temperatură 0,8; top_p 0,95; max_tokens 1500. Aceiași la toate rulările.
- **Seed:** fiecare rulare primește un seed propriu, generat determinist din seed-ul principal `20261122`. Seed-ul e salvat lângă fiecare răspuns.
- **Număr de rulări:** 20 pe fiecare combinație condiție × sarcină → 4 × 2 × 20 = **160 de rulări**.
- **Ordinea rulărilor:** toate cele 160 de rulări sunt amestecate aleator (cu seed fix) și executate în acea ordine, ca o eventuală schimbare în timp (încălzirea laptopului, cache) să nu favorizeze o condiție.
- **Pilot:** înainte de experiment se face o rulare de probă (`--pilot`, câte o rulare pe combinație) doar pentru a verifica funcționarea. **Datele pilot nu intră în analiză.**

Setările sunt în `config.json`; toate valorile efectiv folosite sunt salvate cu fiecare rulare.

## 5. Evaluare oarbă

- **Evaluator automat principal:** un model diferit de generator, `qwen3.5-9b` (Q4_K_M), cu temperatură 0.
- Evaluatorul primește **doar** cererea (identică în toate condițiile) și răspunsul. Nu primește prima linie a mesajului, codul condiției sau alte informații.
- Ordinea în care evaluatorul vede răspunsurile e amestecată aleator.
- Scor: originalitate de la 1 la 5, după grila din `prompts/judge_rubric.txt`.
- **Evaluare umană (opțională, secundară):** `make_blind_sheet.py` produce un tabel cu răspunsurile amestecate și fără etichete; cheia e într-un fișier separat, deschis doar după notare.

**Risc de „dezvăluire”:** un răspuns poate menționa singur comanda (de exemplu „Mod creativ activat!”), ceea ce ar putea influența evaluatorul. Răspunsurile **nu** sunt modificate. În schimb, se raportează câte răspunsuri menționează comanda și se face o analiză de sensibilitate fără ele (secțiunea 7).

## 6. Rezultate măsurate

### Primare (stabilite dinainte; doar ele decid verdictul)

- **P1 — diversitatea numelor (T1):** proporția de nume unice din toate numele produse într-o condiție (după normalizare: litere mici, fără diacritice, fără numerotare și punctuație). Mai mare = mai variat.
- **P2 — originalitatea textului (T2):** scorul mediu dat de evaluatorul automat principal.

### Secundare (descriptive; nu decid verdictul)

- Scorul de originalitate al evaluatorului pentru T1.
- Respectarea cerinței la T1: proporția de răspunsuri cu exact 5 nume.
- Lungimea răspunsurilor în cuvinte (ca să vedem dacă o diferență e doar de lungime).
- Diversitatea lexicală la T2 (distinct-2: proporția perechilor de cuvinte unice).
- Numărul de răspunsuri care menționează comanda sau un „mod”.
- Numărul de răspunsuri trunchiate (oprite la limita de tokeni).
- Scorurile evaluatorilor umani, dacă există.

## 7. Analiza statistică

- **Comparații:** B față de A, B față de C, B față de D, pentru fiecare rezultat primar → 6 teste.
- **Test:** test de permutare bilateral, 10.000 de permutări, seed fix. Pentru P1, statistica e diferența de diversitate între condiții; pentru P2, diferența de medii.
- **Corecție pentru comparații multiple:** Holm, aplicată celor 6 teste. Prag: p ajustat < 0,05.
- **Mărimea efectului:** diferența dintre condiții, cu interval de încredere 95% prin bootstrap (5.000 de reeșantionări).
- **Răspunsuri trunchiate:** rămân în analiză; se raportează numărul lor.
- **Sensibilitate:** P2 se recalculează excluzând răspunsurile care menționează comanda.

## 8. Reguli de decizie (simetrice, stabilite dinainte)

Pentru fiecare comparație, rezultatul e unul din trei:
- **B mai bun** — p ajustat < 0,05 și diferența în favoarea lui B;
- **B mai slab** — p ajustat < 0,05 și diferența în defavoarea lui B;
- **Nicio diferență detectată** — p ajustat ≥ 0,05. Asta **nu** înseamnă că efectul e zero, ci că testul nu l-a putut distinge; se raportează intervalul de încredere.

Interpretare:

| Rezultat | Concluzie |
|---|---|
| B mai bun decât C **și** decât D, la cel puțin un rezultat primar, și nu mai slab la celălalt | Afirmația e **susținută** pentru acest model: sintaxa bate atât limbajul obișnuit, cât și placebo-ul. |
| B nu diferă de D, dar diferă de A | Linia are efect, dar efectul vine din cuvântul „creative”, nu dintr-un „mod” activat. |
| B nu diferă de C | Forma de comandă nu aduce nimic în plus față de o instrucțiune în cuvinte. |
| B nu diferă de A | Nu s-a detectat niciun efect al liniei. |
| B mai slab decât A, C sau D | Se raportează la fel de vizibil ca un rezultat favorabil. |

## 9. Limite cunoscute

- Un singur model generator, de mărime mică. Rezultatul nu se generalizează automat la alte modele.
- „Creativitatea” e măsurată indirect: prin varietatea numelor și printr-un evaluator automat, care are propriile preferințe.
- 20 de rulări pe combinație pot detecta doar efecte moderate sau mari. Un efect mic poate trece nedetectat.
- Testul acoperă doar sintaxa dată ca exemplu public.

## Abateri

*(Se completează după experiment, dacă e cazul.)*
