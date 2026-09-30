# Plan vigente: de los bloques cortos a los largos

28-09-2026. Orden solicitado por el usuario tras la
[segunda opinión](SEGUNDA_OPINION_20260928.md). Sustituye su orden de ejecución;
conserva los argumentos y límites matemáticos de esa evaluación y el
[plan del 27-09](LEEME.md) como antecedentes.

Una sesión es un bloque con un objetivo acotado, evidencia y cierre escrito.
Estos presupuestos son límites iniciales de inversión, no predicciones de
éxito ni de duración de una demostración. Los rangos de sesiones de la tabla
reservan el máximo de cada bloque; si uno acaba antes, se adelanta el siguiente.
El trabajo se mantiene local y sin subagentes. No se programan nuevos censos.

| Orden | Sesiones reservadas | Frente y presupuesto | Entregable del bloque |
|---|---|---|---|
| 1 | 1–2 | Nashida: 1–2 sesiones | Original y código identificados; cotejo del enunciado, dependencias y puente condicional con Condoras; decisión sobre integración. |
| 2 | 3–6 | Pandas: 2–4 sesiones | Formalización del lema escrito con sus hipótesis y cotejo independiente. La cota universal del residuo queda fuera de este presupuesto. |
| 3 | 7–12 | Wirsching: 4–6 sesiones | Revisión del programa y del preprint de Tavares; aislamiento del control por residuos pendiente y de un objetivo limitado. |
| 4 | 13–18 | CST: 6 sesiones | Cotejo de dos rachas impares, parametrización exacta y examen de una desigualdad o reducción para longitudes arbitrarias. |
| Después | Sin fecha asignada | CST completa, Wu 1 y extensiones | Reestimar sólo cuando los bloques anteriores proporcionen un mecanismo concreto. |

**Avance del 28-09:** diagnóstico inicial de Nashida realizado y puente
condicional certificado en Lean; ver su [ficha](../nashida20260928/LEEME.md).
La reproducción de la formalización externa queda como ampliación separada,
no como un resultado ya obtenido. Siguiente bloque: Pandas. Las sesiones
reservadas no contabilizan mensajes ni se declaran consumidas automáticamente.

**Avance del 30-09:** Pandas cerrado en una sesión; ver su
[ficha](../pandas20260930/LEEME.md). Formalizado con `Res >= 1` demostrado,
la pregunta de Gao con `Res < 4` y en densidad, y la aplicación de combinar
escalas (Marmotas), cuya obstrucción es una cuenta de pasos por encima de la
barrera. Siguiente bloque: Wirsching.

**Wirsching, sesión 1 (30-09):** [ficha](../wirsching20260930/LEEME.md). El
eslabón abierto es (⋆3); (⋆1) literal falla en todo nivel calculado, con ceros
exactos, y su refutación en un 3-ádico refutaría la conjetura 2 tal como está
escrita. La versión útil para el laboratorio es por entero y con ventana
desplazada. Quedan hasta 5 sesiones reservadas.

## Bloque 1: Nashida

**Sesión 1.** Localizar el texto primario y fijar su versión y el commit del
código. Cotejar mapa, dominio, extremos de los intervalos, desigualdad de la
barrera, cuantificadores y dependencia de las constantes. Leer el enunciado
Lean final y las hipótesis que realmente descarga. Registrar la procedencia
de las comprobaciones del autor sin confundirlas con una reproducción local.

**Sesión 2.** Derivar independientemente lo que la cota permite concluir sobre
la llegada a 1 y `dWu`. Comprobar bordes y normalizaciones con `Condoras.lean`.
Decidir si merece un certificado local, qué quedaría como hipótesis y qué
costaría reproducir las dependencias externas. Si la auditoría descubre una
obstrucción concreta, documentarla y cerrar el diagnóstico sin ampliar el
presupuesto automáticamente.

Ficha de trabajo: [Nashida](../nashida20260928/LEEME.md).

## Bloque 2: Pandas

Revisar el lema corregido y su caso de borde; expresar con las definiciones
vigentes las identidades de altura, tiempo y residuo; completar Lean y
consultar los axiomas. El entregable conserva la hipótesis de que las dos
órbitas terminan y las cotas del residuo. No se confunde con la pregunta de
Gao sin esas cotas. Una nueva idea sobre residuos se registra como candidata
para los bloques siguientes.

