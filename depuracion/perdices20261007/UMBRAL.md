# Perdices: frontera, reserva y alcance contra el fugitivo

Continuación del 07-10-2026. [Acoplamiento previo](LEEME.md),
[formalización](PerdicesAcoplamiento.lean),
[cotejo independiente](cotejar_umbral.py), [salida exacta](cotejo_umbral.json).

## Qué pieza añade a la casa

El supuesto fugitivo puro cumple `P_j=3^S_j(n)/2^j >= 1` para todo j.
Si `1<=P_j<2`, su siguiente paso debe ser impar: una bajada lo haría
cruzar. En cambio, desde un prefijo con k pasos y s subidas, **todas**
las continuaciones de L pasos sobreviven si y sólo si `3^s>=2^(k+L)`.
Ésta es una equivalencia universal, no una observación de un barrido.

Con la rareza de tiempos bajos ya demostrada en CasaPlaneador, se
deduce que, para cada L fijo, un fugitivo tendría esa reserva en una
proporción de tiempos que tiende a uno. Es una restricción sobre el
mismo entero y también un límite de este ataque: la condición de no
cruzar por sí sola deja de prohibir palabras en esas ventanas. No dice
que el fugitivo elija sus bits al azar, ni que podamos cambiar su órbita.

## Mapa, dominio y condicionamiento

Usamos `T(n)=n/2` si n es par y `(3n+1)/2` si es impar, en naturales.
`S_j(n)` cuenta impares entre `n,...,T^(j-1)(n)`. El tiempo y las longitudes
se miden en pasos del atajo; el pronóstico P es adimensional.

`H_k` exige `P_j>=1` para **cada** `0<=j<=k`. La ley real considerada es
la de `T^k(U) mod 3^m`, con U uniforme entre los representantes de
`[0,2^k)` que cumplen H_k. No es una ley temporal de una órbita fija.

Para las cuentas, una palabra binaria w empieza la cadena artificial
en cero: `C_empty(0)=0`, `f_0(x)=x/2`, `f_1(x)=(3x+1)/2` módulo `3^m`.
Dividir por 2 significa multiplicar por su inverso modular. Sea
`D_k(s,x)` el número de palabras de longitud k, vivas en cada prefijo,
con s unos y salida x. La biyección de CasaCadena identifica las palabras
con los representantes enteros. Las salidas artificiales y reales
coinciden para cada palabra con `s>=m`; en particular sus leyes completas
coinciden si el mínimo s entre supervivientes es al menos m. El informe
marca explícitamente cuándo se cumple esa condición.

## Recurrencia y corrección exacta de frontera

Inicialmente `D_0(0,0)=1`. Cada estado `(s,x)` con cuenta c añade c a
`D_(k+1)(s+b,f_b(x))` si `3^(s+b)>=2^(k+1)`, para b=0,1. Como el padre
ya cumple `3^s>=2^k`, la rama b=1 siempre sobrevive. Sólo se prohíbe la
rama b=0 de la **frontera** `2^k<=3^s<2^(k+1)`.

Sean N el número de padres, B el de padres en la frontera, F el vector
de las 2N salidas sin prohibiciones y E el vector de las B bajadas
prohibidas. Entonces

```
D_(k+1)(x) = F(x)-E(x),    N_(k+1)=2N-B.
```

Si p es la ley superviviente del paso nuevo, Q=F/(2N) la ley sin borrar
y e=E/B la ley eliminada, con `epsilon=B/(2N)`, la descomposición exacta es

```
Q = (1-epsilon)p + epsilon e,
TV(p,Q) = epsilon TV(p,e) <= epsilon <= 1/2.
```

Aquí TV es media suma absoluta. Si B=0, p=Q y no se define e. La
identidad surge de contar ambas clases de hijos, y la igualdad de TV
de restar los vectores y tomar valores absolutos. Es prueba escrita
de cuentas y probabilidades; la recurrencia completa no está formalizada
en Lean. El script verifica sus identidades racionales en cada paso.

## Reserva de un bloque y una cota adaptada

`Admisible k s w` exige que el estado inicial y todos los prefijos de
w cumplan la desigualdad del pronóstico. Lean prueba la composición
por concatenación y el puente exacto con las palabras de órbitas reales.
También prueba

```
(para toda w de longitud L, Admisible k s w) <=> 2^(k+L)<=3^s.
```

