# Răspuns la auditul pre-execuție

Raportul auditorului e în `AUDIT_RAPORT.md` (verdict: „Necesită corecturi blocante”). Conform regulilor din `AUDIT.md`, au fost reparate doar observațiile blocante; nu urmează o a doua rundă de audit.

Fiecare observație blocantă a fost întâi verificată. B4, B5 și B6 au fost reproduse direct pe cod; B1, B2, B3, B7, B8 și B9 sunt corecte ca raționament. Toate au fost acceptate.

## Observații blocante

| Cod | Problema | Corectură |
|---|---|---|
| B1 | Regulile de interpretare atribuiau mecanisme („efectul vine din cuvânt”) pe baza unor rezultate nesemnificative și puteau produce afirmații contradictorii | §8 rescris: verdict global în trei variante (susținut / nesusținut / suspendat), rezultatele raportate separat pe P1 și P2, fără atribuirea unui mecanism și fără a trata „nicio diferență detectată” ca egalitate. `analyze.py` urmează noile reguli. |
| B2 | Permutarea ignora perechile definite de seed-ul comun | §7 și `analyze.py`: test de permutare **pe perechi** (același model, sarcină și repetiție), stratificat pe model; bootstrap pe perechi pentru P2; regulă fixă pentru perechile incomplete, raportate. Pe exemplul auditorului, p scade de la 0,196 la 0,0001. |
| B3 | Intervalul bootstrap pentru P1 subestima sistematic diversitatea | Intervalul pentru P1 a fost eliminat din protocol și din raport; rămân estimarea punctuală și testul de permutare. |
| B4 | Un contrast nedefinit (NaN) putea primi verdictul „B mai slab” sau putea decide verdictul global | Contrastele cu statistică nedefinită sau fără perechi într-un model sunt marcate **neestimabil**; o permutare nedefinită se numără ca extremă; orice contrast neestimabil sau model lipsă suspendă verdictul global. |
| B5 | Formule introductive („Sigur!”) erau numărate drept nume | Reguli noi de extragere (§6): dacă există linii numerotate sau cu buline, se folosesc doar acestea; altfel se exclud liniile terminate în „:”, „!” sau „?”. Verificat: aceleași nume dau aceeași extracție cu și fără introducere. |
| B6 | Parserul lua prima cifră din orice text („de la 1 la 5, dau 4” → 1) | E acceptat doar un răspuns format dintr-o singură cifră 1–5 (eventual cu punct); orice altceva e înregistrat ca invalid (§5, `judge.py`). |
| B7 | Eșecurile definitive nu erau înregistrate și se reîncercau la fiecare reluare | Cererile eșuate de 3 ori, cu serverul pornit, sunt salvate cu starea „eșuat” și nu se mai reîncearcă; dacă serverul e oprit, scriptul se oprește fără să marcheze eșecuri. Evaluarea se aplică doar generărilor reușite; eșecurile se raportează separat (`run_experiment.py`, `judge.py`, `status.py`, `analyze.py`, §4 și §7). |
| B8 | README anunța Python 3.9, dar analiza folosea o funcție din 3.10 | README cere Python 3.10+; în plus, corelația e calculată acum fără acea funcție. |
| B9 | Modelele nu erau identificate până la fișierul exact | Script nou, `model_fingerprints.py`, care înregistrează în `MODELE.md` fișierul GGUF și suma SHA-256 pentru fiecare model; se rulează după pilot, înainte de etichetă (§4, README). |

## Observații neblocante

| Cod | Tratament |
|---|---|
| N1 | Trecută la limite (§9); era deja acoperită de analiza de sensibilitate. |
| N2 | Eroare de fapt în README („160 de cereri” în loc de 800). Corectată, fiind o greșeală de documentație, nu o schimbare de design. |
| N3 | Raportul arată acum și numărul răspunsurilor cu un singur scor valid, cum promitea §5. Corectat odată cu B6, pentru că atinge același cod. |
| N4 | Trecută la limite (§9). |

Toate modificările au fost testate cap-coadă cu un server simulat, inclusiv cu cereri eșuate și scoruri invalide.
