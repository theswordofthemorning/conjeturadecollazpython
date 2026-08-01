# Bitácora

Resumen corto por sesión. Lo detallado va en `CLAUDE.md`; esto es para saber en
diez líneas qué pasó y por dónde se iba. La entrada más reciente arriba.

---

## 2026-08-01 (tarde) — el punto 5 cerrado, y una cita que existía y aun así sobraba

Mantenimiento otra vez, delegado a un agente como manda la regla de prioridad.
**Se cerraron las diez correcciones que quedaban del punto 5.** El detalle está
ahí abajo, en el propio punto 5. Lo que vale la pena contar aquí son las tres
cosas que salieron y no estaban previstas.

### 1. La cita fantasma existía. Y había que quitarla igual

El plan decía: *«localizar la cita del `≥ 19.478.780.533` o degradarla»*. Se
localizó — **Laurore, *Adv. Pure Math.* 15(6) (2025), DOI
`10.4236/apm.2025.156018`**, con DOI que resuelve en Crossref. Y aun así hubo que
sacarla, por tres razones acumuladas:

- editorial **SCIRP**, **cero citas**;
- el número es **once veces más débil** que el estado del arte (Barina 2025:
  `217.976.794.617` en el atajo, `355.504.839.929` en el clásico). O sea que el
  repo llevaba citada como *«lo que exige la literatura»* **una cota peor que la
  que ya se conocía**;
- **no encaja en la forma cerrada de Eliahou 1993** (`301994a + 17087915b +
  85137581c`, `b ≥ 1`, `a·c = 0`). Barrido exhaustivo propio: **0 soluciones**,
  mientras que `10.439.860.591`, `114.208.327.604` y `217.976.794.617` sí
  encajan.

> **La salida que faltaba en la lista.** Eran dos opciones —localizar o
> degradar— y resultan ser tres: **localizar y descartar igualmente.** Que una
> cita exista no la hace buena; hay que mirar dónde se publicó y si el número
> mejora o empeora lo que ya se sabía.

### 2. El `0,2286` no difería «en la tercera cifra». Estaba en otra unidad

El punto 5 decía que el grosor de la lámina y `ln(Res(993))` diferían en la
tercera cifra. **Es peor: uno está en bits y el otro en nats, y no miden lo
mismo.** `0,2286 bits = 0,158478 nats` contra `0,225654 nats = 0,325550 bits` —
factor **1,42**. Y el `0,2286` **ni siquiera es una cota**: su máximo se alcanza
en el par `(221 → 16)`, que es la trayectoria entera del 221, así que ese número
mide el 221 y nada más.

*Es la hermana exacta del acierto de `elmasuno.py` —allí dos números que parecían
distintos eran el mismo—, y las dos se arreglan igual: **traducir a las mismas
unidades antes de comparar.***

### 3. La frase de la holgura mezclaba TRES rangos, no dos

Lo que estaba anotado eran dos. Con `pisoaltitud.py` delante salieron tres: los
`99.999 casos` no son del enunciado de los impares (ése tiene **49.999**), son de
la variante del **atajo**. **Tercera aparición del mismo modo de fallo** — tomar
el valor de una muestra por una constante — después del `1,7345` del coral y del
`0%` de encimadas de Harriss.

### El saldo en código

`mapahilos.py` y `elmasuno.py` calculan `RES_993` en vez de copiarla (y el
segundo corta con `SystemExit` si alguien la vuelve a escribir a mano);
`guardarhilos.py` imprime por separado el hecho y la atribución;
`guardarafirmaciones.py` renombra el cuantificador a `clase_residual` y añade
tres correcciones y una constante. Los cuatro corridos, 0 fallos. Barrido cp1252
sobre los 35 `.py`: **0 hallazgos**.

---

## 2026-08-01 (mañana) — el día en que la documentación se editó a ciegas

Sesión corta y de mantenimiento. **El saldo es una regla nueva, y la pagó un
error propio.**

### El error, que es lo único que vale la pena contar

Se pidió una revisión del `CLAUDE.md`. Se revisó y se corrigió **sin hacer
`git fetch` antes**. El remoto tenía un commit de más (`b1b32f3`: 5.114 líneas,
siete `.py` nuevos y dos bases), y ese commit **ya había hecho las mismas
correcciones**. Todo el trabajo salió redundante y hubo que tirarlo y rehacerlo
contra la versión buena.