Para la suficiencia, después de j pasos el pronóstico es al menos
`(3^s/2^k)/2^j>=1`, cualquiera que sea el número de subidas. Para la
necesidad basta escoger L ceros. Si el prefijo ya sobrevivía, cada
continuación protegida tiene un representante entero superviviente;
el representante puede variar con la continuación y el horizonte.

Fijemos un horizonte K y un bloque terminal de longitud `1<=L<=K`.
Sea A el número de prefijos supervivientes de longitud K-L con
`3^s>=2^K`, y N_K el número total de supervivientes de longitud K.
Cada uno de esos A prefijos admite exactamente `2^L` continuaciones.
Su fracción entre supervivientes finales es `G=A*2^L/N_K`.

Dentro de esa parte, los sufijos son uniformes. El acoplamiento previo
admite que el arranque dependa de la palabra, así que también sirve
para el valor real al inicio del bloque. Con `nu_m` estacionaria y
`q(L,m)=2^(-L)*sum_(0<=j<m,j<=L) binom(L,j)`, obtenemos

```
TV(ley(T^K(U) mod 3^m | H_K), nu_m) <= G*q(L,m)+(1-G).
```

La prueba divide la ley en la parte protegida, con error a lo sumo q,
y su complemento, con error a lo sumo 1, y aplica convexidad de TV.
Si A=0 sólo afirma TV<=1, sin condicionar a un evento vacío. N_K es
positivo porque la palabra de K unos sobrevive. Ésta es una prueba
escrita; la construcción de medidas y la cota de TV no están formalizadas.

El precio del condicionamiento aparece explícito en `1-G`. La cota
es válida, pero amplia: con K=300, módulo 3, el mejor L entre 1 y 24
es 2 y da aproximadamente 0,3754, frente a una TV exacta aproximada
de 0,007048. Módulo 27, L=6 da 0,7582 frente a 0,04569. El barrido
por sí solo no decide el límite. La [continuación del 25-10](../perdices20261025/SESGO_FRONTERA.md)
demuestra después, por una inyección y conteo universales, que la ley
condicionada no converge a ninguna ley fija, ya módulo 3.

## Puente determinista con el planeador

Para un entero fijo n y una longitud L, definamos

```
B_L(K) = #{j<K : 3^S_j(n) < 2^(j+L)}.
```

Cuenta los tiempos que no tienen reserva para todas las palabras de
longitud L. `cuenta_sin_reserva`, en Lean, prueba su inclusión en
`{j<K : 3^S_j(n)<=3^L*2^j}`, usando `2^L<=3^L`.

Para un fugitivo puro, el teorema existente
[`CasaPlaneador.tiempos_bajos_mul`](../casa20261004/CasaPlaneador.lean)
da, por esa inclusión y para todo r natural,

```
B_L(K)*16^r <= 6^L*(n+K) + 2^L*2^(100r).
```

Asimismo, `tiempos_bajos_raros`, con c=L, implica `B_L(K)/K -> 0` para
L fijo. Incluso permite ventanas crecientes en horizontes concretos:
si `L=r`, `K=2^(100r)` y `n<=K`, entonces

```
B_r(K)/K <= 2*(3/8)^r + (1/8)^r.
```

La última desigualdad se obtiene sustituyendo y dividiendo por K16^r.
Es un corolario escrito de los lemas certificados; no se ha compilado
su composición como un único teorema. CasaPlaneador usa la implementación
vigente y Perdices la recuperada: sus módulos Casa no se mezclan en
una misma caché. Ambos usan la misma S de Ocelotas.

Esto se aplica a un solo fugitivo hipotético, cohete o planeador
intermitente. No impone una distribución uniforme a sus bloques ni
asegura descenso. La continuación [tamaño y regresos](TAMANO.md) usa
el **mismo entero positivo**: combina la rareza con la identidad afín
para probar `T^k(n)/P_k=o(k)` en Lean. Una segunda vía, por el producto
y la inyectividad, da una cota de sexta raíz con prueba escrita;
su ordenación y telescopio quedan pendientes de formalizar.

## Continuación de la rama probabilística

