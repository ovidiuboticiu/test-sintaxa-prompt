---
title: "Are o „sintaxă de comandă” vreun efect asupra creativității unui model de limbaj?"
subtitle: 'Un experiment preînregistrat cu linia `\texttt{//Dev\_Lab\_Op\_Mode -{}-creative}`{=latex} pe cinci modele locale'
author: "Ovidiu Boticiu"
date: "25 noiembrie 2026"
lang: ro-RO
---

\Needspace{6\baselineskip}

## Rezumat

**Obiectiv.** În comunitățile online despre inteligență artificială circulă afirmația că anumite linii de tip comandă, scrise la începutul unei conversații, ar activa „moduri” speciale ale modelelor de limbaj și le-ar controla comportamentul mai bine decât o instrucțiune formulată obișnuit. Studiul de față testează un exemplu public al acestei afirmații, prezentat ca un mijloc de a obține răspunsuri mai creative: linia `\mbox{\texttt{//Dev\_Lab\_Op\_Mode -{}-creative}}`{=latex}.

**Metodă.** Cinci modele de limbaj mici (4–8 miliarde de parametri), din cinci familii diferite, au fost rulate local, fără instrucțiuni de sistem. Fiecare a primit două sarcini în limba română (cinci nume pentru o cafenea și primul paragraf al unei povești) în patru condiții care diferă doar prin prima linie a mesajului:

- **A:** nicio linie (referința);
- **B:** linia testată, `//Dev_Lab_Op_Mode --creative`;
- **C:** instrucțiunea obișnuită „Răspunde cât mai creativ.”;
- **D:** placebo, `//Zq_Rt_Op_Mode --creative` (aceeași formă, „mod” inventat).

\noindent Au rezultat 800 de răspunsuri, cu 20 de repetiții pe fiecare combinație și seed-uri comune între condiții. Rezultatele primare au fost diversitatea numelor (P1) și originalitatea paragrafului (P2), notată orb de doi evaluatori automați. Protocolul, testele statistice și regulile de decizie au fost fixate într-o etichetă Git înainte de colectarea datelor.

**Rezultate.** Față de lipsa oricărei instrucțiuni, linia testată a crescut scorul de originalitate al paragrafelor cu 0,45 puncte pe o scală de la 1 la 5 (interval de încredere 95%: 0,33–0,57), cu aceeași direcție la toate cele cinci modele. Placebo-ul D nu s-a deosebit însă de linia testată la niciunul dintre rezultatele primare, iar instrucțiunea obișnuită C a obținut rezultate mai bune decât linia testată atât la diversitatea numelor (−0,040), cât și la originalitate (−0,26; interval 95%: −0,39 până la −0,12).

**Concluzie.** Conform regulilor preînregistrate, afirmația nu este susținută de acest experiment. Pe modelele testate, linia nu s-a comportat ca un „mod” distinct: o linie inventată cu aceeași formă a avut un efect asemănător, iar o propoziție obișnuită în română a fost mai eficientă. Experimentul nu poate separa efectul cuvântului „creative” de cel al formei de comandă și nu se extinde automat la modele mari sau la servicii online.

**Cuvinte-cheie:** modele de limbaj; inginerie a prompturilor; sensibilitate la formă; preînregistrare; control placebo; evaluare automată oarbă; test de permutare.

\clearpage

## 1. Introducere

Utilizatorii modelelor de limbaj caută, firesc, formulări care să le îmbunătățească răspunsurile. Pe lângă recomandările documentate de furnizori, circulă și rețete mai neobișnuite. Una dintre ele susține că anumite linii scrise ca o comandă de program, de exemplu

```
//Dev_Lab_Op_Mode --creative
```

pot fi folosite la începutul unei sesiuni noi pentru a „activa” un comportament anume. Potrivit acestei afirmații, o astfel de linie ar controla modelul mai bine decât o instrucțiune formulată în cuvinte.

Afirmația are o parte testabilă. Dacă linia activează un mod real, răspunsurile primite cu ea ar trebui să difere sistematic de cele primite fără ea. Mai important, ar trebui să difere și de cele primite cu o linie de aceeași formă, dar cu un nume inventat. Dacă diferența apare doar față de lipsa oricărei instrucțiuni, ea poate fi explicată prin sensibilitatea obișnuită a modelelor la forma promptului sau prin cuvântul „creative” pe care linia îl conține.

**Întrebarea studiului:** are linia `//Dev_Lab_Op_Mode --creative` un efect asupra creativității răspunsurilor și, dacă da, se deosebește acest efect de cel al unei linii placebo de aceeași formă și de cel al unei instrucțiuni obișnuite?

Studiul privește **doar** exemplul de mai sus, așa cum a fost dat public, aplicat unor modele care nu au nicio configurare care să îl definească: fără instrucțiuni de sistem, fără instrucțiuni personalizate și fără o aplicație care să interpreteze linia. Testul nu poate exclude ca linia să aibă o semnificație într-o aplicație anume sau într-un set de instrucțiuni care o definește explicit. Scopul nu este evaluarea vreunei persoane, ci verificarea unei afirmații tehnice cu o metodă pe care oricine o poate repeta.

