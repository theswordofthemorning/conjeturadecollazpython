# Jinetas: cuánto descenso se pierde al reiniciar una racha

10-10-2026. Tercer ensayo de la [ruta](../casa20261004/RUTA_20261010.md),
después de [conservar todos los prefijos](PREFIJOS.md).

**Resultado:** retirar una racha reduce el contador, pero cambia la
referencia del descenso. La condición exacta que falta es que la caída
posterior supere la subida acumulada desde la semilla original. La
cota con suelo admite una forma más precisa que conserva todos los
pasos pares; su signo sigue siendo equivalente a ese suelo. Estas
identidades no construyen una inducción sin límite de rachas.

Se conserva el nombre Jinetas para esta auditoría. No se afirma
prioridad matemática ni una mejora del alcance de Ocelotas.

## 1. Dominio y piezas que ya estaban disponibles

Mapa atajo `T(n)=n/2` para n par y `(3n+1)/2` para n impar, sobre
enteros positivos. La semilla original cumple n≥3; n=2 baja en un paso.
Los índices cuentan pasos de T y las palabras se leen cronológicamente.
Una racha es un bloque maximal de entradas impares, seguido de al
menos una entrada par. En el primer cruce se puede truncar el último
bloque par. No hay ley probabilística, promedio ni hipótesis externa
LMN en los lemas de esta ficha.

La revisión dirigida de Ocelotas encontró estas piezas vigentes:

| Fuente | Lo que ya permite | Lo que requiere |
|---|---|---|
| [Criba afinada](../cst20260930/OcelotasPrefijosAfinados.lean), `criba_despues_corte` | Acotar los impares restantes después de una entrada par | Un presupuesto R de rachas y una cota del valor actual |
| [Descuento](../cst20260930/OcelotasDescuentoRachas.lean), `paso_descontado` | Encadenar exponentes `a_i−1` | Positividad y al menos un paso par por bloque |
| [Suelo](../cst20260930/OcelotasSueloRachas.lean), `paso_suelo` | Ganar el factor `(N+1)/(2N+1)` | El extremo del bloque cumple y≥N |

Por tanto, descontar una unidad por racha o volver a introducir el suelo
n no proporciona una restricción ausente del desarrollo anterior.
No se recompilaron sus certificados masivos ni se ampliaron tablas.

## 2. Regla de reducción examinada y obligación que deja

Supongamos que el primer cruce de n ocurre en k, con r≥2 rachas.
Cortar justo después de la primera racha y sus pasos pares, en i<k:

```text
x=T^i(n), δ=x−n≥0;   r_cola≤r−1.
```

El coeficiente del prefijo es `C_i≥1`. El de la cola completa es
`C_k/C_i<1`, de modo que la cola desde x también tiene primer cruce
finito, en algún j≤k−i. Una hipótesis inductiva de CST para r−1 rachas
daría `y=T^j(x)<x`.

Esta es una regla concreta, con contador entero r que disminuye y
caso terminal r=1 ya cubierto por Ocelotas bajo sus hipótesis. **Falla
el paso que debe conservar la conclusión:** `y<x` no implica `y<n`.
Además, j puede ser anterior a k−i; reiniciar adelanta el cruce local.

La obligación exacta es

```text
y<n  ⇔  x−y>δ  ⇔  x−y≥δ+1.                     (1)
```

Si la cola tiene `M y=A x+B`, con M=2^j>0, A=3^s y B≥0, entonces

```text
y<n  ⇔  (M−A)x−B > Mδ.                         (2)
```

CST aplicado a x sólo entrega que el lado izquierdo de (2) es
positivo. Hace falta superar **Mδ**, no sólo cero. Las equivalencias
(1) y (2) se demuestran restando y multiplicando por M positivo.

**Testigo real del fallo de esa inferencia:** desde 7, cortar tras
`1110` deja x=13. La cola alcanza su primer cruce con `10`, en 10:

```text
7 → 11 → 17 → 26 → 13 | → 20 → 10 → 5
δ=6, caída local=3;  10<13 pero 10≥7.
C_6=81/64>1;  C_7=81/128<1, y T^7(7)=5<7.
```

