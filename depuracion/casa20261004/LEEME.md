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
| Antes del primer cruce, el tamaño va pegado al pronóstico: `n·3^S/2^k ≤ T^k(n) ≤ (n + S/3)·3^S/2^k` | ✔ Lean | `tamano_antes_del_cruce` |

### Muro A: el pronóstico no se equivoca

| Tramo | Estado | Dónde |
|---|---|---|
| Con hasta 24 picos antes del cruce acierta exacto (CST) | ✔ Lean, bajo LMN | [24 rachas](../cst20260930/VEINTICUATRO_LEAN.md); en el plano, `muroA_hasta_24` |
| El muro A solo, aunque sea sin el B, ya excluye los circuitos | ✔ Lean | `muroA_sin_circuitos` |
| En la casa del vecino (5n+1) el muro A se cae: el 13 cruza y nunca baja de sí mismo | ✔ Lean | `vecino_grieta`: la prueba del muro A tiene que usar algo propio del 3 |
| Con hasta 77 picos, sumando el cálculo de Rozier–Terracol | ✔ Lean, dos hipótesis externas | [77 rachas](../cst20260930/SETENTA_Y_SIETE_LEAN.md) |
| Para cada cantidad fija de picos, los fallos posibles caben en una región finita explícita | ✔ Lean, bajo LMN | [Cota general](../cst20260930/COTA_GENERAL.md), [cola](../cst20260930/COLA_PARAMETRICA.md) |
| CST comprobada para todo n ≤ 2,8·10^19 | ✔ externo | Rozier–Terracol (2026), corolario 5.4 |
| Ningún circuito tiene 91 picos o menos | ✔ externo | Hercher (2023) |
| Cualquier cantidad de picos | ✘ | haría falta el «dominó»: reducir muchos picos a menos |

El muro A completo implica que no hay circuitos, un problema abierto.

### Muro B: el pronóstico siempre llega

| Tramo | Estado | Dónde |
|---|---|---|
| Casi todo número (densidad 1) tiene primer cruce | ✔ Lean | `rasgo_raro`; Terras (1976), Everett (1977) |
| Casi toda órbita alcanza valores casi acotados | ✔ externo | Tao (2019) |
| Un número sin primer cruce nunca baja de sí mismo ni llega a 1 | ✔ Lean | `fuga_pura_no_baja`, `fuga_pura_no_llega` |
| El muro B es exactamente «no hay fugas puras» | ✔ Lean | `muroB_iff` |
| Un número sin primer cruce tiene órbita no acotada; más aún, nunca repite un valor y crece hacia el infinito | ✔ Lean | `rasgo_fuga`, `rasgo_sin_repetir`, `rasgo_infinito` |
| Sube en al menos 63 de cada 100 pasos, en todo momento | ✔ Lean | `rasgo_sube` |
| Su patrón de subidas y bajadas nunca se vuelve periódico | ✔ Lean | `rasgo_no_periodico` |
| Por debajo de 2^(100m) hay a lo sumo 2·2^(96m) números sin primer cruce (unos x^0,96 por debajo de x) | ✔ Lean | `rasgo_pocos` |
| En su órbita hay puntos sin retorno, tan lejos como se quiera: valores de los que nunca vuelve a bajar | ✔ Lean | `rasgo_minimos` |
| Su tamaño va pegado a su pronóstico, en todo momento | ✔ Lean | `rasgo_tamano` |
| Es cohete (su pronóstico crece sin límite y su órbita está llena de fugas puras) o planeador (vuelve una y otra vez a tamaños que crecen apenas como el tiempo) | ✔ Lean | `rasgo_cohete_o_planeador` |
| Con el muro A nunca anda solo: sus puntos sin retorno son fugas puras | ✔ Lean | `crias_con_muroA`, `fugas_sin_tope` |
| Con el tramo de Ocelotas, sus puntos sin retorno son fugas puras o cruzan con al menos 25 picos | ✔ Lean, bajo LMN | `crias_con_ocelotas` |
| Si ninguna órbita crece sin límite, el muro B está en pie | ✔ Lean | `muroB_de_sin_fugas` |
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

Desde el 06-10 hay también un segundo plano de la misma casa, el
clásico: Collatz equivale a que no haya circuitos ni fugas
(`collatz_iff_sin_intrusos`). Los dos planos se conectan así: el muro A
excluye los circuitos (`muroA_sin_circuitos`) y la falta de fugas levanta
el muro B (`muroB_de_sin_fugas`).

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

## El retrato del fugitivo en Lean

Hecho el 06-10, a pedido del usuario («continúa con la investigación»).
[CasaRetrato.lean](CasaRetrato.lean) supone una fuga pura, un número
cuyo pronóstico nunca baja de 1, y demuestra sin hipótesis externas lo
que tendría que cumplir:

| Teorema | Rasgo |
|---|---|
| `fuga_pura_dos` | es al menos 2 (el 0 y el 1 cruzan) |
| `rasgo_sube` | en todo momento lleva al menos 63 subidas de cada 100 pasos, porque 3^63 < 2^100 |
| `rasgo_sin_repetir`, `rasgo_infinito`, `rasgo_fuga` | su órbita nunca repite un valor y crece hacia el infinito; si repitiera, daría vueltas a un ciclo y el pronóstico de cada vuelta bajaría de 1 (`ciclo_cruza`) |
| `rasgo_no_periodico` | su patrón de subidas y bajadas nunca se vuelve periódico: dos números con el mismo patrón completo son el mismo número (`mismo_patron_iguales`), y entonces la órbita repetiría un valor |
| `rasgo_raro_cuenta`, `rasgo_raro` | casi ningún número es así: entre 0 y N−1 hay a lo sumo N/16^m + 2^(96m) fugas puras, para cada m, y su densidad es cero |
| `retrato` | los rasgos de un mismo número, juntos |

La rareza sale de contar patrones. Dos números con las mismas k primeras
subidas y bajadas coinciden módulo 2^k (`misma_paridad_congruentes`), así
que en cada bloque de 2^k números hay un número por patrón. Si a los
100m pasos el pronóstico aún no bajó de 1, el patrón tiene al menos 63m
subidas. Cada patrón así pesa al menos 2^(63m) en la suma de 2^subidas,
que vale 3^(100m), y como 3^100 ≤ 2^159 no pasan de 2^(96m)
(`pocos_patrones`, `cuenta_sin_cruce`).

[cotejo_retrato.py](cotejo_retrato.py) lo contrasta sin Lean: las dos
desigualdades; los 2^k patrones distintos para k ≤ 12; el conteo número
por número igual al conteo por patrones para k ≤ 18; y la fracción exacta
sin cruce a los 100, 200 y 300 pasos, de 3,32·10⁻³, 8,21·10⁻⁵ y 2,25·10⁻⁶,
bajo el tope de 1/16, 1/256 y 1/4096. La fracción que no cruza en
ningún paso cae de 2,39·10⁻⁴ a los 100 pasos a 5,47·10⁻⁸ a los 300; en la
casa del vecino (5n+1) se queda en 0,176.

**Lo que el retrato no dice.** Los rasgos no se contradicen entre sí.
Los de patrón (63 de cada 100, nunca periódico) los cumplen muchísimos
patrones infinitos, y cada patrón infinito corresponde a un «número» con
infinitas cifras binarias (un 2-ádico). Un choque tendrá que usar que el
fugitivo es un número común, con cifras finitas. Ése es el paso 3. Un
ejemplo de lo fino que es: con el atajo, (3·(−1)+1)/2 = −1, así que el −1
sube en cada paso y su pronóstico nunca baja de 1, pero da vueltas en su
sitio. `ciclo_cruza` lo descarta sólo porque exige un número positivo.

## Paso 3: el tablero del choque

Primera ronda, 06-10, a pedido del usuario («sigue con lo del choque»).
El usuario propuso además que el retrato crezca de cuatro rasgos a cinco
o seis hasta acorralar al fugitivo, y que la casa gane terminaciones con
teoremas nuevos, de modo que las dos cosas se alimenten entre sí.
[CasaTablero.lean](CasaTablero.lean) trae lo de esta ronda, sin
hipótesis externas salvo LMN en un solo teorema.

**Qué es acorralar.** Cada rasgo nuevo achica el retrato, pero el
fugitivo sólo queda descartado cuando dos rasgos no pueden cumplirse a
la vez. Antes de buscar esa pareja, cada rasgo pasa dos pruebas de
fuego.

- **La del fantasma.** ¿Lo cumple también un «número» con infinitas
  cifras binarias? Si lo cumple, no sirve para el choque, porque el
  fantasma existe. Con la misma regla en los enteros con signo, el −1, el
  −5 y el −17 dan vueltas sin que su pronóstico baje nunca de 1
  (`fantasma_nunca_cruza`, para el −1). Todo baile periódico que nunca
  cruza es el de un número negativo: el número es −c/(3^s − 2^p), y una
  vuelta multiplica el pronóstico por 3^s/2^p > 1. También hay fantasmas
  sin baile periódico: el baile con subidas de pendiente 1/√2 nunca
  cruza, y su número tiene unos y ceros sin fin, así que no es un entero.
- **La del vecino.** ¿Vale también en la casa de 5n+1? Allí el muro A se
  cae de verdad: el pronóstico del 13 baja de 1 a los 7 pasos (5^3 = 125 <
  128 = 2^7), pero el 13 nunca baja de sí mismo y da vueltas por 13 → 33 →
  83 → 208 → 104 → 52 → 26 → 13 (`vecino_grieta`). Y el 7 lleva 100 000
  pasos sin cruzar: todo indica que es un fugitivo de verdad, aunque nadie
  lo ha demostrado.