\Needspace{6\baselineskip}

## 2. Context

Sensibilitatea modelelor de limbaj la forma promptului este bine documentată. Sclar și colaboratorii (2024) au arătat că modificări mici de formatare, cum ar fi separatorii, spațiile sau majusculele, pot produce diferențe de până la 76 de puncte de acuratețe la un model de 13 miliarde de parametri. În plus, formatul favorabil diferă de la un model la altul. He și colaboratorii (2024) au găsit diferențe de până la 40% între variante ale aceleiași cereri scrise ca text simplu, Markdown, YAML sau JSON, cu o stabilitate mai mare la modelele mai mari. Mishra și colaboratorii (2023) au raportat că instrucțiunile scrise ca pseudo-cod au îmbunătățit performanța la unele sarcini.

Aceste studii reformatează însă **întreaga** cerere și păstrează conținutul. Nu am găsit un test al unei linii-comandă de tip „mod” comparate cu un placebo. Pentru sintaxa testată nu am găsit nici o documentație publică din partea furnizorilor de modele. Afirmațiile despre astfel de linii documentează existența unei practici, nu validitatea ei.

Consecința pentru designul experimentului este directă: o diferență între linia testată și lipsa oricărei instrucțiuni, luată singură, poate reflecta doar sensibilitatea obișnuită la formă. Numai o diferență față de un placebo cu aceeași formă ar indica ceva specific liniei testate.

\Needspace{6\baselineskip}

## 3. Metodă

\Needspace{6\baselineskip}

### 3.1 Condiții

Fiecare cerere a fost trimisă într-o conversație nouă, fără instrucțiuni de sistem. Cele patru condiții diferă doar prin prima linie a mesajului (Tabelul 1).

\Needspace{8\baselineskip}

**Tabelul 1. Condițiile experimentale**

| Cod | Prima linie a mesajului | Rolul condiției |
|:--|:----------------------|:------------------------------|
| A | *(nicio linie)* | Referință: cererea simplă |
| B | `//Dev_Lab_Op_Mode --creative` | Linia testată |
| C | `Răspunde cât mai creativ.` | Aceeași intenție, în cuvinte obișnuite |
| D | `//Zq_Rt_Op_Mode --creative` | Placebo: aceeași formă și același cuvânt, cu un „mod” inventat |

Logica designului este următoarea. Dacă B activează un mod real, B trebuie să difere de D. Dacă B și D se comportă la fel, efectul nu poate fi atribuit numelui „Dev\_Lab\_Op\_Mode”. Dacă B nu întrece C, forma de comandă nu aduce nimic în plus față de limbajul obișnuit.

\Needspace{6\baselineskip}

### 3.2 Sarcini

Au fost folosite două sarcini în limba română, cu textul identic în toate condițiile:

- **T1 (listă):** „Propune 5 nume pentru o cafenea dintr-un oraș mic din România. Scrie doar lista, câte un nume pe rând.”
- **T2 (text liber):** „Scrie primul paragraf, de cel mult 120 de cuvinte, al unei povești despre un far părăsit.”

\Needspace{6\baselineskip}

### 3.3 Modele și setări

Cele cinci modele generatoare provin din familii diferite și au fost rulate local în LM Studio 0.4.25, prin interfața compatibilă OpenAI, în cuantizarea Q4\_K\_M (Tabelul 2). Fișierele exacte ale modelelor sunt identificate prin suma SHA-256 în fișierul `MODELE.md` din repozitoriu.

\Needspace{10\baselineskip}

**Tabelul 2. Modelele generatoare și sesiunile de generare**

| Denumire scurtă | Identificator API | Familie | Generare (UTC) |
|:-----------|:-----------------------------|:----------|:--------------|
| Phi-4 mini | `microsoft_phi-4-mini-instruct` | Microsoft Phi | 22.11, 18:13–19:40 |
| Ministral 3 8B | `ministral-3-8b-instruct-2512` | Mistral | 22.11, 19:50–21:14 |
| Granite 4.1 8B | `granite-4.1-8b` | IBM Granite | 23.11, 16:16–17:19 |
| Gemma 4 E4B | `gemma-4-e4b-it` | Google Gemma | 23.11, 18:19–21:13 |
| Qwen3 4B | `qwen3-4b-instruct-2507` | Alibaba Qwen | 24.11, 14:08–14:47 |

Parametrii de generare au fost trimiși explicit cu fiecare cerere și au fost aceiași pentru toate modelele: temperatură 0,8; top\_p 0,95; top\_k 40; repeat\_penalty 1,1; cel mult 1.500 de tokeni. Comportamentul implicit de raționament intern al fiecărui model a fost păstrat, pentru a reproduce situația unui utilizator obișnuit. Dintre cele cinci modele, doar Gemma 4 E4B a raționat. Raționamentul nu a intrat în textul evaluat, iar numărul tokenilor de raționament a fost înregistrat ca rezultat secundar.

