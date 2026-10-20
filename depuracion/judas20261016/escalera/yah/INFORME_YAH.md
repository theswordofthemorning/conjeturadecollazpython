# Informe de las tandas de YAH — 19-10-2026

## Resumen

Ningún sistema con las dos ramas dio prueba. El peldaño 5 (G completo) y
las dos debilitadas mínimas, G_A2 y G_B4, se comportan igual ante la
cascada: caen sólo las reglas con L y quedan 11 reglas que resisten a todas
las formas de dimensión ≤ 3. Cada rama sola (peldaños 3 y 4) da QED en
segundos. Lo que estas formas no superan es la mezcla de las dos ramas, aun
en su versión más estrecha. Sin una idea nueva, más horas de YAH no
prometen nada.

## Mapa, dominio y sistemas

- G(z) = 3z/2 si z es par; G(z) = (9z+1)/8 si z ≡ 7 (mod 8); para en las
  demás clases. Dominio: z entero, z ≥ 1. Un paso es una aplicación de G.
- G_A2: la rama A sólo actúa si z ≡ 2 (mod 4). G_B4: la rama B sólo actúa
  si z ≡ 7 (mod 16). Peldaño 3: sólo la rama A. Peldaño 4: sólo la rama B.
- Los sistemas de reescritura codifican cada función en la base mixta de
  YAH ([srs_piloto.py](../../srs_piloto.py), [debilitar.py](debilitar.py)).
  Que el sistema termine equivale a que la función pare en todo z ≥ 1.
  Para G está probado en Lean (`piloto_iff`,
  [JudasPiloto.lean](../../JudasPiloto.lean)); para las debilitadas, sólo
  comprobado por simulación en z < 2^12.
- Los tiempos son de pared.

## Resultados

Tras quitar las reglas con L, los tres residuos tienen la misma forma: las
9 reglas X, una regla de la rama A y una de la rama B.

| Sistema | Rama A del residuo | Rama B del residuo |
|---|---|---|
| G (peldaño 5) | `f R -> a0 R` (todo z par) | `t t t R -> a2 a2 R` (todo z ≡ 7 mod 8) |
| G_A2 | `t f R -> a1 t R` (sólo z ≡ 2 mod 4) | `t t t R -> a2 a2 R` |
| G_B4 | `f R -> a0 R` | `f t t t R -> a1 a1 f R` (sólo z ≡ 7 mod 16) |

| Sistema | Tanda | Caen | UNSAT sobre el residuo | Sin decidir |
|---|---|---|---|---|
| G | 120, 900 y 3600 s por forma; 15:54–22:26, parada | `L t t R -> L f f f R` | dimensión ≤ 3; tropical d4 (19 y 30 s); natural d4 (421 y 509 s) | natural d5 y d6; ártica d4 y d5 |
| G_A2 | 120, 900 y 3600 s por forma; 16:53–22:26, parada | `L f R -> L t R` y `L t t R -> L f f f R` | dimensión ≤ 3; tropical d4 (116 y 226 s); natural d4 (723 y 1691 s) | natural d5 y d6; ártica d4 y d5 |
| G_B4 | 30 s por forma; 22:43–22:50, completa | `L t t R -> L f f f R` | dimensión ≤ 3; tropical d4 (23 y 25 s) | natural d4 a d6; ártica d4 y d5 |

«Dimensión ≤ 3» son las 11 formas natural d1–d3 y ártica y tropical d2–d3,
en las dos orientaciones. Los pares de tiempos corresponden a las dos
orientaciones. «Sin decidir» son las formas que agotaron su tope: hasta
900 o 3600 s en G y G_A2, y 30 s en G_B4.

### Diagnóstico de 30 minutos

Perfil `--diagnostico` de [PLAN_YAH.md](PLAN_YAH.md): cuatro
solucionadores, 30 s por forma y 1800 s en total. Duró 7 min 31 s y se
detuvo, como prevé el plan, en el primer sistema sin prueba.

- Calibración: los peldaños 1 a 4 dan QED en 5 s, con las mismas formas
  que la calibración anterior de 60 s.
- G_B4: 43 corridas en 7 min 26 s; quedan 11 reglas.
- G_B5, G_B6 y G_B7 no se corrieron (ver el punto 2 de abajo).

## Qué se puede afirmar

