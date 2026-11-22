# Raport — testul sintaxei de prompt

> **DATE PILOT** — doar verificarea funcționării. Fără valoare statistică.

Rulări reușite: 40; eșuate definitiv: 0. Modele generatoare: `gemma-4-e4b-it`, `qwen3-4b-instruct-2507`, `ministral-3-8b-instruct-2512`, `granite-4.1-8b`, `microsoft_phi-4-mini-instruct`. Evaluatori: `qwen3.5-9b`, `gemma-4-12b-it`.

## Descriere pe model și condiție

| Model | Cond. | T1 diversitate nume | T1 exact 5 nume | T1 scor | T2 scor | T2 distinct-2 | Cuvinte T2 | Menționează comanda | Trunchiate | Eșuate |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma-4-e4b-it | A | 1.000 | 1/1 | 3.50 | 3.50 | 1.000 | 90.0 | 0 | 0 | 0 |
| gemma-4-e4b-it | B | 1.000 | 1/1 | 2.50 | 3.00 | 1.000 | 91.0 | 0 | 0 | 0 |
| gemma-4-e4b-it | C | 1.000 | 1/1 | 2.50 | 3.50 | 0.989 | 93.0 | 0 | 0 | 0 |
| gemma-4-e4b-it | D | 1.000 | 1/1 | 2.50 | 3.50 | 0.979 | 94.0 | 0 | 0 | 0 |
| qwen3-4b-instruct-2507 | A | 1.000 | 1/1 | 3.00 | 3.50 | 0.992 | 120.0 | 0 | 0 | 0 |
| qwen3-4b-instruct-2507 | B | 1.000 | 1/1 | 3.00 | 4.00 | 0.965 | 115.0 | 0 | 0 | 0 |
| qwen3-4b-instruct-2507 | C | 1.000 | 1/1 | 3.50 | 4.00 | 0.991 | 117.0 | 0 | 0 | 0 |
| qwen3-4b-instruct-2507 | D | 1.000 | 1/1 | 4.00 | 4.00 | 0.968 | 126.0 | 0 | 0 | 0 |
| ministral-3-8b-instruct-2512 | A | 1.000 | 1/1 | 3.50 | 4.00 | 0.993 | 153.0 | 0 | 0 | 0 |
| ministral-3-8b-instruct-2512 | B | 1.000 | 1/1 | 2.50 | 4.00 | 0.992 | 121.0 | 0 | 0 | 0 |
| ministral-3-8b-instruct-2512 | C | 1.000 | 1/1 | 3.50 | 4.00 | 0.993 | 140.0 | 0 | 0 | 0 |
| ministral-3-8b-instruct-2512 | D | 1.000 | 1/1 | 4.00 | 4.00 | 0.989 | 172.0 | 0 | 0 | 0 |
| granite-4.1-8b | A | 1.000 | 1/1 | 2.00 | 2.00 | 1.000 | 144.0 | 0 | 0 | 0 |
| granite-4.1-8b | B | 1.000 | 1/1 | 2.50 | 2.50 | 0.991 | 113.0 | 0 | 0 | 0 |
| granite-4.1-8b | C | 1.000 | 1/1 | 3.00 | 3.00 | 1.000 | 92.0 | 0 | 0 | 0 |
| granite-4.1-8b | D | 1.000 | 1/1 | 2.50 | 2.50 | 1.000 | 119.0 | 0 | 0 | 0 |
| microsoft_phi-4-mini-instruct | A | 1.000 | 1/1 | 4.00 | 1.00 | 0.518 | 735.0 | 0 | 1 | 0 |
| microsoft_phi-4-mini-instruct | B | 1.000 | 0/1 | 2.00 | 2.00 | 0.990 | 195.0 | 0 | 0 | 0 |
| microsoft_phi-4-mini-instruct | C | 1.000 | 1/1 | 2.50 | 2.00 | 0.951 | 258.0 | 0 | 0 | 0 |
| microsoft_phi-4-mini-instruct | D | 1.000 | 1/1 | 1.50 | 2.00 | 0.975 | 193.0 | 0 | 0 | 0 |

## Scorurile evaluatorilor

- `qwen3.5-9b`: 40 valide, 0 invalide, 0 eșuate.
- `gemma-4-12b-it`: 40 valide, 0 invalide, 0 eșuate.
- Răspunsuri cu ambele scoruri valide: 40; cu un singur scor valid: 0; fără niciun scor valid: 0.
- Acordul evaluatorilor: corelație Pearson 0.40, acord exact 42%.

## Numele extrase la T1 (verifică manual extragerea)

