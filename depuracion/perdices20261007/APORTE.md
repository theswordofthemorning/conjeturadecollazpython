# Perdices: aporte ponderado y límite del contador de excepciones

10-10-2026. Continuación de [Excepciones](EXCEPCIONES.md).

**Resultado:** el aporte de una cadena `110` se satura aunque crezca
su longitud. La cantidad que la neutraliza exactamente, `(x+5)/P`,
no es monótona entre regresos: hay excursiones reales con cambio
positivo, cero y negativo, certificadas en Lean. Una familia explícita
tiene E excepciones arbitrariamente grande y aporte normalizado
acotado, al variar la semilla. Por tanto, contar excepciones no permite
inferir por sí solo un progreso uniforme hacia el descenso.

## 1. Mapa y cantidades

Atajo `T(x)=x/2` para x par y `(3x+1)/2` para x impar, en naturales.
`x_j=T^j(n)`, `S_j` cuenta entradas impares con índice menor que j,
`P_j=3^S_j/2^j`, `I_j=1/P_j` y `R_j=x_j/P_j`. Los índices miden
pasos del atajo. No se usa una ley aleatoria.

Una excursión no unitaria u<v tiene extremos consecutivos bajo un
techo fijo `C=3^c`, y palabra `1^a_0 0^b_0 ... 1^a_(r−1) 0^b_(r−1)`.
Los inicios de bloque son τ_i=u+t_i; el último bloque par puede
estar truncado en v. E cuenta los bloques `(a_i,b_i)≠(2,1)`.
Las identidades siguientes valen para palabras reales sin suponer
una fuga pura infinita.

## 2. Aporte de un bloque y de una cadena completa

Para un bloque de longitudes a,b desde x hasta y y coeficiente inicial p,

```text
2^(a+b)y = 3^a(x+1)−2^a,
P_final = p·3^a/2^(a+b),
R_final−R_inicial = [1−(2/3)^a]/p.                  (1)
```

En particular, `0<ΔR<1/p`. La longitud par b no figura en este aporte,
pero cambia los coeficientes de los bloques siguientes. La identidad
orbital de Lean `carga_bloque`, especializada a desplazamiento cero,
da (1); el traslado conserva el origen n y el tiempo u.

Si hay k bloques consecutivos `110`, sus coeficientes crecen como
`p(9/8)^j`. Sumando geométricamente,

```text
ΔR = 5[1−(8/9)^k]/p < 5/p.                        (2)
```

Para k=0 el aporte es cero. Lean certifica la forma equivalente
`ΔR=5(I_inicial−I_final)` y su cota estricta, a partir de la
invariancia orbital que se prueba en §3. Así, una cadena larga no
puede tratarse como k aportes de tamaño uniforme.

Agrupar los bloques `110` en cadenas maximales no vacías. Si sus
inicios son σ_j y los inicios de excepciones son τ_i, (1)-(2) dan

```text
ΔR = Σ_cadenas 5[1−(8/9)^k_j]/P_σ_j
     + Σ_excepciones [1−(2/3)^a_i]/P_τ_i,
0<ΔR<5 Σ_cadenas 1/P_σ_j + Σ_excepciones 1/P_τ_i.   (3)
```

Hay a lo sumo E+1 cadenas. Todo inicio interior tiene P>C≥P_u;
por ello se deduce la cota escrita

```text
0<R_v−R_u < (6E+5)/P_u.                            (4)
```

(3)-(4), incluida la agrupación general, tienen prueba escrita y
cotejo independiente; no se presentan como un nuevo lema formal
de agrupación. Son cotas superiores: no se pueden invertir para
obtener un aporte mínimo proporcional a E.

## 3. Neutralizar 110 produce un balance con signo

Para un real λ definir `J_λ(j)=(x_j+λ)/P_j=R_j+λI_j`.
La identidad de un bloque da

```text
J_λ(final)−J_λ(inicio) = I_inicio · κ_λ(a,b),
κ_λ(a,b) = [3^a−2^a+λ(2^(a+b)−3^a)]/3^a.          (5)
```

Para `110`, `κ_λ(2,1)=(5−λ)/9`. Por tanto **λ=5 es el único
desplazamiento constante** que neutraliza exactamente ese bloque.
En ese caso

```text
κ_5(a,b) = [2^a(5·2^b−1)−4·3^a]/3^a,
J_5(v)−J_5(u) = Σ_excepciones κ_5(a_i,b_i)/P_τ_i.   (6)
```

`suma_excepciones` prueba (6) en Lean, incluida la composición desde
el origen n. `carga_cadena` certifica que cualquier cadena interior
110 deja J_5 exactamente constante. El signo de κ_5 depende de a,b;
no es el indicador de excepción ni tiene un signo fijo.

Tres excursiones consecutivas bajo **C=3** muestran los tres signos:

| n | u | v | Palabra de la excursión | ΔR | ΔJ_5 |
|---:|---:|---:|---|---:|---:|
| 7 | 2 | 4 | `10` | 4/27 | 8/9 |
| 15 | 2 | 5 | `110` | 20/81 | 0 |
| 63 | 2 | 8 | `111100` | 260/729 | −80/729 |

