# Borrador de Perdices: constantes con F invertible y A≠B

26-10-2026. Continúa la [clasificación matricial](CLASIFICACION_F_INVERTIBLE.md).
**Borrador local sin integrar en el registro.** El usuario retiró el objetivo
automático durante esta tanda; se conserva el desarrollo y se detiene su
continuación autónoma. El verificador de este borrador es
[comprobar_numerales.py](comprobar_numerales.py), conservado separado del
verificador de los cuatro resultados ya integrados.

**Resultado propuesto:** en el objetivo 57 conectado, ninguna interpretación afín
natural 2×2 con F invertible y A≠B puede eliminar una primera regla
dinámica. Se cubren las tres formas clasificadas, con todos sus parámetros
y vectores constantes sin cota. El argumento no demuestra terminación H
ni excluye F singular, A=B no escalar o falta de conexión. Revisión humana
y prioridad pendientes.

## 1. Dominio, reglas y significado del promedio

Se mantienen el atajo T sobre enteros positivos, el mapa parcial H y el
sistema invertido del objetivo 57 de [Trazas, §1](TRAZAS_MATRICES.md#1-dominio-y-alcance).
Cada letra x denota `z ↦ M_x z+v_x`, con matrices y vectores naturales,
incluido cero. `XY=X∘Y`. Se comparan coeficientes y constantes por separado;
una dinámica es estricta sólo si su constante 0 izquierda es mayor.
Se mantienen las tres dinámicas y las nueve estáticas de la primera etapa.

A,B,E,F,G son matrices de letras, no bloques de paridades. La conexión
significa `W01,W10>0` para `W=A+B+E+F+G`; implica las seis igualdades de
intercambio. F invertible y A≠B permiten aplicar la clasificación anterior.

El promedio usado abajo es **uniforme sobre las 2^h palabras binarias
formales de longitud h**. Equivale a enumerar una vez cada numeral del
intervalo `[2^h,2^(h+1))`. No es una ley sobre órbitas Collatz, no supone
mezcla y no condiciona una semilla a supervivencia. h cuenta letras,
no pasos T ni H.

## 2. Comparación estática de numerales

Para la semántica entera usual, a,b representan `2x,2x+1`; e,f,g,
`3x,3x+1,3x+2`; c inicia en 1. Los nueve intercambios preservan ese entero:

```text
ea→ae, fa→be, ga→af, eb→bf, fb→ag, gb→bg,
ec→bc, fc→aac, gc→bac.                                (1)
```

Cada entero n≥1 tiene una representación ternaria que parte de c si su
primera cifra es 1 y de ac si es 2. Las cifras restantes se añaden como
letras e,f,g por la izquierda. El segundo arranque es necesario: no se
supone que todos los numerales ternarios comiencen en 1.

Las reglas (1) llevan esa palabra a la única representación binaria de n.
Para comprobar terminación de esta conversión basta el par lexicográfico
formado por el número de letras ternarias y el número de pares con una
ternaria a la izquierda de una binaria. Los seis intercambios reducen la
segunda cuenta; las tres reglas terminales reducen la primera. Una forma
normal no puede contener una ternaria: la situada más a la derecha tendría
a su derecha una binaria o c, y admitiría una regla.

En cualquier interpretación afín que oriente débilmente las nueve reglas,
cada conversión disminuye el vector componente a componente. La composición
en un contexto conserva la desigualdad porque todas las matrices son no
negativas. Evaluando en el vector cero:

```text
valor binario de n ≤ valor ternario de n.              (2)
```

Esto vale para todos los enteros n, independientemente de si sus órbitas
T realizan algún bloque. No se usa aquí la terminación de las dinámicas.

## 3. Lema de crecimiento 5:4

El lema siguiente sirve en cualquier dimensión finita. Supongamos las
nueve orientaciones estáticas, vectores no negativos, un vector columna
u estrictamente positivo y una fila ℓ estrictamente positiva, con

```text
ℓu=1,   Q=(A+B)/2,   ℓQ=λℓ,   λ≥2,
Eu≤λu, Fu≤λu, Gu≤λu.                                 (3)
```

Entonces **v_a=v_b=0**.

En efecto, los dos arranques `v_c` y `A v_c+v_a` están acotados por `αu`
para algún α≥0. Las tres constantes ternarias están acotadas por `βu`
para algún β≥0. Son máximos de finitas razones, pues cada coordenada de
u es positiva. Un numeral con j letras ternarias queda acotado por

```text
[αλ^j + β(1+λ+...+λ^(j-1))]u ≤ (α+β)λ^j u,           (4)
```

usando λ≥2; para j=0 la suma es vacía. No se requiere que A y B
individualmente conserven u: sólo el arranque ac es un vector fijo.

Para todo k≥1 se tiene `2^(5k+1)≤3^(4k)`: vale para k=1, y el paso
inductivo multiplica por 32 a la izquierda y por 81 a la derecha.
Así todos los numerales binarios de longitud 5k, cuyos valores están en
`[2^(5k),2^(5k+1))`, admiten a lo sumo 4k letras ternarias. Por (2), (4),
cada uno de sus vectores binarios es ≤`Kλ^(4k)u`, donde `K=α+β` es fijo.

Sea X_h el promedio vectorial de las 2^h palabras binarias, aplicado a
v_c, y `d=(v_a+v_b)/2`. La enumeración exacta da

```text
X_0=v_c,  X_(h+1)=Q X_h+d,
ℓX_(h+1)=λℓX_h+z,     z=ℓd≥0.                        (5)
```

En particular `ℓX_(5k)≥λ^(5k-1)z`. La cota ternaria da
`λ^(5k-1)z≤Kλ^(4k)`, es decir `λ^(k-1)z≤K` para todo k≥1.
Esto fuerza z=0: si z>0, elegir un natural n>K/z contradice
`λ^n≥n+1`. Como ℓ tiene todas sus entradas positivas y v_a,v_b son no
negativos, z=0 implica ambos vectores nulos. Es una prueba universal;
no depende de un censo ni de aproximaciones de logaritmos.

Si v_a=v_b=0, las tres constantes dinámicas izquierdas son v_d. Las
derechas son ≥v_d por no negatividad; la orientación débil las hace
iguales. Por tanto ninguna dinámica puede ser estricta.

## 4. Aplicación a las tres formas

Sea r la primera fila de M_d. Si r=0, las constantes dinámicas ya son
iguales. En adelante r≠0. La parte matricial de `da≥d` da rA≥r, de modo
que rA≠0.

### Imagen común

Se puede escribir `A=λu p`, `B=λu q`, con p,q no negativas y `pu=qu=1`.
Entonces `E=s u p`, `F=sI`, `G=s u q`. La conexión de
`W=(λ+s)u(p+q)+sI` fuerza u y p+q estrictamente positivos. Tomando
`ℓ=(p+q)/2`, se obtiene `ℓu=1`, `ℓQ=λℓ` y `Eu=Fu=Gu=su`.

Además, `BAA=λ²A` y `ABE=sλA`. Su desigualdad dinámica, con rA≠0,
fuerza λ≥s. Para λ≥2 se aplica §3 y se anulan v_a,v_b.

### Núcleo común

Aquí `E=G=sI` y `R=F/s` es no negativa, de traza cero, con R²=I. Por tanto
`R=[[0,t],[1/t,0]]` para t>0. Podemos tomar

```text
u=(t,1),   ℓ=(1/(2t),1/2),   Q=λ(I+R)/2.
```

Se cumplen `ℓu=1`, `ℓQ=λℓ` y `Eu=Fu=Gu=su`. La comparación matricial
`rBAA≥rABE` es `λ²rB≥sλrA`, de modo que rB≠0. La de `dbba≥dbaf` es
`λ²rB≥sλrB`, usando BF=sB. Así λ≥s, y para λ≥2 vuelve a servir §3.

### Resonancia 2:3

Los proyectores `P_a=(A-μI)/μ` y `P_b=(B-μI)/μ` son no negativos,
de rango uno e imagen común. La no negatividad diagonal se justificó
en [Clasificación, §4](CLASIFICACION_F_INVERTIBLE.md#4-consecuencia-para-un-candidato-conectado-con-entradas-hasta-3).
Escribamos `P_a=u p`, `P_b=u q`, con `pu=qu=1`. Entonces

```text
A=μ(I+u p), B=μ(I+u q),
E=ν(I+2u p), F=ν(I+u(p+q)), G=ν(I+2u q).
```

La conexión de `W=(2μ+3ν)I+(μ+3ν)u(p+q)` fuerza u y p+q positivos.
Para `ℓ=(p+q)/2`, se tiene `ℓQ=2μℓ` y `Eu=Fu=Gu=3νu`.
La comparación dinámica ya demostrada exige `2μ≥3ν`. Como μ,ν son
naturales positivos, μ≥2. Se aplica §3 con λ=2μ≥4 y se anulan v_a,v_b.

## 5. Los bordes de factor uno

En las dos formas de rango uno, λ=1 obliga a s=1. Aquí no se sustituye
crecimiento exponencial por una afirmación falsa: se usan las constantes
directamente. Permutar las coordenadas interiores y las columnas de M_d
conserva las desigualdades y la constante 0 de salida. Un cambio diagonal
positivo interior también conserva el orden y la no negatividad, aunque
los vectores transformados sean reales; los argumentos siguientes los
admiten. Ningún cambio de base triangular arbitrario se usa para el orden.

### Imagen común, λ=1

A,B tienen traza uno, rango uno e imagen común estrictamente positiva.
Sus diagonales naturales son 1,0 o 0,1. Si coincidieran las diagonales,
coincidirían A,B. Con diagonales opuestas, la imagen común fuerza que
las dos entradas cruzadas no nulas tengan producto uno. Tras permutar:

```text
A=E=[[1,0],[1,0]], B=G=[[0,1],[0,1]], F=I.
```

rA≥r obliga a r=(r0,0), con r0>0; se cancela r0. Denotando por a_i,b_i,
c_i,e_i,f_i,g_i las constantes, cuatro estáticas dan

```text
g0+a1≤b1+f1,  f1+b1≤b0+e1,
c0+a1+b0≤c1+g0,  c1+b1≤c0+e1.
```

Las dinámicas segunda y tercera dan `e1≤a1`, `f0≤b1`; `fc≥aac` da
`2a0≤f0`. Sumar las cuatro estáticas y dos veces la segunda dinámica
produce `-b1≥0`. Por no negatividad, b1=f0=a0=0 y e1=a1. Los tres
descensos son `a0`, `a1-e1`, `b1-f0`: todos cero. No se exige a1=0.

### Núcleo común, λ=1

Un cambio diagonal positivo convierte R en el intercambio de coordenadas.
Como AF=A y BF=B, las columnas de A y B coinciden; B=RA intercambia sus
filas. Sus diagonales, que el cambio diagonal no altera, son naturales
de suma uno. Tras permutar:

```text
A=[[1,1],[0,0]], B=[[0,0],[1,1]], E=G=I, F=[[0,1],[1,0]].
```

Las partes matriciales de `da≥d` y `dbaa≥dabe` fuerzan r0=r1>0.
Tras cancelar ese factor, r suma las coordenadas. Escribiendo
`x=sum v_a`, `y=sum v_b`, `z=sum v_e`, `w=sum v_f`, las reglas
`ec≥bc`, `fc≥aac` y las dos últimas dinámicas dan

```text
y≤z,  2x≤w,  z≤x,  w≤y.
```

Su suma fuerza x=0, y luego y=z=w=0. Los tres descensos son cero.
Con esto quedan cubiertos todos los parámetros de las tres formas.

## 6. Formalización y contraste independiente

[PerdicesCrecimientoNumerales.lean](PerdicesCrecimientoNumerales.lean)
contiene ocho núcleos: comparación 5:4 para todos los naturales, crecimiento
de potencias, anulación del coeficiente acotado, contradicción 5:4, piso
de la recurrencia afín, ambos bordes y ponderación positiva. Lean 4.32.2,
axiomas estándar y sin `sorryAx`: [evidencia](evidencia_lean_numerales.json),
[salida](evidencia_lean_numerales.txt). La conversión de palabras, la
identidad matricial del promedio y la aplicación completa a las tres
formas conservan prueba escrita. No se presentan como formalizadas.

[Cotejo](cotejar_numerales.py), [resultados](cotejo_numerales.json):

- 255 conversiones exactas, 3313 pasos, contrastadas con las nueve reglas.
  Los tres certificados del control 15 y la representación aritmética
  literal dan 13.252 comparaciones en contexto, todas correctas.
- 36 promedios con Fraction, que enumeran 2044 palabras en cuatro modelos
  y alturas 0..8, coinciden con la recurrencia afín independiente.
- Las dos sumas lineales de §5 se verifican por sus doce coeficientes
  constantes y se cotejan mediante evaluación literal en cero y las bases.

Los censos contrastan código; la obstrucción sin cota descansa en la
prueba escrita y sus núcleos formales. La representación aritmética usual
tiene factor ternario 3 y binario 2: sirve de control positivo de conversión,
pero no cumple (3), por lo que no contradice el lema.

## 7. Alcance de la clausura

Queda cerrada **la familia conectada F invertible, A≠B**, sin cota de
entradas o constantes. No se ha hallado un orden que pruebe terminación:
se ha probado que esta familia no puede proporcionarlo.

El objetivo automático fue retirado. La integración y revisión de este
borrador, F singular, A=B no escalar y la ausencia de conexión continúan
pendientes. El promedio de palabras no
es la transferencia orbital exigida por la segunda condición primordial.
Tampoco aporta control de una semilla fija ni cierra una premisa externa.
Ninguna de las tres condiciones se ha alcanzado todavía.
