# Plano de la casa: qué le falta a la prueba de que todo número llega a 1

**Ruta vigente, 10-10-2026, continuación:**
[Colisiones](../perdices20261007/COLISIONES.md) excluye al planeador
intermitente. Toda fuga pura tendría `P_k -> infinito` y `R_k -> ξ`
real finito. Prueba en Lean, con antecedente Garcia–Tal (1999).
La [cola](../perdices20261007/COLA.md) tiene piso y dinámica en Lean,
con límite relativo cero. [Mínimos futuros](../perdices20261007/MINIMOS.md)
formaliza la cota cuantitativa y los reinicios de fuga pura sin MuroA:
`Collatz <-> MuroB y ausencia de circuitos no triviales`. Ambas
condiciones siguen abiertas. [Repeticiones](../perdices20261007/REPETICIONES.md)
acota la repetición de un bloque desde una misma semilla y calcula
el defecto que aparece al cambiarlo.
[Cancelaciones](../perdices20261007/CANCELACIONES.md) formaliza la
resonancia y los reinicios del ensayo `1`/`110`. Su persistencia
infinita sigue abierta; esta clase no equivale a todo MuroB.
Siguiente: controlar historias no periódicas de una misma semilla.
Las decisiones anteriores se conservan
abajo como antecedentes; la búsqueda de una cota de duración ya
no es necesaria para excluir al planeador.

**Antecedentes del 10-10-2026:** [balance y programa](RUTA_20261010.md),
con [primer ensayo ejecutado: Jinetas](../jinetas20261010/LEEME.md).
El traslado quedó auditado; el intercambio `01/10` crea y destruye
paradojas por el acarreo modular. Se descarta ordenar sólo por el
aditivo. El relleno de ceros no añade una congruencia sobre la semilla
original. El [ensayo por prefijos](../jinetas20261010/PREFIJOS.md)
conserva un mismo n, pero en el primer cruce vuelve a CST y no fuerza
terminar. La [auditoría de rachas](../jinetas20261010/RACHAS.md)
precisa la compensación que falta al reiniciar desde un valor mayor;
las cotas del factor 3 no la garantizan. El [paso 3 de Perdices](../perdices20261007/CRUCE.md)
ya combina sexta raíz y casi fugitivos: exponente 4/25 para regresos,
con constantes y cadena Lean auditadas. El [estudio de separaciones](../perdices20261007/SEPARACION.md)
acota la duración por rachas: un planeador necesitaría excursiones con
rachas no acotadas. El [cierre orbital en Lean](../perdices20261007/EXCURSIONES.md)
ya incluye extracción y enumeración de regresos; la exclusión universal
sigue abierta. El [ritmo de rachas](../perdices20261007/RITMO.md) reduce
la base de 2 a 8/5 y exige superar una escala logarítmica en toda cola.
El [balance par](../perdices20261007/BALANCE.md) ya está enlazado con la órbita:
excluye una cola de excursiones interiores 110, aunque tengan rachas no
acotadas. El [cierre por excepciones](../perdices20261007/EXCEPCIONES.md)
ya exige cantidades no acotadas de bloques distintos de 110 en toda cola.
El [aporte ponderado](../perdices20261007/APORTE.md) ya está calculado:
muchas excepciones pueden aportar poco y la cantidad que neutraliza 110
no es monótona localmente. El [enlace con la semilla](../perdices20261007/SEMILLA.md)
prueba que infinitos regresos exigirían duraciones mayores que cualquier
múltiplo fijo de `(x+1)^5`, para el valor de entrada x. El aporte local
no decide la congruencia de la prolongación. Siguiente: buscar una cota
de duración basada en esa entrada; todavía no está demostrada.
La [novena raíz](../perdices20261007/NOVENA.md) usa que sólo una
entrada impar puede ser divisible por 3. Mejora los regresos a
`O(K^(8/75))` y exige superar toda cota `H(x+1)^8` en una cola
con infinitos regresos. Esa es la cota superior que ahora bastaría
demostrar para excluir al planeador intermitente.

04-10-2026. El usuario eligió la ruta B, la reducción al absurdo: suponer
un número que no baja y anotar todo lo que tendría que cumplir. Pidió
verla como una casa, con un inventario de las piezas que debe tener
cualquier prueba de Collatz: cuáles ya están y cuáles faltan.

Mapa: `T(n)=n/2` si n es par y `(3n+1)/2` si es impar. El **pronóstico**
de n a los j pasos es `3^S_j(n)/2^j`, donde S_j(n) cuenta las subidas
(pasos impares). El **primer cruce** τ(n) es el primer j en que el
pronóstico baja de 1. El **primer descenso** σ(n) es el primer j con
`T^j(n)<n`. Siempre τ(n) ≤ σ(n).

## La casa en una página

Inventario matemático al 07-10; decisión de trabajo actualizada el 10-10.
Los resultados formales conservan las hipótesis indicadas en cada ficha.

- **El techo y los muros.** Collatz equivale a dos muros: A, «si el
  pronóstico dice abajo, el número termina bajando», y B, «el pronóstico
  siempre llega a decir abajo». Los dos están en pie para casi todo
  número, y ninguno para todos.
- **Los dos intrusos.** Toda falla de Collatz pasa por una **fuga pura**
  (el intruso del muro B, un avión que nunca aterriza) o por una
  **grieta** (el del muro A, un paracaidista cuyo altímetro dice «suelo»
  mientras sigue en el aire). De los dos hay retrato: el fugitivo tiene
  nueve rasgos y la grieta los suyos, y los dos son raros. El noveno
  (07-10, noche) dice que su techo sube rápido: antes del tiempo K, su
  pronóstico alcanza `K^(5/6)/n`.
- **El primer choque.** No hay planeador fuerte: un fugitivo no puede
  volar siempre bajo, porque cada aterrizaje necesitaría una pista nueva
  en un país casi sin pistas (la estela). Quedan dos especies, el cohete
  y el planeador intermitente; los conteos disponibles no los excluyen.
- **Las ventanas.** Están en Lean los teoremas clásicos de «casi todos»:
  los A, B y C de Terras, el descenso y el teorema E (con constante
  escrita), la rareza x^0,95 de Lagarias y el teorema de Korec completo.
  Dejan ver cómo se porta casi todo número, pero el fugitivo y la grieta
  viven en el conjunto de densidad cero.
- **Lo que falta.** Los dos muros completos: «no hay circuitos» (el
  dominó del muro A) y «no hay fugas puras» (el cohete y el planeador
  intermitente del muro B). Son los dos problemas abiertos del centro de
  Collatz; nadie sabe hacerlos.

