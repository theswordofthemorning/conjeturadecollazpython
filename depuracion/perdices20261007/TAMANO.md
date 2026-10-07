# Perdices: tamaño normalizado y regresos sublineales

## Pieza que se añade a la casa

Un mismo fugitivo puro tendría que cumplir restricciones más fuertes
que la cota lineal anterior. Si `P_k` es su pronóstico, queda en Lean

```
R_k := T^k(n)/P_k = o(k).
```

Por tanto, para cualquier techo fijo C>0, sus regresos a `P_k<=C`
cumplen `T^k(n)=o(k)`, restringiendo el límite a esos tiempos.
En términos explícitos: para cada ε>0 existe K tal que, si k>=K
y `P_k<=C`, entonces `T^k(n)<=εk`. K depende de n, C y ε.

Esto mejora `T^k(n)<=C(n+k/3)`. No excluye todavía al planeador:
un valor puede tender a infinito y ser sublineal en el instante de
visita. Tampoco excluye al cohete ni resuelve el muro A.

La segunda vía da una mejora cuantitativa con prueba escrita:
`R_k^6<=n^6(S_k+1)<=n^6(k+1)`. Por tanto, en esos regresos,
`T^k(n)<=Cn(k+1)^(1/6)`. La identidad multiplicativa y su desigualdad
elemental se formalizan; falta formalizar la ordenación y el telescopio
que producen esta cota de sexta raíz completa.

## Mapa, dominio e índices

Se usa el atajo en los naturales,
`T(x)=x/2` para x par y `(3x+1)/2` para x impar.
Escribimos `x_j=T^j(n)`, `b_j=x_j mod 2`,
`S_k=sum_{0<=j<k} b_j`, `P_k=3^S_k/2^k` e `I_k=1/P_k`.
El tiempo se mide en pasos de ese atajo; S cuenta las entradas impares
**anteriores** al instante k. En particular `P_0=I_0=1` y `R_0=n`.

La identidad afín vale para todo n natural, incluido cero. Para los
resultados sobre un fugitivo se supone `FugaPura n`: `P_j>=1` para
todo j. Los teoremas previos implican n>=2 e inyectividad de su órbita.
Las magnitudes se formalizan en los reales y se contrastan con Fraction.
No hay ley probabilística, promedio sobre semillas ni condicionamiento.

## Prueba escrita independiente

En un paso par `P_{j+1}=P_j/2` y `x_{j+1}=x_j/2`, por lo que R
no cambia. En un paso impar `P_{j+1}=3P_j/2` y
`x_{j+1}=(3x_j+1)/2`, por lo que

```
R_{j+1}=R_j+1/(3P_j).
R_k=n+(1/3) sum_{j<k, b_j=1} I_j.
```

El denominador usa P **antes** del paso impar. Así, para n=3, el
primer paso da `R_1=5/(3/2)=3+1/3`.

Para un fugitivo, `0<I_j<=1`. Sea
`A_c(k)=#{j<k : P_j<=3^c}`. En esos tiempos usamos `I_j<=1`;
en el complemento, `I_j<3^(-c)`. Al ampliar la suma impar a todos
los tiempos obtenemos

```
sum_{j<k} I_j <= A_c(k)+k/3^c,
R_k <= n+(A_c(k)+k/3^c)/3.                     (1)
```

La rareza de tiempos bajos ya probada da `A_c(k)/k -> 0` para cada
c fijo. Para ε>0 elegimos primero c con `3^(-c)<=ε`, después K
con `A_c(k)<=εk` y `3n<=εk` para k>=K. La desigualdad (1) da
`R_k<=εk`. El orden de cuantificadores importa: n queda fijo durante
todo el argumento; no se cambia la semilla al ampliar el horizonte.

Finalmente, si `P_k<=3^c`, entonces `x_k=P_k R_k<=3^c R_k`.
Aplicar el resultado con ε/3^c demuestra los regresos sublineales.
Cualquier C positivo queda bajo alguna potencia de 3, por lo que
la formulación escrita con techos arbitrarios se sigue del enunciado
Lean para techos `3^c`.

Hay además una cota explícita, para cualesquiera naturales c,m,k:

```
R_k <= n + ( [6^c(n+k)+2^c*2^(100m)]/16^m + k/3^c )/3.       (2)
```

