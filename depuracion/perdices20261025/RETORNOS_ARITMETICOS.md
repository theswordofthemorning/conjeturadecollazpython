# Perdices: retornos de observaciones aritméticas con crecimiento real

25-10-2026. Se retoma el control de una misma semilla en
[A/B](../perdices20261007/congruencias_codex20261016/RUTA_CODEX.md).
Se conserva Perdices; no se reivindica prioridad bibliográfica.

**Resultado negativo sobre una plantilla:** ninguna función que sea
eventualmente no decreciente con el tamaño dentro de cada clase de
observación puede descender estrictamente en todos los bloques reales A/B,
si observa sólo un módulo fijo y una lista finita de valoraciones de
polinomios fijos. Las valoraciones pueden ser arbitrariamente grandes;
lo que se fija es su lista, no una cota de sus valores.

La obstrucción usa órbitas enteras positivas y conserva la misma semilla
durante todo el recorrido. No depende del testigo racional de 23.
**No refuta el reloj, la terminación de A/B ni todas las funciones de rango.**

## 1. Mapa, dominio y un testigo pequeño

T(n)=n/2 para pares y (3n+1)/2 para impares, sobre enteros positivos.
A=1 dura un paso T; B=110 dura tres. En sus dominios reales,
A(n)=(3n+1)/2 y B(n)=(9n+5)/8. Consideramos bloques con entradas y
salidas impares, de modo que admitan seguir con el lenguaje.
No se introduce una ley aleatoria ni condicionamiento.

El recorrido literal es

```text
231 --A--> 347 --T--> 521 --T--> 782 --T--> 391.
                     <----------- B ---------->
```

Los cuatro bits son 1110. Sus extremos satisfacen

```text
(v_2(231+1),v_2(231+5))=(3,2)
                      =(v_2(391+1),v_2(391+5)),   391>231.
```

Por tanto, una función R no decreciente con n al fijar estas dos
valoraciones cumple R(391)>=R(231). Si descendiera estrictamente en
cada bloque A/B, tendría R(391)<R(347)<R(231), contradicción.
La dependencia de R respecto de las valoraciones puede ser no lineal.

En particular, fracasa la plantilla
`a log(n+5)+F(v_2(n+1),v_2(n+5))`, con a>=0 y F arbitraria.
Esto es más fuerte que descartar una combinación lineal concreta.
El argumento completo de este caso está formalizado en Lean, para
rangos con valores en cualquier tipo preordenado.

## 2. Enunciado general

Fijar un módulo M>=1, un entero h>=1 y una lista finita de pares
(p_i,P_i), donde p_i es primo y P_i es un polinomio entero no nulo.
La observación de n es

```text
O(n)=(n mod M, v_(p_1)(P_1(n)),...,v_(p_d)(P_d(n))).
```

Se usa la valoración del valor absoluto; la marca infinito en los
ceros no interviene en la construcción, que evita todos esos ceros.

**Teorema.** Existen una palabra no vacía V de bloques A/B, una clase
aritmética infinita de semillas positivas n y una observación o fija,
tales que para cada una de esas semillas:

1. V se realiza con T literal, conservando integridad y positividad.
   Todas sus fronteras de bloques son impares.
2. Si y es su salida, entonces y>n y O(y)=O(n)=o.
3. El número de bloques de V es múltiplo de h.

Las semillas varían al variar las observaciones. No se construye una
órbita infinita de una semilla fija.

## 3. Elección de un punto periódico auxiliar

Para b>=1 tomar W_b=A B^b. Su extensión afín es

```text
F_b(x)=(D x+E)/N,
N=2*8^b,   D=3*9^b,   E=11*9^b-10*8^b,
z_b=-E/(D-N).
```

F_b(z_b)=z_b y el denominador reducido de z_b es coprimo con 6.
Los z_b son distintos: poniendo u=(9/8)^b, la razón
E/(D-N)=(11u-10)/(3u-2) es estrictamente creciente con u.
Los z_b son racionales negativos auxiliares; no son las semillas finales.

Cada P_i tiene finitas raíces racionales. Se puede elegir b con
P_i(z_b)!=0 para todos i. Basta ensayar b desde 1 hasta uno más que
la suma de los grados. Esta elección evita, por ejemplo, que añadir
la observación v_2(11n+19) invalide siempre el testigo: ella anula
z_1=-19/11, pero se puede pasar a z_2=-251/115.

Elegir también un entero u>=1 con P_i(u)!=0 para todos i.
Se encuentra entre 1 y uno más que la misma suma de grados.

## 4. Construcción CRT que conserva todas las observaciones

Escribir M=2^(a_2) 3^(a_3) Q_0 con Q_0 coprimo con 6.

Elegir k_2>=max(1,a_2) y k_3>=a_3. Para cada observación de primo 2 o 3,
aumentar k_p hasta que sea estrictamente mayor que v_p(P_i(z)).
Esto es posible porque P_i(z)!=0 y z es integral en esos dos primos.

Para cada p_i distinto de 2 y 3, incluir p_i^(v_(p_i)(P_i(u))+1)
en un múltiplo común Q de Q_0. Así Q es coprimo con 6.
La aplicación F_b módulo Q es una permutación afín: tanto N como D
son invertibles. Un exponente suficiente para que sea la identidad es
Q*phi(Q). En efecto, después de phi(Q) iteraciones su pendiente es 1;
repetir esa traslación Q veces la anula. Si Q=1 tomar exponente 1.