Pentru fiecare combinație de model, sarcină și condiție s-au făcut 20 de repetiții, adică 5 × 2 × 4 × 20 = 800 de rulări. Pentru un model, o sarcină și o repetiție date, toate cele patru condiții au primit **același seed**, astfel încât singura diferență dintre ele a fost prima linie a mesajului. Seed-urile au fost derivate determinist din seed-ul principal 20261122. Modelele au fost rulate pe rând, într-o ordine fixată dinainte. În interiorul fiecărui model, cele 160 de rulări au fost amestecate aleator, pentru ca eventualele schimbări în timp, cum ar fi încălzirea calculatorului, să nu favorizeze vreo condiție.

\Needspace{6\baselineskip}

### 3.4 Evaluare oarbă

Originalitatea răspunsurilor a fost notată de două modele diferite de toate generatoarele: Qwen3.5 9B și Gemma 4 12B, rulate cu temperatura 0 și fără raționament intern. Fiecare evaluator a primit **doar** cererea, identică în toate condițiile, și răspunsul. Nu a primit prima linie a mesajului, condiția sau numele modelului generator. Răspunsurile au fost prezentate fiecărui evaluator într-o ordine aleatoare proprie.

Grila a cerut o notă de originalitate de la 1 („banal, previzibil”) la 5 („foarte original și memorabil, fără să se abată de la cerere”), cu instrucțiunea explicită de a nu ține seama de lungime sau de corectitudinea gramaticală. Era valid doar un răspuns format dintr-o singură cifră între 1 și 5; orice alt răspuns ar fi fost înregistrat ca invalid. Scorul folosit în analiză este media celor doi evaluatori. Textul complet al grilei este dat în Anexă.

Experimentul nu a inclus evaluatori umani. Autorul cunoștea ipotezele și nu avea la dispoziție evaluatori independenți. Datele brute sunt publice, iar repozitoriul conține instrumentele pentru o evaluare umană oarbă ulterioară.

\Needspace{6\baselineskip}

### 3.5 Rezultate măsurate

Au fost stabilite dinainte două rezultate primare, singurele care decid verdictul:

- **P1, diversitatea numelor (T1):** proporția de nume unice din toate numele produse de un model într-o condiție, după normalizare (litere mici, fără diacritice, fără numerotare și punctuație). Reguli fixate dinainte au exclus din liste formulele introductive, descrierile și eventualele mențiuni ale comenzii.
- **P2, originalitatea paragrafului (T2):** scorul mediu dat de cei doi evaluatori.

Rezultatele secundare, descriptive, includ scorul de originalitate la T1, respectarea cerinței de a da exact cinci nume, lungimea paragrafelor, diversitatea lexicală (distinct-2), acordul dintre evaluatori, numărul răspunsurilor trunchiate sau care menționează comanda și raționamentul intern.

\Needspace{6\baselineskip}

### 3.6 Analiza statistică și regulile de decizie

O **pereche** este formată din două răspunsuri ale aceluiași model, la aceeași sarcină și aceeași repetiție (deci cu același seed), în două condiții diferite. Pentru fiecare comparație s-a calculat diferența dintre condiții în fiecare model, apoi media acestor diferențe peste cele cinci modele. S-au făcut trei comparații (B față de A, C și D) pentru fiecare rezultat primar, deci șase teste.

Semnificația a fost evaluată printr-un test de permutare bilateral pe perechi, stratificat pe model, cu 10.000 de permutări și seed fix. Valorile p au fost corectate pentru comparații multiple prin metoda Holm (Holm, 1979), cu pragul de 0,05 aplicat valorii ajustate. Pentru P2 s-a raportat și intervalul de încredere 95% obținut prin bootstrap pe perechi, cu 5.000 de reeșantionări în interiorul fiecărui model (Efron și Tibshirani, 1993). Pentru P1 nu s-a raportat interval de încredere, deoarece reeșantionarea duplică liste întregi și ar subestima sistematic diversitatea.

Fiecare comparație primește unul dintre patru rezultate: **B mai bun** (p ajustat < 0,05, diferență în favoarea lui B), **B mai slab** (p ajustat < 0,05, diferență în defavoarea lui B), **nicio diferență detectată** (p ajustat ≥ 0,05) sau **neestimabil**. Regulile pentru verdictul global sunt simetrice și au fost fixate dinainte (Tabelul 3).

\Needspace{8\baselineskip}

**Tabelul 3. Regulile preînregistrate pentru verdictul global**

| Situație | Verdict |
|:------------------------------------------|:---------------------|
| Vreo comparație este neestimabilă sau lipsește un model | Suspendat |
| La **același** rezultat primar, B este mai bun decât C **și** decât D, iar B nu este mai slab la niciuna dintre cele șase comparații | Afirmația este susținută pentru acest set de modele |
| Orice altă situație | Afirmația nu este susținută de acest experiment |

\Needspace{6\baselineskip}

### 3.7 Preînregistrare și audit

Protocolul, codul, prompturile și regulile de decizie au fost salvate în repozitoriul Git al studiului și marcate cu eticheta `preinregistrare-v1` (commit d313317). Versiunea publicată cu această etichetă datează din 22 noiembrie 2026, ora 18:10 UTC; prima rulare a experimentului a început la 18:13 UTC. O rulare pilot, cu câte un răspuns pe combinație și alte seed-uri, a servit doar la verificarea funcționării. Datele ei sunt păstrate separat și nu intră în analiză.

