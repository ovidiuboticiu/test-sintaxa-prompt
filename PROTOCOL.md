# Protocol preînregistrat — v1

Acest protocol a fost scris și salvat în repozitoriu **înainte** de colectarea datelor experimentului. Singura excepție permisă e rularea pilot (secțiunea 4), folosită doar pentru a verifica funcționarea scripturilor; datele ei nu intră în analiză și sunt păstrate separat, în `data/pilot.jsonl`.

Commit-ul care conține versiunea finală a protocolului are eticheta git `preinregistrare-v1`; data ei poate fi verificată cu `git show preinregistrare-v1`. Orice abatere de la protocol va fi trecută în secțiunea „Abateri” din raportul final, cu motivul ei.

## 1. Întrebarea

În discuții despre prompturi apare afirmația că anumite „sintaxe” de tip comandă, de exemplu

```
//Dev_Lab_Op_Mode --creative
```

scrise la începutul unei sesiuni noi, controlează comportamentul unui model de limbaj mai bine decât un prompt formulat obișnuit, în cuvinte.

Întrebarea testată: **produce această linie un efect asupra răspunsurilor, și dacă da, efectul vine din forma de comandă sau doar din cuvântul pe care îl conține?**

Testul privește **doar exemplul de mai sus**, așa cum a fost dat public. Nu poate spune nimic despre alte „sintaxe” nepublicate.

## 2. Context: ce se știe deja

- Modelele de limbaj sunt sensibile la forma promptului, chiar când conținutul e același. Schimbări mici de formatare (separatori, spații, majuscule) au produs diferențe de până la 76 de puncte de acuratețe la LLaMA-2-13B, iar formatul „bun” diferă de la un model la altul (Sclar et al., *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design*, ICLR 2024, arXiv:2310.11324).
- Aceeași cerere scrisă ca text simplu, Markdown, YAML sau JSON a dus la diferențe de până la 40% la GPT-3.5-turbo; modelele mai mari au fost mai stabile (He et al., *Does Prompt Formatting Have Any Impact on LLM Performance?*, arXiv:2411.10541, 2024).
- Instrucțiunile scrise ca pseudo-cod au îmbunătățit performanța la unele sarcini (Mishra et al., *Prompting with Pseudo-Code Instructions*, EMNLP 2023).

Aceste studii reformatează **toată** cererea, păstrând conținutul. Nu am găsit un test al unei linii-comandă de tip „mod” comparată cu un placebo. Consecința pentru acest experiment: o diferență între B și A, luată singură, poate fi doar sensibilitate obișnuită la formă. Doar o diferență între B și placebo-ul D ar indica ceva specific sintaxei testate.

## 3. Condiții

Fiecare cerere e trimisă într-o conversație nouă, fără system prompt. Condițiile diferă doar prin prima linie a mesajului:

| Cod | Prima linie | Rolul condiției |
|---|---|---|
| A | *(nimic)* | Referință: cererea simplă |
| B | `//Dev_Lab_Op_Mode --creative` | Sintaxa testată |
| C | `Răspunde cât mai creativ.` | Aceeași intenție, în cuvinte obișnuite |
| D | `//Zq_Rt_Op_Mode --creative` | Placebo: aceeași formă și același cuvânt, dar un „mod” inventat pentru acest test |

Logica: dacă B activează un „mod” real, B trebuie să difere de D. Dacă B și D se comportă la fel, efectul vine din cuvântul „creative” sau din simpla prezență a unei linii. Dacă B și C se comportă la fel, forma de comandă nu aduce nimic în plus față de limbajul obișnuit.

Textul exact al condițiilor e în `prompts/conditions.json`.

## 4. Sarcini, modele și setări

### Sarcini

- **T1 (listă):** „Propune 5 nume pentru o cafenea dintr-un oraș mic din România. Scrie doar lista, câte un nume pe rând.”
- **T2 (text liber):** „Scrie primul paragraf, de cel mult 120 de cuvinte, al unei povești despre un far părăsit.”

Textul exact e în `prompts/tasks.json`.

### Modele generatoare

Cinci modele mici, din cinci familii diferite, rulate local în LM Studio (cuantizare Q4_K_M), prin API-ul compatibil OpenAI:

| Model | Familie |
|---|---|
| `gemma-4-e4b-it` | Google Gemma |
| `qwen3-4b-instruct-2507` | Alibaba Qwen |
| `ministral-3-8b-instruct-2512` | Mistral |
| `granite-4.1-8b` | IBM Granite |
| `microsoft_phi-4-mini-instruct` | Microsoft Phi |

