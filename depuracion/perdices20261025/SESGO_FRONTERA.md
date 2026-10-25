# Perdices: la ley condicionada no converge, ya módulo 3

25-10-2026. Continúa [Población protegida](PROTEGIDOS.md). Se conserva
Perdices; no se reclama prioridad bibliográfica. Esta nota sí estudia
la distribución real, mientras la nota anterior sólo limitaba una cota.

**Resultado escrito:** sea pi_K la ley de `T^K(U) mod 3`, con U uniforme
en `[0,2^K)` condicionado a `H_K: 3^S_j(U)>=2^j` para todo j<=K.
La sucesión pi_K **no tiene límite**. En particular no converge a la
ley estacionaria libre `nu_1=(0,1/3,2/3)` usada en Perdices.
Hay infinitos horizontes con `TV(pi_K,nu_1)>=1/36864`; de hecho, esos
horizontes tienen densidad inferior positiva.

No es una afirmación sobre los tiempos de una semilla fija ni una
refutación de la mezcla sin condicionamiento. No demuestra Collatz,
el reloj A/B ni la inexistencia de fugitivos. La formalización completa
y la revisión humana se distinguen de la prueba escrita al final.

## 1. Definiciones y ley exacta

Se usa el atajo T(n)=n/2 para pares y (3n+1)/2 para impares, sobre
enteros no negativos. K,j cuentan pasos T; `P_j=3^S_j/2^j`.
Una palabra de K paridades sobrevive si todos sus P_j>=1.
N_K es su número, y `s_K=min{s:3^s>=2^K}`. Por la biyección de
paridades, contar esas palabras equivale a la ley de semillas declarada.

Para K>=1, el primer bit de un superviviente es 1. Módulo 3, una
subida envía cualquier estado a 2 y una bajada intercambia 1 y 2.
Así pi_K=(0,p_K,1-p_K), donde p_K es la fracción con residuo 1,
y `TV(pi_K,nu_1)=|p_K-1/3|`. Una palabra termina en residuo 1
si y sólo si su racha terminal de ceros tiene longitud impar.

B_K cuenta los supervivientes de K bits con `1<=P_K<2`: sólo éstos
pierden la continuación 0. Si B_K>0, todos tienen exactamente s_K
unos, porque el intervalo `[2^K,2^(K+1))` contiene a lo sumo una
potencia de 3. R_K cuenta todos los supervivientes de residuo 1;
R^b_K cuenta los de residuo 1 dentro de la frontera.

## 2. Inyección en la frontera alta

Llamar **frontera alta** a los índices K con
`3/2<=3^s_K/2^K<2`. En ellos,

```text
2 R^b_K <= B_K.                                         (1)
```

Prueba: una palabra fronteriza de residuo 1 termina en `v 1 0^j`
con j>=1 impar. Enviarla a `v 0 1 0^(j-1)`. Conserva longitud,
número de unos y producto final, y pasa a residuo 2. El único prefijo
que podría perder supervivencia es `v 0`; su producto es
`P_K 2^j/3 >= (3/2)*2/3=1`. Los prefijos posteriores coinciden en
producto con los anteriores y los previos a v no cambian.
La transformación es inyectiva: la racha final de ceros de la imagen
determina j-1 y permite deshacer el intercambio. Esto prueba (1).

## 3. La pérdida de frontera obliga a una desviación real

Contar los hijos 0 y 1 da, para K>=1,

```text
N_(K+1)=2N_K-B_K,
R_(K+1)=N_K-R_K-B_K+R^b_K.
```

Con d_K=p_K-1/3 se obtiene la identidad

```text
N_K d_K + N_(K+1) d_(K+1) = R^b_K - 2B_K/3.            (2)
```

En frontera alta, el lado derecho es <=-B_K/6 por (1).
Como N_(K+1)<=2N_K, la desigualdad triangular implica

```text
max(|d_K|,|d_(K+1)|) >= B_K/(18N_K).                    (3)
```

Es una cota inferior de la TV real en al menos uno de dos horizontes,
no un piso de una estimación superior.

## 4. Una pérdida grande alcanza frontera alta en siete pasos

Siempre `s_(j+1)-s_j` es 0 o 1. Además

```text
s_(j+8)-s_j >= 5.                                      (4)
```

En efecto, por minimalidad `3^s_j<3*2^j`; si el incremento fuera <=4,
se tendría `3^s_(j+8)<3^5*2^j<2^(j+8)`, contradicción.
La desigualdad usada es 3^5<2^8; el caso j=0 también cumple el encaje.

Entre ocho incrementos que suman al menos cinco, alguno de los pares
disjuntos (1,2),(3,4),(5,6),(7,8) tiene dos unos. Existe entonces
h en {j+1,j+3,j+5,j+7} con
`s_h=s_(h-1)+1` y `s_(h+1)=s_h+1`. La primera igualdad da
`3^s_h/2^h>=3/2`; la segunda da `<2`. Es una frontera alta.

Si B_j>0, extender cada palabra fronteriza con los bits
`s_(i+1)-s_i` hasta h. Sus productos siguen siendo >=1 y termina
en la frontera h. Se trata de una inyección, con el mismo prefijo,
por lo que B_h>=B_j. Como cada palabra tiene a lo sumo dos hijos,
N_h<=2^(h-j) N_j. Por tanto

```text
B_j/N_j >= 1/16  ==>  B_h/N_h >= 1/2048,
max(|d_h|,|d_(h+1)|) >= 1/36864.                       (5)
```

No se altera una órbita individual: se construyen palabras distintas
dentro de la población cuya ley se está estudiando.

## 5. Hay suficientes pérdidas; la sucesión no converge

