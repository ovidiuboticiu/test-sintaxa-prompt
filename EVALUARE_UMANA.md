# Instrucțiuni pentru evaluatorul uman

Evaluarea umană **nu face parte din experimentul inițial** și nu schimbă verdictul lui. Oricine o poate face ulterior pe datele publicate, ca să verifice dacă oamenii văd aceleași diferențe ca evaluatorii automați. Rezultatele se raportează separat.

## Ce primești

Fișierul `results/evaluare_umana.csv`, care se deschide în Excel. Are patru coloane:

| Coloană | Conținut |
|---|---|
| `cod` | Un cod de tipul R001, R002… |
| `cerere` | Ce i s-a cerut modelului |
| `raspuns` | Ce a răspuns modelul |
| `scor` | **Aici scrii nota ta, de la 1 la 5** |

Nu afli și nu trebuie să afli ce model sau ce variantă de prompt a produs fiecare răspuns. Asta e esența evaluării „oarbe”.

## Ce notezi

Doar **originalitatea** răspunsului față de cerere:

| Notă | Înseamnă |
|---|---|
| 1 | Banal, previzibil: idei și formulări foarte des întâlnite |
| 2 | Mai ales convențional, cu puține elemente proprii |
| 3 | Moderat original: câteva idei sau formulări mai puțin obișnuite |
| 4 | Original: idei sau imagini neașteptate, dar potrivite cererii |
| 5 | Foarte original și memorabil, fără să se abată de la cerere |

La listele cu nume de cafenea, notezi cât de neobișnuite și de inspirate sunt numele, luate împreună. La paragraful despre far, notezi cât de proaspete sunt ideile, imaginile și formulările.

## Ce NU notezi

- **Lungimea.** Un răspuns mai lung nu e automat mai bun.
- **Greșelile de limbă**, cât timp textul se înțelege.
- **Dacă respectă exact cerința** (de exemplu, 4 nume în loc de 5). Asta se măsoară separat, automat.
- **Liniile de tip „Mod creativ activat!”** sau alte comentarii ale modelului despre el însuși. Le ignori și notezi doar conținutul.

## Reguli de lucru

1. **Nu deschide fișierul `data/cheie_evaluare.csv`** până nu ai terminat de notat tot. El spune de unde vine fiecare răspuns.
2. **Nu încerca să ghicești varianta de prompt.** Dacă ți se pare că recunoști ceva, notează oricum doar originalitatea.
3. **Notează în ordinea din fișier**, fără să sari și fără să revii ca să „echilibrezi” notele.
4. **Citește întâi 5–10 răspunsuri fără să notezi**, ca să-ți faci o idee despre nivelul general. Apoi începe de la primul.
5. **Fă pauze.** După aproximativ 40 de răspunsuri atenția scade; e mai bine să continui altă dată.
6. **Salvează fișierul în același format** (CSV, separat prin punct și virgulă). Dacă Excel te întreabă, alege să păstrezi formatul CSV.

## Cât durează

Pentru un eșantion de 80 de răspunsuri (`python scripts/make_blind_sheet.py --n 80`), aproximativ o oră, cu pauze.

## Mai mulți evaluatori

Dacă vor să noteze mai multe persoane, fiecare primește propria copie a fișierului, notează independent și nu discută notele cu ceilalți până la final. Acordul dintre evaluatori e o informație utilă în sine.
