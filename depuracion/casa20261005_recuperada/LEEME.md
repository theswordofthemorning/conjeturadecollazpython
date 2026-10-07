# Plano de la casa: qué le falta a la prueba de que todo número llega a 1

04-10-2026. El usuario eligió la ruta B, la reducción al absurdo: suponer
un número que no baja y anotar todo lo que tendría que cumplir. Pidió
verla como una casa, con un inventario de las piezas que debe tener
cualquier prueba de Collatz: cuáles ya están y cuáles faltan.

Mapa: `T(n)=n/2` si n es par y `(3n+1)/2` si es impar. El **pronóstico**
de n a los j pasos es `3^S_j(n)/2^j`, donde S_j(n) cuenta las subidas
(pasos impares). El **primer cruce** τ(n) es el primer j en que el
pronóstico baja de 1. El **primer descenso** σ(n) es el primer j con
`T^j(n)<n`. Siempre τ(n) ≤ σ(n).

## La norma: qué hace que una casa sea casa

Collatz sólo puede fallar de dos maneras. Si la órbita de un número no
llega a 1, o se repite (un **circuito** que no pasa por 1) o crece sin
límite (una **fuga**). No hay tercera forma: una órbita acotada termina
repitiendo un valor. Con fuerza bruta se podría encontrar un circuito,
pero nunca confirmar una fuga, porque una órbita no se puede seguir
para siempre.

Toda prueba, tenga la forma que tenga, debe levantar dos muros:

| Muro | Enunciado exacto | Qué impide |
|---|---|---|
| A: el pronóstico no se equivoca para siempre | si τ(n) es finito, σ(n) es finito | los circuitos y las fugas disfrazadas |
| B: el pronóstico siempre llega | τ(n) es finito para todo n ≥ 2 | las fugas puras |

**Collatz equivale a A y B juntos.**
- Si un número no llega a 1, el menor valor m de su órbita nunca baja
  de sí mismo, así que σ(m) es infinito. Si el pronóstico de m llega
  (τ(m) finito), falla A: es un circuito o una fuga disfrazada. Si no
  llega, falla B: es una fuga pura.
- Al revés, si Collatz vale, todo σ es finito y, como τ ≤ σ, se cumplen
  A y B.

El **techo** es ese argumento: une los dos muros y, por inducción, lleva
todo número a 1.

La conjetura CST de Terras (σ = τ: el pronóstico acierta justo en el
cruce) es una versión **reforzada** del muro A, y es la que construye
Ocelotas. El plano usa A y no CST porque, si CST fuera falsa y Collatz
verdadera, A seguiría en pie.

Las puertas A y B de la conversación del 04-10 son estos dos muros:
mientras no estén completos, por ahí se puede colar un contraejemplo.

## Inventario

✔ en pie · ◐ a medias · ✘ falta. «Lean» indica prueba verificada.

### Radier: los hechos básicos

| Pieza | Estado | Dónde |
|---|---|---|
| Fórmula de Terras: `2^j T^j(n) = 3^S_j(n) n + β`, con β ≥ 0 | ✔ Lean | [Ocelotas](../cst20260930/LEEME.md); artículo IV, lema 2.1 |
| Cada patrón de j subidas y bajadas corresponde a una sola clase módulo 2^j | ✔ Lean | [OcelotasResiduos](../cst20260930/OcelotasResiduos.lean), [Tejonas](../gao20260920/Tejonas.md) |
| Antes del primer cruce no hay descenso (τ ≤ σ) | ✔ Lean | `no_desciende_antes` |
| Collatz equivale a que todo n ≥ 2 baje alguna vez de sí mismo | ✔ Lean | `llega_de_descensos`, `desciende_de_llega` |
| Llegar a 1 es lo mismo con el mapa clásico que con el atajo | ✔ Lean | `llega_iff` |
| Sólo hay dos fallas posibles: circuito o fuga | ✔ Lean | `dos_fallas` |

### Muro A: el pronóstico no se equivoca

