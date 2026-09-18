# ACTA DE LA 12a REVISION ADVERSARIAL

**Objeto:** el frente de densidad del 10-09-2026 completo
(`depuracion/frente20260910/`), las cinco tandas, sin revision externa
previa.

**Revisor:** Claude (Opus 5), sesion del 12-09-2026. De a una tanda,
sin agentes, un acta por tanda.

**Regla de la casa:** once de once revisiones mordieron. Esta tambien
mordio: **ocho hallazgos**. Pero conviene decir el titular entero desde
el principio, porque cambia como se leen: **ninguno de los ocho rompe
un teorema.** La matematica de las cinco tandas se sostiene.

---

## 1. Que se hizo, y que no

Nada del laboratorio ha sido modificado. Todo lo de esta revision vive
en `revision12_adv1/`. En particular **no ejecute los scripts del
frente**, para no sobrescribir sus `*_salida.txt`: reimplemente lo que
necesitaba desde las definiciones escritas.

### Lo verificado de forma independiente

| que | como |
|---|---|
| los cuatro ficheros Lean del frente | **recompilados por mi** con Lean 4.32.2; los cuatro dan exit 0, salida identica a la registrada, **cero `sorryAx`**, cero `native_decide` |
| la ley de paso `paso` | derivada a mano desde `T(x)` y contrastada contra **1.439.748 pares enteros reales**, 0 fallos |
| las demostraciones escritas | rehechas linea por linea, cada una en su acta |
| los numeros publicados | reproducidos con DP y scripts propios, escritos desde los `.md` y no desde su Python |

### Lo que NO verifique, y hay que decirlo

- **La hipotesis de modelado.** Todo el frente trabaja con bits de
  Terras equiprobables e independientes. Que eso represente la cadena
  real viene de LEONAS y de Terras, fuera de este frente. No lo revise;
  si esa hipotesis se cae, se cae todo lo de aqui y mucho mas.
- **El DP del laboratorio contra su propia especificacion.** Construi
  el mio y compare salidas; no audite `contraccion.py` ni
  `conteoconjunto.py` por dentro.
- **Que los enunciados Lean sean los "correctos".** Recompilarlos
  prueba que las pruebas son validas y los lei para ver que dicen lo
  que la prosa afirma. Eso no es lo mismo que garantizar que sean los
  enunciados que el programa necesita.
- Nada de esto sustituye a un revisor humano con el contexto completo.

---

## 2. Veredicto por tanda

| tanda | veredicto | mordidas |
|---|---|---|
| 1 -- Suricatas / invariantes | **correcta**; el Lean tapa la unica grieta real (3 no invertible sobre Int) | M1, M2 |
| 2 -- Balance de las Castoras | **correcta**; identidad (C) cierra exacta en 234 celdas y 2 testigos | M3, M4 |
| 3 -- Obstruccion de las Erizas | **correcta**; la ruta esta bien retirada | M5 |
| 4 -- Reloj de las Mangostas | **correcta**; la ley (M1) es exacta, no una cota | M6 |
| 5 -- Puente de las Gacelas | **correcta**; la mas fina del frente | M7, M8 |

Reproducciones que coinciden **al digito** con lo publicado: los
componentes comunes (2 y 1) y las 8.188 identidades de traslacion; las
siete normas SVD a 12 decimales; el rango `H/E` `0.038917-0.266228`; la
fraccion N0-N1 de Delta `17.7200%-25.6189%`; los estados del DP (3.154
en `t=16`, 590.042 en `t=28`); los cocientes de escala `0.450422` y
`0.469286`; el umbral de balota `T=29`; y los cuatro numeros del
contraejemplo de Gacelas.

---

## 3. Las ocho mordidas, por importancia

### Grupo A -- documentacion con consecuencia real (hay que arreglarlo)