## Bloque 3: Wirsching

Leer las piezas necesarias del programa y contrastar las pruebas que anuncia
Tavares. Escribir el enunciado aritmético restante y separar operador límite,
control de residuos y densidad de los predecesores reales. Intentar una
instancia limitada que aporte información sobre ese paso. No se presupuesta
una auditoría completa ni la resolución de todo el programa.

## Bloque 4: CST

1. Cotejar la literatura y fijar el alcance del objetivo de dos rachas.
2. Parametrizar exactamente las semillas admisibles y el término aditivo.
3. Contrastar por una segunda derivación y revisar bordes; primer punto de decisión.
4. Buscar una desigualdad que controle longitudes arbitrarias.
5. Examinar una reducción entre palabras que conserve el primer cruce y el margen.
6. Auditar los intentos y decidir si extender, estrechar el objetivo o cambiar de frente.

La formalización de una prueba nueva se presupuestará cuando exista una
prueba escrita suficientemente estable. `atacacst.lean` aporta la identidad
afín, no la desigualdad universal pendiente.

## Criterio común para gastar más trabajo

### Herramienta que aporta la lectura de Nashida: combinar escalas

**Una cota útil a escalas limitadas puede servir de base a una recurrencia
que la transporte a escalas mayores.** Se incorpora expresamente al camino
por petición del usuario. En Nashida, la cota de barrera fija empeora con
el rango del intervalo; se usa sólo en una escala de arranque elegida en
función de la barrera. Desde allí, una recurrencia entre ventanas acumula
un error controlado. El empalme obtiene una cota uniforme en el extremo.
Es una técnica del artículo, no un hallazgo nuevo del laboratorio.

Antes de trasladarla a otra ruta, escribir y comprobar:

1. Qué cantidad se quiere acotar y con qué mapa, dominio, normalización y ley.
2. En qué rango la cota inicial es válida y útil.
3. Qué recurrencia se demuestra para esa misma cantidad, o qué comparación
   demostrada conecta las cantidades de los dos regímenes.
4. Dónde se solapan los rangos y cómo se elige la escala de arranque.
5. Cómo se controla la suma de errores sin hacer depender la constante del
   extremo que se quiere tratar uniformemente.

Aplicaciones **candidatas**, todavía sin esos ingredientes demostrados:

- **Pandas:** aplicada el 30-09 (Marmotas). La cota del residuo en `[1, B)` se
  propaga con un factor `(1 + 1/(3B))^S`; el empalme es la primera entrada
  en `[1, B)`. El error sólo se controla si S, los pasos `3n+1` por encima de
  B, está acotado; esa cota falta.
- **Wirsching:** comparar cotas para conjuntos finitos de predecesores con
  una recurrencia que controle los residuos a mayor profundidad. El paso
  entre la dinámica límite y los predecesores enteros debe justificarse.
- **CST:** combinar familias de palabras ya tratadas con una reducción que
  conserve el primer cruce y el margen de descenso para longitudes mayores.
  Aquí la escala puede ser la longitud o el número de rachas; una cota de
  densidad no sustituye la desigualdad que se necesita para cada semilla.
- **Cadena de Gao:** una mejora del encuentro sólo sirve al problema del
  destino si se añade una comparación con un observable de llegada a 1.
  La recurrencia de Nashida no se transfiere a la fusión por analogía.

El próximo bloque deberá revisar esta lista al fijar su objetivo. Detalles
de la fuente y de su alcance: [auditoría de Nashida](../nashida20260928/LEEME.md).

### Decisión al cerrar cada bloque

Continuar si hay una herramienta demostrada para una familia infinita,
una reducción válida o una obstrucción precisa que cambie la decisión.
Un aumento de cortes finitos no basta por sí solo. Las ideas de un bloque
corto pueden modificar los siguientes: registrar la razón antes de cambiar
el objetivo. La prioridad de revisión humana de los resultados ya obtenidos
se mantiene al margen de este calendario de exploración.

El cómputo inicial se dedica a lectura, álgebra y verificación de pruebas.
La reproducción de un proyecto Lean externo puede exigir otra versión y
descargas grandes; eso se evalúa antes de integrarlo en el laboratorio.
No se asigna un coste de CPU sin medirlo ni se da por resuelta una conjetura
por haber consumido las sesiones previstas.