La prueba de [Población protegida, §4](PROTEGIDOS.md#4-ni-siquiera-elegir-l-adaptativamente-elimina-el-piso)
da al menos delta H índices K entre 1 y H con
`N_K/N_(K-1)<=31/16`, donde

```text
c=8^27/(5^17 3^10),
delta=1-log(c)/(27 log(31/16))>0.
```

Cada uno corresponde a un padre j=K-1 con B_j/N_j>=1/16.
Por (5) produce un horizonte t en [K,K+7] con TV>=1/36864.
Un mismo t puede proceder de a lo sumo ocho K. Luego entre 1 y H+7
hay al menos delta H/8 horizontes con esa desviación. Su densidad
inferior es al menos delta/8>0, y en particular

```text
limsup_(K->infinito) TV(pi_K,nu_1) >= 1/36864.           (6)
```

Falta excluir un límite diferente de nu_1. Hay un paso sin pérdidas
en cada grupo de tres pasos: como 3^2>2^3,
`s_(j+3)<=s_j+2`, y alguno de esos tres incrementos es cero.
Si `s_(K+1)=s_K`, B_K=0; entonces (2) da

```text
p_(K+1)=(1-p_K)/2.                                    (7)
```

Si p_K tuviera un límite p, la subsucesión infinita de pasos libres
obligaría p=(1-p)/2, es decir p=1/3. Esto contradice (6).
Por tanto pi_K no converge a **ninguna** ley fija módulo 3.
También se excluye convergencia a una ley fija módulo 3^m para cualquier
m>=1: proyectarla módulo 3 daría un límite de pi_K.

La oscilación también se ve entre horizontes vecinos. Si hay un paso
libre entre K y K+2, (7) y la desigualdad triangular dan
`|d_K|<=3 max_(K<=j<=K+2)|p_(j+1)-p_j|`.
Por (6), `limsup TV(pi_(K+1),pi_K)>=1/110592`.
Esta constante no pretende ser óptima.

## 6. Qué cambia en la investigación

La pregunta de Umbral sobre convergencia u oscilaciones de la ley bajo
H_K recibe una respuesta negativa a la convergencia. La comparación de
K=300 con nu_1 era pequeña, pero no podía justificar un límite; ahora
hay una obstrucción escrita que se aplica a horizontes arbitrariamente
grandes. La medición no se usa para probarla.

Esto cierra la propuesta específica de transferir **esa convergencia a
una ley fija** desde la población superviviente: la premisa es falsa.
Quedan posibles una familia de leyes dependiente de la fase/horizonte,
un promedio temporal de poblaciones o un argumento aritmético individual.
Ninguna de ellas se demuestra aquí; incluso con una ley poblacional
adecuada faltaría el puente hacia una semilla excepcional fija.

## 7. Evidencia y alcance formal

[Programa independiente](cotejar_sesgo.py), [resultado](cotejo_sesgo.json):
32767 palabras y 32767 enteros hasta K=14; 40 pares de la inyección;
159 identidades de residuos; 42 fronteras altas y 97 traslados con piso
hasta horizonte 160; siete distancias coinciden exactamente con la
evidencia anterior. Se usan enteros y Fraction. No se importan ni
ejecutan experimentos antiguos ni se amplía el censo A/B.

```powershell
python -B -X utf8 depuracion/perdices20261025/cotejar_sesgo.py --horizonte 160 --directo 14 --salida depuracion/perdices20261025/cotejo_sesgo.json
```

[Lean](PerdicesSesgoFrontera.lean), [evidencia](evidencia_lean_sesgo.json)
y [salida](evidencia_lean_sesgo.txt): once lemas recompilados desde fuente
con Lean 4.32.2 y sólo axiomas estándar, sin sorryAx. Cubren la seguridad
aritmética del intercambio, (2), (3), el piso trasladado, el paso libre,
los incrementos unitarios y de tres/ocho pasos, la existencia del par
adyacente, la frontera alta y la oscilación local. Imports directos
cotejados con Mathlib fijado; no auditoría transitiva completa.

[Extensión del intercambio](PerdicesIntercambio.lean),
[evidencia](evidencia_lean_intercambio.json) y
[salida](evidencia_lean_intercambio.txt): otras 26 consultas con sólo
axiomas estándar. Define supervivencia de todos los prefijos mediante
productos racionales y prueba su equivalencia con la definición recursiva.
Formaliza la descomposición por la última subida, el intercambio de listas,
la conservación de longitud, subidas y producto, el cambio de residuo,
la inyectividad y `2*card(clase 1)<=card(frontera alta)` para cualquier
longitud y número de subidas. La frontera alta exige explícitamente
`3/2<=producto<2`. La recurrencia de residuos es la inducida por las ramas
de paridad; su identificación con las órbitas naturales queda fuera del módulo.

**Tramo formal pendiente:** la extracción de cuentas desde las órbitas,
la densidad de horizontes y el teorema de no convergencia de la medida.
Estas partes tienen la prueba escrita anterior, no certificación Lean
completa. La revisión humana sigue pendiente.

```powershell
python -B -X utf8 depuracion/perdices20261025/comprobar_lean.py --lean C:/Users/Home/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean.exe --modulo PerdicesSesgoFrontera --salida depuracion/perdices20261025/evidencia_lean_sesgo.json
python -B -X utf8 depuracion/perdices20261025/comprobar_lean.py --lean C:/Users/Home/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean.exe --modulo PerdicesIntercambio --salida depuracion/perdices20261025/evidencia_lean_intercambio.json
```

El resultado se conserva como segunda [alta versionada](alta_registro.json),
con el alcance poblacional explícito y la [conservación del catálogo](evidencia_registro.json).