**M3. `LEEME.md` seccion 5 propone como objetivo vigente lo que Erizas
demostro imposible.** Castoras.md si retiro el objetivo; el indice del
frente no. Sus dos parrafos seguidos dicen "No continuar intentando
demostrar el margen uniforme global" y "Ahora se busca ... acote su
margen H desde abajo, **con constante uniforme**". Y "margen uniforme"
esta definido en Castoras como `H >= epsilon(1-s)E`, que es literalmente
(E0). Quien entre por LEEME --que es lo que la nota manda-- se lleva de
tarea la unica tarea ya cerrada.

**M5. La retirada anunciada es mas ancha que lo demostrado.** La
seccion 5 de Erizas necesita `m` **ilimitada** a `t` fijo: medi que en
todo `m` finito el cociente esta estrictamente por debajo del limite
que el absurdo usa. Erizas misma dice "esto NO impide equidistribucion
a una escala `m` FIJA"; LEEME lo convierte en un "no continuar" sin
condiciones. **Con M3, LEEME seccion 5 esta equivocada en las dos
direcciones a la vez: prohibe lo que sigue abierto y propone lo que
esta cerrado.** Es el unico punto del frente que yo arreglaria hoy.

### Grupo B -- cosecha sin recoger (la casa se cobra de menos)

**M7 (la mas rentable). (G2) de Gacelas mejora a Erizas, y nadie las
conecto.** Erizas fija su caja con `S_t >= 1/(t+1)`; Gacelas demuestra
el mismo dia `S_t >= 1/sqrt(2t+3)`, estrictamente mejor para `t>=2`,
misma cadena, mismo `tau`, uniforme en `c0`. Sustituyendo, el exponente
de la caja baja de `t^(3/4)` a `t^(5/8)`: en `t=5000`, `log2 L_t` cae
de 1783 a 682. Eso **ensancha lo que (E8) excluye**, que es justo la
frontera que M5 senala como no dibujada. Ya esta demostrado dentro de
la casa; solo hay que enchufarlo.

**M8. El "piso `1/sqrt(log x)`" de Gacelas es la supervivencia, no el
producto.** El mismo argumento, dividido por `S_T` en vez de acotarlo,
da `P(Pi_tau x <= 1 | tau > T) >= 1 - 62(61/62)^T sqrt(2T+3)`, que en
`T=1024` es **0,99983 y no lleva logaritmo**. Consecuencia para el
programa: **el cuello no es `Pi_tau` en absoluto, es `W_tau` solo** --
lo que la seccion 4 dice en cualitativo, confirmado en cuantitativo.

**M6. El reloj de Mangostas es `O(n)`, no `O(n log n)`.** (M6) acota la
suma de rachas por `n` veces el maximo y le cobra el peor `a_n` a cada
racha; medi `E[A] = 2.3499` sobre las alturas reales en `t=24` frente
al `a_n = 6` que aplica. Con la media, o con una Chernoff sobre la
parte geometrica (que no necesita independencia, igual que la union que
ya usa), sale `O(n)`.

**M2. Una mejora de etiqueta no anotada.** El lema de las Suricatas sube
`C6` de *medido en `m=4,6,8`* a *teorema en todo `m`*, y ni LEEME ni la
etiqueta grabada en `correlacionafin.py` lo registran.

### Grupo C -- reporte (el resumen no lleva el dato que decide)

**M1 y M4. Se publica el rango y no la tendencia.** LEEME seccion 4
titula "cero cruces de 1/2" y Castoras publica `H/E` entre 0,0389 y
0,2662; ninguno dice que el peor `H/E` **cae** con el tiempo (0,1727 ->
0,0695 y 0,1507 -> 0,0427 entre `t=12` y `t=24`), ni que `rho` sube
hacia 1/2 con la forma `1-2rho ~ c/t` -- que es exactamente el
contraejemplo numero 1 que LEEME seccion 1 escribe de su puno.
**Rebajadas por lo que encontre despues:** Erizas SI reporta la subida
(da 0,450422 y 0,469286 para ensenarla). El frente no es ciego; los dos
resumenes no llevan el dato.

---

## 4. Lo que hay que decir a favor

Un revisor adversarial que solo lista mordidas miente por omision.

