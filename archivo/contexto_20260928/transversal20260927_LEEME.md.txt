# Ruta transversal: de los pares a la llegada a 1

**Seguimiento del 28-09:** el orden vigente está en el
[plan por sesiones](PLAN_SESIONES_20260928.md). Esta nota conserva el plan
del 27-09; el cotejo posterior de Nashida y su puente condicional se
documentan en la [auditoría](../nashida20260928/LEEME.md).

27-09-2026. Es un plan: no trae resultados nuevos demostrados. Cada
afirmación dice si es prueba escrita, formalización, conteo exacto o
lectura. Nada de esta nota entra al registro de afirmaciones mientras no se
demuestre.

## Por qué hace falta

Lo demostrado corre en paralelo a Collatz. Gao ([Tejonas](../gao20260920/Tejonas.md),
[Hienas](../gao20260920/Hienas.md)), Garner (2) ([Alpacas](../garner20260926/Alpacas.md))
y Wu 2 ([Condoras](../gao20260920/formal/Condoras.lean)) hablan de pares n,
n+1 que se funden. Salvo en las rachas construidas, ninguno dice que un
número llegue a 1. Lo abierto choca contra esa pared:

| Pregunta | Qué falta |
|---|---|
| Wu 1: `lim d(M) = 1` | que los n que llegan a 1 tengan densidad 1 (Condoras) |
| Garner (1) con alturas finitas | lo mismo: que casi todos lleguen a 1 |
| Pregunta de Gao (1993, pág. 266): ¿`height(n)=height(n+1)` implica `σ∞(n)=σ∞(n+1)`? | controlar el residuo |

Una ruta transversal cruza de los pares a las trayectorias sueltas. Hay tres
cruces a la vista.

## Cruce 1: Pandas y la pregunta de Gao

Mapa clásico `C`. Hasta la primera llegada a 1, S(n) cuenta los pasos
impares y τ(n) las divisiones por 2; τ es el `σ∞` de Gao y el tiempo del
atajo T. La altura es H = τ + S, y el residuo de Roosendaal cumple
`2^τ = 3^S·n·Res(n)`.

- **Prueba escrita** ([lemadepandas.txt](../../lemadepandas.txt), del 03-08,
  corregida el 13-09). Si n y n+1 llegan a 1, `H(n)=H(n+1)` y
  `1<=Res(n),Res(n+1)<3`, entonces `τ(n)=τ(n+1)` y `S(n)=S(n+1)`. Con
  `d=τ(n)-τ(n+1)`, se tiene `6^d=(n/(n+1))·Res(n)/Res(n+1)`. Para n>=2
  ese cociente queda entre 1/6 y 3, así que d = 0.
- **Es el argumento de Gao, hecho exacto.** Gao apoya su pregunta con un
  argumento que él llama tosco: `(n+1)/n ≈ 6^(d2-d1)`. Pandas añade los
  residuos que faltaban.
- **Conteo exacto** ([pandas_gao.py](pandas_gao.py), [salida](pandas_gao_salida.txt)).
  Para `1<=n<2^20`:
  - los 1.048.575 residuos son menores que 3;
  - el máximo es 1,253142144 y se alcanza en 993 y en sus dobles;
  - de los 500.898 pares con igual altura, ninguno tiene distinto `σ∞`.
- **Consecuencia.** Un contraejemplo a Gao necesita un residuo de al menos 3,
  más del doble del mayor conocido. La pregunta se deduce de una forma débil
  de la conjetura del residuo (afirmación 131 del registro). Los cálculos de
  residuos de Roosendaal la dejarían comprobada hasta donde él llegó. El
  registro anota `2^32`, pero no se ha cotejado con su fuente.
- **Lo que falta.** En Lean sólo está `pandas_seis` (`zoologico.lean`), que
  es la parte de las potencias de 6. Los artículos I y II no citan Pandas.

## Cruce 2: Condoras con Nashida (2026)

**Corrección del 28-09 al texto histórico que sigue:** el original r8
cuenta órbitas que permanecen estrictamente por encima de N0. Por tanto,
la hipótesis del puente debe cubrir `1<=n<=N0`, incluyendo N0. Si sólo
se cubre `n<N0`, para `N0>=2` se aplica la cota a `N0-1`. K no está explicitada en el
artículo. El puente condicional ya está formalizado localmente; la prueba
externa no se ha recompilado aquí. Véase la [ficha](../nashida20260928/LEEME.md).

Nashida (2026b) es *A power-saving bound, uniform in the endpoint, for
Collatz orbits that stay above a fixed barrier* (Zenodo,
10.5281/zenodo.22986670). Con el mapa clásico, los `N<=X` cuya órbita nunca
baja de `N0` son a lo sumo `K·N0^(-c')·X`, con `c'≈3,5·10^-6` y una K que no
se puede calcular. Está formalizado en Lean, sin hipótesis. **Sólo se leyó
el resumen.**

