# Lectura conjunta de las 268 afirmaciones

03-10-2026. Solicitada por el usuario para obtener una evaluación propia
de su hipótesis de trabajo: todos los enteros positivos llegan a 1.

## Alcance de esta lectura

Se leyeron individualmente los **268 enunciados**, con su estado,
cuantificador y referencia, desde `afirmaciones.db` en modo de sólo lectura.
Se contrastaron notas de las afirmaciones clave, los 63 nodos del mapa,
dependencias de las cadenas principales y las correcciones pertinentes.
También se leyeron las fichas de Tejonas, Alpacas, Erizas y la cota general
de Ocelotas, y las definiciones y enunciados finales pertinentes en Lean.

Es una evaluación del contenido y de sus conexiones. No constituye una
nueva comprobación completa de las 268 demostraciones, ni una recompilación
de todos los archivos históricos. Se usan sus evidencias y alcances
registrados; la revisión humana de los resultados principales sigue pendiente.

El catálogo contiene 163 entradas demostradas, 86 medidas, 12 conjeturadas
y siete refutadas. «Demostrado» incluye implicaciones condicionales,
pruebas escritas y teoremas finitos. Hay resultados externos, etapas
sucesivas de un mismo resultado y registros de actividad: por ejemplo,
el nº 159 recoge la regla de nombres. El total no cuenta pruebas
independientes de Collatz.

## Conclusión propia

**Mi evaluación favorece que Collatz sea verdadero y considera razonable
trabajar con esa hipótesis. El repositorio aporta fundamento matemático
concreto a esa postura.** Su aportación más fuerte es haber convertido
regularidades observadas en identidades, restricciones y resultados
universales con alcances precisos.

**La lectura no permite concluir que los resultados ya obliguen a todos
los enteros positivos a llegar a 1, ni que sólo falte redactar una conexión
final.** No identifico en ellos un mecanismo que excluya toda excepción.
Tampoco asigno un porcentaje de certeza o de avance hacia la demostración.

Coincido con la hipótesis del usuario como juicio de investigación apoyado
en evidencia. Mi discrepancia está en interpretar cada resultado como una
confirmación adicional de la conclusión universal: varios son herramientas,
otros describen modelos distintos y otros descartan mecanismos propuestos.

## El camino que muestra el catálogo

| Afirmaciones | Lectura del avance | Límite relevante |
|---|---|---|
| 1–40 | Identidades de trayectorias, residuos, paridades y familias de fusión. | Algunos resultados suponen llegada a 1; otros tratan el espejo, otro mapa. Los nº 33–34 ya señalan el límite de una criba finita. |
| 41–98 | Coordenadas de pares, Perras, Gatas, Jirafas, preludios y fórmulas de estratos. | Reunir trayectorias y contar sus clases no garantiza el destino final de su cola común. Hay mediciones históricas posteriormente corregidas. |
| 99–147 | Resultados de densidad, modelos estadísticos, restricciones de ciclos y verificaciones finitas. | «Casi todos», un límite de periodo y un rango finito dejan abiertos casos individuales fuera de su alcance. |
| 148–208 | Cadena simbólica, accesibilidad, momentos, retornos y control de sesgos. | La ley probabilística y el condicionamiento importan. El nº 194 es un resultado del modelo V2; el nº 206 refuta una contracción propuesta. |
| 209–238 | Obstrucciones precisas y posterior cierre de una vía de absorción, transporte, Gao, Garner y Wu 2. | La absorción de esta cadena representa fusión. La llegada a 1 de todos los enteros continúa siendo otra afirmación. |
| 239–244 | Transporte entre escalas y exploración de condiciones de Wirsching. | Faltan controles universales de duración o hipótesis de las reducciones; las mediciones no los descargan. |
| 245–268 | Ocelotas: descenso en el primer cruce bajo condiciones cada vez más amplias, cotas generales y nuevas cribas. | Sigue supuesto el primer cruce finito. Los cierres globales tienen un límite de rachas y las hipótesis externas declaradas. |

## Tres avances que sí pesan en la valoración

### 1. Una cadena completa supera sus primeras mediciones

Los nº 227–233 enlazan presupuestos finitos, repetición de ensayos,
el paso al límite y transporte a pares reales. Según los enunciados y
evidencias del repositorio, culminan en densidad natural 1 de la
coalescencia de Gao. Esto tiene más contenido que observar muchos pares
que se juntan: el resultado alcanza todos los tamaños en el sentido
asintótico preciso.

