# Perdices: cruzar la sexta raíz con la cuenta de casi fugitivos

10-10-2026. Ejecución del paso 3 de [Tamaño](TAMANO.md), después de
la [auditoría de rachas de Jinetas](../jinetas20261010/RACHAS.md).

**Resultado:** para una misma hipotética fuga pura y un techo fijo,
la cuenta de regresos mejora de `O(K^(1/6))` a `O(K^(4/25))`, con
constantes explícitas. `4/25=0,16` frente a `1/6≈0,1667`. La cota
entera permite conservar la mejor entre ambas, sin aproximar raíces.
Esto certifica la combinación que ya se había estimado por escrito;
no excluye infinitos regresos muy separados ni una fuga pura.

Se mantiene el nombre Perdices. No se afirma prioridad bibliográfica:
son consecuencias de la sexta raíz y del conteo ya presentes en el
repositorio, con el cambio de intervalo y las constantes desarrollados.

## 1. Mapa, dominio y condicionamiento

Mapa atajo `T(n)=n/2` para n par y `(3n+1)/2` para n impar.
`x_j=T^j(n)`, `S_j` cuenta entradas impares en los índices `0,…,j−1`
y `P_j=3^S_j/2^j`. Una unidad temporal es un paso de T.

Se supone **FugaPura n**, es decir, `P_j≥1` para todo j. De esa
hipótesis se deducen n≥2, ausencia de descenso e inyectividad de
la órbita. No se demuestra que exista ningún n con esa propiedad.
Todos los cuantificadores siguientes conservan ese mismo n.

Para c,K naturales, sea C=3^c y

```text
F(n,c,K) = #{j<K : P_j≤C}.
Q=(C n)^6 K;
X=⌊Q^(1/6)⌋, es decir X^6≤Q<(X+1)^6.
```

No hay ley probabilística ni independencia supuesta. Las potencias,
raíces enteras, cardinales y divisiones enteras se calculan exactamente.
Los techos son 3^c; la cota previa de sexta raíz sí admitía C real.
Para otro techo fijo C≥1 se puede escoger c con C≤3^c, a costa de
debilitar las constantes. No se afirma que éstas sean uniformes en n o c.

## 2. La combinación conserva el techo y la semilla

Si j<K y P_j≤C, la [sexta raíz](PerdicesSexta.lean) da

```text
x_j^6 ≤ C^6 n^6 (S_j+1) ≤ (C n)^6 K = Q.
```

Por tanto `1≤x_j≤X`. El extremo superior se incluye: para aplicar
una cuenta sobre `0≤v<N` se debe usar **N=X+1**, no X.

Además, para todo i≥0 la composición de coeficientes da

```text
P_i(x_j) = P_(j+i)(n)/P_j(n) ≥ 1/C.
```

Así, cada x_j contado es un casi fugitivo de **nivel C=3^c** en el
sentido de [PerdicesEstela](PerdicesEstela.lean), `CasiFuga c x_j`.
La inyectividad convierte la cuenta de tiempos en una cuenta de
valores distintos del intervalo `0,…,X`. No se aumenta el nivel
al trasladar la órbita ni se elige otra semilla al aumentar K.

Para todo m≥0, `cuenta_casi_fugas` entrega

```text
F(n,c,K) ≤ B_m(X,c)
        := (⌊(X+1)/2^(100m)⌋+1) · 2^(c+96m).       (1)
```

Esta es la cota nueva exacta, combinable con las dos elementales:

```text
F(n,c,K) ≤ min(K, X, B_m(X,c)).                      (2)
```

Se puede minimizar sobre m. Basta probar
`0≤m≤⌊log2(X+1)/100⌋+1`: después de ese último valor el cociente
entero ya es cero y `B_m=2^(c+96m)` crece estrictamente. El
cotejador incluye también un candidato redundante en algún borde.

## 3. Exponente espacial y temporal, sin constantes ocultas

Escribir N=X+1≥1 y elegir m con

```text
H=2^(100m)≤N<2^100 H.
```

Multiplicando (1), la división entera se elimina:

```text
F·16^m ≤ 2^c(N+H) ≤ 2^(c+1)N.
```

Elevar a 25 usa `(16^m)^25=H`. Multiplicar por `N≤2^100 H`
y cancelar N>0 demuestra

```text
F^25 ≤ 2^(25c+125) N^24.                           (3)
```

Es la cota espacial `F≤32·2^c N^(24/25)`. El 32 es conservador:
se eligió para obtener un certificado entero sencillo, no como óptimo.

Si K≥1, n≥2 implica Q≥1 y X≥1. Por ello
`N≤2X` y `N^6≤2^6 Q`. Elevar (3) a la sexta y sustituir da

```text
F(n,c,K)^150 ≤ 2^(150c+894) · (3^c n)^144 · K^24.   (4)
```

La constante 894 es `6·125+24·6`. Para n,c fijos, (4) equivale a

```text
F(n,c,K) ≤ 2^(c+149/25) (3^c n)^(24/25) K^(4/25).   (5)
```

Los exponentes racionales de (5) sólo explican la escala; (4) es la
forma certificada con naturales. K=0 se trata aparte: F=0, y (4)
sigue siendo cierta. `radio_existe` prueba que siempre existe un X
con las dos desigualdades de raíz, sin asumir cálculos en flotantes.

## 4. Qué mejora y desde cuándo

El exponente pasa de `1/6` a `4/25`: la diferencia es **1/150**.
La expresión (5) mejora estrictamente la expresión previa
`3^c n K^(1/6)` cuando

```text
K > 2^(150c+894)/(3^c n)^6.                         (6)
```

