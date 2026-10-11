# Perdices: las excepciones al patrón 110 deben ser no acotadas

10-10-2026. Continuación de [Balance](BALANCE.md).

**Resultado:** para una misma fuga pura con infinitos regresos a un
techo fijo, no basta intercalar un número acotado de bloques distintos
de `110`. En toda cola debe haber excursiones con tantas excepciones
como se quiera. Lean certifica el enlace orbital completo. También hay
una tasa logarítmica necesaria con prueba escrita, separada de Lean.

## 1. Dominio y contador

Atajo `T(x)=x/2` para x par y `(3x+1)/2` para x impar.
`x_j=T^j(n)`, `S_j` cuenta entradas impares anteriores a j y
`P_j=3^S_j/2^j`. Los tiempos son pasos del atajo. No hay una ley
aleatoria ni hipótesis de independencia.

Los regresos satisfacen `P_j≤C=3^c`, con n y c **fijos**. Una
excursión no unitaria entre regresos consecutivos u<v tiene la palabra
real `1^a_0 0^b_0 ... 1^a_(r−1) 0^b_(r−1)`, con a_i,b_i≥1.
El último bloque par puede estar truncado en v.

Una **excepción** significa aquí un bloque `(a_i,b_i)≠(2,1)`;
no significa un contraejemplo de Collatz. Se cuentan todos los bloques,
incluido el último. Definimos

```text
E_0=0,
E_(i+1)=E_i + 1 si (a_i,b_i)≠(2,1), y E_i en otro caso.
```

Para un intervalo unitario usamos E=0 por convenio. Quitar el último
bloque del contador cambia E a lo sumo en uno, por lo que no cambia
la conclusión de no acotación ni la tasa asintótica escrita.

## 2. Una cadena larga se comprime en una sola estimación

Sea x>0 la entrada de una palabra real y L natural con `x+5≤2^L`.
Escribimos t_i para el tiempo local al comienzo del bloque i.
Para cualquier prefijo, incluso fuera de una fuga pura,

```text
T(y)+5 ≤ 2(y+5),
T^t(x)+5 ≤ 2^t(x+5) ≤ 2^(L+t).                     (1)
```

Si los bloques j,...,k−1 son `110`, con q=k−j, la congruencia de
Balance da

```text
8^q | T^t_j(x)+5,
2^(3q)=8^q ≤ T^t_j(x)+5 ≤ 2^(L+t_j),
t_k=t_j+3q,    t_k+L≤2(t_j+L).                     (2)
```

(2) no paga un factor por cada repetición. Vale también para la
cadena vacía j=k, y no pierde el valor de entrada de la misma órbita.

Para cualquier bloque, sea o no `110`, su congruencia impar da
`2^a_i≤T^t_i(x)+1≤2^(L+t_i)`, luego `a_i≤L+t_i`.
La identidad par y la positividad de la salida dan
`2^b_i≤T^(t_i+a_i)(x)≤2^(L+t_i+a_i)`. Por tanto

```text
b_i≤L+t_i+a_i,
a_i+b_i≤3(L+t_i),
t_(i+1)+L≤4(t_i+L).                                (3)
```

La positividad es necesaria en el paso que elimina el valor de salida
del producto `2^b_i·T^t_(i+1)(x)`.

## 3. Cota según el número de excepciones

Después de leer k bloques, escoger j justo después de la última
excepción, o j=0 si no hay ninguna. Los bloques j,...,k−1 son `110`.
Una inducción mantiene

```text
t_j+L ≤ 8^E_k L.                                   (4)
```

Un bloque `110` sólo prolonga esa cadena. Al aparecer una excepción,
(2) comprime la cadena previa con factor dos, y (3) añade la excepción
con factor cuatro: el factor total es ocho. El caso inicial es L≤L.
Finalmente se aplica (2) a la cadena que queda al final:

```text
d+L ≤ 2·8^E L,      d≤(2·8^E−1)L.                  (5)
```

`duracion_excepciones` formaliza la primera desigualdad para **toda
palabra real desde x>0**. No necesita hipótesis de fuga, techo ni
regreso. Con `L=ceil(log2(x+5))`, la duración es `O(8^E log(x+5))`.
La constante es conservadora; no se afirma que la base ocho sea óptima.

Los intervalos unitarios también satisfacen la segunda cota con E=0,
pues L≥3. La familia de Balance tiene h arbitrario pero E=1: sólo
su último bloque par rompe `110`. En sus cinco ejemplos publicados
se verifica `d≤15L`; el crecimiento de la semilla explica por qué
es compatible con (5).

## 4. Cierre orbital formal

Supongamos `FugaPura n`: `P_j≥1` para todos los tiempos. En un regreso
u, con x=x_u, la sexta raíz certificada da `x^6≤(Cn)^6(u+1)` y x≥1.
Si una excursión admite E≤H, elegir L=x+5 en (5) basta para obtener

```text
d≤2·8^H(x+5)≤12·8^H x,
d²≤D(n,c,H)(u+1),
D(n,c,H)=(12·8^H)²(Cn)^6+1.                        (6)
```

