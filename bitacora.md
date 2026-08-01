# Bitácora

Resumen corto por sesión. Lo detallado va en `CLAUDE.md`; esto es para saber en
diez líneas qué pasó y por dónde se iba. La entrada más reciente arriba.

---

## 2026-08-01 — el día en que la documentación se editó a ciegas

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

**El punto 5 sigue abierto: se cerraron 2 de sus 6 correcciones.** Quedan la
holgura mínima del piso (1), el exponente de la criba (4), el `0,2286` contra
`ln(Res(993))` (5) y la errata de `RES_993` en `mapahilos.py` (6) — más las
cuatro cosas de la lista de abajo, de las que sólo se mencionó que las dos
discrepancias con Hercher existen, **sin escribir sus valores**.

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
| `clase_mod_2k` | **Sí**, vía los restos de los once. Comprobación real |
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

### 5. CONSOLIDAR EL `CLAUDE.md` — abierto: 2 de 6 hechas el 01-08-2026

La sesión del **31-07-2026** dejó seis ficheros nuevos y **seis correcciones sin
escribir en el documento**. El código está hecho y verificado; la documentación
va atrasada. Es exactamente la deuda del punto 3, otra vez, sólo que al revés.

**Estado: las número 2 y 3 se consolidaron el 01-08-2026 (commit `d8b1d73`).
Quedan la 1, la 4, la 5 y la 6, y las cuatro de la lista de después.**

**Las seis correcciones al `CLAUDE.md`:**

1. **La holgura mínima del piso no es una constante.** Vale `log2(1 + 1/(3n))` y
   decrece con `n`, o sea que depende del rango barrido. Y la frase del documento
   **mezcla dos rangos**: el `+0,000002` y los `99.999 casos` son de un barrido a
   **200.000**; el `28.325 de 50.000` de los pares es a **100.000**.
   *(Tercera vez que aparece el mismo modo de fallo: tomar el valor de una muestra
   por una constante. Las otras dos fueron el `1,7345` del coral y ésta.)*
2. **El `+1` aparece DOS veces, no tres.** `ε = ln(2^B/(3^A·n))` y
   `S = Σ ln(1+1/(3x))` son **idénticamente la misma suma** (`elmasuno.py`,
   20.011 casos exactos). El residuo `1,7e-7` era error de coma flotante. Y de ahí
   sale que `ε > 0` queda **demostrado para todo `n`**, no medido en 6.555 pares.
3. **La explicación del coral era casi toda falsa.** `45 = 3²·5` adelanta el choque
   **de 32 a 31: un nivel de treinta y uno**. El motor real son las permutaciones
   de aristas, que existen para cualquier `N`. La ley medida es
   `(N+11)/2` si `N ≡ 3 (mod 4)` y `(N+19)/2` si `N ≡ 1 (mod 4)`, sin rastro de la
   factorización. **Y la predicción del número primo de rumbos FALLÓ**: 43 y 47
   chocan antes que 45. Hay que reescribir la sección entera y quitar esa
   candidatura a nota original.
4. **El exponente de la criba `2^(−0,05k)` es el asintótico.** En el rango real
   (`k = 34`) es ≈ **0,108**, el doble.
5. **El grosor `0,2286` y `ln(Res(993)) = 0,225654` NO son el mismo número.** El
   documento los identifica; uno se midió sobre pares de una trayectoria y el otro
   sobre trayectorias enteras, y difieren en la tercera cifra.
6. **Errata de constante:** `mapahilos.py` guarda `RES_993 = 1.2531421442887503`
   y el exacto es `2^61/(3^32·993) = 1,2531421443950680…` — mal desde la décima
   cifra. No mueve nada medido, pero hay que arreglarlo.

**Y cuatro cosas más que salieron al clasificar y no están escritas:**

- **`«cualquier otro ciclo mide ≥ 19.478.780.533 pasos»` no tiene fuente.** Se
  atribuye a «la literatura de 2025», sin autor ni título. Es la única afirmación
  marcada `demostrado` cuya fuente no nombra a nadie. Localizarla o degradarla.
- **La comprobación 4 de `guardarhilos.py`** se anuncia como «la literatura
  predijo nuestro hallazgo» y se apoya en **Wu–Huang 2001, marcada como no
  verificable**. El hecho es cierto (`clasesfusion.py` lo rederiva); la atribución
  no está comprobada.
- **El vocabulario de `afirmaciones.db` se quedó corto:** la rueda del árbol es una
  clase residual **módulo `3^j`, no `2^k`**. La categoría real es «clase residual».
- **Las dos discrepancias con Hercher** (`reimpl.py`) no están documentadas: el
  séptimo `epsilon` (`1,2298e-43` contra `1,11e-43`) y la tercera fila de la
  Tabla 1 (`4,640282e18` contra `4,68e18`).

**Y la observación estructural que más importa para el objetivo elegido:** de las
72 afirmaciones de la base, el bucle `casi_todo_n` tiene **5 filas y 3 sin fichero
detrás**. El repo **no tiene ni una línea de código propio** que verifique nada de
tipo «casi todo `n`» — todo es literatura ajena (Everett, Tao). Y ése es justo el
hueco «casi todos → todos» donde se decidió apuntar. Hay 31 piezas que componen
sobre clases y **cero instrumentos propios sobre densidad**.

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
