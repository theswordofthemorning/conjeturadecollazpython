# Garzas -- confluencia, libélula y la columna j = 2

24-09-2026. Nace del rechazo del mismo día: la objeción de Irvine fue que
«exactamente 12 posiciones» es una restricción arbitraria. Lo es. Buscando
qué tiene de no arbitrario el parámetro `j`, sale que `j` no puede tomar
cualquier valor: **la mitad de los valores posibles son imposibles**, y eso
se demuestra en diez líneas.

Tres resultados: el **lema de la garza** (quién puede ser un punto de
fusión), el **teorema de la libélula** (`j` es siempre par) y
**`e_2(n) = 1`** con su representante en forma cerrada.

**Atribución, antes de seguir.** El segundo no es nuevo: la ficha
rechazada A399819 ya decía «Only even j occur, since the two orientations
of an opposite-parity position must occur equally often», que es el mismo
hecho con la misma razón. Lo que se añade aquí es la demostración escrita,
el lema de la garza que la refuerza por el otro extremo y la verificación
exhaustiva hasta `2^26`. El primero y el tercero sí son nuevos: no aparecen
en ninguna de las fichas.

Verificador: [`garzas.py`](garzas.py), salida en
[`garzas_salida.txt`](garzas_salida.txt). No importa nada del laboratorio;
es deliberado, para que contraste de verdad con `estratoscadena.py`.

Notación: `T` es la aplicación acortada (A014682), `T(x) = x/2` si `x` es
par y `(3x+1)/2` si es impar. Un par `(r, r+1)` *funde en el paso n* si `n`
es el primer paso con `T^n(r) = T^n(r+1)`; el valor común es el *punto de
fusión* `m`. El par es *balanceado* si las dos trayectorias reciben el mismo
número de entradas impares en esos `n` pasos. `j` es el número de posiciones
`i` (con `0 <= i < n`) en que `T^i(r)` y `T^i(r+1)` tienen paridad opuesta.

## Lema de la garza

**Si `x != y` y `T(x) = T(y) = m`, entonces `{x, y} = {2m, (2m-1)/3}`, esos
dos números tienen paridad opuesta, y `m = 2 (mod 3)`.**

Demostración. Una preimagen par de `m` cumple `x/2 = m`, luego `x = 2m`, y
es única. Una preimagen impar cumple `(3x+1)/2 = m`, luego `x = (2m-1)/3`,
y también es única. Como `x != y` son ambas preimágenes y sólo hay una de
cada paridad, `{x, y}` son exactamente esas dos, de paridad opuesta. Para
que la impar exista hace falta `3 | 2m-1`, esto es `2m = 1 (mod 3)`, o sea
`m = 2 (mod 3)`; y recíprocamente, si `m = 3s+2` entonces
`(2m-1)/3 = 2s+1`, que es impar sin condición adicional. ∎

Un número tiene dos preimágenes si y sólo si es `2 (mod 3)`. Los 199 999
primeros valores lo confirman sin excepción, y los 16 puntos de fusión
distintos que aparecen en el barrido de testigos (2, 11, 20, 38, 47, 101,
173, 182, 209, 236, 524, 911, 1154, 1343, 2045, 5690) son todos `2 (mod 3)`.

## Teorema de la libélula

**En todo par balanceado, `j` es par y `j >= 2`.**

Demostración. Para `0 <= i < n` sea `s_i = [T^i(r) impar] - [T^i(r+1) impar]`,
que vale `0` en las posiciones de igual paridad y `±1` en las opuestas. Ser
balanceado es exactamente `suma de s_i = 0`. Esa suma tiene `j` sumandos no
nulos, todos `±1`; para que se anulen tiene que haber tantos `+1` como `-1`,
luego `j` es par. Y `j >= 1` porque `r` y `r+1` tienen paridad opuesta, así
que la posición `i = 0` ya cuenta; siendo par, `j >= 2`. ∎

(El lema de la garza da lo mismo por el otro extremo: la posición `i = n-1`
también es siempre de paridad opuesta. Para `n >= 2` son dos posiciones
distintas, y como `j` es par, ese par de posiciones es todo lo que un
`j = 2` puede permitirse; de ahí arranca la sección siguiente.)