**Actualización del 25-10-2026:** [Población protegida](../perdices20261025/PROTEGIDOS.md)
demuestra `G(K,L)<=K(K+1)(3/4)^L`. Si
`L>=8*ceil(log2(K+1))`, el certificado `F=1-G(1-q)` es al menos
`1-1/(K+1)`. Además, F>=1/31 para todas las longitudes simultáneamente
en una proporción positiva de horizontes. Así, elegir L adaptativamente
no hace que este certificado tienda a cero en todos los horizontes.
Es una barrera de la **cota superior**, no una cota inferior de la TV
real ni una refutación de la mezcla. Prueba escrita, contraste exacto
y formalización parcial con alcance explícito en la nota.

Un argumento adicional en [Sesgo de frontera](../perdices20261025/SESGO_FRONTERA.md)
sí controla la TV real: `limsup TV(pi_K,nu_1)>=1/36864`, en una
proporción positiva de horizontes. Los pasos libres obligarían a que
cualquier límite fuese nu_1; por tanto pi_K no converge a ninguna ley
fija, tampoco tras pasar a módulos 3^m. Ley poblacional bajo H_K;
no se afirma nada equivalente para los tiempos de una semilla fija.

La prioridad inmediata es el [plan determinista de tamaño](TAMANO.md#qué-debe-aportar-el-siguiente-paso),
porque restringe un entero fijo. Esta rama queda como continuación:

1. Formalizar las medidas finitas, la corrección exacta de frontera
   y la cota `TV<=G*q+(1-G)`. Distinguir la ley sobre representantes
   uniformes condicionada por H_K de los tiempos de una sola órbita.
2. La estimación de G y la pregunta de convergencia a una ley fija ya
   tienen las respuestas anteriores. Una continuación tendría que
   estudiar leyes dependientes del horizonte, promedios u otro
   condicionamiento; no repetir la búsqueda de esa convergencia falsa.
3. Antes de usar esa mezcla contra un fugitivo, demostrar un puente
   que controle sus bloques concretos. Tener reserva para todas las
   continuaciones no implica que su órbita las elija uniformemente.
   El contraejemplo `1/6>1/8` sigue siendo un control obligatorio para
   cualquier propuesta que herede la cota sin condicionamiento.

El [criterio temporal del 25-10](../perdices20261025/FRECUENCIAS_TEMPORALES.md)
precisa una implicación: con K>=163, TV<=1/100 entre las frecuencias de
una misma órbita módulo 9 y nu_2 fuerza `3^S_K<2^K`. El criterio desde
tres cotas marginales está formalizado. No se demuestra la hipótesis
para fugitivos; tampoco es la ley poblacional pi_K. El balance modular
admite el recorrido racional de 23, así que no resuelve la integridad A/B.
La [extensión a todo m](../perdices20261025/OBSERVABILIDAD_TERNARIA.md)
formaliza el balance orbital general y precisa la ambigüedad de la clase
`(3^m-1)/2`. El control aritmético de sus frecuencias sigue pendiente.

El entregable de esta rama sería una estimación con su ley e hipótesis
explícitas. Sólo contribuiría a excluir un fugitivo si además se
demuestra ese puente individual; la mezcla de una población no basta.

## Validación y alcance formal

Se añadieron 11 consultas Lean: inicio y final de Admisible, concatenación,
reserva suficiente, equivalencia para todas las continuaciones, puente
con la órbita, caracterización de los representantes supervivientes,
realización de bloques protegidos, rama impar permitida, obligación
impar del fugitivo en la frontera e inclusión de tiempos sin reserva.
El módulo tiene ahora 27 consultas y su cierre 123, todas con axiomas
estándar en Lean 4.32.2. Véase [evidencia](evidencia_acoplamiento.json).

El contraste exacto separado comprende 300 identidades de frontera,
20 772 cotas de bloques, 8191 enteros enumerados hasta horizonte 12,
2025 sincronizaciones y 91 cuentas de continuaciones protegidas.
Además, el criterio de reserva se verifica mediante productos Fraction
en 648 triples `(k,s,L)` y 20 655 palabras, incluyendo L=0 y estados
inicialmente muertos. Se ejecutó también el borde de parámetros
`m=1, pasos=1, directo=0, bloque=1`.

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_umbral.py --m-max 3 --pasos 300 --directo 12 --bloque-max 24 --salida depuracion/perdices20261007/cotejo_umbral.json
```

Los contrastes son finitos y no sustituyen los argumentos universales.
Los muros A y B permanecen abiertos; este bloque precisa el sesgo del
condicionamiento y su alcance, sin excluir una nueva especie de fugitivo.
