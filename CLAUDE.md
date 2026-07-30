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

**Trece** de los scripts importan `plotly.graph_objects`; `mallaespejo.py`,
`mallaespejo2.py` y `mallascerradas.py` además usan `plotly.subplots`. Durante
mucho tiempo `plotly` faltaba en `requirements.txt` y el repo no arrancaba en una
máquina limpia — ya está arreglado. `numpy` lo usa **solo `viz3d.py`**.

**Las dos mitades se instalan por separado, y conviene saber cuál te falta.** Al
**30-07-2026**, en el Python 3.14.5 de esta máquina, están las tres:
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

El inventario exacto, para no buscarlo a mano — **ocho** archivos definen
`secuencia_de(n)`: `collazarbol`, `collazcruce`, `collazlamina`, `collazmalla`,
`coralcollaz`, `cruzarestos`, `mallacollaz`, `mallascerradas`. **Dos** la arman
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

Los `.html` y `.png` están en `.gitignore`.

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
`python main.py camino 27` crasheaba desde Sublime. Corrido el **30-07-2026**
sobre los 19 `.py`: **0 hallazgos**, está limpio — si aparece uno nuevo, lo
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
| `maquinitacollaz.py` | Escupe los 114 pasos de un número, uno por línea |
| `teoriacollaz.txt` | El planteamiento filosófico del que salió la idea de la esfera |
| `patron detectado manualmente.txt` | Notas a mano sobre las posiciones 57 y 114 |
| `collazclaude.png` | Captura del coral de Harriss 16°/−8°, para mirarlo sin renderizar. **No está en git** (`*.png` está ignorado): existe solo en esta máquina y no sobrevive a un clon |

Todos los archivos de la tabla están trackeados **salvo `collazclaude.png`**. (Antes
aquí decía que `maquinitacollaz.py` y `patron detectado manualmente.txt` estaban
fuera de git; ya no es cierto, los dos se commitearon.) Para comprobarlo:
`git ls-files`.

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

**La causa, y refuerza la doctrina en vez de romperla: `45 = 3² · 5`.** El retículo
de relaciones enteras entre las 45 raíces tiene rango `45 − 24 = 21`, y las
relaciones son el **triángulo** (`e_k + e_{k+15} + e_{k+30} = 0`, tres direcciones a
120°) y el **pentágono** (cinco a 72°). El segundo choque es literalmente tres
triángulos; el primero es una mezcla que usa la simetría de orden 5. O sea que **el
cierre lo trae la conmensurabilidad del ángulo —16 y 8 dividen a 120—, no Collatz.**
Es el mismo fenómeno que el hexágono, sólo que hace falta llegar a profundidad 31
para verlo.

Conclusión para la pregunta que se hizo: **45 rumbos NO bastan para un árbol
infinito.** El coral de Harriss sí se vuelve a juntar; lo que pasa es que tarda.

*Predicción derivada, sin medir todavía:* si la causa es la factorización de 45,
entonces con un número **primo** de rumbos el único núcleo es la suma de las `p`
raíces, y un choque exigiría acumular las `p` direcciones exactamente por igual. El
umbral de profundidad debería dispararse. Es barato de medir y sería el candidato
serio a nota original sobre el método de dibujo.

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