- **Balance y siguiente paso.** [Jinetas](../jinetas20261010/LEEME.md)
  deja las fórmulas exactas, su certificación parcial y los testigos
  contra la monotonía del margen. El segundo ensayo obtiene un intervalo
  de semillas compatible con todos los prefijos, pero sus cotas no dan
  la disminución estricta necesaria. En el primer cruce vuelve a CST.
  El tercer ensayo prueba el puente cuantitativo del corte y el límite
  de la cota de suelo; no entrega una inducción por rachas.
  No se ha cerrado ningún muro: A también incluye grietas divergentes;
  CST completo no probaría la existencia del cruce del muro B.

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
| Ninguna órbita vuela en franja: para todo número y todo c, el pronóstico sale alguna vez de la franja entre 1/3^c y 3^c | ✔ Lean | `ninguna_orbita_en_franja` |
| Si el pronóstico cruza por primera vez en el paso k y k·2^k ≤ 3n, el número baja en ese mismo paso (Terras) | ✔ Lean | `desciende_si_grande`, `desciende_de_cruce` |
| Hacia atrás: si u llega a v sin que su pronóstico baje de 1/3^c, entonces u ≤ 3^c·v | ✔ Lean | `atras_acotado` |

### Muro A: el pronóstico no se equivoca

| Tramo | Estado | Dónde |
|---|---|---|
| Casi todo número (densidad 1) baja de sí mismo: por debajo de 2^(104m), los que nunca bajan son a lo sumo (100m+2)·2^(100m) | ✔ Lean | `casi_todo_desciende`, `cuenta_sin_descenso`; Terras (1976), Everett (1977) |
| Casi todo número cumple CST: baja justo en su primer cruce | ✔ Lean | `casi_todo_cst`; Terras (1976) |
| Para cada k, los que bajan en a lo sumo k pasos tienen densidad exacta F(k) = (restos módulo 2^k que cruzan en k pasos)/2^k, y F(k) → 1 | ✔ Lean | `densidad_terras`, `terras_tiende_a_uno`: el teorema A de Terras (1976), completo; también los teoremas B y C (`teorema_B`, `teorema_C`) |
| Con hasta 24 picos antes del cruce acierta exacto (CST) | ✔ Lean, bajo LMN | [24 rachas](../cst20260930/VEINTICUATRO_LEAN.md); en el plano, `muroA_hasta_24` |
| El muro A solo, aunque sea sin el B, ya excluye los circuitos | ✔ Lean | `muroA_sin_circuitos` |
| El menor valor de todo circuito es una grieta | ✔ Lean | `circuito_tiene_grieta` |
| Una grieta cruza tarde para su tamaño: 3n < k·2^k, con k su primer cruce | ✔ Lean | `grieta_tarde` |
| Con primer cruce k ≥ 2^16, sólo el menor número de su clase módulo 2^k podría ser grieta (teorema E de Lagarias, con la constante escrita) | ✔ Lean, bajo LMN | `teorema_E_lmn`; con la cota de Rhin, desde k = 98: `teorema_E_rhin` |
| En la casa del vecino (5n+1) el muro A se cae: el 13 cruza y nunca baja de sí mismo | ✔ Lean | `vecino_grieta`: la prueba del muro A tiene que usar algo propio del 3 |
| Con hasta 77 picos, sumando el cálculo de Rozier–Terracol | ✔ Lean, dos hipótesis externas | [77 rachas](../cst20260930/SETENTA_Y_SIETE_LEAN.md) |
| Para cada cantidad fija de picos, los fallos posibles caben en una región finita explícita | ✔ Lean, bajo LMN | [Cota general](../cst20260930/COTA_GENERAL.md), [cola](../cst20260930/COLA_PARAMETRICA.md) |
| CST comprobada para todo n ≤ 2,8·10^19 | ✔ externo | Rozier–Terracol (2026), corolario 5.4 |
| Ningún circuito tiene 91 picos o menos | ✔ externo | Hercher (2023) |
| Ningún circuito tiene 24 picos o menos: desde su menor valor, una vuelta tiene al menos 25 rachas | ✔ Lean, bajo LMN | `circuito_exige_25` |
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
| Con el exponente de Lagarias: por debajo de x = 2^(10000m), a lo sumo 2·x^0,95 números sin primer cruce | ✔ Lean | `rareza_lagarias`; Lagarias (1985), teorema F |
| En su órbita hay puntos sin retorno, tan lejos como se quiera: valores de los que nunca vuelve a bajar | ✔ Lean | `rasgo_minimos` |
| Su tamaño va pegado a su pronóstico, en todo momento | ✔ Lean | `rasgo_tamano` |
| Es cohete (su pronóstico crece sin límite y su órbita está llena de fugas puras) o planeador (vuelve una y otra vez a tamaños que crecen apenas como el tiempo) | ✔ Lean | `rasgo_cohete_o_planeador` |
| Su pronóstico no tiene techo: pasa cualquier nivel, tan tarde como se quiera; no hay planeador fuerte, que vuele siempre bajo; en los primeros k = 2^(100m) pasos pasa de k^0,0158 | ✔ Lean | `sin_planeador_fuerte`, `pronostico_sin_techo`, `techo_crece` |
| Casi nunca está bajo: para cada nivel, los momentos con el pronóstico por debajo tienen densidad cero; en los primeros 2^(100m) pasos el pronóstico pasa de 3^m salvo en una fracción 3·(3/8)^m | ✔ Lean | `tiempos_bajos_raros`, `tiempos_bajos_potencia` |
| Es cohete o planeador intermitente, que vuelve bajo cada vez más de tarde en tarde | ✔ Lean | `cohete_o_planeador_intermitente` |
| Con el muro A nunca anda solo: sus puntos sin retorno son fugas puras | ✔ Lean | `crias_con_muroA`, `fugas_sin_tope` |
| Sin el muro A, los puntos sin retorno de toda órbita que crece sin límite son fugas puras o grietas, y son raros: por debajo de 2^(104m), a lo sumo (100m+2)·2^(100m) | ✔ Lean | `crias_sin_muroA`, `sin_retorno_raros` |
| Toda órbita que crece sin límite, pura o no, termina subiendo en al menos 63 de cada 100 pasos, salvo una constante | ✔ Lean | `fuga_sube`; Lagarias (1985), (2.31) |
| Con el tramo de Ocelotas, sus puntos sin retorno son fugas puras o cruzan con al menos 25 picos | ✔ Lean, bajo LMN | `crias_con_ocelotas` |
| Si ninguna órbita crece sin límite, el muro B está en pie | ✔ Lean | `muroB_de_sin_fugas` |
| Todo número, sin excepción | ✘ | es «no hay fugas puras», abierto |

### Ventanas: dejan entrar luz, pero no sostienen la casa

- Todo número hasta 2^71 llega a 1 (verificación externa, Barina 2025).
- Casi toda órbita baja por debajo de n^θ en a lo sumo log₂ n pasos,
  para todo θ mayor que log 3/log 4 ≈ 0,7925: el teorema de Korec (1994),
  completo en Lean (`korec_real`), sin hipótesis externas; para θ = 0,8,
  también con las constantes escritas (`casi_todo_baja_08`). Sección
  «Una ventana: Korec».
- Casi todo número cumple CST: baja justo en su primer cruce
  (`casi_todo_cst`, en Lean; Terras, 1976). Misma sección.
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

