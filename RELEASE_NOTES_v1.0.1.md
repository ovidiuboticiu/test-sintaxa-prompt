# Versiunea 1.0.1 — 25 noiembrie 2026

Revizuire editorială a raportului științific, după o evaluare independentă făcută de ChatGPT (OpenAI) la cererea autorului. Toate observațiile au fost verificate înainte de implementare. **Datele, protocolul preînregistrat, eticheta `preinregistrare-v1`, rezultatele statistice primare și verdictul nu s-au schimbat.** Versiunea 1.0.0 rămâne disponibilă ca istoric.

## Corecturi de interpretare

- Formulările care tratau lipsa unei diferențe semnificative ca egalitate („nu s-a deosebit”, „nu a adus nimic în plus”) au fost înlocuite cu formulări calificate statistic: față de placebo nu s-a detectat o diferență semnificativă, ceea ce nu demonstrează echivalența și nu exclude diferențe mici.
- A fost eliminată o comparație nejustificată între intervalele de încredere ale contrastelor B–D și B–C.
- Se precizează că un contrast semnificativ ar fi arătat o diferență de comportament, nu un mecanism intern.
- Preînregistrarea este descrisă cu limita ei: protocolul a fost fixat într-un repozitoriu atunci privat, deci eticheta și data release-ului nu sunt o dovadă externă independentă a cronologiei (raport, secțiunea 3.7; README).
- A fost corectată contradicția privind numărul rulărilor analizei (secțiunea 3.7 vs. secțiunea 7).
- Evaluatorii: au aceeași direcție la toate contrastele, dar diferă ca mărime și semnificație (corectat în secțiunea 4.6); preferința pentru propria familie nu mai este prezentată ca afectând egal toate condițiile.
- Limite noi menționate: dependența indicatorului P1 de numărul de nume extrase; faptul că B și D conțin un cuvânt englezesc, iar C e în română; P2 ca măsură operațională a originalității.

## Adăugiri

- Figura 1: diferențele de originalitate și intervalele de încredere (forest plot).
- Secțiunea 4.8 și Tabelul 11: analiză exploratorie, nepreînregistrată, a originalității fără Phi-4 mini. Concluziile rămân aceleași (B–A +0,319; B–C −0,238; B–D +0,088, nesemnificativ). Cifrele au fost verificate independent.
- Bibliografia: autori compleți, precizarea contextului cifrelor citate (LLaMA-2-13B; GPT-3.5-turbo la traducerea codului; CodeGen și BLOOM) și linkuri active.

## Prezentare

- Numele modelului este repetat pe fiecare rând în Tabelele 4 și 5, astfel încât tabelele rămân lizibile când se continuă pe pagina următoare.
- În rezumat, diferențele negative sunt etichetate explicit ca „B minus C”.
- Calendarul studiului devine Tabelul 12. Raportul are acum 23 de pagini.
