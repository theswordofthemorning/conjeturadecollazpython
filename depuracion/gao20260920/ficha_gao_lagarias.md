# Ficha: la conjetura de Gao según Lagarias

Cotejo del 25-09-2026 para el enunciado de [Tejonas](Tejonas.md).

## Fuente secundaria (leída)

J. C. Lagarias, *The 3x+1 problem: An annotated bibliography (1963–1999)
(sorted by author)*, arXiv:math/0309224, versión servida el 25-09-2026,
página 28, entrada 68:

> He conjectures that the set {n : C^(k)(n) = C^(k)(n+1) for some k ≤ log2 n}
> has natural density one, and proves that it has a natural density which is
> at least 0.389.

En la introducción de la misma bibliografía (página 1), C es el mapa clásico:
`C(x)=3x+1` si x es impar y `x/2` si es par; T es el atajo `(3x+1)/2`. Por
tanto el enunciado coincide con `GaoEnunciado.conjetura_gao`: el mismo C, el
mismo conjunto con `k<=floor(log2 n)` (equivale a `k<=log2 n` para k entero)
y densidad natural uno como límite.

## Fuente primaria (leída el 25-09 por la noche)

G.-G. Gao, *On consecutive numbers of the same height in the Collatz
problem*, Discrete Math. 112 (1993) 261–267, doi:10.1016/0012-365X(93)90240-T.
Por la tarde ScienceDirect devolvió 403; por la noche el usuario aportó el
PDF, que no se sube al repositorio por derechos de autor.

- **Mapa** (pág. 261): `C(n)=3n+1` si n es impar y `n/2` si es par. Es el
  mismo `f` de `GaoEnunciado`.
- **Coalescencia** (pág. 264):

  > We say that n and n+1 coalesce if C^(k)(n) = C^(k)(n+1), with both
  > having the same number of divisions by 2 in the first k iterations, and
  > the number 1 has occurred in neither trajectory of n nor that of n+1 in
  > the first k iterations.

  Gao advierte que es más estricta que la de Lagarias (1985): con aquélla,
  4 y 5 coalescen tras 3 iteraciones; con ésta, no.
- **Densidad por niveles** (pág. 265): `d̄_k = 2^-k #{n < 2^k-1 : n y n+1
  coalescen tras <= k iteraciones}`. Así figura en el texto extraído; un
  término más o menos no cambia el límite. El Corolario 2 prueba que `d̄_k`
  crece, así que existe `d̄* = lim d̄_k`.
- **La conjetura** (pág. 265):

  > The computations of Table 3 suggest the stronger conjecture that, for
  > large enough n, almost every pair of consecutive integers greater than
  > n have the same height and the same total stopping time. [...] The
  > conjecture asserts that d̄_k → 1 as k → ∞.

  Añade que entonces `d* = lim sup d_k = 1`, con `d_k = d(2^k)`: la
  densidad de coalescencias sin límite de pasos.
- **El 0,389** es `d̄_24`, un valor calculado de la tabla 3 (pág. 266). Con
  el Corolario 2 da `d̄* >= 0,389`. No sale de clases módulo `2^17`: la
  cercanía con `A398792(17)/2^17` no es una identidad.

## Qué cambia el cotejo

`GaoEnunciado.conjetura_gao` coincide literalmente con el **resumen de
Lagarias**, no con el enunciado de Gao. Gao exige además:

- el mismo número de divisiones por 2;
- que ninguna trayectoria pase por 1;
- la misma cota k para todos los `n < 2^k`, en vez de `k <= log2 n` para
  cada n.

La frase de Lagarias «proves that it has a natural density which is at
least 0.389» también simplifica: Gao prueba que existe `lim d̄_k` y calcula
`d̄_24`.

**Actualización del 26-09: la forma literal está formalizada**
([Hienas](Hienas.md)). `GaoLiteral.conjetura_gao_literal` demuestra
`d̄_k -> 1` y `d(x) -> 1` con la coalescencia exigente de Gao. Para el 1 se
toma la lectura más estricta: no aparece en `C^0..C^k`. No hizo falta la
fusión balanceada: cualquier encuentro en `k <= log2 n` pasos ya tiene las
mismas divisiones por 2 y no pasa por 1 (`Hienas.puente`), y de la
densidad de Lagarias se deducen las de Gao. Con las mismas definiciones,
Lean recalcula la tabla 3 hasta k=12, y
[verificar_hienas.py](verificar_hienas.py) los 21 valores.

Queda la salvedad que el propio Gao señala: coalescer da la misma altura
sólo si las trayectorias llegan a 1. El artículo deja otras preguntas que
esto no toca: rachas arbitrariamente largas, su heurística, y si
`height(n)=height(n+1)` implica que coincidan los tiempos totales de parada.

## Estado en la literatura (búsqueda breve, 25-09-2026)

No se encontró una prueba publicada. El proyecto ccchallenge.org, que
formaliza artículos sobre Collatz, lista Gao (1993) como «not formalized».
Una búsqueda breve no excluye trabajos no indexados. No se contactó a nadie.

Ampliada el 26-09:

- Las dos bibliografías anotadas de Lagarias (1963–1999 y 2000–2009, en
  `lecturas/`) no traen ninguna prueba. Wu (1995) prueba que crece una
  densidad condicionada y conjetura que crece la otra. Garner (1985)
  conjetura que la mayoría de los enteros tienen la altura de un vecino, y
  que hay rachas arbitrariamente largas de la misma altura.
- Semantic Scholar da 9 trabajos que citan a Gao: cuatro versiones de las
  bibliografías de Lagarias, LaDue (2017, arXiv:1709.02979, condiciones para
  pares concretos, sin densidades) y cuatro que sólo se vieron por título o
  resumen: 1994, 2007, 2022 y Frinkle et al. (2025, J. Supercomputing,
  cómputo de rachas para A277109).
- ccchallenge.org sigue listando Gao (1993) como «Wishlist», sin formalizar.
- zbMATH devolvió 403; MathSciNet y Google Scholar no se consultaron. La
  búsqueda sigue sin ser exhaustiva.