1. **Medición.** Cada UNSAT dice que ninguna interpretación de esa forma
   (tipo, dimensión, ancho y orientación) orienta todas las reglas del
   residuo de forma débil y alguna de forma estricta. Lo decide CaDiCaL; no
   se guardó certificado del UNSAT.
2. **Prueba escrita: subir k no ayuda con estas formas.** Las familias
   están anidadas como conjuntos de reglas: G_A2 ⊂ G_A3 ⊂ G_A4 ⊂ G_A5 y
   G_B4 ⊂ G_B5 ⊂ G_B6 ⊂ G_B7 (comprobado comparando los ficheros de
   `sistemas/`). En una prueba en cascada de G_B5, la etapa que quita la
   primera de las 11 reglas del residuo de G_B4 todavía las tiene todas,
   así que su interpretación también vale para ese residuo. Por tanto no es
   de ninguna forma que allí dio UNSAT, en ninguna orientación. Lo mismo
   vale para G_B6 y G_B7, y para G_A3…G_A5 respecto de G_A2.
3. **Por qué cae cada rama sola.** La rama A sola baja v2(z) en 1 en cada
   paso. La rama B sola baja v2(z+1) en 3, porque (9z+1)/8 + 1 = 9(z+1)/8.
   En las mezclas, al acabar una racha de una rama, la valuación de la otra
   depende de cifras altas aún no usadas, y ninguna de las dos decrece.
   Además cada paso aumenta z (3z/2 > z y (9z+1)/8 > z): no hay ciclos, y
   parar siempre equivale a no tener órbitas divergentes.
4. **Hipótesis, no comprobada.** Para este método, la primera mezcla ya
   tiene la dificultad de G: los tres residuos se comportan igual. Si es
   así, lo que falta es una medida o una barrera, no tiempo de CPU.

## Lo que no se afirma

- Que G, G_A2 o G_B4 no terminen, ni que no tengan prueba matricial: las
  formas de dimensión ≥ 4 siguen sin decidir. En G_A2, decidir natural d4
  costó 12 y 28 minutos.
- Ningún QED nuevo. No hay nada que certificar en Lean salvo los QED de
  calibración.
- La equivalencia entre cada sistema debilitado y su función sigue
  comprobada sólo por simulación.

## Siguiente decisión

Recomiendo no relanzar pasadas largas de la cascada. En orden:

1. **Auditoría de Nashida** sobre G_A2 y G_B4, ya preparada en
   [PLAN_YAH.md](PLAN_YAH.md) («Nashida: qué comprobar antes de ampliar»)
   y en [ccchallenge20261019](../../../ccchallenge20261019/PLAN.md). No
   gasta horas de CPU y dice si hay una barrera estructural que explique la
   resistencia.
2. **G_B4 a mano.** Es el sistema más pequeño que resiste (11 reglas, dos
   dinámicas): buscar una medida, o el motivo de que no haya una simple.
3. **Una sola forma larga**, y sólo si 1 o 2 señalan cuál (por ejemplo,
   natural d4 sobre G_B4).

## Evidencia

- [resultados_diagnostico/](resultados_diagnostico/): `consola.txt`,
  `resumen.json` (SHA-256 de los 8 sistemas, presupuesto y motivo de
  detención), un registro por corrida y los residuos. Copia exacta de
  `~/herramientas/yah/resultados/diagnostico-Wn7vGEih/` sin `trabajo/`.
- [resultados/](resultados/) (G) y
  [resultados_debilitadas/](resultados_debilitadas/) (G_A2): tandas largas,
  commits `9225ac2` y `1e066b0`.
- YAH `8a4dfda` con el parche de `prover/sat.py` (`randint` con `10**9`),
  Python 3.12.3 y CaDiCaL 3.0.1 ([LEEME.txt](LEEME.txt)).
- SHA-256 de `sistemas/G_B4.srs`:
  `cc35118ef03067a72c82dcb11b81862c370d416359dd890be082621aa6ff8aba`.

## Cambio en el lanzador

`lanzar.sh` usa ahora un candado fijo, `/tmp/collatz-yah-<uid>.lock`, se
lance con sudo o desde el escritorio; antes dependía de `XDG_RUNTIME_DIR`.
Con `--fondo`, si ya corre otra tanda, avisa y no crea carpeta; antes la
tanda nueva se cerraba sin mensaje. Probado con el candado ocupado
(rechazo, código 1) y libre (ensayo del peldaño 1, QED).
