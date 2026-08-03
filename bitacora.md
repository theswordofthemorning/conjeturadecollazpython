# Bitácora

Resumen corto por sesión. Lo detallado va en `CLAUDE.md`; esto es para saber en
diez líneas qué pasó y por dónde se iba. La entrada más reciente arriba.

---

# ⇢ 03-08-2026 — LA ECUACIÓN DE LAS NUEVAS, y dos agujeros cerrados

Sesión de lectura completa del repo + visita a OEIS, y después tres entregas
**todo local** (Lean + Python, sin agentes — orden del usuario por presupuesto):

1. **`nuevasfusion.py` (fichero nuevo): las clases nuevas de `b(k)` tienen
   ECUACIÓN.** Una clase se estrena en el nivel `k+1` exactamente cuando
   `T^k(r)` y `T^k(r+1)` se encuentran **por primera vez en un vórtice**
   (`a = 3b+1`, paridades opuestas, `S` compensada en 1 — la regla del
   segundo padre del 221). Caracterización **con recíproco**, `k = 3…15`,
   0 fallos y 0 falsos positivos; reproduce `b(k)` término a término.
   **La pregunta de la razón 2 deja de ser un conteo ciego.** Precedente
   encontrado en OEIS: `A076227`/`A100982` tienen recursión exacta
   (Zarubin 2019, Winkler) vía los saltos de `Smin` — la continuación es
   derivar la recursión de `b(k)` contra esos saltos, que son las
   semiconvergentes de `log₂3` ya certificadas en `verificar_ciclos.py`.

2. **`franjaeverett.py` NO COMPILABA** (dos strings sin cerrar en las líneas
   542 y 589: texto adversarial del 01-08 pegado dentro de un `print`). **El
   fichero nunca había corrido en su forma actual.** Reparado y corrido
   entero, exit 0: la afirmación enterrada **se confirma contra su propia
   tabla** — `M = 5, 9, 101, 1001, 10001` empatan a 0 excepciones reales
   (hasta `10⁶`; los «sin certificar» son exactamente los impares `< M`), y
   con `M = 10001` el umbral baja a **1,585011**, a `4,8e-05` de `log₂3`.
   Detalle nuevo que la tabla regala: **`M = 27` tiene 2 excepciones
   reales** (14 sin certificar contra 12 impares `< 27`) — el único de la
   lista que no empata, y nadie sabe cuáles son ni por qué. Salida completa
   en `franjaeverett_salida.txt`.

3. **El hueco Lean↔Python de `atacacst` está cerrado.** `tramo_finito` sólo
   cubría `m > T^k(r)` y el `.py` decide con `m > T^k(r) − r`: la franja
   intermedia no tenía teorema. Nuevo **`tramo_finito_fino`** en
   `atacacst.lean` (tres líneas desde `palanca`, hipótesis sin resta
   truncada: `T^k(r) < r + m`), compilado, `#print axioms` limpio.

De OEIS: **`a(k)` y `b(k)` siguen sin estar** (consultadas hoy con los
términos correctos — la primera consulta usó colas mal recordadas y la cazó
la capa 1 — y control Fibonacci que devuelve `A000045`). El rincón está
vivo: comentario de jul-2026 en `A076227` (Hikawa: palabras binarias con
`2^m < 3^(suma parcial)`) y tres preprints 2026 sobre vectores de paridad.

## ⇢ Y EL PASO SIGUIENTE SE DIO LA MISMA SESIÓN: los vórtices, tabulados

Midiendo QUÉ vórtices producen las nuevas (`k = 3…15`) salieron dos cosas,
y la capa 1 las separó en el acto:

- **DEMOSTRADO — la familia extremal.** El `b` máximo de cada nivel es un
  **repunit ternario** (`13, 121, 1093, 9841, 88573, 797161 = (3^m−1)/2`,
  `m` impar) y el resto extremal es el par «casi todo unos»: **para todo
  `j` par, `(2^j−2, 2^j−1)` se funde por primera vez en el paso `j+2` con
  vórtice en `b = (3^{j−1}−1)/2`**. Demostración de cuatro líneas (está en
  la COMPROBACIÓN 5 de `nuevasfusion.py`), comprobada `j = 4…60`.
  **Corolario: `b(j+2) ≥ 1` para todo `j` par — las nuevas nunca se
  acaban.** Que ese `b` sea el máximo del nivel queda medido, no demostrado.
- **REFUTADO ANTES DE PUBLICARSE — «todo `b` es `1 mod 3`».** Vale hasta
  `k+1 = 14` y se rompe en `k+1 = 15` con `b = 2255 ≡ 2 (mod 3)`
  (`r = 16891`). Era muestra chica. Quedó anotado en el fichero para no
  rederivarlo.

`afirmaciones.db` regenerada: **84 afirmaciones** (las 4 de hoy: ecuación
de las nuevas, familia extremal, `tramo_finito_fino`, franja `M = 10001`)
y **33 correcciones** (la del fichero que no compilaba).

## ⇢ Y LA SEGUNDA VUELTA ENCONTRÓ LA FORMA DE LA RECURSIÓN: los estratos

Estratificando las nuevas por el número `|M|` de **pasos mixtos** (paridades
del par distintas ⟺ diferencia impar), comprobación 6 de `nuevasfusion.py`:

- **`|M|` es PAR siempre** (779 de 779; demostrable en tres líneas — `ΔS`
  cambia ±1 sólo en mixtos y vuelve a 0).
- **El estrato `|M| = 2` tiene EXACTAMENTE UNA clase por nivel, y es la
  familia del repunit** (verificado a mano en `(14,15)` y `(22,23)`).
  `|M| = 4` también exactamente una. Las dos unicidades: medidas, no
  demostradas.
- **Los estratos altos crecen como polinomios de grado creciente** (`|M|=6`
  termina con diferencias 5,6,7,8: cuadrático) y **entra un estrato nuevo
  cada dos niveles**. O sea: la razón `b(k+1)/b(k) → 2` vendría de la
  ENTRADA de estratos, no de que ninguno acelere — **el triángulo tipo
  Pascal que Zarubin encontró para `A076227`, ahora con candidato propio.**

## ⇢ Y LA PRIMERA FILA DEL TRIÁNGULO QUEDÓ DEMOSTRADA la misma noche

**TEOREMA (comprobación 7 de `nuevasfusion.py`): en cada nivel `k+1 ≥ 4`
hay EXACTAMENTE UNA clase nueva con `|M| = 2`** — `r = 2^{k−1}−2` si `k`
impar, `r = 3·2^{k−1}−2` si `k` par, alternando. Demostración en cuatro
piezas (está entera en el comentario): `|M| = 2` fuerza `r` par; la
diferencia pierde exactamente un factor 2 por paso compartido, luego
`v₂(r+2) = k−1` deja **solo dos candidatos**; el ganador cumple el
encuentro con la identidad `T(c·2^m − 1) = 3c·2^{m−1} − 1`; y el perdedor
falla siempre (su vórtice pediría `3^q − 1 = 3^{q+2} − 1`). Comprobado
hasta `k = 60`, más la unicidad completa por fuerza bruta en `k ≤ 15`.
**La primera fila del triángulo de estratos es `1, 1, 1, …` para siempre —
la primera pieza demostrada del mecanismo «la razón 2 viene de la entrada
de estratos».** `afirmaciones.db`: **86 afirmaciones, 47 demostradas.**

## ⇢ Y LA REDUCCIÓN ENTRE ESTRATOS, DEMOSTRADA: |M|=4 es un |M|=2 con preludio

La hipótesis «el estrato `|M| = 4` es el perdedor prolongado» **falló**
(capa 1, 12 de 12 en contra) — y lo que salió es mejor. El ganador de
`|M| = 4` es **el vecino izquierdo del perdedor** (`2^{k−1}−3` / 
`3·2^{k−1}−3`, con `r` IMPAR — justo el caso que `|M| = 2` excluía), con
mixtos siempre en `[0, 1, 2, k]`. Y al derivarlo salieron dos teoremas
(comprobación 8 de `nuevasfusion.py`, exit 0):

- **LEMA GENERAL**: para `C` impar con `C ≡ 3^q (mod 4)`, el par
  `(C·2^q−2, C·2^q−1)` se funde exactamente en el paso `q+2`, `S = q`,
  vórtice en `(3^{q−1}C−1)/2`. Los casos `C = 1, 3` son la alternancia
  del teorema de `|M| = 2`. Comprobado en ~2.000 pares (`C ≤ 201`,
  `q ≤ 40`).
- **FAMILIA `|M| = 4`**: los dos primeros pasos **contraen el par a
  consecutivo otra vez** (`d₂ = 1`), dejándolo en el lema con `C = 3c`,
  `q = k−3`. **Los estratos se reducen unos a otros** — `|M| = 4` es dos
  mixtos de preludio más un `|M| = 2` desplazado. *Esa reducción es la
  forma de la recursión del triángulo.* Comprobada `k = 4…60`. La
  unicidad de `|M| = 4` sigue **medida** (1 por nivel, `k ≤ 15`).

`afirmaciones.db`: **88 afirmaciones, 49 demostradas.**

## ⇢ EL MAPA DE DEPENDENCIAS ENTRA A LA BASE, con su regla (orden del usuario)

`afirmaciones.db` tiene ahora **dos tablas nuevas: `nodos` (14) y
`dependencias` (20 aristas)** — el árbol del programa de las nuevas, de
`definiciones` hasta `recursion_bk`. Y la **REGLA DEL AVANCE**, en código
(`COMPROBACION 0` del generador, corta con `SystemExit`): un nodo
`demostrado` no puede depender de un nodo no demostrado; nada trabajado
puede depender de un `pendiente`; y los pendientes se listan `AVANZABLE`
sólo con todos los padres demostrados. Hoy: `cuadratica_M6` y
`recursion_bk` están **BLOQUEADOS** — porque `unicidad_M4` sigue en
`medido`. La regla se aplicó a sí misma en el acto: el nodo
`M4_ruta_impar` no se registró como demostrado hasta que la comprobación 9
compiló y pasó.

## ⇢ Y LA RUTA IMPAR DE |M| = 4, DEMOSTRADA (comprobación 9)

- **`r` impar ⟹ pasos 0, 1, 2 mixtos** (`|M| ≥ 4` siempre) — el reverso
  exacto del teorema de `|M| = 2`. Exhaustivo `r < 2^14`.
- **La contracción es exacta**: con `r ≡ 1 (mod 4)`, el par vuelve a ser
  consecutivo en el paso 2, con menor `(3r+1)/4`.
- **Unicidad dentro de la ruta**: tras la contracción se aplica entero el
  argumento de `|M| = 2` — `v₂(s₂+2) = k−3`, rango `C ≤ 11`, necesidad
  `C ≡ 3^{k−3} (mod 4)`, y `r` entero exige `3 | C`: quedan `C ∈ {3, 9}`
  y el mod 4 elige **uno**. `k = 5…60`.
- *Capa 1 se cobró dos descuidos míos en el chequeo (no en la matemática):
  comparaba la contracción tras 3 pasos en vez de 2, y medía el exit del
  `grep` en vez del de python.*

`afirmaciones.db`: **89 afirmaciones, 50 demostradas, 14 nodos, 20
aristas.**

## ⇢ LA COORDENADA D — la herramienta nueva — y la ruta `r ≡ 3 (mod 4)` excluida

Al atacar la exclusión salió **la coordenada del programa entero**:
`D = g − 2s − 1` (gap menos dos veces el menor, menos uno). Tres hechos,
demostrados en el comentario de la comprobación 10:

- **el vórtice es exactamente `D = 0` con `s` impar** (con `s` par el
  mixto es β, que agranda el gap y no fusiona nunca);
