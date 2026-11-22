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

**Domeniul testului:** efectul liniei asupra unor modele care nu au nicio configurare care să o definească (fără system prompt, fără instrucțiuni personalizate, fără o aplicație care să o interpreteze). Testul nu poate exclude ca linia să aibă o semnificație într-o aplicație anume sau în instrucțiuni personalizate care o definesc.

## 2. Context: ce se știe deja

- Modelele de limbaj sunt sensibile la forma promptului, chiar când conținutul e același. Schimbări mici de formatare (separatori, spații, majuscule) au produs diferențe de până la 76 de puncte de acuratețe la LLaMA-2-13B, iar formatul „bun” diferă de la un model la altul (Sclar et al., *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design*, ICLR 2024, arXiv:2310.11324).
- Aceeași cerere scrisă ca text simplu, Markdown, YAML sau JSON a dus la diferențe de până la 40% la GPT-3.5-turbo; modelele mai mari au fost mai stabile (He et al., *Does Prompt Formatting Have Any Impact on LLM Performance?*, arXiv:2411.10541, 2024).
- Instrucțiunile scrise ca pseudo-cod au îmbunătățit performanța la unele sarcini (Mishra et al., *Prompting with Pseudo-Code Instructions*, EMNLP 2023).

Pentru sintaxa testată nu am găsit o documentație publică. Afirmații despre linii de tip comandă care ar activa „moduri” speciale circulă însă în comunități online; ele documentează existența afirmațiilor, nu validitatea lor.

Studiile de mai sus reformatează **toată** cererea, păstrând conținutul. Nu am găsit un test al unei linii-comandă de tip „mod” comparată cu un placebo. Consecința pentru acest experiment: o diferență între B și A, luată singură, poate fi doar sensibilitate obișnuită la formă. Doar o diferență între B și placebo-ul D ar indica ceva specific sintaxei testate.

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

- **Identificarea exactă a modelelor:** după pilot și înainte de etichetă, `scripts/model_fingerprints.py` înregistrează în `MODELE.md`, pentru fiecare model generator și evaluator, fișierul GGUF folosit (calea din LM Studio, care indică sursa) și suma lui SHA-256.
- **Rulări eșuate:** o cerere care eșuează de 3 ori consecutiv, cu serverul pornit, e înregistrată ca **eșuată definitiv** și nu se mai reîncearcă la reluare. Dacă serverul nu răspunde, scriptul se oprește fără să marcheze eșecuri. Evaluarea pornește doar când toate cele 800 de rulări sunt încheiate (reușite sau eșuate definitiv) și se aplică doar celor reușite.

## 5. Evaluare oarbă

- **Evaluatori automați:** două modele diferite de toate modelele generatoare, din familii diferite: `qwen3.5-9b` și `gemma-4-12b-it` (Q4_K_M), cu temperatură 0.
- Evaluatorul primește **doar** cererea (identică în toate condițiile) și răspunsul. Nu primește prima linie a mesajului, condiția sau modelul care a generat răspunsul.
- Fiecare evaluator vede răspunsurile într-o ordine aleatoare proprie.
- Scor: originalitate de la 1 la 5, după grila din `prompts/judge_rubric.txt`. **E valid doar un răspuns format dintr-o singură cifră între 1 și 5** (eventual urmată de punct), după eliminarea spațiilor și a raționamentului intern. Orice alt răspuns e înregistrat ca **invalid** și nu se reîncearcă.
- **Scorul folosit în analiza principală** e media celor doi evaluatori. Dacă un evaluator nu dă un scor valid, se folosește scorul celuilalt; numărul acestor cazuri se raportează.
- Fiecare evaluator face parte din aceeași familie cu unul dintre generatoare (Qwen, Gemma), ceea ce poate crea o preferință pentru „propriile” texte. Media celor doi și analiza de sensibilitate pe fiecare evaluator separat (secțiunea 7) arată dacă asta schimbă concluzia. Preferința ar afecta oricum în mod egal toate cele patru condiții ale aceluiași model.
- Dacă la pilot un evaluator produce raționament intern foarte lung, raționamentul se dezactivează din setările LM Studio înainte de etichetă, iar decizia se notează în „Abateri”.
- **Evaluare umană:** nu face parte din această versiune a experimentului. Autorul cunoaște ipotezele și nu are la dispoziție evaluatori independenți. Datele brute sunt publice, iar `make_blind_sheet.py` și `EVALUARE_UMANA.md` permit oricui o evaluare umană oarbă ulterioară, raportată separat.

**Risc de „dezvăluire”:** un răspuns poate menționa singur comanda (de exemplu „Mod creativ activat!”), ceea ce ar putea influența evaluatorul. Răspunsurile **nu** sunt modificate. Se raportează câte răspunsuri menționează comanda și se face o analiză de sensibilitate fără ele. La T1, liniile de acest tip nu sunt numărate ca nume.

## 6. Rezultate măsurate

### Primare (stabilite dinainte; doar ele decid verdictul)

- **P1 — diversitatea numelor (T1):** proporția de nume unice din toate numele produse de un model într-o condiție (după normalizare: litere mici, fără diacritice, fără numerotare și punctuație). Mai mare = mai variat. **Extragerea numelor:** (1) se ignoră liniile care menționează comanda sau un „mod activat”; (2) dacă răspunsul conține linii numerotate sau cu buline, se folosesc **doar** acestea; (3) altfel se folosesc toate liniile, mai puțin cele terminate în „:”, „!” sau „?” (formule introductive); (4) dintr-o linie se păstrează doar partea dinaintea unei descrieri („ – …”, „: …”, „(…)”); liniile mai lungi de 8 cuvinte sau 60 de caractere nu sunt nume.
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

