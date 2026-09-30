# Ocelotas: revisión y extensión exacta hasta diez rachas — 30-09-2026

**Resultado:** bajo la hipótesis externa `RhinEntera`, CST vale para cualquier
`n >= 2` cuyo primer cruce finito tenga **a lo sumo diez rachas impares**.
Hay prueba escrita y cálculos exhaustivos con enteros, cotejados de forma
independiente. El [cierre posterior](CIERRE_LEAN.md) formaliza la criba y
el descenso para las palabras reales representadas por `Palabra`, bajo
Rhin. La [interfaz posterior](CONTADOR_LEAN.md) construye `Palabra` desde
el contador canónico y formaliza también la ausencia de descenso anterior.
Se mantiene el nombre Ocelotas: es una extensión del mismo resultado.

## Qué se revisó y qué se corrigió

Al comenzar había cambios locales en `r_rachas_fino.py` y su salida, y cinco
archivos nuevos de exploración/verificación. Se conservaron esos cambios y
las salidas. El registro `verificar_r_rachas_29_salida.txt` estaba vacío:
no acredita un barrido terminado. No había procesos Python/Lean activos.
Los registros hasta `2^22` y `2^23` se conservan como evidencia anterior;
esta sesión no repitió esos censos.

No se encontró una contradicción en los lemas matemáticos de la extensión.
Sí faltaban la derivación general, la justificación de la cola infinita y una
criba exacta. `expm1` mejora la evaluación numérica, pero no la hace exacta;
60 cifras, una holgura fija y `ceil` no prueban redondeo dirigido. Se corrigió
esa garantía injustificada en `r_rachas_fino.py` y se protegió su ejecución
con `main`, conservando los dos parámetros posicionales locales.

Se recompiló `Ocelotas.lean`: código 0; sus axiomas siguen siendo `propext`,
`Classical.choice`, `Quot.sound`. Su enunciado contiene `RhinEntera` como
hipótesis, aunque `#print axioms` no la enumera: es un argumento del teorema,
no un axioma global. El registro y el estado ahora explicitan también ese
condicionamiento. Esta revisión se limitó al frente CST; no reaudita Gao,
Garner, Wu, Pandas ni Wirsching.

También se precisó la lectura del apéndice A de Rozier–Terracol: el argumento
elemental excluye el caso **acíclico** de una racha; el caso cíclico usa la
exclusión conocida de circuitos, que requiere teoría trascendente.

## Mapa, índices y enunciado

Se usa `T(n)=n/2` si n es par y `T(n)=(3n+1)/2` si es impar, sobre enteros
positivos. Una unidad de tiempo es **un paso de T**, no un paso del mapa
clásico sin atajo. `S_j` cuenta los términos impares entre los índices
`0,...,j-1`. El primer cruce `k=τ(n)` significa

```text
2^j <= 3^S_j para 1 <= j < k,   y   3^S_k < 2^k.
```

Para n par, k=1 y hay descenso inmediato. Para n impar, la palabra hasta k
empieza por 1 y termina por 0: un paso impar multiplica el coeficiente por
3/2 y no puede producir su primer cruce hacia abajo. Escribimos

```text
1^a_1 0^b_1 ... 1^a_r 0^b_r,   a_i,b_i >= 1.
A_0=0, A_i=a_1+...+a_i, q=A_r, P=3^q, Delta=2^k-P.
ell_i=sum_{j<i}(a_j+b_j); x_i=T^ell_i(n); x_1=n.
```

Aquí `1 <= r <= R`, con R=10 para el resultado certificado. Todos los
conteos y exponentes son enteros, sin ley probabilística ni promedio.
En el último paso, `2^(k-1) < P < 2^k`, por primer cruce y paridad; así
`0 < Delta < P` y `k=bit_length(P)`.

## 1. Término aditivo y consecuencias de un fallo

La composición exacta de los tramos da `2^k T^k(n)=Pn+B`, donde

```text
B = sum_i 2^ell_i * 3^(q-A_i) * (3^a_i - 2^a_i).
B/P = sum_i (2^ell_i / 3^A_(i-1)) * (1-(2/3)^a_i) < r.
```

Cada prefactor es <=1 por primer cruce; para i=1 es 1. Cada segundo factor
está estrictamente entre 0 y 1. Por tanto `0 < B < rP <= RP`.

Si `T^k(n) >= n`, entonces `Delta*n <= B < RP`. Definiendo
`M=(R+1)P/Delta`, resulta