- **en compartidos `D` es impar y evoluciona afín**: `(D−1)/2` o
  `(3D−1)/2`; el tramo termina cuando `D` se hace par, y el mixto que
  sigue es vórtice si y sólo si ese `D` es 0;
- **`D < 0` es invariante** — quien entra en negativo no vuelve.

Con eso: `r ≡ 3 (mod 8)` cae en `D₃ = −3` (par tras tres mixtos:
`{(3r+7)/8, +(3r−1)/4}`) y su cuarto mixto **nunca** es vórtice;
`r ≡ 7 (mod 8)` encadena cuatro mixtos seguidos. **EXCLUIDAS de
`|M| = 4`** (exhaustivo `r < 2^15` + seguimiento del tramo completo).
Junto con la comprobación 9: **la unicidad de `|M| = 4` está demostrada
para TODO `r` impar.** Falta sólo la ruta `r` par (medida, `k ≤ 15`) —
`unicidad_M4` sigue en `medido` y el mapa mantiene `cuadratica_M6`
BLOQUEADO. *La D convierte «se funden» en «D llega a 0», y los estratos
en la contabilidad de sus rebotes — ésa es la reformulación con la que
seguir.*

`afirmaciones.db`: **90 afirmaciones, 51 demostradas.**

## ⇢ LA COORDENADA E — autónoma de verdad — y la ruta par acorralada

Mejorando la D salió **`E = D − 3s`, que dentro de un tramo compartido
es un mapa 1-dimensional determinista**: su propia paridad elige su
regla (`E` impar → `(E−1)/2`, `E` par → `(3E−4)/2`), sin mirar los
valores. Con eso (comprobación 11, exit 0):

- **La órbita del rebote es forzada**: un par con `r` par arranca en
  `D = 1`, su primer mixto llega exactamente en `D = 0`, y si rebota
  (`s` par) entra en `E = 1` → `1, 0, −2, −5, −3` y el ciclo
  `(−2, −5, −3)` para siempre.
- **El vórtice directo del rebote es IMPOSIBLE**: exigiría
  `(E, s) = (−3, 1)` — el par `{1, 4}` — y la cadena hacia atrás,
  forzada por las paridades de la órbita, pide `(2·4−1)/3 = 7/3`. No es
  entero. *(Consistente con `|M|` par; la E lo re-demuestra por vía
  independiente.)*
- **El límite honesto, que es el `+1` reapareciendo**: en los pasos
  MIXTOS ni `D` ni `E` son autónomas — ahí entra el valor. Por eso el
  patrón `[0, rebote, m₃, vórtice]` de `r` par queda ABIERTO en general.
- **Acorralado con barrido dirigido** (pares sueltos, sin construir
  `buenas(k)`): entre las más de 300.000 fusiones con `S` igualada de
  pares `r` par `< 2^20`, **el estrato `|M| = 4` está VACÍO** — el
  diccionario salta de `|M|=2` a `|M|=6`. Y una perla medida: los
  `|M|=2` son exactamente `2^18` — la mitad exacta — huele a biyección
  de Terras, anotado sin demostrar.

`afirmaciones.db`: **91 afirmaciones, 52 demostradas.** `unicidad_M4`
sigue `medido` (solo falta el patrón de 4 mixtos con `r` par);
`cuadratica_M6` sigue BLOQUEADO.

## ⇢ EL TERCER MIXTO CLASIFICADO, Y EL CENSO DE LAS DIEZ FAMILIAS DE E

**Comprobación 12** — el tercer mixto de `r` par, clasificado entero con
`(D, E)` (dentro de un tramo el par es determinista y `s = (D−E)/3` se
recupera): **caso A** (`w` impar: mixto inmediato) cae en
`D' = −(3w+1)/2 − 1 < 0 → excluido, DEMOSTRADO`; **caso B-α** (tramo
rebotado terminando en `E ∈ {1, −5, −3}`) cae en `D' = D/2 − 3s − 2 < 0
→ excluido, DEMOSTRADO`. **La única puerta que le queda a un `|M| = 4`
con `r` par es la rama B-β** (`E ∈ {0, −2}`), abierta en general (árbol
2-ádico) y acorralada doble: ningún `(w, 6w+2)` con `w < 2^16` funde en
su segundo mixto, más el barrido real a `2^20`.

**Comprobación 13 — el censo, de la idea del usuario** (*«toda órbita
relevante de E pertenece a una de N familias»*): el mapa de `E` como
sistema propio sobre `Z` (`impar → (E−1)/2`, `par → (3E−4)/2`) **es de
tipo Collatz**, y su censo en `[−10⁵, 10⁵]` da **DIEZ familias** — fijos
`−1` y `4`, 2-ciclo `(−11)`, 3-ciclos `(−5)` (el del rebote, 47% de la
cuenca) y `(24)`, 5-ciclos `(−77)` y `(−59)`, 11-ciclo `(84)`, 27-ciclos
`(−4163)` y `(−5099)`. **Ninguna órbita escapa.** Aviso de alcance: censo
medido, no teorema — la completitud para todo `Z` es exactamente la
pregunta que en Collatz lleva 90 años abierta. El nodo nuevo
`clasificacion_rutas` (el salto propuesto) queda en el mapa, BLOQUEADO
hasta cerrar `unicidad_M4`.

`afirmaciones.db`: **93 afirmaciones, 53 demostradas, 17 nodos, 26
aristas.**

## ⇢ Y LA RAMA B-β, ITERADA EN EL MAPA (D, E) PURO HASTA u = 10⁷

El cuarto tramo es determinista en `(D, E)`, así que no hace falta
simular pares: comprobación 14 itera el mapa desde las dos familias de
arranque (`(15u+1, 12u+1)` y `(15u−2, 12u−2)`) para `u ≤ 10⁷` — **ninguna
de las 2·10⁷ órbitas termina en `D = 0`**. El acorralado pasa de `2^16`
estados a ~300× más lejos. En papel además: `E < 0` también es
absorbente (mismos mapas que `D`), y el vórtice exigiría pasar por
`(D, E) = (1, 1−3s)` con `s` par — el pre-vórtice tiene forma fija.
La rama sigue **abierta en general** (el árbol 2-ádico de paridades);
`unicidad_M4` continúa en `medido`.

## ⇢ EL VIRAJE (03-08-2026, decisión del usuario, con criterio propio validado)

El usuario preguntó: *«¿qué propiedad nueva tiene `H` que `D` y `E` no
tenían?»* — y la respuesta cerró la vía: **NINGUNA. `H = 2D − E = l − 1`,
el valor MAYOR del par menos 1** (dos líneas de álgebra; por eso sus
mapas eran «otro Collatz»: SON la trayectoria del grande). Corolario:
`D = l − 3s − 1`, `E = l − 6s − 1` — **el estado es 2-dimensional,
`(D, E)` lo genera, no existe tercera coordenada.** Registrado como
afirmación demostrada.

**Decisión:** B-β queda **CONGELADA como problema abierto interno** (era
otro Collatz dentro de Collatz; triple acorralado la respalda). El
programa vira a `clasificacion_rutas`. Dos arreglos honestos al mapa:
la arista `clasificacion_rutas ← unicidad_M4` sobraba (la clasificación
no la necesita), y la regla del avance decía «padres demostrados» donde
el usuario dictó «comprobada» — un censo nunca va a ser teorema y no por
eso bloquea lo que se apoya en él. Ahora: **`clasificacion_rutas` →
AVANZABLE**; `cuadratica_M6` y `recursion_bk` siguen en cola.

## ⇢ EL PASO 1 DE LA CLASIFICACIÓN, HECHO EN AUTONOMÍA (`itinerarios.py`)

*(Sesión con el usuario ausente — «elige las rutas tú misma». Ruta
elegida: el único nodo AVANZABLE del mapa.)* Fichero nuevo con tres
comprobaciones (cruce contra `b(k)` en los 13 niveles incluido), y el
resultado es una de cal y una de arena:

- **POSITIVO — la contracción, visible en las etiquetas**: el último
  tramo de todo `|M| = 4` vive en `{−5, −77, −4163}`, exactamente las
  familias que aparecen en `|M| = 2`. El teorema de la reducción entre
  estratos dejó huella medible.
- **NEGATIVO, y vale tanto como el positivo**: la familia ASINTÓTICA es
  un invariante ruidoso para contar — el tramo solo usa un prefijo
  finito de la órbita de `E`, y la familia mezcla información que el
  tramo nunca ve (conteos por itinerario erráticos, no polinómicos).
  Itinerarios distintos por estrato: 3, 9, 90, 243, 224, 76, 7.
- *Dos conjeturas de un minuto de vida, muertas por la capa 1: «solo
  aparecen familias negativas» (las positivas sí aparecen en estratos
  altos; solo falta el punto fijo `−1`, por cuenca trivial) — y el
  primer tanteo contaba TODAS las fundidas por un `ant = B1` que
  faltaba; lo cazó el cruce contra `b(k)`.*

`afirmaciones.db`: **95 afirmaciones.** Conteos del `CLAUDE.md`: **38**.

## ⇢ EL REINICIO UNIFORME, LA ECUACIÓN DE RENOVACIÓN — Y EL FANTASMA QUE CAZÓ

**TEOREMA DEL REINICIO UNIFORME (comprobación 16):** la contracción manda
`r = 4t+1` al par consecutivo **fresco** `(3t+1, 3t+2)`, y `t ↦ 3t+1` es
biyección de `Z/2^m` — **la autosimilitud del problema de fusión es
exacta**, `P(fusión | contracción) = f`. Y el `w` del rebote es uniforme
(Terras 1.2). Corolario: la **ecuación de renovación exacta**
`f = 1/4 + f/4 + g/4 + h/4`, con `f ≥ 1/3` demostrado en tres líneas.
Si `g` y `h` se calculan exactos al estilo Perras, **`f` queda decidida —
y `f = 1` sería la conjetura de Wu en densidad**: el pez gordo tiene
nombre y ecuación.

**Y LA ECUACIÓN TRABAJÓ DE DETECTOR EN SU PRIMER USO.** No cerraba
(`0,4039` contra `0,4453` medido), y perseguir la discrepancia destapó
**una familia fantasma**: el estado con `D = 0` es el par `{s, 3s+1}` y
su rebote real es **`(w, 9w+2)`** con `E = 3w+1` — no el `(w, 6w+2)` con
órbita `E = 1` de las comprobaciones 11 (corolario), 12 y 14. El error
nació de confundir el gap con el valor mayor, pasó tres comprobaciones
*porque solo miraban al fantasma*, y cayó cuando la ecuación no cerró
(con la familia real cierra: `0,4504`, y 8.191 rebotes de pares reales
caen todos en `(w, 9w+2)`). **Corregido todo**: comprobaciones 12 y 14
reescritas sobre la familia real (con el **teorema de paridad del
rebote**: `|M| = 3` no balancea `ΔS` ⟹ `r` par exige `|M| ≥ 4`), filas
de la base enmendadas, corrección nº 34 registrada con su lección:
*una ecuación de conservación que no cierra es un detector de premisas
falsas más fino que cualquier barrido — el barrido del fantasma pasaba
limpio porque medía al fantasma.*

`afirmaciones.db`: **97 afirmaciones, 56 demostradas, 34 correcciones.**
Medido con topes declarados: `f ≈ 0,445`, `g ≈ 0,188`, `h ≈ 0,173`.

## ⇢ EL CENSO DEL REBOTE Y EL LEMA DEL BALANCE: el sistema CIERRA en dos incógnitas

Paso 1 de la ruta de `RutaTeoremas.md`, ejecutado. **El censo de
reentradas del rebote real `(w, 9w+2)`** (`w < 2^15`, tope 600):
**cobertura 100%** — consec 45,4% (el **96% con `δ = 0`**), rebote 43,8%,
fusión desbalanceada 10,3%, fusión limpia 0,6%. Cero sin clasificar.

