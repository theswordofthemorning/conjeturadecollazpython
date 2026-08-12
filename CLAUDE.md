# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Conjetura de Collatz — laboratorio

Repo de exploración de la conjetura de Collatz (`n/2` si es par, `3n+1` si es
impar; se conjetura que todo `n ≥ 1` termina en 1).

> ## ⇢ LA INVESTIGACIÓN ACTIVA (04-08-2026): LEER `RutaTeoremas.md` PRIMERO
>
> La línea viva del repo es el programa de fusión de pares consecutivos,
> y al cierre del 04-08 **todo él se reformuló como UN SOLO OBJETO: la
> CADENA `(k, c)`** (teorema de **Leonas**, `paseodeladeuda.py` +
> `cadenakc.lean`). Todo estado de par vivo es una forma
> `{v, 3^k·v + c}`, la dinámica entera son **seis leyes exactas**
> decididas por un bit de Terras, y el zoológico previo —Perras, Gatas,
> Jirafas, el rebote, las puertas, las torres— son estados y
> transiciones suyas. El barrido simbólico reproduce `a(k)` exacto y
> extendió la serie hasta **`a(36)`**.
>
> **La pregunta del programa quedó reducida a UNA PIEZA.** La cadena de
> tres teoremas del cierre — **Tigresas** (cada paso del núcleo es
> moneda justa `×1/2 / ×3/2`: `E[m] = 1` exacto, perpetuidad crítica
> κ=1), **Arañas** (en `u = c/3^k` la torre DESAPARECE: la dinámica es
> el IFS `{u/2, (3u−1)/2}` más perturbación sumable) y **Moscas** (la
> tensión transferida: masa viva con `|u| > x` acotada por `B_θ/x^θ`
> **uniforme en t**, autocontenido) — deja abierto sólo **el PISO DE
> ABSORCIÓN POR VISITA**: si no se desvanece, `φ = 1` (Gao–Wu en
> densidad); si se desvanece, `φ < 1` con techo.
>
> **Tres revisiones adversariales externas aplicadas** (actas en los
> `teoremade*.txt` y `bitacora.md`). **`RutaTeoremas.md` tiene el estado
> exacto, la tabla del ZOOLÓGICO y los pasos siguientes en orden** — es
> el contexto de arranque; este documento es la doctrina de trabajo y el
> archivo histórico.
>
> ### La regla de nomenclatura (orden del usuario, 04-08-2026)
>
> **Todo teorema, lema o hallazgo PROPIO lleva nombre de animal en
> femenino** — Perras, Gatas, Jirafas, Leonas, Tigresas, Arañas, Moscas,
> Zorras, Lobas, Osas, Yeguas, Vacas, Cabras, Ovejas, Ciervas, Conejas,
> Nutrias, Ardillas, Comadrejas, Panteras, Ratas, Pumas. **No es
> decoración: es referencial** — al leer «Jirafas» se sabe al instante
> que es nuestro y no de la literatura. *(Históricos con otro género, ya
> citados en actas externas y por eso intocables: los 3 Chanchitos,
> Komodo 3, Pandas.)* **La tabla completa con estatus y fichero vive en
> `RutaTeoremas.md`, sección EL ZOOLÓGICO.** Para textos que salgan del
> repo: numeración seria con el descriptivo entre paréntesis.

No es una biblioteca ni un paquete. Son programas sueltos, cada uno con su
número configurable arriba del archivo, pensados para ejecutarse y mirar el
resultado. **El código se escribe simple a propósito**: nombres en castellano,
comentarios que explican lo obvio, sin abstracciones.


> ### ⇢ EL SISTEMA DE DERIVADOS (09-08-2026, diseño del usuario)
>
> Este fichero es **EL TRONCO**: doctrina viva, operativa, y resúmenes
> con código **`[D-nn]`**. El texto completo de cada rama vive en
> **`derivados.md`** bajo el MISMO código, íntegro y sin editar (la
> cirugía fue mover, no borrar). Si un resumen no alcanza: abrir
> `derivados.md` y buscar el código. Regla de mantenimiento: lo nuevo
> entra aquí condensado; la prosa larga nace en `derivados.md` con su
> código nuevo.

## REGLA CERO: REVISAR, REVISAR, REVISAR

**El cambio de mentalidad, dicho por el usuario el 01-08-2026 y establecido como
la regla que manda sobre todas las demás:**

> **NO** «hacer el menor esfuerzo y lo más rápido posible».
> **SÍ** «hacer el mejor esfuerzo, comprobando siempre, y después mandar un
> agente adversarial para que además lo revise».

**Son TRES capas, y ninguna sustituye a la otra:**

| capa | quién | cuándo |
|---|---|---|
| **1** | **yo, contra mi propio cálculo** | antes de enseñar el número |
| **2** | **un agente adversarial** | después, sobre lo que ya di por bueno |
| **3** | **el trío: Lean + independiente + comparador** | toda comprobación matemática — ver **LA REGLA DE LOS TRES**, más abajo |

*(La capa 3 se añadió el mismo día, al instalar Lean. Donde aplica —cualquier
cosa con forma de teorema o de cálculo— **sustituye a la capa 2**, porque el
comparador es un adversarial mejor apuntado: tiene una discrepancia que buscar
en vez de una página en blanco.)*

*Se establece después de que el asistente cometiera —midiendo en vivo, delante
del usuario— el error del mapa clásico contra el del atajo: exactamente el que
este documento tiene registrado dos veces. La capa 1 lo habría atrapado.*

### Capa 1 — antes de enseñar cualquier número

> **Pásale a tu propio cálculo la misma lista con la que se ataca a los
> agentes.** No después, no si sobra tiempo: antes.

```
1. QUE MAPA USE?  clasico (3n+1) o atajo ((3n+1)/2)?
   En el atajo cada paso impar TAMBIEN divide, asi que  B_clasico = A + B_atajo.
   Confundirlos ya costo: el 2/ln(4/3) atribuido mal (49,5% de error), la
   traduccion de Everett (0,7369 en vez de 1,73697), y este mismo error.
2. ES PROMEDIO O ES COTA?  Un promedio no demuestra ningun caso individual.
3. VERIFICACION CIRCULAR?  Estoy comparando una constante del repo consigo misma?
4. CUANTIFICADOR ESCONDIDO?  El bucle empieza en 1 y digo "para todo m"?
5. MUESTRA TOMADA POR CONSTANTE?  Paso con el 1,7345, con el 0% de Harriss y
   con la holgura del piso.
6. MISMAS UNIDADES?  Bits contra nats ya dio un factor 1,42 de diferencia.
7. SE PUEDE EVALUAR SIN HABER TERMINADO LA TRAYECTORIA?  Si no, es contabilidad.
8. EL LIMITE DEL BARRIDO LO ELEGI REDONDO?  4^k y 10^k son TODOS = 4 (mod 6),
   asi que 10^6, 10^7, 2^28, 2^30, 2^32 y 100000 caen en la MISMA clase.
   Si lo que mido es del tamano de UN termino, el limite no es un detalle:
   es un parametro, y redondo significa sesgado.
```

*(El punto 8 salio el 01-08-2026 de la auditoría de la refutación **#51**, y es
**prima hermana** del punto 5, no la misma: allí el problema era el **tamaño** de
la muestra, aquí es que el **borde** cae en una clase especial. Los cuatro `N`
que «coincidían» lo hacían por construcción — el `512`, el `2048` y el `8192`
**sí** difieren, y nadie los probó porque no suenan a límite de barrido. **Muerde
sólo cuando el efecto medido es del orden de un término**; en un promedio sobre
todos los `n < N` da igual.)*

### Capa 2 — el adversarial, después

