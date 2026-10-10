# Perdices: velocidad necesaria de las rachas entre regresos

10-10-2026. Continuación de [Excursiones](EXCURSIONES.md).

**Avance:** la pérdida `2^h` puede reducirse a `(8/5)^h`. Con esta
cota, infinitos regresos de una misma fuga pura exigirían que
`(8/5)^(6h)/(u+1)^4` fuese no acotado en toda cola de excursiones.
Este enunciado entero está en Lean. Una derivación escrita con
logaritmos da una tasa necesaria más fuerte; se distingue debajo.
Ninguna de las dos excluye todas las posibles fugas.

## 1. Mapa, índices e hipótesis

Atajo `T(x)=x/2` para x par y `(3x+1)/2` para x impar, en naturales.
`x_j=T^j(n)`, `S_j` cuenta las entradas impares con índice menor que j
y `P_j=3^S_j/2^j`. El tiempo se mide en pasos del atajo. No hay ley
aleatoria ni se condiciona una distribución.

Se fija **la misma semilla n**, `FugaPura n` (`P_j≥1` para todo j),
y el mismo natural c, con techo `C=3^c`. Los regresos satisfacen
`P_j≤C`. Una excursión tiene extremos consecutivos u<v, duración
`d=v-u` y h rachas impares entre las entradas `[u,v)`. La racha
inicial cuenta aunque empezara antes de u. Si d>1, empieza impar,
termina par y posee la palabra real `1^a_0 0^b_0 ... 1^a_(h-1) 0^b_(h-1)`
con a_i,b_i positivos; el último bloque par puede estar truncado.
Los intervalos d=1 se incluyen aparte en las cotas orbitales.

## 2. Sustituir la base 2 por 8/5