Y del análisis salió el **LEMA DEL BALANCE FORZADO** (comprobación 17,
demostrado en tres líneas desde Terras 1.2): toda fusión válida para una
clase residual ENTERA está S-balanceada — la igualdad de las dos formas
afines fuerza `3^{S_x} = 3^{S_y}`. **Corolarios:** (1) la fusión
desbalanceada tiene **medida 2-ádica CERO** (una solución esporádica por
clase — el fenómeno de cerca del atractor, otra vez); (2) las reentradas
consecutivas con `δ ≠ 0` tampoco pesan; (3) **el sistema de renovación
colapsa a DOS incógnitas** (`f` y `g`) más masas de clase calculables.
Cruce gratis: las clases fundidas mod `2^12` del verificador son
**1.476 = `a(12)` exacto**.

**El siguiente paso quedó afilado**: calcular las masas de clase del
censo de forma EXACTA (nivel a nivel, estilo Perras — cada salida del
censo es una unión de clases residuales decidida en pasos acotados) y con
la orientación canónica de las reentradas rebote (ojo: el signo de `δ` al
reentrar depende de qué lado quedó menor — el censo actual mide `δ` en
lados originales, hay que reorientarlo). Con esas masas, el sistema
lineal se resuelve y **`f` queda decidida**.

## ⇢ LA PRIMERA REVISIÓN EXTERNA DICTÓ (Opus 5) — Y LA IDENTIDAD EXACTA CIERRA

**Perras: no lo rompió** (A1–A5 aguantan). Tres agujeros de redacción,
cerrados en la sección 9 del `.txt`: el lema que faltaba (`r` impar ⟹
`|M| ≥ 3`, con demostración del revisor), la indexación paso/estado, y la
costura `N`/`Z₂` declarada. **Gatas: (a) aguanta; dos golpes que se
aplicaron**: (1) **Gao Guo-Gang 1993** (Discrete Math. 112) tiene el
levantamiento (su Lema 2) y la existencia de `f` (su Corolario 2, misma
letra `d_k`) — corrección nº 35, la base «elemental del repo» era de
1993; (2) **la sección 4 se retira como validación** — el «cierre»
0,4504/0,4453 comparaba dos estimaciones con el mismo sesgo de
truncamiento (Gao midió la densidad subiendo 0,310→0,512 entre 10² y
10⁸). *La lección del fantasma, un nivel más arriba.*

**Y LA VALIDACIÓN BUENA, PROPUESTA POR EL REVISOR, PASÓ ENTERA**
(`identidadexacta.py`): la partición vale como **igualdad de enteros**
en cada nivel —

> `a(k+2) = a(k) + (2^k − 1) + G(k) + H(k)` — EXACTA, `k = 3…14`,
> con la rama de la contracción dando `a(k)` clavado (12/12) y la
> ventana de Perras dando `2^k − 1` clavado (12/12).

Sin topes, sin Monte Carlo, sin sesgo. **`G` y `H` nacen como sucesiones
exactas** (`G: 0,0,0,0,1,5,16,44,110,259,588,1302`;
`H: 0,0,0,1,3,9,24,58,134,300,659,1426`) — las «`g` y `h` exactas» que
pedía la pregunta del día. Regalos verificados: la rama `h` se reduce a
`{w, 9w−1}` (casi espejo del rebote), y los contraejemplos de
Elia–Tucker viven **todos en `|M| = 8`** (la aserción ahora es tabla).
Pendientes del revisor que quedan: **conseguir LaTourette 2007** (riesgo
real para la novedad de Perras), leer Rozier y Frinkle et al. 2025 /
A277109, el test espejo `3n−1` del pipeline completo, y el chequeo de
rango (anti-tautología) antes de las sub-renovaciones. Conteos: **40**.

## ⇢ LAS MASAS DE CLASE, Y EL MURO CON NOMBRE (`masasdeclase.py`)

El paso siguiente ejecutado: la descomposición exacta de `g` y `h` en
masas de clase (enumeración mod `2^p`, `p = 8…16`, eventos de clase
F/C/B con dos testigos). **El sistema es exacto y las horquillas
rigurosas** — `f ∈ [0,4263, 1]` en `p = 16`, cota inferior subiendo,
horquilla conteniendo siempre el `f` medido (0,4453). **Y el muro,
honesto**: la masa indecisa decae ~2% por nivel — **el mismo muro de
convergencia lenta que la razón de `b(k)`, porque es la misma pregunta
escrita como sistema.** `a(32)/2^32 = 0,4357` sigue siendo la mejor cota
inferior. La vía que queda (anotada en el fichero): NO subir `p` — la
cola indecisa son «tramos largos antes de reentrar» y debería tener su
propia renovación; ésa es la conjetura de trabajo para la próxima
sesión. Jirafas quedó bautizado y con su `.txt` de revisión
(`teoremadejirafas.txt`). Conteos del `CLAUDE.md`: **39**.

## ⇢ LA VERIFICACIÓN BIBLIOGRÁFICA DE LOS DOS TEOREMAS (orden del usuario)

Leído entero **Elia–Tucker 2015** (arXiv:1511.09141, el PDF completo) y
barrida la web. Veredicto:

- **Perras cambia de etiqueta y GANA valor**: el patrón «primer 0
  seguido de 1» **es el stem `s_i` de Garner 1985**, que demostró la
  suficiencia (la mitad ⟸) y conjeturó la necesidad para TODA fusión —
  y Elia–Tucker la refutaron (3067/3068, el par que el repo ya conocía).
  **Lo que Perras añade y no está en ninguno de los dos**: la necesidad
  restringida al estrato mínimo (`|M| = 2 ⟺ stems`) es VERDADERA, y el
  conteo exacto `2^{m−1}` con el borde resuelto (Elia–Tucker solo
  midieron: «0,214% de contraejemplos bajo 5·10⁹»). **Perras = la
  conjetura de Garner, falsa en general, demostrada en el estrato mínimo
  con su densidad exacta.** Los contraejemplos de Elia–Tucker viven en
  estratos ≥ 4 — la estratificación es exactamente lo que reconcilia a
  Garner con sus contraejemplos.
- **El Reinicio Uniforme queda bautizado TEOREMA DE GATAS** (orden del
  usuario): no se encontró ecuación de renovación para coalescencia de
  consecutivos en la literatura; el único paper de distribución de
  coalescencia (arXiv:2005.09456) estudia pares `(n, 3n+2)`, es
  empírico y **está retirado por su autor**. Aviso de la casa: «no
  encontrado» no es «no existe».

## ⇢ EL TEOREMA DE LA MITAD EXACTA (comprobación 15) — el objetivo del /goal

La perla del `2^18` exacto **dejó de ser perla**:

> **TEOREMA.** Para `r` PAR, `(r, r+1)` se funde con `|M| = 2` si y sólo
> si en el vector de paridad de `s₁ = r/2` **el primer 0 va seguido de un
> 1**; y entre `s₁ ∈ [1, 2^m)` fusionan **exactamente `2^{m−1}`**, para
> todo `m ≥ 2`, sin casos.

Demostración entera en el comentario: con `D = 1`, el primer valor par
de la trayectoria de `s₁` baja `D` a 0; el vórtice pide `T^{j+1}(s₁)`
impar (el bit siguiente al primer 0); `ΔS = 0` es automático; y el
conteo cierra **incluido el borde** — de los dos residuos frontera funde
exactamente uno para cada `m`, según `3^m mod 4`. Equivalencia
exhaustiva `s₁ < 2^16`, conteos clavados `m = 2…16`. **Es la primera
MEDIDA exacta de una fila del triángulo** (el estrato 2 pesa 1/2 entre
los `r` pares — Terras 1.4, la moneda, actuando sobre dos bits), y el
caso `j = 0` es Garner 1985. `afirmaciones.db`: **96 afirmaciones, 55
demostradas.**

**Pendiente, en orden (el mapa manda):** (0) **el refinamiento del paso
1**: etiquetar los tramos por datos FINITOS (el `E` de arranque módulo
algo, el largo del tramo), no por el destino al infinito — ahí se decide
si el conteo por etiqueta es polinómico;
(2) `clasificacion_rutas`: qué familia de E toca cada ruta y dónde el
vórtice (`D = 0`) interrumpe la órbita — ahí los estratos dejan de
analizarse uno a uno; (3) `cuadratica_M6` vía esa clasificación; (4) las
2 excepciones de `M = 27`; (5) cobrar el `X₀ = 10⁹` con la `B(k)`.
Conteos del `CLAUDE.md` en 37. **Sin commit aún — todo junto cuando el
usuario diga.**

---

# ⇢ 02-08-2026 — LA DEPURACIÓN TOTAL DICTÓ: 100 de 100. EMPEZAR POR AQUÍ

**Encargo del usuario: verificar TODO `afirmaciones.db` (80 afirmaciones + 20
constantes) antes de publicar nada.** Los cuatro adversarios pendientes de la
entrada de abajo quedaron recogidos por el camino: la sesión de la mañana
(`429f4e04`) murió por límite de uso con la mega-tanda A en vuelo, y esta sesión
rescató todo de los journals — **el trabajo pagado no se pagó dos veces**.

## El marcador final

> **100/100 — 75 CONFIRMADAS · 13 CORREGIDAS · 12 NO_DECIDIBLES · 0 REFUTADAS.**
> Todo en `depuracion/veredictos.jsonl`, una fila por ítem con su evidencia.

## Cómo se pagó, porque el método cambió a mitad por orden del usuario

1. **Lotes 1–3 + mega-A: tríos completos** (Lean + Python a ciegas + comparador).
   ~9M tokens. El andamio de Terras, fusión, pinza, pisos, Garner/Wu, espejos,
   negativos — la parte donde la independencia importaba.
2. **El resto: pasada LOCAL a coste ~cero** — los `verificar_*.py` del repo
   (11 scripts, exit 0 todos), los 4 `.lean` recompilados (0 `sorryAx`), y un
   consolidado propio escrito de cero (`depuracion/pasada_local/`). *«El código
   tiene oráculo»: para mediciones, ejecutar ES verificar.*

## Lo que encontró que no se sabía

- **`A65`, y es un off-by-one publicado: el espejo base 10 tiene 44.451
  dos-ciclos bajo 100.000, no 44.450.** Cerrado con combinatoria, no medido:
  (90.000 reversibles − 1.098 palíndromos)/2 = 44.451.
- **`A71`**: la tupla de 176 en `722.067.240` se confirma entera; su
  **maximalidad** bajo `2^30` nadie la re-verificó — es de Wu, y así queda dicho.
- **`A29`**: «sube k veces seguidas» es del ATAJO (el clásico lo rompe en `k=2`),
  y `2^4000 − 1` da **4.000** impares seguidos, no 3.999.
- **`A51` re-verificado EXACTO**: desviación **0,0** prediciendo el bit siguiente
  sobre los 2^13 residuos completos — la biyección lo fuerza. *(El primer intento
  propio contaminaba con la cola post-convergencia; lo cazó la capa 1.)*
- Y las 11 corregidas de los tríos (A2/A3/A5 bordes `n=1`, A27 `k=0`, A28
  biyección a teorema, A34 asintótico vs régimen, A11/A13/A16/A63…).

## Los 12 NO_DECIDIBLES, por clase

- **bibliográficas** (Tao A37, 5x+1 A39, Barina `2^71` A66, Wang A64): se citan,
  no se re-demuestran aquí.
- **coral** (A44, A72, A73, A74 y C20): barrido caro prohibido — pendiente de
  una pasada CPU dedicada.
- **irreproducibles** (A52 sin nulo registrado, A54 la esfera borrada, A43 sin
  tendencia limpia): del pasivo «números sin código», y así quedan marcados.

## LO QUE QUEDA, en orden

1. ⇢ **HECHO la misma noche: las 13 correcciones aplicadas** al generador, la
   base regenerada y el `CLAUDE.md` (commit `96ee1fc`).