**Todo lo que se dé por bueno va a un agente adversarial**, con el encargo de
romperlo y no de aplaudirlo. No es un lujo para lo grande: es el paso normal.
El adversario recibe la lista de arriba más los modos de fallo históricos, y su
resultado válido incluye «no pude romperlo» — pero sólo después de intentarlo.

> **⇢ PERO SI LO QUE SE REVISA ES MATEMÁTICA O UN CÁLCULO, esta capa se hace
> con el trío de LA REGLA DE LOS TRES**, no con un adversarial suelto. Un
> adversarial solo tiene que inventar por dónde atacar; el comparador del trío
> ya tiene dos derivaciones independientes delante. **El adversarial suelto
> queda para lo que no se puede partir en dos**: prosa, atribuciones,
> decisiones de método y lecturas bibliográficas.

**POR QUÉ ES LA REGLA CERO Y NO UNA MÁS.** Estos errores **no se quedan
quietos**: se escriben, se citan al día siguiente, y otra medición se apoya en
ellos. La cota de ciclos hizo esa cadena tres veces en un día —`19.478.780.533`
→ `217.976.794.617` → `114.208.327.604`— y cada eslabón parecía una corrección
rigurosa. **Un error propio no revisado tumba días de trabajo, no minutos.**

*Y el corolario incómodo, que es el argumento entero: los seis adversarios de la
auditoría rompieron los seis bloques. **Seis de seis.** Si un revisor externo
encuentra algo el 100% de las veces, entonces una medición sin revisar tiene, por
defecto, un fallo dentro — y eso incluye las del asistente.*

> **El coste de revisar se paga una vez. El de no revisar se paga cada día que
> otra cosa se apoye encima.**

## LEAN 4 — las reglas vivas [detalle íntegro: D-01 en derivados.md]

- **`lean --version` AL ABRIR** toda sesión que toque un `.lean`; si falla, reinstalar (elan, release de GitHub → `~/.elan`). El toolchain NO está en git y ya desapareció una vez.
- **Lo que tenga forma de TEOREMA va a Lean; lo que tenga forma de MEDICIÓN se queda en Python** con su control A/B y su adversarial.
- Núcleo sin Mathlib: hay `by_cases, cases, calc, rw, rwa, omega, decide, exfalso, show, unfold, split, rename_i`. **NO hay** `by_contra, ring, set, rcases, obtain`. Nombres de lemas: **sondear con `#check`**, no adivinar.
- **`#eval` NO vale como comprobación** (lo calcula el compilador): se escribe teorema `by decide` (lo revisa el núcleo). Todo `.lean` lleva un caso conocido del repo comprobado + cruce con implementación que no comparta código. Control final: **`#print axioms` sin `sorryAx`**.
- LA TRAMPA: Lean garantiza demostración↔enunciado, NO enunciado↔objeto.
- Al 12-08-2026 son **20 `.lean`**, todos núcleo puro, 0 `sorryAx`.

## LA REGLA DE LOS TRES [detalle íntegro: D-02]

Para lo que se vaya a escribir aquí o sostener algo: **1·LEAN** (demostrar) + **2·INDEPENDIENTE** (calcular sin ver al primero) + **3·COMPARADOR** con su lista: ¿enunciaron LO MISMO (mapa, cuantificadores, unidades)? ¿coinciden por premisa compartida? — **coincidir no es verificar** —; si discrepan, decidir; ¿`sorryAx`/`SystemExit`? La independencia se protege **AL LANZAR** (decir qué ficheros NO abrir). Si Lean no puede formalizar, el POR QUÉ es el entregable («es un promedio», «es contabilidad»…). Para tanteos basta la capa 1. *Régimen vigente (orden del usuario, 03-08): todo local y sin agentes por defecto; el trío/adversarial se lanza cuando el usuario lo pide.*

## REGLA DE PRIORIDAD: lo secundario va a un agente, siempre

**El tiempo de la sesión es para pensar sobre Collatz, no para mantenimiento.**
Establecido el 01-08-2026, después de una sesión entera gastada en arreglar
documentación mientras la investigación no avanzaba ni un paso.

**Manda a un agente en segundo plano, sin preguntar, todo lo que sea:**

- correcciones de documentación, conteos, erratas y consolidaciones del `CLAUDE.md`
- barridos largos (`clasesfusion.py` a `k` grande, cribas, verificaciones masivas)
- localizar o degradar citas bibliográficas
- limpiezas de datos, vocabularios de `afirmaciones.db`, reindexados
- cualquier cosa cuyo resultado sea *«el repo queda más ordenado»* en vez de
  *«ahora sabemos algo que no sabíamos»*

**Se queda en la conversación principal** lo que exige juicio sobre la
matemática: decidir qué medir, leer un resultado, discutir si algo es un promedio
o una cota, y las decisiones que cambian el rumbo.

> **La prueba para decidir, en una línea: ¿esto responde una pregunta sobre
> Collatz, o deja el repo más prolijo?** Lo segundo se delega. Siempre.

Y si una tarea secundaria aparece a mitad de otra cosa: **no se hace en el
momento.** Se anota y se delega, o se manda al agente y se sigue.

## LO PRIMERO DE TODO: `git fetch` antes de tocar nada

**Antes de editar este archivo, `bitacora.md`, o cualquier cosa, sincronizá con
el remoto.** No es formalidad: aquí se trabaja desde varias sesiones el mismo
día, y `CLAUDE.md` es un archivo de 2.000 líneas que se edita en todas.

```
git fetch origin && git status -sb
```

**`git status` a secas NO basta, y esta es la trampa exacta.** Sin `fetch`,
`status` compara contra la última copia *local* del remoto y escribe
`## main...origin/main` sin flechas — que se lee como «sincronizado» y puede ser
mentira. Sólo después del `fetch` aparece el `[behind N]` de verdad.

**Ya mordió, el 01-08-2026:** una sesión corrigió los conteos de `CLAUDE.md`
contra una versión que tenía un commit de menos — y ese commit ya había hecho las
mismas correcciones, además de añadir siete `.py`. Todo el trabajo salió
redundante y hubo que rehacerlo contra la versión buena.

Si ya editaste sin haber hecho `fetch` y aparece `behind`: **no fuerces el
merge.** `git stash push -- <archivo>`, `git merge --ff-only origin/main`, y
después mirá qué de lo tuyo sigue haciendo falta. Casi siempre es menos de lo que
parece.

## Instalación [historia y avisos: D-03]

`pip install -r requirements.txt` (numpy, matplotlib, plotly). Lean 4 aparte (elan — ver LEAN 4 arriba). **`jq` NO está**: usar `python -c`. No hay tests, ni linter, ni `pyproject`, ni CI: no buscarlos. CONTEOS al 12-08-2026: **83 `.py` · 20 `.lean` · 3 `.db`** — la regla: quien añade un fichero actualiza el conteo EN EL MISMO COMMIT (ya se desfasó cuatro veces).

## Cómo está repartido el repo [detalle: D-04]

Núcleo de cálculo: salida a stdout/txt/db, **constantes en MAYÚSCULAS arriba**, comprobaciones ANTES de concluir cortando con **`SystemExit`**, código a nivel de módulo — **importarlos LOS EJECUTA** (excepción con `if __name__`: `clasesparalelo.py`, multiprocessing en Windows). **Sólo CUATRO dibujan** (`collazmalla`, `mallaresiduos`, `mallascerradas`, `mapahilos` — importarlos abre navegador). La duplicación de `secuencia_de` es **DELIBERADA**: no refactorizar. Programa nuevo: copiar la forma de `pinzaciclos.py`/`cotatramos.py`. Los `verificar_*.py` re-derivan lo importado de la literatura; su salida es un veredicto. `collatz.py` es el único módulo; `main.py` su CLI (`verificar/records/camino`).

