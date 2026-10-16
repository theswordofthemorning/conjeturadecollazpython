# Perdices: dos cambios, orientación resuelta y obligación restante

16-10-2026. Primera aplicación del [filtro de exploración](../exploracionmath20261016/EXPLORACION.md#8-filtro-de-admisión-de-una-nueva-vía).
Continúa [Transporte impar](TRANSPORTE_IMPAR.md#6-obligación-que-queda-para-varias-alternancias).
Conserva el nombre Perdices; no reclama prioridad bibliográfica.

**Resultado:** todo prefijo real `A^a B^b A^c`, con `a,b,c>=1`, cumple el
presupuesto `epsilon=1/2, K(n)=2*ell(n)`. Se obtiene por tamaño y consumo
de valuaciones, sin una nueva hipótesis de independencia ni de descenso.
Para `B^a A^b B^c` queda una obligación aritmética explícita; una región
de sus parámetros también satisface el presupuesto. No se cierra todavía
toda la clase de dos cambios, ni las alternancias generales, ni Collatz.

## 1. Mapa, índices y criterio

`T(x)=x/2` para x par y `(3x+1)/2` para x impar, sobre naturales positivos.
`A=1`, `B=110`, con paridades realmente realizadas desde **la misma**
semilla n. No se usa ley aleatoria. a,b,c cuentan bloques, mientras L
cuenta pasos de T. Las fronteras de las tres rachas son n,y,z,w.

Para el primer y último tipo de bloque se usan las constantes 1 (A)
y 5 (B). Con `v_in=v2(n+c_in)`, `v_fin=v2(w+c_fin)` y
`ell=ceil(log2(n+5))`, el candidato equivale exactamente a

```text
L+2*v_fin <= 2*v_in+4*ell.                            (P2)
```

Es la equivalencia por la identidad firmada `L=v_in+Eeta-v_fin`;
no se sustituye la recarga por su parte positiva. Las valuaciones se
aplican sólo a números positivos. Ninguna cota depende de una salida
desconocida.

## 2. Una cota de tamaño con coeficientes enteros

La desigualdad exacta `3^17=129140163 < 134217728=2^27` implica:
si `2^d Y <= 3^s X`, `X<=2^ell` y `2^v<=Y`, entonces

```text
17*(d+v) <= 27*s+17*ell.                              (1)
```

Prueba: `2^(d+v)<=3^s*2^ell`; elevar a 17, aplicar
`3^(17s)<=2^(27s)` y comparar exponentes de base 2. No se usan
logaritmos en coma flotante. Es sólo una cota de tamaño, no una
estimación aritmética nueva para las partes impares.

Por separado, de `2^d Y=3^s X` se obtiene
`d+v2(Y)=v2(X)`, ya que 3 es impar.

## 3. Presupuesto universal para A^a B^b A^c

Las identidades de las rachas, obtenidas iterando las de cada bloque, son

```text
2^a(y+1)       = 3^a(n+1),
2^(3b)(z+5)   = 3^(2b)(y+5),
2^c(w+1)      = 3^c(z+1).                            (2)
```

La entrada y de B es `3 mod 8`, luego `v2(y+1)=2` y
`v_in=a+2<=ell`. Si `u=v2(y+5)` y `v=v2(z+1)`, el consumo da
`3b<=u` y `v=c+v_fin`.

Por encaje, o directamente a partir de (2),

```text
2^a(y+5) <= 3^a(n+5),
2^(a+3b)(z+1) <= 3^(a+2b)(n+5).
```

Aplicar (1) a ambas desigualdades produce

```text
51b <= 17ell+10a,
17(c+v_fin) <= 17ell+10a+3b.                         (3)
```

Estas cotas ya cierran (P2). En detalle,

```text
17(L+2*v_fin) <= 37a+57b+34ell-17c.
```

De la primera desigualdad de (3), multiplicada por 19 y dividida por
17, se tiene `57b <= 19ell+(190/17)a`. Por ello

```text
3a+57b <= 19ell+(241/17)a
        <= (564/17)ell-482/17
        <= 34ell+68+17c.
```

Se usó `a<=ell-2`, `ell>=0` y `c>=0`. Sustituir en la cota anterior da
`17(L+2*v_fin)<=17(2*(a+2)+4ell)`, que es (P2).
La prueba incluye todas las semillas y longitudes admisibles, no sólo
los cilindros cotejados. Los casos con alguna racha ausente se cubren
por el resultado previo de hasta un cambio.

## 4. Parametrización exacta de B^a A^b B^c

Aquí el segundo cambio impone `v2(z+1)=2`, por ser z entrada de B.
Consumir A^b da `v2(y+1)=b+2>=3`. Puesto que `y+5=(y+1)+4`, se tiene
`v2(y+5)=2`, y al retroceder la primera racha B^a:

```text
v_in=3a+2,                     n+5=2^(3a+2)*q,
y+5=4*9^a*q,                  y+1=2^(b+2)*r,
9^a*q=2^b*r+1,                q,r positivos impares,
z+1=4*3^b*r,                  z+5=4*(3^b*r+1),
k=v2(3^b*r+1)>=1,             3^b*r+1=2^k*s,
v_fin=k+2-3c,                 s positivo impar.       (4)
```

Esta descripción también es suficiente: dados a,b>=1 y r positivo
impar con `9^a | 2^b*r+1`, definir q por (4),
`n=2^(3a+2)q-5`, y elegir `1<=3c<=k+2`. La primera racha B consume
exactamente 3a de las 3a+2 unidades; sus entradas son `3 mod 8`.
La siguiente A consume b de las b+2 unidades y acaba de nuevo en una
entrada B. La tercera racha B consume 3c unidades. Todos los valores
son enteros positivos y realizan las paridades requeridas.

Como `L=3a+b+3c`, sustituir (4) en (P2) da la equivalencia exacta

```text
b+2*v2(3^b*r+1) <= 3a+3c+4*ell(2^(3a+2)*(2^b*r+1)/9^a-5).  (5)
```

Para a,b,r fijos, c=1 es el caso más exigente, y siempre es admisible
porque k>=1. Por tanto, cerrar toda BAB equivale a probar (5) con c=1
para **todos** los a,b,r indicados. La semilla no se reinicia: está
determinada por esos mismos parámetros.

## 5. Región de BAB que sí queda cubierta

El encaje hasta z y (1) dan

```text
2^(3a+b)(z+5) <= 3^(2a+b)(n+5),
17*(3c+v_fin) <= 17ell+3a+10b.
```

Por tanto,

```text
17(L+2*v_fin) <= 57a+37b+34ell-51c.
```

En consecuencia, la condición explícita

```text
37b <= 34ell+45a+51c+68                              (6)
```

es suficiente para (P2). Para estudiar todas las terceras rachas basta
tomar c=1. Fuera de (6) **no se ha refutado** (P2): sólo deja de bastar
esta cota de tamaño. La zona pendiente tiene una racha A central larga
en relación con los bits de la semilla.

## 6. Qué aportó el intento de acoplamiento

Las dos ecuaciones de (4) comparten la misma parte impar r:

```text
9^a*q - 2^b*r = 1,
2^k*s - 3^b*r = 1.
```

Eliminar r da una relación no nula,

```text
3^(b+2a)*q - 2^(b+k)*s = 3^b-2^b > 0.              (7)
```

Pero el miembro derecho es impar y no es divisible por 3. Esta primera
eliminación **no** aporta la alta divisibilidad buscada; tampoco basta
su no nulidad para obtener una contradicción. Haría falta otra cota
para k, r o s en la zona pendiente de (6). No se ha importado el
argumento de determinantes de math como si ya proporcionara esa cota.

El cambio respecto del punto de partida es verificable: se cierra
toda ABA por tamaño, se cubre una región de BAB y se reduce el resto
a (5). La dificultad se concentra en la divisibilidad excepcional de
`3^b*r+1` cuando r satisface simultáneamente `2^b*r=-1 mod 9^a`.
La misma estimación aplicada con una semilla nueva no sería un cierre
de la obligación original.

## 7. Certificación, contraste y siguiente paso

[PerdicesDosCambios.lean](PerdicesDosCambios.lean) formaliza (1), el
consumo, la valuación de entrada B, el cierre ABA bajo las tres
identidades afines (2), la suficiencia algebraica de (6) y la reducción
lineal de (5). El enlace entre las iteraciones de T y (2), y la
parametrización completa (4), conservan prueba escrita en esta nota.
La formalización no afirma el presupuesto para todas las palabras.

[cotejar_dos_cambios.py](cotejar_dos_cambios.py) contrasta con T literal:
cilindros de ambas orientaciones, extremos de la tercera racha,
partes impares pequeñas y congruencias simultáneas por CRT que fuerzan
una valuación terminal exacta. Es una comprobación finita independiente,
no la prueba universal. Las dos orientaciones se comprueban sin asumir
(P2) en la parte BAB pendiente; cualquier fallo se guarda como testigo.

La [evidencia Lean](evidencia_dos_cambios.json) y su
[salida](evidencia_dos_cambios.txt) registran Lean 4.32.2 y ocho consultas
sin `sorryAx`, con sólo propext, Classical.choice y Quot.sound. Se cotejaron
los imports directos con Mathlib fijado; no se hizo una reconstrucción
transitiva completa de la biblioteca.

El [cotejo guardado](cotejo_dos_cambios.json) comprende 6912 representantes
de cilindros (a,b,c hasta 12, dos traslados), 2011 casos con r impar hasta
63 y b hasta 512, y 360 casos CRT con valuación terminal prefijada y bordes
de c. Total: 9283; 1517 fuera de (6); ningún contraejemplo observado.
Por ejemplo, a=1,b=81,r=1,c=1 queda fuera de (6), pero k=2 y satisface
(P2) holgadamente. Fallar (6) sólo indica insuficiencia de esa estimación.

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_dos_cambios.py --racha-max 12 --traslados 2 --b-max 512 --r-max 63 --salida depuracion/perdices20261007/cotejo_dos_cambios.json
python -B -X utf8 depuracion/perdices20261007/comprobar_dos_cambios.py --salida depuracion/perdices20261007/evidencia_dos_cambios.json
```

**Continuación del 16-10:** [Altura BAB](ALTURA_BAB.md) demuestra que un fallo
de P2 exige una terna abc de calidad mayor que 18, sin excluir su existencia.
Con epsilon=7/17 y el mismo K=2*ell, en cambio, cierra por tamaño todo BAB
y por ello todas las palabras con hasta dos cambios. La prioridad pasa a
un tercer cambio desde la misma semilla; P2 general sigue abierto.
Revisión humana pendiente.