Înainte de etichetare, protocolul și codul au trecut printr-un audit extern într-o singură rundă, făcut de un alt sistem AI (Codex, OpenAI), cu reguli de oprire fixate dinainte. Auditul a identificat nouă observații blocante, toate corectate înainte de etichetare: printre altele, testul pe perechi, tratarea contrastelor neestimabile, parsarea strictă a notelor și reguli explicite de extragere a numelor. Nu a urmat o a doua rundă de audit. Analiza a fost rulată o singură dată, după încheierea colectării tuturor datelor, fără nicio examinare intermediară a rezultatelor primare.

\clearpage

## 4. Rezultate

\Needspace{6\baselineskip}

### 4.1 Integritatea datelor

Toate cele 800 de rulări au reușit; nu există rulări eșuate, duplicate sau răspunsuri goale. Fiecare dintre cele 40 de celule (model × sarcină × condiție) conține exact 20 de răspunsuri. Ambii evaluatori au dat câte 800 de note valide, astfel încât toate perechile au fost complete. Unsprezece răspunsuri, toate de la Phi-4 mini, au fost trunchiate la limita de 1.500 de tokeni, din cauza unor bucle repetitive: nouă în condiția A, unul în B și unul în D. Niciun răspuns nu a menționat comanda și niciun model nu a anunțat că ar fi intrat într-un „mod”.

Acordul dintre evaluatori a fost moderat: corelația Pearson între notele lor a fost 0,48, iar notele au coincis exact în 50% din cazuri.

\Needspace{6\baselineskip}

### 4.2 Statistici descriptive

Tabelele 4 și 5 prezintă rezultatele pe fiecare model și condiție.

\Needspace{14\baselineskip}

**Tabelul 4. Sarcina T1 (nume de cafenea), pe model și condiție**

| Model | Cond. | Diversitatea numelor (P1) | Răspunsuri cu exact 5 nume | Originalitate T1 |
|:----------|:--:|------:|------:|------:|
| Gemma 4 E4B | A | 0,930 | 20/20 | 3,05 |
|  | B | 0,940 | 20/20 | 3,35 |
|  | C | 0,970 | 20/20 | 3,92 |
|  | D | 0,960 | 20/20 | 3,10 |
| Qwen3 4B | A | 0,880 | 20/20 | 3,73 |
|  | B | 0,850 | 20/20 | 3,42 |
|  | C | 0,930 | 20/20 | 3,75 |
|  | D | 0,910 | 20/20 | 3,30 |
| Ministral 3 8B | A | 0,980 | 20/20 | 3,35 |
|  | B | 0,990 | 20/20 | 3,38 |
|  | C | 1,000 | 20/20 | 3,80 |
|  | D | 1,000 | 20/20 | 3,27 |
| Granite 4.1 8B | A | 0,950 | 20/20 | 3,30 |
|  | B | 0,900 | 20/20 | 2,83 |
|  | C | 0,980 | 20/20 | 3,52 |
|  | D | 0,970 | 20/20 | 3,30 |
| Phi-4 mini | A | 0,952 | 19/20 | 2,12 |
|  | B | 1,000 | 14/20 | 2,90 |
|  | C | 1,000 | 19/20 | 3,38 |
|  | D | 0,983 | 16/20 | 3,00 |

\Needspace{14\baselineskip}

**Tabelul 5. Sarcina T2 (paragraful despre far), pe model și condiție**

| Model | Cond. | Originalitate (P2) | Distinct-2 | Lungime medie (cuvinte) | Trunchiate |
|:----------|:--:|------:|------:|------:|------:|
| Gemma 4 E4B | A | 3,20 | 0,800 | 107,9 | 0 |
|  | B | 3,40 | 0,802 | 98,5 | 0 |
|  | C | 3,80 | 0,828 | 104,3 | 0 |
|  | D | 3,35 | 0,798 | 98,3 | 0 |
| Qwen3 4B | A | 3,40 | 0,737 | 120,5 | 0 |
|  | B | 3,88 | 0,736 | 112,0 | 0 |
|  | C | 4,12 | 0,743 | 122,2 | 0 |
|  | D | 3,83 | 0,745 | 114,8 | 0 |
| Ministral 3 8B | A | 3,17 | 0,826 | 125,5 | 0 |
|  | B | 3,58 | 0,835 | 141,7 | 0 |
|  | C | 4,03 | 0,834 | 146,7 | 0 |
|  | D | 3,62 | 0,831 | 137,1 | 0 |
| Granite 4.1 8B | A | 2,33 | 0,826 | 82,6 | 0 |
|  | B | 2,52 | 0,820 | 107,3 | 0 |
|  | C | 2,38 | 0,846 | 97,1 | 0 |
|  | D | 2,23 | 0,836 | 85,7 | 0 |
| Phi-4 mini | A | 1,20 | 0,584 | 584,1 | 9 |
|  | B | 2,15 | 0,791 | 256,8 | 1 |
|  | C | 2,48 | 0,777 | 283,8 | 0 |
|  | D | 1,93 | 0,718 | 297,5 | 1 |

