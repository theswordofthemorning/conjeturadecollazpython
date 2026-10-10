# Perdices: balance par, congruencias y excursiones interiores 110

10-10-2026. Continuación de [Ritmo](RITMO.md).

**Resultado:** el presupuesto que conserva todas las longitudes pares
ya está enlazado con la excursión real en Lean. Una familia exacta muestra
que esas longitudes pueden ser mínimas en todos los bloques interiores,
con la compensación par al final, al cambiar la semilla. En cambio,
una misma fuga pura con infinitos regresos no puede tener todas sus
excursiones tardías de la forma `(110)^(h−1) 11 0^b`, aunque h no esté
acotado. Esta última exclusión también está formalizada.

## 1. Mapa y alcance

Se conserva el atajo T: dividir por dos en una entrada par y aplicar
`(3x+1)/2` en una impar, con n natural. `x_j=T^j(n)`, `S_j` cuenta
entradas impares anteriores a j y `P_j=3^S_j/2^j`. Los índices miden
pasos del atajo. No se introduce ninguna ley aleatoria.

Un regreso al techo fijo `C=3^c` satisface `P_j≤C`. Los extremos u<v
son consecutivos si no hay regreso interior. Para una excursión no
unitaria, la palabra de entradas es `1^a_0 0^b_0 ... 1^a_(h−1) 0^b_(h−1)`
con longitudes positivas. Sea x=x_u, t_i el tiempo local al comienzo
del bloque i, s_i la suma de longitudes impares anteriores y e_i la
suma par anterior: `t_i=s_i+e_i`. El último bloque par puede estar
truncado en v.

El presupuesto de §2 sólo requiere una órbita y regresos consecutivos.
La exclusión de §4 exige además **FugaPura n**, `P_j≥1` para todo j,
e infinitos regresos, siempre con la misma n y el mismo c.

## 2. Presupuesto orbital con las longitudes pares

Poner `y_i=x_(u+t_i)`. Las dos identidades afines de un bloque dan

```text
2^(a_i+b_i)(y_(i+1)+1) + 2^a_i
  = 3^a_i(y_i+1) + 2^(a_i+b_i).                    (1)
```

Si `2^t_j≤3^s_j` en los extremos de bloque hasta i, una inducción
entera usando (1), multiplicada por `2^t_i`, prueba

```text
2^t_i(y_i+1) ≤ 3^s_i(x+1+i).                       (2)
```

En el paso inductivo, el término añadido `2^t_(i+1)` es a lo sumo
`3^s_(i+1)`; el término positivo restado puede descartarse para esta
cota. Esta derivación evita división y conserva t_i completo.

Para j interior a la excursión, `P_(u+j)>C≥P_u`, luego el coeficiente
local `3^(S_(u+j)−S_u)/2^j` es mayor que uno. Así se justifica la
hipótesis de (2) en todos los comienzos de bloque i<h. La congruencia
`2^a_i | y_i+1`, con y_i+1>0, entrega

```text
2^(s_(i+1)+e_i) ≤ 3^s_i(x+1+i),   0≤i<h.           (3)
```