## Paso 3, segunda ronda: el planeador

07-10-2026: el pendiente (a), dentro de la meta que el usuario dio a la
sesión («avanza con la investigación»). [CasaPlaneador.lean](CasaPlaneador.lean),
sin hipótesis externas.

**El primer choque: no hay planeador fuerte.** Un planeador *fuerte*
sería un fugitivo cuyo pronóstico se queda para siempre por debajo de un
mismo nivel. No existe (`sin_planeador_fuerte`): el pronóstico de todo
fugitivo pasa cualquier nivel, y lo vuelve a pasar tan tarde como se
quiera (`pronostico_sin_techo`).

La prueba es una **estela**. Cada momento en que el fugitivo vuela bajo,
con pronóstico a lo sumo 3^c, deja atrás un número que:

- es chico: en el paso j vale a lo sumo 3^c·(n + j) (`chico_si_bajo`, del
  rasgo 6);
- es **casi fugitivo** de nivel 3^c: desde allí el pronóstico puede bajar,
  pero nunca más que el factor 3^c (`casi_fuga_de_bajo`);
- es distinto de todos los anteriores, porque la órbita nunca repite un
  valor (rasgo 2).

Si volara siempre bajo, en k pasos dejaría k casi fugitivos distintos,
todos menores que 3^c·(n + k). Pero los casi fugitivos son raros, como los
fugitivos, con un factor 2^c más (`cuenta_casi_fugas`, por la misma cuenta
de patrones del rasgo 4): por debajo de x hay a lo sumo unos 2^c·x^0,96.
Para k grande no alcanzan. Es un avión que tendría que aterrizar cada minuto en
una pista nueva, en un país casi sin pistas. Chocan tres piezas del
retrato: el rasgo 2, el 6 y la rareza del rasgo 4 llevada a los casi
fugitivos.

**Rasgo 8: casi nunca está bajo.** La misma estela cuenta los momentos
bajos de cualquier fugitivo (`tiempos_bajos`). Para cada nivel tienen
densidad cero (`tiempos_bajos_raros`). En cifras: para un fugitivo menor
que 2^(100m), en sus primeros 2^(100m) pasos el pronóstico pasa de 3^m
salvo en una fracción 3·(3/8)^m de los momentos (`tiempos_bajos_potencia`,
útil desde m = 2). Como 3^m es k^0,0158 con k = 2^(100m), el pronóstico
pasa casi todo el tiempo por encima de una potencia pequeña del tiempo, y
en esos k pasos llega a pasarla (`techo_crece`): el techo que no tiene se
aleja al menos a ese ritmo.

**Las dos especies que quedan** (`cohete_o_planeador_intermitente`):

- el **cohete**: su pronóstico termina pasando cualquier nivel y ya no
  vuelve a bajar de él;
- el **planeador intermitente**: vuelve por debajo de un nivel una y otra
  vez, pero cada vez más de tarde en tarde, y entre medio pasa cualquier
  techo.

**Ninguna órbita vuela en franja.** La estela no necesita un fugitivo
puro: basta que la órbita crezca sin límite, porque entonces tampoco
repite valores (`fuga_inyectiva`), y el tamaño sigue pegado al pronóstico
mientras éste no baje de 1/3^c (`tamano_en_franja`). Con eso, para todo
número y todo nivel, el pronóstico sale alguna vez de la franja entre
1/3^c y 3^c (`ninguna_orbita_en_franja`). Si la órbita está acotada, cae
en un circuito y el pronóstico se hunde hacia cero (`acotada_baja`); si
crece sin límite, la estela lo saca por arriba o por abajo
(`fuga_sale_de_franja`). Es una terminación del plano clásico: ninguna
fuga, pura o no, vuela siempre a media altura. En particular, una grieta
del muro A cuya órbita escape tampoco vuela en franja.

**El tablero, con el rasgo 8.**

| Rasgo | Lean | ¿Fantasma? | ¿Vecino? | Tipo |
|---|---|---|---|---|
| 8. Su pronóstico no tiene techo y casi nunca está bajo | `pronostico_sin_techo`, `tiempos_bajos_raros` | no lo cumple: hay un fantasma que vuela siempre entre 1 y 3 | la prueba no pasa: allí los casi fugitivos abundan | de carne y hueso y del 3 |

Es el primer rasgo de los dos tipos a la vez, el puente que la primera
ronda echó en falta, aunque por ahora sólo alcanza a la subespecie del
planeador fuerte.

- **El fantasma que vuela bajo** sube en el paso j justo cuando hace falta
  para que 3^subidas no baje de 2^j. Su pronóstico queda siempre entre 1 y
  3, su baile nunca es periódico y su órbita no repite valores; pero es un
  número con infinitas cifras binarias, sin tamaño, y su estela no se puede
  contar. En Lean, tramo por tramo: para cada L hay un número menor que 2^L
  cuyos primeros L pasos son los de un planeador fuerte
  (`fantasma_planeador`). Por eso el choque necesita todos los pasos y el
  tamaño del número: mirar una cantidad fija de pasos nunca basta.
- **En la casa del vecino** (5n+1), entre los números menores que 2^16, el
  18 % no baja de 1 en 80 pasos y el 51 % no baja de 1/5: los casi fugitivos no son raros y la
  cuenta no da nada. Si allí hay fugitivos de pronóstico acotado, no se
  sabe.

**Lo que ya se sabía.** El pariente conocido más cercano es de Lagarias
(1985, §2, teorema F y ecuación 2.32, leídos el 07-10 en la versión web de
su artículo): los números con tiempo de parada infinito son a lo sumo
c₁·x^(1−η) por debajo de x, con η ≈ 0,05004, y por eso los puntos sin
retorno de una órbita que escapa también lo son: «los elementos de una
trayectoria divergente no pueden ir al infinito demasiado despacio». Eso
no basta contra el planeador fuerte: a una órbita que crece como el
tiempo le pueden quedar muy pocos puntos sin retorno, del orden del
logaritmo del tiempo. La estela cuenta, en cambio, todos los momentos de
pronóstico bajo, gracias a los casi fugitivos. Es un refinamiento modesto
de ese argumento clásico; no se buscó más en la literatura y no se
pretende prioridad. La rareza en Lean de ese día (x^0,96) era algo más
débil que la de Lagarias (x^0,95); más tarde, el mismo 07-10,
`rareza_lagarias` la alcanzó para las fugas puras (sección «Una ventana:
Korec»).

**Lo que no funcionó: la vuelta de circuito.** La idea anotada en (a) era
ver el tramo entre dos regresos como una vuelta de circuito y usar LMN.
No da: que el pronóstico regrese a un nivel no obliga a que el tamaño
regrese a un valor (la órbita crece hacia el infinito), así que no aparece
ninguna casi igualdad entre 3^s y 2^p que LMN pueda prohibir. Funcionó la
otra herramienta del 3, la cuenta de patrones, que la primera ronda sólo
había usado para contar fugitivos y no para seguir a uno.