Sea x=x_u, `x+1≤2^L` y s_i el total de pasos impares anteriores al
bloque i. La congruencia orbital de [Separación](SEPARACION.md#3-pocas-rachas-sí-limitan-la-duración)
da `2^s_(i+1)≤(x+1)3^s_i`. Elevando a la quinta potencia y usando
el cálculo entero **3^5=243≤256=2^8**:

```text
5 s_(i+1) ≤ 5L + 8s_i,
3·5^h s_h + 5·5^h L ≤ 5·8^h L.                    (1)
```

La segunda desigualdad se obtiene por inducción desde s_0=0.
La casi fuga desde el regreso impone `2^d≤3^(c+s_h)`, luego
`5d≤8(c+s_h)`. Multiplicando por `3·5^h` y usando (1):

```text
15·5^h d ≤ 40(8^h−5^h)L + 24c·5^h
         ≤ 15(3L+2c)8^h,
5^h d ≤ (3L+2c)8^h.                               (2)
```

(2) conserva la semilla y el nivel, y mejora la base exponencial.
La constante elegida es holgada; para h pequeño la cota antigua
puede ser menor. En el cotejo, n=27,c=1,u=5,v=56 tiene h=13:
la cota antigua es 114676 pasos y la nueva es aproximadamente 10358,
frente a los 51 pasos reales. Es una mejora de cota, todavía muy holgada.

## 3. Teorema entero: un factor normalizado no acotado

Para formalizar la tasa basta elegir L=x+1 y usar la sexta raíz:

```text
5^h d ≤ (3+2c)8^h(x+1),
(x+1)^6 ≤ 64(Cn)^6(u+1).                           (3)
```

La primera incluye d=1. Definimos `D=64(3+2c)^6(Cn)^6`.
Si para todos los intervalos consecutivos se tuviera

```text
8^(6h) ≤ B·5^(6h)(u+1)^4,
```

(3), elevada a la sexta potencia, daría `d^6≤DB(u+1)^5`.
El lema abstracto `reloj_sextico` prueba para toda lista monótona t:

```text
(t_(i+1)−t_i)^6 ≤ A(t_i+1)^5 para todo i
  ⇒ t_i+1 ≤ (A+t_0+1)(i+1)^6.                      (4)
```

Prueba independiente: con M=A+t_0+1 y la hipótesis inductiva,
`d_i^6≤A M^5(i+1)^30≤M^6(i+1)^30`, por lo que
`d_i≤M(i+1)^5`. Se suma al valor previo y se usa
`z^6+z^5=z^5(z+1)≤(z+1)^6`. Incluye A=0 y t_0>0.

(4) contradice el reloj séxtico imposible de Separación, deducido
de `F(K)^150≤2^(150c+894)(Cn)^144 K^24`. Se puede empezar después
de cualquier U y enumerar los mínimos siguientes. Así, Lean prueba:

```text
FugaPura n ∧ InfinitosRegresos n c
 ⇒ ∀B U, ∃u v, U<u ∧ Consecutivos n c u v
               ∧ B·5^(6h)(u+1)^4 < 8^(6h),
     h = rachas(T^u(n),v-u).                       (5)
```

Para B≥1, tomar logaritmos de (5) equivale a exigir excursiones con
`h > [2/(3 log2(8/5))]log2(u+1) + log2(B)/(6 log2(8/5))`.
El primer coeficiente es aproximadamente **0,98318**. Se obtiene
en tiempos arbitrariamente tardíos y para cualquier B, manteniendo
n,c. No afirma que lo cumpla toda excursión ni que h_i tienda a infinito.
Para c=0 no hay infinitos regresos: la premisa ya es imposible.

## 4. Afinamiento escrito de la tasa

Este apartado conserva logaritmos exactos y **no está formalizado**.
Poner `α=log2 3>1`. La congruencia anterior da
`s_(i+1)≤L+αs_i`, por tanto

```text
s_h ≤ L(α^h−1)/(α−1),
d ≤ αc + αL(α^h−1)/(α−1).                          (6)
```

Con L=ceil(log2(x_u+1)), la sexta raíz `x_u^6≤(Cn)^6(u+1)`
implica `L≤K(n,c)log2(u+2)`. Incluyendo d=1, hay una constante
K' fija tal que `d≤K' α^h log2(u+2)`.

Sea t_i la enumeración de todos los regresos, desde cualquier cola,
y h_i sus rachas. Si eventualmente `h_i≤η log2(t_i+1)`, con
`0≤η<21/(25 log2 α)`, escoger a con
`η log2 α<a<21/25`. El logaritmo se absorbe en esa diferencia
positiva de exponentes: `d_i≤A(t_i+1)^a` para A fijo.

Por concavidad de `y^(1−a)`, con 0≤a<1,

```text
(t_(i+1)+1)^(1−a) − (t_i+1)^(1−a) ≤ (1−a)A.
```

Sumando, `t_i+1=O((i+1)^(1/(1−a)))`. Pero la cuenta de regresos
exige `t_i+1≥k(n,c)(i+1)^(25/4)` con k>0. Los exponentes son
incompatibles porque `1/(1−a)<25/4`. Por tanto:

```text
limsup_i h_i/log2(t_i+1) ≥ 21/(25 log2(log2 3)) ≈ 1,26421.  (7)
```

Se omite el eventual término t_i=0 en el cociente. (7) es una
condición necesaria, no una igualdad ni una tasa óptima demostrada.
Usar sólo la base racional 8/5 da el coeficiente menor 1,23881.
El teorema Lean (5) es más conservador; no se presenta como certificación
de (6), la concavidad ni (7).

## 5. Qué aportan exactamente las longitudes pares

También hay una identidad escrita que evita descartarlas. En una
excursión no unitaria, t_i es el tiempo local anterior al bloque i,
e_i el total previo de pasos pares, `t_i=s_i+e_i`,
`q_i=P_(u+t_i)/P_u=3^s_i/2^t_i` y `z_i=x_(u+t_i)+1`.
Las identidades afines de las dos rachas dan

```text
z_(i+1)/q_(i+1) − z_i/q_i = (1−2^(−b_i))/q_(i+1),
z_i/q_i = x_u+1 + Σ_(l<i) (1−2^(−b_l))/q_(l+1).    (8)
```

Para i<h, los extremos de bloque anteriores son interiores a la
excursión, luego su P>C≥P_u y q>1. En consecuencia,
`z_i/q_i≤x_u+1+i`. Como `2^a_i` divide z_i y z_i>0:

```text
2^(s_(i+1)+e_i) ≤ 3^s_i(x_u+1+i),     0≤i<h.        (9)
```

**Cierre posterior:** [Balance](BALANCE.md#2-presupuesto-orbital-con-las-longitudes-pares)
formaliza (9) desde la excursión real mediante una inducción entera.
El telescopado racional de (8) conserva su prueba escrita.

La cota `≤x_u+1+i` se usa **antes** del bloque final. En el extremo
final sólo sabemos q_h>1/2; no se extiende (9) inventando q_h≥1.
Así se aprovechan todas las longitudes pares y el techo interior.
Pero P>C da un límite **superior** a e_i en función de s_i; no da
el límite inferior adicional que cancelaría el crecimiento de α^h.
La identidad no suministra esa cancelación por sí sola.

## 6. Evidencia, límites y continuación

[PerdicesRitmo.lean](PerdicesRitmo.lean) contiene diez lemas, incluida
la extracción heredada, la enumeración y el teorema (5).
[comprobar_ritmo.py](comprobar_ritmo.py) audita dieciséis módulos previos
sin recompilarlos y compila sólo el nuevo: diecisiete módulos y 152
consultas acumuladas, diez nuevas. Lean 4.32.2, Mathlib fijado;
únicamente `propext`, `Classical.choice`, `Quot.sound`, sin pruebas
incompletas ni hipótesis externas en estos enunciados.
[Evidencia JSON](evidencia_ritmo.json), [salida](evidencia_ritmo.txt).
La revisión humana está pendiente.

[cotejar_ritmo.py](cotejar_ritmo.py) usa órbitas directas, enteros y
`Fraction`. [Resultado](cotejo_ritmo.json): 4737 intervalos, 341 bloques,
341 comprobaciones de (8)-(9), 9474 de la implicación para los saltos
y 42405 del reloj abstracto maximal mediante raíz sexta entera.
Son prefijos antes del primer cruce, semillas 2..512, hasta 256 pasos,
c=0..4 y constantes del reloj 0..32. No prueban FugaPura ni infinitud.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_ritmo.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_ritmo.json
python -B -X utf8 depuracion/perdices20261007/cotejar_ritmo.py --n-max 512 --pasos 256 --nivel-max 4 --d-max 32 --salida depuracion/perdices20261007/cotejo_ritmo.json
```

Si faltan objetos, reproducir primero el [cierre previo](EXCURSIONES.md#4-formalización-y-contraste).
No se reclama prioridad bibliográfica. El cohete, la grieta y el
planeador con suficientes rachas siguen abiertos.

**Continuación:** [Balance](BALANCE.md) construye excursiones con pares
interiores de longitud uno al variar la semilla, pero excluye en Lean
una cola del patrón interior 110 para una misma fuga con infinitos
regresos. El siguiente trabajo permite un número acotado de bloques que
rompan ese patrón. Formalizar (7) sigue como pendiente distinto.
