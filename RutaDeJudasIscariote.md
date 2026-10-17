# Ruta de Judas Iscariote

16-10-2026. Rama de Claude (Opus 5.5). El nombre lo puso el usuario, «por la
traición entre IA»: esta rama discrepa del siguiente paso de la de Astra.

**Ruta paralela, no sustituta.** La [ruta de Astra](depuracion/coherencia20260913/RUTA_339_20261012.md),
su [exploración](depuracion/exploracionmath20261016/EXPLORACION.md) y la
[siguiente obligación de Tres cambios](depuracion/perdices20261007/TRES_CAMBIOS.md#7-certificación-y-siguiente-obligación)
siguen vigentes en su rama. Esta nota no modifica ningún documento anterior;
sólo los cita. Cada rama avanza por separado.

**Tesis.** Comparto la meta (D), el filtro de admisión y el piloto 1/110.
Discrepo del control acumulativo de congruencias como siguiente paso. Esas
congruencias muerden cuando una valuación es del orden de ell y las cotas de
tamaño quedan justas; las excursiones récord no pasan por ahí. Viven en un
régimen genérico: muchos cambios, recargas pequeñas y cotas holgadas. En ese
régimen el censo coincide con el modelo de restos uniformes al 0,05 %, y el
piloto es un caso particular de una conjetura publicada y abierta, la 4.12 de
Yolcu–Aaronson–Heule, con la forma de los números Z de Mahler. Mi
expectativa: no hay mecanismo conocido para ese régimen. Esta ruta lo
comprueba en una sesión y, si se confirma, deja de gastar tandas ahí.

## 1. Lo que comparto

- La meta (D) de [RUTA §3](depuracion/coherencia20260913/RUTA_339_20261012.md#3-la-fórmula-exacta-que-debe-cerrar-la-investigación),
  con la misma semilla y una K que no use la salida.
- El [filtro de admisión](depuracion/exploracionmath20261016/EXPLORACION.md#8-filtro-de-admisión-de-una-nueva-vía)
  y cerrar cada sesión con prueba, contraejemplo exacto u obligación precisa.
- El piloto 1/110 antes que H: bloques expansivos y potenciales explícitos.
- Los resultados de Perdices hasta tres cambios y su límite con cuatro. Esta
  rama no los toca ni los repite.

## 2. Calibración del piloto

Convenciones de [SALIDAS §1](depuracion/perdices20261007/SALIDAS.md#1-convenciones-y-resultados-finitos)
y [RUTA §4](depuracion/coherencia20260913/RUTA_339_20261012.md#4-dónde-pondría-el-esfuerzo-principal):
atajo T, clase AB de prefijos de `{1,110}^ω`, λ(n), bloques A y B, recargas
firmadas, (R) y `ell=ceil(log2(n+5))`.

### 2.1 Lectura en Siracusa

Prueba escrita. Sea n impar, `y_0=n, y_1, ...` su órbita impar y
`ν_i=v2(3y_i+1)`. Las paridades de T son `1 0^(ν_0-1) 1 0^(ν_1-1) ...`.
Son prefijo de AB mientras `ν_i<=2`, `ν_0=1` y no haya dos `ν=2` seguidos,
porque cada 0 debe ir precedido de 11. Como `ν=1` si `y=3 mod 4`, `ν=2` si
`y=1 mod 8` y `ν>=3` si `y=5 mod 8`:

> n impar sale de 1/110 exactamente cuando su órbita impar empieza en
> 1 mod 8, visita 5 mod 8 o visita 1 mod 8 dos veces seguidas.

Un n par sale en el paso 0. Cotejo: 200 000 semillas impares hasta 400 000,
sin discrepancias entre las dos lecturas de λ. Transiciones entre impares
consecutivos, por fuerza bruta: 1 va a {1,3,5,7} con ν=2; 3 va a {1,5} con
ν=1; 5 va a {1,3,5,7} con ν≥3; 7 va a {3,7} con ν=1.

### 2.2 Su lugar en Yolcu–Aaronson–Heule

Leído en el original, [§4.5](https://arxiv.org/html/2105.14697v3#S4.SS5).
Las conjeturas 4.11, 4.12 y 4.13 afirman que toda trayectoria no convergente
visita 1, 5 y 7 módulo 8, respectivamente; la 4.14, que visita 5 o 7. Las
cuatro siguen abiertas; de la 4.14 escriben «Even the following easier
statement remains unproved». Demuestran las variantes {1,5} y {1,7} y el
teorema 4.10: no se puede evitar 2, 3, 4 ni 6.

- Una órbita positiva que quedara en AB para siempre crecería en cada bloque
  y nunca visitaría 5 mod 8. Por tanto **la conjetura 4.12 implica la versión
  cualitativa del piloto**: el piloto es un caso particular de una conjetura
  publicada y abierta. La cota `λ(n)<=C·log2(n)` es más fuerte que esa versión.
- H, la clase sin 00 ni 111 de [SALIDAS §3](depuracion/perdices20261007/SALIDAS.md#3-enlace-con-el-problema-publicado),
  es la de la 4.14, que la 4.12 también implica.
- Con esas transiciones, las variantes demostradas sobre impares ({1,5},
  {1,7} y evitar 3) sólo admiten `A^ω`, que sólo realiza −1, u órbitas que
  contraen. Las abiertas admiten mezclas de
  entropía positiva con ciclos de residuos que expanden. En AB **todos** los
  ciclos expanden: 7 (×3/2) y 3→1 (×9/8).

### 2.3 La forma de Mahler, ya leída el 07-10

La [nota de Mahler](depuracion/mahler20261007/LEEME.md) leyó enteros Mahler
(1968) y Flatto–Lagarias–Pollington (1995), y concluyó que el ingrediente de
FLP [necesita un pasillo](depuracion/mahler20261007/LEEME.md#el-ingrediente-de-1995-necesita-un-pasillo)
en el que el cohete no vive. Aquí se añaden tres hechos sobre el piloto, que
sí es una clase restringida:

1. **El conteo de Mahler tiene aquí un análogo inmediato.** Prueba escrita:
   cada prefijo admitido es una concatenación completa de 1 y 110, con
   descomposición única, y la biyección de paridades da
   `#{1<=n<2^L : λ(n)>=L} = c_L`, con `c_L=c_(L-1)+c_(L-3)` (1, 1, 2, 3, 4,
   6, …) y `c_L ≍ r^L`, donde `r=1,46557` es la raíz de `x^3=x^2+1`. Fuerza
   bruta hasta L=18 sin fallos. Así `#{n<x : λ(n)>=log2 x} = O(x^0,5515)`,
   análogo del `x^0,7` de Mahler y del `x^0,585` de Flatto. Como allí, falta
   pasar de «pocos» a «ninguno».
2. **El piloto no da pasillo a FLP.** Para una órbita que quedara en AB para
   siempre, el diccionario de esa nota da `T^k(n)=ξ·P_k−t_k`, luego
   `{ξ·P_k}={t_k}`. Si t es la cola en la entrada de un bloque y t' la de la
   entrada siguiente, `t=1/3+2t'/3` para A y `t=5/9+8t'/9` para B. Las
   imágenes de [1,5] son [1,11/3] y [13/9,5], que lo cubren: el conjunto de
   colas posibles es exactamente [1,5], todo el círculo módulo 1. AB restringe
   paridades; no encierra partes fraccionarias. El paso 1 de FLP no tiene
   material, y el 2 tampoco tiene razón fija (P_k se multiplica por 3/2 o por
   1/2). Cotejo exacto: 126 palabras periódicas de hasta seis bloques; cada
   cola está en [1,5] y su opuesta es un ciclo racional de T con esas
   paridades. Los ciclos racionales de AB tienen sus entradas de bloque en
   [−5,−1].
3. **Lo demás de esa literatura no cambia el cuadro.** Bugeaud–Dubickas (2005)
   describen con palabras sturmianas los ξ irracionales cuyas partes
   `{ξ·b^n}`, con b entero, caben en un intervalo de largo 1/b: entropía cero,
   como en nuestra [Complejidad](depuracion/perdices20261007/COMPLEJIDAD.md).
   Dubickas–Mossinghoff (2009) prueban que un número Z para 3/2, si existe,
   supera 2^57: es el análogo de nuestro censo hasta 2^50.

## 3. Dos regímenes, medidos

### 3.1 Modelo de restos uniformes

Heurística declarada, no teorema. Ley: para L mayor que los bits de la
semilla, el resto de cada palabra admitida es uniforme módulo 2^L; los
bloques siguen la medida de máxima entropía, A con probabilidad 1/r y B con
1/r^3. Da `h=log2 r=0,55146` bits por paso, un récord de primer orden
`B/(1−h)=2,2295·B` (111,5 para B=50), 0,265 cambios por paso y un
crecimiento de 0,277 bits por paso. Con el conteo exacto, el número esperado
de semillas menores que 2^50 con λ≥L es `c_L·2^(50−L)`: 0,97 para L=110 y
0,52 para L=112. El máximo cae entre 106 y 119 con probabilidad 0,9, con
mediana 111.

La pieza 2 de la [contabilidad informacional](depuracion/exploracionmath20261016/EXPLORACION.md#5-segunda-transferencia-información-de-una-órbita-sin-azar-supuesto),
un coste positivo demostrable de persistir, vale aquí `1−h≈0,45` bits por
paso: exacta con la ley uniforme sobre restos, sin prueba para una órbita
fija. Es la misma pieza que falta en Mahler.

### 3.2 El censo coincide con el modelo

El [censo AB hasta 2^50](depuracion/perdices20261007/medicion_salida_ab.json)
visitó 719 397 383 nodos. Hasta L=50 son exactamente `Σc_L = 384 377 663`;
los otros 335 019 719 son prefijos de largo mayor que 50 con representante
menor que 2^50. El modelo predice 334 853 199,7: cociente **1,0005**. El
máximo observado, 112, cae dentro del intervalo previsto. Es un contraste
agregado, no una demostración, pero las dos cifras contrastables, nodos y
máximo, no separan la órbita real del azar en este régimen.

### 3.3 Récords: muchos cambios, recargas pequeñas, cotas ociosas

Medición finita sobre los 21 récords con λ≥40, de 2 203 815 a
338 203 040 342 655, con la concatenación real máxima de RUTA §4. En todos,
L=λ, (R) es exacta y se cumple la identidad por rachas de §3.5.

| | 21 récords | Modelo o testigo de cuatro cambios |
|---|---|---|
| Cambios por paso | 0,16 a 0,32; media 0,260 | 0,265 en el modelo |
| Mayor recarga η | 21, con ell=43; η/ell ≤ 0,49 | testigo: 998 a 2601, con ell=1000 |
| Mayor valuación usada | 23 | testigo: 5 en la entrada, luego de 1000 a 2603 |
| Holgura mínima del encaje | 13,7 bits; 31,4 o más si ell≥40 | testigo, con 2^ell: 0,17; 0,96; 1,51 y 47,4 bits |

La holgura es `log2(3^S·(n+5))−D−v` en cada entrada de bloque: lo que el
[encaje universal](depuracion/perdices20261007/TRES_CAMBIOS.md#1-dominio-y-herramienta-conservada)
todavía permitiría. El mayor récord, 338203040342655, tiene ell=49, L=λ=112,
27 cambios, v_in=7, v_fin=0, Ση=105, recarga máxima 15, valuación máxima 17
y holgura mínima 35,5 bits.

En el [testigo de cuatro cambios](depuracion/perdices20261007/TRES_CAMBIOS.md#5-barrera-explícita-con-cuatro-cambios),
tres de los cuatro encajes quedan justos y las valuaciones son del orden de
ell; por eso la [congruencia módulo 9](depuracion/perdices20261007/TRES_CAMBIOS.md#6-una-congruencia-impide-realizar-ese-testigo)
fija la parte impar y lo descarta. En los récords, cada frontera deja al
menos 13,7 bits sin usar: la parte impar admite más de 2^12 valores
compatibles con el tamaño y una congruencia aislada no la fija.

### 3.4 La escalera de cambios no alcanza a los récords

Enumeración exacta de todas las concatenaciones reales con a lo sumo m
cambios que cruzan L=110: 94 089 hojas con m≤3. Cada semilla mínima se cotejó
con su órbita literal, y la minimalidad, por fuerza bruta en 16 casos con
L=8, 12, 16 y 20.

| Cambios | Menor semilla con λ≥110 |
|---:|---|
| ≤0 | 2^110−1 |
| ≤1 | ≈2^105,13 |
| ≤2 | ≈2^96,63 |
| ≤3 | 44152383406100078085198053371 ≈ 2^95,16 |
| sin límite | 338203040342655 ≈ 2^48,27, con 27 cambios (censo) |

Con pocos cambios, durar 110 pasos exige semillas de al menos 95 bits; las
reales lo logran con 48 bits y unos 0,26 cambios por paso. Una prueba por
número de cambios necesita uniformidad en ese número, y
[Tres cambios](depuracion/perdices20261007/TRES_CAMBIOS.md) ya advierte que
un epsilon que tienda a cero con él no da (P). La serie 7/17, 1/13 y el
límite con cuatro cambios recuerda a los m-ciclos
([calibración contra Hercher](depuracion/cst20260930/CICLOS_CALIBRACION.md)):
cada paso cuesta más y nadie ha cerrado el caso general por ese camino.

### 3.5 Por qué el número de cambios es el parámetro duro

Con r rachas de constantes `c_i∈{1,5}`, la identidad de RUTA §3 se escribe

```text
2^L x_L − 3^S n = Σ_i c_i (3^(S−S_i) 2^(D_i) − 3^(S−S_(i+1)) 2^(D_(i+1))),
```

donde D_i y S_i son los pasos y los impares antes de la racha i. Son 2r
términos de la forma `±c·2^β·3^α`; el cotejo la comprueba en los 21 récords.
Con pocas rachas es terreno de Baker y de abc:
[Altura BAB](depuracion/perdices20261007/ALTURA_BAB.md) ya encontró que un
fallo en BAB exigiría calidad abc>18. Con rachas proporcionales a L, el
número de términos crece sin cota, y la versión de abc para m términos tiene
exponente 2m−5 (Browkin–Brzeziński, 1994): ni suponiéndola se obtiene un
control uniforme.

## 4. La ruta de esta rama

**J1, hecho el 16-10.** Esta calibración y su evidencia. En esta rama se
cierra la escalera por número de cambios: el resultado con tres cambios se
conserva y no se sube a cuatro, cinco o seis.

**J2, una sesión: buscar un mecanismo para el régimen genérico.** Pregunta
única: ¿hay algún teorema que impida a una órbita entera quedarse para
siempre, o más de C·log n pasos, en una clase de paridades de entropía
positiva con todos sus ciclos expansivos? Equivale a pedir la pieza 2 de la
contabilidad informacional para una órbita fija. No se releen Mahler ni FLP.
Fuentes que el laboratorio aún no ha leído:

- Akiyama–Frougny–Sakarovitch (2008): base racional 3/2 y partes
  fraccionarias de potencias de racionales;
- Flatto (1992), que FLP citan para el exponente log2(3/2);
- Dubickas–Mossinghoff (2009): algoritmos de búsqueda y su relación con
  mapas sobre enteros;
- las pruebas de las variantes {1,5} y {1,7} en YAH §4.5, para ver qué tipo
  de argumento las cierra.

Cada candidato pasa el filtro de admisión y una prueba de fuego: no puede
aplicarse a −1 ni a −5, que se quedan en AB para siempre (`A^ω` y `B^ω`), ni
a los ciclos racionales de §2.3; tiene que usar que n es un entero positivo.
Si un original no se puede descargar, se pide al usuario, como se hizo con
FLP. Salidas:

- (a) un enunciado para el régimen genérico que pase los seis puntos → J3a;
- (b) ninguno → J3b.

**J3a.** Trasladarlo a 1/110, demostrarlo o refutarlo, y formalizar lo
cerrado.

**J3b.** Cerrar el piloto en esta rama como problema abierto calibrado, caso
particular de la conjetura 4.12 y con la forma de Mahler. Dedicar la rama a
consolidar lo demostrado: preparar la revisión humana de Gao, Wu, Garner y
Ocelotas, con qué afirma cada uno, qué está formalizado y qué falta. Ningún
envío ni contacto sin autorización del usuario. Sobre el
[plan B para Rozier](depuracion/cst20260930/revision_rozier_20261016/PLAN_RESPUESTA.md),
esta rama recomienda no atar la respuesta a un avance del piloto, que puede
no llegar.

**Expectativa: J3b.** Queda escrita para poder comprobarla.

## 5. Qué refutaría esta ruta

1. Que la rama de Astra pruebe (P) con un epsilon uniforme, sin depender del
   número de cambios, para una familia que contenga las palabras de los
   récords de §3.3: recargas de a lo sumo ell/2 y cotas holgadas. Eso
   refutaría la tesis central.
2. Que J2 encuentre un mecanismo para entropía positiva con ciclos
   expansivos: la expectativa J3b sería errónea.
3. Que un censo futuro hasta 2^60, que esta ruta no propone, diera un máximo
   muy fuera de [128, 141]. Ese es el intervalo del 90 % según el modelo, con
   mediana 133. Un desvío así señalaría estructura no aleatoria aprovechable.

Las cifras de §3 son mediciones finitas: dicen dónde viven los casos que una
prueba debe eliminar; no prueban nada universal.

## 6. Lo que esta rama no hace

- No modifica ni borra contenido de la rama de Astra. Si hace falta tocar un
  Markdown compartido, sólo agrega.
- No relee Mahler ni FLP, no sube la escalera de cambios y no amplía censos.
- No cambia a H ni a ciclos. H es la clase de la 4.14, de entropía 0,406 bits
  por paso y con bloques que contraen y expanden: otro caso de la 4.12. En
  ciclos, las 83 rachas de Ocelotas quedan por debajo de las 91 de Hercher.
- No anuncia, no envía y no contacta.

## 7. Correcciones a mi respuesta del 16-10

Al revisar para esta nota:

- FLP (1995) ya estaba leído entero desde el 07-10; J2 no lo repite.
- El piloto no es sólo pariente de la 4.14: es un caso particular de la 4.12.
- Bugeaud–Dubickas (2005) trata bases enteras b, no 3/2.
- Con la convención de RUTA §4, que añade la última A, los récords tienen
  entre 8 y 29 cambios, no entre 7 y 29.

## 8. Evidencia y reproducción

[diagnostico_ruta.py](depuracion/judas20261016/diagnostico_ruta.py) escribe
[diagnostico_ruta.json](depuracion/judas20261016/diagnostico_ruta.json) en
unos 25 s. Usa enteros y `Fraction` salvo en el modelo de §3.1, y es
independiente de los medidores de Perdices. Lee el censo conservado y guarda
su huella sha256; no repite censos.

```powershell
python -B -X utf8 depuracion/judas20261016/diagnostico_ruta.py --censo depuracion/perdices20261007/medicion_salida_ab.json --salida depuracion/judas20261016/diagnostico_ruta.json
```

Tipos: §2.1 y el conteo de §2.3 son pruebas escritas con cotejo; §2.2 es
lectura del original con deducción; el cubrimiento de §2.3 es exacto; §3.1 es
heurística; §3.2 y §3.3 son mediciones finitas; §3.4 es enumeración exacta.
Sin Lean: ninguna pieza es un teorema que otra rama vaya a usar. Estas
afirmaciones no tienen alta en el registro versionado; esta nota no toca
`registro.json`. Revisión humana pendiente.

**Estado:** J1 y J2 cerrados el 16-10. J2 dio la salida (b). J3b empezó el
mismo día con el [expediente de revisión humana](depuracion/judas20261016/EXPEDIENTE_REVISION.md).
El 17-10, AProVE no probó el piloto en este equipo: KILLED con su
portafolio y MAYBE con dos estrategias acotadas (§12). Falta correrlo en una
máquina Linux con más memoria.

## 9. J2, cerrado el 16-10: salida (b)

Detalle, tabla de fuentes y cotejo en
[J2_MECANISMOS.md](depuracion/judas20261016/J2_MECANISMOS.md). En resumen:

- **Reformulación exacta.** Con `z=(n+1)/4`, el piloto cualitativo equivale a
  que se detenga `G(z)=3z/2` si z es par, `(9z+1)/8` si `z=7 mod 8`.
  - Su rama A es la de la condición necesaria de Mahler para los números Z,
    `M(2m)=3m`, `M(4m+1)=6m+2`, en la forma de Michel (1993).
  - Su rama B es la de la H de YAH, que equivale a la 4.14.
  - `G(0)=0` y `G(-1)=-1` son −1 y −5, y G no tiene ciclos racionales
    positivos.
  - Cotejo: tres lecturas de λ coinciden bajo 2^21 y en los 21 récords.
  - En Lean: `JudasPiloto.piloto_iff`, con sólo axiomas estándar.
- **Lectura.** Los mecanismos publicados excluyen órbitas por contracción, por
  pasillo finito, por complejidad lineal o por conteo. El piloto escapa de los
  cuatro: todos sus ciclos expanden, sus colas cubren `[1,5]` y su
  complejidad es exponencial. Los certificados por bloques de Stephan (2026)
  necesitan retención finita. El argumento de mezcla de Kari–Kopra (2017)
  fabrica su trampa a medida. La normalidad de Andrieu–Eliahou–Vivion (2025)
  sólo lo resuelve suponiendo tanto como la conclusión.
- **Calibración.** El piloto es consecuencia de 4.12 y está entre Mahler (por
  la rama A) y la 4.14 (por la rama B). Es del mismo tipo que el problema 4/3
  de Dubickas–Mossinghoff (2009). Todos siguen abiertos.
- **Prioridad.** La cota lineal de Complejidad (≈1,71·m) es el Teorema 5 de
  Dubickas (2009). Se agregó la cita a
  [COMPLEJIDAD.md](depuracion/perdices20261007/COMPLEJIDAD.md#6-prioridad-y-fuentes).
  La del registro está propuesta y validada en copia temporal
  ([correccion_registro.json](depuracion/judas20261016/correccion_registro.json)),
  sin aplicar.

El original de Dubickas–Mossinghoff (2009) se leyó completo en el PDF que
aportó el usuario. Confirma el veredicto y trae un dato: su récord de
supervivencia en Mahler bajo 2^57, 137 pasos, cae sobre la misma ley del
modelo uniforme que nuestro 112 bajo 2^50. Falta el de Flatto (1992), que se
pide al usuario.

## 10. J3b, empezado el 16-10

El piloto queda cerrado en esta rama como problema abierto calibrado:
consecuencia de la conjetura 4.12, hermano de H y con la forma de Mahler, sin
pasillo. La rama pasa a consolidar.

[EXPEDIENTE_REVISION.md](depuracion/judas20261016/EXPEDIENTE_REVISION.md)
reúne Gao, Garner, Wu y Ocelotas en una página. Para cada uno da:
- qué afirma y qué no dice;
- el teorema Lean, con las líneas de cada definición y sus premisas;
- lo ya cotejado;
- preguntas concretas para quien revise;
- lo que falta y quién lo hace.

[verificar_expediente.py](depuracion/judas20261016/verificar_expediente.py)
comprueba sin compilar que siguen vigentes las huellas de los 69 archivos
distintos registrados y que las auditorías sólo nombran axiomas estándar.
Resultado: ninguna diferencia.

Pendientes que esta rama no hace sola, porque piden permiso o una persona:
- la lectura humana;
- el impreso de Wu (Garner se leyó el 17-10);
- llevar el artículo IV a 83 rachas;
- integrar en el registro la cita de Dubickas, ya validada;
- cerrar el 47 por escrito.

## 11. Siguiente paso: AProVE

**Por qué.** J2 leyó los certificados automáticos de YAH, pero no los probó
sobre el piloto. [piloto_yah.srs](depuracion/judas20261016/piloto_yah.srs)
escribe la G de §9 como reescritura de cadenas, con las reglas de YAH que
pasan cifras de base 3 a base 2. Termina desde toda cadena si y sólo si G se
detiene en todo z>=1 ([J2 §2](depuracion/judas20261016/J2_MECANISMOS.md)).

Las dos mitades del sistema terminan con medidas explícitas, comprobadas regla
por regla en [medidas_srs.py](depuracion/judas20261016/medidas_srs.py):
- las reglas X, con (cifras ternarias, inversiones);
- el sistema sin L, con (cifras binarias, inversiones).

En el sistema completo ninguna sirve: junto a L nacen cifras binarias, y las
reglas dinámicas crean ternarias. Una prueba tiene que medir el cruce, y esa
medida es lo que busca un probador.

**Qué hace cada herramienta.**
- Python simula órbitas, y una simulación finita no prueba nada universal.
- Lean comprueba una medida que se le da, pero no la busca.
- AProVE la busca: prueba interpretaciones por matrices, pares de dependencia
  y otras técnicas, y resuelve las cuentas con solucionadores SAT y SMT. Si la
  encuentra, `-C ceta -p cpf` escribe la prueba para CeTA, un certificador
  verificado en Isabelle. También se puede trasladar a Lean.

**Instalación, el 17-10 con el usuario.** Según las páginas de
[descarga](https://aprove.informatik.rwth-aachen.de/download) y
[uso](https://aprove.informatik.rwth-aachen.de/usage), consultadas el 16-10:
- AProVE es código abierto (LGPL-2.1) y está hecho para Java 25. Esta máquina
  tiene Java 8 y no tiene WSL. Java 8 puede quedarse: se llama al `java` de
  la 25 por su ruta completa.
- Usa Z3 (4.4.0 o más), Yices 1 (no la 2) y MiniSat (2 o más). En Windows,
  MiniSat va por Cygwin y `libz3java.dll` se copia como `z3java.dll`.
- Acepta el formato `.srs`. La orden es `java -ea -jar aprove.jar -m wst`
  seguida del archivo, con `-t` para el tiempo en segundos y `-p plain` para
  ver la prueba.
- Eclipse no hace falta: es sólo la interfaz gráfica. La orden se corre desde
  la terminal, como Lean, sin usar la API de Java.
- Hay una imagen Docker con todo incluido y una interfaz web en sus
  servidores. La web enviaría el problema afuera: sólo con permiso.

Orden propuesto: Java 25 y Z3 en Windows, y el peldaño 1 de abajo para probar
la instalación. Si AProVE pide MiniSat o Yices, se decide con el usuario entre
Cygwin y WSL.

**Escalera de calibración.** Cinco peldaños, todos con el mismo tiempo,
anotando YES, NO o MAYBE y los segundos:
1. sólo las reglas X;
2. el sistema sin L;
3. la rama A sola: X y `f R -> 0 R`;
4. la rama B sola: X, `t t t R -> 2 2 R` y `L t t R -> L f f f R`;
5. el sistema completo.

Los peldaños 1 a 4 terminan, y se sabe por qué. Los dos primeros, por las
medidas de arriba. Cada rama sola gasta factores 2: la A los de z, porque
`z -> 3z/2`, y la B los de z+1, porque `z+1 -> 9(z+1)/8`. Juntas, cada rama
puede reponer los factores que gasta la otra. Los peldaños fáciles dicen si la
instalación funciona y hasta dónde llega el probador.

**Salidas.**
- YES en el peldaño 5: sería una prueba del piloto. Antes de afirmar nada se
  certifica con CeTA o en Lean, y la rama pasa a J3a.
- MAYBE o TIMEOUT: confirma (b) también para esta clase de mecanismo, con el
  presupuesto anotado.
- NO: sería un contraejemplo o un error en J2 §2. Se detiene todo y se
  comprueba a mano.
- Si falla un peldaño fácil, el problema es de instalación o de formato, no
  del piloto.

**Expectativa: MAYBE.** YAH sólo lograron certificados automáticos en clases
que contraen o de entropía cero (J2 §4), y la 4.14, hermana de G por la rama
B, sigue abierta. Queda escrita para poder comprobarla.

No se instala nada sin el usuario ni se envía nada a servidores ajenos sin su
permiso.

## 12. AProVE, corrido el 17-10

Detalle, evidencia y reproducción en
[escalera/LEEME.md](depuracion/judas20261016/escalera/LEEME.md).
- Peldaños 1 a 4: YES, como se esperaba. La instalación funciona.
- Peldaño 5, el piloto: KILLED a 300 s y a 3600 s, con 4 núcleos y 5 GB de
  heap. Según §11, confirma (b) con ese presupuesto. No hubo ningún NO.
- La hora no avanzó sobre los 300 s: hacia el minuto 20 se agotó el heap
  (21 `OutOfMemoryError`). En este equipo, de 16 GB, el límite es la memoria.
- Dos estrategias acotadas, con técnicas distintas, sí terminan: MAYBE a los
  39 y a los 43 min (§5 del detalle). Las dos quitan lo fácil y se detienen
  en el mismo núcleo de 2 o 3 pares, que es G misma.
- El portafolio completo, rama por rama y con horas, sigue en curso (§6 del
  detalle). Al derecho se quedó sin memoria a los 31 min; se repite aquí y
  en un portátil de 24 GB.
- En Windows hicieron falta un parche para Java 27 y un adaptador para
  Yices 1 (§2 del detalle).

**Pendiente:** el peldaño 5 en una máquina Linux con 32 GB o más. Lo más
simple es la imagen Docker de AProVE, que trae todo y no necesita parche ni
adaptador. Los pasos, la instalación directa y cómo leer el resultado están
en el §4 del detalle.

## Fuentes

- E. Yolcu, S. Aaronson y M. J. H. Heule, «An automated approach to the
  Collatz conjecture», [arXiv:2105.14697v3](https://arxiv.org/html/2105.14697v3), §4.5.
- Mahler (1968) y Flatto–Lagarias–Pollington (1995): ver las
  [fuentes de la nota de Mahler](depuracion/mahler20261007/LEEME.md#fuentes).
- Y. Bugeaud y A. Dubickas, «Fractional parts of powers and Sturmian words»,
  C. R. Math. Acad. Sci. Paris 341 (2005) 69–74
  ([CRAS](https://comptes-rendus.academie-sciences.fr/mathematique/articles/10.1016/j.crma.2005.06.007/)).
  Leído el resumen.
- A. Dubickas y M. J. Mossinghoff, «Lower bounds for Z-numbers», Math. Comp.
  78 (2009) 1837–1851 ([AMS](https://www.ams.org/mcom/2009-78-267/S0025-5718-09-02211-X/)).
  Leído completo en J2, en el PDF aportado por el usuario.
- S. Akiyama, Ch. Frougny y J. Sakarovitch, «Powers of rationals modulo 1 and
  rational base number systems», Israel J. Math. 168 (2008) 53–91
  ([PDF](https://www.irif.fr/~cf/publications/IJM.pdf)). Leídos §1 y §6 en J2.
- L. Flatto, «Z-numbers and β-transformations», Contemp. Math. 135 (1992)
  181–201, MR 1185087 ([AMS](https://pubs.ams.org/view?ProductCode=CONM/135)).
  Sin leer ni cotejar; citado por FLP, Dubickas–Mossinghoff y
  Andrieu–Eliahou–Vivion. El 17-10 el PDF del capítulo pedía cuenta o
  acceso institucional.
- Fuentes nuevas de J2: ver [J2 §6](depuracion/judas20261016/J2_MECANISMOS.md#6-evidencia-fuentes-y-pendientes).
- J. Browkin y J. Brzeziński, «Some remarks on the abc-conjecture», Math.
  Comp. 62 (1994) 931–939; enunciado consultado en
  [Wikipedia](https://en.wikipedia.org/wiki/N_conjecture).
- Simons–de Weger y Hercher: ver la
  [calibración de ciclos](depuracion/cst20260930/CICLOS_CALIBRACION.md).
- AProVE: páginas de [descarga](https://aprove.informatik.rwth-aachen.de/download)
  y [uso](https://aprove.informatik.rwth-aachen.de/usage), consultadas el 16-10.
  Instalado y corrido el 17-10 (§12).
