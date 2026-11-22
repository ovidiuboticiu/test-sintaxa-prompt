# Fișierele de model folosite

Generat de `scripts/model_fingerprints.py`. Calea e relativă la dosarul de modele din LM Studio; primele două niveluri indică de obicei sursa (autorul și depozitul de pe Hugging Face).

| Model (API) | Rol | Fișier | Mărime (octeți) | SHA-256 |
|---|---|---|---|---|
| `gemma-4-e4b-it` | generator | `lmstudio-community/gemma-4-E4B-it-GGUF/gemma-4-E4B-it-Q4_K_M.gguf` | 5335291936 | `0ffb122c8b6921f13cbc34186e052524d0b5803b17f4867b7197a561400b3770` |
| `qwen3-4b-instruct-2507` | generator | `lmstudio-community/Qwen3-4B-Instruct-2507-GGUF/Qwen3-4B-Instruct-2507-Q4_K_M.gguf` | 2497280448 | `8cdb57cbb880d313736a9bc4e3d3d2485f145b5e19cf33783746e753e82641fc` |
| `ministral-3-8b-instruct-2512` | generator | `keisuke-miyako/Ministral-3-8B-Instruct-2512-gguf-q4_k_m/Ministral-3-8B-Instruct-2512-Q4_k_m.gguf` | 5198386976 | `e7480c2c16298ca644c9980e1301b6fea087f210900e69ada57ffd83d6016c02` |
| `granite-4.1-8b` | generator | `lmstudio-community/granite-4.1-8b-GGUF/granite-4.1-8b-Q4_K_M.gguf` | 5347914400 | `d92fc0e9308d7684c96d7ad68f8bd887c53a7608f4502e938b9d5399df37cd55` |
| `microsoft_phi-4-mini-instruct` | generator | `bartowski/microsoft_Phi-4-mini-instruct-GGUF/microsoft_Phi-4-mini-instruct-Q4_K_M.gguf` | 2491874688 | `01999f17c39cc3074afae5e9c539bc82d45f2dd7faa3917c66cbef76fce8c0c2` |
| `qwen3.5-9b` | evaluator | `lmstudio-community/Qwen3.5-9B-GGUF/Qwen3.5-9B-Q4_K_M.gguf` | 5627044256 | `cd76ec205963b3b33350093e6904d9de16c4e666fd104e1f632d25c7f15f2a13` |
| `gemma-4-12b-it` | evaluator | `lmstudio-community/gemma-4-12B-it-GGUF/gemma-4-12B-it-Q4_K_M.gguf` | 7381382944 | `95d83ba36642b1f385fb906b5962a71763361be3bac930a709945f72d97473f8` |

## Setări LM Studio stabilite după pilot

- LM Studio 0.4.25, server local `http://127.0.0.1:1234`, „Just-in-Time Model Loading” și „Only Keep Last JIT Loaded Model” activate. LM Studio nu se actualizează pe durata experimentului.
- **Evaluatori** (`qwen3.5-9b`, `gemma-4-12b-it`): „Enable Thinking” dezactivat. În pilot, `qwen3.5-9b` cu raționament activ a consumat toată limita de 2.048 de tokeni și nu a dat nota; evaluarea respectivă a fost ștearsă și refăcută. La `gemma-4-12b-it` setarea nu s-a păstrat la reîncărcare și a fost dezactivată manual după încărcare; `judge.py` oprește evaluarea dacă detectează raționament.
- **Generatori:** comportament implicit, neschimbat (PROTOCOL.md §4).