**Lo que sigue abierto.** El cohete y el planeador intermitente esquivan
la estela: pasan casi todo el tiempo arriba, donde los números son enormes
y la estela se dispersa. La cuenta de patrones sólo asegura que por
debajo de x hay a lo sumo unos x^0,96 casi fugitivos de cada nivel (en
Lean), y aun afinada no baja de x^0,95, el límite de contar bailes; por
eso el método no da más que una potencia pequeña del tiempo. Para acorralar
al cohete hace falta otra cosa: la cuenta de patrones no distingue a un
número común de un fantasma que sube sin techo, y fantasmas así hay de
sobra (el −1 es uno). Es el muro de siempre de los argumentos de conteo:
dan «casi todos», no «todos».

**Los pendientes (b) y (c), con la herramienta nueva.** Revisados el 07-10,
con su presupuesto.

- **(b) La pinza** cerró para el planeador fuerte: allí la propia estela da
  el brazo «si hay uno, hay muchos». Para el fugitivo general no cierra.
  Hacia atrás, un número que llega a un fugitivo v sin que su pronóstico
  baje de 1/3^c es a lo sumo 3^c·v (`atras_acotado`), así que el árbol de v
  aporta sólo un puñado de casi fugitivos de cada nivel. Con todas las
  fugas, la pinza pide que las órbitas que escapan sean menos de x^0,84
  por debajo de x, y eso incluye que tengan densidad cero: no conocemos
  prueba de eso (Lagarias, 2021, §8, da por abierta incluso su existencia),
  y la densidad de Terras no alcanza, porque una órbita puede bajar primero
  y escapar después. Se cierra sin más avance.
- **(c) El dominó del muro A** no se mueve con la estela. Una grieta es un
  circuito o una órbita que escapa. Contra los circuitos la estela no sirve,
  porque un circuito repite valores y su pronóstico se hunde hacia cero; de
  las que escapan sólo dice que su pronóstico tampoco vuela en franja. El
  dominó sigue siendo el problema de los m-ciclos; se cierra con su
  presupuesto.

[cotejo_planeador.py](cotejo_planeador.py) lo contrasta sin Lean: los
patrones de largo 100m con 2^(100m) ≤ 3^c·3^|A| quedan bajo el tope
2^c·2^(96m) para m ≤ 6 y c ≤ 30; entre 0 y 2^L − 1 hay justo C(L, s)
números con s subidas, para L ≤ 18; con 5n+1, los patrones de largo 100
que no cruzan al final son unos 2^99,85, más que el tope 2^96; el
fantasma vuela 2000 pasos entre 1 y 3, con 803 unos y 797 ceros en sus
primeras 1600 cifras y sin periodo ≤ 300, y sus recortes a L ≤ 400 cifras
son números menores que 2^L que siguen su baile durante L pasos, como dice
`fantasma_planeador`; y en los récords de pasos sin
cruzar por debajo de 2^22 (el mayor, 1 126 015, aguanta 224 pasos) las
cotas de `chico_si_bajo` y `casi_fuga_de_bajo` se cumplen en cada momento
bajo, y el pronóstico pasa por debajo de 3 sólo entre el 3 y el 9 % del
camino.

## El retrato de la grieta

07-10-2026, dentro de la meta que el usuario dio a la sesión («avanza
hasta nuevo aviso»). [CasaGrieta.lean](CasaGrieta.lean).

La casa tenía el retrato del intruso del muro B, el fugitivo, pero no el
del muro A. Ese intruso es la **grieta**: un número cuyo pronóstico baja
de 1 pero que nunca baja de sí mismo. Es como un paracaidista cuyo
altímetro marca «ya llegaste al suelo» mientras él sigue en el aire. El
muro A dice exactamente que no hay grietas (`muroA_iff_sin_grietas`).
Aquí se la supone y se anota lo que tendría que cumplir, como con el
fugitivo.

**El viento sólo levanta a los livianos.** El pronóstico mira sólo las
subidas y las bajadas. El tamaño real lleva además el +1 de cada subida,
que empuja hacia arriba como el viento. Hasta el primer cruce, ese
empuje suma a lo sumo S/3 veces el pronóstico (`tamano_antes_del_cruce`).
Por eso, si el pronóstico cruza por primera vez en el paso k y el número
es grande comparado con k·2^k, el viento no alcanza y el número baja
justo en ese paso (`desciende_si_grande`; la forma exacta,
`desciende_de_cruce`, pide S·3^S < 3n). Es el teorema C(b) de Terras
(1976), con la cota escrita. Una grieta, en cambio, tiene que ser liviana
para su pronóstico (**rasgo G1**, `grieta_tarde`): cruza en un paso k ≥ 2
con 3n < k·2^k.

**Casi todo número baja de sí mismo** (`casi_todo_desciende`; Terras,
1976, y Everett, 1977). Un número que nunca baja, o aguanta 100m pasos
sin cruzar, y ésos son pocos por la cuenta de patrones del retrato, o
cruza antes y entonces es chico, por G1. En cifras
(`cuenta_sin_descenso`): por debajo de 2^(104m), los que nunca bajan son
a lo sumo (100m+2)·2^(100m). Con eso el muro A gana su tramo de «casi
todo número», como el muro B tenía el suyo desde el 06-10. Lagarias
(1985, teorema F) da una cota mejor, a lo sumo c₁·x^0,95 por debajo de x;
la de Lean se acerca a x^0,962, por un factor logarítmico, y no usa LMN.

**Con LMN, sólo el primero de la fila** (`teorema_E_lmn`). Los números que
bailan igual en sus primeros k pasos forman una fila: los de una misma
clase módulo 2^k. LMN impide que 3^S quede demasiado pegado a 2^k, así
que el viento tendría que ser todavía más fuerte. Bajo LMN, una grieta
cumple 3n ≤ k·2^(19(log₂ k + 33)²) (`grieta_lmn`), y si su primer cruce es
k ≥ 2^16, es menor que 2^k: el primero de su fila. Es el teorema E de
Lagarias (1985), que deja la constante como «efectivamente calculable»;
aquí queda escrita. Con la cota de Rhin, la de Ocelotas, basta k ≥ 98, y
la grieta cumple 3n ≤ k^15 (`teorema_E_rhin`, `grieta_rhin`). El umbral
de validez de Rhin sigue sin cotejar con la fuente
([RHIN_LEAN](../cst20260930/RHIN_LEAN.md)); por eso la versión principal
es la de LMN.

**Los dos intrusos se reducen a dos clases de números.** El menor valor
de todo circuito es una grieta (`circuito_tiene_grieta`). Y, sin el muro
A, cada punto sin retorno de una órbita que crece sin límite es una fuga
pura o una grieta (`crias_sin_muroA`). Esos puntos son raros: una órbita
pasa por a lo sumo (100m+2)·2^(100m) de ellos por debajo de 2^(104m)
(`sin_retorno_raros`, la (2.32) de Lagarias en cifras). Toda falla de
Collatz pasa, pues, por fugas puras o por grietas, y de las dos clases
hay prueba en Lean de que son raras. Pero raras no es ninguna.