- **Los cuatro Lean recompilan sin `sorryAx`, y ninguno afirma de mas.**
  Mire los enunciados de nombre mas fuerte (`obstruccion_finita`,
  `balance_global`, `conteo_alto`, `masa_armonica`) y todos son lo que
  la prosa dice que son: ingredientes escalares o combinatorios, con el
  enlace a la cadena declarado explicitamente como **no** formalizado.
  No encontre ni un caso de teorema con nombre grande y contenido
  chico.
- **Los tres contraejemplos del frente son genuinos y se calculan por
  la ley**, no a mano: los dos de Castoras salen de `flatMap` sobre
  `paso`, y el de Gacelas es una enumeracion de 16 palabras.
- **Las autocorrecciones son reales.** Mangostas retira la lectura de
  "racha forzada de 21 pasos" del propio laboratorio y la sustituye por
  la ley correcta, con el conteo certificado en Lean. Erizas retira una
  ruta entera. Castoras acepta esa retirada en su cabecera.
- **Las reservas estan puestas antes de que el revisor llegue.** "No
  implica un margen uniforme en m", "NO es una implementacion ciega",
  "las cotas son deliberadamente holgadas", "Una mediana marginal no
  prueba esa interseccion". En cinco tandas no encontre **ninguna**
  afirmacion cuyo alcance estuviera inflado por encima de lo probado.
  El sesgo de esta casa es hacia declarar de menos, y tres de las ocho
  mordidas son precisamente eso.

---

## 5. Errores mios, anotados

Dos de mis scripts fallaron antes de dar la razon a la nota, y en los
dos casos el fallo era mio:

1. En Castoras normalice el exceso interno dividiendo por la masa en
   vez de por su cuadrado: daba `G=12`, `R=9/4`, `U=11` y la identidad
   (C) "fallaba" en el testigo 1. El testigo 2 pasaba igual con el bug,
   porque sus grupos tienen un solo elemento.
2. En Mangostas trunque las colas de la enumeracion: salia
   `P(L>=21) = 2^-20 - 2^-39` en vez de `2^-20`, y con eso 130
   "violaciones" de (M2) y 19 de (M4).

Los dejo escritos porque los dos sintomas --un termino fuera de sitio,
una cola corta por un epsilon del tamano de la truncatura-- se
confunden con facilidad con un error de la nota, y no lo eran.

---

## 6. La unica recomendacion

Arreglar `LEEME.md` seccion 5 (M3 + M5): decir que (E0) con `m`
ilimitada esta cerrada, que las versiones a escala acotada no lo estan,
y quitar "con constante uniforme" del objetivo siguiente. Es lo unico
del frente que hoy puede desviar trabajo hacia una pared conocida.

Despues, si se quiere cobrar lo que ya esta pagado: M7 (enchufar (G2)
en la caja de Erizas) es la mejora mas barata y la de mayor efecto.

---

## 7. Reproduccion completa

    lean depuracion/frente20260910/invariantes.lean
    lean depuracion/frente20260910/balance.lean
    lean depuracion/frente20260910/obstruccion.lean
    lean depuracion/frente20260910/rachas.lean
    lean depuracion/frente20260910/transferencia.lean

    python revision12_adv1/rep_cadena_real.py
    python revision12_adv1/rep_invariantes.py
    python revision12_adv1/rep_norma_limite.py
    python revision12_adv1/rep_testigos.py
    python revision12_adv1/rep_castoras.py
    python revision12_adv1/rep_erizas.py 28
    python revision12_adv1/rep_erizas_escala.py
    python revision12_adv1/rep_mangostas2.py
    python revision12_adv1/rep_gacelas.py

Actas por tanda: `acta_tanda1_suricatas.md`, `acta_tanda2_castoras.md`,
`acta_tanda3_erizas.md`, `acta_tanda4_mangostas.md`,
`acta_tanda5_gacelas.md`.

---

**No se ha probado el teorema de conteo, ni P2, ni densidad uno, ni
Collatz. Esta revision no cambia eso: solo confirma que lo que el
frente dice haber probado, lo probo.**