Unido a Condoras daría lo siguiente, que todavía no está escrito con
cuidado ni formalizado:

    si todo n < N0 llega a 1, entonces liminf d(M) >= 1 - K·N0^(-c').

- **Por qué.** Si todo n < N0 llega a 1, un n que no llega a 1 nunca baja de
  N0. Por eso esos n tienen densidad superior de a lo sumo `K·N0^(-c')`.
- **El papel de Hienas.** Casi todo n coalesce con n+1 sin pasar por 1. Si
  además n llega a 1, n y n+1 tienen la misma altura, y n cuenta en d(M).
- **Lo que no hace.** El puente une las dos líneas, pero no cruza la pared.
  La densidad 1 exige verificar Collatz hasta N0 tan grande como se quiera, y
  hoy se sabe hasta `2^71` (Barina 2025, por cómputo).

## Cruce 3: Wirsching y los predecesores

Wirsching (1993–2003, cinco artículos en ccchallenge) estudia la densidad
del conjunto de predecesores de un número. **Sin leer.**

- **La idea.** Si todo m no múltiplo de 3 tuviera predecesores de densidad
  positiva, Wu 1 equivaldría a Collatz.
- **Por qué.** Supongamos que m0 no llega a 1. Después de su primer paso
  impar, su órbita sólo pasa por números no múltiplos de 3; sea m uno de
  ellos. Ningún predecesor de m llega a 1. Si esos predecesores tuvieran
  densidad positiva, los que llegan a 1 no tendrían densidad 1, y por
  Condoras Wu 1 fallaría.
- **Qué falta.** Leer qué demostró Wirsching y qué dejó como conjetura.

## Novedad: la lista de ccchallenge (27-09)

[ccchallenge_lista.py](ccchallenge_lista.py) ([salida](ccchallenge_salida.txt))
lee la lista completa por la API de ccchallenge. Tiene 379 registros:
368 sin empezar, 4 en formalización, 6 esperando auditoría y 1 auditado.
Gao 1993, Garner 1985 y Wu 1992 están sin empezar.

- **Nadie demuestra Gao, Garner ni Wu.** Sobre consecutivos o coalescencia
  sólo aparecen trabajos ya cotejados (Garner 1985, Gao 1993, Wu 1992, 1993
  y 1995, Wu–Huang 2001) y dos de 2026 que no compiten. Se miraron los
  títulos de los 379 registros y los 32 resúmenes que trae la lista.
- **Nuevos para el laboratorio:**
  - Novgorodtsev (2026b), Zenodo, 10.5281/zenodo.21848913. Coalescencia con
    reloj exacto para una familia de consecutivos de densidad 1/8; extiende a
    LaDue. Es afín, y citable en el artículo I.
  - Kolpakov, Al Jumas y Luo (2026), hal-05731017. Estudio empírico: la
    correlación entre vecinos depende de cuándo se funden.
  - Nashida (2026), tres preprints en Lean hechos con Claude: el del cruce 2,
    otro para mapas generalizados (22986677) y otro que mejora la cota de
    Terras (22986641).
- **Otras formalizaciones.** Tao (2022) tiene dos esperando auditoría, y
  Terras (1976) y Krasikov–Lagarias (2003) se están formalizando.
- **Auditoría.** El artefacto Lean sería la primera formalización de Gao,
  Garner y Wu en la lista, y su auditoría es la revisión externa que falta.
  La cola estaba parada: 6 esperando y ninguna en curso. Enviarlo requiere
  autorización del usuario.

## Pasos, en orden

1. **Leer** enteros Nashida (2026b) y Wirsching (2003), *On the problem of
   positive predecessor density in 3N+1 dynamics*. Con eso se decide si el
   cruce 2 da un teorema o una observación.
2. **Formalizar Pandas completo** con las definiciones de `GarnerEnunciado`
   (altura y `σ∞`).
3. **Formalizar el cruce 2** si se sostiene, con el código Lean de Nashida,
   siempre que su versión de Lean y Mathlib lo permita.
4. **Citas para AFM.** En la respuesta a los árbitros, citar Pandas (I y II),
   Nashida (II y III), y Novgorodtsev y Kolpakov et al. (I). Nada se cambia
   en Zenodo sin el usuario.

## Reproducir

```
python -B -X utf8 pandas_gao.py          # unos 5 s
python -B -X utf8 ccchallenge_lista.py   # lee la API; la lista cambia con el tiempo
```

## Fuentes

- [lemadepandas.txt](../../lemadepandas.txt) y
  [Matematica.md](../coherencia20260913/Matematica.md), sección 1.
- G.-G. Gao, Discrete Math. 112 (1993) 261–267, pág. 266. Se leyó en el PDF
  que aportó el usuario, que no se sube.
- `https://ccchallenge.org/api/papers`, leída el 27-09.
- H. Nashida (2026), Zenodo: 10.5281/zenodo.22986670, 22986677 y 22986641.
  Sólo se leyeron los resúmenes.
- A. Novgorodtsev (2026b), Zenodo: 10.5281/zenodo.21848913. Sólo el resumen.
- A. Kolpakov, H. Al Jumas y Y. D. Luo (2026), HAL: hal-05731017. Sólo el
  resumen.
- G. Wirsching (1993, 1994, 1996, 1997 y 2003), según ccchallenge. Sin leer.
- La afirmación 131 del registro (residuo de Roosendaal) y Barina (2025),
  J. Supercomputing 81(7), art. 810.
