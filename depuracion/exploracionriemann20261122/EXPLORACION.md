# Exploración de la prueba de Riemann de Alpöge: patrones para Collatz

22-11-2026. Exploración pedida por el usuario: comparar nuestro trabajo con la
prueba de Riemann anunciada el 20-11-2026, buscando formas de ver y caminos
nuevos. **Decisión:** no se adopta ningún lema ni premisa. La lectura sugiere
un modelo de juguete concreto y una forma de organizar el obstáculo de
integridad. Ninguno de los tres criterios de reapertura del
[balance](../balance20261025/BALANCE.md#condiciones-para-reabrir-la-búsqueda)
queda satisfecho.

## 1. Material y alcance

- [Nota «Remark» de Alpöge](https://alpo.ge/remark.pdf), cuatro páginas,
  leída entera. Es impresionista. El autor advierte que parte de la línea
  temporal parafrasea un resumen de Claude «que podría no tener sentido».
- [Declaración conjunta Lean/Mathlib](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)
  del 21-11 y la [página de verificación de Sutherland](https://math.mit.edu/~drew/grh/),
  consultadas mediante resúmenes. Certifican que el teorema demostrado es
  `RiemannHypothesis` de Mathlib, con sólo los axiomas estándar. La biblioteca
  tiene unos 17 millones de líneas en 175 187 módulos. Según los resúmenes,
  los cinco teoremas verificados cubren RH y GRH para L de Dirichlet.
- [Quanta sobre la quasi-RH de OpenAI](https://www.quantamagazine.org/ai-proved-the-quasi-riemann-hypothesis-what-happens-now-20261019/)
  y [Al Jazeera](https://www.aljazeera.com/news/2026/11/21/riemann-hypothesis-has-the-worlds-most-famous-maths-problem-been-cracked).
- No se descargó ni leyó el archivo Lean (14 partes, unos 61 GB de exportación).
  Ningún matemático ha explicado todavía el argumento. Buzzard: «no sabemos
  por qué el teorema es cierto». Todo lo que sigue es **analogía heurística**,
  no transferencia demostrada.

## 2. Qué mecanismo describe la nota

1. **Esquema de Stepanov.** Sobre cuerpos de funciones, Riemann se prueba con
   un objeto auxiliar que se anula con **multiplicidad** alta en muchos puntos.
   El grado acota por arriba y la multiplicidad por abajo; la incompatibilidad
   limita el conteo. Es una prueba puntual, no un promedio.
2. **El ingrediente que falta sobre Z.** «La multiplicidad es difícil de
   encontrar sobre los enteros; correspondería a derivar números enteros.»
3. **El sustituto.** Una cadena de levantamientos theta
   `U(X0) -> U(X1) -> ... -> U(Xm)`. Cada eslabón **gana una unidad de
   multiplicidad**. La multiplicidad se mide como divisibilidad: el paso 2 de
   la línea temporal da `p^(a/p + a/p^3 + ... - O(log a))`, una valoración de
   tipo Legendre. La longitud de la cadena se toma `m ~ sqrt(X)` para una suma
   de von Mangoldt de longitud X; según el autor, la propuso Claude.
4. **Coste por eslabón.** El paso 14 calcula el coste exacto de cada
   levantamiento. A priori el método se detiene en 2/3, y para pasar de ahí
   necesita «división». El paso 15 pega una estructura entera a través de una
   familia de caracteres de Hecke (un «mcd», promedio extra).
5. **Signos en vez de cancelación.** Una prueba «sólo de signos» de
   Weil/Deligne: `qN = M^k + R`. El lado izquierdo tiene signo definido y R se
   controla iterando Parseval k veces; signos opuestos impiden cancelar.
   Positividad `W(1_S) >= 0` mediante un determinante, «Stepanov con
   multiplicidad uno», y luego *bootstrap*.
6. **Torre.** Una torre de Iwasawa «por analogía con el palomar en
   `F_{q^n}/F_q`», con nivel elegido mediante Behrend.
7. **Método de trabajo.** Primero un modelo de juguete donde funcionaban dos
   ideas distintas. Luego la situación análoga exacta. La pieza decisiva llegó
   al final (15-11), con el marco ya montado. Lean fue el único árbitro, y el
   autor espera simplificaciones.

La quasi-RH de OpenAI añade dos lecciones según Quanta. El éxito dependió de
**elegir la familia correcta** en la que encajar zeta (formas metaplécticas).
Además, la prueba combina herramientas conocidas: el modelo supuso que bastaban
y acertó.

## 3. Correspondencia con nuestro obstáculo

Dominio: enteros positivos; mapa atajo T; `P_k = 3^S_k / 2^k` como en el
balance. Sin ley aleatoria.

| Riemann (nota) | Collatz (repositorio) | Estado y límite |
| --- | --- | --- |
| Densidad de ceros en la recta: casi todos, no todos | Gao/Tao: densidad 1; Wu 1 abierto; MuroB necesita cada semilla | Mismo hueco de cuantificadores. Stepanov lo salta con una prueba puntual, no con un promedio mejor. |
| Multiplicidad (cota inferior aritmética) contra grado (cota superior) | Integridad 2-ádica del cilindro contra cotas de tamaño (ventanas, `P_k`) | El testigo 23 de [Ventanas simultáneas](../perdices20261007/congruencias_codex20261016/VENTANAS_SIMULTANEAS.md) muestra que el tamaño solo pierde la integridad. Falta un objeto que obligue a usar ambas a la vez. |
| La multiplicidad sobre Z se vuelve divisibilidad | Cada paso de paridad fija un bit más de `n mod 2^k` | Analogía natural: cada paso es «una unidad de multiplicidad». No existe aún el objeto entero que acumule esas unidades. |
| Determinante de interpolación | LMN/Laurent ya entra en los circuitos ([Ocelotas](../cst20260930/revision_rozier_20261016/REVISION.md)); la familia 017 de [la exploración anterior](../exploracionmath20261016/EXPLORACION.md) sugirió enlazar varias recargas | La novedad de Alpöge no es el determinante, sino fabricar la multiplicidad eslabón a eslabón. |
| Cadena de longitud `sqrt(X)` | Ventanas fijas de hasta cuatro rachas en [RUTA_CODEX](../perdices20261007/congruencias_codex20261016/RUTA_CODEX.md) | Sugiere dimensionar el objeto auxiliar con la longitud de la ventana. Es heurística, no una cota. |
| Coste por eslabón; 2/3 a priori; promedio en una familia | En Codex el coeficiente crece geométricamente | Misma forma de fallo. La nota primero calcula el coste exacto y luego promedia en una familia en la que los costes no se alinean. |
| Torre de Iwasawa y palomar | Torres `Z/2^k` y `Z/3^j` ([Wirsching](../wirsching20260930/LEEME.md)); CRT en ventanas | CRT ya recupera el cilindro. Falta acotar uniformemente el menor representante, que el balance señala como punto concreto. |
| Positividad `W >= 0` y argumentos sólo de signos | Rangos de terminación; [Retornos](../perdices20261025/RETORNOS_ARITMETICOS.md) y [Pesos binarios](../perdices20261026/PESOS_BINARIOS.md) descartan rangos monótonos de observaciones fijas | Si existe un certificado, no será un rango local monótono. Podría ser una positividad global, como la familia de formas de Weil. Especulativo. |
| Modelo de juguete en cuerpo de funciones | **F2[x]**: Collatz sin acarreos (§4) | Disponible y demostrado. Es el hallazgo más accionable de esta lectura. |

## 4. El modelo de juguete: Collatz sin acarreos en F2[x]

Hicks, Mullen, Yucas y Zavislak (Amer. Math. Monthly 115, 2008) estudian
`f -> f/x` si x divide a f, y `f -> (x+1)f + 1` si no. Codificando f en
binario, multiplicar por x+1 es `n XOR 2n`: **es 3n+1 sin acarreos**. Según
las fuentes secundarias consultadas, toda órbita llega a 1 (también Snapp y
Tracy). [Nichols (arXiv:1610.02545)](https://arxiv.org/pdf/1610.02545) muestra
que con `x^2+x+1` (7n sin acarreos) la conjetura análoga falla. La cota de
pasos mejoró a `O(grado^1.5)` en [arXiv:2401.03210](https://ar5iv.labs.arxiv.org/html/2401.03210).
No se leyó el texto del Monthly; hay que cotejar los enunciados antes de citarlos.

`juguete_f2x.py` reproduce el cuadro en un barrido finito, sin prueba:

```
python3 -B depuracion/exploracionriemann20261122/juguete_f2x.py --grado-maximo 18
```

- `m = x+1`: los 2^19-1 polinomios no nulos de grado <= 18 llegan a 1, sin
  ciclos ni crecimiento. El máximo de pasos es 100 en grado 18, cerca de 5.6·grado.
  Es medición, por debajo de la cota publicada.
- `m = x^2+x+1`, grado <= 12: 343 ciclos distintos sin 1 (el menor desde
  `x^2+1`). 523 de 8191 semillas superan el grado 200, lo que no prueba que
  diverjan.
- Órbita entera de 27: 41 pasos impares, con 248 bits corregidos por acarreo
  respecto de la versión sin acarreos.

**Lectura.** El juguete tiene la misma dicotomía que 3n+1 frente a 5n+1/7n+1, y
en él la conjetura es un teorema. Lo único que separa el juguete de Collatz son
los acarreos. Por tanto, «los acarreos» desempeña el papel que «la
multiplicidad sobre Z» tiene en la nota de Alpöge: es el nombre preciso del
ingrediente que no se transporta. Las notas actuales tratan los acarreos como
ruido ([Casa](../casa20261004/RUTA_20261010.md), [Pesos binarios](../perdices20261026/PESOS_BINARIOS.md)).
El juguete permite estudiarlos como el objeto central.

## 5. Propuestas, en el formato que exige el balance

**A. Prueba del juguete y mapa de su transporte (barato).** Formalizar en Lean
el teorema de F2[x] con multiplicador x+1 y marcar cada paso que use la
ausencia de acarreos. *Implicación:* ninguna directa hacia MuroB. Da el
catálogo exacto de lo que habría que sustituir. *Hipótesis verificable:* el
invariante que hace decrecer el grado y el punto en que falla con
`x^2+x+1`. *Descarte:* si la prueba depende de la ausencia de acarreos en
cada paso sin un invariante aislable, el juguete sólo sirve como control.

**B. Determinante de Stepanov sobre reinicios de fuga.** Supongamos una órbita
positiva inyectiva que no cumple MuroB. [Colisiones](../perdices20261007/COLISIONES.md)
da reinicios con `P >= 1`; cada bloque cumple `2^L x' = 3^S x + c`, con c
determinado por la palabra. Habría que buscar una matriz entera construida
con m de esos bloques cuyo determinante Δ cumpla tres cosas: (i) Δ ≠ 0;
(ii) `v_2(Δ)` crece con cada eslabón; (iii) `|Δ|` queda acotado por la
condición expansiva. Si `2^v_2(Δ) > |Δ|`, hay contradicción. *Implicación:*
excluiría la fuga y daría MuroB en esa semilla. Los circuitos siguen aparte.
*Descarte acotado:* probar las matrices candidatas en las familias `2^L-1` y
en la palabra W del testigo 6416623. Se descarta la candidata si Δ se anula
idénticamente o si `2^v_2(Δ) <= |Δ|` con margen que crece con m. Hoy falta
el objeto; esto es una obligación, no un método.

**C. Coste exacto por eslabón en Codex.** Antes de buscar otro reloj, calcular
qué aporta y qué cuesta cada racha añadida, como en el paso 14 de la nota.
Luego, buscar una familia sobre la que promediar en la que esos costes no se
alineen. *Advertencia:* sobre los múltiplos de d, la familia 3n+d es conjugada de
3n+1 (`x -> d·x`). Promediar en d no dice nada nuevo sobre las órbitas de
3n+1; en las otras clases añade ciclos ajenos. La familia tiene que ser de
otra clase, por ejemplo niveles de la torre 3-ádica.

## 6. Controles y advertencias

- **Filtro 3 frente a 5.** Por Conway, los Collatz generalizados son
  indecidibles, así que un método válido tiene que usar la aritmética concreta
  de 2 y 3. Toda propuesta debe fallar para `x^2+x+1` en F2[x] y para 5n+1 en
  Z. Si «demuestra» también esos casos, es errónea.
- La nota no aporta nada nuevo para los circuitos más allá de Baker/LMN, que ya
  se usan.
- La coincidencia de que la nota use el grupo triangular (2,3,6) y la curva CM
  `C/Z[ω]`, en la que 2 es inerte, no se toma en serio sin un mecanismo.
- Lean certifica el enunciado de Alpöge, no una interpretación transferible a
  Collatz. Nada aquí se registra en `registro.json` ni se anuncia.

## 7. Resultado de la propuesta A (22-11)

[JugueteF2x.lean](JugueteF2x.lean) compila con Lean 4.32.2 y la Mathlib
fijada en `gao20260920/formal`, sin `sorry` y sólo con los axiomas estándar
([evidencia](evidencia_lean_juguete.txt)). Mapa: el de §4 sin atajo, sobre
`(ZMod 2)[X]`.

| Teorema Lean | Enunciado | ¿Se transporta a Z? |
| --- | --- | --- |
| `llega_a_uno` | Todo `f ≠ 0` llega a 1 en a lo sumo `d^2+2d` pasos, con `d = natDegree f` (la cota publicada) | Es la conjetura en el juguete. |
| `dos_pasos` (L1) | `T(T(X·h+1)) = (X+1)·h+1`: una racha impar dura lo que el orden de X en `f+1` | **Sí, exactamente.** `racha_entera`: `Tz^k(2^k·a-1)+1 = 3^k·a`. |
| `natDegree_dos_pasos` (L2) | El par de pasos impar conserva el grado; un paso par lo baja | **No.** Es el único uso de la ausencia de acarreos. |
| `natDegree_dos_pasos_siete` | Con `X^2+X+1`, el par de pasos impar sube el grado en uno | Control: la prueba falla donde debe. |

**Lectura.** El juguete se demuestra con L1, que vale en Z, y L2, que sólo
vale sin acarreos. Al acabar una racha de longitud k, en F2[x] se tiene
`(X+1)^k·a`, del mismo grado que `X^k·a`; en Z se tiene `3^k·a` frente a
`2^k·a`. El análogo de `P_k = 3^S/2^k` en el juguete es `S·1 - k·1 <= 0`
en grado, así que **MuroB es trivial en F2[x]**. Con `X^2+X+1` el análogo
es `2S - k`, que puede ser positivo.

Conclusión: a diferencia del juguete de Alpöge, este no contiene una idea
nueva que transportar. Confirma con prueba formal lo que el balance ya
localizó: toda la dificultad está en el tamaño arquimediano (`log2 3 > 1`,
los acarreos). El control de rachas no es el obstáculo. Quedan útiles dos
cosas: el filtro `X^2+X+1` formalizado y L1 entero en Lean. Ningún
criterio de reapertura queda satisfecho. Un juguete que sirviera para
MuroB debería tener multiplicador de tamaño estrictamente entre 1 y 2 en
la valoración que controla el tamaño, como `log2 3`. En F2[x] con el grado
eso no existe, porque los grados son enteros.

## 8. Resultado de la propuesta B (22-11)

[stepanov_presupuesto.py](stepanov_presupuesto.py), [resultados](presupuesto_stepanov.json).
Mapa: atajo T. Una palabra de paridades es **expansiva** si todos sus
prefijos cumplen `P_k >= 1`. Conteo exacto y medición finita; nada es
prueba universal.

**Reformulación.** MuroB falla en n si y sólo si n pertenece a
`K = {x en Z_2 : P_k(x) >= 1 para todo k}`. En el nivel L, K es la unión
de los `e(L)` cilindros expansivos. El conteo exacto hasta L=2000 da una
pendiente `log2 e(L)/L` de 0,9485 entre L=1000 y L=2000. La tasa de
Chernoff del paseo `±log(3/2), log(1/2)` predice β = 0,94996 (θ = 0,488,
ρ = 0,96591). MuroB equivale a que **ningún entero >= 2 esté en un
Cantor 2-ádico de dimensión de caja ≈ 0,95**. Que esa dimensión sea β es la
tasa estándar de grandes desviaciones, y aquí sólo se coteja numéricamente.
En el juguete F2[x] el análogo de K se reduce a la palabra de unos, con β = 0
(§7).

**Candidatos descartados con el criterio de §5.**

1. *Determinantes lineales de datos de bloque.* Los vectores
   `(2^t x_t, 3^S_t, ρ_t)` son ortogonales a `(1, -x_0, -1)`, así que todo
   3×3 se anula idénticamente. Los menores 2×2 valen
   `2^t_i 3^S_i ρ_ventana`, que es la identidad de la ventana (20 pares
   cotejados exactamente en 6416623 y 2^40-1). Se descartan: valoración y
   tamaño son la misma identidad.
2. *Funciones auxiliares que sólo usan la pertenencia a un cilindro.* El
   cálculo de Siegel requiere unas `e(L)` congruencias módulo `2^M`, con
   `M <= L`. Para que una función de grado D y altura H se anule en los
   puntos de tamaño menor que N hace falta `D·log2 N < M`, pero el lema de
   Siegel exige `D·log2 H >~ M·e(L)`. El déficit es un factor de orden
   `2^(0,95L)`, de la misma naturaleza que el «coste por eslabón» de Alpöge.
   Stepanov lo cubre con una relación algebraica común a todos los puntos
   (Frobenius, `x^q = x`). En Collatz, las únicas relaciones comunes son las
   afines por palabra del punto 1, que son tautológicas. Se descarta mientras
   no haya un análogo de Frobenius.

**Medición de representantes.** La densidad exacta de `τ(n) >= t`, el
primer k con `P_k < 1`, es `e(t)/2^t`. Si los enteros se comportaran como
residuos al azar, el menor n con `τ >= t` aparecería hacia
`log2 n ≈ t - log2 e(t)`. Los récords hasta 2·10^6 siguen esa predicción
con 2 o 3 bits de diferencia (τ = 81..224; por ejemplo 1126015 tiene
τ = 224, con 20,10 bits observados frente a 19,73 predichos). El 0,05 de la
predicción ingenua `1-β` omitía el factor polinómico. No se ve ninguna
anomalía aritmética de los representantes pequeños que un determinante
pueda aprovechar.

**Conclusión.** B queda descartada en sus formas naturales. Lo que
sobrevive no es un determinante sino un enunciado diofántico: los enteros
positivos evitan un Cantor 2-ádico de dimensión ≈ 0,95 definido por la
aritmética de 2 y 3. Es la familia de problemas «enteros en conjuntos
fractales», donde la nota de Alpöge y Tao emplean ideas de Fourier. Es una
pista bibliográfica, no un método comprobado. Ningún criterio de reapertura
queda satisfecho.
