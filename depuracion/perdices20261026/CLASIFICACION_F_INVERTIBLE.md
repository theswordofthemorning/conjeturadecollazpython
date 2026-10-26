# Perdices: tres formas con F invertible y A distinta de B

26-10-2026. Continúa [Trazas matriciales](TRAZAS_MATRICES.md).
**Resultado:** se clasifica por prueba escrita la parte matricial de los
seis intercambios cuando F es invertible y A≠B. Hay dos formas singulares
y una forma con autovalores en proporciones 2:1 y 3:1. No se descartan
sus constantes arbitrarias ni se certifica terminación. Revisión humana
y prioridad pendientes.

## 1. Hipótesis y tres formas necesarias

Todas las matrices son 2×2 con entradas naturales, incluido cero. Se
conservan composición, orden, mapa T, mapa parcial H y objetivo 57 de
[Trazas, §1](TRAZAS_MATRICES.md#1-dominio-y-alcance). Las mayúsculas denotan
matrices de letras; no son bloques de paridades. No se asigna una ley
aleatoria ni una unidad temporal a esta clasificación algebraica.

Se supone `det F≠0`, `A≠B` y

```text
EA=AE, FA=BE, GA=AF, EB=BF, FB=AG, GB=BG.              (1)
```

En el objetivo conectado, las desigualdades débiles implican (1) por el
teorema de trazas. La clasificación siguiente sólo requiere (1); no exige
conexión. Todo quinteto con estas hipótesis pertenece a una de las formas:

| Forma | Parámetros naturales positivos | Identidades |
| --- | --- | --- |
| Imagen común | λ,s | `A²=λA`, `B²=λB`, `AB=λB`, `BA=λA`; `F=sI`, `λE=sA`, `λG=sB`. A,B tienen rango uno e imagen común. |
| Núcleo común | λ,s | `A²=λA`, `B²=λB`, `AB=λA`, `BA=λB`; `E=G=sI`, `λF=s(A+B)-sλI`, `F²=s²I`. A,B tienen rango uno y núcleo común. |
| Resonancia 2:3 | μ,ν | A,B tienen autovalores μ,2μ; E,F,G tienen autovalores ν,3ν. Para `N=A-B`, `AN=2μN`, `NA=μN`, `N²=0`; `μE=2νA-μνI`, `μF=ν(A+B)-μνI`, `μG=2νB-μνI`. |

No se dice que todos los parámetros y matrices de la tabla sean naturales
o satisfagan las dinámicas: la no negatividad e integridad siguen siendo
requisitos. Tampoco se afirma que cada forma admita descenso. En las dos
primeras formas `λ=tr A=tr B`; en la tercera `3μ=tr A`, `4ν=tr F`.
Los determinantes de F son, respectivamente, `s²`, `-s²` y `3ν²`.

## 2. Reducción a una misma forma triangular

De cuatro ecuaciones de (1) se obtienen, sin invertir A ni B,

```text
F AB = B² F,       F BA = A² F.                        (2)
```

Como F es invertible, las matrices de cada par son semejantes. Escribiendo
`a=det A`, `b=det B`, las igualdades de determinantes dan `ab=a²=b²`, luego
`a=b`. Las trazas de (2), junto con `tr AB=tr BA`, dan
`tr(A²)=tr(B²)=tr(AB)`. Para una matriz 2×2, `tr(A²)=(tr A)²-2det A`.
Las trazas de A,B son no negativas; por tanto `tr A=tr B`.

Así N=A-B es no nula, `tr N=0` y

```text
det N = det A + det B - tr A tr B + tr AB = 0.
```

La identidad 2×2 de Cayley–Hamilton, verificable expandiendo las entradas,
da `N²=0`. N tiene rango uno. En una base real donde N tiene su única
entrada no nula en (0,1), la igualdad `tr(AN)=0` obliga a `A10=0`.
B=A-N es triangular en la misma base. Escribimos

```text
A=[[l,a],[0,m]],      B=[[l,b],[0,m]],      a≠b.         (3)
```

El cambio de base se usa para resolver ecuaciones, **no** para transportar
el orden componente a componente ni las constantes naturales.

### Los valores propios repetidos y opuestos

Si l=m≠0, AB=BA y (2) implica A²=B² por cancelación de F. La entrada
cruzada sería `2l(a-b)=0`, contradicción.

Si l=-m≠0, en las coordenadas originales `tr A=tr B=0` y las cuatro
diagonales son cero. Poniendo `A01=x,A10=y,B01=u,B10=v`, se tiene
`xy=uv>0` y `xv+yu=2xy`. Los números positivos xv,yu tienen producto
`(xy)²` y suma `2xy`; son iguales a xy. De ahí x=u e y=v, contradicción.

Si l=m=0, las matrices naturales A,B son nilpotentes. La igualdad
`tr AB=0` obliga a que sus posibles entradas no nulas tengan la misma
orientación; tras intercambiar coordenadas son `aJ,bJ`, con `a,b≥0`,
donde J tiene su único uno en (0,1). Si sólo una es no nula, (1) fuerza
una fila o columna de F a cero. Si ambas son no nulas, (1) fuerza F
triangular con diagonales u,v positivas, y `au=bv`, `bu=av`. Entonces
`(a-b)(u+v)=0`, de nuevo A=B. Se han cubierto los bordes nulos.

Por tanto `l²≠m²`. La entrada (1,0) de (2) fuerza `F10=0` en la base
(3). EA=AE y GB=BG fuerzan `E10=G10=0`. F es triangular invertible, por
lo que sus dos diagonales son no nulas.

## 3. Resolución de las tres ramas

**m=0.** Entonces l≠0. Las primeras diagonales de E,F,G coinciden en s;
escribamos sus segundas diagonales como q,t,r, y sus entradas (0,1)
como e,f,g. Las seis ecuaciones cruzadas son

```text
sa=le+aq, sa=le+bq, sa=lf+at,
sb=lf+bt, sb=lg+ar, sb=lg+br.
```

Restar y cancelar a-b da `q=r=0`, `t=s`; luego `f=0`, `le=sa`, `lg=sb`.
Al volver a las coordenadas originales resulta la forma de imagen común.
Aquí λ=l=tr A>0 y F=sI implica que s es un natural positivo.

**l=0.** Ahora m≠0. Las segundas diagonales de E,F,G coinciden en t;
las primeras son q,s,r, respectivamente. Las ecuaciones cruzadas son

```text
qa+em=at, sa+fm=bt, ra+gm=at,
qb+em=bt, sb+fm=at, rb+gm=bt.
```

Se obtiene `s=-t`, `q=r=t`, `e=g=0`, `mf=t(a+b)`. Esto da la forma de
núcleo común con λ=m=tr A>0 y parámetro s de la tabla igual a t. Puesto
que E=G=tI son matrices naturales y F es invertible, t es natural positivo.
F tiene traza cero; en las coordenadas originales sus diagonales son cero
y ambas entradas cruzadas positivas. No es una matriz singular.

**lm≠0.** Las diagonales de E,F,G coinciden, digamos s,t, y sus entradas
cruzadas son e,f,g. Las ecuaciones cruzadas son

```text
sa+em=le+at, sa+fm=le+bt, sa+gm=lf+at,
sb+em=lf+bt, sb+fm=lg+at, sb+gm=lg+bt.
```

Las dos primeras y las dos últimas dan
`m(e-f)=t(a-b)=m(f-g)`. Como m,t y a-b son no nulos,
`e-f=f-g≠0`. Las ecuaciones restantes dan
`(s-3t)(a-b)=0` y `(l-2m)(e-f)=0`. Así `l=2m`, `s=3t` y

```text
e=2ta/m,       f=t(a+b)/m,       g=2tb/m.
```

Se obtiene la tercera fila con μ=m,ν=t. La no negatividad de las trazas
originales da μ,ν>0. También son enteros: `9det A=2(tr A)²` obliga a
`3 | tr A`; `16det F=3(tr F)²` obliga a `4 | tr F`. Las fórmulas de la
tabla son identidades matriciales, por lo que se conservan al deshacer
el cambio de base. Esto completa la clasificación bajo (1), sin suponer
invertibles A,B ni ignorar los casos de rango uno.

## 4. Consecuencia para un candidato conectado con entradas hasta 3

En la tercera forma, la recta de N es el espacio propio de A,B para 2μ,
y de E,F,G para 3ν. Contiene un vector v no negativo y no nulo. Una
justificación explícita: `(A-μI)/μ` es una proyección no negativa de rango
uno. Sus entradas cruzadas son no negativas; las diagonales también,
pues `(A00-μ)(A11-μ)=A01 A10≥0` y su suma es μ>0.

Si `W01,W10>0`, la igualdad `Wv=(4μ+9ν)v` fuerza las dos coordenadas de
v a ser positivas. Si r es la primera fila no negativa de M_d y existe
alguna dinámica estricta, r≠0 y rv>0. Aplicar `rBAA≥rABE` a v da

```text
(2μ)³ rv ≥ (2μ)²(3ν) rv,       luego 2μ≥3ν.           (4)
```

Con entradas matriciales en 0..3, `3μ=tr A≤6` y (4), ν≥1, fuerzan μ=2.
Entonces A00=A11=3 y det A=8 exige A01 A10=1, es decir A01=A10=1.
Lo mismo para B; resultaría A=B, contradicción. Por tanto, en ese ensayo
acotado, un candidato conectado con F invertible y A≠B **debe estar en
una de las dos formas de rango uno**. Esto es un filtro algebraico; no
declara insoluble la plantilla completa 0..3 ni permite ampliar la cota.

## 5. Formalización, contraste y límites

[PerdicesClasificacionTriangular.lean](PerdicesClasificacionTriangular.lean)
formaliza seis núcleos: igualdad de determinantes y trazas a partir de sus
identidades escalares, las tres resoluciones triangulares y la cancelación
del borde nilpotente. [Evidencia](evidencia_lean_clasificacion.json),
[salida](evidencia_lean_clasificacion.txt): Lean 4.32.2, axiomas estándar,
sin `sorryAx`. La semejanza, triangularización, clasificación matricial
completa, integridad de parámetros y consecuencia (4) conservan prueba
escrita; no se presentan como formalizadas.

[Cotejo entero](cotejar_clasificacion.py), [resultado](cotejo_clasificacion.json):
recorre el espacio de 1.048.576 quintetos binarios con poda exacta.
Ocho satisfacen (1), F invertible y A≠B: seis tienen imagen común y dos
núcleo común; cuatro son conectados. Contrasta además 81 ejemplos de
cada forma singular y 216 de resonancia, todos con entradas naturales.
Entre estos últimos, 72 cumplen (4); **eso no los convierte en certificados**.
El clasificador comprueba las ecuaciones originales antes de las fórmulas.
Las 256 matrices con entradas 0..3 confirman que la única con
`tr A=3μ`, `det A=2μ²` y μ≥2 es `[[3,1],[1,3]]`, como exige §4.

[Exploración singular](explorar_singulares.py),
[resultado](exploracion_singulares.json): doce asignaciones canónicas con
λ=1,2,3 y 1≤s≤λ, primera fila de M_d en 0..3 y vectores naturales sin
cota, dieron UNSAT en Z3 4.15.4. No tienen certificado Lean de UNSAT y no
cubren todas las matrices de las dos formas. No se generaliza ese ensayo.

La clasificación elimina una indeterminación de coeficientes, no la
persistencia de una semilla. Ninguna de las tres condiciones primordiales
queda satisfecha. Restan las constantes de estas formas, `F` singular,
`A=B` no escalar y los intercambios sin conexión bidireccional. La siguiente
acción debe usar estas ramas explícitas; una nueva enumeración sin cota
ni un timeout mayor no completarían la prueba.
