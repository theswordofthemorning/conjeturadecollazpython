# Perdices: qué exige la cola real del cohete

10-10-2026. Continúa [Colisiones](COLISIONES.md). El planeador sigue
excluido. Este bloque precisa la cola del cohete y descarta un salto
injustificado a una ventana de ancho fijo. **Cohete, grieta y Collatz
siguen abiertos.** No se reclama prioridad bibliográfica.

## 1. Mapa y alcance

Atajo T sobre naturales, par n/2 e impar (3n+1)/2. Para una semilla
n>0, `x_j=T^j(n)`, `S_k=#{j<k:x_j impar}`, `P_k=3^S_k/2^k`,
`I_k=1/P_k` y `R_k=x_k/P_k`. Los índices cuentan pasos del atajo.
No hay ley aleatoria ni condicionamiento probabilístico.

Las identidades finitas valen sin fuga ni inyectividad. Para los
límites se supone que `j -> x_j` es inyectiva en todos los naturales.
Entonces Colisiones da `R_k -> ξ` real finito y `P_k -> infinito`.
En Lean `estatura n` es el supremo de R; sólo se interpreta como ξ
bajo esas hipótesis. Se define

```text
t_k = (ξ-R_k)/I_k = ξ P_k-x_k.
```

FugaPura aporta positividad e inyectividad; no se certifica su
existencia mediante prefijos finitos.

## 2. Una segunda identidad monótona

Además de R_k, es monótona la cantidad

```text
A_k = R_k+I_k = (x_k+1)/P_k.
```

Un paso impar deja A sin cambio; un paso par añade I_k. Por inducción,

```text
R_k = n + (1/3) sum_{j<k, impar} I_j,
A_k = n+1 + sum_{j<k, par} I_j.                          (1)
```

La primera identidad ya estaba formalizada. La segunda incluye el
1 inicial: olvidarlo cambia el piso de la cola. Una comprobación
independiente consiste en telescopar los incrementos de I:

```text
I_(j+1)-I_j = I_j si x_j es par; = -I_j/3 si es impar.
```

Como I_k->0, ambas sucesiones R y A tienen límite ξ. Resulta

```text
ξ >= n+1,
sum_{j>=0} I_j = 4(ξ-n)-1 < infinito.                   (2)
```

La identidad finita, anterior al límite, es
`sum_{j<k} I_j = 4(R_k-n)+I_k-1`. Lean prueba sumabilidad y el
valor exacto de la serie en (2), ya sobre **todos** los índices.
Por separado, los valores de las series par e impar son ξ-n-1 y
3(ξ-n); estas dos igualdades infinitas se deducen aquí por escrito
de (1), sin lemas Lean específicos adicionales.

## 3. Piso, dinámica y tamaño relativo de la cola

Aplicar A_k<=ξ y multiplicar por P_k da

```text
t_k >= 1,
t_(k+1) = t_k/2                   si x_k es par,
t_(k+1) = (3t_k-1)/2              si x_k es impar.        (3)
```

Por tanto, antes de un paso par t_k>=2; antes de a pasos pares
consecutivos t_k>=2^a. El mismo cálculo expresa la cola mediante
las dos series futuras:

```text
t_k = (1/3) sum_{j>=k, impar} P_k/P_j
    = 1 + sum_{j>=k, par} P_k/P_j.                       (4)
```

El piso y la dinámica de (3), incluidos los bloques de ceros, están
en Lean. (4) se deduce por escrito de (1) y sus límites. La versión
finita con corte K es

```text
t_k^(K) = (R_K-R_k)/I_k
        = 1 + sum_{k<=j<K, par} I_j/I_k - I_K/I_k.        (5)
```

El término final no se puede omitir: n=1, k=0, K=1 da t=1/3.
El piso infinito de (3) no vale para todo corte finito.

Por otro lado,

```text
t_k/x_k = (ξ-R_k)/R_k -> 0.                             (6)
```

También está formalizado. (6) dice que la cola es pequeña en
relación con x_k; **no dice que t_k tienda a cero ni que esté
acotada por una constante**. Por ejemplo, la implicación lógica
`a_k/b_k ->0 => a_k acotada` ya falla con a_k=k y b_k=k².
No son órbitas Collatz; sólo distinguen las dos afirmaciones.

## 4. Prefijos con colas finitas arbitrariamente grandes

Para cada q>=1 tomar la palabra

```text
w_q = 1^(2q) 0^q 11,       K=3q+2,       k=2q.
```

Existe una única clase de semillas módulo M=2^K que realiza esa
palabra, por la biyección de paridades ya disponible. Su representante
n_q satisface 0<n_q<M porque el primer bit es 1. Explícitamente,

```text
B_q = 9(3^(2q)-2^(2q)) + 5*2^(3q),
n_q = -B_q * (3^(2q+2))^(-1) mod 2^(3q+2).              (7)
```

La composición afín da `2^K x_K=3^(2q+2)n_q+B_q`.
Todos los pronósticos de ese prefijo son >=1: las primeras 2q
subidas aumentan P; tras los q pasos pares aún queda `(9/8)^q>=1`;
las dos subidas finales vuelven a aumentarlo. En el inicio de los
ceros, los dos términos impares futuros de la cola finita dan

```text
t_(2q)^(3q+2) = 2^q/3 + 2^(q+1)/9 = (5/9)2^q.          (8)
```

Así no hay una cota absoluta uniforme para estas colas finitas
deducible sólo de que el prefijo no cruce. **Varía la semilla.**
Esto no construye una fuga infinita fija, no demuestra que tales
prefijos se prolonguen a cohetes, ni refuta una posible cota B(n)
para la cola de un cohete. Sirve para impedir esa inferencia a partir
de datos finitos. (7)–(8) tienen prueba escrita y cotejo exacto;
la familia completa no está formalizada en Lean en este módulo.