## 7. Analiza statistică

- **Perechi.** O pereche e formată din două răspunsuri ale aceluiași model, la aceeași sarcină și aceeași repetiție (deci cu același seed), în două condiții diferite. Toate comparațiile se fac pe perechi.
- **Perechi incomplete.** O pereche intră în analiză doar dacă ambele răspunsuri există și au valoarea necesară (pentru P2: cel puțin un scor valid fiecare). Numărul perechilor excluse se raportează pentru fiecare comparație.
- **Analiza principală combină cele cinci modele.** Pentru fiecare comparație se calculează diferența dintre condiții în fiecare model, apoi media acestor diferențe peste modele.
- **Comparații:** B față de A, B față de C, B față de D, pentru fiecare rezultat primar → 6 teste.
- **Test:** test de permutare bilateral **pe perechi**: în fiecare pereche, cele două etichete se schimbă între ele cu probabilitatea 1/2, independent, în toate modelele; statistica se recalculează integral. 10.000 de permutări, seed fix. O permutare la care statistica nu e definită se numără ca extremă (conservator).
- **Corecție pentru comparații multiple:** Holm, pe cele 6 teste. Prag: p ajustat < 0,05.
- **Mărimea efectului:** diferența medie. Pentru P2 se raportează și intervalul de încredere 95% prin bootstrap pe perechi (5.000 de reeșantionări, în fiecare model). **Pentru P1 nu se raportează interval de încredere**: reeșantionarea duplică liste întregi și ar subestima sistematic diversitatea.
- **Contraste neestimabile.** O comparație e **neestimabilă** dacă vreun model nu are nicio pereche completă sau dacă statistica nu e definită (de exemplu, nicio listă de nume extrasă într-o condiție). O comparație neestimabilă nu primește verdict direcțional; dacă oricare din cele 6 comparații e neestimabilă sau lipsește un model, **verdictul global se suspendă**.
- **Rulări eșuate definitiv:** lipsesc din analiză; numărul lor se raportează pe model și condiție.
- **Pe fiecare model (secundar):** aceleași 6 teste, cu corecție Holm separată pentru fiecare model.
- **Sensibilitate (P2, necorectată):** fără perechile în care vreun răspuns menționează comanda; doar cu primul evaluator; doar cu al doilea evaluator.

## 8. Reguli de decizie (simetrice, stabilite dinainte)

Pentru fiecare comparație din analiza principală, rezultatul e unul din patru:
- **B mai bun** — p ajustat < 0,05 și diferența în favoarea lui B;
- **B mai slab** — p ajustat < 0,05 și diferența în defavoarea lui B;
- **Nicio diferență detectată** — p ajustat ≥ 0,05;
- **Neestimabil** — vezi §7.

Verdictul global:

| Situație | Verdict |
|---|---|
| Vreo comparație e neestimabilă sau lipsește un model | **Suspendat.** |
| La **același** rezultat primar, B e mai bun decât C **și** decât D, iar B nu e mai slab la niciuna dintre cele 6 comparații | Afirmația e **susținută** pentru acest set de modele. |
| Orice altă situație | Afirmația **nu e susținută** de acest experiment. |

Pe lângă verdict, raportul enumeră, separat pentru P1 și P2, rezultatul fiecărei comparații (față de A, C și D), orice rezultat „B mai slab” la fel de vizibil ca unul favorabil, și la câte modele diferența a mers în favoarea lui B.

Limitele interpretării:
- „Nicio diferență detectată” **nu** înseamnă că efectul e zero sau că două condiții sunt echivalente; poate fi și o diferență reală pe care testul nu a putut-o distinge.
- Experimentul compară patru texte. El nu poate atribui un efect unui mecanism anume (cuvântul „creative”, forma de comandă sau un „mod” activat). Contrastul cu placebo-ul D arată doar dacă B se distinge de o linie de aceeași formă, cu același cuvânt.

## 9. Limite cunoscute

- Cinci modele mici (4–8 miliarde de parametri), rulate local. Literatura (secțiunea 2) arată că efectele de formă diferă de la un model la altul, deci rezultatul nu se transferă automat la modele mari sau la servicii online.
- „Creativitatea” e măsurată indirect: prin varietatea numelor și prin evaluatori automați, care au propriile preferințe. Scorurile evaluatorilor automați nu au fost validate față de evaluatori umani; P1 (diversitatea numelor) nu depinde de niciun evaluator.
- Sarcinile sunt în limba română; unele modele mici o stăpânesc mai slab. Comparațiile se fac însă în interiorul aceluiași model, deci asta afectează toate condițiile la fel.
- 20 de rulări pe combinație și model pot detecta, pe un model luat separat, doar efecte moderate sau mari. Analiza combinată are mai multă putere.
- Testul acoperă doar sintaxa dată ca exemplu public, aplicată unor modele fără nicio configurare care să o definească (§1).
- Un model poate „confirma” singur că a intrat într-un mod (de exemplu „Mod creativ activat!”). O astfel de confirmare nu e o dovadă; contează doar ce se măsoară în răspunsuri.
- Un răspuns poate repeta singur comanda și astfel își poate dezvălui condiția în fața evaluatorului; riscul e măsurat prin analiza de sensibilitate (§7).
- Dacă evaluarea e întreruptă și reluată, răspunsurile rămase sunt amestecate din nou, deci ordinea în care le vede evaluatorul diferă de cea dintr-o rulare continuă. Fiecare evaluare rămâne independentă și oarbă.

## Abateri

*(Se completează după experiment, dacă e cazul.)*
