# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Conjetura de Collatz — laboratorio

Repo de exploración de la conjetura de Collatz (`n/2` si es par, `3n+1` si es
impar; se conjetura que todo `n ≥ 1` termina en 1).

No es una biblioteca ni un paquete. Son programas sueltos, cada uno con su
número configurable arriba del archivo, pensados para ejecutarse y mirar el
resultado. **El código se escribe simple a propósito**: nombres en castellano,
comentarios que explican lo obvio, sin abstracciones.

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

## Instalación

```
pip install -r requirements.txt      # numpy, matplotlib, plotly
```

**Catorce** de los **35** scripts importan `plotly.graph_objects`, y **cuatro**
usan además `plotly.subplots`. Durante mucho tiempo `plotly` faltaba en
`requirements.txt` y el repo no arrancaba en una máquina limpia — ya está
arreglado. `numpy` lo usan **siete**: `viz3d.py`, `clasesfusion.py`,
`clasesparalelo.py`, `densidadfusion.py`, `descensoresto.py`, `pinzaciclos.py` y
`redhilos.py` (la red neuronal a mano). **`matplotlib` solo dos**: `viz3d.py` y
`collazejecucion.py`. Y `sqlite3` lo usan **cuatro** (`guardarafirmaciones.py`,
`guardarhilos.py`, `guardarrespuestas.py`, `mapahilos.py`), pero **ése viene con
Python** y no hay que instalar nada.

> **La proporción que importa: sólo 14 de 35 dibujan.** El repo empezó siendo de
> visualización y hoy la mayoría son programas de cálculo que escupen números por
> stdout. Al escribir uno nuevo, el caso por defecto ya no es plotly.

**Las dos mitades se instalan por separado, y conviene saber cuál te falta.** Al
**01-08-2026**, en el Python 3.14.5 de esta máquina, están las tres:
`numpy 2.4.4`, `matplotlib 3.11.1`, `plotly 6.9.0` — o sea que **ahora corre todo,
incluido lo de matplotlib** (`viz3d.py`, `collazejecucion.py`,
`python main.py graficar`), que durante meses se caía por falta de `matplotlib`.
Si algo de matplotlib falla, lo primero es comprobar que no cambiaste de
intérprete. Para saber qué hay:

```
python -c "import importlib.metadata as m; [print(p, m.version(p)) for p in ['numpy','matplotlib','plotly']]"
```

No hay tests, ni linter, ni `pyproject.toml`, ni CI. No los busques.

**`jq` no está instalado en esta máquina.** Si haces falta parsear JSON en un
hook o en un script de shell, usa `python -c`.

## Las dos mitades del repo

Esto es lo que no se ve leyendo un archivo solo. **Las dos mitades no se hablan
entre ellas**, y es a propósito.

**Mitad A — el motor y su CLI.** `collatz.py` es el único módulo de verdad:
tiene type hints, docstrings y `tabla_de_pasos` con memoización. `main.py`
(argparse) y `viz3d.py` lo importan. Nadie más lo importa.

```
python main.py verificar --limite 1000000    # busca contraejemplos
python main.py records   --limite 10000      # semillas que baten records
python main.py camino    27                  # imprime la trayectoria
python main.py graficar  --paisaje 1000 --coral 3000 [--mostrar]
```

`viz3d.py` es matplotlib y escribe **`.png`** (`paisaje3d.png`, `coral3d.png`).
`main.py graficar` lo importa de forma diferida, solo si se lo pide.

**Mitad B — los programas sueltos (`collaz*.py`, `malla*.py`, `cruzarestos.py`,
`coralcollaz.py`).** Ninguno importa `collatz.py`. Cada uno **redefine su propio
`secuencia_de(n)` de cinco líneas**. Eso es duplicación deliberada: cada archivo
se abre, se lee entero y se ejecuta por sí solo, sin saltar a otro. **No los
refactorices para que compartan el motor** — romperías justamente lo que los hace
legibles. (Ojo: no es *una* función duplicada, son **tres versiones distintas**.
Unas devuelven la lista sola, `collazcruce` devuelve `(valores, colores)`, y
`collazcirculo`/`collazejecucion` la arman con un `while` a nivel de módulo.)

El inventario exacto, para no buscarlo a mano — **diez** archivos definen
`secuencia_de(n)`: `collazarbol`, `collazcruce`, `collazlamina`, `collazmalla`,
`coralcollaz`, `cruzarestos`, `elmasuno`, `guardarhilos`, `mallacollaz`,
`mallascerradas`. **Dos** la arman
inline con un `while` (`collazcirculo`, `collazejecucion`). Y **cuatro no tienen
trayectoria completa** porque no la necesitan: `mallaespejo` y `mallaespejo2`
trabajan con reglas de **un paso** (`collatz(n)`, `T(n)`, `espejo`, `espejo2`),
`mallaresiduos` solo mira el arranque (`patron_de_arranque`), y `mallabasica` es
la malla de control **sin Collatz** de ningún tipo.

Su forma es siempre la misma:

1. Un bloque de comentarios arriba explicando qué se está mirando y por qué.
2. Constantes en MAYÚSCULAS editables (`NUMERO = 221`, `TAMANO_LETRA`, …).
3. Código a nivel de módulo, sin `main()` ni `if __name__`. **Importarlos los
   ejecuta.** No hagas `import collazmalla` para inspeccionarlo: te abre el
   navegador.
4. Los de plotly terminan en `figura.write_html(archivo, auto_open=True)`.

**Excepción obligatoria al punto 3: `clasesparalelo.py` sí lleva
`if __name__ == "__main__"`**, y lo necesita — `multiprocessing` en Windows
reimporta el módulo en cada proceso hijo, y sin el guard el barrido se fork-bombea.
No se lo quites por uniformidad. (`main.py` también lo lleva, pero ése es la CLI y
nunca tuvo la forma de los sueltos.)

Los `.html`, los `.png` y los `.pdf` están en `.gitignore`. **Los `.json` de
`mallas/` no** — son el único resultado que sobrevive a cerrar el navegador, y
están para eso.

**Mitad C — los que no dibujan, y ya son mayoría.** `guardarmallas.py` empezó
siendo *la excepción*; hoy **19 de los 35 no dibujan nada** y sólo 16 abren
navegador o ventana:

```
NO DIBUJAN (19)  clasesfusion, clasesparalelo, collatz, coralprimos, cruzarecords,
                 densidadfusion, descensoresto, elmasuno, espejobases,
                 guardarafirmaciones, guardarhilos, guardarmallas, guardarrespuestas,
                 main, maquinitacollaz, pinzaciclos, pisoaltitud, redhilos, reimpl
DIBUJAN    (16)  los 14 de plotly + viz3d y collazejecucion (matplotlib)
```

Los de la Mitad C no abren el navegador, no tienen `NUMERO`, y su resultado es
**stdout, un `.json`, un `.txt` o un `.db`**. Conservan del resto la constante en
MAYÚSCULAS arriba y las comprobaciones que cortan con `SystemExit`, pero no la
parte de plotly. **Al escribir uno nuevo de cálculo, copiá la forma de
`pinzaciclos.py`, no la de `collazmalla.py`** — y acordate de que la advertencia
de "importarlos te abre el navegador" no aplica a éstos, pero **sí ejecutan el
cálculo entero al importarlos**, que en `clasesfusion.py` son veinte minutos.

**Los scripts nuevos (`malla*`, `cruzarestos`, `coralcollaz`) usan ventana
completa**: sin `width`/`height` fijos, con `autosize=True` y
`default_height="100vh"`. Y ponen los números a dos radios alternados para que
dos vecinos no se pisen. El texto 3D de plotly tiene tamaño fijo en píxeles, así
que al hacer zoom la geometría crece y los números se separan solos.

**Cuidado con `collazmalla.py` y `collazlamina.py` si cambias `NUMERO`:** son
O(L²) con exponenciación de enteros grandes dentro del bucle. Con el 221 (115
números) va instantáneo; con una trayectoria de 500 pasos se arrastra.

## Cómo se ejecuta

Se abre el archivo, se cambia el número de arriba, y se corre
(`python archivo.py`, o Ctrl+B en Sublime Text).

**Sublime Text no acepta `input()`** — el programa se cuelga esperando. Por eso
cada script trae el valor en una constante editable arriba del archivo, nunca
solo `input()`. `collazejecucion.py` es el único que además tiene salida de
emergencia: si `NUMERO_FIJO = None`, prueba `input()` cuando hay tty de verdad y
si no abre una ventanita de tkinter. Al escribir un script nuevo, copia el
patrón de la constante, no el de tkinter. *(Hoy `NUMERO_FIJO` no es `None`: vale
`2213046546463218645`, un número de 19 cifras que quedó de una prueba. La rama de
tkinter está ahí pero no se ejecuta.)*

Los gráficos de plotly se abren solos en el navegador (zoom con la rueda, giro
con el mouse, valores al pasar el cursor).

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
sobre los **35** `.py`: **0 hallazgos**, está limpio — si aparece uno nuevo, lo
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
| `main.py` | CLI: `verificar`, `records`, `camino`, `graficar` |
| `viz3d.py` | Vistas 3D en matplotlib → `.png` (paisaje de trayectorias, coral) |
| `collazejecucion.py` | Una trayectoria como línea de tiempo horizontal (matplotlib, con barra para desplazarse) |
| `collazcirculo.py` | La trayectoria dada la vuelta al globo: ida por delante (F), vuelta por detrás (B) |
| `collazcruce.py` | Dos trayectorias de igual longitud cruzándose sobre una esfera |
| `collazarbol.py` | El árbol de Collatz sobre la esfera: tronco + ramas que brotan en los vórtices |
| `collazmalla.py` | **La malla real**: cada par de puntos en coordenadas (A, B) |
| `collazlamina.py` | **La lámina**: los pares en 3D, todos sobre un plano de grosor 0,23 |
| `mallabasica.py` | Malla de control **sin Collatz**: 100 paralelos × 100 meridianos numerados |
| `mallacollaz.py` | La malla con los números de verdad: eje Y = el 221, eje X = el 1276 |
| `mallaresiduos.py` | **La malla completa de los arranques**: 2^k restos × k pasos |
| `cruzarestos.py` | La malla de restos cruzada contra el 221 y el 1276 |
| `coralcollaz.py` | El coral de Harriss, con la medida de si los puntos calzan |
| `mallaespejo.py` | **El A/B**: la misma maquinaria con dos reglas (espejo base 10 y Collatz) |
| `mallaespejo2.py` | **El espejo en base 2**: las dos identidades exactas, y el A/B/C de tres reglas |
| `mallascerradas.py` | **Los aros que cierran solos** (Pisano, +7, ×2 mod 27) y **la rueda del árbol** |
| `guardarmallas.py` | **Persiste 11 mallas cerradas** en `mallas/*.json`. No dibuja nada |
| `guardarhilos.py` | **Los 11 hilos 100000–100010 en sqlite** (`hilos.db`) y la malla de sus cruces |
| `hilos.db` | La base: tablas `hilos`, `pasos`, `cruces`, `fusiones`, `cola_comun` |
| `mapahilos.py` | **Los once a la vez**, cuatro paneles. La razón de unos lo explica todo |
| `redhilos.py` | **Una red neuronal a mano** (solo numpy) puesta a buscar dónde muere la predicción |
| `densidadfusion.py` | **La conjetura abierta de Wu, medida** hasta 2^28 (tabla vectorizada) |
| `clasesfusion.py` | **El criterio demostrado**: qué clases mod 2^k se funden para todo `m` |
| `sucesiones.txt` | Las dos sucesiones que **no están en OEIS**, con definición y verificaciones |
| `espejobases.py` | **El espejo en 15 bases**: por qué la base 2 es la única con teorema |
| `mallas/*.json` | Las mallas guardadas, **sí versionadas**. `indice.json` lista las once |
| `maquinitacollaz.py` | Escupe los 114 pasos de un número, uno por línea |
| `teoriacollaz.txt` | El planteamiento filosófico del que salió la idea de la esfera |
| `patron detectado manualmente.txt` | Notas a mano sobre las posiciones 57 y 114 |
| `bitacora.md` | **Resumen por sesion y lo que queda pendiente.** Empezar por aqui |
| `clasesparalelo.py` | El barrido de clases repartido entre nucleos. Se verifica solo contra a(30) |
| `pinzaciclos.py` | **La pinza de descarte de ciclos**: un candidato por resto, en cerrado. Barrido de 2^30 restos |
| `records.json` | **Los récords publicados** de Roosendaal y Barina: retraso, altitud, clase, planeo, residuo |
| `cruzarecords.py` | El repo cruzado contra esos récords. Cinco comprobaciones |
| `oeis_borrador.txt` | El envío a OEIS redactado y listo. **No se ha enviado** |
| `resultado_paralelo_k32.txt` | La verificación cruzada de `a(32)`: secuencial y paralelo dan `1.871.137.623` |
| `pisoaltitud.py` | **El piso de la altitud**, con su corrección: vale para `n` impar, y los pares fallan a propósito |
| `elmasuno.py` | **`ε` y `S` son la misma suma**, exacto. El `+1` aparece dos veces, no tres |
| `reimpl.py` | **El Teorema 23 de Hercher reproducido**, 7/7, sin un float en la cadena que decide |
| `coralprimos.py` | El número **primo** de rumbos. La predicción falló y la explicación del 45 se cayó |
| `descensoresto.py` | **El tiempo de descenso contra el resto**. `A076227` reproducida; la criba nunca se vacía |
| `guardarafirmaciones.py` | Escribe `afirmaciones.db`. No dibuja nada |
| `afirmaciones.db` | **Las tres capas**: `afirmaciones` (con cuantificador), `constantes` (con aviso), `correcciones` |
| `guardarrespuestas.py` | Captura las transcripciones de Claude Code y las mete en `respuestas.db` |
| `respuestas.db` | **El cuaderno de las conversaciones.** Tabla `respuestasclaude`, append-only |
| `lecturas/*.pdf` | Terras 1976, Tao 2019 y las dos bibliografías de Lagarias. **NO están en git** |
| `the-ultimate-challenge...pdf` | El libro de 2010 (22 MB). **Tampoco está en git** |
| `.claude/settings.local.json` | Permisos ya concedidos: `python *`, `py *`, `git fetch *` |

Todo lo de la tabla está trackeado **salvo los `.pdf`** y los `.html`/`.png` que se
regeneran. Para comprobarlo: `git ls-files`.

> **AVISO SOBRE LOS PDF (30-07-2026).** `.gitignore` ignora `*.pdf`, así que **la
> bibliografía leída no sobrevive a un clon**: `lecturas/` y el libro de 22 MB
> existen sólo en esta máquina. Es el mismo aviso que tenía `collazclaude.png` —
> que ya se cumplió: **ese archivo ya no existe**, se perdió, y por eso se quitó de
> esta tabla. Si los PDF hacen falta en otra máquina, hay que volver a bajarlos; lo
> que **sí** sobrevive es lo que se extrajo de ellos, que está escrito aquí abajo.

## REGLA: el registro de las conversaciones (`respuestas.db`)

**Las respuestas de Claude en consola traen observaciones, correcciones y
lineamientos que no están en ningún otro sitio.** Se dieron por perdidas más de
cien. El `CLAUDE.md` no puede absorberlas porque crecería sin control, así que
van a su propia tabla.

**No estaban perdidas.** Claude Code guarda la transcripción entera de cada
sesión, literal y con marca de tiempo, en:

```
~/.claude/projects/<ruta-del-proyecto-con-guiones>/*.jsonl
```

