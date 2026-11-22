# Audit pre-execuție

Acest fișier descrie auditul făcut **înainte** de eticheta `preinregistrare-v1` și înainte de colectarea datelor. Auditul are o singură rundă.

## Pentru auditor

Ai acces la tot repozitoriul. Citește `README.md` și `PROTOCOL.md`, apoi codul din `scripts/` și fișierele din `prompts/`. Poți rula scripturile; fără LM Studio, `run_experiment.py --dry-run` și `status.py` funcționează și fără server.

Răspunde **doar** la aceste cinci întrebări:

1. **Design:** testează cele patru condiții (A, B, C, D) ceea ce pretinde protocolul? Lipsește un control fără de care concluzia din §8 nu ar fi justificată?
2. **Cod vs. protocol:** fac scripturile exact ce descrie protocolul (condiții, seed-uri, ordine, număr de rulări, extragerea numelor, scoruri, teste, corecție Holm, reguli de decizie)?
3. **Orbire:** există vreo cale prin care evaluatorii automați află condiția sau modelul generator, în afara conținutului răspunsului însuși?
4. **Statistică:** sunt testele și regulile de decizie potrivite pentru întrebare și aplicate simetric (același prag pentru rezultat favorabil și nefavorabil)?
5. **Reproductibilitate:** poate o persoană din afară să repete experimentul doar pe baza `README.md`?

## Cum clasifici fiecare observație

- **BLOCANTĂ:** poate schimba verdictul sau îl poate face neinterpretabil. Explică exact cum.
- **NEBLOCANTĂ:** orice altceva (stil, îmbunătățiri posibile, limite deja declarate).

Pentru fiecare observație BLOCANTĂ indică fișierul, linia sau secțiunea, și o corectură minimă. Nu propune extinderi ale experimentului (alte modele, alte sarcini, alte măsuri); acestea sunt NEBLOCANTE prin definiție.

Dacă nu găsești nimic blocant, spune explicit: „Nicio observație blocantă.”

## Reguli de oprire (stabilite dinainte)

1. Se repară **doar** observațiile BLOCANTE.
2. Observațiile NEBLOCANTE se trec, pe scurt, la „Limite” în `PROTOCOL.md`, fără alte modificări.
3. După reparații se pune eticheta `preinregistrare-v1`. **Nu urmează o a doua rundă de audit.**
4. După colectarea datelor nu se mai modifică nimic din protocol sau din analiză.

Raportul auditorului se salvează în `AUDIT_RAPORT.md`.