**Por qué no se vio:** `git status` a secas escribe `## main...origin/main` sin
flechas —que se lee como «sincronizado»— porque compara contra la última copia
*local* del remoto. El `[behind 1]` sólo aparece **después** del `fetch`.

> **Regla nueva, y va como PRIMERA sección del `CLAUDE.md`, antes de
> «Instalación»: `git fetch origin && git status -sb` antes de tocar nada.**
> Con el caso de hoy escrito como ejemplo, y la salida si ya editaste sin
> `fetch`: `stash` → `merge --ff-only` → mirar qué de lo tuyo sigue haciendo
> falta. Casi siempre es menos de lo que parece.

*Es el mismo tipo de trampa que las de cp1252 y la del estimador `B/A`: no es
falta de cuidado, es una herramienta que informa algo cierto y engañoso a la vez.
Por eso se anota, no se recuerda.*

### Lo que sí quedó arreglado (commit `d8b1d73`)

**Conteos.** El commit anterior decía *«conteos al día (28 .py)»* y **añadió
siete `.py` en ese mismo commit**, dejándolos desfasados en el acto:

| | decía | es |
|---|---|---|
| scripts | 28 | **35** |
| `numpy` | seis | **siete** (faltaba `descensoresto.py`) |
| `sqlite3` | dos | **cuatro** |
| `secuencia_de` | nueve | **diez** (faltaba `elmasuno.py`) |
| auto-verificados | 28 / 20 | **35 / 27** |

Barrido cp1252 rehecho sobre los 35: **0 hallazgos**.

**La Mitad C.** `guardarmallas.py` figuraba como *«el único programa cuyo
resultado no es una imagen»*. Hoy **19 de los 35 no dibujan** y sólo 16 abren
navegador o ventana. El caso por defecto de un script nuevo ya no es plotly, y
el documento ahora lo dice y manda copiar `pinzaciclos.py`.

**Dos correcciones del punto 5, consolidadas en la prosa** (estaban sólo en esta
bitácora, y la prosa seguía afirmando lo refutado):

- **El `45 = 3²·5` del coral**, que estaba presentado como *la candidata a nota
  original*. Corregido en los tres sitios donde vivía, con la ley que sí gobierna
  el umbral y la predicción fallida de los primos.
- **El `+1` aparece dos veces, no tres.**

Y **la Fase 1 del plan de la pinza** figuraba como pendiente teniendo ya
`reimpl.py` en el repo.

### Lo que NO se hizo, para que no se dé por cerrado

**El punto 5 quedó abierto: se cerraron 2 de sus 6 correcciones.** Quedaban la
holgura mínima del piso (1), el exponente de la criba (4), el `0,2286` contra
`ln(Res(993))` (5) y la errata de `RES_993` en `mapahilos.py` (6) — más las
cuatro cosas de la lista de abajo, de las que sólo se mencionó que las dos
discrepancias con Hercher existen, **sin escribir sus valores**. *(Las ocho se
cerraron esa misma tarde; ver la entrada de arriba.)*

*Nota de fechas: el punto 5 habla de «la sesión del 31-07-2026» y el commit que
la contiene está fechado el 30-07. No se tocó; queda anotado por si confunde.*

---

## 2026-07-30 — el día de las correcciones

Sesión larga. **El saldo real no son los hallazgos: son las siete correcciones a
cosas que el repo daba por buenas.** Ninguna la encontró nadie de fuera.

### Lo que se midió nuevo

| | |
|---|---|
| **El umbral de los 45 rumbos** | El coral de Harriss **sí** se vuelve a juntar. Primer choque exacto en profundidad **31**; a la 59 es el 1–1,5% de los nodos. Verificado con resto cero módulo `Φ₄₅` en aritmética entera. La causa es `45 = 3²·5`, o sea el ángulo, no Collatz |
| **Los negativos son `3n−1`** | Identidad exacta, 8.095.665 pasos, 0 fallos. Tres ciclos, ningún cuarto hasta 10⁶. Y las dos reglas ciclan en **lados opuestos de `log₂3`**, forzosamente |
| **Las constantes** | Wagon `9,4779555…` (con entrada en OEIS) medida a 0,064%. La escalera `1:2:3` de las constantes de parada |
| **El ajuste fino** | `q = 3` es el único impar que converge. Pero el umbral `4` resultó ser `f = 1/2` reescrito, o sea Terras otra vez |
| **Collatz contra la moneda** | Entropía de exactamente `k` bits hasta `k=12` y a profundidad 128; pero `P(impar\|impar) = 0` exacto y el patrón **se puede encargar** (`2^4000−1` da 3.999 impares seguidos) |
| **El piso de la altitud** | Una **cota**, no una tendencia. Lo único de la sesión con forma de teorema |
| **La pinza de ciclos** | Barrido de 2.147 millones de restos. Recuperó **los cuatro ciclos de Collatz sobre `Z`** sin que se le hablara de negativos |
| **`k = 32`** | La cota inferior demostrada sube a **43,5658%**. `a(32) = 1.871.137.623` |
| **Los récords publicados** | 243 récords de Roosendaal y Barina traídos y cruzados contra el repo. Nada se rompe |

