# Rhin en Ocelotas: auditoría de la fuente y paso a Lean — 02-10-2026

Sexta tanda de [CST](LEEME.md). Responde al «siguiente» que dejó el 30-09:
auditar rango y constantes de Rhin contra la fuente original y estudiar su
descarga en Lean. Resultado en tres frases:

- **La fuente original no se pudo leer;** su umbral de validez sigue sin
  cotejar. Las citas que sí se leyeron confirman la forma y la constante.
- **En Lean la hipótesis es ahora la desigualdad real publicada**, sólo en el
  caso homogéneo y sólo para `H ≥ H0` con `H0 ≤ 131072`. El paso a la forma
  entera, antes hecho a mano, está demostrado
  ([OcelotasRhin.lean](OcelotasRhin.lean)).
- **La forma entera vale con aritmética exacta para todo `k` hasta un entero
  de 3010 cifras** ([certificado](verificar_rhin_convergentes.py),
  [salida](verificar_rhin_convergentes_salida.txt)). Eliminar Rhin del todo
  exige formalizar una medida de independencia lineal de `log 2, log 3`; la
  criba tolera exponentes hasta 100 ([tolerancia](tolerancia_rhin_salida.txt)).

## 1. Qué se consultó

| Fuente | Qué dice | Acceso |
|---|---|---|
| Rhin, *Approximants de Padé et mesures effectives d'irrationalité*, Progr. Math. 71 (1987) 155–164 | Original. La vista previa de Springer sólo trae pp. 155–156 (introducción y definiciones) | De pago; **la proposición de la p. 160 no se leyó** |
| Simons y de Weger, Acta Arith. 117 (2005) 51–70, lema 12 (preprint v1.44, 2010, en deweger.net) | `Λ > e^(−13,3(0,46057 + log K))`. Prueba: «We apply the Proposition on p. 160 of [Rh] with u0 = 0, H = u1 = K + L, and u2 = −K. Together with Lemma 8 the result follows.» | Leído |
| Q. Wu, Math. Comp. 72 (2003) 901–911, introducción | Rhin obtuvo una medida de independencia lineal de `1, log 2, log 3` menor que 7,616, en sentido asintótico (`H ≥ H0(ε)` efectivo, sin explicitar) | Leído |
| Rhin y Toffin, J. Number Theory 24 (1986) 284–297 | Aproximantes de Padé simultáneos de tipo II de `1, log(1+α_1 z), …, log(1+α_r z)`, con determinante explícito. Teorema 3, explícito para todo `H ≥ 1` (usa `d_n ≤ 2,826^n`): si `ω₁ = θ α^(r+1) Q^r 2,826^r < 1`, entonces `|Λ| ≥ c₁ H^(−μ₁)`. Corolario: `log|u0 + u1 log(3/4) + u2 log(5/4)| ≥ −(88 log H + 196)` | Leído (PDF aportado por el usuario el 02-10) |
| Hercher, JIS 26 (2023) 23.3.5 | No cita a Rhin; usa las cotas de Simons–de Weger | Leído |
| Proyecto Lean `justinalick/collatz-m-cycles-101-lean` | Toma la cota de Simons–de Weger como hipótesis `RhinBound`, sin descargarla | Leído (README) |

Lectura conjunta: hay dos resultados de Rhin. El exponente 7,616 es
asintótico y su `H0` no es explícito; el **13,3 de la p. 160 es la versión
explícita**, de la forma `|u0 + u1 log 2 + u2 log 3| ≥ H^(−13,3)` con
`H = max(|u1|, |u2|)`. Ninguna cita reproduce su umbral, y en la literatura de
ciclos `K > 10^10`, así que un umbral moderado pasaría inadvertido allí.

## 2. Constantes

- El `0,46057` de Simons–de Weger es `log(log2 3)`, ligeramente redondeado
  hacia arriba (`e^0,46057 = 1,584966 > 1,000001·log2 3`). Sale de su lema 8,
  `H = K + L < 1,000001·(log2 3)·K`, propio de los ciclos. **No es una
  constante de Rhin.**
- En Ocelotas, `u1 = k`, `u2 = −q`, y `H = max(k, q) = k` porque
  `2^q ≤ 3^q < 2^k`. Rhin da `Λ = k log 2 − q log 3 ≥ k^(−13,3)` sin factor
  adicional.
- `Δ = 2^k − 3^q = 3^q(e^Λ − 1) ≥ 3^q Λ ≥ 3^q k^(−13,3) ≥ 3^q k^(−14)`: es
  `RhinEntera`. El margen de 13,3 a 14 se pierde a propósito para trabajar con
  enteros. Este paso está ahora demostrado en Lean (`desde_homogenea`).

## 3. Rango