Media peste modele a scorului de originalitate la T2 a fost 2,66 în condiția A, 3,11 în B, 3,36 în C și 2,99 în D. Pentru diversitatea numelor, valorile corespunzătoare au fost 0,938, 0,936, 0,976 și 0,965. Diversitatea numelor a fost aproape de valoarea maximă, 1, la majoritatea modelelor și condițiilor, ceea ce lasă puțin loc pentru diferențe la P1.

\Needspace{6\baselineskip}

### 4.3 Rezultatele primare

Tabelul 6 prezintă cele șase comparații preînregistrate, pe toate modelele combinate.

\Needspace{12\baselineskip}

**Tabelul 6. Comparațiile primare (toate modelele combinate)**

| Rezultat | Compa­rație | Dife­rență | IÎ 95% | p | p Holm | Rezultatul comparației |
|:-----------|:-------|-------:|:--------------:|------:|------:|:---------------|
| P1 diversitate | B vs A | −0,002 | — | 0,857 | 0,857 | nicio diferență detectată |
| P1 diversitate | B vs C | −0,040 | — | 0,0001 | 0,0006 | B mai slab |
| P1 diversitate | B vs D | −0,029 | — | 0,028 | 0,083 | nicio diferență detectată |
| P2 originalitate | B vs A | +0,445 | [0,325; 0,565] | 0,0001 | 0,0006 | B mai bun |
| P2 originalitate | B vs C | −0,255 | [−0,385; −0,120] | 0,0008 | 0,0032 | B mai slab |
| P2 originalitate | B vs D | +0,115 | [−0,015; 0,245] | 0,112 | 0,224 | nicio diferență detectată |

*Notă.* Diferența este media, peste cele cinci modele, a diferenței medii pe perechi din fiecare model. Valoarea p = 0,0001 este cea mai mică posibilă cu 10.000 de permutări. Nicio comparație nu a fost neestimabilă și nicio pereche nu a fost incompletă.

Linia testată a obținut un scor de originalitate mai mare decât lipsa oricărei instrucțiuni, dar nu s-a deosebit de placebo-ul D la niciunul dintre rezultatele primare. Față de instrucțiunea obișnuită C, linia testată a avut rezultate mai slabe la ambele rezultate primare.

\Needspace{6\baselineskip}

### 4.4 Verdictul preînregistrat

Criteriul de susținere cerea ca, la același rezultat primar, B să fie mai bun atât decât C, cât și decât D. Criteriul nu a fost îndeplinit la niciunul dintre rezultate: față de D nu s-a detectat nicio diferență, iar față de C linia testată a fost mai slabă. Conform regulilor din Tabelul 3, **afirmația nu este susținută de acest experiment.**

Verdictul opus ar fi necesitat ca B să depășească semnificativ, după corecția Holm, atât C, cât și D la același rezultat primar, fără să fie mai slab la vreo comparație. Rezultatele sunt departe de această situație: la P2, diferența față de C are semnul opus celui cerut, iar intervalul ei de încredere nu include zero.

\Needspace{6\baselineskip}

### 4.5 Consecvența între modele și rezultatele pe fiecare model

Tabelul 7 arată, pentru fiecare comparație, la câte modele diferența a mers în favoarea liniei testate, indiferent de semnificație. Tabelul 8 prezintă testele separate pe fiecare model, cu corecție Holm proprie fiecărui model. Aceste rezultate sunt secundare și nu decid verdictul.

\Needspace{8\baselineskip}

**Tabelul 7. Numărul de modele la care diferența a fost în favoarea lui B**

| Rezultat | B vs A | B vs C | B vs D |
|:----------------|:------:|:------:|:------:|
| P1 diversitate | 3 din 5 | 0 din 5 | 1 din 5 |
| P2 originalitate | 5 din 5 | 1 din 5 | 4 din 5 |

\Needspace{14\baselineskip}

**Tabelul 8. Diferențele pe fiecare model (p ajustat Holm în paranteză)**

| Model | Rez. | B vs A | B vs C | B vs D |
|:------------|:----:|:---------------|:---------------|:---------------|
| Gemma 4 E4B | P1 | +0,010 (1,000) | −0,030 (1,000) | −0,020 (1,000) |
|  | P2 | +0,200 (0,776) | −0,400 (0,100) | +0,050 (1,000) |
| Qwen3 4B | P1 | −0,030 (1,000) | **−0,080 (0,026)** | −0,060 (0,505) |
|  | P2 | **+0,475 (0,002)** | −0,250 (0,126) | +0,050 (1,000) |
| Ministral 3 8B | P1 | +0,010 (1,000) | −0,010 (1,000) | −0,010 (1,000) |
|  | P2 | +0,400 (0,052) | **−0,450 (0,004)** | −0,050 (1,000) |
| Granite 4.1 8B | P1 | −0,050 (0,901) | **−0,080 (0,022)** | −0,070 (0,274) |
|  | P2 | +0,200 (0,901) | +0,150 (0,901) | +0,300 (0,901) |
| Phi-4 mini | P1 | **+0,048 (0,027)** | 0,000 (1,000) | +0,017 (0,828) |
|  | P2 | **+0,950 (0,003)** | −0,325 (0,828) | +0,225 (0,828) |