**El tablero.** Un rasgo es *de carne y hueso* si el fantasma no lo
cumple o no tiene sentido para él: usa que el fugitivo es un número
común, positivo y con cifras finitas. Es *del 3* si no vale en la casa
del vecino.

| Rasgo | Lean | ¿Fantasma? | ¿Vecino? | Tipo |
|---|---|---|---|---|
| 1. Sube en al menos 63 de cada 100 pasos | `rasgo_sube` | lo cumple | vale (allí, 44 de cada 100) | ninguno |
| 2. Nunca repite un valor y crece hacia el infinito | `rasgo_infinito` | el −1 da vueltas; «crecer» no tiene sentido para un fantasma | vale | de carne y hueso |
| 3. Su baile nunca se vuelve periódico | `rasgo_no_periodico` | lo cumple el de pendiente 1/√2 | vale | ninguno |
| 4. Es raro: a lo sumo unos x^0,96 por debajo de x | `rasgo_raro`, `rasgo_pocos` | los fantasmas también son raros | no vale: allí el 17,6 % no cruza en 300 pasos | del 3 |
| 5. Puntos sin retorno: tan lejos como se quiera hay valores de los que nunca vuelve a bajar | `rasgo_minimos` | no tiene sentido | vale | de carne y hueso |
| 6. Su tamaño va pegado al pronóstico | `rasgo_tamano` | no tiene sentido | vale, con S/5 en vez de S/3 | de carne y hueso |
| 7. Cohete o planeador | `rasgo_cohete_o_planeador` | el de pendiente 1/√2 es cohete | vale | de carne y hueso, a medias |

El rasgo 7 separa dos especies de fugitivo. El **cohete** tiene un
pronóstico que crece sin límite, y entonces su órbita está llena de
fugas puras, sin ayuda del muro A: cada paso desde el que el pronóstico
ya nunca baja deja una (`fuga_de_minimo`). El **planeador** vuelve una y
otra vez por debajo de un mismo nivel C, y entonces regresa una y otra
vez a tamaños que crecen apenas como el tiempo: `3·T^k(n) ≤ C·(3n + k)`.

**La pinza.** Hay rasgos de los dos tipos, pero hablan de cosas
distintas: el del 3 cuenta cuántos fugitivos puede haber, y los de carne
y hueso describen a uno solo. Para que choquen hace falta una pinza: un
brazo dice «hay pocos» (rasgo 4, en Lean) y el otro tendría que decir
«si hay uno, hay muchos». Hoy el segundo brazo da esto:

- con el muro A, los puntos sin retorno del fugitivo son, a su vez, fugas
  puras (`crias_con_muroA`), y las hay tan grandes como se quiera
  (`fugas_sin_tope`);
- con el tramo de Ocelotas, bajo LMN, cada punto sin retorno es una fuga
  pura o cruza con al menos 25 picos (`crias_con_ocelotas`);
- un cohete deja crías fugitivas aun sin el muro A.

Pero las crías van en fila sobre una sola órbita, y la rareza permite
hasta x^0,96 fugitivos por debajo de x: «infinitas» no alcanza. Hacia
atrás tampoco: un fugitivo cuya órbita pasa por n es menor o igual que n
(`fuga_pura_no_baja`), así que sólo hay una cantidad finita. La pinza no
cierra.

**Ideas probadas en esta ronda.**

| Idea | Por qué no cierra |
|---|---|
| Que choquen los rasgos de baile (1, 3 y «nunca cruza») | el fantasma de pendiente 1/√2 los cumple todos a la vez |
| La pinza: rareza contra crías | las crías van en fila sobre una sola órbita; harían falta muchísimas más |
| Tamaño contra órbita que no repite valores | sólo obliga a que el pronóstico pase alguna vez de casi 3 (cuenta a mano: los k+1 primeros valores son distintos y ninguno pasa de (n + k/3) por el mayor pronóstico) |
| Muro A y Ocelotas | dan crías, no choque: las crías pueden ser fugitivos sin más |
| La cadena de Gao | habla de casi todos los números, y el fugitivo vive en el conjunto de densidad cero |
| El resto módulo 3 | lo decide el baile (tras cada subida, el valor deja resto 2) y no vuelve a influir en él |

**Terminaciones de la casa.** `collatz_iff_sin_intrusos` y
`muroB_de_sin_fugas` (sección «Techo»), y `tamano_antes_del_cruce`, que
vale para cualquier número antes de su primer cruce (sección «Radier»).

