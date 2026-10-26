# Perdices: una serie A/B puede tener límite real racional

26-10-2026. Continúa la precaución de [Cola, §6](../perdices20261007/COLA.md#6-una-precaución-bibliográfica-concreta).
Se conserva Perdices, sin reivindicar prioridad. Es una construcción propia
para comprobar un paso bibliográfico, no una refutación de Collatz.

**Resultado:** todo número real de [-4,-1] es el límite real de la serie
inversa de alguna palabra infinita de bloques A=1 y B=110. Hay palabras
aperiódicas de esta clase con límite real -3/2 y con límite real -2.
En el segundo caso, el límite 2-ádico de las mismas sumas no puede ser -2:
sus residuos son impares. No se decide si ese límite 2-ádico es racional.

Esto refuta dos inferencias auxiliares sobre límites reales que aparecen
en la lectura de López–Stoll (2021). **No refuta su teorema principal sobre
la densidad de una órbita racional 2-ádica.** Ese teorema sigue sin ser una
premisa admisible para este laboratorio mientras falte reparar el enlace.

## 1. Objetos, índices y ley

El mapa entero que interesa es T(n)=n/2 para n par y (3n+1)/2 para n impar,
n positivo. Aquí se estudian además sus ramas afines **prescritas**, sin
comprobar paridad, sobre reales negativos:

```text
A(x)=(3x+1)/2,             B(x)=(9x+5)/8.
```

B compone los bits 110. No son órbitas enteras salvo que se demuestre la
compatibilidad de las paridades. k cuenta bloques, L_k pasos T prescritos,
S_k bits iguales a 1 y P_k=3^S_k/2^L_k. No hay muestreo ni ley aleatoria.

Para una palabra infinita v de bits, con unos en las posiciones d_i,
contadas desde cero, las sumas inversas son

```text
H_L(v) = -sum_(d_i<L) 2^d_i/3^(i+1).
```

Estas sumas racionales tienen denominador impar y determinan un límite
2-ádico Φ_2(v): después del bit L los términos nuevos son divisibles por
2^L. El límite real Φ_R(v), cuando existe, es otro objeto. La construcción
que sigue prueba su existencia; no los identifica.

## 2. Selector de bloques e intervalo invariante

Fijar q_0=q en [1,4], x_0=-q. Elegir sucesivamente

```text
si q_k<=3: elegir A y q_(k+1)=(3q_k-1)/2;
si q_k>3:  elegir B y q_(k+1)=(9q_k-5)/8.
```

La primera rama lleva [1,3] a [1,4]. La segunda lleva (3,4] a
(11/4,31/8]. Por inducción, 1<=q_k<=4 para todo k. Esta regla define
una sola palabra infinita para cada q; no se cambian los arranques al
prolongar la palabra. Dentro de B, los dos valores intermedios de q
son (3q-1)/2 y (9q-5)/4. Por tanto todos los estados por bits, incluidas
las fronteras, quedan en [1,31/4].

Cada bloque tiene pendiente al menos 9/8. Por composición afín,

```text
x_k=P_k[-q-H_(L_k)],
H_(L_k)=-q+q_k/P_k,
0 < H_(L_k)+q <= 4(8/9)^k.                         (1)
```

La última cota tiende a cero. Las sumas de bits son no crecientes y
quedan entre las de dos fronteras consecutivas. Por tanto la serie
completa, y no sólo la subsecuencia de bloques, converge a -q.
Además 3S_L>=2L para todos los prefijos: cada bloque completo lo cumple,
y los fragmentos interiores posibles son 1 y 11. Así
liminf S_L/L>=2/3>log(2)/log(3), pues 9>8.

## 3. Dos límites racionales, con palabras aperiódicas

Para q=3/2, el comienzo por fronteras es

```text
-3/2 -> -7/4 -> -17/8 -> -43/16 -> -113/32 -> -857/256,
             A       A        A         A           B.
```

La palabra empieza `AAAABBBABBBBB...` y (1) da Φ_R(v)=-3/2.
En cada paso T prescrito, un numerador impar sobre 2^d, d>=1, permanece
impar y el denominador reducido gana un factor 2. En fronteras A/B,
los numeradores, escritos con q positivo, son

```text
3a-2^d       sobre 2^(d+1),
9a-5*2^d     sobre 2^(d+3).
```

Son impares. Por ello el denominador en el paso L es exactamente
2^(L+1). La trayectoria prescrita es acotada en las fronteras y tiene
infinitos valores distintos, todos racionales.

Para q=2, la palabra empieza `AABBABBBB...`, Φ_R(v)=-2 y la primera
aplicación prescrita es -2 -> -5/2. Desde ahí se aplica el mismo argumento:
el denominador del paso L>=1 es 2^L. El T literal daría -2 -> -1.
Confundir ambos recorridos elimina precisamente la condición de paridad.
Como el primer bit prescrito es 1, Φ_2(v)=1 mod 2; no es el entero -2.

**Aperiodicidad de ambas palabras.** Si una cola fuese periódica con
periodo de d bits y s unos, tendría 3s>=2d y D=3^s>N=2^d.
La composición del periodo es (Dx+E)/N. Una trayectoria acotada bajo
esa aplicación expansiva debe estar en su punto fijo -E/(D-N).
Su denominador reducido es impar. Pero cualquier cola de los ejemplos,
después del primer paso, comienza en un racional de denominador par.
Contradicción. No se está infiriendo aperiodicidad de un prefijo medido.

## 4. Qué impide incorporar el resultado externo

Se consultaron directamente el [preprint v1](https://arxiv.org/abs/2101.12747v1)
y su [texto, §§2 y 6](https://arxiv.org/html/2101.12747v1).
El teorema 1 afirma que una órbita racional 2-ádica no periódica tiene
densidad inferior de unos igual a log(2)/log(3). Su enunciado, si tuviese
una prueba válida, excluiría la persistencia positiva A/B: las fronteras
crecen estrictamente, mientras la densidad inferior es al menos 2/3.
Eso sería una aplicación a esta clase, todavía insuficiente para MuroB
general, los circuitos o el reloj uniforme L<=C*ell(n)+D.

La comprobación presente precisa el problema del argumento:

- Después de (15)–(16), §2 excluye límites reales racionales de
  denominador par. El ejemplo q=3/2, formado por los propios bits 1/110,
  contradice esa exclusión. La convergencia de los residuos no permite
  trasladar al límite real la integridad 2-ádica de las sumas parciales.
- Al final de §6 se usa la acumulación de una trayectoria real para
  concluir que su arranque no pertenece a Q_odd. El ejemplo q=2 tiene
  arranque -2 en Q_odd y fronteras acotadas, distintas. Es una
  pseudotrayectoria: los denominadores no se conservan porque las ramas
  no obedecen la paridad racional. Para invocar la discreción de una
  órbita racional hace falta demostrar previamente esa compatibilidad.

La identidad de residuos de (15) sí es válida como límite de sumas
parciales. Lo que falla es interpretarla como preservación de la
racionalidad entre completaciones. Los ejemplos no dan una órbita
racional 2-ádica divergente y no contradicen por sí solos el teorema 1.
El puente que su prueba necesita no queda reparado.

## 5. Alcance formal, contraste y decisión

[Lean](PerdicesLimitesReales.lean) prueba el intervalo para todo arranque
real q en [1,4], la identidad de las sumas por bloques, la cota geométrica
y el límite real, incluidos -3/2 y -2. También prueba la conservación de
numeradores impares y la incompatibilidad algebraica de un punto fijo
con denominador diádico no trivial. La identificación con la serie de
bits y la exclusión de periodicidad eventual están escritas arriba;
el módulo no formaliza Φ_2 ni su racionalidad.

[Compilación y axiomas](evidencia_lean.json): 11 consultas con Lean 4.32.2,
únicamente axiomas estándar, sin sorryAx. [Salida íntegra](evidencia_lean.txt).
Se cotejan fuentes y objetos de los imports directos de Mathlib fijado;
no se realiza una auditoría transitiva completa. Revisión humana pendiente.

[Cotejo independiente](cotejar_limites.py), con enteros y Fraction:
28 recorridos, 1702 pasos prescritos, siete arranques y bordes q=1,3,4.
Reconstruye las sumas bit a bit y los cilindros mediante composición
afín; cada representante obtenido recorre literalmente T con esos bits.
Comprueba los denominadores y la incompatibilidad inicial de -2.
Las semillas enteras dependen del horizonte: no se construye una órbita
entera infinita. No se repite ningún censo histórico.
El [resultado exacto](cotejo_limites.json) conserva los recorridos.

```powershell
python -B -X utf8 depuracion/perdices20261026/cotejar_limites.py --bloques 96 --salida depuracion/perdices20261026/cotejo_limites.json
python -B -X utf8 depuracion/perdices20261026/comprobar_lean.py --lean C:/Users/Home/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean.exe --salida depuracion/perdices20261026/evidencia_lean.json
```

[Altas versionadas](alta_registro.json) integradas mediante el generador:
367 afirmaciones tras la ampliación digital, con
[conservación de las 365 previas](evidencia_registro.json).
[Verificación de sesión](evidencia_sesion.json), incluidos enlaces y fuentes:

```powershell
python -B -X utf8 depuracion/perdices20261026/verificar_sesion.py --base ffba1c46bd85eb07ad042bc86b88238925827d7a --salida depuracion/perdices20261026/evidencia_sesion.json
```

**Decisión:** esta fuente no satisface la tercera
[condición de reapertura](../balance20261025/BALANCE.md#condiciones-para-reabrir-la-búsqueda).
Tampoco se obtuvo aún control aritmético individual ni transferencia de
mezcla excepcional. Queda agotado el uso de *este transporte automático
de racionalidad*. No se declara agotada toda Perdices. El paso pendiente
es una estimación que conserve la integridad binaria de una misma semilla
con precisión creciente; la convergencia real por sí sola no la aporta.
El [examen posterior](PRECISION_CRECENTE.md) muestra que el levantamiento
exacto conserva la obligación del reloj. La [auditoría de ruta](AUDITORIA_RUTA.md)
identifica el siguiente frente concreto que sigue sin agotar.