Como el menor valor de un circuito es una grieta, el tramo de Ocelotas
(toda grieta necesita al menos 25 picos antes de su primer cruce) dice,
bajo LMN, que ningún circuito tiene 24 picos o menos en una vuelta
(`circuito_exige_25`). Hercher (2023) llegó a 91, fuera de Lean; esto es
el mismo tramo de Ocelotas, ahora leído como cota para los circuitos.

**La grieta que escapa sube como el fugitivo.** Toda órbita que crece sin
límite, pura o no, termina subiendo en al menos 63 de cada 100 pasos,
salvo una constante (`fuga_sube`, la (2.31) de Lagarias). Cuando los
valores ya pasan de 1000, el +1 de cada subida casi no pesa
(`crecimiento_alto`), y 3001^63 ≤ 2^100·1000^63 hace el resto. Vale para
una grieta cuya órbita escapa, que el retrato del fugitivo no cubría.

**El tablero, con la grieta.**

| Rasgo | Lean | ¿Fantasma? | ¿Vecino? | Tipo |
|---|---|---|---|---|
| G1. Cruza tarde para su tamaño | `grieta_tarde` | no tiene sentido: habla del tamaño | vale con 5: el 13 y el 17 son grietas y lo cumplen | de carne y hueso |
| G2. Con LMN, es la primera de su fila | `teorema_E_lmn` | no tiene sentido | no la distingue: con una cota de Baker para 2 y 5 valdría igual (no se calculó); el 13 cruza en el paso 7, demasiado pronto para que aplique | de carne y hueso |
| El menor valor de un circuito es una grieta | `circuito_tiene_grieta` | no lo cumplen los circuitos negativos: en el del −5 el pronóstico nunca baja de 1 | vale: el 13 y el 17 | de carne y hueso |
| Ningún circuito tiene 24 picos o menos | `circuito_exige_25` | no lo cumplen: los circuitos negativos tienen 1 o 2 rachas por vuelta | no vale: el circuito del 13 tiene 1 racha | de carne y hueso y del 3, pero sólo por tramos |

La rareza, «casi todo número baja», es del 3, como la del rasgo 4: en la
casa del vecino no vale. La fila de los 24 picos usa las dos cosas, como
el rasgo 8, pero hereda el defecto de Ocelotas: vale para una cantidad
fija de picos, no para todas a la vez.

**Lo que ya se sabía.** Todo esto es clásico; se leyó el 07-10 en la
versión web de Lagarias (1985, §2). El descenso de los números grandes es
el teorema C(b), de Terras. «Casi todo número baja» es el teorema A, de
Terras (1976) y de Everett (1977). «Sólo el primero de la fila» es el
teorema E, que usa la teoría de Baker. La rareza de los puntos sin
retorno es la (2.32). Lo nuevo es sólo la forma: en Lean, sin `sorry`,
con las constantes escritas (2^16 bajo LMN, 98 bajo Rhin). No se buscó si
esas constantes ya están publicadas; no se pretende prioridad.

**Lo que no da.** No hay choque. Como el del fugitivo, el retrato de la
grieta dice «raras», no «ninguna». Para los circuitos, G1 da una cota
mucho más débil que las conocidas (Hercher, 2023: ningún circuito tiene
91 picos o menos), y no mueve el dominó. Lo que sí deja es el mapa de las
dos clases de intrusos, fugas puras (muro B) y grietas (muro A), cada
una con su rareza demostrada en Lean.

[cotejo_grieta.py](cotejo_grieta.py) lo contrasta sin Lean. Para
2 ≤ n < 2^20, el primer descenso llega justo en el primer cruce, y la
condición de `desciende_de_cruce` cubre al 96,7 % (la de
`desciende_si_grande`, al 96,4 %). Los 34 381 restantes tienen un cruce
largo para su tamaño (hasta 183 pasos, en n = 1 027 431) y también bajan
en su cruce, aunque eso Lean no lo prueba. k^15 < 3·2^k vale desde
k = 98 y falla en 97; la desigualdad de LMN vale desde k = 43 790, y Lean
usa 2^16 = 65 536. En la casa del vecino, el 13 y el 17 son grietas de
verdad: cruzan a los 7 pasos, cumplen 5n ≤ S·5^S y son el menor valor de
su circuito. Y entre los n < 2^14, el 17,5 % pasa de 2^200 sin bajar
nunca. Para toda fuga: 3001^63 ≤ 2^100·1000^63, con margen de 2^0,117, y
la cota de `crecimiento_alto` se cumple en 3 505 289 tramos de órbitas
reales. Los circuitos que sí existen (el 13 y el 17 en 5n+1; el −1, el
−5 y el −17 con negativos) tienen 1 o 2 rachas por vuelta.

## Una ventana: Korec

07-10-2026, misma meta. [CasaVentana.lean](CasaVentana.lean), sin
hipótesis externas.

Las ventanas no sostienen la casa, pero dejan ver cómo se porta casi
todo número. Terras probó que casi todo número baja alguna vez de sí
mismo. Korec (1994) probó mucho más: para todo exponente mayor que
log 3/log 4 ≈ 0,7925, casi todo número n baja alguna vez por debajo de
n elevado a ese exponente. Aquí está en Lean el caso 0,8: **casi toda
órbita baja por debajo de n^0,8 en a lo sumo log₂ n pasos**
(`casi_todo_baja_08`).

**Por qué 0,7925.** Un número típico sube en la mitad de los pasos y baja
en la otra mitad. En log₂ n pasos su pronóstico queda en
(3/4)^(log₂ n / 2) = n^(−0,2075), y el número, en n^0,7925. Para bajar más
hace falta subir menos que la mitad de las veces, y eso es cada vez más
raro. Para 0,8 basta poco: en bloques de 1000 pasos, menos de 503 subidas
(`baja_korec`). Los patrones con 503 subidas o más son menos que 2^1000
(`margen_pesos`), pero por un margen finísimo: 2^0,026 por bloque.

**Cómo se cuenta.** Es la misma cuenta de patrones del retrato del
fugitivo, con pesos 503 y 497 en vez de 2 y 1 (`pocos_patrones_pesos`),
para contar «más de la mitad de subidas». El viento, el +1 de cada
subida, se acota para cualquier camino (`tamano_general`). Las
desigualdades con números de miles de cifras se comprueban en el núcleo
de Lean (`decide +kernel`), y en la parte con números reales esas
constantes quedan como números opacos (`korec_opaco`).

**Lo que dicen los números de verdad.** [cotejo_ventana.py](cotejo_ventana.py)
lo contrasta sin Lean. Además de los márgenes y de la cuenta exacta de
patrones (2^998,81 de 2^1000), mide cuántos bajan de verdad. Hasta 2^19,
entre el 60 y el 63 % de los números de cada tramo baja por debajo de
n^0,8 en a lo sumo log₂ n pasos; con 0,75, por debajo del umbral, entre
el 48 y el 55 %, en lenta caída. El «casi todos» de Korec es asintótico:
con un margen tan fino llega para números astronómicos, y el teorema no
dice desde cuándo. La cota de `tamano_general` se cumple en 1 200 000
casos.