Consecuencia inmediata: **`e_j(n) = 0` para todo `j` impar.** La mitad de la
tabla de estratos es idénticamente nula, y no por casualidad. Dos barridos
exhaustivos independientes lo confirman sin una sola excepción:
[`garzas.py`](garzas.py) en Python puro hasta `2^18` (2551 pares
balanceados) y [`libelula_amplia.py`](libelula_amplia.py) vectorizado hasta
`2^26`, cubriendo los niveles `n = 3..26` completos. Ningún `j` impar,
ningún `j < 2`.

Conviene no engañarse con esto: **las fichas sí lo decían**. A399819 lo
enunciaba en su comentario décimo, con la misma justificación en una línea.
Que `j = 8, 10, 12` fueran pares no era inocente y estaba escrito. El
editor lo leyó y aun así rechazó, de modo que este hecho, por sí solo, no
es el argumento que faltaba. Lo que aquí se añade es su demostración
completa y el barrido hasta `2^26`; el valor nuevo está en las secciones
siguientes.

## Contraste independiente

`garzas.py` reproduce, sin compartir una línea de código con el laboratorio:

- `A398792` y `A398793` (vía `suma_j e_j(n) = A398793(n-1)`, n = 3..18);
- las tres series históricas de `estratoscadena.py`, que salieron por el
  barrido de la cadena `(k, c)` desde `(0,1)`, un camino completamente
  distinto:

      e8   3, 7, 15, 27, 45, 73, 111, 166, 237   (N = 10..18)
      e10  0, 1, 4, 12, 30, 65, 131, 247, 447
      e12  0, 0, 0, 1, 5, 18, 52, 134, 315

  más el precedente `e8(9) = 1`. Treinta valores, cero discrepancias.

El barrido vectorizado va más lejos: las sumas `suma_j e_j(n)` para
`n = 3..26` dan

    1, 1, 2, 2, 3, 4, 6, 11, 19, 34, 60, 106, 190, 341, 623, 1148,
    2124, 3963, 7451, 14072, 26699, 50913, 97379, 186769

que son, término a término, los 24 primeros valores no nulos de A398793 tal
como está **aprobada en OEIS**. Es decir: 24 términos de una sucesión
publicada revalidados por un enumerador que no comparte una línea con el
que los produjo.

Dos implementaciones sin código común dando los mismos números es la mejor
evidencia que tenemos de que la tabla de estratos está bien calculada.

## Columnas extremas

Las dos primeras columnas no nulas son constantes iguales a 1 —demostrado
para `j = 2`, comprobado para `j = 4`— con representante en forma cerrada:

    j = 2:  r = 2^(n-2) - 2      si n es par
            r = 3·2^(n-2) - 2    si n es impar

    j = 4:  r = 3·2^(n-2) - 3    si n es par
            r = 2^(n-2) - 3      si n es impar

y su punto de fusión recorre `m_k = (9^(k+1) - 1)/4 = 2, 20, 182, 1640,
14762, ...`, que satisface `m_{k+1} = 9·m_k + 2`. Para `j = 2` el índice es
`k = (n-3)/2` truncado; para `j = 4`, `k = (n-4)/2` truncado.

### La columna `j = 2`: teorema

**Teorema. Para todo `n >= 4`, `e_2(n) = 1`**, y el único par es
`r = 2^(n-2)-2` si `n` es par, `r = 3·2^(n-2)-2` si `n` es impar.

La prueba tiene dos mitades: una reducción a dos candidatos y el descarte
de uno de ellos.

Demostración. Si `j = 2`, las dos posiciones de paridad opuesta son la
primera y la última: la `i = 0` porque `r` y `r+1` siempre difieren en
paridad, la `i = n-1` por el lema de la garza, y no hay más porque `j = 2`.
Luego para `1 <= i <= n-2` las dos trayectorias tienen igual paridad, de
modo que `d_i = T^i(r+1) - T^i(r)` es par, y cada paso lo transforma en
`d_i/2` (ambos pares) o `3·d_i/2` (ambos impares). En `i = n-1` las
paridades son opuestas y `d_(n-1)` es impar. Recorriendo los `n-2` pasos,

    |d_(n-1)| = |d_1| · 3^u / 2^(n-2)

con `u` el número de posiciones intermedias de paridad impar. Como
`3^u` no aporta factores 2 y `d_(n-1)` es impar, `|d_1| = 2^(n-2)·q` con
`q` impar.