2. La pasada CPU del coral (barata en tokens, cara en horas de máquina).
3. `guardarrespuestas.py` + zip de transcripciones al cerrar esta sesión.

## ⇢ Y EL ATAQUE A CST ARRANCÓ, la misma noche, todo local

**`atacacst.py` + `atacacst.lean`** (encargo del usuario: atacar con Lean y
Python, sin agentes). La palanca: en cada clase `r mod 2^k` donde el
coeficiente cae, el fallo de CST sólo puede vivir en `m ≤ T^k(r) − r` — **un
tramo finito por clase, y eso está DEMOSTRADO en Lean para todo `k, r, m`**
(`palanca`, `tramo_finito`; núcleo, sin Mathlib, sin `sorryAx`, compiló a la
primera).

**Resultado:** CST decidida **para todo `n ≥ 2` con `σ* ≤ 27`** — incluido el
jump value `k = 27` — autocontenido, sin `X₀` importado. Complementa el corte
`σ* ≤ 16.294` de `paradacoef.py`, que sí depende del barrido a `2·10⁷`.

**Y el hallazgo que deja una pregunta afilada: el tramo estuvo VACÍO las 27
veces** (`T^k(r) ≤ r` en toda clase caída, con las únicas igualdades en
`r ∈ {0, 1}`). Si eso fuera teorema para todo `k`, **CST entera caería**.

> **⇢ CORRECCIÓN DE PUNTERÍA, la misma noche (capa 1 sobre esta bitácora).**
> Aquí decía que la continuación era el jump value `k = 46` por enumeración
> dirigida. **Mal apuntado, por dos motivos.** (1) «Tramo vacío en la clase de
> `r`» es EQUIVALENTE a «CST se cumple en el representante `r`» — no es un
> milagro aparte, es CST en los números chicos, reformulada. (2) La propia
> palanca implica que una clase con tramo abierto exige `r ≤ B(k)`, y
> `paradacoef.py` ya demostró `B(k) ≤ 2·10⁷` para **todo `k ≤ 16.294`** con su
> barrido propio — así que `k = 46` (y el 65, y el 149…) **ya estaban
> decididos**. La frontera real es **`k = 16.295`**, donde `B(k)` rebasa por
> primera vez el barrido de `2·10⁷`.
>
> **La continuación buena: subir `X₀` (el barrido directo `σ = σ*`), que es
> CPU pura y cero tokens, y dejar que el corte se corra solo por la curva
> `B(k)`.** La misma noche: **`10⁸` en 2 minutos y `10⁹` en ~18 — 0
> diferencias en los dos** (`atacacst2.py`, resultados en
> `atacacst2_progreso*.txt`). `X₀` queda **50×** por encima del `2·10⁷` de
> `paradacoef.py`. La conversión `X₀ → K nuevo` con la maquinaria `B(k)`
> queda para la sesión siguiente; a este ritmo, `10¹⁰` sería una noche de
> CPU si hiciera falta.

---

# ⇢ CIERRE DEL 01-08-2026 (noche) — LOS DOS TRÍOS DICTARON. EMPEZAR POR AQUÍ

> ## ⚠ LO PRIMERO AL VOLVER: HAY CUATRO ADVERSARIOS SIN RECOGER
>
> Se lanzaron al final de la sesión, sobre el repo **ya commiteado y pusheado en
> `5f4db09`**, y la sesión se cerró antes de que dictaran. **Sus veredictos no
> están aplicados.** Es el mismo caso del comparador que se perdió el 01-08 por
> la tarde, así que esta vez queda escrito qué se les pidió:
>
> | lente | encargo |
> |---|---|
> | **contradicciones internas** | buscar qué de lo escrito hoy contradice algo viejo que no se tocó. El fallo tiene historial: *«cuando se corrija algo, hay que buscar dónde más se afirmaba»* |
> | **prosa contra código** | coger afirmaciones con número del `CLAUDE.md`, ejecutar el fichero del que dicen venir, y ver si cuadran. Y listar las que **ya no son reproducibles** porque su fichero murió en la purga |
> | **romper lo de hoy** | atacar los tres bloques nuevos: el vuelco sobre OEIS, el veredicto del tipo `ℕ`, y lo que se dio por cerrado. En particular si *«ningún invariante mod `2^k` distingue los dos mapas»* está demasiado fuerte |
> | **ficheros sin auditar** | `espejoak.*`, `pruebaresta.lean`, `cotatramos3n1.*`, `paradacoef.py`, `franjaeverett.py`, `medidamonotona.py`, `auditarrefutaciones.py` y otra pasada a `verificar_terras.py`, que ya tuvo un bug |
>
> **Si no dejaron nada, hay que relanzarlos.** Y el aviso de método, que ya va
> por la segunda vez hoy: **un veredicto que no se aplica antes de cerrar, se
> pierde.**
>
> ### ⇢ EL PRIMERO SÍ DICTÓ, y trajo 25 hallazgos
>
> **El de contradicciones internas entregó: 7 graves, 10 medianos, 8 erratas.**
> Aplicados los 7 graves y 9 más. **Su hallazgo estructural explica casi todos:
> la sección «Lo que queda pendiente» de este fichero era un FÓSIL anterior al
> 30-07** — sin fecha, así que se leía como viva, y sobrevivió a la purga, a las
> dos auditorías y a los dos tríos sin que nadie la tocara. Siete de sus puntos
> mandaban trabajo ya hecho, ya refutado, o sobre ficheros borrados.
>
> **Lo que dejó sin aplicar, para mañana** (nada de esto cambia una decisión):
>
> | # | qué |
> |---|---|
> | 13 | `CLAUDE.md` cita *«la tabla de ángulos de arriba»* y sus cifras `0,003% vs 97%`: **esa tabla se borró con `coralcollaz.py`** |
> | 18 | esta bitácora dice *«80 · 22 · 20»* en la entrada de la tarde — era cierto entonces, hoy son **32** correcciones; conviene marcarlo, no reescribirlo |
> | 24 | en la tabla del 30-07, *«la causa es `45 = 3²·5`»* sigue sin marca de que `coralprimos.py` la refutó |
> | 25 | el `0,5186` de la densidad viene de `densidadfusion.py`, **retirado por ser un promedio muestreado** |
>
> ### ⇢ LOS CUATRO DICTARON. Y lo que hay que leer es el veredicto del cuarto
>
> **Los cuatro encontraron algo. Pero el que auditó prosa contra código, que era
> el que podía tumbar el repo, dijo esto:**
>
> > *«**El núcleo duro aguanta.** Las cinco cosas que sostienen decisiones —la
> > cota de ciclo con `X₀ = 2^71`, la sucesión `a(k)`, el criterio de fusión, el
> > piso de la altitud y la cota `B(k)` de CST— las derivé desde cero y **salen
> > clavadas**, incluida la coincidencia fina de que **16.294 es exactamente** el
> > corte que permite `X₀ = 2·10⁷`.»*
>
> **Verificó 24 afirmaciones con implementación propia y 24 cuadraron.** Lo que
> falla es de un solo tipo, y el repo ya le puso nombre: **un número publicado
> sin su rango.**
>
> **Aplicado:** la razón de la fila `k=23` era la del escalón de abajo
> (**1,9069**, no 1,8973); los vórtices del 221 son **51** aritméticos y el 50
> venía de una decisión de dibujo de un fichero borrado; CST está verificada a
> **2·10⁷**, no a `2·10⁶` —y de ese rango sale el corte `σ* ≤ 16.294`—; tres
> etiquetas decían **10⁷** y eran **10⁶**; el `0,5837` del piso es el valor a
> 200.000 y las *«once veces»* son **nueve**; el `0,5186` estaba declarado
> retirado en un párrafo y usado como dato vivo en el siguiente. Y en código:
> `franjaeverett.py` publicaba *«el óptimo está en M = 9»* **contra su propia
> tabla** (contando excepciones reales, `M = 5, 9, 101, 1001, 10001` empatan a
> cero, y el umbral baja a **1,585011**, no a 1,63763); y `verificar_terras.py`
> titulaba *«comprobado y no supuesto»* una sección **cuya mitad es un
> supuesto** — el fichero que ya tuvo un bug ahí.
>
> **PENDIENTE REAL, y es el pasivo de fondo: ONCE NÚMEROS siguen presentados
> como medidos sin código detrás**, y sólo uno (`3,49031`) lleva la marca. Están
> listados en el informe del adversario. *El peor no es el más grande: es
> «correlación latitud / `log₂(valor)` = 0,12», que **no es reproducible ni en
> principio** porque «latitud» era una coordenada de un dibujo que ya no existe.*
>
> Y lo que dejaron los otros dos, sin aplicar: `medidamonotona.py` cuenta 5
> codominios bien ordenados y son 7, etiqueta como «acotadas» tres candidatas
> que no lo están, y dice que «el precio crece con `k`» cuando su tabla baja en
> 4 de 7 escalones; `paradacoef.py` tiene un `if` que es la misma desigualdad que
> su `while` (dos verificaciones donde hay una) y una fila del A/B con **cero
> instancias medidas**; `auditarrefutaciones.py` arrastra un `243` heredado
> cuando él mismo calcula `240`, y su tabla del #54 muestra que **todo `N` primo
> adelanta 0** sin que el veredicto lo use — que es el resto vivo de la
> predicción del número primo de rumbos.
>
> ### Lo que SÍ quedó comprobado antes de cerrar
>
> - **Batería mecánica sobre el repo entero: 0 fallos.** 34 `.py` parsean, 0
>   hallazgos cp1252, los conteos cuadran, las tres bases con
>   `integrity_check = ok`, 0 filas apuntando a ficheros inexistentes, los 4 zips
>   abren, y los números que viven en varios sitios coinciden.
> - **EL REPO SOBREVIVE A UN CLON LIMPIO**, y es la primera vez que se comprueba.
>   Clonado desde GitHub a un directorio nuevo: **54 ficheros, ninguna diferencia
>   con el local**, y **11 de 11 scripts baratos corren** más la CLI
>   (`main.py camino 27` → 111 pasos, techo 9.232). *Es justo lo que le faltó a
>   `lecturas/*.pdf` y al toolchain de Lean.*
> - **La única excepción, y es por diseño:** `guardarrespuestas.py` **no puede
>   correr desde un clon en otra ruta**. Deduce el slug del directorio actual, y
>   las transcripciones viven donde Claude Code las escribió, indexadas por la
>   ruta original. Falla con un mensaje claro que dice qué cambiar. **No es un
>   bug, es una atadura a la máquina** — y por eso existe `transcripciones/`.

Sesión de **corregir**, no de medir. Salió una cosa que no se buscaba: **dos de
las correcciones eran el error**, y las dos enterraban algo bueno.

## Lo que cambia decisiones

1. **LEAN NO ESTABA INSTALADO.** El `CLAUDE.md` decía *«instalado el
   01-08-2026»* y `~/.elan` **no existía**. Reinstalado (4.32.2). Los **cuatro**
   `.lean` compilan a **0 errores / 0 `sorryAx`**. *Se perdió el verificador del
   único fichero con categoría de «demostrado»: los `.lean` están en git, el
   toolchain no.* **Regla nueva: `lean --version` al abrir.**

2. **El trío del `3n−1`: la frase del `CLAUDE.md` era FALSA.** *«Para `3n−1` la
   `C` es negativa **y el tipo `ℕ` ya no sirve**»*. Las dos mitades no se
   contradecían — **el error era el «luego»**, un *non sequitur*. Y los dos
   agentes **nunca discreparon**: sus `C` son opuestas (`C_lean = −C_python`).
   El comparador refutó también al **agente de Lean**, compilando él mismo la
   forma con resta. Queda en `pruebaresta.lean`.