### Las siete correcciones

1. El `0%` de encimadas del coral **era falso** — sólo valía hasta 3.000 semillas.
2. El `1,7345` del coral **no es una constante**, es el valor de una muestra (se asienta en `1,7320`).
3. La fila "se escapan del rango" del A/B **no discrimina**: mide el rango, no la regla.
4. `2/ln(4/3)` es la constante del **atajo**, no del mapa clásico.
5. El par `(8k+4, 8k+5)` es de **Garner**, no de Lagarias.
6. `Wu–Huang 2001` **no se pudo verificar**: sin DOI, no está en Crossref, y Elia–Tucker no la citan.
7. **Al piso de la altitud le faltaba la hipótesis `n impar`** — sin ella es falso en 28.325 de 50.000 pares.

**La séptima es la que más enseña.** El piso se probó contra los **243 récords
publicados** —los números que más suben y más tardan de todo lo conocido— y
**pasaron los 243**. Lo cazó el barrido de control sobre números corrientes.
*Los extremos confirman; los controles refutan.*

### Dos negativos nuevos

- **Ninguna constante de Collatz coincide con ninguna constante fundamental.**
  Test con modelo nulo: `p = 0,317`, y **sube a 0,45** al corregir el nulo.
- **La racha inicial no predice la altitud** (correlación 0,59). Lo que hace es
  ponerle un piso exacto — cota sí, tendencia no.

### Vías que quedaron cerradas, con su razón

- **El barrido de restos está muerto.** Terras excluyó en 1976 todos los bucles
  de periodo ≤ 2.592, y nuestro `k` *es* ese periodo. Todo su rango alcanzable ya
  es teorema. Para territorio virgen harían falta `2^2592` restos: 781 cifras.
- **Las cribas no sirven para ciclos, y es estructural.** `T^k` es una biyección
  sobre `Z/2^k`: cada vector de paridad es una clase única. No hay nada que
  descartar. Una criba necesita que muchas clases compartan destino.
- **Los promedios no pueden demostrar nada** sobre un caso individual. La
  pregunta que queda como filtro permanente: **¿esto es un promedio o es una cota?**

---

## Lo que queda pendiente

### 1. El plan de la pinza, en tres fases

Lo que lo hace viable: **Hercher no usa el teorema de Baker en ninguna parte** —
toda la maquinaria diofántica entra como un número importado. Y la métrica del
esfuerzo, medida: **60 líneas de stdlib excluyen `m ≤ 82`**; todo el aparato del
paper (dos programas en C++, cinco semanas de cómputo) compra el tramo 82 → 91.

- **Fase 1** — traer `reimpl.py` al repo. 130 líneas, reproduce el Teorema 23
  dígito a dígito en 5,5 s. Sería el primer programa del laboratorio que
  reproduce matemática arbitrada.
- **Fase 2** — la escalera afín de Wang: un intervalo intersecado con una clase
  residual. *Eso es la pinza.* Media está construida en `clasesfusion.py`.
- **Fase 3** — **verificar a Wang**, no superarlo. Su preprint (`m ≤ 95`) tiene
  dos días, no está arbitrado y nadie lo ha comprobado. Si aguanta, se dice; si
  se cae, eso sí es un hallazgo.

### 2. El resto de la cola

- **El número primo de rumbos.** Predicción escrita y sin medir: con un número
  primo de rumbos el umbral de profundidad del coral debería dispararse. Barato.
