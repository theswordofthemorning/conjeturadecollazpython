# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Conjetura de Collatz — laboratorio

Repo de exploración de la conjetura de Collatz (`n/2` si es par, `3n+1` si es
impar; se conjetura que todo `n ≥ 1` termina en 1).

No es una biblioteca ni un paquete. Son programas sueltos, cada uno con su
número configurable arriba del archivo, pensados para ejecutarse y mirar el
resultado. **El código se escribe simple a propósito**: nombres en castellano,
comentarios que explican lo obvio, sin abstracciones.

## Instalación

```
pip install -r requirements.txt      # numpy, matplotlib, plotly
```

Doce de los scripts importan `plotly.graph_objects`; `mallaespejo.py` y
`mallaespejo2.py` además usan `plotly.subplots`. Durante mucho tiempo `plotly`
faltaba en `requirements.txt` y el repo no arrancaba en una máquina limpia — ya
está arreglado.

**Las dos mitades se instalan por separado, y conviene saber cuál te falta.** En
julio de 2026, en el Python 3.14.5 de `C:\Python314`, estaban `numpy` y `plotly`
pero **no `matplotlib`**. Con eso funcionan todos los scripts de plotly (las
mallas, el coral, el espejo) y se cae todo lo de matplotlib: `viz3d.py`,
`collazejecucion.py` y `python main.py graficar`. Para saber qué hay:

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

Su forma es siempre la misma:

1. Un bloque de comentarios arriba explicando qué se está mirando y por qué.
2. Constantes en MAYÚSCULAS editables (`NUMERO = 221`, `TAMANO_LETRA`, …).
3. Código a nivel de módulo, sin `main()` ni `if __name__`. **Importarlos los
   ejecuta.** No hagas `import collazmalla` para inspeccionarlo: te abre el
   navegador.
4. Los de plotly terminan en `figura.write_html(archivo, auto_open=True)`.

Los `.html` y `.png` están en `.gitignore`. **Los `.json` de `mallas/` no** — son
el único resultado que sobrevive a cerrar el navegador, y están para eso.

**`guardarmallas.py` es la excepción a la forma de arriba:** no dibuja, no abre
el navegador, no tiene `NUMERO`. Escribe archivos y comprueba que se puedan
volver a leer. Es el único programa del repo cuyo resultado no es una imagen.

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
patrón de la constante, no el de tkinter.

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
`python main.py camino 27` crasheaba desde Sublime. Para revisarlo:

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
| `mallas/*.json` | Las mallas guardadas, **sí versionadas**. `indice.json` lista las once |
| `maquinitacollaz.py` | Escupe los 114 pasos de un número, uno por línea |
| `teoriacollaz.txt` | El planteamiento filosófico del que salió la idea de la esfera |
| `patron detectado manualmente.txt` | Notas a mano sobre las posiciones 57 y 114 |
| `collazclaude.png` | Captura del coral de Harriss 16°/−8°, para mirarlo sin renderizar |

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
| 16° | −8° (Harriss) | 45 | 6.520 | **0%** |
| 7° | −17° (el de `viz3d`) | 357 | 6.520 | **0%** |
| 60° | −30° | 13 | 3.497 | 46% |
| 90° | −45° | 9 | 1.476 | 77% |
| 120° | −60° | 6 | **221** | **97%** |

Con 120°/−60° hay 6 direcciones posibles, el paseo cae en una retícula hexagonal
y por el principio del palomar los puntos **tienen** que repetirse. Es cierre de
verdad, **pero lo trae el ángulo elegido, no Collatz.** Collatz pone el paseo; el
ángulo pone el cierre. Con los ángulos de Harriss no cierra nada, y por eso parece
un coral: se ramifica para siempre y nunca se vuelve a juntar.

**De dónde sale la forma, y cómo se apaga.** En el coral **63,43% de los pasos
son pares y 36,57% impares** → **1,7345 divisiones por multiplicación**, por
encima del equilibrio. Con `16°/−8°` eso da un **giro medio de +7,22° por paso**:
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
- **Oliveira e Silva** usa la fusión de `n` y `n−1` como optimización
  industrial de su criba de verificación: le quita el **17,5%** de las hojas.

**La comprobación 4 cierra el círculo.** `100005 = 32·3125 + 5`, así que
nuestro par `(100005, 100006)` **es un caso de la primera familia publicada**.
Comprobado en `m = 1, 2, 7, 100, 3125, 9999, 40000`: **todos se funden en el
paso 6 contra el paso 6, desfase 0, sin excepción.** La literatura predijo
nuestro hallazgo veinticinco años antes de que lo miráramos.

**Y el mecanismo general estaba en Lagarias 1985**: `8k+4` y `8k+5` se funden
siempre en 3 pasos; y si dos trayectorias se funden, entonces
`2^r·k + n₁` y `2^r·k + n₂` se funden **para todo `k`** — una sola fusión
genera una progresión aritmética infinita de fusiones. Eso es exactamente lo
que produce los bloques de pasos iguales.

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