Es (1) combinada con `tiempos_bajos_mul`. No hace falta simular
`2^(100m)` pasos para que el enunciado valga. Por ejemplo, para
`k=2^(100m)` y n<=k, al tomar c=m resulta el corolario escrito

```
R_k/k <= n/k + (3/8)^m + 1/3^(m+1).
```

En este último paso se usa `2^m<=6^m`; esa especialización no tiene
una consulta Lean propia. La cota (2) y el límite sí están formalizados.

## Formalización y dependencia de la estela

[PerdicesTamano.lean](PerdicesTamano.lean) formaliza la identidad
afín, separación de tiempos, cota explícita, resultado sublineal y
su aplicación a regresos. No se necesita una hipótesis analítica
externa ni se asume Collatz.

## Segunda vía: prueba escrita de la sexta raíz

Para n>0, dividir el incremento afín por `R_j=x_j/P_j` da

```
R_k=n*product_{j<k, b_j=1}(1+1/(3x_j)).
```

Para un fugitivo, las q=S_k entradas impares de este producto son
distintas y al menos 3: la órbita es inyectiva, n>=2 y nunca baja de n.
Al ordenarlas `a_1<...<a_q`, por ser impares se tiene `a_r>=2r+1`.
Como cada factor decrece al aumentar a_r,

```
(R_k/n)^6 <= product_{r=1..q}(1+1/(6r+3))^6
             <= product_{r=1..q}(r+1)/r = q+1.              (3)
```

La segunda desigualdad se comprueba para todo r>=1 multiplicando
por denominadores positivos. Su diferencia es

```
(r+1)(6r+3)^6-r(6r+4)^6
  =729+5381r+15624r^2+22140r^3+15120r^4+3888r^5 >= 0.
```

El caso q=0 usa el producto vacío y da igualdad. Así queda probada
por escrito `R_k^6<=n^6(S_k+1)`. La prueba usa el entero fijo y
los valores que visita, sin recurrir a densidades ni a la cuenta de
Terras. De hecho vale para cualquier prefijo positivo cuyas entradas
impares sean distintas y al menos 3, aunque después cruce.

En un regreso `P_k<=C`, multiplicar por `P_k^6<=C^6` y usar S_k<=k
da `x_k^6<=C^6 n^6(k+1)`. Esto es compatible con regresar a valores
crecientes pero muy lentamente; aún no hay contradicción.

También queda un corolario escrito sobre el número de regresos: para
k>=1, todos los valores visitados en tiempos j<k con `P_j<=C` son
enteros positivos distintos y a lo sumo `Cn k^(1/6)`. Por ello hay
a lo sumo `floor(Cn k^(1/6))` tales tiempos. Esta mejora cuantitativa
de la densidad cero tampoco dice que el conjunto de regresos sea finito.

`identidad_producto` y `factor_sexta` están en el módulo Lean.
La reorganización del producto, la cota `a_r>=2r+1` y su telescopio
son el tramo escrito pendiente de formalizar. El resultado sublineal
anterior sí tiene su cadena completa formalizada por la vía de la estela.

## Dependencias reproducibles

[PerdicesEstela.lean](PerdicesEstela.lean) reproduce el tramo
necesario de las pruebas vigentes de
[CasaTablero](../casa20261004/CasaTablero.lean) y
[CasaPlaneador](../casa20261004/CasaPlaneador.lean), en su propio
espacio de nombres: cota del tamaño, cuenta de casi fugitivos y
rareza de tiempos bajos. El único cambio interno es reemplazar
el acceso a `rasgo_tamano` por su prueba `tamano_antes_del_cruce`.
Esto evita importar los cientos de certificados de 24 rachas que
CasaTablero incorpora a través de CasaOcelotas. Las pruebas
reproducidas no se presentan como descubrimientos adicionales.

Se importa CasaRetrato y CasaPlano **vigentes**, junto con su cierre
de Ocelotas. No se mezcla con Casa de la sesión recuperada ni con
la caché de PerdicesAcoplamiento. El
[comprobador](comprobar_tamano.py) registra versión de Lean,
fuentes, objetos, dependencias, entorno y consultas de axiomas;
su [evidencia](evidencia_tamano.json) y
[salida](evidencia_tamano.txt) permiten auditar ese cierre.
Lean 4.32.2: 12 módulos, 100 consultas, 14 en PerdicesTamano y 10
de pruebas reproducidas en PerdicesEstela. Sólo `propext`,
`Classical.choice` y `Quot.sound`; sin `sorryAx` ni avisos nuevos.