3. **El trío de `a(k)`: es TEOREMA, y el motivo de retirar el envío a OEIS se
   cae.** `a₊(k) = a₋(k)` para **todo `k`**, demostrado en Lean sin Mathlib. La
   biyección es `2^k − 1 − r`. **La bitácora la tenía archivada como fallida por
   un `±1`** (decía `2^k−2−r`). Y el resultado es más ancho: `n ↦ −n` es un
   automorfismo de `Z/2^k`, luego **ningún invariante mod `2^k` distingue los dos
   mapas** — control que lo remata: **`A076227`, que SÍ está en OEIS, también
   sale idéntica**. El A/B contra `3n−1` no era un control para esto.

## Lo que se cerró sin gastar máquina

- **El pendiente «llegar a `k ≥ 20` y decidir si es teorema o se rompe»: cerrado
  a favor de teorema.** Iba a costar horas de CPU y costó una demostración.
- **Los conteos, por tercera vez.** 28 → **34** `.py`, 26 → **32** con
  `SystemExit`, cinco → **seis** `sqlite3`, siete → **ocho** `secuencia_de`, y
  **seis ficheros** que no tenían fila en la tabla. Barrido cp1252: 0 hallazgos.
- **`afirmaciones.db` iba una auditoría por detrás**: siete afirmaciones que el
  documento ya había refutado, y **20 filas** apuntando a ficheros borrados (yo
  había contado 9). Base regenerada: **80 · 32 · 20**.
- **`respuestas.db`**: 701 mensajes, 7 sesiones. **355 mensajes ya sólo viven
  ahí** — tres transcripciones desaparecieron del disco en menos de tres días.
  Nuevo: **`transcripciones/`**, un `.zip` por sesión, dentro del repo.

## La lección, y es la misma tres veces

> **Auditar una refutación encuentra tanto como auditar una afirmación.**

Pasó con la biyección `2^k−2−r` (un `±1` enterró un teorema), con el motivo de
la retirada de OEIS (un control que no controlaba), y con la explicación del
agente de Lean (conclusión correcta, razón falsa). **Y las tres se cazaron
compilando o ejecutando, no opinando.**

## Lo que queda abierto

- **`espejoak.lean` dice «para todo `k`» y tiene un tramo decidido sólo hasta
  `k = 7`**: Terras y el borde están demostrados para `T₊`, no para `T₋`. Es
  cierto y sale en tres líneas, pero **hoy no está demostrado**.
- La pregunta grande de siempre: la razón `b(k)/b(k−1)`, ¿converge por debajo de
  2 o llega a 2? Sigue sin decidirse; `k = 34` no la decidiría tampoco.
- **La independencia de los agentes hay que protegerla al lanzar.** El
  `CLAUDE.md` se les inyecta entero y ya contiene medio argumento. Dos tríos, dos
  contaminaciones — una declarada y otra no.

---

# ⇢ ESTADO AL CIERRE DEL 01-08-2026 (tarde) — lo anterior

*(Escrito con dos workflows todavía corriendo, por si la sesión se cierra antes
de que terminen. Si estás leyendo esto en una sesión nueva: lo primero es
comprobar si dejaron sus ficheros.)*

## ⇢ LO MÁS NUEVO: LEAN 4 ENTRA AL REPO, Y CON ÉL LA REGLA DE LOS TRES

**`cotatramos.lean`** (commit `3b3c6c2`) **demuestra** lo que `cotatramos.py`
mide: la identidad de Terras, la cota `3^A·n₀ ≤ 2^B·n_k` y el corolario, **para
todo `n₀` y todo `k`**, sin Mathlib, comprobado en 1,8 s. `#print axioms` sale
limpio (**no hay `sorryAx`**), y el 221 está verificado por el **núcleo** —
`A = 41, B = 73`, cruzado además contra Python sin compartir una línea.
*Fue el primero; al cerrar el día ya son cuatro.*

**Y el procedimiento que manda desde ahora, dictado por el usuario:**

> **Toda comprobación aritmética o matemática va por TRES agentes:** uno la
> demuestra en **Lean**, otro la calcula **por su cuenta sin ver el primero**, y
> un tercero **compara los dos**. Detalle completo en `CLAUDE.md` →
> *LA REGLA DE LOS TRES*.

**El matiz que hay que conservar, porque es fácil inflarlo:** Lean caza **unas
13 de las 32** correcciones que este repo tiene registradas — **menos de la
mitad**. No caza muestras tomadas por constante, estimadores ni citas. Lo que sí
caza es **la clase que este repo repite**: hipótesis que faltan (cuatro veces) y
confusión de mapas (tres). *Y salió un extra: al formalizar, la hipótesis
`0 < n₀` del corolario resultó **sobrar**. Primera vez que se quita una en vez
de descubrir que faltaba.*

### ⇢ EL PRIMER TRÍO YA ESTÁ LANZADO: el control A/B del `3n−1`

**Estrena la regla con algo cuyo resultado ya sospechamos**, que es la manera
barata de saber si el trío funciona antes de gastarlo en algo caro.

| agente | crea | estado |
|---|---|---|
| **1 · LEAN** | `cotatramos3n1.lean` | **ENTREGADO.** Compila sin Mathlib, sin `sorry`, 4 invocaciones y 0 fallidas |
| **2 · INDEPENDIENTE** | `cotatramos3n1.py` | **ENTREGADO.** 307.807 pares, 0 fallos, 0,63 s |
| **3 · COMPARADOR** | — | **CORRIENDO AL CERRAR LA SESIÓN.** Su veredicto es lo primero que hay que recuperar |

**A los dos se les dio el MISMO enunciado y NO se les dio la identidad** — cada
uno tuvo que derivar la forma de `C` por su lado, o la comparación no mediría
nada. Los dos ficheros están **commiteados pero sin veredicto**: no los cites
como verificados hasta que el comparador dicte.

### ⚠ LO QUE HAY QUE MIRAR PRIMERO AL VOLVER: una frase mía puede estar mal

**Los dos coinciden en (II), (III) y en la discriminación.** Pero sobre la
pregunta del tipo dicen cosas distintas, y **una de ellas contradice lo que yo
escribí en `CLAUDE.md` unas horas antes**:

| | qué dice |
|---|---|
| **yo, en `CLAUDE.md`** | *«para `3n−1` la `C` es negativa y **el tipo `ℕ` ya no sirve**»* |
| **agente 1 (Lean)** | **NO hizo falta `ℤ`.** El problema no es el tipo sino **dónde se pone la `C`**: con `2^B·n_k + C = 3^A·n₀` no hay resta y la inducción cierra sola |
| **agente 2 (Python)** | lo que cambia es **el signo de `C`** (`C ≤ 0`), y la desigualdad lo arrastra |

> ⇢ **RESUELTO (01-08-2026, noche). La frase era FALSA: `ℕ` basta.** Pero
> **ninguno de los dos agentes tenía razón del todo.** El comparador compiló él
> mismo la forma con resta, sobre estado arbitrario y **sin invariante
> reforzado**, y con eso refutó también la explicación del agente de Lean: poner
> la `C` al otro lado es **más cómodo, no necesario**. *Su conclusión quedó
> reforzada; su razón, corregida.* La compilación que lo decidió está en
> **`pruebaresta.lean`**, y el párrafo del `CLAUDE.md` está reescrito.

**Dos cosas más que dejaron los agentes y que el comparador tiene encargadas:**

- El corolario **no se traduce cambiando una palabra**: en `3n−1`, *«baja ⟹
  `2^B > 3^A`»* es **falso** (`n₀ = 2 → 1`, `A=2, B=3`, o sea `8 ≤ 9`; 2.023
  casos). El que vale es *«**sube** ⟹ `2^B < 3^A`»*.
- El agente 2 **confesó un riesgo de contaminación**: leyó `cotatramos.py` como
  plantilla, y ese fichero trae un cruce parcial sobre `3n−1`. *Que lo declarara
  él solo es exactamente lo que la regla busca.*

### LO QUE SE SACÓ EN LIMPIO, y es poco pero es duro

1. **`cotatramos.lean` — lo único DEMOSTRADO del repo.** La identidad de Terras,
   la cota y el corolario, para todo `n₀` y todo `k`. `#print axioms` sin
   `sorryAx`. **No es «0 fallos en 329.400 pares»: es todos.**
2. **Lean instalado y con su regla de uso escrita**, incluida la parte incómoda:
   caza **unas 13 de 32** correcciones, menos de la mitad. Lo que caza es la
   clase que este repo repite.
3. **LA REGLA DE LOS TRES**, y con ella la REGLA CERO pasa a tres capas.
4. **La auditoría de las diez refutaciones** (`eea5a8d`): 8 confirmada, 2
   exagerada, **0 refutada**. Y el adversarial encontró cuatro defectos **en la
   auditoría**, mejores que los que la auditoría encontró.
5. **Las tres vías cerradas** (`wzu334m64`, 7 agentes): CST sigue viva y es la
   mejor; franja y monótona se cierran **con su razón escrita**; y las tres
   midieron **`A076227` sin darse cuenta**, cruzada por accidente con 0
   discrepancias entre tres implementaciones.

### PUNTOS A FAVOR, al día

| pieza | categoría | estado |
|---|---|---|
| **la cota por tramo** `3^A·n₀ ≤ 2^B·n_k` | **teorema** | **demostrado en Lean**, todo `n₀`, todo `k` |
| el corolario «baja ⟹ `2^B > 3^A`» | **teorema** | **demostrado en Lean** |
| el piso de la altitud | cota | 0 fallos; enunciado afinado dos veces |
| el criterio de fusión (43,57%) | cota | exacto hasta `k = 32`, sin muestreo |
| la pinza de ciclos | rederivación | verificada; **vía cerrada a propósito** |
| **CST: «no hay contraejemplo con `σ* ≤ 16.294`, para todo `x`»** | **cota** | del workflow, **sin aplicar aún** |
| `A076227` | dato | **cruzada por tres implementaciones independientes** |

### PENDIENTES, en orden

1. ⇢ **HECHO (01-08-2026, noche). El comparador dictó: la frase era FALSA.**
   `ℕ` basta, y no por lo que decía el agente de Lean — el comparador compiló él
   mismo la forma con resta (`pruebaresta.lean`) y refutó también su
   explicación. Los dos agentes nunca se contradijeron: sus `C` son opuestas.
2. **Aplicar la auditoría de las diez** al `CLAUDE.md`: las dos EXAGERADAS, los
   cuatro defectos del adversarial (re-tecleo presentado como reimplementación,
   dos tautologías con recuento, una sensibilidad mal medida, y el `5,86x` que es
   una **elección de unidad** blindada con un `SystemExit` — verificación
   circular cometida por el auditor).
3. **Aplicar las tres vías** al `CLAUDE.md`: las dos correcciones obligatorias de
   CST, y las razones por las que franja y monótona se cierran.
4. **Commitear `medidamonotona.py`** si el workflow no lo dejó.
5. ⇢ **CERRADO (01-08-2026, noche): ES TEOREMA, y no hizo falta llegar a
   `k ≥ 20`.** `a₊(k) = a₋(k)` para todo `k`, demostrado en Lean; la biyección es
   `2^k − 1 − r` (la que aquí figuraba como *«no se pudo confirmar»* estaba
   corrida por uno). **Y con eso se cae el motivo que mató el borrador de OEIS**:
   `n ↦ −n` es un automorfismo de `Z/2^k`, así que ningún invariante mod `2^k`
   separa los dos mapas — **`A076227`, que está en OEIS, tampoco los separa**.
6. **El control A/B en Lean para el resto de piezas** — ahora que hay trío, es
   barato.
7. **Nueve de los diez bloques de la búsqueda web siguen sin código propio.**

### LA LECCIÓN DEL DÍA, que se repitió tres veces