- **Colorear el árbol de `collazarbol.py` con la rueda** mod 3.
- **El `+1` aparece ya tres veces** (grosor 0,2286 de la lámina, el `+2` del
  espejo base 2, la desviación −0,0035 de la fracción impar). ¿Son la misma
  cantidad? Sería lo único que **unifica** piezas en vez de acumularlas.
- **`clasesfusion.py` a `k = 34`.** Con `clasesparalelo.py` cuesta ~4× lo de
  `k=32`. No va a decidir la conjetura de Wu — los incrementos de la razón
  (`0,0050 → 0,0039 → 0,0037 → 0,0031 → 0,0027 → 0,0026`) encogen demasiado
  despacio para distinguir "geométrico" de "1/k" — pero alarga la única serie
  que puede.
- **OEIS.** `oeis_borrador.txt` está redactado y listo. **No se ha enviado**, y
  requiere una cuenta y una firma que son de una persona.

### 3. La deuda de método

**La sesión del 30-07-2026 casi no dejó código.** Casi todo se midió en scripts
sueltos fuera del repo y sólo quedó escrito en el `CLAUDE.md`. Sobrevivieron
`pinzaciclos.py`, `cruzarecords.py`, `records.json` y `clasesparalelo.py`; el
resto de las mediciones **no se pueden reproducir**. Es la deuda más concreta
que tiene el laboratorio.

*(Parte de esa deuda se pagó el mismo día: `pisoaltitud.py`, `elmasuno.py`,
`reimpl.py` y `coralprimos.py` devolvieron cuatro de esas mediciones a fichero
ejecutable, y `afirmaciones.db` recoge los enunciados con su cuantificador.)*

### 4. LA PASADA CRUZADA — encargada a Fable 5, pendiente

**Qué hay que hacer.** Cruzar **cada una de las afirmaciones de
`afirmaciones.db`** contra **dos pools de datos a la vez**:

1. **Los once hilos de `hilos.db`** (100000 … 100010, con sus pasos, cruces,
   fusiones y cola común ya calculados). Son el caso ORDINARIO.
2. **Los 243 récords publicados de `records.json`** — retraso y altitud, de
   Roosendaal y Barina, hasta 2^71. Son el caso EXTREMO. `cruzarecords.py` ya
   sabe leerlos, así que el código de lectura está hecho.

Por cada pareja (dato, afirmación), decir si la cumple, la contradice, o si la
afirmación no aplica.

Nada hay que recalcular: las dos bases y el JSON están en el disco y
versionados. Se abren con `sqlite3` y `json.load` y se cruzan.

**Por qué los dos pools, y no uno.** Es la lección que dejó el piso de la
altitud el 30-07-2026, y es el mejor argumento que tiene este laboratorio:

> **Los extremos confirman; los controles refutan.**

Al piso lo probaron contra los 243 récords —los números que más suben y más
tardan de todo lo conocido— y **pasaron los 243**. El error del enunciado (le
faltaba la hipótesis `n impar`) lo cazó el barrido de números corrientes. Los
récords son tan raros que confirman casi cualquier cosa; los números del montón
son los que rompen.

Los once hilos aportan el montón, con casos incómodos a propósito: el `100009`
tarda 309 pasos y sube a 35 millones; el `100001` es el único solitario de los
once (todos sus cruces son cola común); y los seis del `100002` al `100007` se
funden con desfase cero. Los 243 récords aportan el rango: de 2 a 71 bits, que
es donde una cota se rompe si va a romperse por tamaño.

Si una afirmación falla en cualquiera de los dos pools, es un hallazgo. Si
aguanta en los dos, es un control de verdad.

**EL AVISO QUE NO SE PUEDE SALTAR, y es la razón de que la columna
`cuantificador` exista.** La pasada sólo significa algo para dos de los seis
cuantificadores:

| cuantificador | ¿tiene sentido cruzarlo contra 11 hilos? |
|---|---|
| `todo_n` | **Sí.** Once contraejemplos potenciales. Si falla uno, la afirmación es falsa |
| `clase_residual` | **Sí**, vía los restos de los once. Comprobación real. *(Se llamaba `clase_mod_2k` hasta el 01-08-2026; el módulo no siempre es `2^k`.)* |
| `casi_todo_n` | No. Once números no dicen nada de una densidad |
| `promedio` | **NO, y es peligroso.** Once trayectorias no estiman una media |
| `ciclos` | No aplica: ninguno de los once es un ciclo |
| `verificado_hasta` | No aplica: son afirmaciones sobre rangos, no sobre números |

