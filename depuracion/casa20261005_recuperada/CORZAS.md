# Corzas: el retrato del fugitivo

05-10-2026. Ruta B, paso 2 del [plano de la casa](LEEME.md#ruta-a-seguir), y
apertura con presupuesto acotado de los pasos 3 («buscar choques») y 4
(«el dominó del muro A»). Todo está
demostrado en Lean 4.32.2 sin hipótesis externas, con axiomas estándar.

## Qué es un fugitivo

Mapa: el atajo `T(n)=n/2` si n es par y `(3n+1)/2` si es impar. `S_k(n)`
cuenta las subidas (pasos impares) entre n, T n, …, T^(k-1) n. El
**pronóstico** a los k pasos es `3^S_k(n)/2^k`.

Un **fugitivo** es un número cuyo pronóstico nunca baja de 1:
`2^k ≤ 3^S_k(n)` para todo k (`FugaPura n` en
[CasaPlano.lean](CasaPlano.lean)). El muro B dice exactamente que no hay
fugitivos `n ≥ 2`. Aquí se demuestra cómo tendría que ser uno.

## El retrato, en Lean

[CasaFugitivo.lean](CasaFugitivo.lean); el resumen es `retrato_del_fugitivo`.

| Rasgo | Teorema | Enunciado |
|---|---|---|
| Órbita no acotada | `fugitivo_no_acotado` | supera cualquier cota (`Fuga n`) |
| Nunca repite | `fugitivo_no_repite` | `T^i n ≠ T^j n` si `i ≠ j` |
| Nunca vuelve | `fugitivo_no_vuelve` | `n < T^k n` para todo `k ≥ 1` |
| Patrón no periódico | `fugitivo_no_periodico` | sus paridades nunca se vuelven periódicas |
| Sube mucho | `fugitivo_63` | `63 k < 100 S_k(n)` para todo `k ≥ 1` |
| … y en general | `fugitivo_proporcion_estricta` | si `3^q < 2^p`, `q k < p S_k(n)` |
| Residuo | `fugitivo_tres_mod_cuatro` | `n ≡ 3 (mod 4)` |
| Casi nadie lo es | `fugitivos_densidad_cero` | densidad natural 0 |

Las piezas del radier que hacían falta, también en Lean:

- `S_congr`: `S_k(n)` depende sólo de n módulo `2^k`.
- `iguales_de_paridades`: dos números con la misma sucesión completa de
  paridades son iguales (`congr_de_paridades`: con las k primeras, son
  congruentes módulo `2^k`).
- `suma_pesos`: `∑_{r<2^K} x^S_K(r) = (1+x)^K`; es decir, el número de
  residuos con i subidas es C(K, i).
- `cruza_de_ciclo`: si una órbita entra en un ciclo, su pronóstico baja de 1.

### Cómo se prueba, en palabras

- **No acotada.** Una órbita acotada repite un valor y entra en un ciclo.
  En un ciclo de p pasos con a subidas, la fórmula de Terras con β ≥ 0 da
  `3^a < 2^p`. Cada vuelta multiplica el pronóstico por `3^a/2^p < 1`, así
  que termina bajando de 1: no era fugitivo.
- **No periódico.** Si las paridades de `T^i n` y de `T^(i+p) n` coinciden
  para siempre, los dos números son iguales (`iguales_de_paridades`); la
  órbita entra en un ciclo y vale lo anterior.
- **63 de cada 100.** `2^k ≤ 3^S` y `3^63 < 2^100` dan `63k < 100 S`.
- **Densidad cero.** Un fugitivo tiene, módulo `2^K`, un residuo con
  `2^K ≤ 3^S_K`. Cada uno de esos residuos pesa al menos
  `(√3)^S_K/(√2)^K ≥ 1`, y la suma de los pesos de todos los residuos es
  `((1+√3)/√2)^K` por `suma_pesos`. Así, la proporción de residuos que
  sirven es a lo sumo `ρ^K` con `ρ = (1+√3)/(2√2) ≈ 0,966`
  (`proporcion_sin_cruce`), y la de fugitivos menores que N, para
  `N ≥ 2^K`, es a lo sumo `2ρ^K` (`proporcion_fugitivos`). Es la cota de
  Chernoff con exponente 1/2, escrita con enteros y raíces.

## Casi todo número baja de sí mismo

[CasaCasiTodos.lean](CasaCasiTodos.lean), con la misma cota:

- `cota_superior`: `2^k T^k(n) + 2^k ≤ 3^S_k(n) n + 3^k`, el techo del
  término aditivo de Terras.
- `desciende_de_cruce_grande`: si el pronóstico baja de 1 en el paso k y
  `n ≥ 3^k`, entonces `T^k(n) < n`.
- `casi_todos_descienden`: la proporción de `n < N` que nunca bajan de sí
  mismos tiende a 0 (Terras 1976, Everett 1977).

Los únicos candidatos a contraejemplo mínimo de Collatz nunca bajan de sí
mismos, así que el menor contraejemplo, si existe, está en un conjunto de
densidad 0. **No es Wu 1** («casi todo número llega a 1»), que sigue
abierta: bajar una vez no garantiza seguir bajando.

## El teorema de Terras: la distribución del tiempo de parada

[CasaTerras.lean](CasaTerras.lean). Sea `d_K` el número de residuos
módulo `2^K` cuyo pronóstico no baja de 1 en ninguno de los K primeros
pasos (`supervivientes K`).

- `noBaja_iff_sobrevive`: para `n ≥ 3^K`, no bajar de sí mismo en K pasos
  equivale a que el pronóstico no baje de 1 en esos K pasos. Es CST en
  horizonte K para los números grandes.
- `terras_error`: `|#{n < N : σ(n) > K} − N d_K/2^K| ≤ d_K + 3^K`.
- `terras_distribucion`: la proporción de `n < N` con `σ(n) > K` tiende a
  `d_K/2^K`.
- `terras_limite`: `d_K/2^K → 0`, porque `d_K ≤ c_K`.

Es el teorema de Terras (1976): σ tiene función de distribución límite
`F(K) = 1 − d_K/2^K`, con `F(K) → 1`. En el cotejo por órbitas directas,
para `N = 2^18` y `K ≤ 16`, el número exacto de `n < N` con `σ(n) > K`
resultó ser `N d_K/2^K + 2`: los dos de más son 0 y 1. El error real es
mucho menor que la cota, porque en ese rango no aparece ninguna grieta.

## Contraste independiente

[cotejar_fugitivo.py](cotejar_fugitivo.py), con enteros exactos, hasta
K = 22 ([salida](cotejo_fugitivo.json)): la distribución binomial de S_K,
la periodicidad módulo `2^K`, la cota `c_K² 2^K ≤ (1+√3)^(2K)` comparada en
`ℤ[√3]`, la clase 3 mod 4, y la cota superior y el descenso con
`n ≥ 3^k` para n < 20000 y k ≤ 40 (102 880 pares (n, k) con cruce y `n ≥ 3^k`),
y el error de Terras por órbitas directas para `N = 2^18` y `K ≤ 16`.

| K | c_K: residuos con `2^K ≤ 3^S_K` | proporción | cota ρ^K | d_K: sin cruce hasta K | proporción |
|---|---|---|---|---|---|
| 10 | 176 | 0,172 | 0,707 | 64 | 0,0625 |
| 16 | 6885 | 0,105 | 0,574 | 2114 | 0,0323 |
| 22 | 600 370 | 0,143 | 0,466 | 93 222 | 0,0222 |

La cota sólo usa la condición del último paso; la condición completa
(`d_K`, todos los pasos hasta K) es mucho más fuerte, pero no hace falta
para la densidad cero. La proporción `c_K/2^K` oscila con la parte
fraccionaria de `K log 2/log 3`.

## Paso 3: dónde puede estar un choque

[CasaChoques.lean](CasaChoques.lean). El paso 3 busca dos rasgos del
fugitivo que se contradigan. Con presupuesto acotado se obtuvo el mapa de
dónde **no** puede estar el choque:

- `sin_choque_finito`: para cada K hay `n ≥ 2` (`2^(K+2) − 1`) cuyo
  pronóstico no baja de 1 en los K primeros pasos. Ninguna contradicción
  sale de mirar un tramo finito: tiene que usar el comportamiento infinito.
- `periodico_iff_acotada`: el patrón de paridades de n es finalmente
  periódico si y sólo si su órbita está acotada. Por eso
  `sin_fugas_iff_periodicidad`: «no hay fugas» equivale a «todo natural
  tiene patrón finalmente periódico», y `muroB_de_periodicidad`: esa
  periodicidad levanta el muro B.
- La positividad es indispensable: en los enteros, `T(−1) = −1` y −1 sube
  en todos sus pasos, así que es un fugitivo con órbita acotada. El rasgo
  «no acotada» usa `n ≥ 0` a través de β ≥ 0. (Observación a mano, no en
  Lean.)

Conclusión del presupuesto: los rasgos del fugitivo que dependen sólo de su
patrón de paridades no chocan entre sí, porque números naturales los
cumplen en cualquier tramo finito. Un choque tiene que usar a la vez el
patrón infinito y que n sea un número natural. Eso es la conjetura de
periodicidad de Lagarias (1985) restringida a los naturales, que es
exactamente `∀ n, PatronPeriodico n`: un problema abierto equivalente a que
no haya fugas. La cita es de memoria: falta cotejar el original. **El paso 3
queda delimitado, sin avance de fondo**, como pide el plan cuando una pieza
no avanza.

## Paso 4: cómo tendría que ser una grieta

[CasaDomino.lean](CasaDomino.lean). Una **grieta** es un `n ≥ 2` cuyo
pronóstico baja de 1 pero que nunca baja de sí mismo; el muro A dice que
no hay grietas. Con presupuesto acotado:

- `grieta_desigualdad`: si el pronóstico baja de 1 en el paso k y n no
  baja de sí mismo en ese paso, `(2^k − 3^S_k) n + 2^k ≤ 3^k`.
- `grieta_pequena`: en una grieta, todo paso de cruce k cumple `n < 3^k`;
  en particular `3^τ(n) > n`.
- `minimos_no_bajan`: en toda órbita que no llega a 1 hay, tan lejos como
  se quiera, valores `≥ 2` que nunca bajan de sí mismos: los mínimos de
  sus colas.
- `contraejemplo_con_muroA`: con el muro A, la órbita de un contraejemplo
  contiene infinitos fugitivos. Con la densidad cero no hay choque: una
  órbita es un conjunto ralo.

Conclusión del presupuesto: la desigualdad de la grieta no basta sola,
porque `n < 3^k` deja sitio de sobra cuando el primer cruce es tardío
(`2^K − 1` tiene primer cruce después de K pasos). Ocelotas la refuerza con
la estructura del término aditivo palabra por palabra, y por eso depende
del número de rachas. El dominó necesitaría esa cota para todas las
palabras a la vez: es la conjetura CST de Terras, abierta. **El paso 4
queda delimitado, sin avance de fondo.**

## Evidencia y reproducción

[comprobar_fugitivo.py](comprobar_fugitivo.py) compila desde las fuentes, en
una carpeta temporal nueva y sin cachés, los ocho módulos de Ocelotas que
importa `CasaPlano`, después `CasaPlano`, `CasaFugitivo`, `CasaCasiTodos`,
`CasaChoques`, `CasaTerras` y `CasaDomino`; exige código 0, ningún `sorry` ni aviso en los módulos de la
casa, y sólo `propext`, `Classical.choice` y `Quot.sound` en sus consultas
([evidencia](evidencia_fugitivo.json), [salida](evidencia_fugitivo.txt)).
Desde la raíz:

```text
python -B -X utf8 depuracion/casa20261004/comprobar_fugitivo.py --salida depuracion/casa20261004/evidencia_fugitivo.json
python -B -X utf8 depuracion/casa20261004/cotejar_fugitivo.py --hasta 22 --salida depuracion/casa20261004/cotejo_fugitivo.json
```

## Límites

- Nada aquí afirma el muro B: densidad cero no es conjunto vacío.
- Los rasgos y los teoremas de densidad son conocidos en la literatura
  (Terras 1976, Everett 1977, Lagarias 1985); lo propio es la formalización y el
  inventario. Sin pretensión de prioridad.
- Revisión humana pendiente. Lean certifica los enunciados, no su
  interpretación.