*Notă.* Valorile marcate cu aldin au p ajustat < 0,05 în testul modelului respectiv.

Avantajul liniei testate față de condiția A la originalitate are aceeași direcție la toate cele cinci modele. Nu se datorează, așadar, doar modelului Phi-4 mini, la care condiția A a produs cele mai multe bucle și cele mai slabe scoruri. La niciun model linia testată nu s-a deosebit semnificativ de placebo.

\Needspace{6\baselineskip}

### 4.6 Analize de sensibilitate

Tabelul 9 repetă comparațiile pentru originalitate cu fiecare evaluator separat. Valorile p nu sunt corectate și nu decid verdictul. Analiza fără răspunsurile care menționează comanda, prevăzută în protocol, coincide cu analiza principală, deoarece niciun răspuns nu a menționat comanda.

\Needspace{8\baselineskip}

**Tabelul 9. Originalitatea (P2) cu fiecare evaluator separat**

| Evaluator | B vs A | B vs C | B vs D |
|:--------------------|:----------------|:----------------|:----------------|
| Ambii (analiza principală) | +0,445 (p < 0,001) | −0,255 (p = 0,001) | +0,115 (p = 0,112) |
| Doar Qwen3.5 9B | +0,260 (p = 0,002) | −0,050 (p = 0,619) | +0,170 (p = 0,019) |
| Doar Gemma 4 12B | +0,630 (p < 0,001) | −0,460 (p < 0,001) | +0,060 (p = 0,613) |

Cei doi evaluatori sunt de acord asupra direcției față de condiția A, dar nu și asupra celorlalte contraste. Diferența față de C provine aproape în întregime din notele evaluatorului Gemma 4 12B, iar notele evaluatorului Qwen3.5 9B arată o diferență față de placebo care ar fi semnificativă fără corecție (p = 0,019). Niciunul dintre evaluatori luat separat nu ar fi îndeplinit criteriul de susținere, care cere superioritate simultană față de C și D.

\Needspace{6\baselineskip}

### 4.7 Raționamentul intern

Dintre cele cinci modele, doar Gemma 4 E4B a produs raționament intern (Tabelul 10). În condiția A, modelul a raționat în 29 din 40 de răspunsuri; în condițiile B, C și D, în 39–40 din 40, cu mai mulți tokeni în medie.

\Needspace{8\baselineskip}

**Tabelul 10. Raționamentul intern la Gemma 4 E4B (ambele sarcini)**

| Condiție | Răspunsuri cu raționament | Tokeni de raționament (medie) |
|:----------|:------:|:------:|
| A | 29/40 | 351 |
| B | 39/40 | 534 |
| C | 40/40 | 562 |
| D | 39/40 | 547 |

Prin urmare, orice linie adăugată înaintea cererii, fie comanda testată, placebo-ul sau propoziția obișnuită, a crescut frecvența raționamentului. Linia testată nu s-a deosebit de celelalte două. Rezultatul este secundar, descriptiv și limitat la un singur model.

\clearpage

## 5. Discuție

\Needspace{6\baselineskip}

### 5.1 Ce arată rezultatele

Pe modelele testate, linia `//Dev_Lab_Op_Mode --creative` a avut un efect măsurabil față de lipsa oricărei instrucțiuni: paragrafele au fost notate, în medie, cu aproape jumătate de punct mai originale, la toate cele cinci modele. Efectul nu a fost însă specific liniei. O linie cu aceeași formă și un nume inventat a produs rezultate care nu s-au deosebit de ale ei, iar o propoziție obișnuită în română a fost mai eficientă la ambele rezultate primare. Datele nu arată, așadar, nimic care să corespundă unui „mod” activat de numele „Dev\_Lab\_Op\_Mode”.

Rezultatul este compatibil cu ce se știe din literatură: modelele reacționează la conținutul și forma promptului. O cerere precedată de cuvântul „creative” sau de o instrucțiune explicită de creativitate primește, în medie, răspunsuri notate ca mai originale. Studiul nu a găsit un avantaj al formei de comandă față de limbajul obișnuit; a găsit, dimpotrivă, un dezavantaj.

\Needspace{6\baselineskip}

### 5.2 Ce nu arată rezultatele

Placebo-ul D conține și el cuvântul „creative” și are aceeași formă de comandă. Contrastul B–D arată doar că numele „Dev\_Lab\_Op\_Mode” nu a adus nimic în plus față de un nume inventat. Experimentul nu poate separa efectul cuvântului „creative” de cel al formei de comandă și nu poate atribui efectul observat față de A unui mecanism anume.

„Nicio diferență detectată” nu înseamnă că diferența este zero. Pentru originalitate, intervalul de încredere al diferenței B–D, de la −0,015 la +0,245, nu exclude un avantaj mic al liniei testate față de placebo. Un astfel de avantaj ar rămâne însă mai mic decât dezavantajul față de instrucțiunea obișnuită, al cărui interval de încredere este în întregime negativ.

