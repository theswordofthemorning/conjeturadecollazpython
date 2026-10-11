# El primo de Mahler: una herramienta individual contra el cohete

**Estado: cerrado (07-10-2026, noche), versión corta.** Documenta
identidades y una limitación de la vía; no excluye al cohete. Se propuso
el 07-10 por la noche como segunda idea para avanzar y quedó documentada mientras se hacía
la primera, la
[sexta raíz y el techo](../perdices20261007/TAMANO.md#sexta-raíz-y-techo-en-lean).
Esa misma noche el usuario la eligió con el
[plan corto](#plan-corto-elegido-el-07-10): una sesión para leer los
originales con tres preguntas y cerrar bien, no para construir encima. Se
leyeron todos, incluido el de Flatto–Lagarias–Pollington, y las tres
preguntas quedaron respondidas; ver la
[lectura de los originales](#lectura-de-los-originales-07-10-noche). Queda
en el registro como `mahler_primo_cohete`.

## Por qué hace falta

En el [plano de la casa](../casa20261004/LEEME.md), del muro B quedan dos
especies de fugitivo: el planeador intermitente y el cohete. Todo lo que
tenemos contra ellas (la estela, Perdices, la sexta raíz) dice de varias
formas que el fugitivo **aterriza poco**: son cotas superiores para sus
regresos a pronóstico bajo. Un cohete tiene pronóstico `P_k → ∞`, así que
para cada techo C regresa sólo un número finito de veces. Ninguna cota de
regresos lo alcanza: un avión que nunca aterriza no usa pistas.

Hace falta una propiedad del **número individual**, y no de una población
(Terras, Korec y Tao dicen «casi todos»). Debe usar dos cosas a la vez:
que el fugitivo es un entero positivo, y no un fantasma 2-ádico como el −1,
y que la máquina multiplica por 3/2. La casa lo llama «de carne y hueso y
del 3».

## El problema hermano: los números Z de Mahler (1968)

Mahler preguntó si existe un número real `ξ > 0` tal que la parte
fraccionaria de `ξ·(3/2)^n` sea menor que 1/2 para todo `n ≥ 0`. A esos
números se los llama números Z. La pregunta sigue abierta y Mahler
conjeturó que no existen. Probó que hay a lo sumo uno en cada intervalo
`[g, g+1)` y, para x grande, a lo sumo `x^0,7` por debajo de x (pp. 315 y
321).

**La traducción a una órbita.** Sea `g(x) = ⌈3x/2⌉`, es decir, `3x/2` si x
es par y `(3x+1)/2` si es impar. Si hay un número Z en `[g, g+1)`, la órbita
de g por esa máquina nunca cae en un número que deja resto 3 al dividir
por 4. Se comprueba en pocas líneas. Sean `g_n` la parte entera y
`f_n ∈ [0, 1/2)` la fraccionaria de `ξ(3/2)^n`. Si `g_n` es impar,
`f_{n+1} = 3f_n/2 − 1/2` sólo cae bajo 1/2 cuando `f_n ≥ 1/3`, y entonces
`f_{n+1} < 1/4`. Si `g_{n+1} = (3g_n+1)/2` también fuera impar, haría falta
`f_{n+1} ≥ 1/3`: imposible. Por eso tras un impar viene un par, lo que
obliga a `g_n ≡ 1 (mod 4)`.

**Corrección del 07-10 por la noche.** Esta nota decía «si y sólo si»,
copiado de la bibliografía anotada de Lagarias (entrada 117). El original
sólo afirma la mitad de arriba: el algoritmo «provides a necessary (but not
a sufficient) condition» (Mahler, p. 317). Detalle en
[Mahler dice «sólo si»](#mahler-dice-sólo-si).

Es la misma figura que nuestro cohete: un número concreto cuya órbita, en
una máquina de ×3/2, esquiva algo para siempre. La heurística de las dos
dice que no se puede.

**Lo que allá sí se sabe probar.** Flatto, Lagarias y Pollington (1995):
para `ξ > 0` y enteros coprimos `p > q ≥ 2`,

```text
limsup {ξ (p/q)^n} − liminf {ξ (p/q)^n} ≥ 1/p.
```

Para 3/2, las partes fraccionarias no pueden quedar encerradas en una
ventana más angosta que 1/3. No resuelve el problema de Mahler, cuya
ventana mide 1/2. Pero es un teorema sobre **un** ξ, y usa que las partes
enteras son enteras. Es el tipo de pieza que le falta a la casa: el
retrato hablado imposible, «no cabe por esa ventana». Mahler ya lo había
preguntado al cerrar su artículo: si su teoría valdría para ventanas más
cortas que 1/2 (p. 321). La lectura mostró por qué no llega al cohete:
[necesita un pasillo](#el-ingrediente-de-1995-necesita-un-pasillo).

Lagarias describe como indirecta la relación entre el problema de Mahler
y el 3x+1. La lectura del 07-10 por la noche encontró ya publicada la parte
de las dos reglas; ver [la lectura](#lectura-de-los-originales-07-10-noche).

## El diccionario propuesto

Esta parte es de cosecha propia; después la encontramos en Mahler (ver
[las dos reglas](#las-dos-reglas-ya-son-de-mahler)). Mapa: el atajo
`T(x) = x/2` si x es par y `(3x+1)/2` si es impar, sobre los enteros,
incluidos los negativos para los fantasmas. `S_k` cuenta las entradas
impares de los instantes `j < k`, el pronóstico es `P_k = 3^S_k/2^k` y el
tamaño normalizado es

```text
R_k = T^k(x)/P_k = x + (1/3) · Σ_{j<k, T^j(x) impar} 1/P_j.
```

Es la identidad afín de [PerdicesTamano](../perdices20261007/PerdicesTamano.lean)
(`identidad_afin`, en naturales); para negativos el álgebra es la misma.

1. **La estatura ξ.** Para `x = n > 0`, R_k nunca disminuye y nunca baja
   de n. Existe `ξ = lim R_k`, con `n ≤ ξ ≤ ∞`.
2. **Sólo los cohetes rápidos.** `ξ < ∞` exactamente cuando la suma de
   `1/P_j` sobre los pasos impares converge. Un planeador intermitente
   tiene `ξ = ∞`. Si `P_j ≤ C`, el siguiente paso impar `j' ≥ j` cumple
   `P_j' ≤ C`, porque en medio sólo hubo pasos pares. Eso da infinitos
   términos de al menos `1/C`. Un cohete lento, por ejemplo con
   `P_k ≈ k^0,9`, también puede tener `ξ = ∞`. El rasgo 9 sólo garantiza
   `P_k > k^α` casi siempre, para `α < 5/6`, y eso no basta para converger.
3. **La cola.** Si `ξ < ∞`, entonces `T^k(n) = ξ·P_k − t_k`, con
   `t_k = (1/3) Σ_{j≥k, impar} P_k/P_j ≥ 0`. La cola depende sólo de los
   pasos futuros y vale al menos 1/3 cuando `T^k(n)` es impar. En un tramo
   finito vale la versión exacta `T^k(n) = R_K·P_k − t_k^(K)`, sin límites.
4. **Los fantasmas pesan cero.** Toda órbita de valores acotados con
   `P_k → ∞` tiene `ξ = lim T^k(x)/P_k = 0`. Ejemplos exactos:
   - −1: todo impar, `R_k = −(2/3)^k`;
   - el circuito −5 → −7 → −10: `R_3m = −5·(8/9)^m`;
   - el circuito del −17 (11 pasos, 7 impares): `R_11m = −17·(2048/2187)^m`.

   Un cohete de verdad, en cambio, tendría `ξ ≥ n > 0`.

Así, «¿hay un cohete rápido?» toma la forma «¿hay un `ξ > 0` tal que
`ξ·P_k − t_k` sea, para todo k, un entero con la paridad que dicta su
propio futuro?». Es la forma de la pregunta de Mahler, cuyo `ξ = 0` también
es la solución trivial. **Es una analogía de forma, no una equivalencia.**

Alegoría: ξ es la estatura del número medida con la regla del pronóstico.
Los fantasmas miden cero. Un cohete de carne y hueso mediría al menos n.

## Lectura de los originales (07-10, noche)

Se leyeron enteros Mahler (1968, 9 páginas) y Flatto–Lagarias–Pollington
(1995, 23 páginas), y las dos primeras páginas de Bernstein (1994). De
Rozier (2019) se leyó el §3.2; de López y Stoll (2009), el resumen y el §5;
de Lu y Zheng (2026), la introducción y el §2. El de 1995 lo trajo el
usuario, porque la web de IMPAN filtra las descargas automáticas. Las
copias están en `lecturas/`, fuera de Git.

### Las dos reglas ya son de Mahler

La estatura del diccionario se puede medir con dos reglas. Para una semilla
x del atajo, sean `d_0 < d_1 < …` sus instantes impares y

```text
σ^(K) = Σ_{d_m < K} 2^{d_m} / 3^{m+1},     R_K = x + σ^(K) = 2^K · T^K(x) / 3^{S_K}.
```

- **Regla de siempre (la real).** Si la serie converge, `R_K → ξ = x + σ_∞`.
- **Regla 2-ádica**, en la que un número es más pequeño cuantas más veces se
  deja dividir entre 2. `R_K` lleva `2^K` delante y `T^K(x)` es entero, así
  que tiende a 0. Por eso `x = −σ_2`: la misma serie, sumada con esa regla.

Entonces `ξ = σ_∞ − σ_2`: la estatura es la diferencia entre las dos sumas
de una misma serie. En un fantasma las paridades se repiten y la serie es
geométrica, de razón `r = 2^p/3^q < 1`. Esa razón es pequeña con las dos
reglas, así que las dos sumas dan el mismo racional y `ξ = 0`: −1 suma 1, el
circuito del −5 suma 5 y el del −17 suma 17. En el 1, que gira 1 → 2 → 1, la
razón es 4/3: la suma real diverge y la 2-ádica vale −1, de modo que
`x = 1`. Un cohete de verdad mediría al menos n con la regla de siempre y 0
con la 2-ádica.

Nada de esto es nuevo:

- **Mahler (1968, p. 315)** lo escribió para su máquina. La serie
  `ε_0 + (2/3)ε_1 + (2/3)²ε_2 + ⋯` vale `3r_0` en los reales (su fórmula 8)
  y `−3g_0` en sentido 2-ádico (fórmula 10). Comenta: «It is rather
  interesting that the same series converges in two different senses and
  to two different limits».
- **Bernstein (1994)** dio la regla 2-ádica para el 3x+1:
  `N = (−1/3)2^{d_0} + (−1/9)2^{d_1} + (−1/27)2^{d_2} + ⋯`, leído en el
  original.
- **La regla real sobre la misma serie** ya se estudió. López y Stoll
  (2009, §5) la evalúan en palabras sturmianas. Sale una escalera del
  diablo, y la serie converge sólo si la proporción de impares supera
  `ln 2/ln 3`. Rozier (2019, p. 7) cita además a Edgington y a
  Matthews–Watts. Dice que se espera que la serie diverja en los enteros
  positivos y converja en los negativos.

Nuestra lectura, «la serie converge en los reales exactamente cuando n es
un cohete rápido», es el `α = g_0 + r_0` de Mahler copiado al atajo. No
reclamamos nada.

### Mahler dice «sólo si»

- p. 317: «It thus provides a necessary (but not a sufficient) condition
  for G_1 to be the integral part of a Z-number».
- p. 316: de su desigualdad (12) «one can deduce restrictions» sobre los
  instantes con `ε_m = ε_{m+2} = 1` y `ε_{m+1} = 0`. Las omite porque no las
  usa.
- pp. 318–321: la cuenta `x^0,7` usa sólo la condición necesaria. Cuenta
  palabras sin dos impares seguidos, que son números de Fibonacci, y usa
  que la razón áurea es menor que `2^0,7`.

Flatto (1992) bajó luego el exponente a `log₂(3/2) ≈ 0,585` con la dinámica
completa. Lo confirman FLP (1995, p. 127), que muestran la cuenta en su
p. 135.

La condición completa es la desigualdad (12) de Mahler:
`3r_m = ε_m + (2/3)ε_{m+1} + (2/3)²ε_{m+2} + ⋯ < 3/2`. El patrón impar, par,
impar, par, impar ya suma al menos `1 + 4/9 + 16/81 = 133/81 > 3/2`. Está
prohibido aunque no tenga dos impares seguidos.

Esa condición sí tiene un «si y sólo si» publicado, pero no es el del
resto 3. Con `θ = 2r`, la recurrencia `r_n = ε_n/3 + (2/3)r_{n+1}` se vuelve
`θ_{n+1} = 3θ_n/2 − ε_n`, con `ε_n = ⌊3θ_n/2⌋`: las paridades de g son los
dígitos de θ en la máquina `x ↦ 3x/2 (mód 1)`. FLP (1995, Proposición 2.1,
a partir del desacople de Flatto, 1992) lo enuncian como equivalencia: hay
un número Z en `[g, g+1)` si y sólo si las paridades de g son los dígitos
de algún `θ ∈ [0, 1)`.

[cotejar_mahler.py](cotejar_mahler.py) lo cuenta con fracciones exactas:

- **El 13 de Mahler.** Su algoritmo lo descarta en `g_21 = 67251`, que deja
  resto 3 (la tabla de la p. 317, reproducida). La prueba fina lo descarta
  antes, en `g_10`: 153, 230, 345, 518 y 777 son impar, par, impar, par,
  impar.
- **Ventanas.** De los `2^L` restos de g módulo `2^L`, los que esquivan el
  resto 3 son un número de Fibonacci: 13 con L = 5 y 832 040 con L = 28.
  Pasan la prueba fina 12 y 132 186. Con L = 5 la única diferencia es
  10101. La cuenta fina crece casi exactamente ×1,5 por paso
  (132 186/88 123 ≈ 1,500). La razón medida es de ventana, pero el ritmo
  tiene teorema: la prueba fina es el criterio de FLP cortado a L dígitos,
  y FLP acotan esa cuenta por `c·(3/2)^L` (fórmula 2.20, tomada de Flatto y
  Lagarias, 1994). De ahí sale el exponente de Flatto.

Matiz: esto no refuta el «si y sólo si» como enunciado global. Nadie conoce
una órbita que esquive el resto 3 para siempre, y si no hay ninguna, la
equivalencia se cumple de vacío. Lo erróneo es atribuírsela a Mahler: él
sólo prueba la necesidad, y su argumento sólo da eso. La entrada 128 de la
misma bibliografía, sobre Michel (1993), lo cita bien, en un solo sentido.

### El ingrediente de 1995 necesita un pasillo

**Confirmado con el original**, leído entero. La prueba del teorema 1.4
tiene cinco pasos, y el pasillo aparece en el primero:

1. **Fabricar el pasillo** (pp. 138–139). Si el ancho fuera menor que 1/p,
   desde cierto k todas las partes fraccionarias caerían en una ventana
   `[s', s'+t')` con `t' < 1/p`. La prueba sigue con `ξ' = ξ(p/q)^k`.
2. **Desacoplar** (proposición 2.1 y lema 2.1, pp. 131–133). Dentro de la
   ventana, las partes enteras siguen una máquina fija sobre los naturales
   y las fraccionarias, la transformación `θ ↦ (p/q)θ + α (mód 1)`; los
   símbolos de las dos coinciden salvo una permutación fija. Fuera de la
   ventana falla: «condition (C1) is crucial for Lemma 2.1» (p. 133).
3. **Pocos supervivientes** (teoremas 3.3 a 3.5, pp. 140–146). Para un
   conjunto denso de posiciones s, la transformación deja sólo un número
   finito de puntos que no salen nunca de la ventana `[s, s+1/p)`.
4. **Palomar** (teorema 3.2, p. 139). Con finitos puntos, la órbita de θ
   se repite, y dos partes enteras distintas tendrían los mismos símbolos
   para siempre.
5. **Choque con los enteros** (lema 2.2, p. 133). Cada palabra de k
   símbolos sale de un solo resto módulo `q^k`, así que dos enteros
   distintos no pueden tener todos sus símbolos iguales.

La demostración moderna de Dubickas, que Lu y Zheng (2026, §2) reexponen,
es más directa: escribe las partes fraccionarias como una serie de
«dígitos» enteros de razón fija q/p, usa que esos dígitos no se repiten
por ser enteros y mide el ancho con Morse–Hedlund, sin desacoplar. Llega a
lo mismo, un ancho mínimo, así que tampoco dice nada fuera de un encierro.

Trasladado al cohete:

- **Sólo el paso 5 no pide encierro, y le sale gratis.** Para el atajo es
  la biyección de paridades (Terras, 1976; Everett, 1977): cada palabra de
  largo L sale de un solo resto módulo `2^L`. Un cohete la cumple sin
  contradicción. Lo que la haría morder, que sus paridades se repitieran,
  lo convertiría en circuito: es la cuenta de los fantasmas, donde las dos
  reglas coinciden y dan `ξ = 0`.
- **Los pasos 1 a 4 necesitan pasillo, y el cohete no vive en ninguno.**
  Como `T^k(n) = ξ·P_k − t_k` es entero, la parte fraccionaria de `ξ·P_k`
  es la de su cola `t_k`, y ser cohete no la encierra en ningún sitio.
  Además, no hay una razón fija que desacoplar: los pesos de la cola se
  doblan en los pasos pares y se multiplican por 2/3 en los impares.

**El obstáculo, en una frase.** El teorema de 1995 prohíbe encierros, y el
cohete vuela a cielo abierto. Su única atadura es ser entero, y eso se mide
con la regla 2-ádica. Para que el paso 5 muerda haría falta lo contrario:
algo que obligue a repetirse a las paridades de un entero. Esa es la
conjetura de periodicidad de Lagarias (1985), que Rozier enuncia así: «Q(x)
es racional si y sólo si x es racional». Implica que no hay órbitas
divergentes, así que contiene entero el muro B.

Alegoría: la ley de 1995 dice que nadie puede vivir en un pasillo de menos
de 1/3 de ancho. El inquilino de Mahler vive en uno de 1/2; la ley no lo
desaloja, pero al menos habla de él. Del cohete no dice nada, porque el
cohete no vive en ningún pasillo.

## Plan corto, elegido el 07-10

1. **Leer los originales con tres preguntas.** Hecho.
   - ¿Mahler dice «si y sólo si» o sólo «sólo si»? Sólo «sólo si».
   - ¿El artículo de 1995 tiene algún ingrediente que funcione sin pasillo?
     No, confirmado con el original: la única pieza que no pide encierro le
     sale gratis al cohete y no contradice nada.
   - ¿Ya está publicado lo de las dos reglas? Sí: Mahler (1968), Bernstein
     (1994), López y Stoll (2009) y Rozier (2019).
2. **Si no aparece nada**, escribir en esta nota las dos reglas, el
   obstáculo y la corrección, dar de alta la entrada del registro, cerrar y
   actualizar el ESTADO. Hecho el 07-10 por la noche; la entrada es
   `mahler_primo_cohete`.
3. **Si apareciera un ingrediente sin pasillo**, trasladarlo al cohete y
   someterlo a las tres pruebas de fuego: el −1 (`ξ = 0`), 5n+1 (donde todo
   indica que hay cohetes, como el 7) y 3n−1 (los circuitos de los
   negativos). No hizo falta.

Presupuesto: una sesión. El plan largo anterior (el diccionario en Lean y
el traslado de una ventana) queda archivado: sin un ingrediente sin pasillo
no hay ventana que trasladar.

Expectativa: salir con un «por aquí no» bien escrito. Se cumplió. Contra
el cohete sólo queda el lado 2-ádico, que es la conjetura de periodicidad:
atacar el problema de frente. Antes de abrir eso conviene parar y hacer
[balance de la casa](../casa20261004/LEEME.md#plan-del-07-10-balance-de-la-casa).

## Riesgos previstos y lo que pasó

- El problema de Mahler sigue abierto: como mucho saldría un rasgo parcial.
- Las condiciones no calzan. **Se confirmó, y es el obstáculo:** la de
  Mahler encierra una serie en un pasillo; la del cohete no encierra nada.
- Los cohetes lentos y los planeadores (`ξ = ∞`) quedan fuera.
- El puente podría estar ya publicado. **Se cumplió** en la parte de las dos
  reglas.

## Evidencia

**Integración del 10-10:** cotejadas las huellas de los dos scripts con
sus salidas conservadas. Se repitió el cotejo de fantasmas con 330 pasos
y el de Mahler con `--largo 16 --pasos 330`: coinciden con la evidencia
previa en ese alcance. Se conserva el conteo hasta L = 28 sin repetirlo.
El control del registro pasó con 298 afirmaciones, 63 nodos y 96
dependencias. Este cierre integra trabajo pendiente; no añade una
prueba universal ni una nueva formalización Lean.

[cotejar_fantasmas.py](cotejar_fantasmas.py) comprueba con `Fraction`,
sin coma flotante:

- la identidad `T^k(x) = P_k·R_k` y la suma afín;
- que R nunca disminuye ni baja de n en las semillas positivas;
- la cola finita exacta y su mínimo 1/3 en los pasos impares;
- las tres fórmulas cerradas de los fantasmas.

[Salida](cotejo_fantasmas.json): 12 semillas (3, 7, 27, 97, 871, `2^20−1`,
`2^64−1`, −1, −5, −7, −10 y −17) con 330 pasos, es decir, 3972 identidades
y 3972 colas, y 473 valores de fórmulas de fantasmas. Son identidades
algebraicas en tramos finitos: no prueban que exista ni que no exista un
cohete.

```powershell
python -B -X utf8 depuracion/mahler20261007/cotejar_fantasmas.py --pasos 330 --salida depuracion/mahler20261007/cotejo_fantasmas.json
```

[cotejar_mahler.py](cotejar_mahler.py) comprueba con `Fraction` lo leído:

- la tabla de Mahler para el 13 (p. 317) y los dos cortes, en `g_10` y en
  `g_21`;
- recorriendo los `2^L` restos para `L ≤ 16`: que cada palabra de paridades
  sale de un solo resto, que la prueba fina implica la del resto 3 y que el
  recuento directo coincide con la búsqueda;
- el conteo por ventanas hasta L = 28;
- la fórmula de Bernstein, `x + σ^(K) = 2^K·T^K(x)/3^{S_K}`, en 12 semillas
  (1, 3, 7, 27, 97, 871, `2^20−1`, −1, −5, −7, −10 y −17) con 330 pasos: 3972
  identidades;
- en los fantasmas, la suma cerrada `|x|·(1 − r^m)` con r pequeña en las dos
  reglas, y en el 1 la suma `(4/3)^m − 1`: 639 valores.

[Salida](cotejo_mahler.json). Son cuentas exactas en ventanas finitas.

```powershell
python -B -X utf8 depuracion/mahler20261007/cotejar_mahler.py --largo 28 --pasos 330 --salida depuracion/mahler20261007/cotejo_mahler.json
```

## Fuentes

Leídas el 07-10 por la noche; las copias están en `lecturas/`, fuera de Git:

- K. Mahler, «An unsolved problem on the powers of 3/2», J. Austral. Math.
  Soc. 8 (1968) 313–321
  ([PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6416420BFE33A5DDC3DAB6EA358C2B0B/S1446788700005371a.pdf/an-unsolved-problem-on-the-powers-of-32.pdf)).
  Leído entero.
- D. J. Bernstein, «A non-iterative 2-adic statement of the 3N+1
  conjecture», Proc. Amer. Math. Soc. 121 (1994) 405–408
  ([PDF del autor](https://cr.yp.to/papers/231.pdf)). Leídas las pp. 1–2.
- O. Rozier, «Parity sequences of the 3x+1 map on the 2-adic integers and
  Euclidean embedding», Integers 19 (2019) A8
  ([arXiv 1805.00133](https://arxiv.org/abs/1805.00133)). Leído el §3.2.
- J. López y P. Stoll, «The 3x+1 conjugacy map over a Sturmian word»,
  Integers 9 (2009) A13 ([PDF](https://math.colgate.edu/~integers/j13/j13.pdf)).
  Leídos el resumen y el §5, con el texto extraído defectuoso.
- Q. Lu y W. Zheng, «Fractional parts of powers of negative rationals»
  ([arXiv 2603.16794](https://arxiv.org/abs/2603.16794)). Leídos la
  introducción y el §2.
- L. Flatto, J. C. Lagarias y A. D. Pollington, «On the range of
  fractional parts {ξ(p/q)^n}», Acta Arith. 70 (1995) 125–147
  ([IMPAN](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/70/2/108521/on-the-range-of-fractional-parts-p-q)).
  Leído entero. La descarga automática choca con un filtro antirrobots; la
  copia la trajo el usuario (`lecturas/aa7023.pdf`).

Consultadas antes, en la búsqueda web del 07-10:

- J. C. Lagarias, «The 3x+1 problem: an annotated bibliography
  (1963–1999)» ([arXiv math/0309224](https://arxiv.org/pdf/math/0309224)),
  entradas 22, 62, 117 y 128. La 117 dice «si y sólo si»; el original, no.
  La 128 lo cita bien.
- J. C. Lagarias, panorama en CECM
  ([nodo 14](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node14.html)):
  la relación con el 3x+1, descrita como indirecta.
- [Problema 3/2 de Mahler](https://en.wikipedia.org/wiki/Mahler%27s_3/2_problem)
  (Wikipedia): resumen y estado.