| Tramo | Estado | Dónde |
|---|---|---|
| Con hasta 24 picos antes del cruce acierta exacto (CST) | ✔ Lean, bajo LMN | [24 rachas](../cst20260930/VEINTICUATRO_LEAN.md); en el plano, `muroA_hasta_24` |
| El muro A solo, aunque sea sin el B, ya excluye los circuitos | ✔ Lean | `muroA_sin_circuitos` |
| Una grieta cumple `(2^k − 3^S_k) n + 2^k ≤ 3^k` en cada paso de cruce k, luego `n < 3^τ(n)` | ✔ Lean | `grieta_desigualdad`, `grieta_pequena` |
| Con el muro A, la órbita de un contraejemplo contiene infinitos fugitivos | ✔ Lean | `contraejemplo_con_muroA`, `minimos_no_bajan` |
| Con hasta 77 picos, sumando el cálculo de Rozier–Terracol | ✔ Lean, dos hipótesis externas | [77 rachas](../cst20260930/SETENTA_Y_SIETE_LEAN.md) |
| CST vale para casi todo n: bajo N falla en menos de `14,5 N^0,969` números | ✔ Lean | [Chinchillas](CHINCHILLAS.md): `fallasCST_potencia` |
| Una falla de CST `n ≥ 2^125000` tiene primer cruce después de `log₂ n + 1` pasos; las fallas grandes son menos de `3 (2N)^0,95` | ✔ Lean, bajo la forma entera de LMN | `falla_tardia`, `fallasCST_lmn_potencia` |
| Para cada cantidad fija de picos, los fallos posibles caben en una región finita explícita | ✔ Lean, bajo LMN | [Cota general](../cst20260930/COTA_GENERAL.md), [cola](../cst20260930/COLA_PARAMETRICA.md) |
| CST comprobada para todo n ≤ 2,8·10^19 | ✔ externo | Rozier–Terracol (2026), corolario 5.4 |
| Ningún circuito tiene 91 picos o menos | ✔ externo | Hercher (2023) |
| Cualquier cantidad de picos | ✘ | haría falta el «dominó»: reducir muchos picos a menos |

El muro A completo implica que no hay circuitos, un problema abierto.

### Muro B: el pronóstico siempre llega

| Tramo | Estado | Dónde |
|---|---|---|
| Casi todo número (densidad 1) tiene primer cruce | ✔ Lean | [Corzas](CORZAS.md): `fugitivos_densidad_cero`; Terras (1976), Everett (1977) |
| Casi todo número baja alguna vez de sí mismo | ✔ Lean | `casi_todos_descienden`; no es Wu 1, que sigue abierta |
| El tiempo de parada σ tiene distribución límite `1 − d_K/2^K`, que tiende a 1 | ✔ Lean | `terras_distribucion`, `terras_limite` (Terras 1976) |
| Casi todo número baja por debajo de `n^c`, para todo `c > log 3/log 4 ≈ 0,7925` | ✔ Lean | [Chinchillas](CHINCHILLAS.md): `korec`; Korec (1994), Allouche (1979) |
| Bajo N, menos de `14,5 N^0,969` números nunca bajan de sí mismos, y menos de `(2N)^0,95` son fugitivos | ✔ Lean | `noDescienden_potencia`, `fugitivos_potencia`; el menor contraejemplo estaría ahí |
| Identidad afín `T^k(r + 2^k t) = T^k(r) + 3^S t` y el residuo 3-ádico fijado por el 2-ádico | ✔ Lean | [Perdices](PERDICES.md): `iter_afin`, `tres_determinado`, `paridad_independiente` |
| `T^k(r) mod 3^m`, con r uniforme, tiene exactamente la ley de una cadena de Markov en `ℤ/3^m` | ✔ Lean | `ley_de_la_cadena`, `cadena_correcta`, `palabra_sobre` |
| Mezcla fina 3-ádica (Tao 2019, proposiciones 1.14 y 1.17), que salta la barrera de Korec | ✘ | medida hasta `3^14`, compatible con Tao; sin prueba en Lean |
| Casi toda órbita alcanza valores casi acotados | ✔ externo | Tao (2019) |
| Un número sin primer cruce nunca baja de sí mismo ni llega a 1 | ✔ Lean | `fuga_pura_no_baja`, `fuga_pura_no_llega` |
| El muro B es exactamente «no hay fugas puras» | ✔ Lean | `muroB_iff` |
| Un número sin primer cruce tiene órbita no acotada y nunca repite un valor | ✔ Lean | `fugitivo_no_acotado`, `fugitivo_no_repite`; artículo IV, observación 10.1 |
| Sube en más de 63 de cada 100 pasos, en todo prefijo | ✔ Lean | `fugitivo_63`; log 2 / log 3 ≈ 0,631 |
| Es ≡ 3 (mod 4) | ✔ Lean | `fugitivo_tres_mod_cuatro` |
| Su patrón de subidas y bajadas nunca se vuelve periódico | ✔ Lean | `fugitivo_no_periodico`: un patrón periódico lleva a un ciclo |
| «No hay fugas» equivale a que todo natural tenga patrón finalmente periódico, y eso levanta el muro B | ✔ Lean | `sin_fugas_iff_periodicidad`, `muroB_de_periodicidad` |
| Ningún choque en un tramo finito: para cada K hay n ≥ 2 sin cruce en K pasos | ✔ Lean | `sin_choque_finito` |
| Todo número, sin excepción | ✘ | es «no hay fugas puras», abierto |