\Needspace{6\baselineskip}

### 5.3 Explicații alternative și factori de confuzie

**Lungimea răspunsurilor.** Unele modele au scris paragrafe mai lungi în anumite condiții; de exemplu, Granite 4.1 8B a scris în medie 107 cuvinte cu linia testată și 83 fără ea. Grila le-a cerut evaluatorilor să nu țină seama de lungime, dar o influență indirectă nu poate fi exclusă. Lungimea nu a fost un factor controlat în analiză.

**Buclele modelului Phi-4 mini.** În condiția A, acest model a intrat de nouă ori într-o buclă repetitivă, cu răspunsuri lungi și note foarte mici. Orice linie adăugată a redus frecvența buclelor. Efectul față de A este cel mai mare la acest model (+0,95), dar apare, cu aceeași direcție, la toate celelalte modele.

**Evaluatorii automați.** Acordul dintre cei doi evaluatori a fost doar moderat (r = 0,48), iar analizele de sensibilitate arată că direcția unor contraste depinde de evaluator. Fiecare evaluator aparține aceleiași familii ca unul dintre generatoare, ceea ce poate crea o preferință pentru textele „propriei” familii. O astfel de preferință ar afecta însă la fel toate cele patru condiții ale aceluiași model. Notele automate nu au fost validate față de evaluatori umani. Rezultatul P1, diversitatea numelor, nu depinde de niciun evaluator și conduce la aceeași concluzie: linia testată nu a întrecut nici placebo-ul, nici instrucțiunea obișnuită.

**Efectul de plafon la P1.** Diversitatea numelor a fost aproape maximă la majoritatea modelelor, astfel încât P1 a avut puțin loc să arate o îmbunătățire. Faptul că instrucțiunea obișnuită C a depășit totuși linia testată la acest rezultat arată că măsura nu a fost complet insensibilă.

\Needspace{6\baselineskip}

### 5.4 Relevanța practică

Pentru utilizatorul care vrea răspunsuri mai creative de la un model asemănător celor testate, datele sugerează că o instrucțiune scrisă direct, în cuvinte, funcționează cel puțin la fel de bine ca linia de tip comandă și, pe aceste modele, mai bine. Concluzia privește doar modelele, sarcinile și setările studiate.

\Needspace{6\baselineskip}

## 6. Limite

- **Modele.** Au fost testate cinci modele mici (4–8 miliarde de parametri), rulate local. Efectele de formă diferă de la un model la altul (Sclar et al., 2024), iar rezultatul nu se transferă automat la modele mari sau la servicii online.
- **Domeniul afirmației.** Testul acoperă doar linia dată ca exemplu public, aplicată unor modele fără nicio configurare care să o definească. El nu exclude ca linia să aibă un efect într-o aplicație sau într-un set de instrucțiuni care o definește.
- **Măsurarea creativității.** Creativitatea a fost măsurată indirect, prin diversitatea numelor și prin note de originalitate date de modele de limbaj. Aceste note au propriile preferințe și nu au fost validate față de evaluatori umani.
- **Sarcini și limbă.** Au fost folosite doar două sarcini, în limba română, pe care unele modele mici o stăpânesc mai slab. Comparațiile se fac însă în interiorul aceluiași model, deci limba afectează la fel toate condițiile.
- **Setări.** S-a folosit o singură configurație de generare (temperatură 0,8). Efectul liniei poate fi diferit la alte temperaturi.
- **Puterea statistică.** Douăzeci de repetiții pe celulă permit, pe un model luat separat, detectarea doar a efectelor moderate sau mari. Analiza combinată are mai multă putere, dar nu exclude efecte mici.
- **Mecanism.** Experimentul compară patru texte și nu poate atribui un efect unui mecanism intern.

\Needspace{6\baselineskip}

## 7. Abateri de la protocol

1. **Versiunea scriptului de evaluare.** Pe calculatorul pe care s-a rulat experimentul, scriptul de evaluare era o versiune anterioară, căreia îi lipsea verificarea preînregistrată care oprește evaluarea dacă evaluatorul produce raționament intern. Fișierele de evaluare nu înregistrează tokenii de raționament ai evaluatorilor, astfel că absența raționamentului nu poate fi dovedită direct. Există însă indicii indirecte: toate cele 1.600 de note sunt formate dintr-o singură cifră și s-au încheiat normal (în pilot, raționamentul evaluatorului ducea la trunchiere și la notă lipsă), iar opțiunea de raționament a fost verificată ca dezactivată pentru ambii evaluatori înainte de rulare. Grila, parametrii și regula de parsare a notelor sunt identice cu versiunea preînregistrată.
2. **Versiunea scriptului de analiză.** Analiza a fost rulată inițial cu o versiune incompletă a scriptului, căreia îi lipsea secțiunea secundară despre raționamentul intern. Rezultatele raportate aici provin din versiunea preînregistrată, rulată pe aceleași date. Rezultatele primare și verdictul sunt identice, cifră cu cifră, între cele două rulări.
3. **Scripturile de generare.** Scriptul de generare, funcțiile comune, fișierul de configurare și prompturile de pe calculatorul de execuție au fost verificate ca identice cu versiunea preînregistrată.
4. **Evaluatorul Gemma 4 12B.** Opțiunea de raționament nu se păstra la reîncărcarea modelului și a fost dezactivată manual după încărcare. Modelul a rulat cu patru sloturi paralele, dar cererile au fost trimise strict una după alta.
5. **Sesiuni.** Generarea s-a făcut în cinci sesiuni, câte una pe model, între 22 și 24 noiembrie 2026 (Tabelul 2), fără modificarea setărilor în timpul unei sesiuni.
6. **Afișaj.** Un defect cosmetic al scriptului de generare afișa contorul global raportat la totalul unui singur model (de exemplu „161/160”). Defectul nu afectează datele și a fost lăsat necorectat pe durata experimentului.