No es un contraejemplo de CST: ambos inicios cumplen CST en este
ejemplo. Refuta únicamente transferir sin compensación el descenso
de la cola. La órbita de 7 también figura en
[Rozier–Terracol, §1](https://arxiv.org/html/2502.00948v5#S1);
la auditoría aquí explicita el coste del corte, sin atribuir novedad
al ejemplo ni a las identidades afines.

## 3. La información exacta del factor 3 en cada bloque

Para un bloque `1^a 0^b`, a,b≥1, con entrada x y salida y:

```text
2^(a+b)y = 3^a(x+1)−2^a,
2^a(2^b y+1)=3^a(x+1).                         (3)
```

Derivación independiente: durante los a pasos impares, `T(z)+1`
es `3(z+1)/2`; los b pasos pares dividen el resultado por 2^b.
También se obtiene componiendo las ramas afines una a una.

Con P=2^a, Q=2^b, R=3^a, la diferencia exacta entre ambos lados de
la cota de suelo es

```text
(QN+1)P(y+1) − (N+1)R(x+1) = P(Q−1)(N−y).      (4)
```

Como P>0 y Q>1, queda la equivalencia

```text
(2^b N+1)2^a(y+1) ≤ (N+1)3^a(x+1)  ⇔  y≥N.    (5)
```

La igualdad ocurre exactamente en y=N. Conservando b se mejora la
constante de la cota anterior, que usaba sólo b≥1; **no aparece una
condición nueva sobre el signo**. Usar (5) con N=n al final de una
hipotética trayectoria sin descenso registra precisamente y≥n.
Se puede utilizar como consecuencia de esa hipótesis en una reducción
al absurdo; por sí sola no la contradice.

Para encadenar sin perder la semilla, escribir e=x−n, e'=y−n.
La recurrencia exacta, incluida toda la contribución del factor 3, es

```text
2^(a+b)e' = 3^a e − (2^(a+b)−3^a)n + 3^a−2^a.  (6)
```

El terminal buscado es e'<0. No se ha demostrado una cantidad natural
que disminuya bajo (6) para todos los bloques admisibles anteriores
al descenso. Renombrar e como potencial no resuelve ese requisito.

## 4. Bordes que debe superar cualquier propuesta

Una racha con a=1 y b≥1 satisface `4y≤3x+1`; para x>1, baja desde x.
El borde x=1 permite volver a 1 y explica la desigualdad estricta
requerida. Pero el bloque admisible `110` satisface `8y=9x+5` y crece
para x≥0: por ejemplo, 11→17→26→13.

Más aún, para **cada** k≥1 tomar

```text
n_k=2·8^k−5;
x_j=2·9^j·8^(k−j)−5,       0≤j≤k.
```

Para j<k se tiene `x_j=8u+3`,
`u=2·9^j·8^(k−j−1)−1≥1`. Tres pasos directos dan

```text
8u+3 → 12u+5 → 18u+8 → 9u+4 = x_(j+1).
```

Todos los x_j son impares; por tanto son k bloques maximales `110`
con a=2 y b=1. Sus extremos crecen estrictamente, y sus interiores
tampoco bajan de n_k. El coeficiente al final del bloque j es
`(9/8)^j>1` para j≥1; los otros prefijos también son mayores que 1.
La fórmula demuestra, sin barrido, prefijos sin cruce con tantas
rachas como se quiera **cambiando la semilla con k**.

Esto descarta una cota uniforme del número de rachas en prefijos sin
cruce, independiente de n. No descarta una medida dependiente de n ni una
inducción válida con una hipótesis más fuerte. Tampoco construye
una sola órbita infinita sin cruce, ni un fallo de CST o de Collatz.

## 5. Certificación y reproducción

[JinetasRachas.lean](JinetasRachas.lean) formaliza diez enunciados:
el puente y su versión entera, margen de cola, recurrencia del exceso,
defecto exacto del suelo y su equivalencia, bloque corto, bloque
expansivo, las tres ramas de `110` para todo u natural y el testigo 7.
Las identidades orbitales generales son hipótesis explícitas de los
lemas algebraicos. Su derivación de las palabras y la familia para
todo k están probadas por escrito arriba; no se presenta ese enlace
como una formalización completa de las trayectorias.

El [cotejador independiente](verificar_rachas.py) obtiene bloques por
valuaciones enteras y los contrasta con pasos directos del mapa. Incluye
igualdad y ambos lados del suelo, costes del corte y prefijos de la
familia creciente. Los parámetros acotan controles de la implementación;
sus resultados no sustituyen las pruebas universales escritas.

```powershell
python -B -X utf8 depuracion/jinetas20261010/verificar_rachas.py --a-max 6 --b-max 6 --u-max 31 --familia-max 64 --salida depuracion/jinetas20261010/cotejo_rachas.json
python -B -X utf8 depuracion/jinetas20261010/comprobar_rachas.py --salida depuracion/jinetas20261010/evidencia_rachas.json
```

[Cotejo exacto](cotejo_rachas.json) y [evidencia Lean](evidencia_rachas.json)
conservan 95 bloques, 467 controles del suelo y 471 del corte; siete
miembros de la familia hasta k=64, con bordes y cruces independientes.
Lean 4.32.2 aceptó las diez consultas, sólo con axiomas estándar,
sin `sorryAx` ni avisos. Revisión humana pendiente.

## 6. Decisión y siguiente frente

La auditoría localiza una obligación cuantitativa concreta: (1)–(2).
No justifica extender las tablas de rachas ni anuncia una inducción
resuelta. El descuento y el suelo ya disponibles no salvan por sí
solos el cambio de referencia. Se cierra este ensayo de reinicio simple;
se reabrirá si aparece una regla que transporte la compensación y
pruebe una disminución estricta hasta su terminal.

La lectura de los pendientes confirmó que Mahler ya se cerró el
07-10 y que la sexta raíz ya tiene un cierre Lean local. No se propone
repetir esos trabajos ni se incluyen sus cambios anteriores en este
commit. El siguiente entregable será el **paso 3 de
[Perdices](../perdices20261007/TAMANO.md#qué-debe-aportar-el-siguiente-paso)**:
pasar de su estimación manual a una cota demostrada al combinar la
sexta raíz con la cuenta de casi fugitivos. Primero se auditarán las
dependencias locales necesarias; se exigirán constantes, umbrales,
mismo techo y misma semilla. La estimación previa anticipa sólo una
mejora pequeña del exponente, no una contradicción. Seguirá faltando
la frecuencia mínima de regresos del planeador; el cohete y la grieta
quedan fuera de ese entregable. No se amplían censos.