**Auditar una refutación encuentra tanto como auditar una afirmación.** Pasó con
las diez del bloque E (dos exageradas), pasó con el adversarial que auditó a esa
auditoría (cuatro defectos más), y pasó **conmigo**: la frase del tipo `ℕ` la
escribí el mismo día en que documentaba que no se escriben frases así.

> *Una corrección suena a rigor, y por eso nadie la revisa.*

## 1. LA PURGA, hecha (commit `4f8efdc`)

El repo pasó de **43 a 28 `.py`**, de 16 programas que dibujan a **4**, y el
`CLAUDE.md` perdió **616 líneas (18,5%)**. Total: **−7.106 líneas.**

Lo borrado no estaba mal calculado: **medía la esfera, el ángulo o el módulo
elegidos a mano, no Collatz.** Fuera `collazcirculo`, `collazcruce`,
`mallabasica`, `mallacollaz`, `maquinitacollaz`, `collazejecucion`, `viz3d`,
`coralcollaz`, `cruzarestos`, `collazarbol`, `mallaespejo`, `mallaespejo2`,
`espejobases`, `densidadfusion`, `guardarmallas`, `collazlamina`, las 12 mallas
`.json`, `oeis_borrador.txt`, las notas a mano, y los `.html`/`.png`.

**Dos cosas se rescataron, y las dos importan:**

- **`cotatramos.py`** — el cálculo que `collazlamina.py` hacía antes de dibujar.
  De `C ≥ 0` en la identidad de Terras salen dos desigualdades:
  `2^B·seq[j] ≥ 3^A·seq[i]` para todo par, y **si un tramo baja entonces
  `2^B > 3^A`**. Verificadas sobre **prefijos que nunca tocan el 1** (329.400
  pares, 252.014 tramos descendentes, 0 fallos), o sea que **no asumen
  convergencia**. Y el control A/B discrimina: sobre `3n−1` la `C` es negativa y
  la desigualdad se invierte. *Convierte «el balance decide todo» de promedio
  sobre trayectorias en **cota por tramo**.*
- **`mallascerradas.py` se salvó.** El auditor lo acusaba de no discriminar. Se
  corrió el A/B que nunca se había corrido —los seis restos mod 6— y **sólo el
  resto 4 sale con 0 fallos en las dos ruedas**. La refutación era falsa.

`matplotlib` **se queda** en `requirements.txt` aunque ahora no lo importe nadie:
decisión del usuario, tarde o temprano hará falta.

## 2. LO QUE ESTABA CORRIENDO AL CERRAR

Los dos tienen **conjuntos de ficheros disjuntos** y **prohibido tocar
`CLAUDE.md` y `bitacora.md`** — la documentación se aplica después, a mano.

| workflow | crea | qué busca | estado |
|---|---|---|---|
| **`wzu334m64`** — las tres vías | `paradacoef.py`, `franjaeverett.py`, `medidamonotona.py` | CST, la franja `log₂(10/9)`, y una cantidad monótona | **corriendo**; ya dejó `2884b3d` (franja) y `c9b0bca` (CST) |
| **`wyefzghui`** — auditar refutaciones | `auditarrefutaciones.py` | las diez correcciones del bloque E, con adversario | **TERMINADO**, commit `eea5a8d` |

**Si esos ficheros existen, los workflows llegaron a commitear. Si no, se
perdieron y hay que relanzarlos** — los guiones quedan en el directorio de
workflows de la sesión.

**Resultado del que terminó (`wyefzghui`), en una línea: 8 CONFIRMADA, 2
EXAGERADA, 0 REFUTADA** — no hay nada que rescatar, las diez apuntaban al sitio
correcto, pero dos se sostenían con un número que no pasa el filtro que ellas
mismas exigen. *La regla que sale: **una refutación se publica con el mismo rigor
que una afirmación** — con su rango y sus cifras significativas.* El adversarial
además encontró fallos en la propia auditoría. **Está sin leer entera.**

### Las tres vías, en una línea cada una

- **CST** (`σ*(x) = min{k : 2^k > 3^{m_k}}` contra `σ(x)`). Es la **única** de las
  tres que da un criterio evaluable **antes** de terminar la trayectoria, porque
  `σ*` se calcula sólo del vector de paridad, o sea sólo de `n mod 2^k`. Si
  `σ* = σ`, **no hay ciclos** y el tiempo de parada queda descrito por clases.
  **El control que decide si sirve: medirla sobre `3n−1`.**
- **La franja `log₂(10/9) = 0,152`.** Everett certifica descenso desde
  `B/A > 1,73697`; el equilibrio está en `1,58496`. Los 24 números de 3 a 20.000
  que no certifica caen los 24 dentro, y el más chico es el **27**. La idea a
  probar: afinando la cota `5/3` a `(3M+1)/(2M)` el umbral **baja hacia
  `log₂3`** — pero condicionar a `m ≥ M` sólo vale en el prefijo. **Si queda un
  núcleo que resiste a todo `M`, ese núcleo es el resultado.**
- **La cantidad monótona.** No se espera encontrarla —el `+1` rompe toda medida
  que se porte bien con `n/2` y con `3n`—; **el objetivo es medir CÓMO fallan**.
  Una `Q` que decrece salvo en un conjunto describible es una demostración con un
  agujero localizado. Variante con más posibilidades: que decrezca **en todo
  tramo de `k` pasos** para algún `k` fijo, que basta igual.

## 3. LO QUE HAY QUE HACER CUANDO CIERREN

1. Aplicar al `CLAUDE.md` lo que salga de las dos pasadas.
2. **La cola de la purga**: ~50 menciones sueltas a ficheros borrados y una
   docena de conteos viejos en secciones que no se tocaron. Mecánico, a un agente.

## 4. LOS PENDIENTES DE FONDO, por orden

1. **`a(k)` es idéntica para `3n+1` y `3n−1`** (verificado `k = 3…13`). Falta
   llegar a `k ≥ 20` y decidir si es **teorema** o se rompe. Es lo único que
   puede tumbar o salvar lo que el repo tenía por mejor resultado, y es barato.
2. **Nueve de los diez bloques de la búsqueda web siguen sin código propio**:
   Böhm–Sontacchi, Bernstein–Lagarias, Monks 2006, Krasikov–Lagarias `x^0,84`,
   Applegate–Lagarias, Steiner 1977, la reducción mod 4, y el paper de Fibonacci
   de 2026. *(El bloque 1, CST, es la vía que está corriendo.)*
3. **El hueco de densidad.** `afirmaciones.db` tiene **5 filas `casi_todo_n` y
   las 5 sin fichero**. Cero instrumentos propios sobre densidad, y ahí vive el
   salto «casi todos → todos».
4. **La pasada cruzada**: las 80 afirmaciones contra los dos pools
   (`hilos.db` + `records.json`), respetando el filtro de cuantificador —
   `promedio` y `casi_todo_n` **no se evalúan**, se rechazan.
5. **La Fase 3 del plan de la pinza hay que recalibrarla**: apareció el
   corrigendum de Hercher (14-06-2026) que **acredita el hallazgo a Xinjun
   Wang**, el mismo cuyo preprint el repo descartaba por «cero citas».

## 5. LAS DOS REGLAS NUEVAS DE HOY

- **`git fetch` antes de tocar nada.** `git status` a secas compara contra la
  última copia local del remoto y puede mentir.
- **Lo secundario va a un agente, siempre.** La prueba: ¿esto responde una
  pregunta sobre Collatz, o deja el repo más prolijo? Lo segundo se delega.
- Y una tercera, del usuario: **no se re-ejecutan los barridos caros** en pasadas
  de rigor.

---

## 2026-08-01 (noche) — LAS DOS AUDITORÍAS APLICADAS. 6 de 6 adversarios rompieron algo

Se aplicaron al repo las correcciones de dos auditorías con revisores
adversariales. **La matemática venía verificada; esta pasada era de escritura** —
que el repo *diga* lo correcto. Nueve commits temáticos.

### La regla nueva, primero, porque cambia cómo se trabaja

> **NO SE RE-EJECUTAN LOS BARRIDOS CAROS EN PASADAS DE RIGOR.** Decisión del
> usuario, 01-08-2026. Los que quedan excluidos: `clasesfusion.py` (`K_MAX=32`,
> más de una hora), `pinzaciclos.py` (`K_MAX=30`, 12,5 min), `densidadfusion.py`
> (`POTENCIA=28`), el experimento 3 de `redhilos.py`, y `coralprimos.py`.
>
> **Sus resultados están en `sucesiones.txt`, en `resultado_paralelo_k32.txt` y
> en este documento, y no se vuelven a calcular para corregir un comentario.**
> Si una pasada toca uno de esos ficheros, se comprueba la sintaxis y el barrido
> cp1252 y se deja constancia de que no se corrió. *Correr una hora de CPU para
> validar un cambio de prosa es gastar la máquina en el sitio equivocado.*

### El saldo

**Seis adversarios, seis rompieron algo.** Ninguno salió con las manos vacías, y
eso es un dato sobre el repo, no sobre los adversarios.

### Las sorpresas, ordenadas por lo que cambian

1. **La cota de ciclos estaba mal, Y A NUESTRO FAVOR.** El
   `217.976.794.617 / 355.504.839.929` que se había escrito esa misma mañana
   exige `X₀ ≥ 2^71,884`, y Barina está en `2^71,019`. La buena es
   **`114.208.327.604` (atajo) / `186.265.759.595` (clásico)**, certificada por
   tres caminos. **Y el número lo publica Barina 2025 §6 y lo repite Wikipedia**:
   copiamos bien una fuente arbitrada equivocada. *Es el tercer caso de la misma
   familia y el primero en el que el error nos favorecía — que es la dirección en
   la que nadie mira.*

2. **La marca «CITA SIN VERIFICAR» de Wu–Huang 2001 era el error, no la cita.**
   Existe: *Mathematica Applicata* (Wuhan) 14 (2001), supl., 21–25, MR 1885838,
   y está en la bibliografía anotada de Lagarias con los vectores de paridad
   textuales, que se recalculan bit a bit. **No estaba en Crossref porque es un
   suplemento de una revista china.** *Primera vez que se corrige una refutación
   propia y no una afirmación — o sea que el pendiente de «auditar las
   refutaciones» ya se cobró su primera pieza sin que nadie lo ejecutara a
   propósito.*

3. **Everett estaba mal traducido en las DOS frases**, y una de ellas
   (`«1,585 es el umbral verdadero»`) se contradecía con la sección de la lámina
   del propio documento. Lo correcto es `B/A > 1,73697`, y el `0,7369` es
   literalmente `1/L − 1`. **De ahí salió el hallazgo de la pasada**: el hueco
   `log₂(10/9) = 0,152` es el precio exacto de usar `5/3`, y los 24 números que
   Everett no certifica caen los 24 dentro.

4. **El criterio de fusión vale para `m ≥ 1`, no «para todo `m`».** Falla en
   `m = 0` en tres clases. **Y nadie lo vio porque `clasesfusion.py:202` dice
   `for m in range(1, 40)`** — la fuerza bruta no podía ver el único `m` que
   rompe. **Segunda vez del mismo patrón**, después del piso de la altitud.
   La cota del 43,57% no se mueve.

5. **«`T^k` es una biyección sobre `Z/2^k`» es falso al pie de la letra**, pero
   la conclusión estratégica se salva entera porque sólo usaba la versión
   verdadera. **El repo tuvo suerte**: la frase falsa estaba escrita al lado de
   la buena.

6. **Hercher tiene CORRIGENDUM (14-06-2026)** sobre el Teorema 21 — la pieza que
   `reimpl.py` marca como caja negra. Y **agradece el hallazgo a Xinjun Wang**,
   el mismo cuyo preprint este repo descartaba por «cero citas y metadatos
   descuidados». La Fase 3 del plan estaba calibrada sobre una impresión que hubo
   que revisar.