### Ventanas: dejan entrar luz, pero no sostienen la casa

- Todo número hasta 2^71 llega a 1 (verificación externa, Barina 2025).
- Gao, Garner y Wu 2, en Lean: casi todos los pares de consecutivos se
  juntan pronto, y hay bloques tan largos como se quiera de consecutivos
  que llegan juntos a 1. Son familias que llegan, no todo número.
- Ni siquiera «casi todo número llega a 1» está demostrado: es Wu 1,
  abierta; [Nashida](../nashida20260928/LEEME.md) es un puente condicional.

### Instalaciones: las herramientas

- **Luz:** Lean 4 con Mathlib; todo lo nuestro se verifica ahí.
- **Agua:** LMN, la cota de formas lineales en dos logaritmos, que es la
  que mueve el muro A.
- **Gas:** la maquinaria de densidad de la cadena de Gao (cadenas de
  Markov, martingalas), probada en Lean; candidata para el muro B.
- Certificados exactos por árboles de clases, comprobados en el núcleo
  de Lean.

### Techo

✔ En Lean desde el 04-10: `techo` (con A y B, todo número llega a 1) y
`collatz_iff_muros` (Collatz equivale a tener los dos muros). Con los dos
muros no queda ni circuito ni fuga: `casa_sin_fallas`. El techo está
puesto, pero la casa sigue abierta mientras falten tramos de los muros.

## El plano en Lean

Hecho el 04-10, a pedido del usuario («me parece bien lo de Lean,
hazlo»). [CasaPlano.lean](CasaPlano.lean) define los dos muros, el
circuito, la fuga, la fuga pura y la llegada a 1, y demuestra sin
hipótesis externas:

| Teorema | Qué dice |
|---|---|
| `collatz_iff_muros` | Collatz, con el mapa clásico, equivale a tener los muros A y B |
| `techo` | con A y B, todo número llega a 1 |
| `llega_iff` | llegar a 1 es lo mismo con el mapa clásico que con el atajo |
| `dos_fallas` | una órbita que no llega a 1 contiene un circuito o es una fuga |
| `muroA_sin_circuitos` | el muro A, por sí solo, excluye los circuitos |
| `casa_sin_fallas` | con los dos muros no queda ni circuito ni fuga |
| `muroB_iff` | el muro B es exactamente «no hay fugas puras» |
| `fuga_pura_no_baja`, `fuga_pura_no_llega` | una fuga pura nunca baja de su punto de partida ni llega a 1 |
| `muroA_de_cst`, `muroA_de_tramos` | CST, o todos los tramos por número de picos, levantan el muro A |

[CasaOcelotas.lean](CasaOcelotas.lean) engancha el cierre de Ocelotas:
`muroA_hasta_24` (bajo LMN, el tramo de hasta 24 picos está en pie) y
`grieta_exige_25` (una grieta en el muro A necesita al menos 25 picos
antes del primer cruce).

Los muros que faltan son definiciones: nada en estos archivos afirma
que se cumplan.

[comprobar_casa.py](comprobar_casa.py) verificó por huellas los 670
módulos de Ocelotas importados (20 de la base y 650 del cierre de 24),
compiló los dos archivos en 36 y 34 segundos y auditó sus 19 consultas:
sólo `propext`, `Classical.choice` y `Quot.sound`, sin `sorryAx` ni
avisos ([evidencia](evidencia_casa.json), [salida](evidencia_casa.txt)).
Lean 4.32.2. Para reproducirlo, desde la raíz:

```text
python -B -X utf8 depuracion/casa20261004/comprobar_casa.py --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_veinticuatro_paralelo_20261004 --salida depuracion/casa20261004/evidencia_casa.json
```

Las cachés sólo se leen. Si se borran, hay que reconstruirlas antes con
los comprobadores de Ocelotas.

## El retrato del fugitivo

