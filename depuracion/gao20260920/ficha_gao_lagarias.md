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

## Fuente primaria (no leída)

G.-G. Gao, *On consecutive numbers of the same height in the Collatz
problem*, Discrete Math. 112 (1993) 261–267, doi:10.1016/0012-365X(93)90240-T.
El 25-09-2026 ScienceDirect devolvió 403 y Semantic Scholar no mostró el
texto. El resumen público sólo menciona la 35654-tupla y la heurística de
rachas. La redacción original de la conjetura sigue sin cotejar.

## Estado en la literatura (búsqueda breve, 25-09-2026)

No se encontró una prueba publicada. El proyecto ccchallenge.org, que
formaliza artículos sobre Collatz, lista Gao (1993) como «not formalized».
Una búsqueda breve no excluye trabajos no indexados. No se contactó a nadie.
