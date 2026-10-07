# Cierre pedagógico de la sesión — 07-10-2026

## Qué estamos construyendo

La estrategia sigue siendo construir la casa de Collatz con afirmaciones
demostradas. Para probar por contradicción, suponemos que existe un
contraejemplo y deducimos obligaciones que tendría que cumplir **a la
vez**. Sólo terminaremos cuando dos obligaciones resulten incompatibles.
Acumular restricciones compatibles es avance, pero no es la contradicción.

Trabajamos con el atajo `T(n)=n/2` si n es par y `(3n+1)/2` si es impar.
Después de k pasos, S_k cuenta las entradas impares y
`P_k=3^S_k/2^k` es el «pronóstico»: el factor multiplicativo que resulta
al separar los términos aditivos. No es una probabilidad.

Los dos muros pendientes del plano son: que el pronóstico acabe bajando
de 1, y que ese cruce se traduzca en un descenso real bajo el valor
inicial. Sus posibles fallos son el fugitivo puro y la grieta. Un
fugitivo puro tendría P_k>=1 siempre; las pruebas anteriores obligan
a que su órbita no repita valores. Puede ser cohete, si el pronóstico
tiende a infinito, o planeador intermitente, si vuelve infinitas veces
bajo algún techo fijo aunque también alcance alturas arbitrarias.

## Qué añadió esta sesión

**Recuperación del trabajo.** Se incorporó la sesión local antigua
preservando la ruta vigente de GitHub. Quedaron conservadas las
implementaciones independientes y el respaldo de recuperación. El
[acta](../casa20261005_recuperada/RECUPERACION.md) registra los detalles.

**Una puerta que no se puede dar por cerrada.** La cadena de residuos
olvida el arranque después de suficientes pasos impares. Pero olvidar
el arranque no obliga a repartir las salidas según la ley estacionaria:
la palabra de paridades también importa. Encontramos un ejemplo exacto
de tres pasos donde seleccionar sólo los que no cruzan cambia la ley
y rompe la cota anterior: `1/6>1/8`. Esto descarta esa transferencia
concreta, no un posible argumento distinto.

**La reserva.** Si P>=2^L, cualquier continuación de L pasos puede
mantener el pronóstico al menos en 1. Demostramos el criterio exacto y
escribimos una cota de mezcla que tiene en cuenta esa protección. Un
fugitivo fijo tendría esa reserva en una proporción de tiempos que
tiende a uno para cada L fijo. Eso aún no dice qué continuación toma.

**Una restricción sobre el mismo fugitivo.** Definimos el tamaño
normalizado `R_k=T^k(n)/P_k`. Una identidad exacta, combinada con la
rareza de tiempos de pronóstico bajo, demuestra en Lean `R_k=o(k)`:
R_k acaba siendo menor que cualquier fracción positiva prefijada de k.
Una segunda prueba escrita mejora la cota a
`R_k^6<=n^6(S_k+1)`. Por eso, cuando P_k<=C, el valor real cumple

```
T^k(n) <= C n (k+1)^(1/6).
```

Además, hasta el tiempo k hay como máximo `floor(C n k^(1/6))`
regresos bajo ese techo. La intuición es que los valores visitados
son enteros distintos: un intervalo pequeño sólo puede alojar una
cantidad limitada de ellos. Fijados n y C, multiplicar el tiempo
por 64 sólo duplica esta cota de cantidad de regresos.

## Qué grado de respaldo tiene

| Pieza | Respaldo al cierre |
|---|---|
| Olvido, contraejemplo condicionado y criterio de reserva | 27 consultas nuevas en Lean |
| Identidades, sublinealidad y factor elemental de sexta potencia | 14 consultas nuevas en Lean |
| Cota completa de sexta raíz y cuenta de regresos | Prueba escrita; ordenación y telescopio pendientes en Lean |
| Cotas probabilísticas sobre medidas | Pruebas escritas, formalización de medidas pendiente |
| Cálculos auxiliares | Aritmética exacta independiente; 94 397 contrastes de la sexta potencia |

Los cierres de dependencias tienen 123 y 100 consultas de axiomas;
estos totales incluyen resultados previos y no son cantidades de
descubrimientos nuevos. Lean 4.32.2 usa sólo axiomas estándar, sin
`sorryAx`. La revisión humana sigue pendiente. Los barridos finitos
contrastan las fórmulas; no demuestran Collatz ni la existencia de
un fugitivo. Cada nota temática enlaza sus fuentes y evidencia.

## Qué falta y cómo retomar

La cota crece sin límite y permite regresos infinitos muy separados.
Por eso no hemos descartado al planeador intermitente; tampoco al
cohete ni a la grieta. No hay todavía una contradicción.

La prioridad es [completar la sexta raíz y la cuenta en Lean](TAMANO.md#qué-debe-aportar-el-siguiente-paso),
cruzarlas con el recuento de casi fugitivos y buscar una obligación de
regresar suficientemente a menudo que choque con esas cotas. Si tal
obligación no se obtiene, se documentará el obstáculo sin convertir
rareza en imposibilidad. La [rama probabilística](UMBRAL.md#continuación-de-la-rama-probabilística)
necesita además un puente probado desde su población de palabras
hasta la trayectoria de un entero fijo.

El registro versionado y su base SQLite contienen 281 afirmaciones.
Se preservan `respuestas.db`, los históricos recuperados y el proyecto
de publicación zootheorem. Este cierre documenta el trabajo y sus
próximos pasos; no añade una afirmación matemática nueva.