Ahora el primer paso. Si `r` fuera impar, `d_1 = -r` sería impar, y
`2^(n-2)·q` impar exige `n = 2`: **para `n >= 3` todo par con `j = 2`
tiene `r` par**, y entonces `d_1 = r+2`. De `r + 2 = 2^(n-2)·q` junto con
`0 <= r < 2^n` sale `q < 4 + 2^(3-n) <= 5`, y siendo `q` impar sólo quedan
`q = 1` y `q = 3`, esto es `r = 2^(n-2)-2` y `r = 3·2^(n-2)-2`. ∎

El barrido confirma cada eslabón para `n = 3..22`: el testigo es siempre
par, el exponente de 2 en `r+2` es exactamente `n-2`, y `q` vale 3 en los
niveles impares y 1 en los pares, sin excepción. Verificador:
[`unicidad.py`](unicidad.py), salida en
[`unicidad_salida.txt`](unicidad_salida.txt).

### Y por qué gana uno de los dos

Los dos candidatos hacen lo mismo hasta el final: ambos recorren las
posiciones `1..n-2` con paridades iguales y llegan a la posición `n-1` con
un par que cumple `y = 3x+1`. Sólo se separan ahí, y por un criterio
elemental:

**Un par con `y = 3x+1` funde en el paso siguiente si y sólo si `x` es
impar.** Si `x` es impar, `T(x) = (3x+1)/2 = y/2 = T(y)`, porque `y` es par.
Si `x` es par, `T(x) = x/2` mientras `T(y) = (9x+4)/2`, y la igualdad
exigiría `x = -1/2`. ∎

Los pares que aparecen en esa posición son siempre los mismos, y son
reconocibles: `x_k = (3^k - 1)/2` (repunits de base 3: 0, 1, 4, 13, 40,
121, 364, 1093, ...) con `y_k = 3·x_k + 1 = (3^(k+1) - 1)/2`. Y
`x_k` es impar exactamente cuando `k` es impar, porque `3^k = 3 (mod 4)`
para `k` impar y `1 (mod 4)` para `k` par. De ahí la alternancia entre
`q = 1` y `q = 3` según la paridad de `n`.

Esto también explica el punto de fusión, que deja de ser una observación:
para `k` impar el valor común es

    T(x_k) = (3^(k+1) - 1)/4 = (9^((k+1)/2) - 1)/4

es decir 2, 20, 182, 1640, 14762, ... y la recurrencia `m -> 9m+2` es su
forma cerrada, no un patrón observado.

Las dos familias están catalogadas, lo que da referencias cruzadas reales
y no inventadas: los `x_k` son **A003462**, `(3^k-1)/2`, y los puntos de
fusión son **A125857**, los números que en base 9 se escriben `22...2`.
Que la columna extrema de los estratos aterrice exactamente en dos
sucesiones clásicas es el mejor argumento de que el corte por `j` no es
una etiqueta nuestra. Verificador: [`perdedor.py`](perdedor.py), salida en
[`perdedor_salida.txt`](perdedor_salida.txt); tesis comprobada sin
excepciones en `n = 3..25` y el criterio en 100 000 valores.

### El cierre: las trayectorias son explícitas

Queda ver con qué `k` llega cada candidato, y esto sí se calcula. Las dos
trayectorias tienen forma cerrada `3^a · 2^b - 1`. Para `n` par, con
`r = 2^(n-2)-2` y `r+1 = 2^(n-2)-1`, y para `1 <= i <= n-2`:

    x_i = 3^(i-1) · 2^(n-2-i) - 1        y_i = 3^i · 2^(n-2-i) - 1

y para `n` impar, con `r = 3·2^(n-2)-2`:

    x_i = 3^i · 2^(n-2-i) - 1            y_i = 3^(i+1) · 2^(n-2-i) - 1

Ambas se comprueban por inducción inmediata: si `z = 3^a·2^b - 1` con
`b >= 1`, entonces `z` es impar y `T(z) = 3^(a+1)·2^(b-1) - 1`. De aquí
sale todo de golpe:

- mientras `b = n-2-i >= 1`, ambas son impares; en `i = n-2` ambas valen
  `3^a - 1` y son pares. **Todas las posiciones intermedias tienen paridad
  igual**, luego `j = 2` como se pedía;
- `x_i` e `y_i` difieren en un factor 3, así que nunca coinciden antes:
  la fusión es la **primera** y cae exactamente en el paso `n`;
- en `i = 0` el par es (par, impar) y en `i = n-1` es (impar, par): los dos
  desequilibrios se cancelan y **el par es balanceado**;