Poner t=h*Q*phi(Q), V=W_b^t, y sean L,S sus cantidades de pasos T e
impares. CRT permite escoger n en las tres clases compatibles

```text
n=z mod 2^(L+k_2),
n=z mod 3^k_3,
n=u mod Q.                                               (1)
```

Los residuos racionales de z se usan sólo en los módulos 2 y 3, donde
su denominador es invertible. No se intenta invertirlo módulo Q.
Esto cubre también primos observados que dividen ese denominador.
La clase CRT contiene positivos arbitrariamente grandes.

La primera congruencia implica el cilindro de V. Como z es su punto
fijo y es 2-ádicamente entero, la ecuación afín final es divisible por
2^L. La [equivalencia del cilindro con las paridades](../perdices20261007/congruencias_codex20261016/DENOMINADOR_GLOBAL.md#1-pregunta-y-criterio-exacto)
garantiza todas las fronteras interiores. También puede comprobarse
por inducción: la divisibilidad final fuerza el primer bit, y después
se aplica el argumento al sufijo. Positividad se conserva en ambas ramas.

Para la salida y se tiene exactamente

```text
y-z=(3^S/2^L)(n-z).                                      (2)
```

Luego y=z mod 2^k_2 y mod 3^k_3. El primer encaje, con k_2>=1,
garantiza que la última frontera también es impar; las demás preceden
a un bloque cuyo primer bit es 1. Además F_b^t es identidad módulo Q,
de modo que y=n=u mod Q.

Si x=z mod p^k y k>v_p(P(z)), entonces P(x)=P(z) mod p^k y sus
valoraciones son iguales. Aplicar esto a n,y en los primos 2 y 3,
y a u,n,y en los demás, prueba todas las igualdades de O. También
y=n mod M. Cada bloque aumenta estrictamente un positivo, así que y>n.
Por construcción, V tiene t*(b+1) bloques, múltiplo de h.
Esto prueba el teorema sin suponer terminación ni hacer un barrido.

## 5. Qué plantilla se descarta y qué queda fuera

Supongamos que, para cada observación o, la restricción de R a los
n con O(n)=o es no decreciente una vez superado algún umbral N_o.
Elegir en la clase de §4 un n>N_o. Su salida y>n tiene la misma
observación, así que R(y)>=R(n).

Si R certificase descenso estricto cada h bloques reales, particionar
V en esos lotes daría R(y)<R(n). Es imposible. Se incluyen h=1 y
cualquier tamaño fijo de lote, sin depender del número de cambios A/B.

El resultado descarta perfiles monótonos en tamaño asociados a un
número finito de residuos y valoraciones polinómicas. Extiende a este
tipo de observaciones la idea de la [barrera por residuos para H](../perdices20261007/SALIDAS.md#5-una-obstrucción-a-los-rangos-polinómicos-por-residuos),
con un mapa y una construcción distintos.

No descarta perfiles que oscilen con el tamaño dentro de una misma
observación, información de precisión creciente, dependencias de todo
el pasado, ni presupuestos amortizados sin descenso en cada lote fijo.
Tampoco se afirma que tales alternativas funcionen. Una función real
como 1/n desciende cuando n crece, pero eso no es por sí solo un rango
bien fundado que pruebe terminación.

La utilidad para la investigación es concreta: añadir sólo más
valoraciones fijas a un potencial monótono de tamaño no reparará esta
plantilla. Sigue abierta una restricción aritmética global de realización.

## 6. Evidencia y alcance formal

[Cotejo](cotejar_retornos.py), [resultado](cotejo_retornos.json): 18
recorridos, 1776 pasos T literales, lotes de uno y tres bloques, tres
traslados por clase CRT. Incluye valoraciones en 2, 3 y 5, un polinomio
cuadrático, la raíz 11z+19 que obliga a cambiar de palabra, y el primo
5 que divide el denominador de z_2. Se contrasta la composición afín
potenciada con las paridades y firmas del recorrido real.
No se amplía ni se repite el censo A/B.

```powershell
python -B -X utf8 depuracion/perdices20261025/cotejar_retornos.py --traslados 3 --lote 3 --salida depuracion/perdices20261025/cotejo_retornos.json
```

[Lean](PerdicesRetornoFirma.lean), [evidencia](evidencia_lean_retornos.json)
y [salida](evidencia_lean_retornos.txt): cinco consultas con Lean 4.32.2,
sin sorryAx. Certifica íntegramente el testigo 231->391 y la imposibilidad
para las dos valoraciones de §1, con rango en cualquier preorden.
**La construcción universal de §§2–5 conserva prueba escrita; no se
atribuye al módulo Lean.** Imports directos cotejados con Mathlib fijado;
no auditoría transitiva completa. Revisión humana y prioridad pendientes.

```powershell
python -B -X utf8 depuracion/perdices20261025/comprobar_lean.py --lean C:/Users/Home/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean.exe --modulo PerdicesRetornoFirma --salida depuracion/perdices20261025/evidencia_lean_retornos.json
```

Quinta [alta versionada](alta_registro.json), con
[conservación del catálogo previo](evidencia_registro.json).