Hecho el 05-10: [Corzas](CORZAS.md), con
[CasaFugitivo.lean](CasaFugitivo.lean), [CasaCasiTodos.lean](CasaCasiTodos.lean),
[CasaChoques.lean](CasaChoques.lean), [CasaTerras.lean](CasaTerras.lean) y
[CasaDomino.lean](CasaDomino.lean). Después, Korec y el ahorro de potencia:
[Chinchillas](CHINCHILLAS.md), con [CasaKorec.lean](CasaKorec.lean) y
[CasaPotencia.lean](CasaPotencia.lean) y, bajo LMN, [CasaLMN.lean](CasaLMN.lean);
y el lado 3-ádico, delimitado:
[Perdices](PERDICES.md), con [CasaTres.lean](CasaTres.lean) y [CasaCadena.lean](CasaCadena.lean).
Reconstrucción desde las fuentes,
sin cachés, con [comprobar_fugitivo.py](comprobar_fugitivo.py)
([evidencia](evidencia_fugitivo.json)); contraste independiente en
[cotejar_fugitivo.py](cotejar_fugitivo.py), [cotejar_korec.py](cotejar_korec.py),
[cotejar_potencia.py](cotejar_potencia.py), [cotejar_lmn.py](cotejar_lmn.py),
[cotejar_tres.py](cotejar_tres.py) y [cotejar_cadena.py](cotejar_cadena.py);
medición de la mezcla 3-ádica en [medir_mezcla_tres.py](medir_mezcla_tres.py).

## Ruta a seguir

Acordada con el usuario el 04-10, al cerrar la sesión.

**Sin fuerza bruta.** No se amplía Ocelotas a 25 rachas ni a más. Cada
racha añade un tramo al muro A, pero el muro completo exige todos los
tramos a la vez (`muroA_de_tramos`). Son infinitos, y uno por uno no se
termina nunca. El muro B ni siquiera tiene una versión por rachas. Lo que
falta se construye con argumentos que valgan para todos los casos a la
vez, no con más cálculo. Los tramos ya hechos no se pierden: quedan en
pie y dejan herramientas (LMN, cribas, certificados en Lean).

Orden de trabajo, de lo más chico a lo más grande:

1. **El plano en Lean**: hecho el 04-10 (sección anterior).
2. **El retrato del fugitivo**: hecho el 05-10 ([Corzas](CORZAS.md)).
   En Lean: órbita no acotada, patrón nunca periódico, más de 63 subidas
   de cada 100 pasos, `n ≡ 3 (mod 4)` y densidad cero; además, casi todo
   número baja de sí mismo (Terras, Everett), y el tiempo de parada tiene
   distribución límite (Terras). Después ([Chinchillas](CHINCHILLAS.md)):
   casi todo número baja por debajo de `n^c` para `c > log 3/log 4`
   (Korec), la barrera de los métodos 2-ádicos, y una potencia `N^0,969`
   para los que nunca bajan y para las fallas de CST (`0,95` bajo LMN,
   por encima de `2^125000`). El paso 3-ádico
   hacia Tao, delimitado ([Perdices](PERDICES.md)): identidad afín en
   Lean; la mezcla fina queda medida, sin prueba.
3. **Buscar choques** (abierto). Dos rasgos del fugitivo que se
   contradigan, o uno que choque con algo ya demostrado: la cadena de Gao
   o las cotas de Ocelotas. Si aparece, el muro B queda en pie. Nadie lo
   ha logrado; ésta es la apuesta. Delimitado el 05-10, sin avance de
   fondo ([Corzas](CORZAS.md#paso-3-dónde-puede-estar-un-choque)): no hay
   choque en ningún tramo finito, y el choque que falta equivale a la
   periodicidad de Lagarias para los naturales, abierta.
4. **El dominó del muro A** (abierto). Una reducción que convierta una
   grieta con R+1 picos en otra con menos, o una desigualdad que valga
   para todo R a la vez. Completar el muro A incluye demostrar que no hay
   circuitos.
   Delimitado el 05-10, sin avance de fondo
   ([Corzas](CORZAS.md#paso-4-cómo-tendría-que-ser-una-grieta)): la
   desigualdad de la grieta vale para todo R, pero sola no basta; lo que
   falta es la cota palabra por palabra para todas las palabras, que es
   CST.
5. **Los muros completos.** A completo incluye «no hay circuitos», y B
   completo es «no hay fugas puras». Son los dos problemas abiertos del
   centro de Collatz.

Cada pieza se trabaja con presupuesto acotado, como en el
[plan del 28-09](../transversal20260927/PLAN_SESIONES_20260928.md): si no
avanza, se escribe por qué y se cierra.

**Duda abierta del usuario, 04-10:** «¿para terminar de construir los
muros necesitamos la racha 25, 26 y así sucesivamente? Eso nos dejaría
exactamente al principio del problema». No: ese camino no termina
nunca, y la ruta B existe justamente para evitarlo. Queda para pensarla
en la próxima sesión.
