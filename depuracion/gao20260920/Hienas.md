# Hienas: la conjetura de Gao en su forma literal

26-09-2026. **Demostrado en Lean** ([Hienas.lean](formal/Hienas.lean), 3
consultas de axiomas, y [GaoLiteral.lean](formal/GaoLiteral.lean), 2; sólo
`propext`, `Classical.choice`, `Quot.sound`). **Pendiente de revisión humana.**

## Enunciado

Mapa clásico `C(n)=n/2` si n es par y `3n+1` si es impar. Según Gao (1993,
pág. 264), n y n+1 **coalescen** en el paso k si `C^k(n)=C^k(n+1)`, con el
mismo número de divisiones por 2 en los k primeros pasos, y sin que el 1
aparezca en ninguna de las dos trayectorias. Se toma la lectura más
exigente: el 1 no aparece en `C^0,...,C^k`. Con (pág. 265)

    d̄_k = 2^-k #{n < 2^k-1 : n y n+1 coalescen tras <= k iteraciones},

`GaoLiteral.conjetura_gao_literal` demuestra:

- `d̄_k -> 1`, que es la conjetura tal como la escribe Gao;
- `d(x) -> 1`, con `d(x) = x^-1 #{n < x : n y n+1 coalescen}`. Gao no sabía
  si ese límite existía (pág. 265).

## Prueba

1. **Puente** (`puente`). Si n y n+1 se encuentran en `j <= log2 n` pasos,
   entonces `2^j <= n` y coalescen en el sentido de Gao en ese mismo paso:
   - Nadie pasa por 1: en i pasos no se baja de `n/2^i` (`cota_inferior`), y
     `2^j <= n`. El único caso límite, `n=2^j` justo en el paso j, choca con
     el encuentro, porque n+1 todavía no puede valer 1 (`sin_uno`).
   - Mismas divisiones (`equilibrio`). Con t triplicaciones y m mitades,
     `3^t x <= 2^m C^i(x)` y `3·2^m C^i(x) <= 3^t (3x+2^i)` (`invariante`).
     Si una trayectoria dividiera más, las dos cotas obligarían a
     `18n <= 3(n+1)+2^j`, imposible con `2^j <= n` (`choque`).
2. **Densidades** (`gao_de_lagarias`, `d_de_lagarias`). El conjunto de
   Lagarias está dentro de los que coalescen, salvo `n=2^k-1` en el conteo
   de `d̄_k`. Como la densidad de aquél tiende a 1
   ([GaoEnunciado](formal/GaoEnunciado.lean)), también `d̄_k` y `d(x)`.
3. **Unión** (`GaoLiteral.lagarias`). El enunciado de Lagarias está escrito
   de nuevo en Hienas, que sólo importa Mathlib. Lean acepta que
   `GaoEnunciado.conjetura_gao` lo demuestra tal cual.

## Contrastes

- [GaoLiteral.lean](formal/GaoLiteral.lean) recalcula con un `#guard`, y con
  las mismas definiciones de Lean, los valores `2^k d̄_k` de k=4 a 12:
  1, 4, 11, 29, 65, 145, 305, 641 y 1317. Son la tabla 3 de Gao. Si no
  coincidieran, el archivo no compilaría.
- [verificar_hienas.py](verificar_hienas.py) reproduce los 21 valores de la
  tabla 3 (k=4 a 24, hasta `d̄_24=0,389`) para todos los `n<2^24`. Encuentra
  6.403.423 n de G y ninguno incumple la definición de Gao.
- `leanchecker` sobre Hienas y GaoLiteral, y `leanchecker --fresh` sobre la
  unión: todo con código 0 ([evidencia](evidencia_gao_lean.json)).

## Alcance

Es un teorema de densidad. No dice que las trayectorias lleguen a 1, y
«coalescer» da la misma altura sólo si llegan, como advierte el propio Gao.
Las otras preguntas del artículo siguen abiertas: rachas arbitrariamente
largas de la misma altura, y si la misma altura implica el mismo tiempo de
parada. La densidad converge muy despacio: `d̄_24=0,389`.