Es una comparación entre las dos expresiones superiores, no una
afirmación sobre el valor real de F. El umbral es enorme. La cota
entera (2) puede mejorar antes, porque evita pérdidas al redondear
la escala y al sustituir N por 2X.

Ejemplo de **evaluación numérica de las expresiones**, con n=7 y c=1
(7 no es una fuga pura):

| K | Radio X de la sexta raíz | Mejor B_m | Cota conservada |
|---|---:|---:|---:|
| 64 | 42 | 88, m=0 | 42 |
| 2^600 | 21·2^100 | 44·2^96, m=1 | 44·2^96 |
| 2^1200 | 21·2^200 | 44·2^192, m=2 | 44·2^192 |

No se siguieron órbitas durante esos tiempos: se evaluaron potencias
enteras y las fórmulas. El [cotejo](cotejo_cruce.json) conserva sus
valores completos.

Bordes: K=0 tiene cuenta cero; se admite m=0; las igualdades en
potencias sextas se incluyen correctamente. Con c=0, bajo FugaPura,
P_j≤1 exige P_j=1; la coprimalidad de 2 y 3 sólo permite j=0.
Ese borde tiene una cota mucho mejor, F=1 para K≥1, por observación
escrita; no se vende (5) como óptima. La órbita de 1 no satisface
FugaPura y no puede introducirse en el lema de sexta raíz.

## 5. Formalización y auditoría de dependencias

[PerdicesCruce.lean](PerdicesCruce.lean) formaliza nueve enunciados:
existencia del radio, inclusión orbital en el intervalo, cuenta mixta,
eliminación de la división, existencia de escala, exponente espacial,
su aplicación a regresos, mínimo de cotas y exponente temporal (4).
El enlace con la órbita usa los teoremas de PerdicesSexta y
PerdicesEstela; no se deja como hipótesis una función de conteo abstracta.
Se mantiene explícita la hipótesis global FugaPura.

Se incorpora como dependencia el cierre local de la sexta raíz del
07-10: [fuente](PerdicesSexta.lean), [comprobador](comprobar_sexta.py),
[evidencia](evidencia_sexta.json), [salida](evidencia_sexta.txt),
[cotejador](cotejar_sexta.py) y [cotejo](cotejo_sexta.json), conservados.
Sus huellas de fuente y comprobadores coinciden con la evidencia previa.
La incorporación no constituye un resultado nuevo del 10-10.

El [comprobador nuevo](comprobar_cruce.py) reconstruye el cierre de
14 módulos desde las fuentes vigentes, incluyendo los 13 de la sexta
raíz; evita los cientos de certificados de extensión de rachas y no
usa Casa recuperada. Registra versión, entorno, fuentes, objetos,
dependencias y todas las consultas de axiomas en
[evidencia_cruce.json](evidencia_cruce.json) y
[evidencia_cruce.txt](evidencia_cruce.txt).
La [auditoría de huellas](auditoria_cruce.json) registra también las
fuentes con finales LF para contrastarlas con Git; los registros
históricos de Windows conservan sus bytes CRLF. Revisión humana pendiente.
La ejecuta [auditar_cruce.py](auditar_cruce.py), que también compara
los objetos y las consultas del cierre previo con los recompilados.
Se comprobó además la auditoría en una copia con todas las fuentes y
archivos de entorno normalizados a LF; conserva las huellas históricas.

## 6. Contraste independiente y reproducción

[cotejar_cruce.py](cotejar_cruce.py) usa únicamente enteros:

- raíces por búsqueda binaria, incluidos `x^6−1`, `x^6` y `x^6+1`;
- sumas binomiales exactas, independientes de la prueba ponderada de
  Lean, para las colas que dan `2^(c+96m)`;
- órbitas directas con prefijos vivos y valores distintos comprobados;
  el traslado a casi fuga sólo se comprueba hasta el horizonte
  disponible, nunca se declara una fuga pura mediante un barrido;
- cotas exactas y corolarios elevados a potencias en escalas grandes,
  sin recorrer esas órbitas ni simular tantos pasos.

El control acotado da 29 raíces, 20 colas binomiales, 1685 intervalos,
106374 desigualdades de casi fuga **finita**, 1905 cotas mixtas (220
con m>0) y 90 controles de las potencias finales. Son controles de
la implementación; los enunciados universales dependen de las pruebas.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_cruce.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_cruce.json
python -B -X utf8 depuracion/perdices20261007/cotejar_cruce.py --n-max 128 --pasos 300 --nivel-max 4 --m-max 3 --salida depuracion/perdices20261007/cotejo_cruce.json
python -B -X utf8 depuracion/perdices20261007/auditar_cruce.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/auditoria_cruce.json
```

No se relanzó el censo anterior de la sexta raíz ni ningún censo de
Ocelotas. Mahler y los cambios locales ajenos permanecen separados.

## 7. Límite y siguiente paso

El paso 3 queda convertido en una cota exacta con todas sus constantes.
Para el planeador intermitente sigue faltando una cota **inferior**
de regresos incompatible con (4). Infinitos regresos no bastan:
pueden estar tan separados como para cumplirla. El cohete, que
regresa finitas veces bajo cada techo, y la grieta siguen fuera del
alcance de esta combinación.

El siguiente paso es examinar el tramo entre dos regresos de la misma
semilla al mismo techo, buscando una restricción sobre su separación.
El criterio de éxito será una desigualdad que fuerce más regresos
que (4), con hipótesis demostradas para el planeador; una mera
reformulación de la infinitud no servirá. Antes de experimentar se
deben escribir el dominio, la regla y la dependencia en n y c. No se
propone otra ampliación de censos ni reabrir Mahler sin una idea nueva.