- en `i = n-1` queda `x = (3^k-1)/2` con `k = n-3` si `n` es par y `k = n-2`
  si `n` es impar. **En ambos casos `k` es impar**, luego `x` es impar y el
  par funde. Para el otro candidato el índice es el vecino, que es par, y
  por el criterio no funde. ∎

Contrastado contra la iteración real en `n = 4..60`, sin un solo fallo:
[`cierre_e2.py`](cierre_e2.py), salida en
[`cierre_e2_salida.txt`](cierre_e2_salida.txt).

### La columna `j = 4` se reduce a la anterior

No hace falta empezar de cero: la columna `j = 4` del nivel `n` es la
columna `j = 2` del nivel `n-2` disfrazada. En el par de `j = 4` las cuatro
posiciones opuestas no están dispersas, son `0, 1, 2` y `n-1`; tras dos
pasos el par vuelve a ser consecutivo, `(z, z+1)`, y

    z = r_2(n-2)   (mod 2^(n-2))

donde `r_2` es el representante ya demostrado de `j = 2`. Por Terras eso
basta para que el perfil de los `n-2` pasos restantes sea el mismo. Y hay
un detalle que lo hace nítido: el par de `j = 4` del nivel `n` es
`(r, r+1)` donde `r+1` es justamente el **candidato perdedor** de `j = 2`
de ese mismo nivel.

Comprobado sin fallos en `n = 6..39`: [`columna4.py`](columna4.py), salida
en [`columna4_salida.txt`](columna4_salida.txt).

Y hay una razón, no una coincidencia. Conviene reformular la definición:

**La posición `i` es de paridad opuesta si y sólo si `d_i = T^i(r+1) - T^i(r)`
es impar** —dos números difieren en paridad exactamente cuando su resta es
impar—. Así `j` cuenta las veces que `d` es impar, y como `d_0 = 1`, la
posición 0 siempre cuenta. (Esto vuelve a dar la libélula de un vistazo.)

Con eso, todo depende de `r` módulo 4, y se calcula en dos líneas:

- **`r` par:** `d_1 = r+2`, par, luego la posición 1 no es opuesta.
- **`r = 1 (mod 4)`:** entonces `x_1 = (3r+1)/2` es par e `y_1 = (r+1)/2`
  impar, de donde `x_2 = (3r+1)/4`, `y_2 = (3r+5)/4` y **`d_2 = 1` exacto**:
  el par vuelve a ser consecutivo tras dos pasos, habiendo gastado las
  opuestas 0 y 1.
- **`r = 3 (mod 4)`:** `d_2 = -2r-1`, impar, así que la posición 2 también
  es opuesta y el par gasta opuestas más deprisa.

Comprobado sin discrepancias en `r = 1..199999`.

### Una recursión para toda la clase `r = 1 (mod 4)`

El caso `r = 1 (mod 4)` no sólo se reduce: da una recursión exacta, y se
calcula a mano. Con `r = 4k+1`:

    x_0 = 4k+1 (impar)   y_0 = 4k+2 (par)     posición 0 opuesta, signo +
    x_1 = 6k+2 (par)     y_1 = 2k+1 (impar)   posición 1 opuesta, signo −
    x_2 = 3k+1           y_2 = 3k+2           d_2 = 1: par consecutivo

El par reaparece como `(r', r'+1)` con `r' = 3k+1 = (3r+1)/4`, habiendo
gastado dos posiciones opuestas **de signos contrarios**, que por tanto se
cancelan en el balance. De ahí, para todo `r = 1 (mod 4)`:

    n(r) = 2 + n(r')       j(r) = 2 + j(r')       r balanceado <=> r' lo es

Contrastado en 54 623 pares, sin un fallo.

**Corolario: si `j = 4` entonces `r = 5 (mod 8)`.** En efecto `j(r) = 4`
obliga a `j(r') = 2`, que por el teorema de la columna exige `r'` par; y
`r' = 3k+1` es par exactamente cuando `k` es impar, o sea `r = 5 (mod 8)`.
Las clases módulo 8 observadas con `j = 4` son, en efecto, sólo la 5.

Como además `e_2(n-2) = 1` y la aplicación `r -> (3r+1)/4` es inyectiva,
**hay a lo sumo un par con `j = 4` y `r = 1 (mod 4)` en cada nivel**.