- `pilot-gemma-4-e4b-it__T1-A-01`: ['cantoanele cafelei', 'pauza de bucurie', 'cafeneaua de la valea', 'maretia grautatilor', 'ora si cupa']
- `pilot-gemma-4-e4b-it__T1-B-01`: ['pauza de cafea', 'sub copacul vechi', 'cafeneaua de cuvinte', 'aura timpurilor', 'in cotul orasului']
- `pilot-gemma-4-e4b-it__T1-C-01`: ['pauza de la carti', 'oreile de aur', 'bucataria de suflet', 'cartureasca', 'sub umbra copacilor']
- `pilot-gemma-4-e4b-it__T1-D-01`: ['pauza', 'dimineata in oras', 'coltul strazii', 'targul de veara', 'carti si cafea']
- `pilot-granite-4.1-8b__T1-A-01`: ['casa de cazare pacii', 'mielul de la vale', 'sistemul de gaze', 'cornul zilei', 'trandafirul alb din brasov']
- `pilot-granite-4.1-8b__T1-B-01`: ['cafe cotidian', 'miorita express', 'bucurestiu sons', 'cornul de cafea', 'zorilor in deal']
- `pilot-granite-4.1-8b__T1-C-01`: ['cafe cotnari charm', 'bucareanu s hearth', 'transilvania whisper', 'valea florilor brew', 'miorita s nook']
- `pilot-granite-4.1-8b__T1-D-01`: ['cafe cotnari', 'trandafiri de la satu mare', 'aroma moldovei', 'sutlenii cafenelelor', 'cornul romaniei']
- `pilot-microsoft_phi-4-mini-instruct__T1-A-01`: ['cafe galata', 'espresso central', 'la babele', 'colectorul de ceeaunti', 'rosu cerbul brasovean']
- `pilot-microsoft_phi-4-mini-instruct__T1-B-01`: ['bimbach serenade', 'aroma bucovinei', 'vasile alecsandri haven', 'pamantul negru de latte', 'tranquilitate carpatilor', 'sunet albaura', 'cimpia cerului costei', 'nostalgie sucevei', 'oasele munteniei', 'cantemir s corner']
- `pilot-microsoft_phi-4-mini-instruct__T1-C-01`: ['bunea vanturilor', 'casa aromelor', 'caffe natura', 'espresso minuna', 'pulcheria lattea']
- `pilot-microsoft_phi-4-mini-instruct__T1-D-01`: ['bucovina bunsen', 'transilvania timeless', 'maramures morning brew', 'crisana aroma', 'harghita haven']
- `pilot-ministral-3-8b-instruct-2512__T1-A-01`: ['ceaiul cu vant', 'sub lampile vechi', 'cafeneaua de la coltul pietrelor', 'mica caldura a casei', 'cuptorul lui popa']
- `pilot-ministral-3-8b-instruct-2512__T1-B-01`: ['mandrusorul de ceai', 'pamanturi vapor', 'cafeneaua cu clopote', 'sageata si faina', 'ulita cu melci']
- `pilot-ministral-3-8b-instruct-2512__T1-C-01`: ['padurea zambetelor', 'varful aromelor', 'cafenea de la coltul focului', 'sticla plina de noroi', 'lampile de la etajul al doilea']
- `pilot-ministral-3-8b-instruct-2512__T1-D-01`: ['vorbarea de la colt', 'foaia de ceai si paine', 'luminica', 'deasupra zgomotului', 'casuta cu ceai si nori']
- `pilot-qwen3-4b-instruct-2507__T1-A-01`: ['cafea in padure', 'barbatul cu ceai', 'orasul de peste deal', 'fumatorii din munte', 'ziua de dimineata']
- `pilot-qwen3-4b-instruct-2507__T1-B-01`: ['cafea vintata', 'piatra de sus', 'orasul cu caldura', 'barbatul de la bucuresti', 'sfarsitul zilei']
- `pilot-qwen3-4b-instruct-2507__T1-C-01`: ['cafea in padure', 'bautura de tufa', 'ziua cu barbatul', 'mica caldura', 'piatra cu mana']
- `pilot-qwen3-4b-instruct-2507__T1-D-01`: ['cafea cu pasari', 'bautura de varf', 'marele sfant caiet', 'ziua noastra', 'orasul pe care l au facut']

## Răspunsurile evaluatorilor (primele caractere)

- `qwen3.5-9b` → scor 4: `'4'`
- `qwen3.5-9b` → scor 3: `'3'`
- `qwen3.5-9b` → scor 2: `'2'`
- `qwen3.5-9b` → scor 3: `'3'`
- `gemma-4-12b-it` → scor 4: `'4'`
- `gemma-4-12b-it` → scor 2: `'2'`
- `gemma-4-12b-it` → scor 3: `'3'`
- `gemma-4-12b-it` → scor 4: `'4'`