Modelele cu raționament explicit („reasoning”, „thinking”) au fost excluse: răspunsurile lor lungi ar fi făcut experimentul impracticabil pe un laptop și ar fi adăugat o variabilă în plus.

### Setări

- **Parametri de generare:** temperatură 0,8; top_p 0,95; max_tokens 1500. Aceiași pentru toate modelele și rulările.
- **Rulări:** 20 pe fiecare combinație condiție × sarcină × model → 4 × 2 × 5 × 20 = **800 de rulări**.
- **Seed-uri:** pentru un model, o sarcină și o repetiție date, **toate cele patru condiții primesc același seed**. Astfel singura diferență dintre condiții e prima linie a mesajului. Seed-urile sunt generate determinist din seed-ul principal `20261122` și salvate cu fiecare răspuns.
- **Ordinea:** modelele sunt rulate pe rând, în ordine aleatoare fixă (ca LM Studio să nu reîncarce modelele la fiecare cerere). În interiorul fiecărui model, cele 160 de rulări sunt amestecate aleator, ca o schimbare în timp (încălzirea laptopului, cache) să nu favorizeze o condiție.
- **Sesiuni:** experimentul se poate împărți în mai multe sesiuni de lucru. Generarea se face model cu model, în ordinea fixată de seed: `microsoft_phi-4-mini-instruct`, `ministral-3-8b-instruct-2512`, `granite-4.1-8b`, `gemma-4-e4b-it`, `qwen3-4b-instruct-2507`. Evaluarea începe numai după ce toate cele 800 de răspunsuri sunt generate. Un răspuns e salvat doar după ce s-a terminat complet, deci o întrerupere nu lasă date parțiale; rularea continuă de unde a rămas. Data și ora fiecărui răspuns sunt salvate, deci împărțirea pe sesiuni e vizibilă în date.
- **Pilot:** înainte de experiment se face o rulare de probă (`--pilot`, câte o rulare pe combinație, cu alte seed-uri) doar pentru a verifica funcționarea. **Datele pilot nu intră în analiză.** Pilotul poate duce doar la corecturi tehnice (nume de modele, extragerea numelor, setări ale evaluatorilor), făcute **înainte** de eticheta `preinregistrare-v1`.

Setările sunt în `config.json`; valorile efectiv folosite sunt salvate cu fiecare rulare.

## 5. Evaluare oarbă

- **Evaluatori automați:** două modele diferite de toate modelele generatoare, din familii diferite: `qwen3.5-9b` și `gemma-4-12b-it` (Q4_K_M), cu temperatură 0.
- Evaluatorul primește **doar** cererea (identică în toate condițiile) și răspunsul. Nu primește prima linie a mesajului, condiția sau modelul care a generat răspunsul.
- Fiecare evaluator vede răspunsurile într-o ordine aleatoare proprie.
- Scor: originalitate de la 1 la 5, după grila din `prompts/judge_rubric.txt`.
- **Scorul folosit în analiza principală** e media celor doi evaluatori. Dacă un evaluator nu dă un scor valid, se folosește scorul celuilalt; numărul acestor cazuri se raportează.
- Fiecare evaluator face parte din aceeași familie cu unul dintre generatoare (Qwen, Gemma), ceea ce poate crea o preferință pentru „propriile” texte. Media celor doi și analiza de sensibilitate pe fiecare evaluator separat (secțiunea 7) arată dacă asta schimbă concluzia. Preferința ar afecta oricum în mod egal toate cele patru condiții ale aceluiași model.
- Dacă la pilot un evaluator produce raționament intern foarte lung, raționamentul se dezactivează din setările LM Studio înainte de etichetă, iar decizia se notează în „Abateri”.
- **Evaluare umană (opțională, secundară):** `make_blind_sheet.py` produce un tabel cu răspunsuri amestecate și fără etichete (toate sau un eșantion aleator); cheia e într-un fișier separat, deschis doar după notare.

**Risc de „dezvăluire”:** un răspuns poate menționa singur comanda (de exemplu „Mod creativ activat!”), ceea ce ar putea influența evaluatorul. Răspunsurile **nu** sunt modificate. Se raportează câte răspunsuri menționează comanda și se face o analiză de sensibilitate fără ele. La T1, liniile de acest tip nu sunt numărate ca nume.

## 6. Rezultate măsurate

### Primare (stabilite dinainte; doar ele decid verdictul)