**Lo que ya se sabía.** Es el teorema de Korec (*A density estimate for
the 3x+1 problem*, Math. Slovaca 44, 1994, págs. 85 a 89), para todo
exponente mayor que log 3/log 4; Korec cita como antecedente a Allouche
(1979), y Tao (2019) llegó mucho más lejos: casi toda órbita alcanza
valores casi acotados. Aquí está el caso 0,8, en Lean y con las
constantes escritas, y el teorema completo en `CasaKorec` (abajo). El
artículo de Korec no se leyó: el enunciado viene de su ficha en EuDML y
de reseñas, y la prueba se rehízo aquí con la cuenta de patrones.

**Korec completo** ([CasaKorec.lean](CasaKorec.lean)). El mismo argumento
vale para todo exponente mayor que log 3/log 4, con bloques que crecen al
acercarse al umbral: de largo 2c, con umbral de c + 1 subidas y pesos
c + 1 y c. Los patrones de largo 2c con al menos c + 1 subidas son menos
que 4^c (`margen_entropia`). Para cada exponente racional u/v con
3^v < 4^u hay un bloque que sirve (`existe_bloque`), y entonces casi toda
órbita baja por debajo de n^(u/v) en a lo sumo log₂ n pasos (`korec`).
Como entre log 3/log 4 y cualquier exponente mayor hay un racional, vale
para todo exponente real mayor que log 3/log 4 (`korec_real`): es el
teorema de Korec tal como se enuncia. [cotejo_korec.py](cotejo_korec.py)
lo contrasta sin Lean: el bloque mínimo es de 18 pasos para 0,95, 26
para 0,9, 48 para 0,85, 372 para 0,8 y 1108 para 0,795; y hasta 2^17
baja por debajo de n^θ en a lo sumo log₂ n pasos el 92 % de los números
con 0,95, el 85 % con 0,9, el 72 % con 0,85 y el 62 % con 0,8.

**La rareza, al nivel de Lagarias.** Con la misma cuenta, en bloques de
10 000 pasos y pesos 6309 y 3691, la rareza de las fugas puras pasa de
x^0,96 a x^0,95: por debajo de x = 2^(10000m) hay a lo sumo 2·x^0,95
(`rareza_lagarias`). Es el exponente del teorema F de Lagarias (1985),
η ≈ 0,05, para el primer cruce. El cotejo cuenta los patrones de largo
10 000 con al menos 6309 subidas: son 2^9494,13, bajo el tope de 2^9500.

**Otra ventana, del muro A: CST para casi todo número** (`casi_todo_cst`).
El descenso de Terras da algo más fuerte que «casi todo número baja»:
casi todo número baja justo en su primer cruce, como pide CST, la forma
reforzada del muro A. Los que no lo cumplen, o aguantan 100m pasos sin
cruzar, o son menores que 100m·2^(100m) (`cuenta_sin_cst_bloques`); y
toda cuenta así tiene densidad cero (`densidad_de_cuenta`). Es el teorema
de Terras (1976).

**La densidad exacta de Terras** ([CasaTerras.lean](CasaTerras.lean)).
Es el teorema A de Terras tal como lo enuncia Lagarias: los números que
bajan de sí mismos en a lo sumo k pasos tienen una densidad exacta F(k),
y F(k) tiende a 1. La llave es que dos números congruentes módulo 2^k
bailan igual sus primeros k pasos (`congruentes_mismo_baile`, el
recíproco de un lema del retrato), así que cruzar en k pasos depende sólo
del resto módulo 2^k; y para n grande, bajar en k pasos es lo mismo que
cruzar (`baja_iff_cruza`). Entonces F(k) es la proporción de restos
módulo 2^k que cruzan (`densidad_terras`), y por la cuenta de patrones,
1 − F(k) ≤ 2/16^m si k ≥ 100m (`terras_tiende_a_uno`): una caída
exponencial, como en el teorema D de la reseña de Lagarias, con un
exponente algo peor (0,04 en vez de 0,05). Con las mismas piezas salen el
teorema B (cada patrón de largo k corresponde a exactamente un resto
módulo 2^k: `teorema_B`) y el C (el primer cruce depende sólo del resto,
y para n grande el tiempo de parada es exactamente el primer cruce:
`primer_cruce_resto`, `teorema_C`). Con esto, los teoremas A, B y C de
la sección 2 de la reseña de Lagarias están en Lean, y el D con un
exponente algo peor.
[cotejo_terras.py](cotejo_terras.py): F(k) coincide exactamente con la
proporción real de los números entre 2^20 y 2^21 que bajan en a lo sumo
k pasos; F(1) = 0,5, F(10) = 0,9375 y F(18) = 0,9714. Y para k < 15, los
2^k restos dan 2^k patrones distintos, como dice el teorema B.

**Lo que no da.** Son ventanas: dicen «casi todos», y el fugitivo y la
grieta viven en el conjunto de densidad cero. No tocan ningún muro.

## Mapa de los módulos

Los nueve archivos, en el orden en que se importan. Ninguno usa
hipótesis externas salvo donde se dice.

| Módulo | Qué trae | Consultas |
|---|---|---|
| [CasaPlano](CasaPlano.lean) | el plano: Collatz equivale a los dos muros; las dos fallas; el techo | 17 |
| [CasaOcelotas](CasaOcelotas.lean) | el tramo de hasta 24 picos del muro A, bajo LMN | 2 |
| [CasaRetrato](CasaRetrato.lean) | el retrato del fugitivo, rasgos 1 a 4, y su rareza | 17 |
| [CasaTablero](CasaTablero.lean) | rasgos 5 a 7, el plano clásico, el fantasma y el vecino | 18 |
| [CasaPlaneador](CasaPlaneador.lean) | la estela: no hay planeador fuerte; rasgo 8; ninguna órbita vuela en franja | 27 |
| [CasaGrieta](CasaGrieta.lean) | el retrato de la grieta: descenso de Terras, teorema E (bajo LMN o Rhin), circuitos, toda fuga | 28 |
| [CasaVentana](CasaVentana.lean) | Korec con exponente 0,8 y CST para casi todo número | 16 |
| [CasaKorec](CasaKorec.lean) | el teorema de Korec completo y la rareza x^0,95 de Lagarias | 15 |
| [CasaTerras](CasaTerras.lean) | los teoremas A, B y C de Terras: la densidad exacta del tiempo de parada | 13 |

## Comprobación

