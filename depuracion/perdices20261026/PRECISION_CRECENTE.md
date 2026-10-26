# Perdices: qué aporta conservar todos los bits

26-10-2026. Examen del siguiente paso propuesto tras
[Límites reales](LIMITES_REALES.md). No introduce una solución ni una nueva
afirmación de cierre: desarrolla la representación exacta ya usada en
[Ventanas simultáneas, §5](../perdices20261007/congruencias_codex20261016/VENTANAS_SIMULTANEAS.md#5-lo-que-hay-que-conservar-frontera-entera-y-crt).

## 1. El levantamiento conserva la integridad

T es el atajo sobre naturales. Para una palabra w de L bits, S unos y
aditivo E, poner D=3^S y N=2^L. Su menor representante es

```text
r_L = -E*D^(-1) mod N,       0<=r_L<N,
z_L = T^L(r_L) = (D*r_L+E)/N.
```

No hay ley probabilística. Los índices cuentan pasos T y los residuos
son exactos. La equivalencia entre paridades y congruencias está en
[CasaRetrato](../casa20261004/CasaRetrato.lean), `misma_paridad_congruentes`,
y [CasaTerras](../casa20261004/CasaTerras.lean), `congruentes_mismo_baile`.

Para añadir el bit b hay exactamente dos candidatos módulo 2N:
r_L y r_L+N. Sus estados al cabo de L pasos son z_L y z_L+D.
Como D es impar, tienen paridades contrarias. Por tanto

```text
epsilon_L=(b-z_L) mod 2,
r_(L+1)=r_L+epsilon_L*2^L.                            (1)
```

No se pierde ninguna condición interior. Si se sigue una semilla fija n,
necesariamente r_L=n mod 2^L; epsilon_L es su bit de posición L.

En el testigo de 53 pasos que comienza por AAB, los cuatro primeros
bits prescritos son 1111. El 23 pasa los primeros tres, pero r_3=7 y
r_4=15, mientras 23 mod 16=7. Falla ya el cuarto bit. El representante
6416623 sí pasa todos. Así, (1) supera el testigo racional, pero es la
misma condición exacta de cilindro que ya estaba disponible.

## 2. Dónde reaparece la obligación pendiente

Para una palabra infinita admisible en {1,110}, sus r_L son no decrecientes.
El límite 2-ádico es un natural si y sólo si sólo hay un número finito
de epsilon_L iguales a 1. En tal caso r_L se estabiliza en ese natural.
Como el primer bit es 1, ese natural sería positivo.

Por tanto pedir que **cada palabra infinita admisible obligue a seguir
añadiendo bits iguales a 1** es exactamente excluir una semilla positiva
que persista. No es todavía un control que pruebe esa exclusión.

Hay otra forma finita de ver el mismo punto. Sea m_L el menor representante
entre todos los prefijos admisibles de longitud L. Son conjuntos finitos
no vacíos; m_L>=1 y m_(L+1)>=m_L por (1). Entonces

```text
toda semilla positiva sale de A/B <-> m_L tiende a infinito.
```

Si m_L quedase acotado, por ser una sucesión no decreciente de enteros se
estabilizaría en algún n. Ese mismo n realizaría un prefijo admisible
en cada longitud; sus paridades únicas serían una palabra infinita
admisible. La recíproca es inmediata: una semilla persistente n da
m_L<=n para todo L.

El **reloj uniforme** exige más: existen C,D con

```text
L<=C*ceil(log2(m_L+5))+D       para todo L>=1.          (2)
```

Es equivalente al reloj de todas las semillas porque cualquier otra
semilla que realice un prefijo de largo L es >=m_L. En particular, no
basta probar m_L creciente: puede tener mesetas, y aún falta demostrar
que sale de cada una. Tampoco la terminación sola proporciona (2).

Si j es la última posición de un bit 1 de r_L, se tiene
2^j<=r_L<2^(j+1), de donde

```text
j+1 <= ceil(log2(r_L+5)) <= j+3.
```

Una cota lineal que fuerce un bit nuevo suficientemente cerca del final
es, salvo esas constantes, el propio reloj. Llamarla presupuesto de bits
o de acarreos no aporta por sí solo una desigualdad nueva.

## 3. Resultado de la propuesta

Conservar precisión creciente es necesario para reconstruir cada
trayectoria y rechaza efectivamente al 23. **No se obtuvo una estimación
adicional sobre cuándo aparece el siguiente bit 1.** El levantamiento
exacto, las congruencias simultáneas y la reconstrucción CRT expresan
la misma restricción, no tres restricciones independientes.

El [peso binario](PESOS_BINARIOS.md) tampoco suministra un rango monótono
por lotes fijos. Una dependencia de la colocación completa de los bits
o del pasado exigiría proponer y demostrar otra desigualdad. Su mera
posibilidad no constituye un método pendiente de ejecutar.

Este examen no satisface la primera condición primordial: conserva
integridad, pero el control cuantitativo sigue siendo el reloj reescrito.
No refuta que pueda encontrarse otro control de precisión creciente.
Las identidades anteriores son consecuencias escritas de la biyección
ya formalizada; no se añade otra formalización ni otro censo.