**Correcciones de cosas que se creyeron y eran falsas:**

- `viz3d.py:coral()` usa `giro_par=7, giro_impar=-17`. Los signos son correctos
  pero **la proporción está invertida**: Harriss pone el impar a la *mitad* del
  par, y aquí el impar es el doble y pico.
- La biyección resto ↔ patrón **solo vale con el mapa del atajo**. Con la regla
  clásica salen los Fibonacci, no los `2^k`. (Se afirmó primero lo contrario; la
  comprobación 2 de `mallaresiduos.py` lo atrapó antes de dibujar nada falso —
  por eso esas comprobaciones van *antes* del dibujo y cortan con `SystemExit`.)

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

**Lo único que podría ser inédito:** la tabla de ángulos de `coralcollaz.py` —
cuántos rumbos permite cada par y qué fracción de ramas colapsa (45 rumbos → 0%,
6 rumbos → 97%), más la condición derivada del ángulo nulo
(`impar/par = −1,7345`, la razón de descenso real). No es un teorema: es una
medición sobre nuestro propio método de dibujo. Pero Harriss eligió ángulos por
estética y nadie parece haber barrido el espacio. Candidata a nota original en
visualización recreativa. **Sin verificar en la literatura.**

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

1. **Cinco negativos registrados** (el 221 no prefiere restos; el medio es
   contabilidad; el espejo no correlaciona; el puente no llega al segundo paso;
   la altura no codifica magnitud). Casi nadie anota lo que no funcionó, y por
   eso casi todo el mundo repite las mismas búsquedas.
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
doce programas que se auto-verifican, un documento que separa lo real de lo
dibujado, y un historial de negativos. La mayoría de la exploración amateur no
llega ahí.

Estado del arte, para calibrar: verificación por fuerza bruta al día **2^71**
(Barina, enero 2025). Resultado general más fuerte: **Tao 2019**, "casi todas las
órbitas alcanzan valores casi acotados".

## El proyecto de fondo, y el filtro que hay que aplicarle

La idea es inyectar cualquier progresión y generar la misma malla, para proponer
que las matemáticas no apuntan al infinito sino que dan la vuelta y se conectan.

**El filtro:** un modelo que devuelve la misma malla para cualquier entrada no
está midiendo la entrada, está midiendo el modelo. El poder de demostrar algo
viene de que la malla **salga distinta** según lo que se inyecte. La tabla de
ángulos de arriba es un ejemplo de hacerlo bien: mide una diferencia (0% vs 97%)
y dice qué perilla la causa.

**La versión rigurosa de la intuición:** cualquier regla determinista sobre un
conjunto finito tiene que repetirse — principio del palomar, no es conjetura.
Fibonacci módulo `m` cierra en el período de Pisano (mod 10 son 60 pasos);
`n → n+k` módulo `m` cierra en `m/mcd(m,k)`. Ahí los aros existen y cada
progresión trae el suyo, de distinto tamaño: una malla que discrimina.

**Collatz es el caso raro, no el ejemplar:** su trayectoria completa **no** baja
limpio a un espacio finito, porque `n/2` módulo `m` no queda determinado por `n`
módulo `m`. Solo los primeros `k` pasos bajan (de ahí `mallaresiduos.py`).

## Siguiente sesión

*(El espejo en base 2 ya se hizo — ver arriba. Encontró el puente exacto de un
paso y midió que no llega al segundo.)*

1. **El umbral de los 45 rumbos.** Con `16°/−8°` hay 45 direcciones posibles y
   cero choques en 3.000 semillas. Subir `HASTA` en `coralcollaz.py` y buscar
   dónde aparece el primer choque. Si nunca aparece, 45 rumbos bastan para un
   árbol infinito; si aparece, ese umbral es un número real del modelo.
2. *(Hecho en `mallascerradas.py`: las progresiones cerradas se midieron, salen
   distintas entre sí, y el cruce contra Collatz dio la coincidencia exacta —
   la rueda del árbol. Y hecho en `guardarmallas.py`: las once están en disco,
   incluida la cuarta rueda mod 81.)* Lo que queda de ese hilo: **colorear el
   árbol de `collazarbol.py` con la rueda** — cada rama según la clase mod 3 de
   su semilla — para *ver* el tambor sobre la esfera que ya existe.
3. **Usar las mallas guardadas contra algo que todavía no sepamos.** Ahora que
   `mallas/*.json` existe, el cruce ya no cuesta calcular: se puede barrer las
   once contra trayectorias de Collatz buscando qué otra malla predice algo.
   Aviso por adelantado: lo más probable es que **no prediga nada**, porque el
   negativo de `cruzarestos.py` (el destino hacia adelante es ciego a los
   restos) sigue en pie. La rueda mod 27 funciona porque el árbol *dobla*, y
   doblar es literalmente esa malla. Sin esa correspondencia estructural, un
   cruce que dé positivo sería sospechoso antes que interesante.