**Los dos límites honestos:** (1) es matemática conocida — la estructura
mod 6 / mod 9 del árbol inverso es estándar; se llegó de forma independiente.
(2) La rueda gobierna la **contabilidad del árbol hacia atrás** (dónde brota,
qué clase de hijo). El destino hacia adelante sigue ciego a los restos — el
negativo de `cruzarestos.py` sigue en pie. Las dos cosas son ciertas a la vez:
**el esqueleto es periódico, el viaje no.**

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
**0,496064**, que es exactamente lo medido. **Tercera aparición del mismo `+1`** —
las otras dos son el grosor 0,2286 de la lámina y el `+2` del espejo base 2.

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
log₂(altitud(n) / n)  ≥  racha(n) · log₂(3/2) + 1
99.999 casos, 0 fallos, holgura mínima +0,000002
```

Se demuestra en una línea (`k` pasos impares del atajo llevan `n` a al menos
`3^k·n / 2^(k−1)`). **La racha no predice la altitud: le pone un piso exacto**, y el
piso es ajustado para la mayoría. Es lo único de la sesión con la forma de un
teorema en vez de la de una medición, y por eso vale más aunque diga menos.
*(El `+1` del enunciado es `log₂(2)` y viene de mezclar mapas: con el mapa del atajo
el piso es `racha · log₂(3/2)` sin el `+1`, también con 0 fallos.)*

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
| Identidad `(A,B)`, la lámina, `log₂(3)`, las convergentes | Vía clásica de las cotas de ciclos (Crandall, Steiner, Simons–de Weger) |
| Que `F(k+2)` cuente los patrones del mapa clásico | El conteo estándar de "sin dos adyacentes". Folklore |
| Que el rumbo del coral solo dependa de `(A,B)` | Los giros conmutan. Trivial |
| Que los negativos sean `3n−1` y tengan tres ciclos | Estándar: "`3x+1` sobre `Z` tiene cuatro ciclos conocidos". Dos líneas de álgebra |
| Que `3n+1` cicle por encima de `log₂(3)` y `3n−1` por debajo | Se sigue del signo de `C` en la identidad `(A,B)`. Elemental una vez planteado |
| Las constantes de parada `k/ln(4/3)` | Literatura clásica (Lagarias, Applegate–Lagarias). La de Wagon tiene entrada propia en OEIS |
| El umbral `q < 4` del `qn+1` | Es `f = 1/2` reescrito, o sea Terras 1976 otra vez |
| Que la paridad se comporte como moneda | El modelo probabilístico estándar, formalizado en Lagarias–Weiss 1992 y Kontorovich–Lagarias |

**Lo único que podría ser inédito:** la tabla de ángulos de `coralcollaz.py` —
cuántos rumbos permite cada par y qué fracción de ramas colapsa— **ahora con el
umbral medido** (30-07-2026): primer choque exacto en la profundidad **31**, y la
causa identificada en la factorización `45 = 3²·5` vía las relaciones enteras entre
raíces de la unidad. No es un teorema: es una medición sobre nuestro propio método
de dibujo. Pero Harriss eligió ángulos por estética y nadie parece haber barrido el
espacio. Candidata a nota original en visualización recreativa. **Sin verificar en
la literatura.** *(La otra mitad de esa candidatura, la condición del ángulo nulo,
queda debilitada: el `1,7345` en que se apoyaba no era estable.)*

*Un paralelo que tampoco se encontró en las fuentes, buscado explícitamente el
30-07-2026: nadie parece trazar la comparación moneda-física ↔ Collatz en los
términos de "sesgo condicional a la condición inicial". Lo más cerca es Lagarias
diciendo que la paridad se comporta "en cierto sentido como lanzamientos
independientes". "No encontrado" no es "no existe", pero al menos no es obvio.*

### Lo que sí es inusual aquí, y no es matemática

1. **Siete negativos registrados** (el 221 no prefiere restos; el medio es
   contabilidad; el espejo no correlaciona; el puente no llega al segundo paso;
   la altura no codifica magnitud; ninguna constante de Collatz coincide con
   ninguna constante fundamental; la racha no predice la altitud). Casi nadie
   anota lo que no funcionó, y por eso casi todo el mundo repite las mismas
   búsquedas. **Y cinco correcciones a afirmaciones propias que resultaron
   falsas**, que es la parte que de verdad cuesta escribir.
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
(Barina, enero 2025). Resultado general más fuerte: **Tao 2019**, "casi todas las
órbitas alcanzan valores casi acotados".

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

## Siguiente sesión

*(Ya hechos: el espejo en base 2, la rueda del árbol, y —el 30-07-2026— el umbral
de los 45 rumbos, los negativos, las constantes, el ajuste fino y el A/B contra la
moneda. Todo eso está arriba, con sus correcciones.)*

**Nada de lo de abajo está escrito en un fichero todavía: la sesión del 30-07-2026
se hizo entera en scripts sueltos fuera del repo.** Lo primero, si algo de esto
merece quedarse, es convertirlo en programas con la forma de siempre (constantes
arriba, comprobaciones antes del dibujo, `SystemExit` si fallan).

1. **El número primo de rumbos.** La predicción está escrita y sin medir: si los
   choques del coral vienen de que `45 = 3²·5`, entonces con un número **primo** de
   rumbos el único núcleo es la suma de las `p` raíces y el umbral de profundidad
   debería dispararse. Es barato: mismo código, otro ángulo. Y es lo más cerca de
   una nota original que hay en el repo.
2. **Colorear el árbol de `collazarbol.py` con la rueda** — cada rama según la clase
   mod 3 de su semilla — para *ver* el tambor sobre la esfera que ya existe. Y si se
   quiere bajar otro nivel de engranaje, la cuarta rueda: mod 81, orden 54.
3. **El `+1` aparece ya tres veces** (grosor 0,2286 de la lámina, el `+2` del espejo
   base 2, la desviación `−0,0035` de la fracción impar). Las tres son el mismo
   estorbo medido en tres sitios. Vale la pena buscar si se pueden escribir como una
   sola cantidad, porque sería la única cosa del laboratorio que unifica piezas en
   vez de acumularlas.
4. **Persistencia.** No hay base de datos en el repo y hasta ahora no hacía falta.
   Si se van a comparar puntas de mallas grandes o repetir barridos de millones de
   trayectorias, un `.csv` o `.json` de trayectorias evitaría recalcular todo cada
   vez. Sólo si aparece la necesidad — no antes.