El +1 incorpora los intervalos unitarios. El predicado
`PocasExcepciones x d H` expresa d=1 o la existencia de una palabra
real de duración d con E≤H.

Si todas las excursiones de alguna cola cumplieran E≤H, (6) impondría
el reloj cuadrático `t_i+1≤(D+t_0+1)(i+1)^2`. Contradice la cuenta
de regresos, que excluye incluso un reloj séxtico. Se enumeran los
mínimos regresos siguientes a cualquier U. El teorema final
`infinitos_exigen_excepciones` da:

```text
FugaPura n ∧ InfinitosRegresos n c
 ⇒ ∀H U, ∃u v r a b, U<u ∧ Consecutivos n c u v
      ∧ Palabra(x_u,a,b,r) ∧ tiempo(a,b,r)=v−u
      ∧ r=rachas(x_u,v−u) ∧ E_r>H.                  (7)
```

Incluye extracción orbital y contador canónico de rachas. No afirma
que todas las excursiones tengan cada vez más excepciones. No supone
ni demuestra que exista la fuga. Con c=0 la premisa de infinitos
regresos es imposible, como en los cierres anteriores.

## 5. Tasa necesaria con prueba escrita

Esta consecuencia analítica **no está formalizada**. Enumerar los
regresos t_i y contar E_i en sus excursiones, con E_i=0 si duran uno.
Por la sexta raíz, se puede elegir
`L_i=ceil(log2(x_(t_i)+5))≤K(n,c)log2(t_i+2)`. (5) implica

```text
d_i ≤ K'(n,c)·8^E_i log2(t_i+2).
```

Si eventualmente `E_i≤η log2(t_i+1)` para algún `0≤η<7/25`, escoger
`3η<a<21/25`. El logaritmo se absorbe en la diferencia positiva de
exponentes y queda `d_i≤A(t_i+1)^a` para A fijo. La concavidad de
`y^(1−a)` da, al sumar sus incrementos,
`t_i+1=O((i+1)^(1/(1−a)))`. Pero la cuenta de regresos exige
`t_i+1≥k(n,c)(i+1)^(25/4)`, con k>0, y `1/(1−a)<25/4`.
Es la contradicción desarrollada en [Ritmo, §4](RITMO.md#4-afinamiento-escrito-de-la-tasa).
Por tanto, omitiendo un eventual t_i=0,

```text
limsup_i E_i/log2(t_i+1) ≥ 7/25.                    (8)
```

La tasa (8) cuenta excepciones al patrón; no reemplaza la cota previa
para el número total de rachas ni demuestra que exista un planeador.

## 6. Evidencia y límites de la ruta

[PerdicesExcepciones.lean](PerdicesExcepciones.lean) contiene doce lemas
nuevos. [comprobar_excepciones.py](comprobar_excepciones.py) audita
dieciocho módulos previos sin recompilarlos y compila sólo éste:
diecinueve módulos y 177 consultas acumuladas. Lean 4.32.2; sólo
`propext`, `Classical.choice`, `Quot.sound`, sin pruebas incompletas
ni hipótesis externas en estos enunciados.
[Evidencia](evidencia_excepciones.json), [salida](evidencia_excepciones.txt).
Revisión humana pendiente.

[cotejar_excepciones.py](cotejar_excepciones.py) calcula órbitas directas,
agrupa paridades y realiza palabras mediante su congruencia afín.
El [resultado](cotejo_excepciones.json) contiene:

- 4737 intervalos antes del primer cruce: 4514 unitarios, 341 bloques
  y 59 cadenas `110`; 9474 controles de (6). Semillas 2..512, hasta
  256 pasos, c=0..4; máximo observado de once excepciones.
- 150 configuraciones modulares, 139 palabras distintas, con la
  excepción al principio, al final o entre dos cadenas de hasta 32
  bloques: 2730 bloques y 225 cadenas. Incluye el control `(2,1)`,
  que no debe incrementar E.
- Cinco ejemplos reutilizados de Balance, sin repetir su censo.
  Bordes: palabra vacía y dieciséis bloques `10` desde x=1; ignorar
  sus excepciones da una cota falsa, y su coeficiente cruza debajo de
  uno en el paso dos, por lo que no es una fuga pura.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_excepciones.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_excepciones.json
python -B -X utf8 depuracion/perdices20261007/cotejar_excepciones.py --n-max 512 --pasos 256 --nivel-max 4 --cadena-max 32 --salida depuracion/perdices20261007/cotejo_excepciones.json
```

Si faltan objetos, reproducir primero [Balance](BALANCE.md#5-verificación-y-siguiente-acción).
Los barridos no prueban universalidad ni infinitud. No se reclama
prioridad bibliográfica. El planeador con suficientes excepciones,
el cohete y la grieta siguen abiertos; Collatz no está resuelto.

**Continuación:** [Aporte](APORTE.md) formaliza el balance firmado y
demuestra su falta de monotonía local con ejemplos exactos. Una familia
escrita acumula muchas excepciones con aporte normalizado acotado al
variar n. El siguiente trabajo enlaza los pesos de las excepciones con
la congruencia de una misma semilla a través de varios regresos.