`presupuesto_excursion` formaliza (3), incluida la condición interior.
No se impone un coeficiente local ≥1 al extremo final. El telescopado
racional de [Ritmo, §5](RITMO.md#5-qué-aportan-exactamente-las-longitudes-pares)
conserva su prueba escrita; su consecuencia entera (3) ya está en Lean.

## 3. Familia exacta: pares interiores mínimos y compensación final

La familia prolonga los bloques `110` de
[Jinetas](../jinetas20261010/RACHAS.md#4-bordes-que-debe-superar-cualquier-propuesta).
Para cada k≥10 elegir b mínimo tal que

```text
9^k ≤ 3·8^k·2^b,
m = 5·(9^k)^(-1) mod 2^b,    1≤m<2^b,
n_k = 8^k m − 5.                                   (4)
```

El inverso existe porque 9 es impar. Se tiene b≥1 y m impar. La
órbita comienza con `(110)^k 0^b`: en los extremos de los bloques,

```text
x_(3j)+5 = 9^j 8^(k−j)m,       0≤j≤k.              (5)
```

Para j<k, el valor es 3 módulo 8. Tres pasos directos dan
`8z+3 → 12z+5 → 18z+8 → 9z+4`, que prueba (5) por inducción.
Los extremos con j<k son impares. Al final, la elección modular de m
hace que `x_(3k)=9^k m−5` sea divisible por `2^b`, justificando los
b pasos pares adicionales.

Los coeficientes de cada bloque son `(9/8)^j`, `3(9/8)^j/2` y
`9(9/8)^j/4`. Después se dividen por dos. Todos los coeficientes de
este prefijo son ≥1. Bajo **C=3**, los dos últimos regresos son

```text
u=27,       v=3k+b,       h=k−9.                    (6)
```

En efecto, `(9/8)^9=387420489/134217728<3`, mientras
`(9/8)^10>3`; después del tiempo 27 los interiores de los bloques
también superan 3. La minimalidad de b deja el primer regreso de la
cola exactamente en v, con `3/2<P_v≤3`.

La excursión de (6) es

```text
(110)^(h−1) 11 0^(b+1).
```

Todos sus bloques pares interiores tienen longitud uno, y en sus
comienzos `s_i=2i`, `e_i=i`. Hay tantas rachas impares como se quiera.
Así se descarta una supuesta mejora uniforme `e_i≥θs_i−K` con θ>1/2
y K independiente de la semilla: eligiendo un i grande falla dentro
de una excursión real. En particular, el techo interior no fuerza por
sí solo el equilibrio `θ=log2(3)−1` en cada prefijo de bloques.

| k | b | h | u | v | Último bloque par |
|---:|---:|---:|---:|---:|---:|
| 10 | 1 | 1 | 27 | 31 | 2 |
| 16 | 2 | 7 | 27 | 50 | 3 |
| 32 | 4 | 23 | 27 | 100 | 5 |
| 64 | 10 | 55 | 27 | 202 | 11 |
| 128 | 21 | 119 | 27 | 405 | 22 |

La familia cambia n. Además `n_k≥8^k−5` y
`x_27+5=9^9 8^h m`, por lo que también aumenta mucho la entrada.
No proporciona una órbita infinita sin cruce. El número n_k es incluso
el representante mínimo no negativo de su palabra completa: ésta
impone una única congruencia módulo `2^(3k+b)` por su identidad afín,
y la construcción la realiza con `0<n_k<2^(3k+b)`.

La existencia de la familia para todo k y su minimalidad tienen
prueba escrita aquí; el cotejo finito no reemplaza esa prueba. No se
han formalizado en el módulo nuevo.

## 4. Lo que cambia al conservar la misma órbita

Llamamos **regular** a un intervalo de duración uno o a una palabra
`(110)^(h−1) 11 0^b`, con h,b≥1. No se fija ni se acota h ni b.
El predicado `Regular x d` de Lean recibe la palabra real de duración d.

Cada bloque interior `110` satisface

```text
8(y_(i+1)+5)=9(y_i+5).
```

Al iterar los h−1 bloques interiores y usar coprimalidad:

```text
8^(h−1)(y_(h−1)+5)=9^(h−1)(x+5),
8^(h−1) | x+5,
8^(h−1) ≤ x+5,   h≤x+5.                            (7)
```

El módulo prueba también la versión abstracta: si
`M z_(i+1)=A z_i` y `gcd(M,A)=1`, entonces `M^r | z_0`.
En (7), x+5 es positivo; no se deduce una cota a partir de dividir cero.

Hay exactamente 2h entradas impares. Desde un regreso de la fuga pura,
la casi fuga da `2^d≤3^(c+2h)≤2^(2c+4h)`. Así, usando x≥1:

```text
d≤4h+2c≤(24+2c)x,
d²≤(24+2c)²(Cn)^6(u+1).                            (8)
```

La última desigualdad usa `x²≤x^6≤(Cn)^6(u+1)`.
Para d=1, (8) vale directamente. Por escrito también se tiene la
cota más precisa `d≤4+(4/3)log2(x+5)+2c`, pero no hace falta
formalizar logaritmos para cerrar el argumento.

Si todas las excursiones de una cola fueran regulares, (8) impondría
el reloj cuadrático ya certificado, incompatible con la cuenta de
regresos. `infinitos_exigen_irregulares` prueba en Lean:

```text
FugaPura n ∧ InfinitosRegresos n c
 ⇒ ∀U, ∃u v, U<u ∧ Consecutivos n c u v
                  ∧ ¬Regular(x_u,v−u).             (9)
```

Por tanto hay excursiones tardías con alguna racha impar distinta de
dos, o con algún bloque par interior distinto de uno. (9) no obliga
a que crezca el número de esas excepciones dentro de una excursión.
La familia de §3 satisface (7); no contradice (9) porque varía n.

## 5. Verificación y siguiente acción

[PerdicesBalance.lean](PerdicesBalance.lean): trece lemas nuevos, incluidos
el balance entero, el presupuesto orbital y (9).
[comprobar_balance.py](comprobar_balance.py) audita diecisiete módulos
previos sin recompilarlos y compila sólo éste: dieciocho módulos,
165 consultas acumuladas y trece nuevas. Lean 4.32.2; sólo axiomas
estándar, sin pruebas incompletas ni hipótesis externas de LMN o Rhin
en estos enunciados. [Evidencia](evidencia_balance.json),
[salida de Lean](evidencia_balance.txt). Revisión humana pendiente.

[cotejar_balance.py](cotejar_balance.py) contrasta órbitas directas,
congruencias afines calculadas por otra implementación y `Fraction`.
El [resultado](cotejo_balance.json) contiene 4737 intervalos (4514
unitarios, 49 regulares no unitarios y 174 irregulares), 341 bloques,
119 miembros de la familia k=10..128 y 7140 bloques dentro de ella.
Los controles orbitales generales usan semillas 2..512, hasta 256
pasos, c=0..4 y sólo el prefijo anterior al primer cruce.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_balance.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_balance.json
python -B -X utf8 depuracion/perdices20261007/cotejar_balance.py --n-max 512 --pasos 256 --nivel-max 4 --k-max 128 --salida depuracion/perdices20261007/cotejo_balance.json
```

Si faltan objetos, reproducir antes [Ritmo](RITMO.md#6-evidencia-límites-y-continuación).
No se afirma prioridad bibliográfica ni una prueba de Collatz.
El planeador general, el cohete y la grieta continúan abiertos.

**Siguiente:** comprimir cada cadena consecutiva de bloques `110`
usando (7) y estudiar cuántos bloques que rompen ese patrón son
necesarios entre regresos. La pregunta pendiente es si también queda
excluido un número uniformemente acotado de excepciones, manteniendo
la semilla, el techo y las entradas intermedias de la misma órbita.