La conexión es explícita:
[Lagartijas](../gao20260920/Lagartijas.md) →
[Martas](../gao20260920/Martas.md) →
[Tejonas](../gao20260920/Tejonas.md) →
[Hienas](../gao20260920/Hienas.md).

El estado `pendiente` de la antigua ruta `phi_uno` no invalida esa cadena:
su descripción explica que el objetivo se obtuvo por otra vía, mientras
sus obligaciones antiguas permanecen abiertas. Es un ejemplo de por qué
hay que seguir las dependencias y no leer sólo las etiquetas.

### 2. Se construyen familias infinitas que realmente llegan a 1

El nº 234, [Alpacas](../garner20260926/Alpacas.md), construye bloques
arbitrariamente largos y arbitrariamente altos de consecutivos con
llegada a 1 demostrada. La prueba elige el levantamiento para que el valor
común sea una potencia de 2. De ahí se deduce Wu 2.

Esto demuestra convergencia de familias infinitas concretas. La elección
del levantamiento es esencial: no toma un entero positivo arbitrario
prefijado y demuestra que pertenezca a una de esas familias.

### 3. Ocelotas convierte un posible fallo en restricciones comprobables

El nº 261 ya es una fórmula válida para cualquier cantidad finita de
rachas, bajo LMN. Si un primer cruce finito falla en descender, exige

```text
k < 2^(2r+32),
n < 2^(19(2r+65)^2+r).
```

La [región finita](../cst20260930/COTA_GENERAL.md), los cierres de 22 y
77 y las cribas de los nº 266–267 son avances concretos. Las cotas crecen
con r: fijar r deja una región finita; permitir todos los r no produce
automáticamente una única región finita ni prueba que las regiones estén
vacías. Las hipótesis de cada cierre siguen vigentes.

## Dónde permanece el salto lógico

1. **Fusión y destino.** Dos recorridos que se juntan comparten su futuro;
   la igualdad no demuestra por sí misma que ese futuro llegue a 1.
2. **Densidad y cada entero.** Una excepción individual o un conjunto de
   densidad cero no contradice un resultado de densidad 1. El propio nº 235
   deja abierta incluso la densidad natural 1 de los que llegan a 1.
3. **Accesibilidad y recorrido efectivo.** Hormigas construye una palabra
   de bits que fusiona desde un estado. El número inicial dado determina
   sus propios bits; la existencia de una continuación favorable no obliga
   a ese número a seguirla. El transporte de Tejonas resuelve una cuestión
   de distribución, con el alcance declarado.
4. **Primer cruce.** Ocelotas controla qué sucede en un cruce existente;
   falta demostrar su existencia para todo entero positivo y cerrar el
   descenso sin un límite prefijado de rachas, o encontrar otra ruta universal.

Las refutaciones internas no son contraejemplos a Collatz. Sí muestran
que estructuras y tendencias favorables pueden coexistir con mecanismos
insuficientes para una prueba. Los nº 206 y 211
([Erizas](../frente20260910/Erizas.md)) identifican obstáculos de ese tipo.

## Incidencia concreta de coherencia detectada

El nº **71** está etiquetado como demostrado y combina:

- la identidad válida `D=t-1` para la forma `{s,3s+t}`;
- la frase histórica «la dinámica jamás alcanza la forma `{s,3s+17}`».

Sus notas aclaran que sólo la identidad es la parte demostrada. Además,
las correcciones **38 y 39** del catálogo retiran la supresión de `+16`,
y [auditoria_rigor.py](../../auditoria_rigor.py), test R30, recoge la
comprobación de su aparición. La redacción del enunciado necesita separar
el resultado vigente de la hipótesis histórica refutada.

Esta lectura deja señalada la incidencia; conserva los estados y los
históricos. No interpreta el nº 71 completo como un teorema vigente.

## Consecuencia para la investigación

La conclusión práctica es seguir buscando un argumento general que
controle las excepciones permitidas por los teoremas actuales. Al proponer
un puente entre dos resultados, hay que hacer explícito si cambia de
«existe una familia» a «todo entero», de «casi seguro» a «cada trayectoria»,
o de «si hay cruce» a «el cruce siempre ocurre».

La [premisa del usuario](../../PREMISA_DE_INVESTIGACION.md) queda apoyada
por una lectura sustantiva del trabajo acumulado. El cierre universal
sigue siendo una tarea matemática abierta, cuya dificultad no se mide
por el número de afirmaciones del catálogo.