## Contraste exacto y bordes

[cotejar_tamano.py](cotejar_tamano.py) compara iteración entera con
potencias contra actualización afín por Fraction, y también contra
la identidad multiplicativa. La sexta raíz se verifica elevando a
la sexta potencia: no se usan raíces aproximadas.

El [resultado](cotejo_tamano.json) cubre 2051 semillas: 0..2048 y
repunits binarios adicionales, con 100 pasos por semilla:

- 207 151 identidades afines y 207 050 multiplicativas;
- 66 556 cotas (1) sobre prefijos sin cruce previo;
- 56 900 aplicaciones a un regreso bajo el techo;
- 94 397 cotas (3) en prefijos con entradas impares distintas y >=3,
  y 500 factores y telescopios exactos;
- bordes n=0, k=0, c=0 y control `P_2(1)=3/4` tras el cruce.

El prefijo para (1) sólo necesita `P_j>=1` para j<k; no presupone
que haya un fugitivo entre las semillas. El borde mínimo del CLI
también se ejecutó con n-max=0, pasos=0 y nivel-max=0. Estos controles
son finitos: el resultado universal procede de las pruebas.

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_tamano.py --n-max 2048 --pasos 100 --nivel-max 6 --salida depuracion/perdices20261007/cotejo_tamano.json
python -B -X utf8 depuracion/perdices20261007/comprobar_tamano.py --compilados "$env:TEMP/perdices_tamano_20261007" --salida depuracion/perdices20261007/evidencia_tamano.json
```

## Qué debe aportar el siguiente paso

La restricción nueva usa el tamaño y los valores visitados por el
mismo entero. Falta una cota inferior incompatible, o una mejora
suficiente del recuento de regresos. Orden de trabajo al retomar:

1. **Completar la sexta raíz en Lean.** Ordenar las q entradas impares
   distintas, demostrar `a_r>=2r+1` para `1<=r<=q`, comparar productos
   y telescopar `factor_sexta`. El entregable es la cota completa
   `R_k^6<=n^6(S_k+1)` y su aplicación a `P_k<=C`. Mantener como
   hipótesis generales del lema finito la positividad y las entradas
   impares distintas y >=3; deducirlas después de `FugaPura n`.
   Incluir q=0, k=0 y C>0; auditar versión y axiomas.
2. **Certificar la cuenta de regresos.** Usar la inyectividad de la
   órbita para pasar de valores acotados a cantidad de tiempos:
   para k>=1, `#{j<k:P_j<=C}<=floor(Cn k^(1/6))`.
   Conviene probar primero la versión elevada a la sexta potencia,
   dejando explícitos los pasos sobre raíces y parte entera.
3. **Cruzar tamaño con la cuenta de casi fugitivos.** Aplicar
   `cuenta_casi_fugas` al intervalo más pequeño obtenido en el paso 1.
   Justificar que cada valor contado cumple la condición de casi fuga
   con el mismo parámetro de techo; usar inyectividad para trasladar
   la cuenta espacial a tiempos. Escribir constantes, umbrales y
   dependencia en n y C antes de optimizar. Entregable: una cota
   demostrada que mejore la actual, o la obstrucción precisa que
   impida obtenerla; no se presupone esa mejora.
4. **Buscar el choque que falta.** Investigar si un planeador
   intermitente está obligado a regresar con una frecuencia mínima
   incompatible con la cota superior. Infinitos regresos por sí solos
   no dan esa frecuencia: pueden estar arbitrariamente separados.
   Si no aparece una cota inferior, registrar esa limitación. El
   cohete y la grieta requieren argumentos adicionales propios.

En cada paso se conserva el mismo entero n al ampliar k. Sólo se
repite un cotejo si cambia el enunciado o la implementación, con
aritmética exacta y bordes; ampliar censos no sustituye el argumento.
La sexta raíz, por sí sola, todavía permite una fuga lenta; no debe
presentarse como cierre. La rama probabilística tiene sus pendientes
en [UMBRAL.md](UMBRAL.md#continuación-de-la-rama-probabilística).