**La cadena de diez rachas sólo usa Rhin en `tiempo_diez`, para descartar
`k ≥ 131072`.** Por debajo, el tiempo ya es menor que el corte y la criba
finita no usa Rhin. Por eso basta la hipótesis desde `k = 131072`.

**Certificado por convergentes.** Si la forma entera fallara en `(k, q)` con
`k ≥ 2`, entonces `Λ k^14 < 1`. La fracción reducida `k'/q'` cumpliría
`|log2 3 − k'/q'| < 1/(2q'^2)` y, por Legendre, sería un convergente superior
de `log2 3` con `Λ' k'^14 < 1`. Basta pues revisar los convergentes.
[verificar_rhin_convergentes.py](verificar_rhin_convergentes.py) lo hace con
aritmética exacta:

1. Encierra `log2 3` con 20000 bits mediante cuadrados sucesivos de 3/2,
   sólo con enteros y redondeo dirigido.
2. Toma los 5779 cocientes parciales comunes a las dos cotas. La función
   `ln` del módulo `decimal` coincide en los 4816 primeros.
3. Certifica `log 2 > 0,693` con la serie de `exp` y su resto.
4. Comprueba `Λ p^14 ≥ 1` en los 2889 convergentes superiores. Los siete con
   `q ≤ 200000` también se comprueban con enteros exactos.

Resultado: la forma entera vale para todo `k ≤ p_5777`, un entero de 3010
cifras. El exponente efectivo `μ` (con `Λ = p^(−μ)`) vale como mucho 1,3121
en los convergentes con `p ≥ 1000`, lejos de 13,3. Un barrido exacto
`q ≤ 3000` da como menor cociente `(2^k − 3^q)k^14/3^q` el valor 5461, en
`q = 1`; el único caso de igualdad es el trivial `q = 0`.

Esto no es un teorema Lean. Reduce la dependencia de Rhin a `k > p_5777`,
salvo que su umbral fuera aún mayor.

## 4. Lean: [OcelotasRhin.lean](OcelotasRhin.lean)

Importa la cadena Ocelotas sin modificarla, y además
`Mathlib.Analysis.SpecialFunctions.Pow.Real`: sus 430 módulos se trajeron el
02-10 con `lake exe cache get`.

- `RhinProposicion H0`: `|u0 + u1 log 2 + u2 log 3| ≥ H^(−13,3)` para
  `H = max(|u1|, |u2|) ≥ H0`, con `rpow` real.
- `RhinHomogenea H0`: el caso `u0 = 0`. Vale con cualquiera de las dos
  lecturas de `H`, con o sin `|u0|`.
- `RhinDesde K0`: la forma entera sólo para `k ≥ K0`. Se tiene
  `RhinEntera ↔ RhinDesde 0` (`entera_iff_desde_cero`).
- `desde_homogenea : RhinHomogenea H0 → RhinDesde H0`. Es la traducción
  hecha antes a mano: logaritmos, `e^x ≥ 1 + x` y `k^(−14) ≤ k^(−13,3)`.
- `tiempo_diez_punto`, `tiempo_diez_desde`, `ocelotas_diez_desde`,
  `descenso_contador_desde` y `cst_contador_desde` repiten los cuerpos
  originales con la hipótesis puntual o con `RhinDesde 131072`.
- **`cst_rhin`**: si `H0 ≤ 131072` y vale `RhinHomogenea H0`, entonces para
  todo `n ≥ 2` con primer cruce `k` y como mucho diez rachas impares, la
  órbita no baja de `n` antes de `k` y `T^k(n) < n`. `cst_rhin_proposicion`
  es lo mismo con la proposición general; `fallo_exige_once_rhin` es el
  contrarrecíproco, y `desde_de_entera` muestra que la hipótesis nueva es más
  débil que la antigua.
- **`cst_rhin_tramo`** admite cualquier umbral `H0`. El tramo finito
  `131072 ≤ k < H0` de la forma entera pasa a ser una hipótesis aparte, que
  el certificado de la sección 3 comprueba para todo `H0 ≤ p_5777`. Si el
  umbral de Rhin fuera mayor que 131072, el teorema seguiría valiendo con
  ese certificado (`desde_tramo`).

Axiomas: `propext`, `Classical.choice`, `Quot.sound`
([registro](lean_rhin.txt)). Los ocho módulos anteriores se recompilaron en
la misma pasada, en este clon (Lean 4.32.2), y no cambian. Sus SHA256
difieren de los de [lean_contador.txt](lean_contador.txt) sólo por los
finales de línea: este clon usa `core.autocrlf=true`, y tras normalizar a LF
coinciden los ocho (`OcelotasCertificado.lean` ya está en CRLF en el
repositorio).

## 5. Estudio de la descarga