- **P1 — diversitatea numelor (T1):** proporția de nume unice din toate numele produse de un model într-o condiție (după normalizare: litere mici, fără diacritice, fără numerotare și punctuație). Mai mare = mai variat.
- **P2 — originalitatea textului (T2):** scorul mediu dat de evaluatori.

### Secundare (descriptive; nu decid verdictul)

- Rezultatele pe fiecare model în parte.
- La câte modele diferența a fost în favoarea lui B.
- Scorul de originalitate pentru T1.
- Respectarea cerinței la T1: proporția de răspunsuri cu exact 5 nume.
- Lungimea răspunsurilor în cuvinte (ca să vedem dacă o diferență e doar de lungime).
- Diversitatea lexicală la T2 (distinct-2: proporția perechilor de cuvinte unice).
- Acordul dintre cei doi evaluatori.
- Numărul de răspunsuri care menționează comanda și numărul de răspunsuri trunchiate.
- Scorurile evaluatorilor umani, dacă există.

## 7. Analiza statistică

- **Analiza principală combină cele cinci modele.** Pentru fiecare comparație se calculează diferența dintre condiții în interiorul fiecărui model, apoi media acestor diferențe peste modele.
- **Comparații:** B față de A, B față de C, B față de D, pentru fiecare rezultat primar → 6 teste.
- **Test:** test de permutare bilateral, **stratificat pe model** (etichetele condițiilor se amestecă doar între răspunsurile aceluiași model), 10.000 de permutări, seed fix.
- **Corecție pentru comparații multiple:** Holm, pe cele 6 teste. Prag: p ajustat < 0,05.
- **Mărimea efectului:** diferența medie, cu interval de încredere 95% prin bootstrap stratificat (5.000 de reeșantionări).
- **Pe fiecare model (secundar):** aceleași 6 teste, cu corecție Holm separată pentru fiecare model.
- **Răspunsuri trunchiate sau eșuate:** rămân în analiză cele trunchiate; cererile eșuate de 3 ori lipsesc. Ambele numere se raportează.
- **Sensibilitate (P2, necorectată):** fără răspunsurile care menționează comanda; doar cu primul evaluator; doar cu al doilea evaluator.

## 8. Reguli de decizie (simetrice, stabilite dinainte)

Pentru fiecare comparație din analiza principală, rezultatul e unul din trei:
- **B mai bun** — p ajustat < 0,05 și diferența în favoarea lui B;
- **B mai slab** — p ajustat < 0,05 și diferența în defavoarea lui B;
- **Nicio diferență detectată** — p ajustat ≥ 0,05. Asta **nu** înseamnă că efectul e zero, ci că testul nu l-a putut distinge; se raportează intervalul de încredere.

Interpretare:

| Rezultat | Concluzie |
|---|---|
| B mai bun decât C **și** decât D, la cel puțin un rezultat primar, și nu mai slab la niciuna dintre comparații | Afirmația e **susținută** pentru acest set de modele: sintaxa bate atât limbajul obișnuit, cât și placebo-ul. |
| B mai bun decât A, dar nu decât D | Linia are efect, dar efectul vine din cuvântul „creative” sau din prezența unei linii, nu dintr-un „mod” activat. |
| B nu diferă de C | Forma de comandă nu aduce nimic în plus față de o instrucțiune în cuvinte. |
| B nu diferă de A | Nu s-a detectat niciun efect al liniei. |
| B mai slab decât A, C sau D | Se raportează la fel de vizibil ca un rezultat favorabil. |

Orice concluzie se însoțește de numărul de modele la care diferența a mers în aceeași direcție, ca să se vadă dacă un rezultat combinat vine de la toate modelele sau doar de la unul-două.

## 9. Limite cunoscute

- Cinci modele mici (4–8 miliarde de parametri), rulate local. Literatura (secțiunea 2) arată că efectele de formă diferă de la un model la altul, deci rezultatul nu se transferă automat la modele mari sau la servicii online.
- „Creativitatea” e măsurată indirect: prin varietatea numelor și prin evaluatori automați, care au propriile preferințe.
- Sarcinile sunt în limba română; unele modele mici o stăpânesc mai slab. Comparațiile se fac însă în interiorul aceluiași model, deci asta afectează toate condițiile la fel.
- 20 de rulări pe combinație și model pot detecta, pe un model luat separat, doar efecte moderate sau mari. Analiza combinată are mai multă putere.
- Testul acoperă doar sintaxa dată ca exemplu public.

## Abateri

*(Se completează după experiment, dacă e cazul.)*