7. **`γ(ρ)` unifica cuatro entradas en una.** La identidad de `mapahilos.py` es
   exacta y es Terras en logaritmos; evaluada en `ρ = 1/2` da las tres constantes
   de parada, y el `1:2:3` es `ρ : 1 : 1+ρ`. **Pero no sirve para la fórmula**:
   para conocer `ρ` hay que haber terminado la trayectoria. Vale como
   unificación, no como vía.

8. **El `120` de `densidadfusion.py` es de Wu 1993.** Lo redescubrimos.

### Y lo que aguantó, que es la otra mitad

Trece piezas atacadas con implementación independiente, cero movidas: Terras
1.1, 1.2 y C1.4, la Tabla C, Gao 1993 (los 35.654 uno a uno sobre números de 151
cifras), Wu 1995, A076227, Elia–Tucker, la cota `5/3`, Eliahou, Sinisalo, el
`1,4784` y el Teorema 23. **Está en `CLAUDE.md`, en la sección nueva «La otra
mitad de la auditoría».**

**Y con ella el ANDAMIO**, que no se había escrito nunca: qué se cae si cae cada
pieza. De Terras 1.2 cuelgan seis ficheros, la cota del 43,57%, las dos
sucesiones de OEIS y el enunciado del cuarto camino — y por eso es la mejor
verificada. **De la traducción de Everett no cuelga nada, y por eso su error
vivió un año.** *Lo que sostiene mucho se delata solo; lo que no sostiene nada
hay que ir a auditarlo a propósito.*

### Estado de los pendientes de más abajo

- **La deuda de los siete `verificar_*.py`: SALDADA.** Están trackeados, y de
  paso se arregló el bug que uno de ellos tenía dentro (`frontera()` devolvía el
  último *jump value* en vez del último periodo, con las tres filas de su tabla
  cortas por 1,04× / 16,57× / 10,94×).
- **El pendiente de auditar las refutaciones sigue vivo y acaba de justificarse
  solo** con el caso de Wu–Huang. La tabla de las diez sigue sin ejecutarse.
- **El bloque 1 de la búsqueda web (la conjetura CST) tiene ahora un puntero
  desde la sección de las constantes**: `σ = χ` resultó ser esa conjetura, y el
  enunciado honesto (`E[χ]` es cota inferior demostrada de `E[σ]`) **mejora** la
  categoría de la constante de Wagon en vez de degradarla.
- **`oeis_borrador.txt` sigue sin enviarse**, pero ya no por la cita: la línea
  `%D` está completa. El bloqueo es el de `a(k)` idéntica para `3n+1` y `3n−1`.

---

## ⇢ LA AUDITORÍA DEL 01-08-2026: tres cosas que hay que decidir antes de nada

9 agentes, 3 fases, revisores adversariales, **20 correcciones a la propia
clasificación**. El informe entero está en el output del workflow `wkujctscn`.
Aquí va sólo lo que cambia decisiones.

### 1. `a(k)` ES IDÉNTICA PARA `3n+1` Y PARA `3n−1` — y eso toca el envío a OEIS

Verificado por el revisor con implementación propia, `k = 3…13`:
`1, 3, 8, 18, 39, 82, 170, 351, 721, 1476, 3012` — **los mismos términos con las
dos reglas**. El signo del `+1` es justo lo que convierte un mapa con **un**
ciclo en uno con **tres**; una cantidad invariante bajo esa simetría **no puede
ser evidencia sobre convergencia**.

El criterio de fusión sigue siendo **exacto y correcto** — es la regla `R3` de la
criba de Barina. Lo que se cae es su `sirve_para_la_formula`.

> **`oeis_borrador.txt` NO se envía hasta resolver esto.** Sería publicar una
> sucesión que no distingue el mapa de un ciclo del de tres.

*Pendiente: llegar a `k ≥ 20` y decidir si la coincidencia es un teorema o se
rompe. La biyección `r → 2^k−2−r` que se alegó **no se pudo confirmar**: los
cardinales coinciden, los conjuntos no.*

### 2. EVERETT ESTABA MAL TRADUCIDO, y la versión escrita era infalsificable

El `CLAUDE.md` decía `A/(A+B) < 0,5757 ⟺ B/A > 0,7369`, «más flojo que
`log₂3 = 1,585`». **Falso.** La `N` de Everett son pasos del **atajo**, donde
`X ≡ A` y `N ≡ B` exactamente (comprobado en 27, 221, 703, 9663, 100009,
63728127). La condición real es **`B/A > 1,73697`**, que es **más FUERTE** que
`log₂3`, no más floja.

Y muerde: el **27** (`B/A = 1,7073`) y el **63728127** (`1,6583`) **no la
cumplen y convergen igual** — que es exactamente lo que significa «casi todo `n`».

> Tal como estaba escrita, **toda trayectoria que llega a 1 la cumplía de sobra:
> una comprobación que no puede fallar.** Es justo lo que este repo se prohíbe.

### 3. UNA COTA NUEVA, Y ES MÁS FUERTE QUE LO QUE TENÍAMOS

De `C ≥ 0` en la identidad, sin asumir convergencia:

```
2^B · seq[j]  >=  3^A · seq[i]        para TODO par i<j de TODO n
si un tramo BAJA, entonces 2^B > 3^A
```

Verificado sobre **prefijos que nunca tocan el 1** (semillas de 20/60/200 bits):
356.850 pares, **0 fallos, 0 valores de `C` negativos**; y 272.063 tramos
descendentes, **0 violaciones**. **Convierte «el balance decide todo» de promedio
sobre trayectorias en cota por tramo.** Vive en `collazlamina.py`, en el cálculo
que el fichero hace antes de dibujar.

### Y el hueco, confirmado con números

`afirmaciones.db`: **5 filas `casi_todo_n`, las 5 con `fichero = NULL`.** Cero
instrumentos propios sobre densidad. Reparto: `todo_n` 17 · `clase_residual` 17 ·
`verificado_hasta` 15 · `promedio` 16 · `ciclos` 10.

**Y el repo tiene demostrado él mismo que el cuarto camino está vallado por los
dos lados:** `a(k) ≥ 1` para todo `k` (`descensoresto.py`) dice que la criba
modular **nunca se vacía**; la columna «ambiguo» de `redhilos.py` dice que ninguna
clase se decide antes del bit `k`. Lo que falta no es un pool más grande: es un
instrumento que mida **densidad logarítmica**, que hoy no existe en ninguna línea.

### Deuda inmediata

**7 ficheros `verificar_*.py` (5.034 líneas) están sin trackear en git.** Es el
mismo fallo del 30-07 —matemática fuera del repo— todavía a tiempo de evitarse.
**Nadie los ha auditado**: los escribió el workflow de lo ajeno mientras corría la
auditoría, y no entraban en su inventario.

> **⇢ SALDADA la misma noche (ver la entrada de arriba).** Están trackeados. Y el
> aviso de «nadie los ha auditado» resultó ser bueno: `verificar_terras.py [6](d)`
> tenía un bug —devolvía el último *jump value* que pasa en vez del último periodo
> `k`— que dejaba su tabla corta por factores de hasta 16,57×. Lo cazó
> `verificar_frontera_ciclos.py`, que es su revisión adversarial, y ya está
> arreglado con el hueco entre jump values comprobado en vez de supuesto.

---

## ⇢ PENDIENTE: convertir en `.py` lo que trajo la búsqueda web del 01-08-2026

Encargado el **01-08-2026**. Una búsqueda web cruzó los 63 puntos del repo contra
la literatura y trajo diez cosas. **Ninguna está comprobada con código propio, y
todas salen de fragmentos de búsqueda, no de haber leído los papers.** Es
exactamente el error de Wu–Huang otra vez si se construye algo encima sin
verificar. Un `verificar_*.py` por bloque, con revisor adversarial.

### Lo más importante que se encontró

**LA CONJETURA DEL *COEFFICIENT STOPPING TIME* (Terras 1976, bautizada por
Lagarias).** Es el cuarto camino enunciado por otro hace cincuenta años:

```
σ*(x) := min{ k >= 1 : 2^k > 3^{m_k(x)} }     <- solo el coeficiente
σ (x) := min{ k >= 1 : T^k(x) < x }           <- la parada de verdad
Siempre σ*(x) <= σ(x).   CST: son IGUALES para todo x >= 2.
```

- **Si CST es cierta, NO hay ciclos no triviales.**
- **Si CST es cierta, el conjunto de `n` con tiempo de parada `k` es exactamente
  una unión de clases de congruencia módulo `2^k`.**

Y en coordenadas del repo, `2^k > 3^{m_k}` es **`B/A > log₂3`**. La diferencia
entre `σ*` y `σ` es **exactamente el `C` de la identidad, o sea el `+1`**: `σ*`
ignora `C`, `σ` lo incluye. Luego **CST dice que el `+1` nunca cambia dónde cae
la primera bajada** — el objeto que este repo lleva tres sesiones midiendo sin
saber para qué servía.

### Los diez bloques a convertir en código

