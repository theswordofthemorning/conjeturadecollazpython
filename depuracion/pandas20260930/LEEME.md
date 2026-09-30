# Pandas: bloque 2 del plan — 30-09-2026

Bloque 2 del [plan por sesiones](../transversal20260927/PLAN_SESIONES_20260928.md).
Entregable pedido: formalizar el [lema escrito](../../lemadepandas.txt) con
sus hipótesis y cotejarlo por otra vía. La cota universal del residuo quedaba
fuera del presupuesto y sigue fuera.

**Resultado.** Pandas está formalizado en Lean, afilado y unido a la pregunta
de Gao (1993, pág. 266): ¿`height(n) = height(n+1)` implica
`σ∞(n) = σ∞(n+1)`? La respuesta es sí en tres casos. Es sí para todo n si
todo residuo es menor que 4, y es sí para casi todo n sin hipótesis. Con
Marmotas es sí también para todo par cuyas órbitas bajen de 2^20 sin haber
hecho más de 2^21 pasos `3n+1` por encima de 2^20. La pregunta, para todo n,
sigue abierta.

## Objeto

Mapa clásico `C` (`n/2` o `3n+1`) y definiciones de
[GarnerEnunciado](../gao20260920/formal/GarnerEnunciado.lean): `altura n h`
es la primera llegada a 1 y `mitades n h` es σ∞(n). `triples n h` cuenta los
pasos `3n+1`. El residuo de Roosendaal es
`Res(n) = 2^σ∞(n) / (3^S(n) · n)` y vale
`Res(n) = ∏ (1 + 1/(3y))` sobre las iteradas impares y anteriores a 1.

## Lo demostrado en Lean

[Pandas.lean](Pandas.lean), Lean 4.32.2, compilado desde el proyecto de Gao con
código 0. Todos los teoremas dependen sólo de `propext`, `Classical.choice` y
`Quot.sound` ([registro](lean_local.txt)).

| Teorema | Enunciado |
|---|---|
| `residuo_ge_uno` | `Res(n) ≥ 1` para todo n con altura: `3^S·n ≤ 2^σ∞`. Deja de ser hipótesis. |
| `seis`, `pandas_encuentro` | Si `C^j(n) = C^j(n+1)` con `R_j(n) ≤ 6` y `R_j(n+1) < 6n/(n+1)` (residuos parciales), el encuentro es equilibrado. |
| `pandas` | Igual altura, `Res(n) ≤ 6` y `Res(n+1) < 6n/(n+1)`: igual σ∞ e igual S. |
| `pandas_escrito` | La forma de `lemadepandas.txt`: `Res < 3` en los dos. |
| `gao_de_residuo` | Si `Res < 4` para todo n con altura, la pregunta de Gao tiene respuesta afirmativa. |
| `gao_casi_siempre` | Sin hipótesis: los contraejemplos tienen densidad natural 0. |
| `equilibrio_quince` | Un encuentro en el paso j con `2^j + 3 < 15n` es equilibrado; `Hienas.equilibrio` pedía `2^j ≤ n`. |
| `transporte`, `residuo_por_escalas`, `gao_por_escalas` | Marmotas: la sección siguiente. |

**Por qué 4 y no 3.** En `6^d = n·Res(n) / ((n+1)·Res(n+1))`, con `d ≥ 1` se
obtiene `Res(n) ≥ 6(n+1)/n · Res(n+1) > 6`. Con `d ≤ −1` se obtiene
`Res(n+1) ≥ 6n/(n+1) · Res(n) ≥ 6n/(n+1)`. Esto se debe a que `Res ≥ 1`
es un teorema y no una hipótesis. Como `n ≥ 2` en todo par de igual altura,
`6n/(n+1) ≥ 4`. El argumento de intervalos del lema escrito sólo usaba el
cociente de los residuos y necesitaba `Res < 3`.

**Densidad.** `mitades_de_coalescencia`: si n y n+1 coalescen en el sentido
de Gao y tienen igual altura, tienen igual σ∞. Los contraejemplos quedan
fuera del conjunto de coalescencia, que tiene densidad 1 por `GaoLiteral`
(Hienas). Es un corolario directo de la cadena ya demostrada.

## Marmotas: combinar escalas para el residuo

Aplicación de la técnica que el plan tomó de Nashida, con los cinco puntos
del criterio común:

1. **Cantidad.** `Res(x)`, mapa clásico, x con altura. Es multiplicativa a lo
   largo de la órbita: `Res(x) = R_k(x) · Res(C^k x)`.
2. **Cota inicial.** En `[1, B)` con `B = 2^20`, el máximo exacto es
   `2^61 / 1840049047529878113 = 1,253142144` y se alcanza en 993 y sus dobles.
   Es un cálculo finito, hecho por dos programas independientes.