```text
n < RP/Delta;   n+1 < M,
```

porque `P/Delta>1`. Esto explica por qué el nuevo límite de semillas es
menor que el preliminar: se usa `RP/Delta` al final, reservando M para las
congruencias. No se cambió de mapa ni de definición de racha.

## 2. Congruencias encadenadas

El tramo impar cumple `2^a_i (T^a_i(x_i)+1)=3^a_i(x_i+1)`.
La coprimalidad implica `2^a_i | x_i+1`; como x_i es positivo,
`2^a_i <= x_i+1`. Después del tramo par,
`x_(i+1) <= T^a_i(x_i)`, y por tanto

```text
2^a_i (x_(i+1)+1) <= 3^a_i (x_i+1).
```

Multiplicando las desigualdades anteriores a i, y usando la divisibilidad
de la racha i, obtenemos

```text
2^A_i <= (n+1) 3^A_(i-1).                         (1)
```

Esta es la desigualdad cuya prueba faltaba en la extensión preliminar.

## 3. Cota global y exclusión de la cola infinita

La comparación exacta `3^5=243 < 256=2^8` da `log2(3)<8/5`.
De (1) y `n+1<M`, por inducción,

```text
q < F_R log2(M),   F_R=sum_{i=0}^{R-1}(8/5)^i.
```

Para r<R se amplía la suma, cuyos términos son positivos. Sea `E=ceil(F_R)`.
La única hipótesis externa es

```text
RhinEntera:  P <= Delta*k^14  cuando 2^(k-1) <= P < 2^k.
```

Así, `M <= (R+1)k^14` y `2^q < ((R+1)k^14)^E`.
Como `2^(k-1) <= 3^q < 4^q`, también

```text
2^(k-1) < ((R+1)k^14)^(2E).                      (2)
```

Sean `C=ceil(log2(R+1))`, `t=floor(log2 k)`. De `k<2^(t+1)` y (2):

```text
k <= 2E*(C+14*(t+1)).                             (3)
```

Elija h con `2^h > 2E*(C+14*(h+1))`. Esa desigualdad persiste para todo
t>=h: al incrementar t, el miembro derecho aumenta en 28E; el izquierdo
se duplica, y el miembro derecho anterior ya es >=28E. Si k>=2^h, entonces
t>=h, y (3) contradice `k>=2^t`. Concluimos **k<2^h**, sin extrapolar
un bucle terminado ni una comparación de logaritmos aproximados.

Para R=10, `F_R=354658733/1953125`, `E=182`, `C=4`, `h=17`:
`131072 > 364*(4+14*18)=93184`. Así **k<131072**.

