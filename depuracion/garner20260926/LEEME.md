# Ruta de Garner (1985): rachas arbitrariamente largas de la misma altura

26-09-2026. **Siguiente ruta, elegida por el usuario.** Candidata: sin
prueba escrita completa ni formalización. Todavía no se ha comprobado si
ya está demostrada.

## La conjetura

Garner (1985, Discrete Math. 55, 57–64) conjeturó dos cosas, según Lagarias
(bibliografía anotada 1963–1999, entrada 72):

1. La mayoría de los enteros tienen la misma altura que un vecino.
2. **Hay rachas arbitrariamente largas de enteros consecutivos con la misma
   altura.**

Gao (1993, pág. 262) recoge la segunda, con altura y tiempo total de parada
iguales, y la atribuye a Garner y a Penning. La altura de n es el número de
pasos de `C(n)=n/2 | 3n+1` hasta llegar a 1.

Lo que se sabe:

- Penning (1989), Gao (1993, lema 1) y Wu (1993): una racha de largo L da
  infinitas del mismo largo.
- Los récords se han buscado por cómputo. [A078441](https://oeis.org/A078441)
  da el primer comienzo de una racha de n; no dice que exista para todo n.
  [A277109](https://oeis.org/A277109) mira rachas desde `2^n+1` y llega a
  `2^50-1`. Frinkle et al. (2025, J. Supercomputing) las calculan.
- No se halló una prueba de existencia para todo L. La búsqueda fue breve.

## Idea de prueba (sin formalizar)

Mapa atajo `T`. Para `n=2^t u+r`, `T^t(n)=3^a u+A` con a y A según r.

1. **Muchos pares fusionados.** Por [Martas](../gao20260920/Martas.md) y
   `TejonasGao.transporte`, la proporción de residuos r módulo `2^t` cuyo
   par `(r,r+1)` fusiona por clases hasta t es `P(sigma<=t)->1`.
2. **Un bloque entero.** Por unión de cotas, la proporción de r en
   `[0,2^t-L)` con los L pares `(r+i,r+i+1)` fusionados es al menos
   `1-L·P(sigma>t)-L/2^t`, que es positiva para t grande.
3. **Un solo valor común.** En ese bloque todos los `n_i=2^t u+r+i`, con
   `i=0..L`, tienen el mismo `3^a u+A` tras t pasos, para todo u
   (`canon_rep`, `iter_rep`).
4. **Llegar a una potencia de 2.** Tras un paso impar ningún valor es
   múltiplo de 3, así que A es coprimo con 3. Como 2 es raíz primitiva
   módulo `3^a`, hay `m>=3` con `2^m = A (mod 3^a)`. Con
   `u=(2^m-A)/3^a`, todos valen `2^m` en el paso clásico `t+a`.
5. **Misma altura.** Nadie llegó antes a 1: si no, en el paso `t+a`
   estaría en {1,2,4}, no en `2^m` con `m>=3`. Todos tienen altura `t+a+m`
   y `t+m` divisiones por 2.

Si todo se sostiene, para cada L hay L+1 consecutivos con la misma altura y
el mismo tiempo total de parada. Garner (1) con alturas finitas no sale de
aquí: haría falta saber que casi todos llegan a 1.

## Sondeo

[sondeo_rachas.py](sondeo_rachas.py) sigue los pasos 1 a 5 con t de 2 a 20
y calcula las alturas iterando de verdad. Tarda unos segundos.

| t | pares fusionados | consecutivos | altura | cifras de u |
|---|---|---|---|---|
| 8 | 0,3216 | 5 (r=98) | 24 | 3 |
| 11 | 0,3522 | 6 (r=386) | 77 | 16 |
| 15 | 0,3800 | 9 (r=1680) | 340 | 94 |
| 20 | 0,4021 | 23 (r=614402) | 1049 | 304 |

En todos los casos las alturas y las divisiones coinciden. Los residuos 98,
386 y 1680 son términos de A078441. Es un control finito, no una prueba.

## Pasos, en orden

1. **Novedad.** Leer Garner (1985) y Frinkle et al. (2025), y buscar en
   zbMATH o MathSciNet si ya se demostró.
2. **Prueba escrita.** Revisar sobre todo:
   - la unión de cotas y el borde `r+L<2^t`;
   - que A es coprimo con 3;
   - el argumento de «nadie llega antes a 1».
3. **Lean.** Reutilizar `transporte`, `canon_modulo`, `iter_rep` y `martas`.
   Falta demostrar:
   - la unión de cotas sobre L desplazamientos;
   - que 2 es raíz primitiva módulo `3^a`, por elevación del exponente o
     con `ZMod`;
   - la igualdad de alturas.
4. **OEIS.** Sólo tras la revisión, y con autorización del usuario: un
   comentario en A078441 de que a(n) existe para todo n.
