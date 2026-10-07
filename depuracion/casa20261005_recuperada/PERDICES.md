# Perdices: el lado 3-ádico de la órbita

05-10-2026. Ruta B, primer paso hacia Tao (2019), con presupuesto
acotado. La parte formal está en Lean 4.32.2 sin hipótesis externas, con
axiomas estándar ([CasaTres.lean](CasaTres.lean)). La parte de mezcla
fina es una medición.

## Por qué hace falta

[Chinchillas](CHINCHILLAS.md#la-barrera-de-los-métodos-2-ádicos) mostró
la barrera de Korec. Con sólo `n mod 2^k` no se baja de
`n^(log 3/log 4)`. Tao (2019) probó que casi toda órbita alcanza valores
casi acotados, por debajo de cualquier `f(n) → ∞`. Para eso mira además
`T^k(n) mod 3^j`. Esta nota fija el puente entre los dos lados y
delimita lo que falta.

## Lo que está en Lean

| Teorema | Enunciado |
|---|---|
| `iter_afin` | identidad afín: `T^k(r + 2^k t) = T^k(r) + 3^(S_k(r)) t` |
| `S_afin` | las subidas no cambian a lo largo de la progresión |
| `tres_determinado` | `T^k(n) ≡ T^k(n mod 2^k) (mod 3^(S_k(n)))`: el lado 2-ádico fija el residuo módulo `3^S` |
| `fibra_contenida`, `fibra_inyectiva` | en la clase `r mod 2^k`, con `S = S_k(r) ≤ j`, los `t < 3^(j−S)` dan valores distintos de `T^k` módulo `3^j`, todos en la fibra de `T^k(r)` módulo `3^S` |
| `paridad_independiente` | si `m ≤ S_k(r)`, las subclases `r` y `r + 2^k` dan el mismo `T^k` módulo `3^m` y paridades opuestas |
| `T_mod_tres` | `2 T(x) ≡ x` o `3x + 1` (mod `3^m`), según la paridad de x |
| `sin_multiplos_de_tres` | tras la primera subida, la órbita nunca vuelve a un múltiplo de 3 (`T_impar_mod_tres`: tras una subida, el valor es `≡ 2 mod 3`) |

## La cadena en `ℤ/3^m`

Sea r uniforme módulo `2^(k+1)` y fijemos su clase módulo `2^k`, con
`S_k ≥ m`. Por `paridad_independiente`, la paridad de `T^k(r)` es una
moneda justa independiente de `T^k(r) mod 3^m`. Por `T_mod_tres`, el paso
siguiente hace `X ↦ X/2` o `X ↦ (3X+1)/2` en `ℤ/3^m`, donde dividir por 2
es multiplicar por `(3^m+1)/2`. Así, `T^k(r) mod 3^m` sigue la cadena de
Markov de esas dos ramas con monedas justas.

El enunciado exacto también está en Lean
([CasaCadena.lean](CasaCadena.lean)):

| Teorema | Enunciado |
|---|---|
| `cadena_correcta` | `T^k(n) mod 3^m` es la cadena seguida a lo largo de la palabra de paridades de n, empezada en `n mod 3^m` |
| `palabra_congr`, `congr_de_palabra` | la palabra de los k primeros pasos depende sólo de `n mod 2^k` y la determina |
| `palabra_sobre`, `palabra_inyectiva` | `c ↦ palabra_k(c)` es una biyección de `[0, 2^k)` en las palabras de longitud k |
| `ley_de_la_cadena` | para r uniforme en `[0, 2^k 3^m)`, `T^k(r) mod 3^m` tiene exactamente la ley de la cadena con palabra uniforme y punto de partida uniforme |

La prueba usa el teorema chino del resto: `r ↦ (r mod 2^k, r mod 3^m)`
es una biyección (`coordenadas_inyectivas`).

La ley estacionaria `ν_m` de la cadena es la versión, para el atajo, de
la variable de Syracuse de Tao:
`∑_{l≥1} 3^(l−1) 2^−(a_1+…+a_l)`, con huecos `a_l ≥ 1` geométricos. Su
función característica cumple
`φ_m(ξ) = φ_m(hξ)/2 + e(hξ/3^m) φ_(m−1)(hξ)/2`, con `h = 2^−1 mod 3^m`.
Esto está comprobado numéricamente para `m ≤ 10`, con error máximo
`3,6·10⁻¹⁶`.

## Lo que falta: la mezcla fina

Lo que Tao necesita, escrito en nuestro lenguaje:

- **Proposición 1.17 de Tao.** Para todo A,
  `max_{3∤ξ} |φ_m(ξ)| = O_A(m^−A)`.
- **Proposición 1.14 de Tao.** La oscilación fina
  `osc(m′, m) = ∑_y |ν_m(y) − ν_m′(y mod 3^m′)/3^(m−m′)|` es
  `O_A(m′^−A)`, uniforme en `m ≥ m′`.

Las dos son enunciados sobre la cadena afín aleatoria y no usan la
dinámica de Collatz. Después, el argumento principal de Tao (primer paso
por debajo de `N^α` y estabilización) convierte la mezcla en «casi toda
órbita alcanza valores casi acotados». Las dos partes ocupan varias
secciones del artículo de Tao, y su formalización excede este
presupuesto.

**Por qué no sale gratis.** Desenrollar la recurrencia dos niveles da
`|φ_m(ξ)| ≤ c(ξ) · max|φ_(m−2)|`, con
`c(ξ) = ∑_{s≥2} 2^−s |∑_{j<s} e(h^j ξ/3^m)|`. Los factores `h^j ξ`
recorren la inversa de la duplicación del círculo, así que `c(ξ) < 1`
para cada ξ. Pero c(ξ) se acerca a 1 sin cota uniforme: si `hξ ≡ 2^t`,
las primeras t fases quedan casi alineadas. Ese es el obstáculo que Tao
vence con un argumento combinatorio sobre muchas escalas a la vez. Es un
cálculo a mano, no está en Lean.

## Medición

[medir_mezcla_tres.py](medir_mezcla_tres.py)
([salida](medicion_mezcla_tres.json)). Ley estacionaria exacta de la
cadena para `m ≤ 14` (hasta 4 782 969 estados) y conteo directo con
`k = 20`.

| m | `max_{3∤ξ} |φ_m(ξ)|` | `osc(m−1, m)` | `osc(1, m)` |
|---|---|---|---|
| 1 | 0,577 | — | — |
| 2 | 0,378 | 0,476 | 0,476 |
| 4 | 0,177 | 0,343 | 0,701 |
| 7 | 0,0759 | 0,235 | 0,776 |
| 10 | 0,0383 | 0,178 | 0,813 |
| 14 | 0,0191 | 0,130 | 0,840 |

- **Fourier.** El máximo baja de `1/√3` a 0,019. Las razones sucesivas
  suben de 0,65 a 0,87, así que el decaimiento no es claramente
  exponencial. El exponente polinómico efectivo crece de 1,5 (de m = 4 a
  8) a 2,0 (de m = 7 a 14). Es compatible con el `O_A(m^−A)` para todo A
  de Tao.
- **Oscilación.** `osc(m−1, m)` baja despacio, de 0,48 a 0,13: la cifra
  más fina se mezcla, pero lentamente. `osc(1, m)` sube hacia 0,84,
  porque módulo `3^m` la ley está lejos de la elevación uniforme de la
  ley módulo 3. Eso es lo esperado: para `m′ = 1` la cota de Tao es sólo
  una constante.
- **Módulo 3.** La ley es `(0, 1/3, 2/3)`.
- **Dos cálculos independientes.** El conteo directo de los `r < 2^20`
  con `S ≥ 7` queda a distancia total 0,040 de `ν_7`; la diferencia es
  efecto de k finito. Las oscilaciones por conteo coinciden en tendencia.

## Contraste independiente

[cotejar_cadena.py](cotejar_cadena.py) ([salida](cotejo_cadena.json)):
546 000 casos de `cadena_correcta`, la biyección de palabras para
k ≤ 14 y la ley de la cadena valor por valor en 45 pares (k, m) con
k ≤ 8 y m ≤ 4.

[cotejar_tres.py](cotejar_tres.py) ([salida](cotejo_tres.json)), por
órbitas directas:

| Lema | Casos |
|---|---|
| `iter_afin` | 655 320 |
| `tres_determinado` | 620 000 |
| fibras | 32 764 |
| `paridad_independiente` | 1 114 112 |
| `sin_multiplos_de_tres` | 1 179 950 |

## Conclusión del presupuesto

El puente formal entre el lado 2-ádico y el 3-ádico está hecho, con la
ley exacta de la cadena. Lo que
falta para saltar la barrera de Korec es la estimación de la función
característica de Tao (proposición 1.17), un enunciado puro sobre la
cadena afín. La medición es compatible con él y no sugiere un atajo
elemental: el decaimiento observado es lento y la cancelación depende de
muchas escalas. **El paso queda delimitado, sin avance de fondo**, como
pide el plan cuando una pieza no avanza.

Los números de proposición de Tao se citan de memoria; falta cotejar el
artículo (Forum Math. Pi, 2022). Revisión humana pendiente.