> **NO pongas ese slug a mano.** Estuvo fijado a
> `C--Users-Home-Desktop-conjeturadecollazpython` y **el programa no arrancaba en
> ninguna máquina cuyo usuario no fuera `Home`** — el 01-08-2026 se descubrió que
> la regla llevaba una sesión entera sin poder cumplirse, fallando con un
> `SystemExit` que parecía «no hay transcripciones». Ahora `guardarrespuestas.py`
> **deduce el slug del directorio actual** (cambia `:`, `\` y `/` por guiones) y,
> si aun así no la encuentra, busca la carpeta que termine igual que el proyecto.

> **Ojo con la idea de "capturar el stdout": no existe.** El texto del asistente
> no pasa por ninguna consola —Claude Code lo renderiza directo— así que no hay
> nada que redirigir. La transcripción es la única fuente, y por eso es la que
> se lee.

**LA REGLA, en una línea: al cerrar una sesión que haya producido algo, correr
`python guardarrespuestas.py`.**

Eso lee las transcripciones que haya, mete lo nuevo en `respuestas.db` y no
toca lo viejo. Es **append-only** e **idempotente por `(sesion, orden)`**:
correrlo mil veces no duplica ni borra nada. Al **01-08-2026** lleva **643
mensajes de seis sesiones — 152 preguntas y 456 respuestas, 1.065.063
caracteres**, desde el 29-07.

**Por qué se hace así y no anotando turno a turno:** una regla que exige que el
asistente escriba una fila en cada respuesta depende de que la cumpla siempre, y
eso se degrada. Leer la transcripción al final no depende de nadie y además sale
**literal** en vez de reconstruido.

**Las columnas de análisis van vacías a propósito.** `tipo`, `resumen`,
`hallazgos`, `decisiones` y `ficheros` quedan `NULL` al capturar y se llenan
después, leyendo la fila. Rellenarlas automáticamente sería inventar, y mezclaría
el registro crudo con su interpretación — que es justo lo que el resto del repo
se cuida de no hacer. La columna `origen` separa `capturado` (de la
transcripción, con hora exacta) de `reconstruido` (escrito después, de memoria).

*Esta base rompe a propósito la regla de que las bases se regeneran
(`guardarmallas.py`, `guardarhilos.py`). Un registro histórico no se regenera: si
algún día se limpian las transcripciones viejas, ésta será el único sitio donde
queden.*

## Lo que se estableció, con verificación

Todo lo de abajo se comprobó ejecutando código, no razonando.

**La identidad entre pares.** Para cualquier par de posiciones `i < j` de una
trayectoria, contando `A` = veces que se aplicó `3n+1` y `B` = veces que se
aplicó `n/2` en el tramo:

```
2^B · seq[j]  =  3^A · seq[i]  +  C
```

donde `C` se actualiza `C → 3C + 2^B` en cada paso impar y no cambia en los
pares. Comprobado en **los 6.555 pares** de la trayectoria del 221: **0 fallos**.

> **Es el Teorema 1.1 de Terras (1976)**, publicado en forma cerrada:
> `T^k n = λ_k(n)·n + ϱ_k(n)` con `λ_k = 3^{S_k}/2^k`. Multiplicando por `2^k`
> queda nuestra identidad, y `2^k ϱ_k` es nuestro `C`.

**El único ciclo es una ecuación.** El ciclo `1 → 4 → 2 → 1` escrito con esa
identidad da `A=1, B=2, C=1`, o sea **`2² = 3¹ + 1`** → **`4 = 3 + 1`**.
Buscando ciclos escondidos en los 6.555 pares aparecieron 95 candidatos enteros
positivos; los 95 ciclan de verdad y son `n ∈ {1, 2, 4}` dando 1, 2 o 3 vueltas.
Cero impostores. *(Esto no es evidencia de nada: la literatura de 2025 exige que
cualquier otro ciclo mida ≥ 19.478.780.533 pasos, y nuestro tramo más largo mide
114. La búsqueda no podía encontrar nada.)*

**Es una lámina, no una esfera.** Puestos los pares en (tamaño de salida, tamaño
de llegada, desviación del equilibrio), los 6.555 caen entre `0` y `0,2286` por
encima del plano `desviación = salida − llegada`. **Ninguno cae por debajo.**
Grosor = 1,1% del espacio. Ese grosor es exactamente la contribución de los
`+1`: con `3n` en vez de `3n+1` sería cero.

> **Y el grosor tiene nombre.** Sobre trayectorias enteras el mismo objeto es
> `ε = ln( 2^B / (3^A·n) )`, y `2^B/(3^A·n)` es el **residuo de Roosendaal**.
> Su máximo conocido es **`Res(993) = 1,253142144`**, verificado por Roosendaal
> para todo `x < 2^32` y **conjeturado máximo absoluto**. Su logaritmo:
>
> ```
> ln(1,253142144) = 0,225654
> ```
>
> Barrido propio hasta 200.000 con `Fraction` exacto: `ε` **nunca sale
> negativo** y su máximo es exactamente ese, alcanzado en `n = 993` (y en
> `1986`, `3972`, … que son el mismo número doblado). **El 0,23 de la lámina no
> salió de nuestro dibujo: es una constante con conjetura propia.**
>
> Y de ahí sale la identidad que gobierna los once hilos (`mapahilos.py`):
> `γ(n) = 1/(ln2 − ρ·ln3)` con corrección exacta `B·ε / (ln n·(ln n + ε))`,
> donde `ρ = A/B` es la razón de unos. **La razón de unos ES el hilo**: dos
> números con la misma `ρ` tienen el mismo `γ` y los mismos pasos.

**Los vórtices.** Un número tiene dos padres si y solo si deja resto 4 al
dividirlo entre 6 (el segundo padre es `(v−1)/3`). Es la regla estándar de la
literatura. La trayectoria del 221 tiene 50 vórtices en sus 115 números.
*(En `collazarbol.py:padres()` el 4 se excluye a mano — su otro padre es el 1, que
ya es el arranque del tronco. Es decisión de dibujo, no de aritmética.)*

**El balance decide todo.** El punto de equilibrio es `log₂(3) = 1,585`
divisiones por multiplicación. El 221 tiene `73/41 = 1,78` → cae. Por debajo de
1,585 subiría; justo encima giraría en círculo.

**El 221 falla por ocho.** Un ciclo con `A=41` necesitaría `B=65` (y `65/41` es
una de las mejores aproximaciones fraccionarias a `log₂(3)`). El 221 tiene 73.
Le sobran 8 divisiones, que son el mismo `+8,02` de desviación medido, que es a
su vez el logaritmo del 221.

**Dónde podrían esconderse otros ciclos.** Barriendo 480 casillas `(A,B)`, las
que quedan en pie son exactamente las **convergentes y semiconvergentes de la
fracción continua de `log₂(3)`** — comprobado en las 10 más cercanas, todas sin
excepción. Para esconder un ciclo por encima de lo verificado (2^71, Barina 2025)
haría falta que `2^B` coincidiera con `3^A` hasta la cifra 22.

> **Esto es la Tabla C de Terras (1976), literalmente.** Sus *jump values* son
> los `k` donde `3^⌊kγ⌋ / 2^k` bate récord acercándose a 1 por debajo, con
> `γ = 1/log₂3`. Recalculado aquí con `Fraction` exacto:
>
> ```
> k (= nuestro B):  1, 2, 5, 8, 27, 46, 65, 149, 233, 317, 401, 485, 1539, 2593
> b (= nuestro A):  0, 1, 3, 5, 17, 29, 41,  94, 147, 200, 253, 306,  971, 1636
> ```
>
> **La fila 7 es `(A=41, B=65)`** — el mismo par que este repo encontró para el
> 221. Terras la tabuló hace cincuenta años, y la usó para excluir bucles hasta
> periodo **2592**. La lista entera son las convergentes y semiconvergentes de
> `γ`, exactamente como se rederivó aquí.

### El 1276 y la mitad del 221

**La trayectoria del 1276 ES la segunda mitad de la del 221.** El 1276 es la
posición 57, y `seq(221)[57:] == seq(1276)` da **True**. No son dos objetos: el
1276 es la cola del 221. Los dos tienen el mismo pico, 9.232, porque comparten
ese tramo.

**Pero partirse por el medio no es un patrón. Es contabilidad.** Si `n` tarda `S`
pasos, el número de la posición `k` tarda `S − k`; entonces el de la posición
`S/2` tarda `S/2`. Siempre. Comprobado en **los 10.011 números del 2 al 20.000
con cantidad par de pasos: 10.011 lo cumplen, 0 excepciones.** El 221 solo tuvo
la suerte de tener 114 pasos, que es par.

Y eso explica las notas a mano: **9784 tarda 135 pasos, 87090 tarda 195, 2734182
tarda 125 — los tres impares.** No tienen medio exacto, y por eso en
`patron detectado manualmente.txt` quedaban sobras (el 244 debiendo 21 pasos, el
52 debiendo 11). Todas las cadenas de esas notas son composición de función:
`pos57(pos57(n)) = pos114(n)`, nada más. Y dónde cae la posición 114 lo decide
`(114 − pasos(n)) mod 3`, porque desde el 1 se entra al carrusel `1-4-2` de
período 3: da 0 → aterrizas en 1, da 1 → en 4, da 2 → en 2.

### La malla de los arranques (`mallaresiduos.py`)

**Los primeros `k` pasos de cualquier número los decide `n mod 2^k`.**
Comprobado con números de verdad: 64 restos × 12 representantes = 768 números,
**0 discrepancias**. Esto es un espacio finito que cierra solo, sin forzar nada:
el módulo es circular por definición, `2^k` y `0` son el mismo resto.

**Y aquí las dos versiones de la regla dan cosas distintas. Importa mucho:**

- **Con atajo (`(3n+1)/2` en los impares): biyección perfecta.** Los `2^k` restos
  dan los `2^k` patrones posibles de par/impar, uno cada uno. Comprobado de
  `k=1` a `k=10`, exacto las diez veces. Detalle bonito: el resto 0 es `PPPPPP` y
  el resto `2^k−1` es `IIIIII` — los dos extremos absolutos, y son **vecinos**,
  porque el eje cierra.
- **Con la regla clásica (`3n+1`): NO hay biyección, y salen los Fibonacci.**
  Después de `3n+1` el resultado es siempre par, así que **dos impares nunca van
  seguidos**, y eso prohíbe la mayoría de los patrones. Los que sobreviven son
  **F(k+2)**: `k=4→8=F(6)`, `k=6→21=F(8)`, `k=8→55=F(10)`, `k=10→144=F(12)`.
  Comprobado en los diez. **Fibonacci no se metió a mano: sale de que dos impares
  no puedan ir juntos.**

**Con atajo, en cada paso exactamente la mitad de los restos toca impar** (32 de
64, los seis pasos). De ahí sale el `log₂(3)`.

**LOS DOS MAPAS NO SE PUEDEN MEZCLAR.** Con el mapa del atajo **el 1276 no
aparece en la trayectoria del 221** — la ruta es otra y toda la estructura del
paso 57 se cae. El atajo da la biyección; la clásica da el 221. Cada malla vive
en su regla.

### El cruce restos × 221 (`cruzarestos.py`)

**La malla predice.** Calculada sin mirar el 221 ni una vez (cada resto usa un
representante ajeno a las trayectorias), acierta el arranque de **los 173 números
del 221 y del 1276: 0 fallos.** Los dos lados se calcularon por separado y
coinciden en todo.

### El coral de Harriss (`coralcollaz.py`)

**De quién es.** Es el **Collatz Seaweed** de **Edmund Harriss** (U. de Arkansas),
salido en Numberphile con Alex Bellos, del libro *Visions of Numberland*. La
regla, textual: *"si el paso actual es el doble del siguiente, gira una cantidad
fija en sentido horario; si no, gira **la mitad** de esa cantidad en antihorario"*.
Par → `+θ`, impar → `−θ/2`. Se dibuja **al revés**, del 1 hacia afuera, y por eso
las trayectorias que comparten final comparten tronco.

**El rumbo de cada rama solo depende de (A, B).** Los giros se suman y da igual
el orden: `rumbo = A · θ_impar + B · θ_par`. Comprobado: **730 pares (A,B), 0 con
rumbo ambiguo.** Y `(A, B)` son exactamente las coordenadas de `collazmalla.py`:
los rumbos del coral **son** esa malla pasada a ángulos.

**La punta de cada rama la fija `n mod 2^k`.** 64 restos, 0 con dos versiones. La
malla de `mallaresiduos.py` es la punta de este coral. Los tres objetos —malla
(A,B), malla de restos, coral— son el mismo objeto mirado de tres formas.

**Si los puntos calzan depende de cuántos rumbos permiten los ángulos** (3.000
semillas, 6.520 ramas):

| par | impar | rumbos | posiciones | encimadas |
|---|---|---|---|---|
| 16° | −8° (Harriss) | 45 | 6.520 | **0%** ← *sólo hasta 3.000 semillas, ver abajo* |
| 7° | −17° (el de `viz3d`) | 357 | 6.520 | **0%** |
| 60° | −30° | 13 | 3.497 | 46% |
| 90° | −45° | 9 | 1.476 | 77% |
| 120° | −60° | 6 | **221** | **97%** |

Con 120°/−60° hay 6 direcciones posibles, el paseo cae en una retícula hexagonal
y por el principio del palomar los puntos **tienen** que repetirse. Es cierre de
verdad, **pero lo trae el ángulo elegido, no Collatz.** Collatz pone el paseo; el
ángulo pone el cierre.

#### El umbral de los 45 rumbos: el `0%` era falso (30-07-2026)

Esto resuelve el punto 1 de "Siguiente sesión" y **corrige la fila de arriba**. El
`0%` de Harriss no era una propiedad del ángulo: era el resultado de mirar sólo
3.000 semillas.

**Con `16°/−8°` sí hay choques. Dos umbrales, según qué se pregunte:**

| pregunta | respuesta |
|---|---|
| primer `HASTA` con choque | **10.452** (y la semilla culpable es el propio 10.452) |
| segundo choque | `HASTA` = 25.527 |
| **primera profundidad con choque** (árbol inverso completo) | **31** |
| choques a profundidad 59 | **39.831** en 3.121.576 nodos |
| tasa a partir de la profundidad 42 | **1–1,5% de los nodos de cada nivel** |

Los dos umbrales son distintos y los dos son ciertos: barrer por semillas sólo ve
las ramas que cuelgan de semillas chicas, y por eso el primer choque parece estar
en 10.452; barriendo el **árbol inverso completo** aparece en la profundidad 31,
con cero choques hasta la 30 inclusive, exhaustivo.

**Y son coincidencias exactas, no ruido de coma flotante.** Cada arista es una raíz
45-ésima de la unidad, así que dos ramas caen en el mismo punto **si y sólo si**
`Φ₄₅(x) = x²⁴ − x²¹ + x¹⁵ − x¹² + x⁹ − x³ + 1` divide al polinomio diferencia en
`Z[x]`. Los dos primeros pares dan **resto exactamente cero** en aritmética entera,
sin un solo float; recalculada a 60 dígitos, la distancia real es `8,9·10⁻⁵⁹`. Lo
que se medía como `1,4·10⁻¹⁴` era el error de sumar 35 cosenos.

**No son choques triviales:** los `(A,B)` son distintos en los dos pares —`(9,26)`
contra `(6,23)` y `(45,85)` contra `(40,81)`— y los rumbos finales también. No es
el caso degenerado de "mismo `(A,B)`, misma posición".

**La causa que se le atribuyó — `45 = 3² · 5` — era casi toda falsa.** Lo que se
escribió: el retículo de relaciones enteras entre las 45 raíces tiene rango
`45 − 24 = 21`, generado por el **triángulo** (`e_k + e_{k+15} + e_{k+30} = 0`,
tres direcciones a 120°) y el **pentágono** (cinco a 72°); luego el cierre lo
traería la conmensurabilidad del ángulo, no Collatz.

> ### ⇢ CORREGIDO por `coralprimos.py`: el `45 = 3²·5` explicaba UN nivel de 31
>
> La parte reticular **es cierta y quedó medida**: con `N` primo el único núcleo
> es `(1,1,…,1)`, y en todos los primos del barrido la clave cruda y la clave
> reducida módulo `Φ_N` dan **el mismo número, sin una excepción**. Ninguna
> relación no trivial entre raíces ayuda nunca.
>
> **Pero el motor de los choques no son las relaciones entre raíces.** Es el caso
> trivial que el razonamiento se dejó fuera: **dos ramas que usan las mismas
> aristas en otro orden.** Diferencia de vectores exactamente cero, ninguna
> relación de por medio, y **existe para cualquier `N`**. Sale de que una tirada
> larga de pasos pares recorre el círculo entero de direcciones y vuelve a pisar
> las mismas que la otra rama pisó en otro orden.
>
> **La cuenta que lo cierra:** con `N = 45` el triángulo y el pentágono adelantan
> el choque **un solo nivel**. El 45 habría chocado casi igual siendo primo.
> Atribuirle el choque a su factorización era **quedarse con la causa de un nivel
> e ignorar la de treinta y uno.**
>
> **Lo que sí gobierna el umbral es una recta en `N`, con dos ramas según
> `N mod 4`** — `(N+19)/2` si `N ≡ 1`, `(N+11)/2` si `N ≡ 3`. No sabe nada de si
> `N` es primo.

Conclusión para la pregunta que se hizo, y **ésta sí aguanta**: **45 rumbos NO
bastan para un árbol infinito.** El coral de Harriss sí se vuelve a juntar; lo
que pasa es que tarda. Lo que se cayó fue el *porqué*, no el *qué*.

**De dónde sale la forma, y cómo se apaga.** En el coral **63,43% de los pasos
son pares y 36,57% impares** → **1,7345 divisiones por multiplicación**, por
encima del equilibrio.

> **CUIDADO: el `1,7345` no es una constante, es el valor de una muestra**
> (30-07-2026). Se midió a `HASTA = 3.000`; con más semillas se mueve y se asienta
> en **`1,7320 ± 0,0003`**: `10³`→1,7292 · `3·10³`→1,7345 · `10⁴`→1,7338 ·
> `10⁵`→1,7321 · `10⁶`→1,7321. La cuarta cifra nunca fue estable. Y cae a 0,02% de
> `√3 = 1,7320508`, que es **el tipo exacto de coincidencia que este repo se ha
> propuesto no creerse**: la descomposición del valor dice que es casual. No
> construir nada sobre esa cifra.

Con `16°/−8°` eso da un **giro medio de +7,22° por paso**:
una vuelta completa cada 50 pasos, y la rama más larga (216 pasos) da 4,3 vueltas.

Y entonces —esto se **predijo antes de medirlo**— la espiral debe anularse
exactamente cuando `impar/par = −1,7345`, o sea `par +8°, impar −13,876°`.
Confirmado: giro medio **−0,0001°**. Y la forma se da vuelta:

| | Harriss 16/−8 | Nulo 8/−13,876 |
|---|---|---|
| giro medio | +7,22°/paso | −0,0001°/paso |
| radio a 25 pasos | 9,40 | 23,28 |
| radio a 200 pasos | **12,20** | **175,69** |
| radio / pasos | cae a 0,061 | constante en 0,93 |
| forma | **acotada** (se enrolla) | **se expande** (lineal) |

O sea: **el coral de Harriss no está en expansión, está acotado.** Una rama de 200
pasos termina casi tan cerca del centro como una de 25, porque las profundas se
enrollan. Lo que parece expansión es enrollamiento. La versión que sí se expande
es la de ángulos nulos, y el número que la controla (1,7345) lo pone Collatz.

*Aviso de lectura: el 50/50 de los restos y el 63/37 del coral son los dos
ciertos y miden poblaciones distintas. Los restos reparten parejo sobre todos los
enteros; el coral cuenta nodos del árbol, donde doblar siempre existe y `(n−1)/3`
solo a veces. Por eso el árbol se puebla más de pares.*

### El espejo: la contraparte (`mallaespejo.py`)

La idea es el **complemento a diez**, el que usaban las calculadoras mecánicas
para restar: `espejo(n)` = la potencia de 10 más chica que supera a `n`, menos
`n`. Al 7 le faltan 3 para llegar a 10; al 99876 le faltan 124 para llegar a
100000.

**El cierre es aritmética pura, sin un solo parámetro que tocar:**

```
n + espejo(n) = 10^k     exacto, siempre
```

221+779=1000 · 47+53=100 · 1276+8724=10000 · 124+876=1000.

**Y todo cierra, sin conjetura.** De 1 a 100.000: **99.969 caen en 2-ciclos y 31
en puntos fijos.** Nada se escapa, y se demuestra en dos líneas: `espejo(n) < 10^k`
así que la órbita está acotada, y solo puede bajar de década un número finito de
veces. **44.450 ciclos distintos** bajo 100.000; Collatz tiene **uno**.

- **Puntos fijos: exactamente `5·10^m`** — 5, 50, 500, 5000, 50000. Uno por
  década, porque `n = 10^k − n` da `n = 10^k/2`.
- **Clasificación exacta: "baja de década" ⟺ "empieza con 9".** Con exactamente
  5 excepciones, y las 5 cuadran solas: 9, 90, 900, 9000, 90000 forman 2-ciclos
  con 1, 10, 100, 1000, 10000.
- **Involución en el 88,89%**: cada número tiene exactamente una pareja.
- Las colas miden **≤ 4**. Todo el sistema se resuelve en ≤ 6 pasos.
- **Regalo geométrico:** como `n + espejo(n) = 10^k`, al plotear `(n, espejo(n))`
  cada década cae **exacta sobre la recta `x + y = 10^k`**. El pool no es una
  nube, son segmentos rectos anidados. Y en el círculo de `mallaespejo.py` eso se
  traduce en **cuerdas paralelas**: `n` y `10^k−n` caen en ángulos simétricos
  respecto del mismo eje. Cero grados de libertad.

**EL A/B, que es para lo que sirve de verdad.** Misma maquinaria, mismo círculo,
mismo ángulo, misma cuerda por paso — cambiando solo la regla (N = 1.000):

| | ESPEJO | COLLATZ |
|---|---|---|
| ciclos distintos | **448** | **1** |
| puntos fijos | 3 (`5, 50, 500`) | 0 |
| cola más larga | 2 | 176 |
| cola media | 0,12 pasos | 57,55 pasos |
| pasos que se escapan del rango | **0,1%** | **33,3%** |

**La maquinaria discrimina:** lo que dibuja depende de lo que se le mete, no de
cómo dibuja. Eso hay que tenerlo verificado antes de creerle nada a estas mallas.

El contraste estructural: **el espejo es cerrado bajo su propio rango, Collatz
no.** El espejo nunca sale de su década; Collatz se escapa hacia arriba un tercio
de las veces (los impares con `3n+1 > N`). Por eso uno cierra en 2 pasos con
cientos de aros y el otro tarda 57 de media hacia un solo sumidero.

### El espejo en cualquier base, y por qué la base 2 es la rara (`espejobases.py`)

El repo tenía dos espejos sueltos —base 10 y base 2— y los trataba como dos
casos. Son la misma familia. Mirando las quince bases de 2 a 16 a la vez
(200.000 números cada una) aparece la razón de que la base 2 se porte distinto.

**Los puntos fijos salen de una línea.** `n` es punto fijo si `n = b^k − n`, o
sea `n = b^k/2`, y eso es entero **si y solo si la base es par**:

```
base par    ->  puntos fijos exactamente (b/2) · b^m
base impar  ->  NI UNO. Cero puntos fijos, en cualquier rango.
```

Comprobado en las 15 bases, **0 fallos**. La forma limpia es `(b/2)·b^m`:

| base | primero | la lista |
|---|---|---|
| 2 | **1** | 1, 2, 4, 8, 16, 32 … (las potencias de 2) |
| 4 | 2 | 2, 8, 32, 128, 512 … |
| 6 | 3 | 3, 18, 108, 648, 3888 … |
| 8 | 4 | 4, 32, 256, 2048, 16384 … |
| **10** | **5** | **5, 50, 500, 5000, 50000** |
| 12 | 6 | 6, 72, 864, 10368 … |
| 14 | 7 | 7, 98, 1372, 19208 … |
| 16 | 8 | 8, 128, 2048, 32768 … |

Los `5, 50, 500, 5000, 50000` no son una peculiaridad del diez: son el caso
`b = 10` de `(b/2)·b^m`. Y las potencias de 2 son el caso `b = 2`, donde
`b/2 = 1`.

**Y la parte que importa: la base 2 es la única en la que el espejo está
obligado a bajar.** Si `b^(k−1) ≤ n < b^k`, entonces `b^k − n` cae en
`(0, b^(k−1)·(b−1)]`. Con `b = 2` ese tope es `2^(k−1)`: la imagen **no cabe**
en la década de partida, así que baja siempre. Con `b ≥ 3` el tope es al menos
`2·b^(k−1)`, y sí cabe — de ahí los 2-ciclos.

Consecuencia medida: **de las quince bases, la 2 es la única sin ni un
2-ciclo.** Base 2: 0 números en 2-ciclos. Base 10: 199.969.

> Que el espejo de base 10 diera un zoo (44.450 ciclos) y el de base 2 diera un
> **teorema** (todo cae en potencia de 2, demostrado en una línea) no fue
> suerte ni elección afortunada. Es la única base donde puede haber teorema.
> Y es la base en la que vive Collatz.
>
> *Lo que esto NO dice: nada sobre la conjetura. El espejo base 2 conmuta con
> Collatz un paso y se rompe al segundo (correlación +0,06). Que las dos cosas
> vivan en base 2 las hace parientes, no la misma.*

### El espejo en base 2: el único puente exacto (`mallaespejo2.py`)

El espejo de base 10 no hablaba con Collatz porque Collatz es base 2. Así que se
cambia de base: `espejo2(n)` = la potencia de **2** más chica que supera a `n`,
menos `n`. Y eso es lo mismo que **`−n` módulo `2^k`** — la misma estructura que
ya sabíamos que gobierna el arranque de Collatz (`mallaresiduos.py`).

**Dos identidades exactas. 100.000 comprobaciones, 0 fallos:**

```
n PAR  :   T(2^k − n)  =  2^(k−1) − T(n)          (50.000 casos, 0 fallos)
n IMPAR:   T(2^k − n)  =  3·2^k + 2 − T(n)        (50.000 casos, 0 fallos)
```

**La de arriba dice algo fuerte: en los pasos pares el espejo2 CONMUTA con
Collatz.** Espejar y después dividir entre dos da lo mismo que dividir y después
espejar (bajando un nivel). El espejo2 **es una simetría de la mitad par de
Collatz**. Con base 10 no pasaba nada parecido.

**La de abajo dice dónde se rompe: en los impares casi conmuta, pero sobra un
`+2`.** Y ese `+2` es el `+1` del `3n+1` arrastrado:
`3(2^k − n) + 1 = 3·2^k + 2 − (3n+1)`. Es el mismo estorbo que ya aparecía como
el grosor 0,23 de la lámina en `collazlamina.py`.

*Honestidad sobre la profundidad: son dos líneas de álgebra. Exactas y útiles,
pero verdaderas por construcción, igual que la identidad `(A,B)`. No tocan la
conjetura.*

**Todo cae en una potencia de 2, y está demostrado.** De 1 a 100.000:
`largos de ciclo: {1: 100000}` — **ni un solo 2-ciclo**, todos caen en punto fijo,
y los 17 puntos fijos son exactamente `2^m`. Se demuestra en una línea: si
`2^(k−1) < n < 2^k` entonces `2^k − n < 2^(k−1)`, o sea que baja estrictamente.
Es el análogo **demostrado** de "todo cae en el 1". Colas de hasta 16, media 7,48.

**Y los dos sistemas mueren en el mismo conjunto:** los puntos fijos del espejo2
son las potencias de 2, y la cola de toda trayectoria de Collatz es una tirada de
potencias de 2 — la del 221 termina en `[16, 8, 4, 2, 1]`.

**El A/B/C, misma maquinaria y solo la regla cambiada (N = 1.024):**

| | espejo 10 | espejo 2 | Collatz |
|---|---|---|---|
| ciclos distintos | 472 | 11 | **1** |
| puntos fijos | 3 | 11 | 0 |
| cola más larga | 2 | 9 | **176** |
| cola media | 0,11 | 4,00 | **57,88** |
| se escapan del rango | 2,4% | **0,0%** | **33,3%** |

Tres reglas, tres mallas distintas. El espejo2 queda en el medio: más
Collatz-like que el de base 10 (tiene colas de verdad, un solo tipo de
sumidero), pero cerrado y demostrado.

> **CORRECCIÓN AL PROTOCOLO DEL A/B (30-07-2026): la fila "se escapan del rango"
> NO discrimina.** Aquí parece que sí, pero es un espejismo: separa a los espejos
> de Collatz sólo porque los espejos están **acotados por construcción**. Entre dos
> reglas del mismo tipo no separa nada. Medido con `3n+1` contra `3n−1`, a cuatro
> tamaños: `N=256` → 33,20% las dos · `N=1024` → 33,30% las dos · `N=4096` →
> 33,33% las dos · `N=10.000` → 33,33% las dos. **Los mismos conteos absolutos,
> no sólo los mismos porcentajes.** Se escapan los impares con `3n±1 > N`, y el
> `±1` casi nunca cambia de lado del corte a un impar: **esa fila mide el rango,
> no la regla.** Las que sí discriminan son "ciclos distintos", "cola más larga" y
> "cola media". *Lección general: no toda fila de una tabla A/B vale como
> discriminante, y hay que comprobar cuál vale antes de apoyarse en ella.*

### Los aros que cierran solos, y la rueda del árbol (`mallascerradas.py`)

Esta pieza ejecuta el plan original del laboratorio: mallas circulares
independientes de Collatz, cruzadas después contra Collatz.

**Parte 1 — cada progresión trae su aro, medido caminando:**

| regla | cierre medido |
|---|---|
| `n → n+7` (mod 30) | 30 (= 30/mcd) |
| Fibonacci (mod 10) | 60 (Pisano; mod 100 da 300) |
| `n → 2n` (mod 3^j) | 2, 6, 18, 54, 162 para j=1…5 (= 2·3^(j−1)) |
| `n → n²` (mod 100) | **no cierra limpio**: 6 ciclos de largos {1,4}, colas hasta 2 |

Cuatro cierres distintos → la maquinaria discrimina (el requisito del filtro).

**Parte 2 — la coincidencia exacta que buscaba el plan.** El árbol de Collatz
se construye hacia atrás **doblando**, y doblar módulo m es una de esas
progresiones cerradas. Comprobado en 200 rayos hasta k=44, **0 fallos en todo**:

- **El ritmo de brotes es periódico de período 2** (el aro de 2 mod 3):
  `v` múltiplo de 3 → el rayo **nunca** brota (67 rayos mudos); resto 1 → brota
  exactamente en k pares (67 rayos); resto 2 → exactamente en k impares (66).
- **Los hijos ciclan `1 → 2 → 0` con período 3** (el aro de 4 mod 9): 2.926
  brotes, 2.793 transiciones, 0 fallos. La clase del hijo la fija
  `2^k·v mod 9` con la tabla `{1:0, 4:1, 7:2}`.
- **La rueda maestra: el patrón completo de cualquier rayo se repite cada 18
  duplicaciones** — y 18 es el orden de 2 módulo 27, el mismo aro de la parte 1.
  Ese aro recorre los 18 números no múltiplos de 3 y evita `[0,3,…,24]` — los
  mismos múltiplos de 3 que en el árbol hacen rayos mudos. El eco es exacto.
- **Contra los datos viejos:** los 50 vórtices del 221 cumplen la regla de la
  rueda, 0 fallos.

**Es la primera vez en el laboratorio que un ciclo gobierna la dinámica de
Collatz sin que lo pongamos nosotros**: no es un ángulo elegido ni una esfera —
es el aro de 2 módulo 3, engranado con el de 4 módulo 9, dentro del de 2 módulo
27. La coincidencia de patrón entre una malla cerrada independiente y Collatz
existe y es exacta, brote a brote — no estadística.

### Las mallas guardadas (`guardarmallas.py`, carpeta `mallas/`)

El paso que faltaba del plan original: **guardarlas**. Once mallas circulares,
ninguna calculada con Collatz, escritas en `mallas/<nombre>.json` y versionadas.
Ya no hay que recalcularlas: se abren con `json.load` y se cruzan.

Cada archivo trae `orbita` (el anillo en orden), `aro`, `cola`, `visitados`, y
**`evitados`** — los números del `0` al `módulo−1` que el anillo no pisa. Ese es
el campo que sirve para cruzar.

**El juicio se mide, no se supone.** De cada regla se recorre el espacio entero,
no solo el arranque, y se parte en anillos y colas:

```
cierra_limpio  =  (la cola más larga de todo el espacio es 0)
```

O sea: la regla cierra limpio si y solo si es una biyección. Diez de las once lo
son; `n → n²  (mod 100)` no, y por eso hace renacuajos (cola 2, aro 4). **Se
guarda igual: sin ella la colección no discriminaría nada.**

| malla | aro | cierra | evita |
|---|---|---|---|
| `n+7` mod 30 | 30 | sí | 0 de 30 |
| `n+6` mod 30 | **5** | sí | 25 de 30 |
| `n+1` mod 12 | 12 | sí | 0 de 12 |
| Fibonacci mod 10 | 60 | sí | 0 de 10 |
| Fibonacci mod 100 | 300 | sí | 0 de 100 |
| `2n` mod 3 / 9 / 27 / 81 | 2 / 6 / 18 / 54 | sí | los múltiplos de 3 |
| `3n` mod 10 | 4 | sí | 6 de 10 |
| `n²` mod 100 | 4 | **no** | 96 de 100 |

**10 tamaños de cierre distintos en 11 mallas** — el filtro se cumple.

**Y las cuatro comprobaciones cortan con `SystemExit` antes de dar nada por
guardado:** (1) cada aro coincide con su fórmula; (2) los cierres salen
distintos; (3) **ida y vuelta** — los 11 archivos se releen del disco y tienen
que salir idénticos a lo calculado, 0 fallos; (4) el cruce, **leyendo del
archivo y no de memoria**: los `evitados` de `duplicar-mod27.json` son
exactamente los múltiplos de 3, y usando **solo** ese archivo se predice cuáles
de 200 rayos del árbol son mudos — **67 predichos, 0 fallos**. Una malla
guardada predice Collatz sin volver a calcular Collatz.

*Los JSON son ASCII puro a propósito* (`2*3^(j-1)`, no `2·3^(j-1)`): este repo
ya tiene un historial de líos con cp1252, y un archivo de datos no es lugar para
arriesgarlo.

**Los dos límites honestos:** (1) es matemática conocida — la estructura
mod 6 / mod 9 del árbol inverso es estándar; se llegó de forma independiente.
(2) La rueda gobierna la **contabilidad del árbol hacia atrás** (dónde brota,
qué clase de hijo). El destino hacia adelante sigue ciego a los restos — el
negativo de `cruzarestos.py` sigue en pie. Las dos cosas son ciertas a la vez:
**el esqueleto es periódico, el viaje no.**

### Los once hilos y el cruce por índice de paso (`guardarhilos.py`, `hilos.db`)

Los once números `100000 … 100010`, cada uno hasta el 1, en sqlite; y cada paso
de cada hilo cruzado contra cada paso de todos los demás. La pregunta no es
*qué valor sale* sino **en qué paso sale**.

**Lo que hay ahí:**

| n | pasos | pico |
|---|---|---|
| 100000, 100008, 100010 | **128 los tres** | ≤ 150.016 |
| 100001 | 89 | 300.004 |
| **100002 … 100007** | **53 los seis** | ≤ 854.368 |
| 100009 | **309** | **35.075.104** |

Seis consecutivos con 53 pasos exactos no es casualidad: **se funden**. Y se
funden **con desfase cero** — paso 18 contra paso 18, paso 26 contra paso 26.

**El número que resume todo: de los 983 cruces que no son cola común, 833
(el 85%) tienen desfase 0.** Y 18 de las 55 parejas se funden en desfase 0.
Comparar por índice de paso no es una manera de mirar entre otras: es donde
está casi toda la estructura.

**La trampa, medida y separada.** Las once trayectorias comparten la cola
`[16, 8, 4, 2, 1]` por obligación. 275 de los 1.258 cruces son eso y no
significan nada. `hilos.db` marca cada cruce con `es_cola` para que el ruido
no se cuente como hallazgo. *(Ejemplo de por qué importa: `100001` no se funde
de verdad con nadie — todos sus "cruces" son la cola. Es el único hilo
solitario de los once, y sin la marca parecería tan conectado como el resto.)*

**Esto tiene nombre y bibliografía desde 1985 — no es nuestro:**

- **Garner (1985)**: hay infinitos pares de consecutivos con la misma altura y
  el mismo tiempo de parada total; la prueba es exactamente el estudio de cómo
  se funden los consecutivos.
- **Gao (1993)**: si existe **una** tupla de `k` consecutivos con la misma
  altura, existen infinitas. Hay una de **35.654** empezando en `2^500 + 1`.
- **Wu Jia-Bang (1992, 1993, 1995)**: la tupla más larga bajo `2^30` mide
  **176** y empieza en `722.067.240`; encontró otra de **310** en
  `6.622.073.000`. Nuestro 6 es minúsculo en comparación.
- **Wu y Huang (2001)**: las familias de pares que se funden son progresiones
  aritméticas módulo `2^k`, y publicaron los ejemplos `(32m+5, 32m+6)`,
  `(64m+45, 64m+46)`, `(128m+29, 128m+30)`.
  > **CITA SIN VERIFICAR (30-07-2026).** No se pudo confirmar esta referencia: no
  > tiene DOI, no aparece en Crossref, y **Elia–Tucker 2015 no la citan** — su
  > bibliografía entera son cuatro entradas (Garner 1985, Lagarias, LaTourette
  > 2007, Terras 1976). O la cita está mal copiada de algún sitio, o el trabajo
  > existe pero es de difícil acceso. **Antes de apoyarse en ella hay que
  > localizarla o quitarla.** Lo que sí está verificado por Crossref: Terras 1976,
  > Garner 1985, Lagarias 1985, Gao 1993 y Elia–Tucker (INTEGERS 15 (2015) #A54).
- **Oliveira e Silva** usa la fusión de `n` y `n−1` como optimización
  industrial de su criba de verificación: le quita el **17,5%** de las hojas.

**La comprobación 4 cierra el círculo.** `100005 = 32·3125 + 5`, así que
nuestro par `(100005, 100006)` **es un caso de la primera familia publicada**.
Comprobado en `m = 1, 2, 7, 100, 3125, 9999, 40000`: **todos se funden en el
paso 6 contra el paso 6, desfase 0, sin excepción.** La literatura predijo
nuestro hallazgo veinticinco años antes de que lo miráramos.

**Y el mecanismo general estaba en Garner 1985**: `8k+4` y `8k+5` se funden
siempre en 3 pasos; y si dos trayectorias se funden, entonces
`2^r·k + n₁` y `2^r·k + n₂` se funden **para todo `k`** — una sola fusión
genera una progresión aritmética infinita de fusiones. Eso es exactamente lo
que produce los bloques de pasos iguales.

### La conjetura abierta de Wu Jia-Bang, medida (`densidadfusion.py`)

De todo lo leído de la literatura, **esto es lo único que quedó abierto y al
alcance de medir**. El resto son teoremas de 1976–2005.

**Cuidado con la palabra "altura".** En la literatura de Collatz, `h(n)` es el
**número de pasos** hasta llegar al 1, no el valor más alto. El valor más alto
se llama *excursión máxima* `t(n)`. Wu habla de *"consecutive numbers of the
same height"*, así que su magnitud es la de los pasos.

**La conjetura (Wu Jia-Bang, 1995):** demostró que una versión condicionada de
la densidad de pares consecutivos con la misma altura **crece** con `N`, y
conjeturó sin demostrarlo que la versión sin condicionar también crece.

**Medido hasta 2^28 = 268.435.456.** La tabla de alturas es `int16` (los pasos
no pasan de ~700 en este rango) y se construye **vectorizada por bloques**: se
avanza un bloque entero un paso a la vez y, en cuanto un número cae por debajo
del inicio del bloque, ya está resuelto. Un bucle de Python sobre 268 millones
tardaría media hora; esto tarda un par de minutos. *(Verificado contra la
versión lenta en los primeros 300.000: **0 discrepancias**.)*

| 2^N | d(altura) | 2^N | d(altura) |
|---|---|---|---|
| 2^10 | 0,364614 | 2^23 | 0,495086 |
| 2^14 | 0,423305 | **2^24** | **0,500265** |
| 2^18 | 0,463060 | 2^26 | 0,509861 |
| 2^21 | 0,483710 | 2^27 | 0,514313 |
| 2^22 | 0,489504 | **2^28** | **0,518577** |

**Monótona en los dieciocho escalones. Cero bajadas.** La conjetura de Wu
aguanta en todo el rango medido.

**Y hay un segundo hito.** Garner (1985) conjeturó que *"la mayoría de los
enteros positivos tienen la misma altura que un entero adyacente"*. La densidad
**cruza el 50% entre 2^23 y 2^24**, y en 2^26 va por **50,99%**. La mayoría ya
está cruzada.

**El control que importa: no todas las nociones de "parecerse" se portan
igual.** La misma medición con el **pico** en vez de la altura **NO es
monótona**: baja de 0,1887 a 0,0671 hasta 2^20 y luego remonta. Diez bajadas de
dieciséis. Que la de la altura suba en todos los escalones no es un artefacto
de la maquinaria — la maquinaria discrimina.

**Las tuplas crecen** (rachas de consecutivos con la misma altura):

```
2^10:   7      2^20:  40      2^25:  96
2^13:  17      2^22:  52      2^26:  96
2^16:  25      2^23:  65      2^27:  98   (en 98.041.684)
2^18:  27      2^24:  77      2^28: 120   (en 136.696.632)
```

Wu (1992) reporta **176** bajo 2^30, empezando en 722.067.240. Nuestro **120 en
2^28** es compatible con esa trayectoria de crecimiento, pero no la confirma:
no llegamos.

*Aviso, por delante: medir que una sucesión crece en dieciséis puntos NO
demuestra que crezca siempre. Esto no resuelve la conjetura de Wu. Lo único que
podía hacer era darle crédito o quitárselo — y si hubiera salido no monótona,
eso sí habría sido un resultado.*

#### El mecanismo, y dónde encajan las dos familias publicadas

Partiendo los pares por el resto del menor, la tasa de coincidencia **no es
uniforme en absoluto**: va del **9%** al **100%**. Hay clases donde el par
coincide *siempre*.

```
mod  8 :  siempre -> {4}                                  1 de 8   = 0,125
mod 16 :  siempre -> {2, 4, 12}                           3 de 16  = 0,188
mod 32 :  siempre -> {2, 4, 5, 12, 18, 20, 22, 28}        8 de 32  = 0,250
mod 64 :                                                 18 de 64  = 0,281
```

**Y las dos familias publicadas caen dentro, exactamente:**

- **resto 4 mod 8** → es el `8k+4` y `8k+5` de **Garner 1985**, que se funden
  siempre en 3 pasos. Sale tasa **1,0000**.
- **resto 5 mod 32** → es la familia `(32m+5, 32m+6)` de **Wu y Huang 2001**.
  Sale tasa **1,0000**.

Ése es el motor de la conjetura: al crecer `N` entran en juego clases módulo
`2^k` cada vez mayores, y la fracción de clases que coinciden siempre crece.
Los peores restos son `31` (9%), `0` (15%) y `15` (16%).

> **Aviso de sesgo.** Al doblar el módulo, la muestra por clase se parte por la
> mitad, así que con pocos ejemplos una clase de tasa 0,99 se mide como 1,000.
> **Ese sesgo está eliminado abajo: el criterio se puede demostrar.**

#### El criterio demostrado, sin muestrear (`clasesfusion.py`)

De la identidad de Terras sale un criterio **exacto y finito** que decide, de
una vez y para los infinitos `m` de la clase, si `(2^k·m + r, +1)` se funden.

Poniendo `n = 2^k·m + r` en `T^k(n) = λ_k·n + ρ_k`, y usando que `λ_k` y `ρ_k`
dependen **solo del resto** (Teorema 1.2):

```
T^k(2^k·m + r)  =  3^{S_k(r)} · m  +  T^k(r)
```

Es una **recta en `m`**, con pendiente `3^{S_k(r)}` y ordenada `T^k(r)`, y las
dos dependen solo de `r`. Luego las dos trayectorias coinciden en el paso `k`
**para todo `m`** exactamente cuando:

```
S_k(r) == S_k(r+1)      (misma pendiente)
T^k(r) == T^k(r+1)      (misma ordenada)
```

Una comprobación finita que vale para infinitos números. Verificado contra
fuerza bruta en 9.672 pares: **0 fallos**.

**Las dos familias publicadas se rederivan en tres líneas:**

```
r=4, k=3:  T^3(4)=2, S=1   |  T^3(5)=2, S=1   -> Garner 1985 (8k+4, 8k+5)
r=5, k=5:  T^5(5)=2, S=2   |  T^5(6)=2, S=2   -> Wu-Huang 2001 (32m+5, 32m+6)
```

**Y la fracción sale exacta, sin muestrear.** El cálculo va **en bloques** de
4 millones de restos con solapamiento de uno (el array entero a `k = 26` serían
537 MB y los temporales del paso lo llevan a 3-4 GB); verificado contra la
versión sin trocear en `k = 3…20`, y también con bloques de 8 para forzar que
casi todo par cruce frontera: **idéntico en los 18 valores**.

| k | clases buenas | fracción | k | clases buenas | fracción |
|---|---|---|---|---|---|
| 3 | 1 | 0,125000 | 22 | 1.715.546 | 0,409018 |
| 5 | 8 | 0,250000 | 24 | 6.966.495 | 0,415235 |
| 10 | 351 | 0,342773 | 26 | 28.247.507 | 0,420921 |
| 16 | 25.241 | 0,385147 | **32** | **1.871.137.623** | **0,435658** |

Es una **cota inferior demostrada**: al menos el **43,57%** de los pares
consecutivos tienen la misma altura, y se decide mirando solo el resto módulo
2^28. *(Eso sí es un resultado: no depende de muestreo ni de ajuste.)*

> **CORRECCIÓN, y estuvo publicada mal.** Una versión anterior de esta sección
> presentaba *"la fracción crece en los 24 escalones"* como un hallazgo. **No
> lo es: está forzado**, y se demuestra en tres líneas.
>
> Si `r` es buena módulo `2^k`, entonces `r` y `r + 2^k` son **las dos** buenas
> módulo `2^{k+1}`. Con `m = 1` en la fórmula: `T^k(2^k + r) = 3^{S(r)} +
> T^k(r)`, e igual para `r+1`; si `r` era buena las dos salidas coinciden.
> Y si `r` es buena a nivel `k`, sus dos iterados **ya son el mismo número**,
> así que sigue siendo buena a nivel `k+1`.
>
> Luego `N(k+1) ≥ 2·N(k)` **siempre**, y por tanto `f(k+1) ≥ f(k)`. La
> monotonía no se verifica: se demuestra. Y la razón `> 2` también es trivial.
> Comprobado además a mano en 14 niveles: **0 fallos**.

La densidad real medida es 0,5186 a 2^28. **La diferencia (unos 10 puntos) son
los pares que se funden pero cuya clase no se funde entera** — coincidencias
que dependen del `m` concreto, no solo del resto.

#### Hacia dónde va la fracción: la pregunta, ya limpia

Como cada clase buena se desdobla en dos, lo único con contenido es cuántas
clases **se estrenan** en cada nivel:

```
f(k+1) − f(k)  =  nuevas(k) / 2^{k+1}       y       f(∞) = f(k) + Σ nuevas(j)/2^{j+1}
```

| k | N(k+1) | heredadas | **nuevas** | razón de nuevas |
|---|---|---|---|---|
| 17 | 103.358 | 102.210 | 1.148 | 1,8427 |
| 20 | 850.737 | 843.286 | 7.451 | 1,8802 |
| 23 | 6.966.495 | 6.915.582 | 50.913 | 1,8973 |
| 25 | 28.247.507 | 28.060.738 | 186.769 | 1,9180 |
| 26 | 56.854.178 | 56.495.014 | 359.164 | 1,9230 |
| 27 | 114.400.435 | 113.708.356 | 692.079 | 1,9269 |
| 28 | 230.136.995 | 228.800.870 | 1.336.125 | 1,9306 |
| 29 | 462.857.658 | 460.273.990 | 2.583.668 | 1,9337 |
| 30 | 930.718.308 | 925.715.316 | 5.002.992 | 1,9364 |
| 31 | 1.871.137.623 | 1.861.436.616 | 9.701.007 | **1,9390** |

**Toda la pregunta se reduce a la razón de crecimiento de `nuevas`.** Si se
queda **por debajo de 2**, la suma converge y la fracción tiene un límite `< 1`.
Si llega a **2**, diverge y la fracción tiende a **1** — y entonces casi todo
par consecutivo tendría la misma altura por razón de resto.

Con estos datos la razón **sube sin estabilizarse y sin dar señal de techo**
(1,8427 → 1,9269 en diez escalones), así que **no se puede decidir**. Es el
mismo muro, pero ahora formulado sobre una sucesión de enteros en vez de sobre
un ajuste de ley de potencias, que es una forma más honesta de no saberlo.

#### Y las dos sucesiones no están en OEIS

Comprobado con **ocho consultas** (la sucesión entera, un prefijo, desplazada,
extendida, la ampliada hasta `k = 28`, y tres variantes de la segunda).
**Todas devuelven "No results".** Control con los Fibonacci: devuelve
`A000045`, o sea que la consulta funciona y el "no results" es real.

```
a(k) = clases mod 2^k que se funden   1, 3, 8, 18, 39, 82, 170, 351, 721, …
       …, 462857658, 930718308, 1871137623         (k = 3 … 32)

b(k) = a(k+1) − 2·a(k)  (las nuevas)  1, 2, 2, 3, 4, 6, 11, 19, 34, 60, …
       …, 2583668, 5002992, 9701007                (k = 3 … 31)
```

Los términos, la definición, la demostración del criterio y las cuatro
verificaciones están en **`sucesiones.txt`**, y el envío queda redactado en
**`oeis_borrador.txt`** con los campos de OEIS ya montados. **No se ha enviado
nada, y de momento no se va a enviar** — la decisión requiere una cuenta y una
firma que son de una persona, no de este repo.

**Reverificado el 30-07-2026 con 28 consultas** (12 numéricas para `a`, 11 para
`b`, más variantes de texto), con control de Fibonacci que devolvió `A000045`
las dos veces: **siguen sin estar**. Un falso positivo que conviene anotar: el
prefijo corto de `b` (`1,2,2,3,4,6`) casa con `A001611` y cinco más, pero
ninguna sigue con `11,19,34`; con ocho términos ya no devuelve nada. *Los
prefijos cortos de sucesiones que empiezan lento casan con cualquier cosa.*

> **Lo más cercano que sí existe, y hay que citarlo: `A076227`, "Number of
> surviving Collatz residues mod 2^n".** Misma familia de objetos —restos módulo
> `2^k` filtrados por un criterio de Collatz— con un conteo distinto. Y tiene
> **actividad reciente** (julio de 2026, preprints sobre vectores de paridad), o
> sea que esta esquina del problema está viva y con gente mirándola. También
> existe `A341362` (primer número de una racha de `n` consecutivos con la misma
> altura), que es el objeto de Wu contado por el otro lado.

> **Qué significa "no está en OEIS", y qué no.** Es evidencia real de que
> **nadie las ha catalogado**. **No** es evidencia de que sean matemáticamente
> nuevas: el criterio del que salen está publicado (Wu–Huang 2001; Elia–Tucker
> 2015 lo enuncian casi textual), así que cualquiera que lo implementara podía
> contarlas. Parece que nadie lo hizo, o nadie pensó que mereciera enviarse.
>
> Es lo único de toda la sesión que no está ya registrado en algún sitio. Es
> modesto —una entrada de catálogo, no un teorema— pero es real y es
> comprobable. **Verificado cuatro veces:** contra fuerza bruta (9.672 pares),
> vectorizado contra sin trocear, con bloques de 8 para forzar fronteras, y con
> una implementación independiente en Python puro (`k = 3…16`, 0 discrepancias).

*(El intento anterior — ajustar `e(k) ~ C/k^p` y extrapolar — daba `p ≈ 1,45` y
un límite ≈ 0,606, pero la estimación **se movía al añadir puntos** (0,594 con
`k ≤ 24`, 0,606 con `k ≤ 25`). Un estimador que se desplaza con la muestra no
es una predicción.)*

### Los negativos son el mapa `3n−1` (30-07-2026)

No hay fichero: todo esto se midió en scripts sueltos, y está aquí porque el
resultado sí importa. **Collatz sobre los enteros negativos es exactamente el mapa
`3m−1` sobre los positivos.** Dos líneas: si `n = −m`, par → `n/2 = −(m/2)`;
impar → `3n+1 = −3m+1 = −(3m−1)`.

Comprobado paso a paso para `m` de 1 a 100.000: **8.095.665 pasos comparados, 0
fallos**, con dos implementaciones que no comparten una línea (una con `Fraction`,
otra separando signo y magnitud, ninguna dividiendo un negativo). *Aviso para quien
copie esto: `-7 // 2 == -4` estorbaría, pero el floor nunca actúa sobre un impar
porque los impares no dividen, multiplican.*

**Hay exactamente tres ciclos, y ningún cuarto.** Verificado por tres caminos
independientes (cerrar en positivo, cerrar en negativo, y detección de ciclo de
Brent), y barrido hasta 1.000.000 con 0 sin clasificar:

| ciclo | largo | cuánto atrae |
|---|---|---|
| `[−1, −2]` | 2 | 32,8% |
| `[−5, −14, −7, −20, −10]` | 5 | 32,3% |
| `[−17, −50, −25, … , −34]` | 18 | 34,9% |

**El A/B discrimina** (N = 1.024): `3n+1` da 1 ciclo y cola media 57,88; `3n−1` da
3 ciclos y cola media 25,20 — converge en menos de la mitad de pasos porque tiene
tres sumideros en vez de uno. *(La fila "se escapan del rango" empata en las dos;
ver la corrección al protocolo, más arriba.)*

**Lo que sí es un hallazgo estructural: las dos reglas viven en lados opuestos de
`log₂(3)`, y es forzoso.** En un ciclo de `3n+1` la constante `C` de la identidad
del repo es **positiva**, luego `2^B > 3^A`, luego `B/A > log₂(3)`. En un ciclo de
`3n−1` la `C` es **negativa** y todo se invierte. Comprobado en los tres ciclos
negativos y en el único positivo, 0 fallos. **El "el balance decide todo" se parte
en dos mitades: `3n+1` sólo puede ciclar por encima del equilibrio, `3n−1` sólo por
debajo.**

Y el ciclo de `−1` escrito con la identidad del repo da **`2 = 3 − 1`**, el espejo
exacto del `4 = 3 + 1`. Los tres `B/A` negativos son `1/1`, `3/2` y `11/7`: los tres
convergentes de la fracción continua de `log₂(3)` — *que no es hallazgo nuevo, es el
mismo mecanismo de las 480 casillas, y sirve como comprobación de consistencia entre
las dos mitades del laboratorio.*

**Estado de novedad: nada de esto es inédito.** Los tres ciclos negativos son
estándar en la literatura; lo que aporta la sesión es la verificación con conteos y
el A/B.

### Las constantes de Collatz (30-07-2026)

Salió de preguntar si existe "la constante de Collatz". **Existe, y varias.** Todas
medidas sobre trayectorias de 2 a 10⁷.

| constante | valor teórico | medido | error |
|---|---|---|---|
| **Wagon** (tiempo de caída medio, tiene entrada propia en OEIS) | **9,4779555565593** | 9,471872 | **−0,064%** |
| hermana de la anterior (conteo reducido) | 3,4926518521864 | 3,49031 | −0,067% |
| media geométrica por paso del atajo, `√3/2` | 0,8660254 | 0,8643758 | −0,190% |
| pasos impares contra `ln(n)`, `1/ln(4/3)` | 3,4760595 | 3,46363 | −0,35% |
| pasos del **atajo** contra `ln(n)`, `2/ln(4/3)` | 6,9521189 | 6,93247 | −0,28% |
| pasos **clásicos** contra `ln(n)`, `3/ln(4/3)` | **10,4281785** | 10,3961 | −0,31% |
| divisiones por multiplicación, `B/A` | **2** | 2,014002 | +0,70% |

**La escalera 1 : 2 : 3 es la misma constante mirada de tres formas** — un bloque
impar cuesta 1, 2 o 3 pasos según se cuenten sólo los `3n+1`, los del atajo o los
clásicos. **Ojo con la atribución:** `2/ln(4/3) = 6,952` es la del **atajo**, no la
del mapa clásico; el clásico es `3/ln(4/3) = 10,428`. Confundirlas da un 49,5% de
error.

**Y `B/A` converge a 2, no a `log₂(3)`.** La raíz es que la valuación 2-ádica media
de `3n+1` vale 2 (porque `P(v=k) = 2⁻ᵏ`): medido **1,99048** sobre 4.041.132 saltos.
El `log₂(3) = 1,585` es el punto de *equilibrio*, no el valor *típico*; son dos
números distintos y no se contradicen.

**TRAMPA DE ESTIMADOR, anotada porque mordió:** la media de las razones `B/A`
trayectoria por trayectoria da **2,174** (+8,7%, no coincide), porque promedia un
cociente con denominador chico y por Jensen se va hacia arriba. El estimador
correcto es el **agregado** `Σ B / Σ A`. La misma trampa reapareció en el ajuste
fino: pesar por pasos y pesar por números dan cosas distintas.

### El ajuste fino: por qué el 3 y no otro (30-07-2026)

Regla generalizada `qn+1` con `q` impar. En el mapa del atajo cada paso multiplica
por `q/2` o por `1/2` mitad y mitad, así que la media geométrica es `√q/2` y el
sistema debería converger sólo si `q < 4`. Medido sobre 100.000 semillas por cada
`q`, con topes de 10⁴⁰ y 10.000 pasos:

| `q` | cae | se dispara | ciclos |
|---|---|---|---|
| 1 | 100% | 0% | 1 |
| **3** | **100%** | **0%** | **1** |
| 5 | 3,03% | 96,97% | 3 |
| 7 | 0,16% | 99,84% | 1 |
| 9, 11, 13 | **0%** | **100%** | **0** |

**Como `q` tiene que ser impar, el 3 es el único valor que converge.** Robusto: con
topes de 10²⁰, 10⁴⁰ y 10⁸⁰ los porcentajes salen idénticos a la milésima.

**PERO el `4,0019` medido no es evidencia independiente, y hay que decirlo.** Se
comprobó que `media = q^f / 2` **exactamente** (desviación máxima 0,00009), donde
`f` es la fracción de pasos impares. Entonces "media = 1" es *idéntico* a `f = 1/2`,
y `f = 1/2` es Terras 1976, que ya estaba anotado como demostrado. **La precisión
del 0,048% mide con qué exactitud recuperamos una densidad conocida, no el umbral.**
El fenómeno (el 3 es especial) es real; el número no es un descubrimiento.

*Honestidad obligatoria: que `5n+1` diverja no está demostrado — es tan conjetural
como Collatz. Lo medido es lo medido. La literatura (Kontorovich–Lagarias) predice
para `5x+1` que sólo `≈ x^0,65` enteros bajo `x` llegan a 1.*

### Collatz contra la moneda (30-07-2026)

El argumento heurístico estándar de por qué Collatz debería ser cierta **es** un
modelo de moneda, y viene de Terras/Everett vía Lagarias. Medirlo dio la
comparación más útil de la sesión.

**Fracciones de paridad, todas las trayectorias de 2 a 10⁶:**

| | atajo | clásico |
|---|---|---|
| fracción impar medida | **0,496524** | **0,331785** |
| predicción | 0,500000 | 0,333333 |

La relación entre los dos mapas es **exacta**: los pasos impares coinciden dígito a
dígito (43.607.946 en los dos) y los pares del clásico son pares + impares del
atajo. El par forzado existe uno por uno, no en promedio.

**Dónde Collatz ES una moneda perfecta:** la entropía de bloques de `k` paridades da
**exactamente `k` bits** para `k = 1…12`, sin un solo bloque faltante — la biyección
resto↔patrón medida como información. Y **sigue dando 12 bits a profundidad 128**:
el proceso no se degrada. 300 trayectorias de semillas de 2000 bits pasan el test de
rachas con `z` medio **+0,020**; el control con `random.Random` da **−0,077**.
Indistinguibles.

**Dónde no lo es, y es brutal:**

- Con el mapa clásico `P(impar | impar) = 0` **exacto**, en 3,3 millones de
  oportunidades. Es la prohibición que genera los Fibonacci, medida directamente.
- La desviación **no se encoge como `1/√N`**: `|desv|·√N` va 1,45 → 1,05 → 1,76 →
  3,62 → **13,02** de 10³ a 10⁷ pasos. Firma de sesgo fijo, no de ruido. El 0,5
  queda a **26 sigmas**.
- **El patrón se puede encargar:** `2^4000 − 1` da 3.999 pasos impares seguidos y
  `2^4000 + 1` da 4.000 alternando. Una moneda produce eso con probabilidad `2⁻⁴⁰⁰⁰`.

**Pero el sesgo no es del proceso, es de la muestra, y se va con el tamaño:**

| bits de la semilla | 16 | 32 | 64 | 128 | 256 |
|---|---|---|---|---|---|
| desviación de 0,5 | −0,0044 | −0,0020 | −0,0015 | −0,0006 | −0,0007 |

**Collatz converge a la moneda justa agrandando la semilla, no acumulando tiradas.**
Ésa es la diferencia exacta con una moneda física.

**Y el origen del sesgo es OTRA VEZ el `+1`**, cerrado con una identidad exacta
(residuo `1,7·10⁻⁷`):

```
−Σ ln(n)  =  I·ln(3/2) + P·ln(1/2) + S ,    S = Σ ln(1 + 1/(3x)) sobre los impares
```

Despejando: sin el sobrante `S` la fracción impar daría 0,497877; **con** `S` da
**0,496064**, que es exactamente lo medido.

> **CORREGIDO por `elmasuno.py`: este `S` y el grosor de la lámina no son dos
> apariciones del `+1`, son UNA.** Se creyó que el `+1` salía en tres sitios
> distintos (grosor `0,2286`, el `+2` del espejo base 2, y este `S`). Pero
> `ε = ln(2^B/(3^A·n))` y `S = Σ ln(1 + 1/(3x))` son **el mismo objeto, término a
> término, idénticamente** — porque en un paso impar el factor es
> `(3x+1)/x = 3·(1 + 1/(3x))`. Verificado con `Fraction` exacto, 20.011 casos.
> **El `+1` aparece dos veces, no tres**, y la lámina queda *demostrada* para todo
> `n` en vez de medida.

**La grieta, formulada:** la fracción impar queda **determinada** por cuánto bajó la
trayectoria y cuántos pasos tardó, y sólo se puede medir en trayectorias **que ya
terminaron en 1**. O sea que el `1/2` no es una ley del proceso sino una
consecuencia contable de haber llegado al final: **el argumento de la moneda asume
lo que habría que demostrar.**

*Contexto bibliográfico, buscado y verificado:* el estudio de la moneda es Bartoš et
al., 350.757 lanzamientos con 48 personas, publicado en JASA 2025 — `Pr(mismo lado
que empezó) = 0,508`, pero `Pr(cara) = 0,500` exacto. El sesgo es **condicional a la
condición inicial** y se anula al marginalizar. Fue **predicho en 2007** por
Diaconis–Holmes–Montgomery desde la mecánica de la precesión, que ya midieron 0,508
con fotografía de alta velocidad. **La analogía con Collatz sale al revés de lo
esperado:** condicionada a su lado inicial la moneda queda *sesgada* (50,8%);
condicionado a `n mod 2^k`, Collatz queda *determinado al 100%*. **La moneda es una
moneda cargada con multiplicadores simétricos; Collatz es una moneda justa con
multiplicadores asimétricos.** El `√3/2` **no** es un sesgo de moneda — confundirlos
sería el error central.

### El piso de la altitud: lo único con forma de teorema (30-07-2026)

Buscando por qué unos números se disparan y otros caen de hocico, se predijo que
`log₂(altitud/n)` crecería con la racha inicial de impares con pendiente
`log₂(3/2) = 0,585`. **La predicción falló como se escribió y acertó donde importa:**
la correlación es **0,59**, no la 0,8 que se exigía — la racha explica el 35% de la
varianza, no el 80%. Pero la **pendiente** da **0,5837**, y leída sobre las medianas
da `+0,5850` **once veces seguidas**, de `k=1` a `k=11`.

**Y el hallazgo real no es una tendencia, es una cota:**

```
PARA n IMPAR:   log₂(altitud(n) / n)  ≥  racha(n) · log₂(3/2) + 1
                99.999 casos, 0 fallos, holgura mínima +0,000002
```

Se demuestra en una línea (`k` pasos impares del atajo llevan `n` a al menos
`3^k·n / 2^(k−1)`). **La racha no predice la altitud: le pone un piso exacto**, y el
piso es ajustado para la mayoría. Es lo único de la sesión con la forma de un
teorema en vez de la de una medición, y por eso vale más aunque diga menos.
*(El `+1` del enunciado es `log₂(2)` y viene de mezclar mapas: con el mapa del atajo
el piso es `racha · log₂(3/2)` sin el `+1`, y ése **sí vale para las dos paridades**.)*

> **CORRECCIÓN (30-07-2026, misma sesión): al enunciado le faltaba la hipótesis
> `n impar`, y sin ella es FALSO.** Con `n` par la racha vale 0, el piso exige
> `altitud ≥ 2n`, y eso **falla en 28.325 de los 50.000 pares** de 1 a 100.000
> — el 10, por ejemplo, sube sólo hasta 16 y necesitaría 20.
>
> **Lo que hay que aprender de cómo apareció:** el error **no lo encontraron los
> casos extremos**. Se probó el piso contra los 243 récords publicados de
> Roosendaal y Barina —los números que más suben y más tardan de todo lo
> conocido— y **pasaron los 243**. Los 15 récords pares pasan **por casualidad**,
> porque son `2 × impar`. Quien lo cazó fue el **barrido de control** sobre
> números corrientes. *Los extremos confirman; los controles refutan. Es el
> mismo argumento que sostiene la doctrina del A/B de este repo, aparecido solo.*

### Los récords publicados, y el repo cruzado contra ellos (`records.json`, `cruzarecords.py`)

30-07-2026. En vez de generar números, **traer los que ya generaron otros** y usar
el repo contra ellos. Son los casos extremos de Collatz: los que más suben y los
que más tardan de todo lo conocido.

| tipo de récord | registros | fuente |
|---|---|---|
| retraso (delay) | 149 | OEIS A006877/A006878 + ericr.nl |
| altitud (path) | 98 | Barina + OEIS A006884/A006885 + ericr.nl |
| clase | 2.425 | ericr.nl |
| planeo (glide) | 34 | ericr.nl |
| completitud y residuo | 39 | ericr.nl |

**Verificación cruzada entre fuentes independientes:** la lista de `n` de los
récords de altitud, Barina contra OEIS — **98/98 idénticos**; las alturas contra
A006885, 96/97 (la excepción es el trivial `n=2`). Y **las 98 altitudes y los 148
retrasos publicados se recalcularon desde cero con enteros exactos: 0
discrepancias.** Lo que no está en dos fuentes va marcado en el JSON.

**Trampas técnicas que costaron tiempo y conviene tener anotadas:**

- **`ericr.nl` sirve un certificado TLS inválido.** `WebFetch` fuerza HTTPS y
  falla siempre; `curl -k` funciona. Wayback está bloqueado.
- **Barina publica la altitud en el mapa del ATAJO** — la clásica es exactamente
  el doble. Confundirlo habría corrompido el cruce en silencio, sin error visible.
- Los **4 récords nuevos** de Barina son las cuatro entradas de 71 bits
  (`1378299700343633691495`, `1735519168865914451271`, `1765856170146672440559`,
  `2358909599867980429759`). Roosendaal le atribuye cinco; el quinto es de 68 bits
  y de su tanda anterior.

**Los cinco cruces:**

1. **El piso de la altitud: 243/243, 0 fallos**, comprobado en forma entera exacta
   (`alt·2^r ≥ 2n·3^r`, sin floats). *Pero el control encontró que al enunciado le
   faltaba una hipótesis — ver la corrección de la sección anterior.*
2. **El residuo de Roosendaal: 0 por debajo de 1 y 0 por encima de `1,253142144`,
   hasta `2^71`.** Roosendaal sólo lo verificó hasta `2^32`, así que **esto es
   evidencia nueva para su conjetura**. Máximo hallado 1,2486 en `n=9`; confirmado
   que `4164943872 = 993·2^22` tiene el mismo residuo que el 993.
3. **El balance `B/A`: 0 récords por debajo de `log₂(3)`.** La predicción se
   confirmó —los récords están **3,3 a 4,7 veces más cerca** del equilibrio que el
   control, con `z` de 24 a 33— **pero el mecanismo que se había supuesto era
   falso.** No es que "subir mucho exija pocas divisiones". La identidad exacta
   `B/A − log₂3 = (ln n + ln Res)/(A·ln 2)` (verificada a `5,6·10⁻¹⁷`) dice que
   **depende sólo de `A`**: los récords están cerca del equilibrio por ser
   **largos**, no por ser **empinados**. La prueba está en el propio dato — los
   récords de *retraso*, que son los más largos, son los que caen más cerca.
4. **La constante de parada** se rompe hacia arriba, como debe: récords de retraso
   **4,25×** lo normal, de altitud **2,81×** (control 10,02 y 10,22, que reproduce
   el 10,396 medido antes).
5. **La fracción impar** también sube (0,3684 y 0,3755 contra 0,331785, a 21 y 38
   sigmas) — **pero no es un hallazgo independiente**: `f = 1/(1 + B/A)` exacto, o
   sea que es el cruce 3 escrito en otras coordenadas. *Anotado para no contarlo
   dos veces.*

**Veredicto: nada de lo que el repo midió se rompe en los casos extremos.** Las
dos cotas demostrables aguantan con cero fallos, y las dos tendencias
estadísticas se desvían hacia arriba exactamente en la dirección y la magnitud
previstas. La única corrección fue de enunciado, no de medición — y la encontró
un control, no los récords.

### La pinza de descarte de ciclos (`pinzaciclos.py`, 30-07-2026)

Junta cuatro piezas que vivían sueltas: la identidad de Terras, la tabla de
convergentes, el barrido de restos y los negativos. De la identidad
`T^k(2^k·m + r) = 3^{S(r)}·m + T^k(r)` y de la condición de ciclo `T^k(n) = n`
sale, despejando:

```
m = (r − T^k(r)) / (3^{S(r)} − 2^k)
```

**Por cada resto hay como mucho UN candidato, y se calcula en cerrado.** Si `m`
no es entero, esa clase queda descartada para los infinitos números que contiene.

**Barrido de 2.147.483.646 restos (`k = 1…30`), en bloques.** Supervivientes
positivos: **`n = 1` y `n = 2`, y nada más.** La predicción escrita antes de
medir se cumplió. Verificaciones que cortan con `SystemExit`: fórmula de Terras
contra iteración cruda (10.000 casos, 0 fallos), el ciclo trivial presente en los
15 `k` pares y ausente en los impares, fuerza bruta hasta 100.000, y una
implementación independiente en Python puro sin numpy — 0 discrepancias.

**Lo que no se buscaba: la ecuación no mira el signo de `m`.** Un `m` negativo
también es solución y da un `n` negativo que cicla, así que el barrido resuelve
el problema **sobre todo `Z`** sin proponérselo. Recupera los cuatro ciclos de
Collatz sobre los enteros sin que se le hable nunca de negativos:

```
dividen(k) = 2 + 2·[2|k] + 3·[3|k] + 11·[11|k]
```

**0 desacuerdos en los 30 valores de `k`, y 0 restos sin explicar en los 2.147
millones.** Cada superviviente es un punto de `{0}`, `{1,2}`, `{−1}`,
`{−5,−7,−10}` o `{−17,…,−34}`. La casilla `(A,B) = (7,11)` de la tabla de
convergentes predijo el ciclo de periodo 11 antes de encontrarlo, y el lado
descartado de la tabla (`2^B < 3^A`) resultó ser exactamente `B/A = 1/1, 3/2,
11/7` — los tres ciclos de `3n−1`.

**Y AQUÍ EL RESULTADO QUE MATA EL MÉTODO, anotado para no volver a intentarlo:**

| `k` | coste | |
|---|---|---|
| 30 | 12,5 min | medido |
| 32 | 50 min | |
| 35 | 6,7 h | |
| 40 | 8,9 días | |
| 45 | 285 días | |

Pero el tiempo no es el problema. **Terras excluyó en 1976 todos los bucles de
periodo ≤ 2.592, y nuestro `k` ES ese periodo.** O sea que **todo el rango que un
barrido de restos puede alcanzar ya está demostrado vacío desde hace cincuenta
años.** Subir `k` no verifica nada desconocido: reverifica un teorema. Para pisar
territorio virgen haría falta `k > 2592`, o sea `2^2592` restos — un número de
**781 cifras**, contra los ~10^80 átomos del universo observable.

> **El barrido de restos no es lento: está muerto.** No puede encontrar nada por
> construcción. Se deja `pinzaciclos.py` como rederivación verificada y como
> registro de por qué esta vía está cerrada. **No subir `K_MAX`.**

*Dos afinados que se evaluaron y no salvan nada:* filtrar por el `S` viable
(`S ≈ k/1,585`) ahorra ~6× — menos de 3 niveles de `k`; y el cruce con
`clasesfusion.py` (si `r` y `r+1` se funden, sus candidatos difieren en
`1/(3^S − 2^k)`, luego como mucho uno es entero, por Catalan) poda un 21%. Los
dos son mejoras **constantes** sobre un problema **exponencial**. Lo que usa la
literatura es otra cosa: enumerar **bloques** en vez de restos, que baja de `2^k`
a `~m³` — por eso Hercher llega a `m = 91` y un barrido se atasca en 32.

### Las cribas industriales, y por qué NO sirven para ciclos (30-07-2026)

Estudio del método real con el que Barina verificó hasta `2^71` con hardware
normal. **No comprueba los `2^71` números: criba clases de restos enteras.**

**El factor de reducción total, que el paper no publica y se calculó desde sus
propios ficheros de criba: `X ≈ 363`.** Barina comprueba de verdad **1 de cada
363** números; para cubrir `2^71` itera unos `2^62,5`.

| criba | vivos | densidad | 1 de cada |
|---|---|---|---|
| A076227 (clásica) `k=34` | 151.917.636 | 0,884% | 113 |
| `h2esieve-34` (Barina, producción) | **85.234.595** | **0,496%** | **202** |
| × criba `3²` (mod 9, `×5/9`) | — | 0,2756% | **363** |

**Las seis reglas de descarte**, todas localizadas en su código abierto:
`R0` sólo `n ≡ 3 (mod 4)` · `R1` descenso garantizado (Brown/Terras, la base) ·
`R2` monotonía sobre niveles inferiores · **`R3` "criba de Eric": si dos
trayectorias se funden, el menor basta** (−18%) · `R4` regla del medio paso
(−18%) · `R5` antecesor menor módulo `3^j` (−31%) · `R6` criba `3^k` en tiempo
de ejecución (−44%).

> **`R3` ES `clasesfusion.py`.** La regla que le da a Barina un 18% es
> exactamente el criterio de fusión que este repo calculó hasta `k=30` por otro
> motivo. *Detalle de implementación que costó descubrir: si sólo comparás los
> supervivientes de `R1`, `R3` no mata nada (0 bajas hasta `k=20`). Hay que
> comparar contra **todos** los `b` menores, incluidos los ya muertos.*

**Dos números que cambian la intuición:**

- **Cada bit extra de criba sólo elimina un 3,4% más.** La densidad escala como
  `2^(−0,05·k)` (el exponente es `H(log₃2) = 0,94996`). Duplicar la memoria no
  compra casi nada, y por eso Barina se para en `2^34`.
- **Reducción ≠ aceleración.** Un factor 138× de criba produce sólo **5,94×** de
  velocidad, porque los supervivientes son justamente los caros — las
  trayectorias largas. Todas las optimizaciones juntas dan 25,65× en CPU. El
  coste total del récord fue **12.395 años-CPU + 159 años-GPU**.

**Y LA RESPUESTA ESTRUCTURAL, que cierra la pregunta de si se puede cribar para
buscar ciclos: NO, y no es por falta de ingenio.**

> Por el teorema de Terras, `T^k` es una **biyección** sobre `Z/2^k`. Cada vector
> de paridad de longitud `k` corresponde a **exactamente una** clase módulo
> `2^k`. **No hay clases que descartar — hay tantos candidatos como vectores.**

Una criba funciona porque muchas clases comparten el destino "ya bajó". Para
ciclos no hay nada que compartir: cada clase es un candidato distinto y único.
Es exactamente lo que `pinzaciclos.py` midió sin saberlo — *un candidato por
resto*. El filtro que sí sirve no es modular sino **diofántico**: la
aproximación de `log₂3` por convergentes (Crandall 1978, Eliahou 1993,
Simons–de Weger, Hercher).

**Lo que sí aporta la criba a los ciclos, y es indirecto:** certifica que todo
`n < B` **baja**, luego ningún ciclo puede tener su mínimo por debajo de `B`. Ese
`B` es el que se mete después en la desigualdad diofántica. *La criba compra el
límite; la exclusión la hace otra matemática.* Y se confirma en el propio código:
`worker.c` imprime `MAXIMUM_CYCLE_OFFSET 0` como constante literal — **el
programa de Barina no busca ciclos en absoluto.**

## Qué es real y qué es dibujo

Importa mantenerlo separado.

**Aritmética verificada:** los números del árbol y sus conexiones; la *altura* de
cada punto en la esfera = su distancia real al 1 (comprobado en los 5.674 números
de las ramas); los vórtices; que las ramas se funden y nunca se cruzan; la
topología del coral; que el rumbo dependa de (A,B); que el arranque dependa del
resto; el 1,7345 de divisiones por multiplicación.

**Elección de dibujo:** la esfera misma (el árbol no vive en una esfera; se mapeó
la distancia al 1 sobre media vuelta, cierra porque se hizo cerrar); la longitud
/ dirección de cada rama; el regreso "por detrás" del 1 a la semilla (la
trayectoria real no vuelve, se queda en `1-4-2`); **los ángulos del coral** (16°,
−8° o cualquier otro par); y **que cada tramo del coral mida 1 siempre** — por eso
la distancia al centro mide *cantidad de pasos*, **no** el tamaño de los números:
el salto de 9.232 a 4.616 dibuja lo mismo que el de 2 a 1.

**Comprobado y negativo:**

- La altura **no** codifica el tamaño del número. Correlación entre latitud y
  `log₂(valor)`: **0,12** — nula.
- **El 221 no prefiere ningún resto.** Pisa 55 de los 64 restos en sus 115
  números; el puro azar daría **53,5**. Diferencia: **+1,5**. No hay señal, no
  hay estructura, y los 9 restos que nunca pisa (`0, 13, 21, 25, 26, 37, 45, 48,
  51`) no tienen nada en común. *(Reparto por mitades, esto sí es limpio: 22
  restos solo en la primera mitad, 22 solo en la segunda, 11 en las dos.)*
- **La malla del 221×1276 no demuestra circularidad.** Sus 4.959 casillas con
  ecuación son exactas (0 fallos), pero el eje X es la cola del eje Y, así que el
  "cierre" en el centro está puesto por construcción, no descubierto.
- **El espejo y Collatz no se hablan.** Dos pruebas independientes:
  (1) la correlación entre `pasos(n)` y `pasos(espejo(n))` es **+0,08** — nula,
  del mismo orden que el 0,12 de la latitud;
  (2) la trayectoria del 221 contiene 5 parejas espejo (`2↔8`, `20↔80`, `47↔53`,
  `332↔668`, `350↔650`) más el punto fijo `5`. Parece mucho, pero un test de
  aleatorización con 20.000 conjuntos al azar **del mismo reparto de décadas** da
  media 4,53 y **p = 0,28**. El 28% del azar lo hace igual o mejor. No hay señal.
  *(Un primer cálculo dio "11 contra 1,48 esperadas" y era falso: ignoraba el
  reparto de décadas. Cuidado con estimar el azar a ojo — el modelo nulo tiene que
  preservar la estructura del dato.)*
- **El puente del espejo base 2 mide exactamente un paso y no llega al segundo.**
  Las dos identidades son exactas para **un** paso de Collatz, pero la correlación
  entre `pasos(n)` y `pasos(espejo2(n))` es **+0,06** — todavía *menos* que el
  +0,08 de base 10. El `+2` se acumula al iterar y borra la relación. Un paso:
  identidad exacta. Dos pasos: ruido. No buscar estructura de trayectoria ahí.
- **Ninguna constante de Collatz coincide con ninguna constante fundamental**
  (30-07-2026). Se hizo el test entero *con modelo nulo*, que es la única forma de
  que valga algo: 9 constantes de Collatz × 8 transformaciones contra 16 constantes
  adimensionales. **1 coincidencia observada, 0,394 esperadas por azar, p = 0,317.**
  El escéptico encontró tres defectos en el nulo (distribución más ancha que la
  real, número de comparaciones desigual, doble conteo), y al corregirlos **el `p`
  sube a 0,40–0,45**: los errores empujaban *a favor* de la señal. Control
  definitivo: el método **no distingue** Collatz de reglas `qn+1` arbitrarias
  (`p = 0,264`). *Y las constantes dimensionales —`c`, `G`, `h`— ni siquiera son
  comparables con un número puro: su valor depende del sistema de unidades.*
- **La racha inicial de impares NO predice la altitud** — correlación 0,59, explica
  el 35% de la varianza. *(Lo que sí hace es ponerle un piso exacto; ver la sección
  del piso. Cota sí, tendencia no.)*

**Correcciones de cosas que se creyeron y eran falsas:**

- `viz3d.py:coral()` usa `giro_par=7, giro_impar=-17`. Los signos son correctos
  pero **la proporción está invertida**: Harriss pone el impar a la *mitad* del
  par, y aquí el impar es el doble y pico.
- La biyección resto ↔ patrón **solo vale con el mapa del atajo**. Con la regla
  clásica salen los Fibonacci, no los `2^k`. (Se afirmó primero lo contrario; la
  comprobación 2 de `mallaresiduos.py` lo atrapó antes de dibujar nada falso —
  por eso esas comprobaciones van *antes* del dibujo y cortan con `SystemExit`.)
- **El `0%` de encimadas de Harriss era falso** (30-07-2026): sólo valía hasta 3.000
  semillas. Hay choques exactos desde la profundidad 31, y a la 59 son el 1–1,5% de
  cada nivel. Ver la sección del umbral de los 45 rumbos.
- **El `1,7345` del coral no es una constante**, es el valor de una muestra a
  `HASTA = 3.000`. Se asienta en `1,7320 ± 0,0003`.
- **La fila "se escapan del rango" del A/B no discrimina**: da 33,3% para `3n+1` y
  `3n−1` por igual, con los mismos conteos absolutos a cuatro tamaños. Mide el
  rango, no la regla.
- **`2/ln(4/3) = 6,952` es la constante del mapa del ATAJO, no del clásico.** Para
  el clásico es `3/ln(4/3) = 10,428`. Atribuirla mal da un 49,5% de error. La
  escalera correcta es 1 : 2 : 3 según se cuenten los `3n+1`, los pasos del atajo o
  los clásicos.
- **La causa del umbral del coral NO es `45 = 3²·5`** (`coralprimos.py`). La parte
  reticular era cierta pero **no era el motor**: explicaba un nivel de treinta y
  uno. Los choques los producen dos ramas con las mismas aristas en otro orden,
  que existe para cualquier `N`; el 43 y el 47 —primos— chocan *antes* que el 45.
  *Se predijo que el umbral se dispararía con `N` primo y no se disparó.*
- **El `+1` no aparece tres veces, aparece dos** (`elmasuno.py`). El grosor de la
  lámina y el sobrante `S` de la fracción impar son **idénticamente la misma
  suma**, no dos apariciones del mismo estorbo. 20.011 casos con `Fraction`.
- **`pisoaltitud.py` confirma que al piso le faltaba `n impar`** — la corrección
  ya estaba escrita, pero ahora tiene código que la reproduce, con los pares
  fallando a propósito para que no se pueda volver a perder.

## Nada de esto es nuevo — el balance, hecho a propósito

Escrito el 29-07-2026, después de preguntar en frío "¿hemos visto algo que nadie
haya visto?". La respuesta es **no**, y conviene tenerla anotada para no
redescubrirla con entusiasmo cada seis meses.

Aviso sobre este balance: no se hizo búsqueda bibliográfica de cada punto. El
juicio se basa en **cuán elemental es cada derivación**, no en haber confirmado
la fuente de todos. Lo único que se buscó en la web fue el coral.

| Lo que encontramos | Estado real |
|---|---|
| `n mod 2^k` fija los primeros k pasos; biyección con el mapa del atajo | **Terras 1976 / Everett 1977.** Tiene nombre: el vector de paridad. Teorema clásico |
| La rueda del árbol (período 2, hijos mod 9, maestra 18) | Consecuencia elemental de la regla mod 6, que ya estaba anotada como estándar. Aritmética modular de primer curso sobre estructura conocida |
| Las dos identidades del espejo base 2 | Dos líneas de álgebra. Nada que publicar |
| El espejo base 10 (44.450 ciclos, fijos en `5·10^m`) | Recreativa elemental. Se deriva en cinco minutos |
| El coral | **De Edmund Harriss.** Publicado, con libro y Numberphile |
| Identidad `(A,B)`, la lámina, `log₂(3)`, las convergentes | Vía clásica de las cotas de ciclos (Crandall, Steiner, Simons–de Weger). **Fechado: Shanks 1965, Atkin 1966. Guy 1983 imprime la lista `1/1, 2/1, 3/2, 8/5, 19/12, 65/41, 84/53, 485/306, 1054/665, 24727/15601, 50508/31867` y dice que hay ciclos en los denominadores 1, 2, 5, 12 y ninguno en 41, 53, 306** — es casilla por casilla nuestro barrido `(A,B)` |
| Fundirse los consecutivos, tuplas con el mismo número de pasos | **Garner 1985, Gao 1993, Wu Jia-Bang 1992–95, Wu–Huang 2001.** El mecanismo general está en Lagarias 1985 |
| Que `F(k+2)` cuente los patrones del mapa clásico | El conteo estándar de "sin dos adyacentes". Folklore |
| Que el rumbo del coral solo dependa de `(A,B)` | Los giros conmutan. Trivial |
| Que los negativos sean `3n−1` y tengan tres ciclos | Estándar: "`3x+1` sobre `Z` tiene cuatro ciclos conocidos". Dos líneas de álgebra |
| Que `3n+1` cicle por encima de `log₂(3)` y `3n−1` por debajo | Se sigue del signo de `C` en la identidad `(A,B)`. Elemental una vez planteado |
| Las constantes de parada `k/ln(4/3)` | Literatura clásica (Lagarias, Applegate–Lagarias). La de Wagon tiene entrada propia en OEIS |
| El umbral `q < 4` del `qn+1` | Es `f = 1/2` reescrito, o sea Terras 1976 otra vez |
| Que la paridad se comporte como moneda | El modelo probabilístico estándar, formalizado en Lagarias–Weiss 1992 y Kontorovich–Lagarias |

**Lo único que podría ser inédito:** la tabla de ángulos de `coralcollaz.py` —
cuántos rumbos permite cada par y qué fracción de ramas colapsa— **con el umbral
medido** (30-07-2026): primer choque exacto en la profundidad **31**. No es un
teorema: es una medición sobre nuestro propio método de dibujo. Pero Harriss
eligió ángulos por estética y nadie parece haber barrido el espacio. Candidata a
nota original en visualización recreativa. **Sin verificar en la literatura.**

**Y la candidatura ha encogido dos veces, las dos por control propio:**

- *La condición del ángulo nulo* se cayó con el `1,7345`, que no era estable.
- *La explicación del umbral por `45 = 3²·5`* se cayó con `coralprimos.py`:
  explicaba un nivel de treinta y uno. Lo que queda en pie es **el umbral medido
  y la recta en `N` con dos ramas según `N mod 4`** — que es un resultado más
  pobre y más cierto que el que se había anunciado.

*Es el patrón de siempre en este repo: lo que sobrevive al control es menos
vistoso que lo que se escribió primero, y por eso vale.*

*Un paralelo que tampoco se encontró en las fuentes, buscado explícitamente el
30-07-2026: nadie parece trazar la comparación moneda-física ↔ Collatz en los
términos de "sesgo condicional a la condición inicial". Lo más cerca es Lagarias
diciendo que la paridad se comporta "en cierto sentido como lanzamientos
independientes". "No encontrado" no es "no existe", pero al menos no es obvio.*

### Collatz llegó a esto desde la teoría de grafos, igual que nosotros

De su único artículo sobre el tema (1986, en chino, reimpreso en el libro).
Importa porque cambia qué es "el problema original".

Collatz no buscaba un problema aritmético. Estaba **clasificando los grafos
dirigidos de funciones aritméticas** (línea, árbol, bosque, punto fijo, ciclo)
y quería un ejemplo de la última categoría que fuera *"lo más simple posible,
pero también representativo"*. Razonó que **para tener un ciclo la función
tiene que a veces subir y a veces bajar**, y fabricó el `3n+1` por diseño:

- probó `n+1` para los impares → solo el ciclo trivial. **Sube muy poco.**
- probó `2n+1` → los impares crecen para siempre, ningún ciclo. **Sube demasiado.**
- probó `3n+1` → *"solo he encontrado el ciclo trivial (4,2,1)"*.

Y su enunciado propio no es "todo llega a 1" sino **"el grafo de la función es
conexo"**. Buscaba **ciclos**, no convergencia. Nunca lo publicó: *"como no pude
resolver el problema, no he publicado la conjetura"*; se lo contó a Hasse en
Hamburgo en 1952 y de ahí salió todo.

*(Es decir: mirar esto como grafo, contar vórtices, buscar el árbol — el punto
de partida de este repo — es literalmente el punto de partida de Collatz en
1932. No es un desvío del problema: es de donde salió.)*

### La demostración de Everett, y qué dice en nuestro lenguaje

Everett 1977 demuestra en tres páginas que casi todo `n` tiene un iterado menor
que `n`. El truco que le permite prescindir del `+1`: en vez del factor exacto
`3/2` usa la cota **`m_{n+1}/m_n ≤ 5/3`** válida siempre que `m_n ≥ 3`. Y define

```
L = log 2 / log(10/3) ≈ 0,5757
```

Su condición de bajada garantizada es `X/N < L`, donde `X` = pasos impares.
**Traducido a nuestras coordenadas** (`A` = veces `3n+1`, `B` = veces `n/2`):

```
Everett:   A / (A+B) < 0,5757    ⟺   B/A > 0,7369
Exacto:                              B/A > log₂3 = 1,585
```

Es más flojo a propósito. `5/3 > 3/2` es una cota pesimista, y ése es el precio
de tener una demostración de tres páginas sin un solo agujero. **Nuestro 1,585
es el umbral verdadero; el 0,7369 es el umbral que se sabe demostrar.**

### Lo que sí es inusual aquí, y no es matemática

1. **Los negativos registrados**, repartidos por todo el documento: el 221 no
   prefiere ningún resto; el medio del 221 es contabilidad y no patrón; la malla
   221×1276 no demuestra circularidad; el espejo no correlaciona con Collatz; el
   puente de base 2 no llega al segundo paso; la altura no codifica magnitud;
   ninguna constante de Collatz coincide con ninguna constante fundamental; y la
   racha inicial no predice la altitud. Casi nadie anota lo que no funcionó, y por
   eso casi todo el mundo repite las mismas búsquedas. **Y las correcciones a
   afirmaciones propias que resultaron falsas**, que es la parte que de verdad
   cuesta escribir — hay una lista entera de ellas más arriba.
2. **El A/B de control** (`mallaespejo.py`, `mallaespejo2.py`,
   `mallascerradas.py`): meter varias reglas por la misma maquinaria y **exigir
   que salgan distintas**. Es lo que separa "mi malla revela estructura" de "mi
   malla dibuja lo que sea".
3. **Comprobar antes de dibujar, cortando con `SystemExit`.** Esto atrapó un
   error real en vivo: se afirmó la biyección resto↔patrón para el mapa clásico
   y la comprobación 2 de `mallaresiduos.py` paró el programa antes de generar
   un gráfico falso. Sin esa disciplina habría quedado una imagen bonita
   sosteniendo una afirmación errónea.

### El techo realista, y hacia dónde no hay camino

**Hacia demostrar que Collatz es una referencia circular, o que el universo es un
sistema cerrado: no hay camino.** No es que esté lejos — es que las mallas no son
el tipo de objeto que demuestra eso, y en esta sesión quedó **medido** por qué:
el cierre lo pone el ángulo que elegís (tabla del coral) o el módulo que elegís
(`mallascerradas.py`), no Collatz. Cuando el cierre viene de la aritmética
—la rueda mod 27— gobierna el esqueleto del árbol hacia atrás y **no** el destino
hacia adelante, que sigue ciego a los restos.

**El techo de este repo es rederivación independiente bien verificada, más
visualización original.** Eso no es descubrimiento, pero tampoco es poco: hay
**treinta y cinco** programas, **veintisiete** de ellos con comprobaciones que
cortan con `SystemExit`, un documento que separa lo real de lo dibujado, y un
historial de negativos. La mayoría de la exploración amateur no llega ahí.

### EL CUARTO CAMINO — el objetivo realista, enunciado el 30-07-2026

Después de un día entero midiendo, el enunciado que quedó, y que sustituye al
propósito místico original:

> **No vamos a encontrar un número que haga bucle. Ni a demostrar que todos bajan
> a 1. Ni que exista uno que suba para siempre.**
>
> **Lo que sí se puede buscar es el cuarto camino: las reglas que generan todos
> los números de la secuencia de Collatz, sin generar la secuencia.**

Es el mejor enunciado de propósito que ha tenido este repo, por tres razones:

1. **Es alcanzable.** Las otras tres salidas son la conjetura entera, un problema
   abierto de noventa años. Ésta no lo es.
2. **Ya está a medias, y es lo que el repo hace mejor sin haberlo dicho así:**
   - `mallaresiduos.py`: los primeros `k` pasos los decide `n mod 2^k`. Es una
     **regla** que da el comportamiento sin calcular la trayectoria.
   - `clasesfusion.py`: un criterio **finito** que decide, para los **infinitos**
     `m` de una clase, si dos consecutivos se funden. Eso es literalmente
     "generar las reglas sin generar la secuencia".
   - `mallascerradas.py`: la rueda mod 27 gobierna dónde brota el árbol inverso,
     sin recorrerlo.
   - Y el Lema 8 de Hercher —`k` impares seguidos ⟹ `n ≡ −1 mod 2^k`— es el
     mismo tipo de objeto, y es el motor de toda la exclusión de ciclos.
3. **Discrimina**, que es el filtro que este repo se exige: una regla que valiera
   para cualquier entrada no diría nada de Collatz.

**Lo que NO es, para no inflarlo:** esto tiene nombre en la literatura —dinámica
simbólica, vectores de paridad, la estructura 2-ádica del mapa— y es un campo con
cincuenta años de trabajo. El cuarto camino no es un programa nuevo: es el
programa correcto, y el único donde este laboratorio puede aportar algo sin
mentirse. *No demuestra la conjetura, y no pretende hacerlo.*

**Por qué las constantes no pueden demostrar nada, anotado para no volver a
preguntarlo.** El laboratorio mide **promedios**; la conjetura es una afirmación
sobre **cada** número. Un promedio nunca demuestra un caso individual: `√3/2 < 1`
dice "en promedio las trayectorias bajan", y una sola órbita que subiera para
siempre no movería ese promedio ni un decimal, porque sería un conjunto de medida
cero. Prueba de que no es paranoia: el `5n+1` tiene media geométrica `1,118 > 1`
("todo sube") **y sin embargo tiene un ciclo**, el del 13, donde nada sube. La
constante no impide la excepción. Y la historia tiene casos peores — la conjetura
de Pólya y la de Mertens se verificaron en millones de casos y son **falsas**, y de
`Li(x) > π(x)` se sabe *con demostración* que falla en algún punto antes de `10³¹⁶`
sin que nadie pueda alcanzarlo con una máquina.

**Lo que sí tendría forma de demostración son cotas, no promedios.** El único
resultado de esta sesión con esa forma es el piso de la altitud
(`log₂(alt/n) ≥ racha·log₂(3/2) + 1`, 0 fallos en 99.999): un "nunca por debajo
de", demostrable en una línea. Vale más que las tres constantes juntas aunque diga
mucho menos. **Cuando aparezca algo nuevo, la pregunta es: ¿es un promedio o es una
cota?**

**Y la fuerza bruta no puede demostrar esto, jamás.** No por falta de máquina: los
enteros son infinitos y verificar hasta `2⁷¹` o hasta `2^(10^100)` deja exactamente
la misma cantidad sin verificar. Sirve para refutar, nunca para demostrar. Tampoco
ayudan los ordenadores cuánticos: no hay algoritmo cuántico para esto, y lo mejor
que da una búsqueda sin estructura es la raíz cuadrada del esfuerzo.

Estado del arte, para calibrar: verificación por fuerza bruta al día **2^71**
(Barina, enero 2025; publicado en *J. Supercomputing* 2025, con aceleración
1.335× de CPU a GPU sobre supercomputadores europeos). Resultado general más
fuerte: **Tao 2019**, "casi todas las órbitas alcanzan valores casi acotados".

**Posterior al libro de 2010, y por tanto no cubierto por él:**

- **Hercher (2023)**, *J. Integer Sequences* 26, art. 23.3.5: **no hay
  `m`-ciclos de Collatz con `m ≤ 91`**, donde `m` = número de mínimos locales
  del ciclo. Mejora el `m ≥ 76` de Simons–de Weger (y el `m ≥ 83` que daba la
  verificación actualizada). El libro de 2010 todavía dice `m ≤ 68`.
- **[ccchallenge.org](https://ccchallenge.org/)** — proyecto comunitario vivo
  que está **formalizando la literatura de Collatz paper a paper** en un
  asistente de pruebas. 372 entradas catalogadas, 364 por formalizar, **1
  terminada**, 4 en curso, 5 esperando auditoría. Es la misma disciplina que
  este repo aplica a mano (comprobar antes de afirmar), llevada al extremo.

## El proyecto de fondo, y el filtro que hay que aplicarle

La idea es inyectar cualquier progresión y generar la misma malla, para proponer
que las matemáticas no apuntan al infinito sino que dan la vuelta y se conectan.

**El filtro:** un modelo que devuelve la misma malla para cualquier entrada no
está midiendo la entrada, está midiendo el modelo. El poder de demostrar algo
viene de que la malla **salga distinta** según lo que se inyecte. La tabla de
ángulos de arriba es un ejemplo de hacerlo bien: mide una diferencia (0,003% vs
97%) y dice qué perilla la causa. *(Era "0% vs 97%" hasta que se midió el umbral:
a 65.145 ramas hay 2 choques, no cero. La conclusión no cambia — cambia tres
órdenes de magnitud, no el signo.)*

**Y el segundo filtro, aprendido el 30-07-2026: no toda fila de una tabla A/B
discrimina.** La fila "se escapan del rango" da el mismo número para `3n+1` y
`3n−1` porque mide el rango elegido, no la regla. Antes de apoyarse en una fila hay
que meterle dos reglas *parecidas* y comprobar que las separa; con reglas muy
distintas cualquier fila parece funcionar.

**La versión rigurosa de la intuición:** cualquier regla determinista sobre un
conjunto finito tiene que repetirse — principio del palomar, no es conjetura.
Fibonacci módulo `m` cierra en el período de Pisano (mod 10 son 60 pasos);
`n → n+k` módulo `m` cierra en `m/mcd(m,k)`. Ahí los aros existen y cada
progresión trae el suyo, de distinto tamaño: una malla que discrimina.

**Collatz es el caso raro, no el ejemplar:** su trayectoria completa **no** baja
limpio a un espacio finito, porque `n/2` módulo `m` no queda determinado por `n`
módulo `m`. Solo los primeros `k` pasos bajan (de ahí `mallaresiduos.py`).

### "Es determinista, luego tiene patrón, luego se puede demostrar"

El argumento intuitivo es: *Collatz es determinista, funciona dentro de una
arquitectura preestablecida, y encontrando el patrón queda demostrado.* Las dos
primeras partes son ciertas. **El paso de "determinista" a "tiene patrón
encontrable" es el que falla**, y es exactamente donde vive la dificultad.

Determinista y sin patrón no son incompatibles. La demostración más limpia de
eso está medida en este repo:

- **`redhilos.py`, experimento 2.** Una red neuronal, con 40.000 ejemplos, ve
  las `k` paridades anteriores de una trayectoria e intenta predecir la
  siguiente. Resultado para `k = 4, 8, 12, 16`: **entre 49,3% y 50,5%.** No le
  gana a una moneda. Y no puede: **Terras (1976), Corolario 1.4** demuestra que
  las paridades son variables independientes con `P = 1/2` **exacta**.
- **`redhilos.py`, experimento 1.** La misma red, viendo los `m` bits bajos de
  `n`: **50% clavado para `m ≤ k`, 100% para `m > k`.** Un acantilado, no una
  pendiente. Información completa o moneda, sin término medio.

O sea: la secuencia es **completamente determinista** —cada paso se calcula sin
ambigüedad— y a la vez **la mejor predicción posible del siguiente bit, dados
todos los anteriores, es tirar una moneda**. No es que no hayamos encontrado el
patrón: es que la estructura del problema demuestra que ahí no hay ninguno que
encontrar.

Lagarias lo dice en una frase que conviene tener presente:

> *"la evidencia empírica indica que `T` conserva la pseudoaleatoriedad hasta
> entrar en órbita periódica; esto apoya la conjetura y a la vez nos priva de
> cualquier mecanismo obvio para demostrarla, **porque los argumentos
> matemáticos explotan la existencia de estructura, no su ausencia**."*

**Sobre "no podemos contar hasta el infinito, pero es lógico pensar que sí
podríamos".** Eso es exactamente lo que hace una demostración por inducción, y
para Collatz no funciona: no se conoce ninguna cantidad que decrezca
monótonamente a lo largo de la trayectoria. Buscar una es un programa legítimo
—Błażewicz y Pettorossi (1983) lo intentaron con medidas sobre las cadenas
binarias— pero nadie la ha encontrado, y el `+1` es la razón: rompe cualquier
medida que se comporte bien con `n/2` y con `3n`.

*Esto no es un argumento para dejarlo. Es el mapa de dónde NO está la salida,
que es lo que evita gastar seis meses en el sitio equivocado.*

### "La maquinita de `if/else`": buscar los que siempre suben y los que siempre bajan

*(Idea planteada el 30-07-2026, evaluada y descartada. Se anota entera porque es
de las que vuelven cada seis meses.)*

**La idea.** Escribir condiciones —`if`/`else` de toda la vida— que garanticen que
un número suba siempre, y otras que garanticen que baje siempre. Aislar las series
que ascienden al 99,9% y las que descienden al 99,9%. Un número que junte las dos
—que suba hasta la cima y desde ahí empiece a bajar hasta volver— sería el ciclo.

Tiene tres partes, y cada una falla de una forma distinta:

**1. Las condiciones ya existen, y son exactas.** Es Terras 1976, y este repo lo
tiene verificado en `mallaresiduos.py`:

```
n ≡ 2^k − 1  (mod 2^k)   ->  sube k veces seguidas, garantizado
n ≡ 0        (mod 2^k)   ->  baja  k veces seguidas, garantizado
```

No son estadísticas: son teoremas, y se escriben como `if`. Ya se usaron hoy para
fabricar `2^4000 − 1`, que da 3.999 pasos impares seguidos.

**2. "Sube siempre" no existe entre los enteros positivos.** Haría falta
`n ≡ 2^k − 1 (mod 2^k)` para **todo** `k` a la vez, y el único objeto que lo
cumple es **`−1`** — el número que "termina en unos" infinitos en base 2. O sea
que el ascensor perfecto existe, pero es uno de los ciclos negativos, no un
entero positivo. *(Y es justo uno de los que la pinza encontró sin buscarlos.)*

**3. EL ERROR DE PUNTERÍA, que es lo que hay que recordar.** Medido:**

| número | qué es | distancia a `log₂3` |
|---|---|---|
| `2²⁰−1` | sube 20 veces seguidas | 0,3331 |
| `2¹²−1` | sube 12 veces seguidas | 0,2186 |
| 27 | uno cualquiera | **0,1224** |
| 77.031 | uno cualquiera | **0,1282** |
| **un ciclo** | — | **0 exacto** |

**Los números corrientes están MÁS CERCA del ciclo que los "subidores del 100%".**
Porque `2^k − 1` sube `k` veces y después se desploma, y esa caída le dispara el
`B/A`. Cuanto más extremo se hace el arranque, más lejos del equilibrio acaba.

> **Un ciclo no es ni ascendente ni descendente: está perfectamente equilibrado.**
> Buscar en los extremos (99,9% arriba, 99,9% abajo) es buscar en los dos únicos
> sitios donde con seguridad no está. El ciclo vive en el centro.

Y "sube hasta un pico y luego baja" **describe todas las trayectorias sin
excepción** — el 27 sube a 9.232 y baja. Para que sea ciclo hace falta *volver
exactamente al punto de partida*, y eso no lo decide ningún `if`: lo decide la
ecuación de `pinzaciclos.py`.

**Lo que sí queda en pie de la idea.** Una máquina de condicionales es un
autómata, y ésa es la forma del único enfoque que hoy rompe el molde: **Yolcu,
Aaronson y Heule (2021)** convierten Collatz en un sistema de **reescritura de
cadenas** sobre una representación mixta binaria-ternaria —puro `if`/`else`— cuya
terminación equivale a la conjetura, y le lanzan un SAT solver con
interpretaciones matriciales. Es el único que ataca el `+1` de frente en vez de
rodearlo. *Con el aviso de Conway (1972): la versión generalizada de Collatz es
**indecidible**, así que puede existir una máquina para este caso, pero no puede
existir un método que la construya en general.*

## Siguiente sesión

> **Esta lista existe tambien en `bitacora.md`, mas corta y mas nueva.** Si las dos
> no dicen lo mismo, **manda la bitacora** — ahi es donde se escribe al cerrar cada
> sesion. Lo de aqui abajo es la version larga, con el razonamiento.

> ### ⇢ HECHO EL 30-07-2026: `clasesfusion.py` llegó a `K_MAX = 32`
>
> Se corrió primero a 30 (unos veinte minutos) y después a 32. **`K_MAX` vale
> **32** en el archivo**, y `a(32) = 1.871.137.623` está **confirmado por dos
> caminos independientes** — el secuencial de `clasesfusion.py` y el repartido
> por núcleos de `clasesparalelo.py` — con el resultado escrito en
> `resultado_paralelo_k32.txt`. (`a(31) = 930.718.308` ya había coincidido igual.)
>
> ```
>  k         N(k)        NUEVAS    razon
> 28  114.400.435       692.079   1,9269
> 29  230.136.995     1.336.125   1,9306
> 30  462.857.658     2.583.668   1,9337
> 31  930.718.308     5.002.992   1,9364
> 32  1.871.137.623   9.701.007   1,9390
> ```
>
> **La cota inferior demostrada sube de 42,6175% a `43,5658%`.** Eso es lo
> único duro: no depende de muestreo ni de ajuste.
>
> **Y la pregunta sigue sin decidirse.** Se pedía mirar si los incrementos de
> la razón seguían encogiendo. Siguen — `0,0050 → 0,0039 → 0,0037 → 0,0031 →
> 0,0027 → 0,0026` — **pero encogen despacio, y ahí está el problema:** si
> decrecen geométricamente, la razón converge por debajo de 2 (en torno a 1,95)
> y la fracción tiene límite `< 1`; si decrecen como `1/k`, la suma diverge
> igual y la razón acaba llegando a 2. **Seis puntos siguen sin distinguir esas
> dos cosas.** El aviso de no extrapolar sigue en pie y ahora vale doble.
>
> Los términos están en `sucesiones.txt` y las consultas a OEIS se repitieron
> con la sucesión ampliada: siguen sin estar.
>
> **Por dónde seguiría este hilo:** `k = 34`, que con `clasesparalelo.py` cuesta
> unas 4 veces lo de `k = 32`. No decidiría nada tampoco — pero alarga la única
> serie que puede distinguir geométrico de `1/k`. Es la única vía barata que
> queda aquí, y está en la cola de `bitacora.md`.

*(Ya hechos: el espejo en base 2 (puente exacto de un paso, no llega al segundo);
la rueda del arbol; las once mallas en disco; los once hilos en sqlite; el espejo
en quince bases; y la conjetura de Wu medida. El 30-07-2026 se sumaron: el umbral
de los 45 rumbos, los negativos como 3n-1, las constantes, el ajuste fino de qn+1
y el A/B contra la moneda. Todo eso esta arriba, con sus correcciones.)*

**AVISO SOBRE LA SESION DEL 30-07-2026: casi no dejo ficheros, y la deuda ya se
pago a medias.** Se hizo casi entera en scripts sueltos fuera del repo. Lo que
sobrevivio de entrada: `pinzaciclos.py`, `cruzarecords.py`, `records.json` y
`clasesparalelo.py`. **Y el mismo dia se devolvieron cuatro mediciones mas a
fichero ejecutable** — `pisoaltitud.py`, `elmasuno.py`, `reimpl.py` y
`coralprimos.py` — mas `afirmaciones.db`, que recoge los enunciados con su
cuantificador.

**Lo que SIGUE sin codigo detras, y es la deuda que queda** (medido y escrito
aqui, pero no reproducible): **los negativos como `3n-1`, las constantes, el
ajuste fino de `qn+1` y el A/B contra la moneda.** Cuatro, no seis. Si alguna
merece quedarse, hay que convertirla en un programa con la forma de siempre
(constantes arriba, comprobaciones antes del dibujo, `SystemExit` si fallan).

1. **LA PREGUNTA MAS CONCRETA QUE HAY EN EL REPO** sigue siendo si la razon
   `b(k)/b(k-1)` converge por debajo de 2 o llega a 2. El `k = 32` ya se corrio,
   por dos caminos independientes, y **no la decidio** (ver arriba). El siguiente
   escalon es `K_MAX = 34` con `clasesparalelo.py`: cuesta unas cuatro veces mas y
   da dos puntos mas de la sucesion de incrementos. Tampoco va a decidirlo, pero
   alarga la unica serie que puede distinguir "decrece geometricamente" de "decrece
   como 1/k". El calculo es **exacto**, no muestreado, que es lo que lo hace
   valioso. *Y el aviso de siempre: que una razon suba hacia 2 en veinte escalones
   no demuestra ni que llegue ni que se quede corta. Acota la pregunta; no la
   contesta.*

2. **EL PLAN DE LA PINZA, en tres fases** (diseñado el 30-07-2026 después de
   destripar el método de Hercher). Lo que lo hace viable es un hallazgo del
   estudio: **Hercher no usa el teorema de Baker en ninguna parte.** Toda la
   maquinaria diofántica entra como **un número importado** de Simons–de Weger
   (`K < 1,4784·m·δ^m`, arbitrado en *Acta Arith.* 117). Aceptándolo como caja
   negra, el resto es elemental. Y la métrica del esfuerzo, medida:

   ```
   ~60 lineas de Python, solo stdlib, con solo T(n) < 3/n   ->  excluye m <= 82
   todo el aparato de Hercher (analisis de casos, Teorema 21,
   dos programas C++, CINCO SEMANAS de computo)             ->  excluye m <= 91
   ```

   **Fase 1 — ⇢ HECHA: `reimpl.py` ya está en el repo.** Reproduce las siete
   iteraciones del Teorema 23 de Hercher, **7/7**, sin un solo `float` en la
   cadena que decide. Es el primer programa del laboratorio que reproduce
   matemática arbitrada. **Y encontró dos discrepancias contra lo publicado**, que
   es justo el tipo de resultado que justificaba hacerlo. *Detalle de rigor que no
   se puede saltar, y que sigue valiendo para la Fase 2: el
   denominador mínimo hay que buscarlo en un intervalo **ensanchado** con
   racionales `δ_lo < δ < δ_hi`, para que el error caiga del lado seguro. Sin eso
   es un número bonito, no una demostración — el mismo espíritu que los
   `SystemExit` antes de dibujar.*

   **Fase 2 — la escalera afín de Wang, que ES la pinza.** El cuello de botella no
   es Baker ni el tiempo: es `X₀`. Para `m = 92` haría falta verificar hasta
   `2^73,9` y el récord mundial es `2^71`; con `X₀ = 2^71` el bucle de Hercher
   **sigue parando en 91**. Por eso Wang no mejoró `X₀`: cambió la técnica. Fija un
   prefijo de exponentes, escribe cada `nᵢ` como función afín del mismo entero
   inicial, y **el conjunto vivo queda como un intervalo intersecado con una clase
   residual módulo `2^s`**. Un nivel vacío es la contradicción. Eso es exactamente
   la pinza: cota por un lado, criba modular por el otro. Y media está construida —
   `clasesfusion.py` ya hace aritmética exacta sobre clases mod `2^k` hasta `k=32`
   con troceado en bloques, y `clasesparalelo.py` lo reparte entre núcleos.

   **Fase 3 — el objetivo, y no es superar a nadie: VERIFICAR A WANG.** Su
   preprint (Zenodo, 29-07-2026, `m ≤ 95`) **no está arbitrado**, tiene cero citas
   y metadatos descuidados. Un resultado así necesita verificación independiente y
   nadie la ha hecho porque tiene dos días. **Si aguanta, se dice. Si se cae, eso
   sí es un hallazgo.** Es lo más difícil que hay al alcance que no consista en
   repetir a otro.

3. **⇢ HECHO: el numero PRIMO de rumbos (`coralprimos.py`). La prediccion
   FALLO**, y es de los pendientes que mas ha enseñado. Se predijo que con `N`
   primo el umbral de profundidad se dispararia. **Los dos primos vecinos del 45,
   el 43 y el 47, chocan ANTES que el 45**, y el maximo del rango no lo tiene un
   primo. La mitad reticular de la teoria si se confirmo (con `N` primo el unico
   nucleo es `(1,1,…,1)`, sin excepcion), pero **resulto no ser el motor**: los
   choques los producen dos ramas que usan las mismas aristas en otro orden, algo
   que existe para cualquier `N`. Ver la correccion completa en la seccion del
   umbral de los 45 rumbos. *Lo que queda para una sesion futura es la recta
   `(N+19)/2` / `(N+11)/2` segun `N mod 4`: esta medida pero no demostrada, y
   demostrarla si tendria forma de cota.*

4. **Colorear el arbol de `collazarbol.py` con la rueda** — cada rama segun la
   clase mod 3 de su semilla — para *ver* el tambor sobre la esfera que ya existe.
   Las once mallas ya estan en disco (`guardarmallas.py`), incluida la cuarta rueda
   mod 81.

5. **Usar las mallas guardadas contra algo que todavia no sepamos.** Ahora que
   `mallas/*.json` existe, el cruce ya no cuesta calcular: se pueden barrer las once
   contra trayectorias de Collatz buscando que otra malla predice algo. Aviso por
   adelantado: lo mas probable es que **no prediga nada**, porque el negativo de
   `cruzarestos.py` (el destino hacia adelante es ciego a los restos) sigue en pie.
   La rueda mod 27 funciona porque el arbol *dobla*, y doblar es literalmente esa
   malla. Sin esa correspondencia estructural, un cruce que de positivo seria
   sospechoso antes que interesante.

6. **⇢ HECHO: el `+1` no aparece tres veces, aparece DOS (`elmasuno.py`).** Se
   pedia buscar si el grosor `0,2286` de la lamina, el `+2` del espejo base 2 y el
   sobrante `S` de la fraccion impar se podian escribir como una sola cantidad.
   **Dos de las tres son la misma suma, y no aproximadamente: identicamente.** El
   `ε = ln(2^B / (3^A·n))` de la lamina y el `S = Σ ln(1 + 1/(3x))` de la fraccion
   impar son **el mismo objeto termino a termino**, y sale de una linea de
   aritmetica: en un paso impar el factor es `(3x+1)/x = 3·(1 + 1/(3x))`.
   Comprobado con `Fraction` exacto en 20.011 casos. **La lamina deja de ser una
   medicion y pasa a estar demostrada para todo `n`.** El `+2` del espejo base 2
   sigue siendo la tercera pieza, aparte. *Es lo unico del laboratorio que
   **unifica** piezas en vez de acumularlas, que era exactamente lo que se pedia.*
