# Ocelotas en Lean sin Rhin — 02-10-2026

Octava tanda de [CST](LEEME.md). [OcelotasLMN.lean](OcelotasLMN.lean) prueba
en Lean CST hasta diez rachas impares **sin la cota de Rhin**. La única
hipótesis externa es una forma debilitada del corolario 2 de Laurent,
Mignotte y Nesterenko (J. Number Theory 55, 1995, 285–321), un teorema
publicado de uso corriente. La proposición de Rhin de la p. 160, que no se
pudo leer ([auditoría](RHIN_LEAN.md)), deja de intervenir.

## Enunciado

```lean
def LMNDebil : Prop :=
  ∀ k q : ℕ, 2 ≤ k → 2 ^ k ≤ 2 * 3 ^ q → 3 ^ q < 2 ^ k →
    Real.exp (-(27 * (Real.log (2 * k) + 21) ^ 2)) ≤ (k : ℝ) * log 2 - q * log 3

theorem cst_lmn (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n
```

También `ocelotas_diez_lmn` (palabras `Palabra`) y `fallo_exige_once_lmn`.
Axiomas: `propext`, `Classical.choice`, `Quot.sound` ([registro](lean_lmn.txt)).

**Por qué `LMNDebil` se sigue de LMN.** El corolario da
`log|b2 log α2 − b1 log α1| ≥ −24,34 D^4 (max{log b' + 0,14, 21/D, 1/2})^2 log A1 log A2`
con `log A_i ≥ max{h(α_i), |log α_i|/D, 1/D}` y `b' = b1/(D log A2) + b2/(D log A1)`.

- Con `α2 = 2`, `b2 = k`, `α1 = 3`, `b1 = q` y `D = 1` se tiene
  `log A1 = log 3` y `log A2 = 1`. Como `q < 0,631 k`,
  `b' = q + k/log 3 ≤ 1,55 k ≤ 2k`, y `24,34·log 3 = 26,74 ≤ 27`.
- El máximo es como mucho `log(2k) + 21`.
- La versión de las notas de Evertse usa `log H(a_i)`. Da `b' ≤ 1,82 k` y el
  producto `log 2·log 3 = 0,76`, así que también implica `LMNDebil`.

Lean certifica el enunciado, no esta lectura de la fuente; queda para la
revisión humana.

## Prueba

La cadena antigua sólo usaba Rhin para descartar `q > 82696`. Ahora:

1. **`q ≤ 82696`**: la criba ya certificada (`criba_certificada`) y las
   semillas `n ≤ 11214` (`descenso_finito`), sin cambios.
2. **`82696 < q < 53715833`**: los convergentes 11 a 16 de `log2 3`.
   - `lagrange`: si `(P1, Q1)` y `(P2, Q2)` cumplen `P2 Q1 − P1 Q2 = ±1` y
     `L = a log 2 − b log 3` toma en ellos signos opuestos, entonces
     `|L P1 Q1| ≤ |L k q|` para todo `0 < q < Q2`. La prueba descompone
     `(k, q)` en la base unimodular, sin teoría de fracciones continuas.
   - Las cotas `log 2` y `log 3` con veinte cifras (`log_dos_cotas`,
     `log_tres_cotas`) salen de la serie de `log(1 − x)` con 64 y 42
     términos (`Real.abs_log_sub_add_sum_range_le`). Fijan los signos de
     `L_11, …, L_16` y dan `|L_j| > 10^-8` para `j = 11…15`.
   - Por tanto `Λ > 10^-8` y `3^q ≤ (2^k − 3^q)·10^8` (`cota_intervalo`).
     Con `fallo_producto` sale `n < 10^9 < 2^30`, y la criba da
     `q ≤ cota(10, 30) = 5317 < 82697`: contradicción.
3. **`q ≥ 53715833`**, luego `k ≥ 2^25`. Con `t = log2 k`,
   `log(2k) + 21 ≤ log 2·(t + 33)` y `27 log 2 ≤ 19` dan
   `Λ ≥ 2^(−19(t+33)^2)`. Así `n < 16·2^(19(t+33)^2)` y la criba da
   `k ≤ 364(19(t+33)^2 + 5) < 2^t` para `t ≥ 25` (`cola_diez_lmn`):
   contradicción.

## Por qué las comparaciones son reales y no enteras

Certificar el orden de los convergentes con `3^q` frente a `2^p` exigiría
números de `10^8` bits. Una prueba con `decide +kernel` sobre
`2^85137581 < 3^53715833` agotó la recursión del núcleo tras 5 minutos. Las
cotas de `log 2` y `log 3` con veinte cifras resuelven lo mismo en unos
30 s.

## Alcance

- Es el mismo teorema que `cst_contador` (Ocelotas, 30-09) y `cst_rhin`
  ([OcelotasRhin](OcelotasRhin.lean)), con una hipótesis distinta y mejor
  documentada.
- Hasta 17 rachas hay ya una prueba sin Lean ni Rhin
  ([séptima tanda](RACHAS_CONVERGENTES.md)). Formalizarla con este mismo
  esquema exige CST en el núcleo para `n < 4,7·10^6` (unas 400 veces el
  censo actual). Queda pendiente de decisión.
- **Trece rachas en Lean parecen asequibles** (estudio del 02-10, sin
  hacer). Bastaría la criba exacta para `q < 15601`, semillas `n < 40146`
  (3,6 veces el censo actual) e intervalos `j = 9…16`, con la cola desde
  `k ≥ 2^27`. Con las constantes 40147 (semillas) y 751 (`cota(13, m) ≤ 751 m`),
  el certificado simple sólo falla en `q = 11611`, que pediría un test más
  fino. Con 14 rachas las semillas suben a `7,7·10^5`.
- LMN no está formalizado en Lean, ni lo está ninguna cota de formas
  lineales en logaritmos conocida por el laboratorio.

## Reproducir

```text
python -B -X utf8 comprobar_rachas_lean.py --salida lean_lmn.txt   # unos 8 min
```

Necesita en la caché de Mathlib del proyecto de Gao los módulos
`Mathlib.Analysis.SpecialFunctions.Pow.Real` y
`Mathlib.Analysis.Complex.ExponentialBounds` (`lake exe cache get …`, 02-10).
