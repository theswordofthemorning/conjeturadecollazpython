# CST hasta 17 rachas por los convergentes de log2 3 — 02-10-2026

**Continuación, 03-10:** [RACHAS_AFINADAS.md](RACHAS_AFINADAS.md) recupera
el margen de los redondeos y eleva 17 a 18 y 73 a 75, sin ampliar censos.
El texto y los certificados de esta séptima tanda se conservan como
evidencia del resultado anterior.

Séptima tanda de [CST](LEEME.md). Usa el
[certificado por convergentes](RHIN_LEAN.md#3-rango) en lugar de una criba por
cada `q`. **Es una prueba asistida por cálculo exacto, no formalizada en
Lean.** Sus lemas estructurales sí lo están.

## Resultado

Sea `T(n) = n/2` o `(3n+1)/2`. Sea `k = τ(n)` el primer cruce del coeficiente
(`3^S_j ≥ 2^j` para `1 ≤ j < k` y `3^S_k < 2^k`), y sea `q = S_k(n)`.

**Teorema.** Todo `n ≥ 2` con `τ(n)` finito
y como mucho **17 rachas impares** en sus `k` primeros pasos cumple
`T^k(n) < n`; por tanto vale CST (`t(n) = τ(n)`). En la cola, para `k` de
más de 3010 cifras, se usa la cota publicada de Laurent, Mignotte y
Nesterenko (1995) en una forma debilitada; sirve igual Rhin. **Ya no se
necesita la proposición de Rhin que no se pudo leer.** Si se toma además como
hipótesis el corolario 5.4 de Rozier y Terracol (CST comprobada para
`2 ≤ n ≤ 2,8·10^19`, arXiv:2502.00948v5, que se apoya en tablas externas de
récords), lo mismo vale con como mucho **73 rachas**.

Antes: hasta 10 rachas, en Lean y bajo Rhin desde `k ≥ 131072`
([OcelotasRhin](OcelotasRhin.lean)). La exploración aproximada del 30-09
([r_rachas_fino](r_rachas_fino_salida.txt)) llegaba a 20 sin certificado.

## Prueba

Sea un fallo, `T^k(n) ≥ n`, con `r ≤ R` rachas. El caso par desciende en un
paso (`descenso_par`), así que `n` es impar. Sea `Λ = k log 2 − q log 3`.

1. **Semilla acotada por `Λ`.** Por `fallo_producto` (Lean),
   `(2^k − 3^q) n < r 3^q`. Como `(2^k − 3^q)/3^q = e^Λ − 1 ≥ Λ`, sale
   `n < R/Λ`.
2. **Criba de las rachas.** Por `criba_desde_trayectoria` y `cota_monotona`
   (Lean), si `n + 1 < 2^m`, entonces `q ≤ cota(R, m)`. Aquí `cota` es la
   recursión entera `cota(r+1, m) = ⌊(5m + 8 cota(r, m) − 1)/5⌋`.
3. **Mejor aproximación** (Lagrange, clásico). Si `q_j ≤ q < q_(j+1)`, con
   `q_j` los denominadores de los convergentes de `α = log2 3` y `j ≥ 1`,
   entonces `‖qα‖ ≥ ‖q_j α‖ > 1/(q_j + q_(j+1))`. Como
   `Λ = log 2·(1 − {qα}) ≥ log 2·‖qα‖`, en ese intervalo `n < s_j`, con
   `s_j = R(q_j + q_(j+1))/log 2`.
4. **Intervalos.** Con `m_j` la longitud en bits de `⌈s_j⌉`, un fallo con
   `q` en el intervalo `j` exige `q ≤ cota(R, m_j)`. Si `cota(R, m_j) < q_j`,
   el intervalo queda vacío. Si no, sus semillas cumplen `n < s_j`.
5. **Cola.** Para `q ≥ q_5778` hacen falta `k ≤ 2q` (`tiempo_por_impares`)
   y `cota(R, m) ≤ G_R m`, con `G_R = 5(8^R − 5^R)/(3·5^R)`.
   - **Con Laurent–Mignotte–Nesterenko** (J. Number Theory 55, 1995,
     corolario 2): con `a1 = 2`, `a2 = 3`, `D = 1`, `log A1 = 1`,
     `log A2 = log 3` y `b' ≤ 2k`, da `log Λ ≥ −30(log(2k) + 21)^2`. Esta
     forma vale también con la versión de las notas de Evertse, que usa
     `log H(a_i)`. Entonces `n < R e^E`, con `E = 30(log 4q + 21)^2`, y un
     fallo exige `q ≤ G_R m(q)`, con `m(q)` de unos `E/log 2` bits. Esa
     función de `q` crece mucho más despacio que `q` y queda por debajo
     desde `q_5778`. Se comprueba con `log 2 ∈ (0,693; 0,6932)`, certificado
     por series.
   - **Con Rhin:** `n < R k^14`, la misma comprobación con `14 log2(2q)`.
6. **Cierre.** Todo fallo con `r ≤ R` tiene `n < N_R`, el máximo de los `s_j`
   que sobreviven. Si CST está comprobada para `2 ≤ n < N_R`, no hay fallo.

Los cálculos son exactos: cocientes certificados, `log 2 > 693/1000` y la
recursión entera.

## Números ([rachas_convergentes.py](rachas_convergentes.py), [salida](rachas_convergentes_salida.txt))

| R | N_R | Intervalo decisivo | Comprobación que cierra |
|---|---|---|---|
| 6 | 8407 | `q_7 = 306` | también las semillas Lean (`n ≤ 11214`) |
| 10 | 234 719 | `q_8 = 665` | barrido propio |
| 17 | 4 674 068 | `q_11 = 79335` | barrido propio, `n < 2^23 = 8 388 608` |
| 18 | 280 033 091 | `q_13 = 190537` | ya no cierra el barrido propio |
| 73 | 1,44·10^19 | `q_32 = 6 234 549 927 241 963` | Rozier–Terracol, `n ≤ 2,8·10^19` |
| 74 | 4,25·10^19 | `q_33 = 130 441 933 147 714 940` | no cierra |

El salto de 17 a 18 lo produce el convergente `301994/190537`, seguido del
cociente parcial 55. Es el mismo `j1 = 301 994` del teorema 5.3 de
Rozier–Terracol. La exploración del 30-09 usaba el factor `r + 1` en lugar de `r`
y el `Λ` exacto de cada `q`. Sus `n_max` para `r = 18, 19, 20` quedan un 5 %
por encima de los nuestros, como cabe esperar de esas dos diferencias.

## Cotejo independiente ([script](cotejo_rachas_convergentes.py), [salida](cotejo_rachas_convergentes_salida.txt))

- CST directa, con código nuevo, para `2 ≤ n < 4 674 093`: sin fallos; el
  mayor primer cruce es 224 (`n = 1 126 015`). El barrido del 30-09 llegaba
  a `2^23` ([salida](verificar_r_rachas_23_salida.txt)).
- La desigualdad de mejor aproximación, comprobada para todo
  `1 ≤ q ≤ 200000` con el encierro racional: lo más justo es el propio
  convergente `q = 190537`, con cociente 1,0034.
- La cota de `Λ` con enteros exactos (`Λ ≥ Δ/2^k`) para `q ≤ 3000`.

## Coherencia con los ciclos

Sea `n` el mínimo de un ciclo no trivial con `K` impares, longitud `L` y `m`
rachas impares (los `m`-ciclos de Simons–de Weger). Como `3^K < 2^L`,
`τ(n) ≤ L`, y la palabra hasta `τ(n)` tiene a lo sumo `m` rachas. Pero la
órbita nunca baja de `n`, así que CST falla en `n`. Por tanto el teorema
implica que no hay `m`-ciclos con `m ≤ 17`, o `m ≤ 73` con Rozier–Terracol.
La literatura ya lo da con más (Simons–de Weger, `m ≤ 75`; Hercher 2023,
`m ≤ 91`). Que la escala coincida es el control esperado: el método es el
suyo, trasladado al primer cruce, como propone la observación 5.5 de
Rozier–Terracol.

## Novedad

Búsqueda rápida del 02-10, sin MathSciNet ni Scholar. Nadie parece haber
seguido la observación 5.5 de Rozier–Terracol (CST por número de máximos
locales). arXiv:2605.13886 está retirado (ver la [ficha](LEEME.md)), y
arXiv:2607.24844 (Fernández e Ibáñez, palabras de Christoffel) estudia el
mínimo de los ciclos, no CST. **La novedad no está certificada.**

## Alcance y límites

- No demuestra CST: sigue abierto un fallo con 18 rachas o más. El barrido
  hasta `2^23` muestra semillas con hasta 61 rachas, así que el corte es
  real.
- **Hipótesis externas:** la cota de Laurent–Mignotte–Nesterenko (o Rhin),
  sólo para `k` de más de 3010 cifras, y el teorema clásico de Lagrange.
  Ninguno está formalizado. La cadena Lean de diez rachas sigue usando Rhin
  desde `k ≥ 131072`: allí LMN es demasiado débil, porque da del orden de
  `e^(−11800)` frente al `k^(−14) ≈ e^(−165)` que exige la forma entera.
- **Lean.** Para diez rachas, el mismo esquema ya está en Lean sin Rhin
  ([octava tanda](LMN_LEAN.md)). Para 17, formalizarlo exige los
  convergentes de `log2 3` hasta
  `q ≈ 1,5·10^6` (encajes de `log 2` y `log 3` con unas 16 cifras), Legendre
  (en Mathlib) o la mejor aproximación, y CST para `n < 4,7·10^6` en el
  núcleo. Este último censo multiplicaría por unas 400 el de `n ≤ 11214`. No
  se emprende sin decisión.
- Con 73 rachas, la hipótesis de Rozier–Terracol es un cálculo externo: sólo
  enmarca el alcance del método.