Y la recursión no sirve sólo para la columna: como `r -> (3r+1)/4` lleva
`{r = 1 (mod 4)}` biyectivamente sobre `{r' = 1 (mod 3)}`, da una identidad
de conteo para **toda** la tabla,

    #{r = 1 (mod 4) de nivel n y estrato j}
      = #{r' = 1 (mod 3) en [0, 3·2^(n-2)) de nivel n-2 y estrato j-2}

donde el rango importa: `r < 2^n` da `r' < 3·2^(n-2)`, no `2^(n-2)`. Con el
rango correcto la igualdad es exacta en `n = 7..18` y en todos los
estratos, sin una sola diferencia. Un tercio de cada fila de la tabla queda
así determinado por la fila de dos niveles antes.

Las clases pares se calculan igual de fácil, y el análisis se ramifica por
clases módulo `2^s`:

- `r = 4l+2`: `x_1 = 2l+1`, `y_1 = 6l+5`, ambos impares, y luego
  `d_2 = 6l+6` par: dos posiciones seguidas sin gastar nada.
- `r = 4l`: `x_1 = 2l`, `y_1 = 6l+2`, ambos pares; pero `d_2 = 2l+1` es
  impar, así que la posición 2 sí es opuesta. Y si además `l` es impar,
  `x_3 = y_3 = (3l+1)/2` y el par **funde en el paso 3** —de ahí que el
  primer testigo de todos sea `r = 4`.

El `j` mínimo por clase módulo 8 queda así:

    0->6   1->6   2->2   3->6   4->2   5->4   6->2   7->8

es decir `j = 2` sólo en las clases 2, 4, 6 y **`j = 4` sólo en la clase 5**,
como predice el corolario.

La clase `r = 3 (mod 4)` se trata con el mismo cálculo. Con `r = 4k+3`,
las posiciones 0, 1 y 2 son opuestas (`d_2 = -2r-1`, impar), y en el paso
siguiente `d_3 = -13k-12` si `k` es impar —impar, luego una cuarta
opuesta— frente a `d_3 = -3k-2` si `k` es par. Es decir:

- `r = 7 (mod 8)`: opuestas en 0, 1, 2, 3, más la de `n-1`: son cinco, y
  siendo `j` par, `j >= 6`. **Descartada para `j = 4`.**
- `r = 3 (mod 8)`: `d_3` par, y el caso queda abierto.

Estado de `e_4(n) = 1`, por clases módulo 8:

| clase de `r` | estado |
|---|---|
| `5 (mod 8)` | a lo sumo uno, por la recursión — **resuelto** |
| `1 (mod 8)` | `j >= 6` por la recursión — **resuelto** |
| `7 (mod 8)` | `j >= 6` por el cálculo de arriba — **resuelto** |
| `3 (mod 8)` | abierto |
| `r` par | abierto |

En los dos casos abiertos el barrido no encuentra ningún `j = 4` (los `j`
alcanzados son `6, 8, ...` y `2, 6, 8, ...` respectivamente), pero eso es
un barrido, no una prueba. Verificador: [`recursion.py`](recursion.py),
salida en [`recursion_salida.txt`](recursion_salida.txt).

Para `j = 4` no tengo el argumento análogo: ahí las posiciones opuestas
son cuatro y no están forzadas a posiciones concretas.

Qué está comprobado y qué no, con precisión:

- que esos `r` **son** pares balanceados que funden en el paso `n` con ese
  `j` y ese punto de fusión: 234 comprobaciones, `n = 3..120`, sin fallos.
  A `n = 60` el testigo es `r = 288230376151711742` y el punto de fusión
  tiene 28 cifras, muy lejos de cualquier barrido;
- para `j = 2`, que es **el único** de su columna: demostrado arriba, para
  todo `n >= 4`;
- para `j = 4`, que es el único de la suya: sólo por barrido exhaustivo de
  los `2^n` residuos hasta `n = 26`, sin excepción. Ahí sigue siendo
  conjetura.

La distinción importa: un barrido finito no es una demostración universal, y
confundir las dos cosas es exactamente lo que hundió las fichas.

## Contraste con la literatura

Esto es lo que más pesa, y no lo vi hasta el final: **las dos columnas
extremas no son objetos nuestros, son las familias clásicas.**

