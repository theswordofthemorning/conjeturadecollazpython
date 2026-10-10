# Perdices: cuánto olvida la cadena y qué no dice del fugitivo

[Cierre pedagógico de la sesión](CIERRE_SESION.md).
**10-10:** [separación y rachas entre regresos](SEPARACION.md): cota orbital
por rachas en Lean y prueba escrita de que un planeador necesita
excursiones con rachas no acotadas; enlace final por formalizar.
Conserva la [cota de regresos 4/25](CRUCE.md), con constantes explícitas.
Para retomar: [plan de tamaño y regresos](TAMANO.md#qué-debe-aportar-el-siguiente-paso)
y [pendientes de la rama probabilística](UMBRAL.md#continuación-de-la-rama-probabilística).

07-10-2026. Continuación de [Perdices recuperadas](../casa20261005_recuperada/PERDICES.md),
sin modificar su evidencia histórica. Es una aplicación del acoplamiento
elemental a la cadena ya construida; no se reclama prioridad.

## Mapa, ley y alcance

Se usa el atajo `T(n)=n/2` para n par y `(3n+1)/2` para n impar.
`S_k(n)` cuenta entradas impares en los primeros k pasos. En `Z/3^m`,
`h=2^(-1)` y las ramas de la cadena son `F_0(x)=hx`,
`F_1(x)=h(3x+1)`. Una palabra w de k bits se lee en orden cronológico;
`s(w)` cuenta sus unos. `C_w(x)` es su composición.

La ley aleatoria usa bits independientes con probabilidad 1/2 para cada
valor. No se supone que las paridades de un entero fijo sean aleatorias.
Nuestra distancia `TV` es `sup_E |mu(E)-nu(E)|`, equivalente a la mitad
de la suma absoluta. La oscilación conserva la suma absoluta completa.

## El olvido, con prueba

Restar las dos ramas y componer da, por inducción,

```text
C_w(x)-C_w(y) = 3^s(w) h^k (x-y)   en Z/3^m.
```

Por tanto, si `s(w)>=m`, la salida es independiente del arranque.
La igualdad vale palabra por palabra, incluso si los arranques dependen
de w. Es la pieza que permite usar el representante entero de cada clase
módulo `2^k`, sin exigir un arranque 3-ádico independiente.

En [PerdicesAcoplamiento.lean](PerdicesAcoplamiento.lean),
`recorrido_nat` identifica la definición en `ZMod` con `CasaCadena.cadena`;
`olvido` y `cadena_olvida` prueban el olvido. `orbita_olvida` lo aplica a
`T^k(n)` cuando `S_k(n)>=m`.

Para cualquier colección finita W de palabras y evento E, las cuentas
para dos arranques sólo pueden diferir en las palabras con menos de m
unos. `cota_evento` certifica una de las dos desigualdades; intercambiar
los arranques da la otra. Al tomar todas las palabras de largo k, su
proporción es exactamente

```text
q(k,m) = 2^(-k) sum_{0<=j<m, j<=k} binom(k,j).
```

## Estacionaria y arranques enteros

Definamos `nu_0=delta_0` y, con `A_1,...,A_m` independientes,
`P(A_i=a)=2^(-a)` para a>=1,

```text
Y_m = sum_{l=1}^m 3^(l-1) 2^(-A_1-...-A_l)  mod 3^m,
nu_m = ley(Y_m).
```

La proyección de `nu_m` al nivel m-1 es `nu_(m-1)`: el último término
desaparece. Separar `A_1=1` de `A_1>1`, cuya probabilidad es 1/2 cada
una, y usar la falta de memoria de la geométrica da
`nu_m=(F_0)_*nu_m/2+(F_1)_*nu_m/2`. En la segunda rama basta la proyección
al nivel m-1. Esto prueba la estacionariedad.

Acoplar cualquier arranque X con uno estacionario Z independiente de
la palabra produce salidas iguales salvo, a lo sumo, en `s(w)<m`:

```text
TV(ley(C_W(X)), nu_m) <= q(k,m).
```

X puede depender de W. Z se elige independiente de ambos. Para m fijo,
q tiende a cero; esto también prueba la unicidad de la estacionaria.

Si U es uniforme en `[0,2^k)`, la palabra de paridades de U es uniforme
entre todas las palabras, por la biyección recuperada en `CasaCadena`.
Tomar `X=U` da la consecuencia para las órbitas reales:

```text
TV(ley(T^k(U) mod 3^m), nu_m) <= q(k,m).
```

Condicionar a `S_k(U)>=m`, cuando k>=m, da exactamente la ley de
`C_W(0)` condicionada a `s(W)>=m`. También queda a distancia a lo sumo q
de `nu_m`: la ley estacionaria es una mezcla de esa misma ley buena,
con peso `1-q`, y la ley del evento malo, con peso q. Para m=0 la
distancia es cero; si k<m el evento bueno es vacío y no se condiciona.

**Alcance formal:** Lean certifica la identidad, el olvido, la conexión
con órbitas y la desigualdad de cuentas por evento. La construcción
probabilística de `nu_m`, la cuenta binomial y los pasos anteriores de
estacionariedad, variación y condicionamiento son prueba escrita; no
están formalizados aquí como teoremas de medidas. Revisión humana pendiente.

## Una obstrucción explícita a la transferencia

Una palabra de sólo unos y longitud k>=m manda todos los arranques a
`-1 mod 3^m`. El olvido es completo, pero la salida es una masa puntual.
`olvido_sin_uniformidad` lo prueba en Lean. Cada horizonte finito se
realiza por un entero (`prefijo_sesgado_realizable`); explícitamente,
`n_k=2^k-1` cumple `T^j(n_k)=3^j*2^(k-j)-1` para `0<=j<=k`.

Módulo 9, `nu_2(8)=22/63`, así que esa masa puntual queda a distancia
`41/63` de la estacionaria, por largo que sea el horizonte. No hay
contradicción con el acoplamiento: la palabra ya no tiene ley uniforme.
El entero `n_k` cambia con k; esto no construye un fugitivo positivo.

Un fugitivo también permite borrar su arranque a cada escala fija,
pues acumula subidas. Lo pendiente es controlar su palabra concreta.
Este bloque no excluye al cohete ni al planeador intermitente y no
convierte «casi todos» en «todos».

## Condicionar a no cruzar: un contraejemplo de tres pasos

El evento `H_k` exige `3^S_j>=2^j` en **cada** paso j<=k. Es distinto
de exigir solamente `S_k>=m`, cuyo condicionamiento sí admite la cota
anterior. Para k=3, entre los ocho representantes sólo sobreviven 3 y 7:

| n | Tres pasos | Palabra | Salida módulo 3 |
|---|---|---|---|
| 3 | 3 → 5 → 8 → 4 | 110 | 1 |
| 7 | 7 → 11 → 17 → 26 | 111 | 2 |

La ley condicionada es `(0,1/2,1/2)` y su TV respecto a
`nu_1=(0,1/3,2/3)` es `1/6`. Sin embargo, `q(3,1)=1/8`.
Por tanto, **la cota sin condicionamiento no se hereda al condicionar
a no cruzar**, ni siquiera en este horizonte. Lean comprueba el conjunto
completo (`supervivientes_tres`), las salidas y la desigualdad exacta
(`condicionar_no_cruce_rompe_cota`), por reducción en el núcleo.
El cotejo independiente usa productos de `Fraction` para el pronóstico.
Esto refuta esa transferencia concreta; no refuta una posible cota
asintótica distinta ni construye un fugitivo.

## Cotejo de Tao y precisión de la medición recuperada

Se cotejó [Tao, versión v5 del 15-02-2022](https://arxiv.org/html/1909.03562v5):
la fórmula (1.26) es la ley de arriba; el lema 1.12 da su recurrencia
finita; 1.14 trata la oscilación fina y 1.17 el decaimiento de Fourier.
Los números recordados eran correctos. La ecuación (1.9) usa el doble
de nuestra TV, y el teorema 1.3 habla de densidad logarítmica.

Converger a `nu_m` al crecer k no controla su oscilación al crecer m.
La mezcla fina de Tao sigue siendo una pieza distinta. Por ejemplo,
`nu_1=(0,1/3,2/3)` ya es estacionaria y no es uniforme.

El texto recuperado llama «exacta» a la ley calculada hasta m=14, pero
su script usa coma flotante y detiene por diferencia de iteraciones.
Es una aproximación numérica: ese criterio solo no aporta un error
certificado respecto al límite. Se conserva literalmente el histórico.
La cifra `0,040088` de aquel informe es suma absoluta, es decir, el doble
de nuestra TV. No se repitió el censo de `2^20` ni el cálculo hasta `3^14`.

## Evidencia reproducible

[cotejar_acoplamiento.py](cotejar_acoplamiento.py) obtiene la estacionaria
con `Fraction` por dos métodos independientes: resolver las ecuaciones
en ciclos de duplicación y sumar exactamente los huecos geométricos
por clases de su período. Verifica normalización, positividad,
estacionariedad y compatibilidad de las proyecciones.

[Salida exacta](cotejo_acoplamiento.json): niveles m=0..6 (hasta 729 estados),
2013 cotas para arranques de la cadena y 100 para órbitas enteras,
10 235 órbitas, 40 700 sincronizaciones y 55 pares (k,m), incluidos bordes.
La fórmula del prefijo sesgado se contrasta en 2145 casos hasta k=64.
Como ejemplo, para m=6 y k=60 la cota es
`2992599/576460752303423488 < 5,2e-12`; la TV exacta desde cero es
aproximadamente `1,61e-15`.

[Comprobador Lean](comprobar_acoplamiento.py),
[evidencia](evidencia_acoplamiento.json) y [registro](evidencia_acoplamiento.txt):
Lean 4.32.2, 13 módulos, 123 consultas de axiomas, 27 de esta extensión;
sólo `propext`, `Classical.choice` y `Quot.sound`, sin `sorryAx`.
Reconstruye exclusivamente el cierre de dependencias de la implementación
recuperada y esta extensión. La reutilización exige huellas de fuentes,
objetos, dependencias y entorno coincidentes; audita las consultas de axiomas.

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_acoplamiento.py --m-max 6 --k-max 10 --pasos 60 --salida depuracion/perdices20261007/cotejo_acoplamiento.json
python -B -X utf8 depuracion/perdices20261007/comprobar_acoplamiento.py --compilados "$env:TEMP/perdices_20261007" --salida depuracion/perdices20261007/evidencia_acoplamiento.json
```

[Continuación: frontera y reserva](UMBRAL.md). La recurrencia condicionada
elimina exactamente las bajadas de prefijos con pronóstico menor que 2.
Once lemas adicionales formalizan la reserva necesaria y suficiente
para permitir todas las continuaciones de un bloque y su realización
entera. Prueba escrita de una cota adaptada: `TV<=G*q+(1-G)`, con G la
fracción protegida por esa reserva; 20 772 contrastes exactos.
En un fugitivo fijo, los tiempos sin reserva tienen densidad cero,
por la rareza previa del planeador. La continuación
[tamaño y regresos](TAMANO.md) combina esa rareza con la identidad afín:
`T^k(n)/P_k=o(k)`, en Lean. La identidad multiplicativa y la ausencia
de repeticiones dan además `(T^k(n)/P_k)^6<=n^6(S_k+1)`, formalizada el
07-10 por la noche en [PerdicesSexta.lean](PerdicesSexta.lean) con su
cuenta de regresos y el rasgo 9: antes del tiempo K el pronóstico
alcanza `K^(5/6)/n` ([detalle](TAMANO.md#sexta-raíz-y-techo-en-lean)).
Sigue siendo compatible con una fuga lenta y no alcanza al cohete.