Eliminar la hipótesis exige demostrar en Lean una cota explícita
`|k log 2 − q log 3| ≥ c k^(−μ)` para todo `k ≥ K1`. Una cota exponencial
`Λ ≥ e^(−εk)` sólo serviría con `ε < 0,0019`, y no es más fácil de obtener.

**Tolerancia** ([tolerancia_rhin.py](tolerancia_rhin.py),
[salida](tolerancia_rhin_salida.txt), estimación): con `μ` hasta 20 la criba
actual casi basta; con `μ = 50` crece unas 7 veces y con `μ = 100` unas 30.
La constante `c` apenas influye, por ser logarítmica, y el tramo
`[k_max, K1)` lo cubre el certificado por convergentes. **Basta una medida
explícita mala.**

**Qué falta, en orden:**

1. Una prueba escrita estable de alguna medida explícita para `log 2, log 3`.
   La de Rhin usa polinomios optimizados por ordenador. Wu (2003) explica de
   dónde salen sus factores. Las rutas de Hata (1990, polinomios de tipo
   Legendre) y de Nikišin/Danilov son candidatas por revisar.
2. Su núcleo, que se formaliza: integrales de un polinomio entero sobre
   `[2,3]` y `[3,4]`, la cota de su tamaño, los denominadores (mínimo común
   múltiplo de `1..n`) y la no anulación de un determinante de dos formas
   consecutivas. Según una estimación a ojo, la prueba ingenua con `((x−2)(x−3)(x−4))^n/x^(n+1)`
   no basta: la pérdida aritmética, del orden de `e^(2n)·6^n`, supera la
   ganancia analítica, del orden de `0,16^n`.
3. El empalme con `cst_rhin`, que ya está preparado: basta producir
   `RhinDesde 131072`.

**Rhin–Toffin (1986) no basta para `log 2, log 3`.** Su teorema 3 es explícito
y elemental: Cauchy, integración por partes, `d_n ≤ 2,826^n` y un
determinante calculado mediante una integral de tipo Selberg. Es un buen
candidato a formalizar. Pero exige `|α_k| ≤ 1/(r+2)` y `ω₁ < 1`, y en el
grupo generado por 2 y 3 no hay ningún par que lo cumpla:
- el único par unimodular con denominador común, `3/4` y `9/8` (`Q = 8`),
  da `θ = 0,4619` y `ω₁ = 3,69`;
- la condición pide `c³/Q < 0,33` con `α = c/Q`, y sólo la cumplen `9/8` y
  `8/9`, que son dependientes.

Con las constantes leídas se reproduce su corolario (`μ₁ = 87,2`,
`c₁ ≈ e^(−195)` para `3/4, 5/4`). Para `log 2, log 3` hacen falta los
polinomios mejorados de Rhin (1987), cuya proposición de la p. 160 sigue sin
leerse. Rhin–Toffin cita también Rhin (1983), Progr. Math. 31, 247–258: otra
fuente posible para dos logaritmos.

**Sin Rhin fuera de Lean.** Con el certificado, la cola sólo empieza en
`k` de 3010 cifras. Allí basta la cota publicada de Laurent–Mignotte–
Nesterenko (1995), cuasipolinómica pero explícita y válida para todo `k`.
Así, el resultado de [17 rachas](RACHAS_CONVERGENTES.md), asistido por
cálculo, ya no usa Rhin. En Lean no basta: la cadena necesita `k^(−14)`
desde `k = 131072`, y LMN da allí del orden de `e^(−11800)`.

**Opción secundaria.** Mathlib tiene el teorema de Legendre
(`Real.exists_rat_eq_convergent`). Con encajes de `log 3` en Lean, el
certificado por convergentes podría entrar en Lean y subir el `H0` admisible.
No elimina Rhin; sólo protege frente a un umbral desconocido.

**Decisión del primer estudio:** no abrir la formalización (paso 2) sin el
paso 1 escrito. **Superado el mismo 02-10:** en vez de formalizar una medida
de independencia, [OcelotasLMN](LMN_LEAN.md) prueba en Lean CST hasta diez
rachas tomando como hipótesis la cota publicada de Laurent–Mignotte–
Nesterenko, con los convergentes de `log2 3` para el tramo intermedio. Rhin
deja de hacer falta en Lean; LMN sigue como hipótesis externa.

## Reproducir

```text
python -B -X utf8 verificar_rhin_convergentes.py   # unos 30 s
python -B -X utf8 tolerancia_rhin.py
python -B -X utf8 comprobar_rachas_lean.py --salida lean_rhin.txt   # unos 6 min
```

El comprobador necesita en la caché de Mathlib del proyecto de Gao el módulo
`Mathlib.Analysis.SpecialFunctions.Pow.Real`. Desde
`depuracion/gao20260920/formal`:
`lake exe cache get Mathlib.Analysis.SpecialFunctions.Pow.Real`.