- `j = 2` da la familia de **Garner**, `(8k+4, 8k+5)`.
- `j = 4` da las de **Wu y Huang**: `(32m+5, 32m+6)`, `(64m+45, 64m+46)`,
  `(128m+29, 128m+30)`. Los representantes `r_4(5)=5`, `r_4(6)=45`,
  `r_4(7)=29` coinciden término a término con las tres familias que cita
  la bibliografía de Lagarias.

Es decir: el corte por `j` no es una etiqueta inventada para ordenar una
tabla. Sus dos primeros valores reproducen exactamente las dos familias
que la literatura ya había aislado, y el teorema `e_2(n) = 1` dice algo
nuevo sobre la de Garner: **es la única de su tipo en cada nivel**.

### El contraejemplo de Elia y Tucker: ya estaba usado

Esto tampoco es nuevo, y hay que decirlo. Elia y Tucker (arXiv:1511.09141)
dieron una familia infinita de **contraejemplos a la conjetura de Garner**,
`2^19·m + 3067`. El laboratorio ya los tenía localizados y verificados
desde agosto, la ficha A399819 ya traía el par `(3067, 3068)` con sus ocho
posiciones, y la respuesta a Irvine del 17-09 lo usaba como argumento
explícito de conexión con la literatura. No convenció. Reutilizarlo como
novedad sería repetir una carta ya jugada.

El parámetro `j` no se ve afectado, y se comprueba:

- el par `(3067, 3068)` funde en el paso 18 con `j = 8`, balanceado, y su
  punto de fusión es 692, que cumple `692 = 2 (mod 3)` como exige el lema
  de la garza;
- los 40 primeros miembros de la familia comparten paso y `j`, y todos
  tienen `j` par.

Sirve como control, no como argumento: donde falla la caracterización
clásica, la clasificación por `j` coloca el contraejemplo sin incidentes, y
los números coinciden con los que ya constaban en la ficha.

Su Teorema 2.1 (`n = 4 (mod 8)`, `n > 4`, funden en el tercer paso) se
reproduce aquí sin fallos en 24 999 casos. Es el mismo hecho que sale del
cálculo de las clases pares de más arriba: **lo que yo había derivado como
propio ya estaba publicado en 2015**, y hay que citarlo como suyo.

Verificador: [`literatura.py`](literatura.py), salida en
[`literatura_salida.txt`](literatura_salida.txt).

## Testigos mínimos

`a(n)` = menor `r` tal que `(r, r+1)` funde por primera vez en el paso `n` y
es balanceado. Tramo contiguo certificado `n = 3..132` (130 términos; cada
uno mínimo porque el barrido recorre `r` en orden creciente desde 0):

    4, 2, 5, 14, 29, 62, 65, 131, 314, 257, 515, 840, 1415, 943, 747,
    1256, 1134, 1671, 1646, 1790, 1771, 1179, 2359, 4723, 3144, 6288,
    4193, 2795, 5022, 9403, 3051, ...

La lista completa está en la sección 6 de `garzas_salida.txt`. Los primeros
términos no son nuestros: `a(3) = 4` es la familia de Garner `(8k+4, 8k+5)`
y `a(5) = 5` la de Wu y Huang `(32m+5, 32m+6)`, ambas ya citadas en A398792.

Corrección a una observación de ayer: el punto de fusión parecía quedarse
clavado en 38 desde `n = 23`. Era un artefacto del rango: a partir de
`n = 31` salta a 911, 11, 47, y en los niveles altos domina el 20. No hay
ley ahí, sólo un tramo corto.

## Qué queda abierto

1. `e_4(n) = 1`: falta sólo probar que toda solución con `j = 4` tiene sus
   posiciones opuestas en `0, 1, 2, n-1`. Hecho eso, la reducción de arriba
   la remite al caso `j = 2`, ya demostrado.
2. (cerrado el 24-09: la forma cerrada de los representantes, el punto de
   fusión y la recurrencia `m -> 9m+2` quedan demostrados arriba).
3. Saber si existe testigo para todo `n`. El argumento del par
   `(2^j - 2, 2^j - 1)` sólo cubre niveles pares; el tramo `3..132` es
   empírico.
4. Si `e_2` y `e_4` son constantes, ¿cuál es la primera columna que crece?
   `e_6` crece despacio (1, 2, 3, 6, 9, 13, 18, 24, 31, 39, 48, 58 para
   `n = 7..18`): diferencias 1, 1, 3, 3, 4, 5, 6, 7, 8, 9, 10, que no es
   regular al principio y sí después.

Nada de esto se ha enviado a ningún sitio.