[comprobar_casa.py](comprobar_casa.py) verificó por huellas los 670
módulos de Ocelotas importados (20 de la base y 650 del cierre de 24).
El 07-10 compiló los nueve archivos en 37, 38, 29, 27, 39, 28, 28, 33 y 32
segundos y auditó sus 153 consultas (17 del plano, 2 del enganche con
Ocelotas, 17 del retrato, 18 del tablero, 27 del planeador, 28 de la
grieta, 16 de las ventanas, 15 de Korec y 13 de Terras): sólo `propext`,
`Classical.choice` y `Quot.sound`, sin `sorryAx` ni avisos
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
   sin retorno, tamaño pegado al pronóstico y cohete o planeador. El 07-10
   llegó el rasgo 8: su pronóstico no tiene techo y casi nunca está bajo.
   El mismo día, el retrato de la grieta, el intruso del muro A (sección
   «El retrato de la grieta»): casi todo número baja, y una grieta cruza
   tarde y, bajo LMN, es la primera de su fila.
3. **Buscar choques** (abierto; primera ronda el 06-10, sin choque;
   segunda ronda el 07-10, sección «Paso 3, segunda ronda: el planeador»,
   con el primer choque, sólo contra el planeador fuerte). Dos rasgos del
   fugitivo que se contradigan, o uno que choque con algo ya demostrado. Si
   aparece, el muro B queda en pie. Nadie lo ha logrado; ésta es la
   apuesta. El choque tiene que usar que el fugitivo es un número común y
   no un fantasma 2-ádico, y no debe valer en la casa del vecino (5n+1),
   donde el muro A se cae de verdad (el 13) y todo indica que hay
   fugitivos (el 7). Lo que sigue está en «Pendientes», más abajo.
4. **El dominó del muro A** (abierto; revisado el 07-10 con la estela y
   con el retrato de la grieta, sin avance). Una reducción que convierta una
   grieta con R+1 picos en otra con menos, o una desigualdad que valga
   para todo R a la vez. Completar el muro A incluye demostrar que no hay
   circuitos.
5. **Los muros completos.** A completo incluye «no hay circuitos», y B
   completo es «no hay fugas puras». Son los dos problemas abiertos del
   centro de Collatz.

Cada pieza se trabaja con presupuesto acotado, como en el
[plan del 28-09](../transversal20260927/PLAN_SESIONES_20260928.md): si no
avanza, se escribe por qué y se cierra.

**Pendientes (06-10).** El usuario los aprobó como ruta, en este orden.
Los tres apuntan al mismo hueco: el puente entre lo de carne y hueso y
lo propio del 3.

- **(a) Estudiar al planeador** (recomendado). El planeador tiene dos
  mitades: su pronóstico vuelve una y otra vez por debajo de un mismo C,
  y su tamaño vuelve una y otra vez a crecer apenas como el tiempo,
  `3·T^k(n) ≤ C·(3n + k)`. La primera mitad sola no alcanza: la cumple el
  baile que sube justo lo necesario para no cruzar (su pronóstico queda
  siempre entre 1 y 3), y todo baile es el de algún número 2-ádico. La
  segunda es de carne y hueso. La idea: si el planeador regresa a tamaños
  parecidos, el tramo entre dos regresos se parece a una vuelta de
  circuito, y contra los circuitos hay herramientas propias del 3 (LMN y
  el tramo de Ocelotas). Riesgo, según una primera cuenta a mano: un
  regreso aproximado deja el pronóstico del tramo cerca de 1, pero LMN
  sólo impide que el tamaño sea enorme comparado con el largo del tramo,
  y un planeador lo cumple sin problema. También contra los circuitos LMN
  alcanza sólo junto con mucho cálculo, y para pocos picos.
  **Hecho el 07-10** (sección «Paso 3, segunda ronda: el planeador»): el
  riesgo se confirmó y la vuelta de circuito no dio; funcionó la cuenta de
  patrones. Primer choque: no hay planeador fuerte. Quedan el cohete y el
  planeador intermitente.
- **(b) Cerrar la pinza.** Falta que un fugitivo obligue a que haya
  muchos. Hacia atrás eso ya pasa, pero con otra población: todo número
  cuya órbita pasa por una fuga es una fuga (no acotada, aunque no sea
  pura), y Krasikov y Lagarias (2003) probaron que, para x grande, por
  debajo de x hay al menos x^0,84 números cuya órbita pasa por un número
  dado que no sea múltiplo de 3. Si se probara que las fugas, todas y no
  sólo las puras, son menos que eso, no habría fugas y
  `muroB_de_sin_fugas` daría el muro B. Riesgo: nuestra rareza vale sólo
  para las fugas puras y es de x^0,96; contar bailes no baja de x^0,95, y
  en 5n+1 casi todas las órbitas parecen escaparse. Hace falta una idea
  nueva, propia del 3. **Revisado el 07-10:** cerró para el planeador
  fuerte; para el fugitivo general no cierra (misma sección).
- **(c) El dominó del muro A** (paso 4 de la lista), si (a) y (b) no
  avanzan con su presupuesto. **Revisado el 07-10:** la estela no lo
  mueve (misma sección).

**Después de los pendientes (07-10).** Quedan dos especies de fugitivo,
el cohete y el planeador intermitente, y las dos pasan casi todo el
tiempo arriba, donde la cuenta de patrones no las alcanza. La siguiente
pieza la elige el usuario. Una idea anotada, sin formalizar: cada mínimo
«de ahí en adelante» del pronóstico de un cohete deja un fugitivo puro
(`fuga_de_minimo`), y de un mínimo al siguiente el pronóstico crece a lo
sumo el factor 3/2, porque el paso que sigue a un mínimo es una subida.
Un cohete deja así al menos log₁,₅(D) crías en momentos en que su
pronóstico es a lo sumo D: muchas, pero sólo logarítmicamente; la pinza
pediría una potencia.

Con la meta «avanza hasta nuevo aviso» se hizo después, el mismo 07-10,
el retrato de la grieta (sección propia): el muro A gana su tramo de
«casi todo número» y el teorema E de Lagarias con constante escrita, sin
choque. Y las ventanas: Korec con exponente 0,8, Korec completo, CST para
casi todo número, la rareza de Lagarias y la densidad exacta de Terras
(sección «Una ventana: Korec»).

La [continuación de Perdices](../perdices20261007/LEEME.md), tras recuperar
la sesión local del 05-10, conecta esa cadena independiente con la ley de
Syracuse de Tao. Formaliza el olvido del arranque tras m subidas módulo
`3^m` y delimita el condicionamiento: una palabra sesgada puede olvidar
todo el arranque y seguir concentrada en un residuo. La cota binomial
para arranques uniformes tiene prueba escrita; la mezcla fina y el control
de la palabra de un fugitivo siguen pendientes. Evidencia exacta hasta
m=6, sin ampliar los censos de órbitas.

La [frontera y reserva](../perdices20261007/UMBRAL.md) precisa ahora el
sesgo de no-cruce y conecta con `tiempos_bajos_raros`: un fugitivo fijo
tendría reserva para toda continuación de longitud fija en una proporción
de tiempos que tiende a uno. No prueba que sus bits sean uniformes.