\Needspace{6\baselineskip}

## 8. Transparență, reproducere și rolul instrumentelor AI

Repozitoriul studiului (<https://github.com/ovidiuboticiu/test-sintaxa-prompt>) conține protocolul preînregistrat, codul, prompturile, identificarea exactă a modelelor, raportul auditului, datele pilot, toate cele 800 de răspunsuri brute, cele 1.600 de note ale evaluatorilor și raportul generat automat de analiză. Eticheta `preinregistrare-v1` permite verificarea faptului că protocolul a precedat datele. Experimentul poate fi repetat pe Windows, Linux sau macOS, cu LM Studio și Python 3.10 sau mai nou, urmând instrucțiunile din fișierul README. Analiza poate fi refăcută din datele publicate cu o singură comandă.

Cercetarea a fost realizată de autor, cu asistența unor instrumente AI. Întrebarea de cercetare, alegerea designului (inclusiv condiția placebo, modelele și numărul de rulări), deciziile asupra protocolului, rularea experimentului și interpretarea rezultatelor aparțin autorului. Claude (Anthropic) a asistat la redactarea protocolului, a codului, a documentației și a acestui raport, la cererea și sub controlul autorului. Codex (OpenAI) a efectuat auditul pre-execuție. Modelele testate și cele folosite ca evaluatori sunt instrumente de măsurare, nu autori.

\Needspace{6\baselineskip}

## 9. Concluzie

Testul preînregistrat nu susține afirmația că linia `//Dev_Lab_Op_Mode --creative` activează un mod creativ distinct. Pe cinci modele locale din familii diferite, linia a îmbunătățit notele de originalitate față de lipsa oricărei instrucțiuni. O linie inventată cu aceeași formă nu s-a deosebit însă de ea, iar instrucțiunea obișnuită „Răspunde cât mai creativ.” a dat rezultate mai bune atât la diversitatea numelor, cât și la originalitatea textului. Rezultatul este limitat la modelele, sarcinile și setările testate, dar metoda și datele sunt publice și pot fi aplicate oricărei alte „sintaxe” sau oricărui alt model.

\Needspace{6\baselineskip}

## Bibliografie

\noindent\hangindent=1.27cm Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC.

\noindent\hangindent=1.27cm He, J., et al. (2024). Does Prompt Formatting Have Any Impact on LLM Performance? *arXiv preprint* arXiv:2411.10541.

\noindent\hangindent=1.27cm Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70.

\noindent\hangindent=1.27cm Mishra, M., et al. (2023). Prompting with Pseudo-Code Instructions. În *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)*. arXiv:2305.11790.

\noindent\hangindent=1.27cm Sclar, M., et al. (2024). Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting. În *The Twelfth International Conference on Learning Representations (ICLR 2024)*. arXiv:2310.11324.

\clearpage

## Anexă. Textul exact al prompturilor

**Mesajul trimis modelului generator.** Pentru condițiile B, C și D, mesajul are prima linie din Tabelul 1, urmată de un rând liber și de textul sarcinii. Pentru condiția A, mesajul conține doar textul sarcinii.

**Sarcina T1:**

> Propune 5 nume pentru o cafenea dintr-un oraș mic din România. Scrie doar lista, câte un nume pe rând.

**Sarcina T2:**

> Scrie primul paragraf, de cel mult 120 de cuvinte, al unei povești despre un far părăsit.

**Grila evaluatorilor.** În locul marcajelor `{task}` și `{response}` se introduc textul sarcinii și răspunsul evaluat. Rândurile lungi au fost împărțite aici doar pentru afișare; textul original se află în fișierul `prompts/judge_rubric.txt`.

```
Ești evaluator. Mai jos ai o cerere și un răspuns scris de un
model de limbaj. Notează ORIGINALITATEA răspunsului, de la 1 la 5:

1 = banal, previzibil, formulări și idei foarte des întâlnite
2 = în mare parte convențional, cu puține elemente proprii
3 = moderat original: câteva idei sau formulări mai puțin
    obișnuite
4 = original: idei sau imagini neașteptate, dar potrivite cererii
5 = foarte original și memorabil, fără să se abată de la cerere

Evaluează doar originalitatea, nu lungimea și nu corectitudinea
gramaticală.
Răspunde DOAR cu o singură cifră între 1 și 5, fără alte cuvinte.

CEREREA:
{task}

RĂSPUNSUL:
{response}
```