| # | resultado | qué comprobar |
|---|---|---|
| 1 | **CST** (Terras / Lagarias) | `σ*(n) == σ(n)` en los 11 hilos, los 243 récords y un barrido. Y medir la holgura `σ − σ*` |
| 2 | **Böhm–Sontacchi 1978**: `x = Σ 2^{m−b_k−1}·3^{k−1} / (2^m − 3^n)` | Es la misma familia que `pinzaciclos.py` (mismo denominador `2^m − 3^n`). Comprobar que las dos fórmulas dan lo mismo, y que recupera los tres ciclos negativos |
| 3 | **Bernstein–Lagarias 1996**: `Φ∘S∘Φ⁻¹ = T`, y `Q_∞` es homeomorfismo 2-ádico | Nuestra biyección finita mod `2^k` es su sombra. Verificar la conjugación a profundidad finita |
| 4 | **Monks 2006** (PAMS 134): **toda** progresión `A + BN` no constante es un conjunto suficiente | ⚠️ **doble filo**: legitima trabajar por clases, pero implica que **ninguna clase es más fácil que el problema entero** |
| 5 | **Krasikov–Lagarias 2003**: `#{n ≤ x que llegan a 1} ≥ x^0,84` | **Es la cota sobre densidad que el repo no tiene** (el hueco #64) |
| 6 | **Applegate–Lagarias 1995**: `π_a(x) ≥ x^0,81` para `a ≢ 0 (mod 3)` | la versión previa, por árbol |
| 7 | **Applegate–Lagarias 2003**: infinitos `n` con `σ_∞(n) > 6,14316·log n` | cota demostrada; nosotros sólo tenemos el promedio `10,428` |
| 8 | **Steiner 1977**: no hay 1-ciclos salvo el trivial | es la **base** de Simons–de Weger y Hercher. Tenemos el tejado sin cimientos |
| 9 | reducción a **`n ≡ 3 (mod 4)`** | las otras tres clases tienen secuencia finita que baja. Lo tenemos implícito y sin enunciar |
| 10 | **arXiv 2606.02621 (2026)**, Fibonacci vía estructura modular | puede ser nuestro `F(k+2)` de `mallaresiduos.py`, o algo mejor. **Leerlo entero** |

*Contexto: [ccchallenge.org](https://ccchallenge.org/) lleva 372 papers
catalogados y **1 formalizado**. Tao, Eliahou y Bernstein–Lagarias esperan
auditoría; Monks 2006 y Knight (2026) están en formalización.*

**Prioridad 1 es el bloque 1.** Si CST resulta ser lo que parece, deja de ser una
búsqueda difusa de «la fórmula» y pasa a ser un enunciado preciso con cincuenta
años, que el repo tiene el instrumental para atacar.

> **⇢ PRIMER CONTACTO CON EL BLOQUE 1 (01-08-2026, noche), y viene por un lado
> inesperado.** Auditando las constantes salió que el repo daba `σ = χ` por
> hecho, y **es precisamente la conjetura CST**: lo demostrado es `σ ≥ χ`.
> Medido: 0 diferencias en los impares hasta `2·10⁶`.
>
> **Y el enunciado honesto MEJORA la categoría de la constante de Wagon:**
> `E[χ]` es una **cota inferior demostrada** de `E[σ]`, no un «promedio». En la
> taxonomía de este repo eso vale más. *Es la única corrección de toda la pasada
> que sube algo de categoría en vez de bajarlo.* El puntero está escrito en la
> sección de las constantes de `CLAUDE.md`.

---

## ⇢ PENDIENTE PRIORITARIO: auditar las REFUTACIONES, no sólo las afirmaciones

Encargado el **01-08-2026**, para ejecutar **en cuanto terminen** los dos
workflows en curso (la auditoría del repo y la verificación de lo ajeno).

**El agujero, y es de método.** Este repo es adversarial con lo que afirma y
crédulo con lo que refuta. Las diez correcciones de *«lo que se creyó y era
falso»* se dieron por buenas en cuanto aparecieron, porque una corrección suena
a rigor. **Pero una refutación es una afirmación como cualquier otra**, y puede
tener los mismos defectos que ella denunciaba: confundir el mapa clásico con el
del atajo, comparar unidades distintas, tomar una muestra por una constante,
extrapolar de un rango a todos los `n`.

**El riesgo concreto: si una sola de las diez está mal, tiramos un dato bueno Y
anotamos una lección falsa.** Lo segundo es peor, porque la lección se aplica
después a otras decisiones.

**Cómo hacerlo:** un agente por corrección, aritmética exacta, y **revisor
adversarial detrás** — el mismo esquema que se usó con lo importado. Los dos
pools ya están en disco: los **once hilos de `hilos.db`** (el caso ordinario) y
los **243 récords de `records.json`** (el extremo). *Los extremos confirman; los
controles refutan.*

| # | la refutación a auditar | cómo se comprueba |
|---|---|---|
| 49 | el `0%` de encimadas de Harriss era falso | árbol inverso, claves módulo `Φ_N`, sin floats |
| 50 | el `1,7345` no es constante sino muestra | re-medir a `10³…10⁶` y ver si se asienta |
| 51 | «se escapan del rango» no discrimina | `3n+1` contra `3n−1` a cuatro tamaños |
| 52 | `2/ln(4/3)` es del atajo, no del clásico | **directo sobre los 11 hilos**: pasos / `ln(n)` en los dos mapas |
| 53 | al piso le faltaba `n impar` | **11 hilos + 243 récords**, forma entera exacta |
| 54 | el `45 = 3²·5` explicaba un nivel de 31 | `coralprimos.py`, primos vecinos del 45 |
| 55 | el `+1` aparece dos veces, no tres | **11 hilos** con `Fraction`: ¿`ε ≡ S` en todos? |
| 56 | el `0,2286` está en bits, no nats, y no es cota | **11 hilos**: `ε` de cada uno, en las dos unidades |
| 57 | el exponente de la criba es `0,108`, no `0,05` | `descensoresto.py` por tramos |
| 58 | la cita del `19.478.780.533` es 11× más débil | bibliográfica — **no** computacional, no forzarla |

**Ocho de las diez son computables, y cinco se pueden atacar directamente contra
los once hilos.** La 58 es bibliográfica y no hay que fingir que se verifica.

> **⇢ ESTE PENDIENTE ACABA DE JUSTIFICARSE SOLO (01-08-2026, noche).** Sin
> ejecutarlo, apareció el primer caso: **la refutación de la cita de Wu–Huang
> 2001 era la equivocada.** Se había dado por buena porque «no aparece en
> Crossref», y resulta que Crossref no indexa suplementos de revistas chinas de
> 2001. La cita existe, está catalogada, y sus datos se reprodujeron bit a bit.
>
> *O sea que la hipótesis de fondo de este pendiente —«una refutación es una
> afirmación como cualquier otra y puede tener los mismos defectos»— ya tiene un
> caso confirmado, y el defecto fue exactamente uno de los previstos: usar un
> instrumento fuera de su rango de validez.* **La tabla de las diez sigue sin
> ejecutarse, y ahora con más motivo.**
>
> *Y la 58 hay que releerla: el «11× más débil» de la cita de Laurore se calculó
> contra el `217.976.794.617` de Barina, que resultó ser el número equivocado.
> Contra la cota correcta el factor es **5,9**. La conclusión —cita válida pero
> débil, y publicada en mal sitio— no cambia.*

**Sólo después de esta pasada se borra el bloque E del resumen.** No antes.

> *Y si las diez aguantan, tampoco es tiempo perdido: pasan de «lo dijo Claude un
> día» a «verificado contra dos pools con revisor adversarial», que es la única
> forma en que este repo acepta algo.*

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
- el número es **5,86 veces más débil** que el estado del arte. O sea que el
  repo llevaba citada como *«lo que exige la literatura»* **una cota peor que la
  que ya se conocía**;
  > ⇢ **CORREGIDO el 01-08-2026 (noche): aquí decía «once veces», comparando
  > contra el `217.976.794.617` de Barina §6 — que resultó ser el número
  > equivocado** (exige `X₀ ≥ 2^71,884` y el récord es `2^71,019`). Con la cota
  > buena, `114.208.327.604` (atajo) / `186.265.759.595` (clásico), el factor es
  > **5,86**. La conclusión —cita válida pero débil, y en mal sitio— no cambia.
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
  > ⇢ **CORREGIDO el 01-08-2026, y la conclusión se refuerza:** el 2.592 es una
  > **foto de 1976**, no la frontera. Con `X₀ = 2^71` el mismo argumento excluye
  > hasta periodo **114.208.327.603**; con sólo `X = 10⁶` ya llega a 4.700. Harían
  > falta `2^114208327603` restos, no `2^2592`.
- **Las cribas no sirven para ciclos, y es estructural.** `T^k` es una biyección
  sobre `Z/2^k`: cada vector de paridad es una clase única. No hay nada que
  descartar. Una criba necesita que muchas clases compartan destino.
  > ⇢ **CORREGIDO el 01-08-2026: las dos frases del medio eran falsas.** `T^k` **no**
  > es una biyección sobre `Z/2^k` —ni está bien definida ahí (`k=1`: `T(0)=0`,
  > `T(2)=1`, misma clase) ni `T` es inyectiva (`T(1)=T(4)=2`)—. Lo cierto es que
  > **resto → vector de paridad** es una biyección `Z/2^k → {0,1}^k`. Y clases que
  > descartar **las hay**: `pinzaciclos.py` descarta casi todas. Lo que no hay es
  > descarte **en bloque**. *La conclusión se salvó porque se apoyaba en la frase
  > de al lado, no en ésta.*
- **Los promedios no pueden demostrar nada** sobre un caso individual. La
  pregunta que queda como filtro permanente: **¿esto es un promedio o es una cota?**

---

## Lo que queda pendiente

> **⚠ ESTA SECCIÓN ERA UN FÓSIL, y lo cazó un adversario el 01-08-2026.** No
> estaba fechada, así que se leía como viva, y sin embargo era anterior al
> 30-07: sobrevivió a la purga, a las dos auditorías y a los dos tríos **sin que
> nadie la tocara**. **Siete de sus puntos mandaban hacer cosas ya hechas, ya
> refutadas, o sobre ficheros borrados.** Reescrita entera abajo.
>
> *Es exactamente el modo de fallo que el `CLAUDE.md` tiene documentado —«cuando
> se corrija algo, hay que buscar dónde más se afirmaba»— sólo que la lista
> estaba en el **otro** fichero, y por eso ninguna de las correcciones la
> alcanzó. **Una sección sin fecha se lee como vigente: o se fecha, o se
> revisa.***

### 1. El plan de la pinza, en tres fases

Lo que lo hace viable: **Hercher no *invoca* el teorema de Baker** — toda la
maquinaria diofántica entra como un número importado de Simons–de Weger.
*(Matiz obligatorio: la caja negra **sí** contiene trascendencia. Su Lema 12
sale de Rhin 1987. «No invoca Baker» es cierto de su artículo, no de la cadena.)*
Y la métrica del esfuerzo, medida: **60 líneas de stdlib excluyen `m ≤ 82`**;
todo el aparato del paper (dos programas en C++, cinco semanas de cómputo)
compra el tramo 82 → 91.

- **Fase 1 — ⇢ HECHA.** `reimpl.py` está en el repo: reproduce el Teorema 23
  **7/7** en 5,5 s, sin un float en la cadena que decide, y dejó **dos
  discrepancias contra lo publicado** (el `ε₇` y la fila `m = 276`), confirmadas
  después por segunda vía en `verificar_ciclos.py`.
- **Fase 2** — la escalera afín de Wang: un intervalo intersecado con una clase
  residual. *Eso es la pinza.* Media está construida en `clasesfusion.py`.
- **Fase 3** — **verificar a Wang**, no superarlo. Su preprint (`m ≤ 95`) no está
  arbitrado y nadie lo ha comprobado.
  > **Recalibrado (01-08-2026):** el **corrigendum de Hercher del 14-06-2026 le
  > acredita a este mismo Wang** el hallazgo del error del Teorema 21. Se
  > verifica porque es interesante y verificable, **no porque se sospeche de
  > él**: «cero citas» mide la edad del preprint y «metadatos descuidados» mide
  > su maquetación, y ninguna de las dos mide si tiene razón.

### 2. El resto de la cola

- **`clasesfusion.py` a `k = 34`.** Con `clasesparalelo.py` cuesta ~4× lo de
  `k=32`. No va a decidir la conjetura de Wu — los incrementos de la razón
  (`0,0050 → 0,0039 → 0,0037 → 0,0031 → 0,0027 → 0,0026`) encogen demasiado
  despacio para distinguir "geométrico" de "1/k" — pero alarga la única serie
  que puede. **Es el único pendiente de esta lista que sigue vivo tal cual.**
- **La recta del umbral del coral**, `(N+19)/2` si `N ≡ 1 (mod 4)` y `(N+11)/2`
  si `N ≡ 3`: está **medida y no demostrada**. Demostrarla sí tendría forma de
  cota. Es lo que quedó en pie de esa línea.
- **OEIS.** El borrador **ya no existe** (lo borró la purga del 01-08-2026), y
  **el motivo que lo mató se cayó** el mismo día: era *«`a(k)` sale idéntica para
  `3n+1` y `3n−1`»*, y con `espejoak.lean` eso pasó a ser **un teorema** — y el
  mismo criterio descalificaría a `A076227`, que sí está catalogada desde 2002.
  Lo único que queda es la decisión personal de abrir cuenta y firmar. **Si se
  retoma, hay que volver a redactar el borrador.**

**⇢ CERRADOS, y estaban aquí pidiendo trabajo ya hecho:**

- ~~**El número primo de rumbos**~~ — **HECHO, y la predicción FALLÓ**
  (`coralprimos.py`): el 43 y el 47 chocan *antes* que el 45. Es la única
  refutación ejecutable de una predicción propia que tiene el laboratorio.
- ~~**Colorear el árbol de `collazarbol.py`**~~ — **cerrado por la purga**: el
  fichero se borró porque el cierre lo ponía la esfera elegida a mano.
- ~~**El `+1` aparece tres veces**~~ — **aparece DOS** (`elmasuno.py`, 20.011
  casos con `Fraction`): el `ε` de la lámina y el sobrante `S` de la fracción
  impar son **la misma suma, término a término**. *(Y el `0,2286` que aquí se
  citaba como «grosor de la lámina» es el `ε` del 221 en **bits**, ni siquiera
  una cota.)*

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
  (`clasesfusion.py` lo rederiva desde Terras y decide los infinitos `m >= 1`), **la
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