## 5. Lo que sí da cuantitativamente la cuenta de colisiones

La cuenta de Colisiones permite empezar los anillos en m en vez
de cero. Si una órbita positiva inyectiva satisface
`x_j>=2^(100m)` para todo j>=k, entonces

```text
sum_{j>=k} 1/x_j <= 3*2^100/2^m,
t_k <= x_k [exp(2^100/2^m)-1].                           (9)
```

Prueba: sumar desde el anillo m las cotas
`3*2^99*2^(-r)`, r>=m. Después aplicar `1+u<=exp(u)` al producto
corrector de la órbita reiniciada en x_k. Su límite normalizado
local es ξ P_k, pues `R_j(x_k)=P_k R_(k+j)(n)`. Restar x_k da (9).
Estos pasos cuantitativos están escritos; **(9) sigue por formalizar**.
Se cotejó el telescopio racional, sin evaluar exponenciales en flotantes.

En particular, para FugaPura n no hay descenso: si n>=2^(100m),
entonces `ξ-n<=n[exp(2^100/2^m)-1]`. Eligiendo el mayor m
admisible, el lado derecho es `O(n^(99/100))` al crecer n entre
semillas de fuga pura. Es una cota condicional uniforme; no afirma
que exista ninguna de esas semillas. Para justificar la notación,
`2^(100m)<=n<2^(100(m+1))` implica
`2^100/2^m < 2^101 n^(-1/100)`, y `exp(u)-1<=2u` para u
suficientemente pequeño. Tampoco esta forma asintótica está en Lean.

Como P_k->infinito, cada cola temporal de P alcanza un mínimo.
Si u es uno de esos mínimos, `P_(u+j)/P_u>=1` para todo j: el
reinicio en x_u es FugaPura. Hay tales u arbitrariamente tardíos,
y x_u->infinito. Así (9) se aplica con x_u como piso futuro. Esta
extracción es un argumento escrito; el módulo no la formaliza.

La anchura de (9) puede crecer con x_u. **Siguiente:** formalizar
esta cota y comprobar si el residuo entero de la palabra añade una
restricción incompatible con ella. Una ventana constante todavía
necesita un argumento adicional; no se obtiene tomando el límite
en una cota relativa.

## 6. Una precaución bibliográfica concreta

Se consultó López–Stoll,
[*The 3x+1 Periodicity Conjeture in R*, arXiv:2101.12747v1](https://arxiv.org/abs/2101.12747v1)
(2021), §2, pp. 7–8, y el enlace de la prueba del teorema 1,
pp. 29–30. No se leyó aquí íntegro el preprint de 51 páginas.
Allí se pasa de la irracionalidad del límite real a la aperiodicidad
del límite 2-ádico asociado a las sumas parciales, usando (15)–(16).
No incorporamos su conclusión al registro como teorema utilizable:
ese transporte de racionalidad requiere una justificación que no
proporciona la mera convergencia en ambos espacios.

Control independiente de la inferencia general: poner

```text
a_m = floor(sqrt(2)*(3/2)^m),
q_m = 2^m a_m/3^m.
```

Entonces `0<=sqrt(2)-q_m<(2/3)^m`, de modo que q_m tiende al
irracional sqrt(2) en los reales. Pero q_m es divisible por 2^m
en los 2-ádicos y allí tiende al racional 0. La secuencia de
residuos compatibles no determina la racionalidad del límite real.
**Estos q_m no son sumas de una palabra Collatz**: no constituyen
un contraejemplo al teorema del preprint. Identifican el puente
adicional que falta cotejar antes de usarlo contra el cohete.

## 7. Evidencia y reproducción

[PerdicesCola.lean](PerdicesCola.lean): 23 lemas nuevos. Identidades
par y total, límite de I, aumentado monótono con límite ξ, piso y
dinámica de la cola, bloques de ceros, sumabilidad y valor de la
serie completa, y límite relativo cero. Sin hipótesis bibliográficas
nuevas. La familia (7)–(8), las series separadas de (4) y la cota (9)
tienen sólo prueba escrita donde se indica.

[comprobar_cola.py](comprobar_cola.py) audita 23 módulos previos y
compila únicamente el nuevo: 24 módulos, 275 consultas de axiomas.
Lean 4.32.2 y Mathlib fijado; sólo axiomas estándar, sin avisos ni
pruebas incompletas. [Evidencia](evidencia_cola.json),
[salida](evidencia_cola.txt). Revisión humana pendiente.

[cotejar_cola.py](cotejar_cola.py), con enteros y Fraction:

- n=1..128, 96 pasos: 12416 identidades y 12288 colas finitas,
  obtenidas también por recurrencia hacia atrás. Incluye ciclos.
- q=1..64: semillas mínimas, paridades, pronósticos y (8) exactos.
- m=1..128: aproximantes q_m, encierro de sqrt(2) mediante cuadrados
  racionales y residuos cero módulo 2^m.
- 129 pisos, 17 anillos por piso: suma y resto geométrico exactos
  de (9). El borde n=1, k=0, K=1 impide aplicar el piso infinito
  a cortes finitos. Estos cálculos no prueban existencia de cohetes.

[Resultado](cotejo_cola.json).

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_cola.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_cola.json
python -B -X utf8 depuracion/perdices20261007/cotejar_cola.py --nmax 128 --pasos 96 --qmax 64 --mmax 128 --salida depuracion/perdices20261007/cotejo_cola.json
```

Si faltan objetos previos, reproducir primero [Colisiones](COLISIONES.md).