**El modo de fallo concreto a evitar:** informar «11 de 11 confirmadas» sobre
una fila de tipo `promedio`. Eso no es confirmación, es ruido con forma de
tabla — el mismo error que produjo el `1,7345` del coral (valor de una muestra
tomado por constante) y el `+0,000002` de la holgura mínima del piso (dos
rangos distintos mezclados en la misma frase). La pasada tiene que **negarse a
evaluar** las filas de `promedio` y `casi_todo_n`, no evaluarlas y matizar.

**Y la trampa propia de estos once, que ya está medida:** las once trayectorias
comparten la cola `[16, 8, 4, 2, 1]` por obligación. 275 de los 1.258 cruces son
eso y no significan nada. `hilos.db` marca cada cruce con `es_cola` justamente
para esto; hay que usar esa columna y no contar la cola como coincidencia.

### 5. CONSOLIDAR EL `CLAUDE.md` — ⇢ CERRADO EL 01-08-2026

La sesión del **31-07-2026** dejó seis ficheros nuevos y **seis correcciones sin
escribir en el documento**, más cuatro cosas sueltas. **Las diez están hechas:**
la 2 y la 3 el 01-08-2026 por la mañana (commit `d8b1d73`), y las ocho restantes
esa misma tarde.

**Las seis correcciones al `CLAUDE.md`:**

1. ⇢ **HECHA. La holgura mínima del piso no es una constante.** Vale
   `log2(1 + 1/(3n))` y decrece con `n`. *Y la frase mezclaba **tres** barridos,
   no dos, que fue lo que apareció al mirarla con `pisoaltitud.py` delante:* los
   `99.999 casos` son del barrido a 100.000 **pero de la variante del atajo** —el
   enunciado de los impares tiene **49.999**—, el `+0,000002` es de un barrido a
   **200.000**, y el `28.325 de 50.000` es de 100.000. Verificado que la fórmula
   reproduce el mínimo medido: `log2(1+1/(3·99.997)) = +0,000004809` contra
   `+0,000004809` medido. *(Tercera vez del mismo modo de fallo; las otras dos
   son el `1,7345` del coral y el `0%` de encimadas de Harriss.)*
2. ⇢ **HECHA (`d8b1d73`). El `+1` aparece DOS veces, no tres.**
3. ⇢ **HECHA (`d8b1d73`). La explicación del coral era casi toda falsa.**
4. ⇢ **HECHA. El exponente de la criba `2^(−0,05k)` es el asintótico.** En el
   tramo `k = 20..40`, que es donde vive el `k = 34` de Barina, el decaimiento
   medido es **`0,108101`** — el doble. Cada bit extra elimina **7,2%** ahí y
   **3,4%** en el límite. La tabla por tramos de `descensoresto.py` (hasta
   `k = 1400`) está copiada al documento, con el aviso del signo: un exponente
   mayor significa que la densidad cae **más deprisa**.
5. ⇢ **HECHA, y salió peor de lo que decía este punto. El `0,2286` y el
   `ln(Res(993)) = 0,225654` no difieren «en la tercera cifra»: están en
   UNIDADES DISTINTAS.** El `0,2286` es `log₂` (bits) sobre los 6.555 pares del
   221; el `0,225654` es `ln` (nats) sobre trayectorias enteras. Traducidos:
   `0,2286 bits = 0,158478 nats` contra `0,225654 nats = 0,325550 bits`, factor
   **1,42**. Y el `0,2286` **ni siquiera es una cota**: el máximo sobre los pares
   del 221 se alcanza en el par `(221 → 16)`, que es su trayectoria entera, así
   que ese número es el `ε` del propio 221 en bits (`Res(221) = 1,17173`). Lo que
   sí vale es la desigualdad `h ≤ log₂(Res(seq[i]))`.
6. ⇢ **HECHA. Errata de constante.** `mapahilos.py` y `elmasuno.py` guardaban a
   mano `RES_993 = 1.2531421442887503`; ahora los dos la calculan como
   `2**61/(3**32*993)` y `elmasuno.py` corta con `SystemExit` si alguien vuelve a
   copiarla. Comprobado que no mueve nada: `mapahilos.py` sigue imprimiendo
   `techo = 0.225654` y `fallos: 0`.