## Cómo se ejecuta

Se abre el archivo, se cambia el número de arriba, y se corre
(`python archivo.py`, o Ctrl+B en Sublime Text).

**Sublime Text no acepta `input()`** — el programa se cuelga esperando. Por eso
cada script trae el valor en una constante editable arriba del archivo, nunca
solo `input()`. *(El único que tenía salida de emergencia con `tkinter` era
`collazejecucion.py`, borrado en la purga. **No copies ese patrón: copiá el de la
constante.**)*

Los cuatro que dibujan abren plotly solo en el navegador (zoom con la rueda, giro
con el mouse, valores al pasar el cursor).

> **REGLA (01-08-2026, del usuario): NO SE RE-EJECUTAN LOS BARRIDOS CAROS EN
> PASADAS DE RIGOR.** Si una sesión sólo corrige comentarios, prosa o
> atribuciones, **no se vuelven a correr**:
>
> ```
> clasesfusion.py    K_MAX = 32       mas de una hora
> pinzaciclos.py     K_MAX = 30       12,5 minutos
> redhilos.py        experimento 3
> coralprimos.py
> ```
>
> Sus resultados están en `sucesiones.txt`, en `resultado_paralelo_k32.txt` y en
> este documento. Lo que sí hay que hacer al tocarlos: **comprobar la sintaxis,
> pasar el barrido cp1252, y dejar dicho que no se corrieron.** *Gastar una hora
> de CPU para validar un cambio de prosa es gastar la máquina en el sitio
> equivocado.*

**TRAMPA DE CARACTERES EN LOS `print()`.** Cuando la salida va a una tubería —y
la de Sublime Text lo es— Windows la codifica en **cp1252**, no en UTF-8. Un
carácter que no exista en cp1252 hace crashear el programa con
`UnicodeEncodeError`, aunque el archivo esté guardado bien.

Sirven (están en cp1252): `· × ° — … ± « »`
**No sirven:** `→` (U+2192), `−` el menos tipográfico (U+2212), `≤ ≥ ✓`

En los comentarios y en los títulos de plotly se puede poner lo que sea, porque
esos no pasan por `stdout`. **La regla es solo para lo que está dentro de un
`print()` o un `raise SystemExit()`.** Escribí `->` y `-` y listo.

Esto ya rompió código de verdad: `main.py` tenía `→` en tres `print()` y
`python main.py camino 27` crasheaba desde Sublime. Corrido el **01-08-2026**
sobre los `.py` (última pasada 04-08-2026, los 52): **0 hallazgos**, está limpio — si aparece uno nuevo, lo
metiste vos. Para revisarlo:

```
python -c "
import glob
for a in sorted(glob.glob('*.py')):
    for i,l in enumerate(open(a,encoding='utf-8'),1):
        if 'print(' in l or 'SystemExit' in l:
            for c in set(l):
                try: c.encode('cp1252')
                except UnicodeEncodeError: print(ascii(a), i, ascii(c))
"
```

## Los archivos

