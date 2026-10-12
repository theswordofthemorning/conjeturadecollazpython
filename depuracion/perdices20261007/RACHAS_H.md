# Perdices: rachas del retorno H y compatibilidad de pasado y futuro

11-10-2026. Continúa [Salidas](SALIDAS.md). **Resultado:** las rachas completas
se leen en base 2 hacia delante y en base 3 hacia atrás. Cualquier pasado
finito puede empalmarse con cualquier futuro finito. La densidad relativa
exacta de admitir k retornos futuros y l pasados es `21^(-k)*16^(-l)`.
Esto no excluye una semilla persistente ni resuelve Collatz. Sin pretensión
de prioridad; revisión humana pendiente.

## 1. Mapa, dominio y unidades

Se usa el mapa parcial de Yolcu–Aaronson–Heule, documentado y cotejado con
la proposición 4.15 de su artículo en [Salidas, §3](SALIDAS.md#3-enlace-con-el-problema-publicado):

```text
D(x)=3x/4       para x=0 mod 4,
E(x)=(9x+1)/8   para x=7 mod 8,
H(x) indefinido en los demás enteros positivos.
```

Un paso H son dos o tres pasos del atajo T, respectivamente. Ahora un
**retorno F** es una racha E de largo b>=1, seguida por una racha D de largo
a>=1, ambas máximas, que termina de nuevo donde puede comenzar E.
Su unidad de tiempo son `a+b` pasos H, o `2a+3b` pasos T.

El dominio recurrente es `C={x>0:x=15 mod 24}`: al terminar D se tiene un
múltiplo de 3, y comenzar E exige `7 mod 8`. F queda indefinida si una
racha sale del dominio de H o su final no pertenece a C.
No hay visitas intermedias a C: las salidas E son `8 mod 9`, y los pasos D
anteriores al último son pares. Por tanto F es el primer retorno de H a C.

Toda órbita infinita positiva de H contiene una cola de retornos F.
En efecto, una racha D dura a lo sumo `floor(v2(x)/2)` y una E a lo sumo
`floor(v2(x+1)/3)`, ambos finitos. Por tanto una órbita infinita alternaría
ambas rachas indefinidamente y visitaría C después de cada D. Recíprocamente,
una órbita infinita de F se expande en una órbita infinita de H. Esta
equivalencia es escrita; no se demuestra ninguna de las terminaciones.

No se asigna una ley aleatoria a una semilla. Las densidades de abajo son
naturales relativas a C: `lim #{x<=X:x en S}/#{x<=X:x en C}`.

## 2. Lectura binaria del retorno y lectura ternaria de su inversa

Desde x en C, un retorno existe precisamente cuando se obtienen a,b>=1,
u,w impares positivos y y en C con

```text
x+1=8^b*u,      9^b*u-1=4^a*w,      y=3^a*w.             (1)
```

La maximalidad equivale a

```text
v2(x+1)=3b,       v2(9^b*u-1)=2a.
```

Si cualquiera de las dos valuaciones deja un resto al dividir por 3 o por
2, respectivamente, no se obtiene el retorno completo. También se comprueba
`y=7 mod 8`; la divisibilidad por 3 de y ya sigue de a>=1.

La misma rama se recupera **unívocamente desde y**:

```text
a=v3(y),   w=y/3^a,
2b=v3(4^a*w+1),   u=(4^a*w+1)/9^b,
x=8^b*u-1; se exige x en C.                              (2)
```

Prueba de las valuaciones exactas: en (1), `4^a*w=9^b*u-1` no es divisible
por 3, luego w no es divisible por 3 y `v3(y)=a`. Como x es múltiplo de 3,
`x+1=8^b*u` tampoco lo es; así u no es divisible por 3 y la segunda valuación
es exactamente 2b. La prueba inversa usa que y es impar, luego w es impar;
`4^a*w+1` y u también son impares. Por tanto (2), si pasa sus condiciones,
reconstruye las dos rachas máximas de (1).

Los datos afines son

```text
M=4^a*8^b,   A=3^(a+2b),   B=3^a*(9^b-8^b),
M*y=A*x+B,       0<B<A.                                  (3)
```

Hay retornos que decrecen y otros que crecen. Ejemplos mínimos de sus ramas:

| a | b | x | F(x) | A/M |
|---:|---:|---:|---:|---:|
| 1 | 1 | 615 | 519 | 27/32 |
| 1 | 2 | 2367 | 2247 | 243/256 |
| 1 | 3 | 14847 | 15855 | 2187/2048 |
| 2 | 5 | 4489215 | 4550463 | 531441/524288 |

El signo de `F(x)-x` se calcula con `(A-M)x+B`; una pendiente menor que 1
por sí sola no decide el signo para una entrada pequeña.

## 3. Cada rama es una biyección entre dos progresiones completas

Para cada a,b>=1, sean A,M,B los de (3). La condición `y=7 mod 8` es

```text
A*x+B=7M mod 8M.
```

A es impar, por lo que determina un único `r2 mod 8M`. Añadir `x=0 mod 3`
por el teorema chino del resto da un único r con `0<r<24M`. Reducir la
congruencia módulo 8 muestra `r=7 mod 8`, luego r pertenece a C.

Esta congruencia basta para realizar la rama. En efecto, de la divisibilidad
por M en (3) se deduce `8^b | x+1` y después `4^a | 9^b*u-1`. El cociente
final y es `7 mod 8`, de modo que w es impar. Entonces u es impar y las
valuaciones binarias son exactamente las de §2, sin hipótesis adicionales.

Sea `s=(A*r+B)/M`. Pertenece a C, y `0<s<24A`: como `r<=24M-1` y `B<A`,
se tiene `A*r+B<24AM`. Así la rama es exactamente

```text
r+24M*t  ->  s+24A*t,      para todo t>=0.                (4)
```

Son progresiones positivas completas, incluidos sus representantes mínimos.
La inyectividad de H hace disjuntas las imágenes de ramas distintas; (2)
también lo muestra directamente. Sus densidades relativas a C son `1/M`
para la entrada y `1/A` para la salida.

## 4. Historias arbitrarias y el empalme de pasado con futuro

Para una historia de k etiquetas `(a_i,b_i)`, poner
`M=producto 4^a_i*8^b_i` y `A=producto 3^(a_i+2b_i)`.
La composición conserva la forma (4), con `0<r<24M` y `0<s<24A`.

**Inducción constructiva.** Si el prefijo termina en `s+24A*t` y la rama
nueva tiene entrada `r'+24M'*q`, basta resolver

```text
A*t=(r'-s)/24 mod M'.
```

A es impar y M' es potencia de 2; hay un único `0<=t<M'`. La entrada
compuesta queda entre 0 y `24MM'`. El valor intermedio es menor que `24AM'`,
y pertenece a la progresión positiva mínima de la rama nueva; luego su
índice q satisface `0<=q<A`. La salida compuesta queda entre 0 y `24AA'`.
Esto prueba la inducción, incluidos los extremos mínimos.

En particular, **toda historia finita de rachas es realizable** por positivos
arbitrariamente grandes. La lectura ternaria no impone una prohibición nueva
entre las etiquetas de una historia futura.

Más aún: fijar cualquier historia pasada P de l retornos y cualquier historia
futura Q de k retornos. Para el punto de empalme x, escribir `x=15+24q`.
La imagen de P exige una clase para q módulo `A_P`, potencia de 3; el dominio
de Q exige otra clase módulo `M_Q`, potencia de 2. Son coprimos. Hay exactamente
una clase de puntos de empalme módulo `24*A_P*M_Q`, con densidad relativa

```text
1/(A_P*M_Q).                                            (5)
```

Todos sus miembros positivos admiten el pasado y el futuro prescritos. Los
pasados son positivos por (4), sin pérdidas de representantes pequeños.

## 5. Densidades y justificación de las uniones infinitas

Sumando las densidades de ramas disjuntas,

```text
sum_{a,b>=1} 1/(4^a*8^b) = (1/3)*(1/7) = 1/21,
sum_{a,b>=1} 1/3^(a+2b)  = (1/2)*(1/8) = 1/16.
```

Los cilindros de §4 y (5) sugieren las densidades `21^(-k)`, `16^(-l)` y
su producto. **Hay que justificar el paso desde las uniones finitas**: la
densidad natural no es aditiva sobre uniones numerables arbitrarias.

Truncar ahora por **N pasos H**, no por el número de retornos. Quienes
completan los k retornos dentro de N pasos forman una unión finita de clases.
Quienes los completan más tarde han de admitir al menos N pasos H. Este
último conjunto tiene densidad absoluta `(3/8)^N`, ya probado en
[Salidas](SALIDAS.md#4-inversa-e-historias-qué-se-puede-probar).

Para el pasado se usa la inversa de H. Sus ramas tienen divisores 3 y 9,
numeradores 4 y 8 y condiciones `0 mod 3` y `8 mod 9`. El mismo levantamiento
ternario de historias da densidad absoluta `(1/3+1/9)^N=(4/9)^N` para admitir
N pasos inversos. Sus pasos preservan positividad en sus clases.

Por tanto el error de ambos truncamientos, medido relativamente a C, tiene
densidad superior acotada por

```text
24*((3/8)^N+(4/9)^N) -> 0.
```

Las sumas finitas convergen a las series geométricas anteriores. Se obtiene,
para todo k,l>=0, la igualdad de densidades naturales

```text
d_C({x: admite k retornos F y l retornos F^(-1)})
    =21^(-k)*16^(-l).                                   (6)
```

Ésta es una independencia de **cuentas de clases** entre pasado y futuro,
con el límite de densidades explicitado. No es independencia temporal de
las rachas de una semilla fija, ni condicionamiento a persistencia infinita.
La densidad cero de esa persistencia no prueba vaciedad.

## 6. Evidencia, formalización y límite

[PerdicesRachasH.lean](PerdicesRachasH.lean) añade ocho teoremas: composición
de iterados parciales, paso D, fórmulas de ambas rachas, bloque E^b D^a,
balance entero y unidades módulo 3 en entrada y salida. Las rachas se
certifican para familias parametrizadas por u,w; **la maximalidad, las
valuaciones exactas, las clases y las densidades tienen prueba escrita**.
Lean 4.32.2; sólo axiomas estándar. Son 18 consultas incluyendo RetornoH.
[Evidencia](evidencia_rachas_h.json), [salida](evidencia_rachas_h.txt) y
[reproductor](comprobar_rachas_h.py).

[cotejar_rachas_h.py](cotejar_rachas_h.py) coteja las fórmulas con iteración
independiente de H y de su inversa:

- 10923 semillas de C hasta 262143: 523 retornos, 682 predecesores;
  siete retornos crecen y 516 decrecen. Es sólo una cuenta finita.
- 32552 representantes de todas las historias de hasta tres retornos con
  `1<=a,b<=5`, con cuentas exactas mediante `Fraction`.
- 882 empalmes: todas las parejas de pasados y futuros de hasta dos retornos
  con `1<=a,b<=2`, en dos representantes de cada clase. Incluye historias vacías.
- Nueve períodos completos para parejas de ramas: 146016 semillas cotejadas
  por iteración directa; cada período contiene exactamente el empalme calculado.

[Resultado](cotejo_rachas_h.json). Las identidades valen para todo el dominio
por las pruebas; los cotejos finitos no certifican una órbita infinita.

**Límite encontrado:** la compresión y la inversa no producen una exclusión
finita de historias. Tampoco deciden si los representantes mínimos se
estabilizan sobre una historia infinita. La familia expansiva `(a,b)=(1,3)`
puede repetirse cualquier número finito de veces cambiando la semilla.

**Siguiente, actualizado:** §7 resuelve la comparación de tamaños: es el
transporte exacto del mínimo concatenado. [Matrices H](MATRICES_H.md) inicia
una búsqueda de órdenes sobre palabras de dígitos, fuera de esa reformulación.

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_rachas_h.py --nmax 262143 --amax 5 --bmax 5 --profundidad 3 --salida depuracion/perdices20261007/cotejo_rachas_h.json
python -B -X utf8 depuracion/perdices20261007/comprobar_rachas_h.py --compilados "$env:TEMP/perdices_retorno_h_20261011" --salida depuracion/perdices20261007/evidencia_rachas_h.json
```

## 7. Tamaño del empalme: transporte exacto del mínimo

Fijar un pasado P y un futuro Q. Usar las notaciones de §4 para P, y llamar
`r_PQ` al menor representante positivo de la historia concatenada. Sea m el
menor punto de empalme. Entonces

```text
m = F^|P|(r_PQ),
M_P*m = A_P*r_PQ+B_P.                                   (7)
```

Prueba: la composición de §4 da `r_PQ=r_P+24*M_P*t`, con `0<=t<M_Q`.
Su imagen tras P es `s_P+24*A_P*t`, que realiza el pasado y el futuro y
queda entre 0 y `24*A_P*M_Q`. Por la unicidad CRT de §4, es precisamente m.

Para cualquier semilla n que realiza P, escribir `y=F^|P|(n)`. Restar las
identidades afines da, **sobre enteros con signo**,

```text
M_P*(y-m)=A_P*(n-r_PQ).
```

Como A_P y M_P son positivos,

```text
y>=m  si y sólo si  n>=r_PQ.                             (8)
```

Así, comparar el menor punto de empalme con el tamaño del valor orbital no
añade una restricción independiente a comparar el mínimo concatenado con la
semilla inicial. Para una misma historia completa, todos los puntos de corte
dan exactamente la misma desigualdad (8). Estas desigualdades de tamaño no
sustituyen la congruencia que exige realizar la historia completa.

Incluso la diferencia normalizada está determinada por el aditivo del pasado:

```text
m/(24*A_P*M_Q) - r_PQ/(24*M_P*M_Q)
    = B_P/(24*A_P*M_P*M_Q).                              (9)
```

Es una reducción algebraica con prueba escrita, sin Lean nuevo. El cotejo
independiente [cotejar_transporte_h.py](cotejar_transporte_h.py) enfrenta CRT,
composición de cilindros, composición afín e iteración directa de H: 7225
parejas de historias, 28719 equivalencias de cotas y 14450 trayectorias.
Incluye pasados/futuros vacíos y semillas del prefijo que aún no realizan el
futuro. [Resultado](cotejo_transporte_h.json).

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_transporte_h.py --profundidad 3 --salida depuracion/perdices20261007/cotejo_transporte_h.json
```