**Retroalimentación.** Va en las dos direcciones. Un rasgo del retrato,
«crece hacia el infinito», dio la terminación `muroB_de_sin_fugas`. Dos
piezas de la casa, el muro A y el tramo de Ocelotas, dieron rasgos nuevos
del fugitivo: sus crías.

[cotejo_tablero.py](cotejo_tablero.py) lo contrasta sin Lean: los 1608
bailes periódicos de largo ≤ 14 que nunca cruzan son de números
negativos; el fantasma de pendiente 1/√2 no cruza en 4000 pasos y tiene
1621 unos y 1579 ceros en sus primeras 3200 cifras; con 5n+1, el 13 y el
17 cruzan a los 7 pasos sin bajar nunca de sí mismos, y el 7 no cruza en
100 000 pasos (su pronóstico nunca baja de 2^0,322); la cota de tamaño se
cumple en 146 559 casos con n < 2^15 y se alcanza justo en 24 576; y por
debajo de 2^k aguantan k pasos sin cruzar unos 2^87,97, 2^181,68 y
2^275,88 números para k = 100, 200 y 300, bajo el tope de Lean.

**Resultado de la ronda.** No hay choque. El choque tiene que usar a la
vez que el fugitivo es un número común (prueba del fantasma) y algo
propio del 3 (prueba del vecino). Hay rasgos de cada tipo, pero ninguno
que use las dos cosas juntas: ése es el puente que falta, y es justo lo
que nadie sabe hacer. La ronda se cierra con su presupuesto; las
posibles segundas rondas están en «Ruta a seguir».

## Comprobación

[comprobar_casa.py](comprobar_casa.py) verificó por huellas los 670
módulos de Ocelotas importados (20 de la base y 650 del cierre de 24).
El 06-10 compiló los cuatro archivos en 41, 40, 34 y 31 segundos y
auditó sus 54 consultas (17 del plano, 2 del enganche con Ocelotas, 17
del retrato y 18 del tablero): sólo `propext`, `Classical.choice` y
`Quot.sound`, sin `sorryAx` ni avisos
([evidencia](evidencia_casa.json), [salida](evidencia_casa.txt)).
Lean 4.32.2. Para reproducirlo, desde la raíz:

```text
python -B -X utf8 depuracion/casa20261004/comprobar_casa.py --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_veinticuatro_paralelo_20261004 --salida depuracion/casa20261004/evidencia_casa.json
```

Las cachés sólo se leen. Si se borran, hay que reconstruirlas antes con
los comprobadores de Ocelotas.

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

1. **El plano en Lean**: hecho el 04-10 (sección «El plano en Lean»).
2. **El retrato del fugitivo**: hecho el 06-10 (sección «El retrato del
   fugitivo en Lean»). Los cuatro rasgos previstos están en Lean: órbita
   no acotada, patrón nunca periódico, al menos 63 subidas de cada 100
   pasos y densidad cero. El mismo día el tablero sumó tres más: puntos
   sin retorno, tamaño pegado al pronóstico y cohete o planeador.
3. **Buscar choques** (abierto; primera ronda hecha el 06-10, sección
   «Paso 3: el tablero del choque», sin choque). Dos rasgos del fugitivo
   que se contradigan, o uno que choque con algo ya demostrado. Si
   aparece, el muro B queda en pie. Nadie lo ha logrado; ésta es la
   apuesta. El choque tiene que usar que el fugitivo es un número común y
   no un fantasma 2-ádico, y no debe valer en la casa del vecino (5n+1),
   donde el muro A se cae de verdad (el 13) y todo indica que hay
   fugitivos (el 7). Segundas rondas posibles: cerrar la pinza (que un
   fugitivo obligue a que haya muchos), estudiar por separado las dos
   especies, cohete y planeador, o pasar al paso 4.
4. **El dominó del muro A** (abierto). Una reducción que convierta una
   grieta con R+1 picos en otra con menos, o una desigualdad que valga
   para todo R a la vez. Completar el muro A incluye demostrar que no hay
   circuitos.
5. **Los muros completos.** A completo incluye «no hay circuitos», y B
   completo es «no hay fugas puras». Son los dos problemas abiertos del
   centro de Collatz.

Cada pieza se trabaja con presupuesto acotado, como en el
[plan del 28-09](../transversal20260927/PLAN_SESIONES_20260928.md): si no
avanza, se escribe por qué y se cierra.

**Duda abierta del usuario, 04-10:** «¿para terminar de construir los
muros necesitamos la racha 25, 26 y así sucesivamente? Eso nos dejaría
exactamente al principio del problema». No: ese camino no termina
nunca, y la ruta B existe justamente para evitarlo. El 06-10 añadió la
duda de los 360°: juntar afirmaciones sobre números termina apuntando a
todos los números. Es cierto: por eso el plano cambia el blanco y apunta
a los dos intrusos, el circuito y el fugitivo, y no a los números.