**Y las cuatro cosas más que salieron al clasificar:**

- ⇢ **HECHA, con giro. La cita de `≥ 19.478.780.533 pasos` SE LOCALIZÓ, y hubo
  que quitarla igual.** Es **Laurore, *Adv. Pure Math.* 15(6) (2025) 351–389,
  DOI `10.4236/apm.2025.156018`** — el DOI resuelve en Crossref. Pero es de
  **SCIRP**, tiene **cero citas**, y sobre todo **el número es 11 veces más
  débil que el estado del arte**: Barina 2025 da `217.976.794.617` (atajo) y
  `355.504.839.929` (clásico). Además **no encaja en la forma cerrada de
  Eliahou 1993** (`301994a + 17087915b + 85137581c`, `b ≥ 1`, `a·c = 0`):
  barrido exhaustivo, **0 soluciones**, mientras que las tres cotas verificadas
  sí encajan. Sustituida por la de Barina en los dos sitios donde vivía.
  *Lección que no estaba prevista: la salida no era «localizar o degradar»,
  eran tres — faltaba **localizar y descartar igualmente**.*
- ⇢ **HECHA. La comprobación 4 de `guardarhilos.py`.** Separadas las dos cosas
  en el `CLAUDE.md` y en el `print()`: **el hecho es cierto y es propio**
  (`clasesfusion.py` lo rederiva desde Terras y decide los infinitos `m`), **la
  atribución a Wu–Huang 2001 sigue pendiente de localizar**. Quitada la frase
  «la literatura predijo nuestro hallazgo».
- ⇢ **HECHA. El vocabulario de `afirmaciones.db`.** `clase_mod_2k` renombrado a
  **`clase_residual`** en las 23 apariciones, con la razón escrita en la
  cabecera: la categoría es la **forma** del argumento —una comprobación finita
  que decide para los infinitos números de una clase de resto— y el módulo es un
  detalle del enunciado. Las dos filas que lo motivaron (la rueda del árbol, mod
  3/9/27; y los evitados de `2n mod 27`) ya no llevan una nota pidiendo perdón
  por la casilla. Base regenerada: **80 afirmaciones, 22 correcciones, 20
  constantes, las tres comprobaciones a 0 fallos.**
- ⇢ **HECHA. Las dos discrepancias con Hercher**, con sus valores y con la
  explicación de por qué ninguna mueve el resultado. El séptimo `ε` sale
  `1,2298e-43` contra `1,11e-43` (el nuestro es **más conservador**, y el
  denominador mínimo es **plano** en todo el rango: seis valores de `ε` entre
  `8e-44` y `5e-43` dan el mismo `7.941.964.418.702.608.664.581`). La fila
  `m = 276` de la Tabla 1 sale `4,640282e+18` contra `4,68e18`, y ahí la
  sospecha va contra el papel: `4,68e18` **no es denominador de ninguna
  semiconvergente de `log₂3`**, luego no es alcanzable por el método.

**Y la observación estructural que más importa para el objetivo elegido:** de las
**80** afirmaciones de la base, el bucle `casi_todo_n` tiene **5 filas y las 5 sin
fichero detrás**. El repo **no tiene ni una línea de código propio** que verifique
nada de tipo «casi todo `n`» — todo es literatura ajena (Everett, Tao). Y ése es
justo el hueco «casi todos → todos» donde se decidió apuntar. Hay **34** piezas
que componen sobre clases y **cero instrumentos propios sobre densidad**.
*(Conteos reverificados contra `afirmaciones.db` el 01-08-2026; los que había
—72, 3 sin fichero, 31 piezas— estaban desfasados.)*

---

## El objetivo, reformulado

> **No vamos a encontrar un número que haga bucle. Ni a demostrar que todos bajan
> a 1. Ni que exista uno que suba para siempre.**
>
> **Lo que sí se puede buscar es el cuarto camino: las reglas que generan todos
> los números de la secuencia de Collatz, sin generar la secuencia.**

Es alcanzable, se puede contradecir, y el repo ya tiene cuatro piezas antes de
que tuviera nombre: `mallaresiduos.py`, `clasesfusion.py`, `mallascerradas.py`, y
el Lema 8 de Hercher, que resultó ser el mismo objeto. Para calibrar: el
resultado más fuerte que existe sobre Collatz, **Tao 2019**, es de este tipo.