Lean certifica los extremos consecutivos y los cambios exactos de
J_5. El contraste directo verifica además que todos los coeficientes
del prefijo hasta v son ≥1. Son pruebas de condiciones **finitas**;
no se declara `FugaPura` para estas semillas.

Esto descarta la monotonicidad de J_5 basada sólo en esas condiciones
locales. No refuta una propiedad adicional que se consiguiera deducir
de una fuga infinita. R, por su parte, crece en los tres ejemplos y
no decide el cambio del valor real:

```text
x_v−x_u = P_v(R_v−R_u) + (P_v−P_u)R_u.             (7)
```

Por ejemplo, en n=7 el valor baja de 17 a 13 durante la excursión,
aunque ΔR>0. Sigue por encima de la semilla 7.

## 4. Muchas excepciones, aporte total acotado

La siguiente familia tiene prueba escrita para todo k≥3. Elegir b
mínimo con `27^k≤3·16^k·2^b`, y poner

```text
m = 19·(27^k)^(-1) mod (11·2^b),   0<m<11·2^b,
n_k = (16^k m−19)/11.                              (8)
```

El inverso existe porque 27 es coprimo con 11·2^b. Se tiene b≥1,
m impar, y n_k entero positivo: módulo 11, 27≡16, por lo que
`16^k m≡19`. Para 0≤j≤k,

```text
11x_(4j)+19 = 27^j 16^(k−j)m.                      (9)
```

Cuando j<k, x_(4j) es 7 módulo 16. Los pasos reales son
`16z+7 → 24z+11 → 36z+17 → 54z+26 → 27z+13`.
Esto prueba (9) por inducción. La elección de m hace que el último
valor sea divisible por 2^b; así, la palabra completa es
`(1110)^k 0^b`. Todos los coeficientes de ese prefijo son ≥1.

Bajo C=3, los últimos regresos consecutivos son

```text
u=8,    v=4k+b,    E=r=k−2,
P_u=(27/16)^2=729/256<3<(27/16)^3.                  (10)
```

Todas las rachas impares de esa excursión tienen longitud tres;
todos sus bloques son excepciones al patrón 110. Los pasos pares
adicionales no cambian R. La relación afín trasladada de (9) da

```text
R_v−R_u = (19/11)[(16/27)^2−(16/27)^k]
        < 4864/8019,
(R_v−R_u)/E → 0.                                   (11)
```

En términos de (3), `ΔR=(19/27)Σ_excepciones 1/P_τ_i`: los pesos
decrecen geométricamente. Por tanto ninguna cota `ΔR≥δE`, δ>0
uniforme en la semilla, se deduce de estas condiciones locales.

Las semillas varían: `11n_k+19≥16^k`. De hecho son los representantes
mínimos de sus palabras módulo `2^(4k+b)`: la identidad afín fija
una única clase, y (8) la realiza con `0<n_k<2^(4k+b)`.
La familia no constituye infinitos regresos de una misma semilla.
Su existencia general, minimalidad y límite (11) no están formalizados
en el módulo nuevo; se apoyan en las pruebas escritas anteriores.

## 5. Evidencia y decisión de ruta

[PerdicesAporte.lean](PerdicesAporte.lean) contiene quince lemas nuevos:
traslado de origen, identidad afín normalizada, desplazamiento único,
suma sobre excepciones, invariancia y aporte de cadenas, y ejemplos
de ambos signos. [comprobar_aporte.py](comprobar_aporte.py) compila
sólo este módulo y audita diecinueve previos sin recompilarlos:
veinte módulos, 192 consultas acumuladas. Lean 4.32.2, sólo axiomas
estándar, sin pruebas incompletas ni hipótesis externas en estos
enunciados. [Evidencia](evidencia_aporte.json), [salida](evidencia_aporte.txt).
Revisión humana pendiente.

[cotejar_aporte.py](cotejar_aporte.py) usa `Fraction`, órbitas directas
y una composición afín independiente para las clases residuales.
El [resultado](cotejo_aporte.json) contiene 223 excursiones no unitarias,
341 bloques y 59 cadenas: 172 cambios positivos de J_5, 44 nulos y
siete negativos. Semillas 2..512, hasta 256 pasos, c=0..4, sólo antes
del primer cruce. La familia usa k=3..128: 126 miembros y 8001 bloques.
Ningún barrido certifica universalidad o infinitud.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_aporte.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_aporte.json
python -B -X utf8 depuracion/perdices20261007/cotejar_aporte.py --n-max 512 --pasos 256 --nivel-max 4 --k-max 128 --salida depuracion/perdices20261007/cotejo_aporte.json
```

Si faltan objetos, reproducir primero [Excepciones](EXCEPCIONES.md#6-evidencia-y-límites-de-la-ruta).
No se reclama prioridad bibliográfica. Collatz, el planeador general,
el cohete y la grieta siguen abiertos.

**Decisión:** conservar el aporte ponderado exacto (3) y el balance
firmado (6); descartar el uso del contador E como sustituto de esos
aportes o de J_5 como cantidad monótona local. El siguiente trabajo
debe enlazar los pesos con la congruencia de **una misma semilla** a
través de varios regresos. Otra condición de abundancia por sí sola
no elimina la posibilidad pendiente.