3. **Recurrencia.** `transporte`: si las k primeras iteradas no bajan de B,
   `2^m · C^k(x) · (3B)^S ≤ 3^S · x · (3B+1)^S`, es decir,
   `R_k(x) ≤ (1 + 1/(3B))^S`, con S los pasos `3n+1` de ese tramo.
4. **Empalme.** Es la primera entrada de la órbita en `[1, B)`. Antes de ella
   todas las iteradas son `≥ B` y después vale la base. `residuo_por_escalas`
   da `Res(x) ≤ (a/b) · (1 + 1/(3B))^S`.
5. **Error.** `potencia_tres` (Bernoulli, sin exponencial):
   `(3B+1)^S ≤ 3 · (3B)^S` si `S ≤ 2B`. El factor no depende del tamaño de x,
   sólo de S. Con la base `a/b < 4/3` queda `Res(x) < 4`.

`gao_por_escalas`: si la base `Res ≤ a/b < 4/3` vale en `[1, B)` y las órbitas
de n y n+1 entran en `[1, B)` tras a lo sumo 2B pasos `3n+1` hechos en
valores `≥ B`, igual altura implica igual σ∞. La base es una hipótesis
explícita del enunciado Lean, como en el
[puente de Nashida](../nashida20260928/LEEME.md). Con `B = 2^20`, esa base la
comprueba el cálculo finito.

**Obstrucción precisa.** Un contraejemplo a la pregunta de Gao exige que la
órbita de n o la de n+1 haga más de `2^21 = 2.097.152` pasos `3n+1` por
encima de `2^20` antes de bajar de `2^20`. No hay ninguna cota demostrada de
ese número para todo n: acotarlo es un problema de tiempos de parada. Por eso
el transporte no cierra la pregunta. Un contraejemplo requiere un residuo al
menos 3,19 veces mayor que el mayor de `[1, 2^20)`.

## Cotejo independiente

[verificar_pandas.py](verificar_pandas.py), ([salida](verificar_pandas_salida.txt),
17 s). No reutiliza [pandas_gao.py](../transversal20260927/pandas_gao.py):
calcula el residuo por el producto de `(3y+1)/(3y)`, propagado hacia atrás
por la órbita, y compara por productos cruzados de enteros.

- La fórmula del producto coincide exactamente con `2^σ∞/(3^S n)` para `n < 2^14`.
- En `[1, 2^20)` ningún residuo es menor que 1. El máximo es el de 993,
  el mismo que da `pandas_gao.py`, y ningún otro n lo iguala salvo los dobles.
- El núcleo `seis` no tiene contraejemplos en la caja `n ≤ 30`, `Y ≤ 8`,
  exponentes `≤ 14`: 4457 casos cumplen las hipótesis y en todos `t1 = t2`.
- Hay 500.898 pares `n, n+1 < 2^20` de igual altura y ninguno tiene σ∞
  distinto. De ellos, 399.979 se encuentran por primera vez en un paso con
  `2^j + 3 < 15n`, así que `equilibrio_quince` los cubre sin residuos. Los
  otros 100.919 necesitan la cota del residuo.
- Los `#guard` de Lean recalculan con las definiciones del enunciado el
  residuo exacto de 993 (altura 93) y las hipótesis de `pandas` en la racha
  943..949 de Gao.

Son comprobaciones finitas. No sustituyen al enunciado universal.

## Decisión del bloque

El bloque entrega lo presupuestado: la formalización con sus hipótesis y un
cotejo independiente. Añade además una reducción válida (`Res < 4`, y Marmotas
con una base finita) y una obstrucción precisa (los pasos por encima de B).
La obstrucción es de tiempos de parada y no se resuelve con residuos: seguir
en Pandas no tiene un mecanismo nuevo. **Se cierra Pandas y el siguiente
bloque es Wirsching.**

Candidatas registradas, sin demostrar:

- Las iteradas impares anteriores a 1 son distintas. Por eso la suma de
  `1/(3y)` por encima de B no pasa de `(1/6)·ln(1 + 2S/B)` aproximadamente, y
  la obstrucción subiría de `2B` a unos `526B` pasos. No se formalizó.
- Si se admitiera la verificación externa hasta `2^71` con retrasos máximos
  por debajo de `2^21`, la base se extendería a `2^71`. Esos datos no se han
  cotejado aquí.

## Reproducir

Desde `depuracion/gao20260920/formal` (primera vez: `lake build GaoFormal`,
unos 3 min si faltan Hienas, Alpacas, GarnerEnunciado o Condoras):

```text
lean --version
lake env lean ../../pandas20260930/Pandas.lean
```

Desde esta carpeta:

```text
python -B -X utf8 verificar_pandas.py
```

No se modificó la configuración Lean del proyecto ni se lanzaron censos
nuevos: el mayor cálculo es el de `2^20`, igual que en el bloque del 27-09.