| Archivo | Qué hace |
|---|---|
| `collatz.py` | Motor: `secuencia`, `altitud_maxima`, `tabla_de_pasos`, `verificar`, `records` |
| `main.py` | CLI: `verificar`, `records`, `camino` |
| `collazmalla.py` | **La malla real**: cada par de puntos en coordenadas (A, B). Dibuja |
| `cotatramos.py` | **LA COTA POR TRAMO**, rescatada de `collazlamina.py`: `2^B·seq[j] ≥ 3^A·seq[i]`, y si un tramo baja entonces `2^B > 3^A`. Verificada sobre prefijos que **nunca llegan al 1** |
| **`atacacst.py`** | **EL ATAQUE A CST** (02-08-2026): en cada clase `r mod 2^k` donde el coeficiente cae, el fallo de CST sólo puede vivir en el tramo finito `m ≤ T^k(r) − r`. Revisa esos tramos y decide CST **para todo `n ≥ 2` con `σ* ≤ 27`**, autocontenido, sin `X₀` importado. Hallazgo: hasta `k = 27` — incluido el jump value — **el tramo estuvo siempre vacío** (`t ≤ r` en toda clase caída) |
| **`atacacst.lean`** | **LA PALANCA, demostrada**: `terras_1_2` + `palanca` (coeficiente cae y `m` fuera del tramo ⟹ bajada real) + `tramo_finito` (basta `m > T^k(r)`) + **`tramo_finito_fino`** (basta `m > T^k(r) − r`, que es **el criterio exacto que usa el `.py`** — hueco Lean↔Python cerrado el 03-08-2026), para **todo** `k, r, m`, sin Mathlib, `#print axioms` limpio. El quinto `.lean` del repo |
| **`atacacst2.py`** | **La fase 2 del ataque: subir `X₀`.** Barrido directo `σ = σ*` avanzando los dos criterios JUNTOS (si uno dispara sin el otro, `SystemExit`: sería el contraejemplo). `X₀` subió de `2·10⁷` a `10⁸` y después a **`10⁹`** (02-08-2026, ~18 min de CPU): **0 diferencias en los dos barridos**, resultados en `atacacst2_progreso*.txt`. La conversión a un corte `σ* ≤ K` nuevo va por la curva `B(k)` de `paradacoef.py` y **sigue pendiente** |
| **`cotatramos.lean`** | **La misma cota, DEMOSTRADA en Lean 4** para todo `n₀` y todo `k`, sin Mathlib. Identidad de Terras, cota y corolario; `#print axioms` limpio; el 221 comprobado por el núcleo. **El primero de los cinco `.lean` del repo** |
| **`cotatramos3n1.lean`** | **La cota del mapa `3n−1`, demostrada.** Agente 1 del primer trío. Identidad sin resta (`2^B·n_k + C = 3^A·n₀`), cota **invertida**, corolario espejo *«sube ⟹ `2^B < 3^A`»*, y la discriminación como **teorema**: cada cota es falsa en el otro mapa, cerrado con `decide`. Los tres ciclos de `3n−1` comprobados por el núcleo |
| `cotatramos3n1.py` | **Lo mismo, calculado por su cuenta.** Agente 2 del mismo trío, sin ver el `.lean`. Deriva la identidad en vez de copiarla; exhaustivo `n₀ = 1…400`, semillas de 200 bits, y tramos que dan **varias vueltas dentro de los tres ciclos** — el caso que en Collatz no existe |
| **`espejoak.lean`** | **`a₊(k) = a₋(k)` DEMOSTRADO para todo `k`**, sin Mathlib y sin `sorry`. La biyección es la reflexión `2^k−1−r`; incluye Terras para `m` **negativo** y el borde demostrado en vez de supuesto. Cruza contra `sucesiones.txt` y contra las ocho clases mod 32 **con `decide`, no con `#eval`** |
| `espejoak.py` | **Lo mismo por su cuenta**, sin ver el `.lean`. Diez comprobaciones con `SystemExit`, dos implementaciones sin código común, y la biyección verificada **como igualdad de conjuntos**, no de cardinales |
| **`pruebaresta.lean`** | **La compilación que cerró una disputa.** No dice nada de Collatz: demuestra que la forma **con resta truncada** también cierra la inducción en `ℕ` sin invariante reforzado, y con eso tumba a la vez la frase del `CLAUDE.md` (*«`ℕ` ya no sirve»*) **y** la explicación que daba el agente de Lean. El registro de que una frase publicada se refutó **compilando** en vez de opinando |
| `paradacoef.py` | **LA CONJETURA CST DE TERRAS, MEDIDA.** `σ*` se calcula sólo de `n mod 2^k`: **es lo único del repo que pasa el detector de contabilidad**. Trae la cota `B(k)`, que descarta contraejemplos con `σ* ≤ K` para **infinitos** números, y el control `3n−1` con el espejo `n → −n` |
| `franjaeverett.py` | **La franja `log₂(10/9)`**, el hueco entre lo que Everett demuestra y el equilibrio. **NO hay núcleo**: con `m ≥ 9` el conjunto excepcional hasta `10⁷` es `{3,5,7}`. Y el control mata la vía: sobre `3n−1` la franja mide **cero**, y `3n−1` no converge. **Reparado el 03-08-2026** — dos strings sin cerrar (texto adversarial pegado dentro de un `print`): **el fichero nunca había corrido entero**. Al correrlo, la afirmación enterrada se confirma: `M = 5, 9, 101, 1001, 10001` empatan a **0 excepciones reales** (hasta `10⁶`) y con `M = 10001` el umbral baja a **1,585011**, a `4,8·10⁻⁵` de `log₂3` (`M = 27` es el único con excepciones reales: 2). Salida en `franjaeverett_salida.txt` |
| `medidamonotona.py` | **La búsqueda de una cantidad monótona, y la medida de cómo falla.** Trece candidatas, ninguna decrece. La razón no es estadística: la clase `2^k − 1 (mod 2^k)` existe para todo `k`. Redescubre `A076227` sin buscarla |
| `auditarrefutaciones.py` | **Auditar las REFUTACIONES, no las afirmaciones.** Las diez del bloque E contra los dos pools: **8 confirmada, 2 exagerada, 0 refutada**. Se niega a evaluar la mitad bibliográfica de la #58 |
| `mallaresiduos.py` | **La malla completa de los arranques**: 2^k restos × k pasos. Dibuja |
| `mallascerradas.py` | **Los aros que cierran solos** y **la rueda del árbol**. Dibuja |
| `guardarhilos.py` | **Los 11 hilos 100000–100010 en sqlite** (`hilos.db`) y la malla de sus cruces |
| `hilos.db` | La base: tablas `hilos`, `pasos`, `cruces`, `fusiones`, `cola_comun`. **El pool ORDINARIO** |
| `mapahilos.py` | **Los once a la vez**, cuatro paneles. La razón de unos lo explica todo. Dibuja |
| `redhilos.py` | **Una red neuronal a mano** (solo numpy) puesta a buscar dónde muere la predicción |
| `clasesfusion.py` | **El criterio demostrado**: qué clases mod 2^k se funden para todo `m ≥ 1` |
| **`itinerarios.py`** | **El paso 1 de la clasificación de rutas** (03-08-2026): el itinerario de cada nueva como palabra de familias del mapa de `E`. Positivo: el último tramo de todo `|M|=4` vive en `{−5, −77, −4163}` — las familias de `|M|=2`: **la contracción, visible en las etiquetas**. Negativo registrado: la familia asintótica es invariante **ruidoso** para contar; el refinamiento pendiente es etiquetar por datos finitos del tramo |
| **`identidadexacta.py`** | **LA IDENTIDAD ENTERA DE LA RENOVACIÓN** (03-08-2026, propuesta por la revisión externa): `a(k+2) = a(k) + (2^k−1) + G(k) + H(k)` **clavada como igualdad de enteros** `k = 3…14` — la autosimilitud de Gatas y la ventana de Perras valen sin simulación ni sesgo. `G` y `H` nacen como sucesiones exactas; la rama `h` se reduce a `{w, 9w−1}`; los contraejemplos de Elia–Tucker viven todos en `|M| = 8` |
| **`masasdeclase.py`** | **Las masas de clase del sistema de renovación** (03-08-2026): la descomposición exacta de `g` y `h` por eventos de clase, con horquilla rigurosa para `f` por nivel. **Y el muro, con nombre**: la masa indecisa decae ~2% por nivel — el mismo muro de convergencia lenta que la razón de `b(k)`, porque es la misma pregunta. La vía que queda: renovación de la cola, no subir `p` |
| **`nuevasfusion.py`** | **LA ECUACIÓN DE LAS CLASES NUEVAS** (03-08-2026): una clase se estrena en el nivel `k+1` exactamente cuando `T^k(r)` y `T^k(r+1)` se encuentran **por primera vez en un vórtice** (`a = 3b+1`, paridades opuestas, `S` compensada en 1 — la regla del segundo padre). Caracterización con recíproco, `k = 3…15`, 0 fallos y 0 falsos positivos; reproduce `b(k)` término a término. **La pregunta de la razón 2 pasa de conteo ciego a congruencia.** Y trae la **familia extremal demostrada**: para todo `j` par, `(2^j−2, 2^j−1)` se funde por primera vez en el paso `j+2` con vórtice en el **repunit ternario** `(3^{j−1}−1)/2` ⟹ `b(j+2) ≥ 1` siempre. Los **estratos por pasos mixtos** (`|M|` par siempre; nuevos estratos entran cada dos niveles — el candidato a mecanismo de la razón → 2), y el **teorema de unicidad de `|M| = 2`**: exactamente una clase por nivel, `2^{k−1}−2` o `3·2^{k−1}−2` alternando — la primera fila del triángulo es `1, 1, 1, …` demostrada. *(Patrón refutado antes de publicarse: «todo `b` es `1 mod 3`» se rompe en `k+1=15` con `b = 2255`.)* |
| `sucesiones.txt` | Las dos sucesiones que **no están en OEIS**, con definición y verificaciones |
| `teoriacollaz.txt` | El planteamiento filosófico del que salió la idea de la esfera |
| `bitacora.md` | **Resumen por sesion y lo que queda pendiente.** Empezar por aqui |
| **`RutaTeoremas.md`** | **El camino a los teoremas de Perras y Gatas** (03-08-2026) por el mapa de dependencias, su estado bibliográfico verificado (Garner 1985, Elia–Tucker 2015), y **la ruta trazada para decidir `f`** — la ecuación de renovación cuya solución sería la conjetura de Wu en densidad. Contexto de arranque de la próxima sesión |
| `clasesparalelo.py` | El barrido de clases repartido entre nucleos. Se verifica solo contra a(30) |
| `pinzaciclos.py` | **La pinza de descarte de ciclos**: un candidato por resto, en cerrado. Barrido de 2^30 restos |
| `records.json` | **Los récords publicados** de Roosendaal y Barina: retraso, altitud, clase, planeo, residuo |
| `cruzarecords.py` | El repo cruzado contra esos récords. Cinco comprobaciones |
| `resultado_paralelo_k32.txt` | La verificación cruzada de `a(32)`: secuencial y paralelo dan `1.871.137.623` |
| `pisoaltitud.py` | **El piso de la altitud**, con su corrección: vale para `n` impar, y los pares fallan a propósito |
| `elmasuno.py` | **`ε` y `S` son la misma suma**, exacto. El `+1` aparece dos veces, no tres |
| `reimpl.py` | **El Teorema 23 de Hercher reproducido**, 7/7, sin un float en la cadena que decide. **Y dos discrepancias contra lo publicado**, ninguna de las cuales mueve el resultado |
| `coralprimos.py` | El número **primo** de rumbos. La predicción falló y la explicación del 45 se cayó |
| `descensoresto.py` | **El tiempo de descenso contra el resto**. `A076227` reproducida; la criba nunca se vacía |
| `guardarafirmaciones.py` | Escribe `afirmaciones.db`. No dibuja nada |
| `afirmaciones.db` | **Las tres capas**: `afirmaciones` (con cuantificador), `constantes` (con aviso), `correcciones` |
| `guardarrespuestas.py` | Captura las transcripciones de Claude Code y las mete en `respuestas.db` |
| `respuestas.db` | **El cuaderno de las conversaciones.** Tabla `respuestasclaude`, append-only |
| `transcripciones/*.zip` | **El `.jsonl` crudo respaldado, un zip por sesión.** Lo que `respuestas.db` no guarda: llamadas a herramientas, resultados y orden. Con su `LEEME.md` y el bloque para regenerarlo |
| `otramedicion2.py` | **La capa de promedios sobre la malla de hilos**, cruzada contra `afirmaciones.db`. La capa no anade informacion |
| **`verificar_terras.py`** | **La columna vertebral, re-derivada**: T1.1, T1.2, C1.4, la Tabla C y la exclusión de periodos. Con el aviso del bug de `frontera()` |
| `verificar_frontera_ciclos.py` | **La revisión adversarial de `verificar_terras.py [6](d)`**. Encontró el bug de la frontera |
| `verificar_everett.py` | La traducción de Everett a `(A,B)`. **Refutó las dos frases del CLAUDE.md** |
| `verificar_fusiones.py` | Garner G1/G2/G3 y Gao. **Encontró el `m ≥ 1`** y las dos hipótesis que le faltaban a G2 |
| `verificar_wu.py` | Wu 1992–95, Wu–Huang 2001, A076227. **Localizó la cita** y midió el agujero del `m = 0` |
| `verificar_ciclos.py` | La cota de longitud de ciclo **por tres caminos**, la fracción continua certificada, Simons–de Weger y el Teorema 23 |
| `verificar_constantes.py` | Wagon contra A122790, las constantes de parada con **dos estimadores**, `Res ≥ 1`, y la biyección de Terras al pie de la letra |
| `.claude/settings.local.json` | Permisos ya concedidos: `python *`, `py *`, `git fetch *` |
| **`retorno11.py`** | **EL CRITERIO FINAL** (aguantó la 4ª revisión): `φ = 1 ⟺ p = P₍₁,₁₎(retorno) = 1` en la cadena modificada; primeros retornos medidos a L = 35 |
| **`oscilacion.py`** | **GOLONDRINAS**: infinitas visitas al fondo c.s. (descenso de `v₂` + oscilación de martingalas); L2 verificado en 60.010 instancias |
| **`lamperti.py`** | La tabla de derivas exacta de `k` (28.436 estados) y las series de la cadena modificada |
| **`minorizacion.py`** | ABEJAS (bloques, incondicional — ver corrección #43), PALOMAS (`b(t) = N_t(1,1)`), BFS de accesibilidad, flujos |
| **`accesibilidad.py`** | **HORMIGAS**: constructor explícito a la fusión desde todo estado; constante fina abierta (corrección #44) |
| **`cadenaqnr.py`** | La cadena para `(qx+r)/2`: ÁGUILAS (`E[m]=(1+q)/4`) y LECHUZAS (`3\|r` ⟹ sin fusión S-igualada); series de `5x+1`/`7x+1` |
| **`diferenciales.py`** | El perfil diferencial exacto `a_Δ(k)`, `Δ ≤ 16` (la «DDT 2-ádica») |
| `pisoporvisita.py` / `empalme.py` / `pisoremedido.py` | Las series del piso por visita (la última con el exponente honesto post-revisión) |
| **`pisoporarranque.py`** | **El test decisivo de γ como fichero del repo** (11-08, paga la deuda de método: vivía sólo en la transcripción): el barrido podado desde `(2, c₀)` a la ventana de Doeblin, escalera de décadas `2000 → 2·10⁶` con horizonte EMPAREJADO T=150, reproducción de los tres puntos publicados a T=130 con `SystemExit`, y las γ por década emparejadas. Salida en `pisoporarranque_salida.txt` |
| **`arranquesporvisita.py`** | **Las dos patas sin medir de la reducción (13), medidas** (11-08): Monte Carlo de la cadena modificada (semilla fija, dinámica entera exacta) — `β = 0,000` (los arranques `\|c_i\|` planos de i=2 a i=1325: mediana ~2⁴, p90 ~2⁷) y el reloj `η = 2,082` (τ_i polinomial ~i², lo que L-B pide con margen infinito). Cruce independiente: `p*(2,2) = 0,84` dentro de la horquilla certificada `[0,763, 0,960]` del barrido exacto de masa |
| **`sombraexogena.py`** | **LA PRUEBA DE CIRCULARIDAD DE L-A** (11-08, dictada por el usuario): L-A escrita como enunciado AUTÓNOMO (paseo perezoso + perpetuidad acoplada por el bit, reloj exógeno — cero Collatz) y medida contra la cadena real. **Post-8ª revisión (R1-R5 aplicadas)**: V2 reproduce la FORMA (γ cayendo; décadas 2-3 a ±0,02, la primera difiere +0,05 significativo — el «±0,03» original era falso sobre su tabla); **el muro es BAJO en su versión estructural** (V2 es diana autónoma legítima, la transferencia acotada; el Laplace lo hizo la 8ª: óptimo en `L*−11`); el bug de la semilla salada ARREGLADO y re-corrido (reproducible); y las sondas a T fijo medían en parte artefacto de horizonte — la medición honesta pide `T ≥ 30·ln x`. Nota: `notaLAautonoma.txt` §6 |
| **`gramaticaderetornos.py`** | **LA GRAMÁTICA DE RETORNOS Y EL RÉCORD DE LA COTA** (11-08, el cierre de la prórroga): la identidad de renovación `F = Σ_j R^{*j} * A` verificada como ENTEROS sobre el triángulo entero (el triángulo ES la convolución de primeros retornos al lazo + cola de absorción — Ovejas, el triángulo y λ unificados), y la resumación geométrica `φ ≥ α/(1−ρ)` da **la nueva cota inferior récord de la densidad de fusión: `φ ≥ 0,443061`** (bloques ≤ 28, enteros exactos) — supera el 0,435658 de `a(32)/2^32`; +1,7 puntos a profundidad emparejada. **AGUANTÓ ENTERO la 8ª revisión** (adv 2: recomputado por dos caminos propios — censo de pares enteros reales + transición inferida — conservación en racionales, consistencia externa; predicción falsable: `a(k)/2^k` cruza 0,4431 hacia k≈36-40; y el cap `z ≤ 12` descarta 25,77% de masa — **subir el cap mejora la cota gratis**: la cadena restringida sin cap ya midió ≈0,4503 en float — ⇢ COBRADO en `recordsincap.py`, 11-08 (2)) |
| **`recordsincap.py`** | **EL RÉCORD SIN CAP, EN ARITMÉTICA EXACTA** (11-08 (2), el P4 del paper cobrado): la misma resumación geométrica SIN el cap de ceros y a bloques `≤ 34` ⟹ **`φ ≥ 0,462781`** — sobre el 0,443061 del cap y el 0,435658 de `a(32)/2^32`. C0 reproduce el récord viejo dígito a dígito; C1 la conservación sube a IGUALDAD exacta de racionales (sin cap nada se descarta); C2 monotonía nivel a nivel; C3 **el censo de pares enteros REALES** (2^20 clases, dos órbitas caminadas a pelo, sin `transicion()`) clava `R(t)` y `A(t)` celda a celda; C4 el veredicto con `SystemExit`. El parcial sin cap a L=28 (0,450341) clava el ~0,4503 en float del adversario de la 8ª. *Etiqueta: capa 1 + censo propio; sin revisión externa aún.* Salida en `recordsincap_salida.txt` |
| **`fichaagkv.txt`** | **AGKV 2005 LEÍDO ENTERO** (11-08 (2), el P1 del paper): los enunciados numerados (Teorema 1.1, Lemmas 2.4–2.7, Prop 3.1, la representación (4.10) de θ), el diccionario AGKV → pieza 3, y **el esqueleto de L3 por REVERSIÓN TEMPORAL en la absorción** — que no estaba en el plan previo: `h(k) = k−1` explícita (Bessel-3 discreto), la serie revertida convergente (análogo del Lemma 2.7) y el trasvase (Lemma 2.5). Bertoin–Doney queda [CITADO VIA AGKV] |
| **`medianauniversal.py`** | **EL MECANISMO DE L3, VERIFICADO POR DOS CAMINOS** (11-08 (2)): forward V2a condicionado a `τ ∈ [T, 2T]` contra la cadena revertida h-transformada (sin código común) — mediana 12,81 → 16,14 → 17,86 → 17,83 contra límite 17,50 (**desvío 1,9% en T=6400**), `P(\|W\| ≤ M75) → 0,750/0,740` (el 0,75 del límite clavado), balota 1,12–1,14 constante. **La mediana universal EXISTE y es la del h-transform de AGKV**; la cola de `\|W̃_∞\|` es la `1/x` de Kesten κ=1 (momentos crudos divergen: la vía de la mediana era la única). *Es medición del mecanismo, no cota.* Extendido la misma tarde a **V2b (rachas)**: converge a SU límite (desvío 1,2%) y los dos límites casi coinciden (17,60 vs 17,50) — la pata de P2. Salida en `medianauniversal_salida.txt` |
| **`trasvasel3.py`** | **LO QUE QUEDABA DE L3, VERIFICADO — y L3 ES TEOREMA** (11-08 (2), tercera pasada): fase A **exacta por DP** — el LLT del paseo absorbido (perfil `(y−1)` a <2%, **la constante `c₀ = 4/√π` clavada a 0,1%**) y el lema D de comparación (`sup D = 2,823` contra el `2^{3/2} = 2,8284` teórico); fases B/C por MC — la primera mitad se aniquila (mediana `e−14 → e−265`) y el truncamiento `err_640 = 0,000` estable en T. Con esto `teoremav2.txt` tiene **L3 y el teorema V2 completos y AUTOCONTENIDOS** (LLT incluido, ya sin cita externa): `φ_V2(x) ≥ c/√log x` con ventana universal — **L-A demostrado para V2**, pendiente de revisión externa. Hallazgo de tasa: `η_R` decae gaussiano-con-deriva (`−0,057R ± 0,6√R`) — la primera calibración del test falló y enseñó esta física. Salida en `trasvasel3_salida.txt` |
| **`medianareal.py`** | **LA MEDIANA UNIVERSAL EN LA CADENA REAL** (11-08 (2), cuarta pasada — el mecanismo de P2 medido): excursiones `(2, c₀) →` fondo, dinámica entera exacta, condicionadas a `τ ∈ [T, 2T]` con `T = 30 ln c₀` — la ley de `log₁₀\|u\|` a la entrada es **independiente del arranque** (mediana +1,195/+1,213/+1,263 en c₀ = 997/999.983/999.999.937: deriva 0,07 décadas sobre SEIS de c₀; q10 clavado +0,56). **Regalo: la balota real da 1,117–1,145 — la misma constante que V2**. Arranques primos no redondos (punto 8 + Cabras). Pista de P3 con forma cerrada: `v₂(3^k−1) = 1 / 2+v₂(k)` (LTE, verificada k ≤ 2000): las ventanas heladas son `O(log k)`. Salida en `medianareal_salida.txt` |
| **`lecturaracha.lean`** | El 20º: **LA LECTURA DE LA RACHA demostrada** (12-08) — la reducción de la Pieza B como teorema: `2^j \| hijo ⟺ 2^{j+1} \| (3c+1)` (bit 0) / `2^{j+1} \| (c−3^{k−1})` (bit 1), con testigos sin división, y la **UNICIDAD de la clase** (`tres_inyectivo`: ×3 inyectivo mod 2^n por inducción — el único ingrediente no lineal). «Racha ≥ j» es UNA congruencia mod 2^{j+1}. Instancias por el núcleo (`decide`): el contraejemplo del adv 1 (`3·1398101+1 = 2^22` exacto) y casos chicos. 0 `sorryAx` |
| **`notaequidistribucion.txt`** | **La Pieza B: la reducción, lo medido exacto y la ruta al teorema** (12-08): el mapa del conteo de colisiones vía el Δ de Tórtolas (k impar inyecta un bit fresco EXACTO; el esquema telescópico autoconsistente) y lo que NO dice |
| **`equidistribucionmixto.py`** | **LA PIEZA B, MEDIDA EXACTA** (12-08, punto 1(a) de la ruta post-9ª): **la reducción** — racha ≥ j tras un mixto ⟺ c cae en UNA clase mod 2^{j+1} (`3c ≡ −1` para bit 0; `c ≡ 3^{k−1}` para bit 1), así que la Pieza B ES equidistribución de `c_t mod 2^m`. DP exacto sobre `(k, c mod 2^{M−t})` con conteos ENTEROS de palabras (cero MC, cero floats), absorción contabilizada, escalera t = 8…24, tres arranques (los dos de siempre + el contraejemplo del adv 1 `c₀ ≡ −3^{−1} mod 2^21`). Veredicto: C_j ≤ 2,95 en toda celda con peso, tendiendo a ~1; el transitorio adversarial reproducido (racha₁ ≥ 19 forzada) y MUERTO a t ≥ 12; residuo peor (m=8) baja 9,5 → 1,6. Cruce independiente: enumeración exhaustiva 2^14 sin código común, igualdad de ENTEROS (E1), y la versión ADAPTADA por k-camino con C_j ≤ 1,000 en celdas gruesas. Colisiones dentro de fibra = estadística de cumpleaños (sin biyección exacta, sin obstrucción). Salida en `equidistribucionmixto_salida.txt` |
| **`dominacioncondicionada.py`** | **LA DOMINACIÓN CONDICIONADA A SOBREVIVIR, MEDIDA** (12-08, el §5(iii) de `notadominacion.txt` — punto 2 de la ruta post-9ª): escalera de horizontes T = 50…414 con ventana emparejada `[0,T)` (todas vs `τ ≥ T`), dos arranques. **Dos hallazgos**: (1) la dependencia del bit de apertura (el «7σ» del adv 1) es **TRANSITORIA** — en rachas tardías (cierre ≥ 100) se anula en ambos arranques (z ≈ 0) y el signo global se INVIERTE en el arranque B: era artefacto del tramo inicial determinista de c₀; (2) la ley condicionada converge a la geométrica **NEUTRA** (media → 1 desde abajo en A, desde arriba en B; `C_j` condicionado ∈ [0,88, 1,06]; tardío 1,010/1,036) — **la dominación condicionada aguanta con C ~ 1**. Regalo: supervivencia `~1/√T` clavada (S4: razón 1,947 ≈ 2). Salida en `dominacioncondicionada_salida.txt` |
| **`rachasreales.py`** | **LA DOMINACIÓN GEOMÉTRICA DE LAS RACHAS REALES** (11-08 (2), quinta pasada — el input del lema de racha de P2, **mejor de lo que el lema pide**): 3,86M rachas de 150k excursiones reales — `P(racha ≥ j)·2^j = 0,92–0,97` para todo `j ≤ 12` con muestra, **por debajo de 1**: el reloj real dominado por la `Geom(1/2)` de V2b sin inflación (franja `k ≥ 9`: máx 1,041; media 0,947 ≈ 1). La dominación que P2 hipoteca es casi una igualdad medida. Pendiente analítico: escribirla desde los lemas v₂ de `tortolas.lean`/`aterrizajen2.lean`. Salida en `rachasreales_salida.txt` |
| **`triangulodefusion.py`** | **El experimento de Pascal para `b(k)`** (11-08, propuesto por `fichawinklerzarubin.txt`): la tabla `F(t,S)` — nuevas absorbidas en el paso `t` con `S` unos, `Σ_S = b(t−1)` clavada t=4..22. **Veredicto NEGATIVO registrado**: con `S` como «posición» no hay recursión de dos términos ni déficit Zarubin concentrado (la coordenada candidata siguiente: `v₂(Δ)` de Tórtolas o la posición del último mixto). Dos regalos: la ley de borde exacta **`F(t, t−2) = ⌊(t−1)/2⌋`** (medida t≤22; el primer registro decía `⌊t/2⌋−1`, que falla en t impar — capa 1) con su derivación esbozada — las palabras de dos ceros que funden son `1^a 0 1^b 0 1` con `a` par: lazo de Gatas → ventana de Perras `(1,2)` → `(1,1)` → fusión, el stem de Garner como fila del triángulo; falta el lema «la rama `a` impar no funde» (candidato: Chanchitos/Cabras) — y la diagonal sesgada (`S/t = 0,5493` en t=22 **y sigue bajando** — sin límite proclamado, corrección de la 8ª) contra el 0,613 de Terras — quiénes funden llevan MENOS impares que lo típico |
| **`monedacondicionada.py`** | **GARZAS (propuesto, 10-08)**: forward-backward exacto del sesgo de la moneda condicionada, POR ALTURA — vive en `k ≤ 3`, `≤ ~0,03` por moneda, en las dos mitades; el balance condicionado a `(1,1)` es NEGATIVO; y el exponente local de `P(X_t=(1,1))` cruza 1 hacia abajo (0,76 a t=30). Validado contra urracas.py (6 cifras; el cruce cazó la degeneración del vórtice en el libro mayor) y por fuerza bruta entera |
| **`firmaacoplamiento.py`** | **TÓRTOLAS (propuesto, 10-08)**: el lema del acoplamiento de la moneda — los dos hijos de `(k, c par)` difieren en `Δ = c + (1−3^k)/2`, comparten trayectoria de `k` y `v₂(Δ)` baja EXACTO 1 por paso: divergen en `j* = v₂(Δ)` justo, con DOS excepciones nombradas (vórtice asimétrico; el signo mixto del único `abs`). Corolario: `j* ≥ horizonte ⟹ sesgo CERO exacto (99,85% clavado, fugas 2·10⁻⁵). El sesgo condicionado es TIMING puro del paseo crítico, desacoplado de `c` |
| **`tortolas.lean`** | El 19º: el núcleo aritmético de TÓRTOLAS demostrado — la diferencia de los hijos ES `Δ` (`delta_hijos`), `Δ=0 ⟹` mismo hijo, las siete leyes par a par con testigos sin división (`±D / ±3D`), el enganche del descenso (`pot2_mitad`), la imparidad conservada por `×3` y signo, las dos imposibilidades de paridad (la divergencia en `j*`), **el porqué de E2 como teorema** (`salida_signo_mixto`: con signos opuestos los abs restan la SUMA), y la instancia `(2,8)` cotejada con `decide` sobre las 4 palabras con la transición real |
| **`gaviotas.py`** | **GAVIOTAS (propuesto, 10-08) — LA COTA MARTINGALA, en dos teoremas**: (A) `\|E[(Ee−E0)·1_F]\| ≤ √(N_c·V_c)` — ocho líneas (bits justos dado el pasado + Doob + Cauchy–Schwarz), **la endogeneidad del horario desaparece del argumento**; (B, la reparación de la corrección nº 50 — el umbral 0,2446 es de LA SUMA, no de `a_D`): el vórtice es moneda centrada y la frontera impar resta, así que **la SUMA entera `a_V + a_D − a_K` queda certificada bajo 0,2446 en todos los T computados** (cota fina 0,198→0,192 en T = 16…28, valor real 0,019). Asintótico `O(T^{−1/4}) → 0` módulo el lema local `P(fondo) ≥ c/√T`. Ortogonalidad `Σ E[ΔM²] = P(1−P)` verificada como IGUALDAD DE RACIONALES |
| **`hormigas.lean`** | El 14º: descenso del gap y de frontera, núcleo puro |
| **`liebres.py`** | **LIEBRES + CEBRAS** (procedencia: sesión Opus 5 del 09-08; **pasó la 5ª revisión externa con correcciones aplicadas**): `φ = 1 ⟺ Σ P(X_t ∈ C) = ∞` para toda ventana finita C (Doeblin exacto `ε ≥ 17887/131072`; C arbitrario vía Hormigas cualitativo), y el umbral `log 2/log 3` como exponente de Lyapunov (la lectura «deriva de log\|u\|» fue ROTA por la 5ª y está retirada) |
| **`urracas.py`** | **TEOREMA DE URRACAS** (**aguantó entera la 5ª revisión**): `exp − contr = 2V + (Ee−E0) + k0 − k_t` exacto por palabra; el sesgo del fondo en tres términos medibles contra el umbral 0,26186 (efectivo ~0,2446 en la cadena) |
| **`urracas.lean`** | El 15º: el libro mayor demostrado — once constructores con testigos, invariancia por paso e inducción sobre caminos, 0 `sorryAx`; cotejado a máquina contra la cadena real por la 5ª revisión |
| **`actarevision0908b.txt`** | El acta de la 5ª revisión externa (tres adversarios contra la terna de la madriguera): LIEBRES aguantó, CEBRAS partida en dos, URRACAS entera |
| **`cabras.lean`** | El 16º: el invariante mod 3 de la torre (la puerta de CABRAS por la cadena entera) — `c % 3 ≠ 0` para todo alcanzado con `k ≥ 1`, corolario `torre_sin_ceros`; el regalo de la 5ª revisión, formalizado |
| **`aterrizajen2.lean`** | El 17º: el aterrizaje de N2 — la pieza 2-ádica con signo de Golondrinas (`v₂(c) > A ⟹` el bit 1 aterriza EXACTO en `v₂ = A−1`; `c = 0` ídem; `v₂(c) < A ⟹` baja exacto 1), testigos sin división, cotejado en 42.196 instancias |
| **`pumasescalera.py`** | Los escalones 7–9 del acorralado: los truncados publicados reproducidos + `K=13`, `K=15` y **`K=17` (5,3M estados, 11-08)** ⟹ `λ ≥ 1,9870`; gaps ×0,78 → ×0,81 → ×0,83 subiendo — consistente con λ = 2. El 8º y el 9º tras las banderas `ESCALON_8`/`ESCALON_9` (~10 min / ~15 min). ⇢ **Superado por `certificadocw.py`** (11-08 (2)): la razón convergida subió a certificado y la escalera al escalón 10 |
| **`certificadocw.py`** | **EL CERTIFICADO COLLATZ–WIELANDT DE LA ESCALERA ENTERA + EL ESCALÓN 10** (11-08 (2), P6 cobrado y superado): `v` entero, mínimo exacto de `(v[suc0]+v[suc1])/v[i]` sobre el soporte (el float sólo busca el vector) — los nueve escalones certificados a `< 5e-5` de lo publicado (los tres altos a `< 1e-6`), y **el escalón 10, jamás corrido (`K=19`, `\|c\| ≤ 3145728`, 22,5M estados): `λ ≥ 1,989042` CERTIFICADO** — el récord de Pumas sin letra chica. Gaps ×0,809 → ×0,831 → ×0,846 hacia 1: consistente con λ = 2. Determinista (reproducción exacta); ~10 min con `ESCALON_10 = True`, ~100 s sin él. Salida en `certificadocw_salida.txt` |
| **`rondadeltronco.py`** | **La 6ª revisión (la ronda del tronco)**: Leonas contra 50.000 pares reales (12,5 M de pasos, 0 fallos de forma; el censo de las coalescencias del ciclo `{1,4}→2`) y Moscas extendida a la cadena modificada. Acta: `actarevision0908c.txt` |
| **`conejas.lean`** | El 18º: CONEJAS formalizada — `(2^j−2, 2^j−1)` llega al mismo `x = 3t+2` en exactamente `j+2` pasos para todo `j` par (peldaño + escalera por inducción, testigo `3^{j−1} = 4t+3`, vórtice en el repunit); `b(j+2) ≥ 1` con núcleo detrás |
| **`actarevision0908c.txt`** | El acta de la 6ª revisión (la ronda del tronco): Leonas con dos frases corregidas (clase vs instancia; el ancla), Arañas con dos adjetivos («sumable», «diminuta»), Tigresas intacta, Moscas reforzada |
| `actarevision0908.txt` | El acta de la 4ª revisión externa (la que rompió Abejas-como-programa y validó el criterio) |
| **`actarevision1108b.txt`** | **El acta de la 8ª revisión externa** (tres adversarios contra la jornada satelital entera; informes íntegros en `_adv1/2/3.txt`): el récord aguantó, ocho mordidas aplicadas |
| **`actarevision1108c.txt`** | **EL ACTA DE LA 9ª REVISIÓN EXTERNA** (11-08 (2), encargo del usuario: atacar el trasvase V2 → real; informes íntegros en `_adv1/2/3.txt`, instrumentos en `revision9_adv*/`): **el teorema V2/L3 AGUANTA** (verificación exacta en racionales; 3 reparaciones de escritura aplicadas — la identidad de binomiales para (LLT-b), el factor 2, el pago del condicionamiento), **los dos récords aguantan en los números** (φ a 12 decimales por dos caminos; CW 10/10 con pinza propia; la predicción de la 8ª CONFIRMADA en k=36), **la dominación del reloj aguanta como hecho** — y lo escrito mordió: la pieza A de `notadominacion.txt` rota tres veces y reescrita, «una equidistribución» son DOS, la balota era `c₀/2` universal del reloj, «sin letra chica» retirado. 7 correcciones con lección a la base. NOVENA REVISIÓN, NOVENA MORDIDA |
| **`paper_programa_densidad.txt`** | **EL PAPER DE LEGADO** (11-08): el programa entero autocontenido — de dónde venimos (la cadena y sus teoremas), dónde estamos (los dos lemas, la circularidad, las dos vías), adónde vamos (P1–P7 con riesgo), el techo declarado y el método |
| **`paper_cota_renovacion.txt`** | **EL PAPER DE LA COTA** (11-08, candidato a nota externa): `φ ≥ 0,443061` por renovación — enunciado, descomposición en bloques, cómputo exacto, la verificación de la 8ª y lo que NO dice |
| `maquinaria.txt` / `notamoscas.txt` | Los cinco objetivos sin Collatz y la nota autocontenida de Moscas |
| `inventario.md` / `derivados.md` | El catálogo del repo, y las ramas del tronco (sistema de derivados `[D-nn]`) |

**Todo lo de la tabla está trackeado, con UNA excepción:
`.claude/settings.local.json` no está en git** (verificado con `git ls-files`
el 02-08-2026 — son permisos locales de esta máquina, y ni siquiera está en
`.gitignore`: simplemente nunca se añadió). Si esta máquina se pierde, los
permisos se vuelven a conceder a mano; no hay nada más que sobreviva sólo ahí.

> **EL AVISO DE LOS PDF SE CUMPLIÓ, y por eso ya no hay fila para ellos.**
> `.gitignore` ignora `*.pdf`, así que la bibliografía leída (Terras 1976, Tao
> 2019, las dos bibliografías de Lagarias y el libro de 2010) vivía **sólo en
> esta máquina**. Al 01-08-2026 **`lecturas/` ya no existe**, igual que le pasó
> antes a `collazclaude.png`. *Lo que sobrevive es lo que se extrajo de ellos y
> está escrito aquí abajo — que es exactamente la razón de escribirlo aquí.*

## REGLA: el registro de las conversaciones [historia: D-05]

Al cerrar **y a mitad de toda sesión larga**: `python guardarrespuestas.py` (texto → `respuestas.db`, append-only idempotente) + el bloque PowerShell de `transcripciones/LEEME.md` (el `.jsonl` crudo → un zip por sesión, dentro del repo). Para 355 mensajes la base ya es LA ÚNICA copia. **Lo que no está en git no sobrevive** — cobrado tres veces (PDFs, toolchain, transcripciones).

## Lo que se estableció, con verificación [EL ARCHIVO: D-06]

La prosa completa de los resultados y correcciones del 29-07 al 01-08 — la identidad de Terras y sus formas, las DOS correcciones a la cota de ciclos (Laurore, Barina), la lámina y `Res(993)`, la Tabla C, las mallas y las tres ruedas, los once hilos, el criterio de fusión y el **43,5658% demostrado**, la saga OEIS y el teorema del espejo `a₊=a₋`, los negativos = `3n−1`, las constantes con sus trampas de estimador, el piso de la altitud, los récords cruzados, la pinza de ciclos y por qué el barrido está muerto, las cribas industriales — vive ÍNTEGRA en D-06. **El índice canónico con cuantificadores es `afirmaciones.db`** (191 afirmaciones · 63 correcciones con lección · 20 constantes con aviso, al 11-08-2026 (2)); D-06 es la prosa de respaldo.

## La otra mitad de la auditoría y EL ANDAMIO [D-07]

Trece piezas atacadas con implementación independiente y CERO movidas (Terras 1.1/1.2/C1.4, Tabla C, Gao, Wu, A076227, Elia–Tucker, el 5/3 de Everett, Eliahou, Sinisalo, el 1,4784, el Teorema 23). Y EL ANDAMIO — la regla de gestión que dejó: lo que sostiene mucho se delata solo al fallar; **lo que no sostiene nada hay que auditarlo a propósito** (traducciones, atribuciones, prosa: donde vivió un año el error de Everett).

## Nada de esto es nuevo — el balance [D-08]

La tabla honesta de qué era de la literatura y qué encogió al revisarse; Collatz llegó desde teoría de grafos (1932) — nuestro punto de partida era el suyo; la traducción CORREGIDA de Everett (**`B/A > 1,73697`**; el 0,7369 era `1/L − 1`, la marca de un paso de más en el denominador); el techo realista. Y **EL CUARTO CAMINO**, el propósito vigente: *las reglas que generan todos los números de la secuencia sin generar la secuencia*. Un promedio nunca demuestra un caso individual — la pregunta filtro de la casa: **¿es un promedio o es una cota?** ⇢ Al 04-08 el techo SE MOVIÓ: la cadena `(k,c)` ya no es rederivación (ver el banner y `RutaTeoremas.md`).

## El proyecto de fondo y los filtros [D-09]

El filtro del modelo (una malla que devuelve lo mismo para toda entrada mide al modelo, no a la entrada); el segundo filtro (no toda fila A/B discrimina: meterle dos reglas PARECIDAS); y «determinista NO implica patrón encontrable» (`redhilos`: 50% clavado — Terras C1.4; Lagarias: *los argumentos matemáticos explotan la existencia de estructura, no su ausencia*). La maquinita de if/else y por qué los extremos son el peor sitio para buscar ciclos: **un ciclo vive en el centro**.

## Siguiente sesión [FÓSIL HISTÓRICO: D-10]

Esta sección quedó SUPERADA: **el arranque vive en `RutaTeoremas.md` (sección «EL ESTADO Y LOS PRÓXIMOS PASOS») y la bitácora manda sobre cualquier lista vieja.** D-10 conserva la versión histórica (el `k = 34`, el plan de la pinza y Wang, los pendientes del 30-07) por si algún hilo se retoma.