La continuación [tamaño y regresos](../perdices20261007/TAMANO.md)
prueba en Lean `T^k(n)/P_k=o(k)` para cada fugitivo. La identidad
multiplicativa y la inyectividad dan además
`(T^k(n)/P_k)^6<=n^6(S_k+1)`, formalizada después (párrafo siguiente).
Restringe los regresos del planeador a una cota de sexta raíz del
tiempo, todavía compatible con una fuga lenta.

**07-10, noche: el rasgo 9 y una idea para el cohete.** La sexta raíz
y su cuenta de regresos quedaron en Lean
([PerdicesSexta](../perdices20261007/TAMANO.md#sexta-raíz-y-techo-en-lean)),
con un corolario: antes del tiempo K, el pronóstico de un fugitivo
alcanza `K^(5/6)/n` (rasgo 9: el techo sube rápido). Hasta ahora
`techo_crece` daba del orden de `K^0,016`. Son cotas de «aterriza
poco»: no alcanzan al cohete, que bajo cada techo regresa sólo un número
finito de veces. Para él se exploró esa misma noche, en versión corta,
la idea del [primo de Mahler](../mahler20261007/LEEME.md): buscar una
herramienta sobre un número individual en el problema de las potencias
de 3/2. Quedó cerrada con un «por aquí no»: el teorema de 1995 sólo
prohíbe encierros, y el cohete no vive encerrado. Los
pasos 3 y 4 del [plan de tamaño](../perdices20261007/TAMANO.md#qué-debe-aportar-el-siguiente-paso)
siguen pendientes, con su evaluación escrita. Siguiente paso: el
[balance de la casa](#plan-del-07-10-balance-de-la-casa). Cohete,
planeador intermitente y grieta siguen abiertos.

**Actualización del 10-10:** el párrafo anterior conserva la decisión
del 07-10. El [cruce](../perdices20261007/CRUCE.md) ya combina la
sexta raíz con casi fugitivos y obtiene la cota de regresos con
exponente 4/25. La [novena raíz y duración](../perdices20261007/NOVENA.md)
mejoró después el exponente a 8/75. La continuación vigente,
[Colisiones](../perdices20261007/COLISIONES.md), excluye finalmente
al planeador y garantiza ξ finito para toda fuga pura. Se retoma
la cola real del cohete con esa hipótesis ya probada; la analogía
de ventanas de Mahler sigue sin proporcionar una contradicción.

**Duda abierta del usuario, 04-10:** «¿para terminar de construir los
muros necesitamos la racha 25, 26 y así sucesivamente? Eso nos dejaría
exactamente al principio del problema». No: ese camino no termina
nunca, y la ruta B existe justamente para evitarlo. El 06-10 añadió la
duda de los 360°: juntar afirmaciones sobre números termina apuntando a
todos los números. Es cierto: por eso el plano cambia el blanco y apunta
a los dos intrusos, el circuito y el fugitivo, y no a los números.

## Plan del 07-10: balance de la casa

**Antecedente histórico, integrado el 10-10.** La agenda vigente está
en [ESTADO_INVESTIGACION.md](../../ESTADO_INVESTIGACION.md).
La [conciliación](../jinetas20261010/CONCILIACION.md) ya atendió las
altas recuperadas y distinguió las discrepancias de huellas. Se
conserva aquí el plan original para no perder sus decisiones.

Propuesto el 07-10 por la noche, al cerrar el
[primo de Mahler](../mahler20261007/LEEME.md); el usuario pidió
documentarlo. Como en el resto de la ruta, los presupuestos son de
exploración, no plazos.

**Por qué parar ahora.** Siguen abiertas las tres especies de intruso: el
cohete y el planeador intermitente (muro B) y la grieta (muro A). Las
herramientas de la casa ya se probaron contra ellas:

- los conteos (la estela y la rareza) mataron al planeador fuerte, y a
  nada más;
- las cotas de regresos (Perdices, la sexta raíz y el rasgo 9) no
  alcanzan al cohete, que bajo cada techo regresa sólo un número finito
  de veces;
- el teorema de 1995 sólo prohíbe encierros, y el cohete no vive
  encerrado.

Contra el cohete sólo queda el lado 2-ádico: la conjetura de
periodicidad de Lagarias, que contiene entero el muro B. Eso ya es
atacar el problema de frente. Antes conviene saber con exactitud qué
está en pie.

Alegoría: antes de subir al último piso, el maestro de obras recorre la
casa con el plano en la mano. Anota qué muro aguanta, cuál es de cartón
y qué herramienta ya no corta.

**Paso 1. El balance** (una sesión, sin código nuevo y sin ampliar
censos). Entregable: una sección «Balance» en esta nota,
[la casa en una página](#la-casa-en-una-página) al día y una línea en el
ESTADO. Contenido:

1. **Una ficha por intruso** (cohete, planeador intermitente y grieta):
   sus rasgos probados y la forma de cada uno (Lean, prueba escrita o
   medida); las herramientas que se probaron contra él, con su «por aquí
   no» en una frase; y lo que falta exactamente.
2. **Lo propio y lo clásico.** Separar el aporte (la estela, los rasgos 8
   y 9, la sexta raíz y las formas en Lean con constantes escritas) de la
   literatura reformulada (Terras, Everett, Korec, Lagarias, Mahler y
   Bernstein), con la
   [revisión de novedad del 27-09](../../papers/revision20260927/REVISION.md#4-novedad)
   como modelo.
3. **Hipótesis externas y revisión.** Qué depende de LMN o de
   Rozier–Terracol, y qué espera revisión humana
   ([pendientes](../../gaopendientes.md)).
4. **Contabilidad.** Las altas de la
   [sesión recuperada del 05-10](../casa20261005_recuperada/RECUPERACION.md)
   que faltan por conciliar, y las huellas de fuente que ya no casan con
   su evidencia (las de `evidencia_tamano.json`; los objetos compilados sí
   coinciden).

**Paso 2. La decisión**, que toma el usuario con el balance delante:

- **(a) El lado 2-ádico (cohete).** Restringida a los enteros positivos,
  la conjetura de periodicidad dice que toda órbita acaba en circuito: es
  «no hay órbitas divergentes» con otro nombre. Su implicación hacia el
  muro B se deduce directamente de `rasgo_no_periodico` y `muroB_iff`,
  ya en Lean. Lo difícil es la conjetura misma.
- **(b) El planeador intermitente.** Hace falta una fuerza que lo obligue
  a volver con una frecuencia mínima. Los
  [pasos 3 y 4 de tamaño](../perdices20261007/TAMANO.md#qué-debe-aportar-el-siguiente-paso)
  quedaron evaluados como débiles.
- **(c) La grieta.** El dominó del muro A (paso 4 de la ruta), revisado el
  07-10 sin avance.
- **(d) Consolidar.** Revisión humana, artículos pendientes y la
  contabilidad del paso 1, sin investigación nueva.

Recomendación previa, a confirmar con el balance: no abrir (a) sin una
idea que lo haga más chico que el problema entero, como un caso parcial
o una clase de números. Como siempre, cada frente lleva presupuesto
acotado; si no avanza, se escribe por qué y se cierra.