La cota externa se cotejó con la [proposición 6.3 de Rozier–Terracol](https://arxiv.org/html/2502.00948v5#S6),
que reproduce Rhin, y con el [lema 12 de Simons–de Weger](https://www.impan.pl/shop/en/publication/transaction/download/product/82263).
Para q>=1, `H=k>=2` y `Lambda=k log 2-q log 3>0`; de
`Lambda>=k^(-13.3)` y `exp(Lambda)-1>=Lambda` se deduce `RhinEntera`.
El borde q=0 fuerza k=1 y se verifica directamente. No se afirma haber
formalizado Rhin ni revisado su demostración original de 1987.

## 4. Criba finita sin flotantes

Para cada `q>=1` con `k=bit_length(3^q)<131072`, se calcula exactamente
`Delta=2^k-3^q` y el menor entero m con `(R+1)P <= 2^m Delta`.
Entonces `n+1<M<=2^m`. Elevando (1) a la quinta potencia y usando
`3^5<2^8`,

```text
5 A_i < 5m + 8 A_(i-1).
C_0=0; C_i=floor((5m+8C_(i-1)-1)/5).
```

Por inducción `A_i<=C_i`, de modo que un fallo exige `q<=C_R`.
La sucesión C_i es creciente para m>=1, por lo que también cubre r<R.
Para cada superviviente se conserva el límite exacto inclusivo

```text
n <= floor((RP-1)/Delta).
```

El [certificado entero](certificado_10_rachas.json), generado por
[certificar_rachas.py](certificar_rachas.py), recorre q=1,...,82696.
El siguiente q=82697 ya tiene k=131072 y todos los posteriores también
quedan fuera de la cota. Sobreviven 888 valores de q, todos con k<=3647.
El máximo de semillas es **11214**, alcanzado por la cota del par
`(q,k)=(2301,3647)`.

La iteración directa verifica `T^τ(n)(n)<n` para **2<=n<=11214**, sin
fallos ni casos inconclusos. El mayor primer cruce observado es 105;
el tope explícito de ejecución es 10000. Un tope agotado provoca error,
nunca se interpreta como descenso ni como contraejemplo. Se cotejan además
la identidad aditiva, la suma por rachas y (1) para n<=2000.

Esto cierra la contradicción para todo r<=10 **bajo RhinEntera**. La
universalidad viene de los pasos 1–3, no del barrido por sí solo.
Antes del primer cruce no puede haber descenso, pues el coeficiente es
>=1 y el término aditivo no negativo; por eso se obtiene `t(n)=τ(n)`.
No demuestra la existencia de un primer cruce para todo n ni Collatz.

## Cotejo independiente y Lean

[cotejar_certificado_rachas.py](cotejar_certificado_rachas.py) no importa el
certificador. Usa una criba más débil `q<E*m`, calcula k por duplicaciones
y los límites con `Fraction`. Deja **1023** supervivientes y obtiene el
mismo límite **11214**. Itera el mapa clásico agrupando el paso impar con
su división por 2 y lleva el coeficiente como racional. Coinciden todas las
filas `(n,k,q,T^k(n))`, incluida su huella SHA-256
([salida](cotejo_10_rachas.json)). Incluye los bordes n=2,3,39,11214.

[OcelotasRachas.lean](OcelotasRachas.lean) formaliza `paso_cota`,
`cota_acumulada`, `cota_paso_monotono`, `criba_desde_congruencias` y `cola_diez`. Esta última
certifica la exclusión diádica para **todo t>=17**. Lean 4.32.2, código 0,
sin `sorryAx`; [registro nuevo](lean_revision_rachas.txt).
La [tanda siguiente](TRAYECTORIAS_LEAN.md) incorpora
[OcelotasTrayectorias.lean](OcelotasTrayectorias.lean): ya deduce las
congruencias desde la palabra real, controla el término aditivo y conecta
Rhin con k<131072 mediante una variante enteramente natural. También
formaliza las condiciones de la criba y la cota de semillas.
La [tercera tanda](FINITO_LEAN.md) certifica la iteración finita para
2<=n<=11214 y el ensamblaje con una obligación aritmética explícita.
El [cierre](CIERRE_LEAN.md) certifica esa obligación para 1<=q<=82696
y la aplica. En la [tanda del contador](CONTADOR_LEAN.md), esa `Palabra`
se extrae de la órbita; quedan explícitos primer cruce, conteo y Rhin.

El registro versionado contiene ahora 246 afirmaciones. Se ejecutó
`guardarafirmaciones.py`: conservación de la fuente histórica, vocabulario,
ficheros, integridad y referencias, todo correcto; se regeneró
`afirmaciones.db` ([registro de validación](registro_revision.txt)).
`respuestas.db` no se modificó. Los controles adicionales comprobaron
29325 bordes racionales del techo binario, n=2,3,39, el rechazo de n<2 y
la salida inconclusa al agotar el tope. Se conservó la CLI posicional del
explorador y su salida para r=2, y su importación ya no lanza el barrido.

No se certifica novedad bibliográfica. No se publicaron ni enviaron estos
resultados. Las cotas decimales para r=11,...,20 siguen siendo exploración;
no heredan este certificado.

## Reproducir

Desde la raíz del repositorio:

```text
python -B -X utf8 depuracion/cst20260930/certificar_rachas.py --rachas 10 --max-pasos 10000 --cotejo-hasta 2000 --salida depuracion/cst20260930/certificado_10_rachas.json
python -B -X utf8 depuracion/cst20260930/cotejar_certificado_rachas.py depuracion/cst20260930/certificado_10_rachas.json --salida depuracion/cst20260930/cotejo_10_rachas.json
```

En esta máquina tardaron aproximadamente 2 s y 5 s. Desde
`depuracion/gao20260920/formal`:

```text
lake env lean --version
lake env lean ../../cst20260930/Ocelotas.lean
lake env lean ../../cst20260930/OcelotasRachas.lean
```

**Siguiente paso:** auditar el rango y las constantes de Rhin en la fuente
original y estudiar su descarga en Lean; revisión humana pendiente.
La cadena hasta el contador está cerrada. No ampliar censos por rutina.
