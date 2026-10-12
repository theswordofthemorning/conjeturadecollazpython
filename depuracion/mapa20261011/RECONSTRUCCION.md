# Reconstrucción del arca — 11-10-2026

## Qué fallaba y qué se reconstruyó

El generador anterior usaba 63 nodos y 96 dependencias de una etapa del
laboratorio. Asignaba las afirmaciones por claves, palabras y carpetas.
Los resultados sin nodo se convertían en talleres o grupos sin conectar.
Esto ocultaba animales con documentos propios y confundía la falta de una
entrada en el catálogo con la falta de antecedentes matemáticos.

El nuevo [catálogo](../coherencia20260913/mapa_investigacion.json) registra
explícitamente **70 nombres, 122 piezas y nueve ramas**. Cada pieza tiene
resumen, límite y fuentes. Cada una de las 331 afirmaciones tiene una pieza
principal. Las familias pueden tener subpiezas: Perdices y Casa se pueden
abrir para seguir sus resultados internos.

Las 70 entradas son 68 nombres de animales, **Focas**, alias documentado de
Queltehues, y **Lurrus**, nombre de una subteoría. No se inventaron animales
para rellenar el árbol ni se añadieron afirmaciones para duplicar resultados
recuperados. Libélulas conserva el «teorema de la libélula» de Garzas como
nombre de búsqueda y pieza propia.

## Fuentes y cobertura

Se cotejaron estas fuentes, con lectura dirigida:

1. La tabla «El zoológico» de la [ruta conservada](../../archivo/contexto_20260913/RutaTeoremas.md.txt),
   líneas 962–1012: 51 nombres.
2. **68 revisiones** de `RutaTeoremas.md` en `git log --all`, tras
   `git fetch origin`. Se extrajeron sólo las filas de la tabla del zoológico.
   El [inventario de Git](inventario_git.json) conserva las revisiones y las
   apariciones de cada nombre. Las fechas de Git no sustituyen las fechas
   de las notas ni prueban prioridad matemática.
3. Las afirmaciones, claves y descripciones vigentes de
   [registro.json](../coherencia20260913/registro.json).
4. Los documentos originales de Perras, Gatas, Jirafas, Pumas y las demás
   piezas faltantes, los índices actuales y las notas de los frentes.
5. La [sesión recuperada](../casa20261005_recuperada/RECUPERACION.md) y la
   [conciliación](../jinetas20261010/CONCILIACION.md) que delimita solapamientos.

La cobertura es la de estos registros y fuentes identificadas. No equivale
a asegurar que no existe un apodo sin indexar en cualquier archivo privado
o temporal del computador. El verificador exige que todos los nombres de
la tabla histórica y su historial consultado estén incluidos.

### Hitos contrastados con Git

| Commit | Qué aporta al mapa |
|---|---|
| `7745462` | Bautizo del primer zoológico: Perras, Gatas, Jirafas, Pumas, Lobas y los demás nombres iniciales. |
| `427051e` | Cambio explícito Focas → Queltehues; el diff conserva la razón y la revisión de la pieza 3. |
| `705c19b` | Bautizos de Víboras, Avispas, Efímeras, Pirañas, Tortugas y Langostas. |
| `48afa4e` | Lurrus reúne el modelo V2, reversión, medianas y el problema de transferencia. |
| `d84866b` | Nueva etapa de Garzas y análisis de los parámetros de Cigarras. |
| `372bce2`, `718cbb8` | Inicio de Ocelotas y sustitución de la hipótesis de Rhin por LMN. |
| `98fc633`, `5688002` | Cierres de 77 bajo las hipótesis declaradas y de 24 bajo LMN. |
| `65d97e0` | Recuperación independiente de Corzas, Chinchillas y la primera Perdices. |
| `96cf471` | Exclusión del planeador por colisiones y sumabilidad. |

El plan [Nashida → Pandas → Wirsching → CST](../transversal20260927/PLAN_SESIONES_20260928.md)
confirma el recorrido señalado por el usuario. Ocelotas nace de CST;
[Casa](../casa20261004/LEEME.md) separa obligaciones universales y escenarios;
[la ruta del 10-10](../casa20261004/RUTA_20261010.md) conecta las continuaciones
de Jinetas y Perdices. Perdices también tiene un antecedente recuperado del
05-10: el mapa no presenta a Jinetas como requisito de toda Perdices.

## Qué significa cada conexión

| Tipo | Interpretación |
|---|---|
| Pertenencia | Una pieza está situada en una rama de investigación. No es una implicación. |
| Usa | Una prueba o construcción utiliza la herramienta indicada, en el alcance descrito. No implica que toda la familia dependa de ella. |
| Antecedente | Una etapa motivó o precedió otra; incluye el orden de exploración. |
| Condicional | Hipótesis externa o puente pendiente. La ficha precisa cuál de las dos cosas es. |
| Contrasta | Una revisión limita, corrige o compara un resultado anterior. |
| Registrada | Dependencia heredada del registro anterior, con sus dos nombres originales. Se conserva como tal; esta tarea no reaudita las 96 pruebas. |

Hay **168 relaciones**: 95 dependencias heredadas entre piezas, una interna
a Conejas, 31 usos documentados, 33 antecedentes, cinco contrastes y tres
condicionales. La pertenencia a ramas se almacena aparte; no infla el número
de dependencias matemáticas. Todos los usos y dependencias heredadas forman
un grafo sin ciclos. Las relaciones históricas y de contraste se consultan
por separado de ese control.

### Conexiones que explican los casos planteados

- **Perras:** Terras y las coordenadas de Comadrejas → mitad exacta del
  estrato mínimo. Gatas usa ese reparto en la ecuación de renovación.
- **Gatas:** la contracción alimenta Panteras y el reparto de Vacas; las
  formas estudiadas se unifican históricamente en Leonas.
- **Jirafas:** la fórmula afín de Terras fuerza igualdad de pendientes.
  Conserva la caracterización de clases; el corolario de densidad retirado
  no reaparece como soporte válido.
- **Pumas:** Leonas define las matrices truncadas; el puente documentado
  por Zorras y los certificados enteros dan cotas inferiores. Langostas
  acota cada truncado por ambos lados. Su cota superior no se adjudica a
  la cadena infinita.
- **Ocelotas:** Terras, residuos y separación de potencias → cierres del
  primer cruce. LMN y Rozier–Terracol se ven como condiciones de los cierres
  que los usan. Casa y ciertas herramientas de Jinetas/Perdices reutilizan
  partes concretas, sin heredar indiscriminadamente todas las hipótesis.
- **Perdices:** CasaCadena recuperada → acoplamiento; el retrato del
  fugitivo → regresos; colisiones → mínimos y exclusión del planeador;
  palabras prohibidas → retorno H → búsqueda matricial. La familia muestra
  aparte las obligaciones abiertas de Muro B y circuitos no triviales.

## Correcciones de coherencia del registro

Se preservaron literalmente afirmaciones, correcciones, constantes, claves
y dependencias. Se actualizaron **tres nodos**, mediante cambios versionados:

| Nodo | Ajuste y respaldo |
|---|---|
| Ocelotas | La descripción de dos rachas bajo Rhin estaba superada. Ahora resume 24 bajo LMN y 77 bajo LMN y Rozier–Terracol, supuesto el primer cruce. Las afirmaciones anteriores siguen conservadas. |
| Arañas | «Perturbación sumable» contradice la corrección ya presente en la afirmación 160 y la revisión del tronco. El nodo dice acotada por paso y retira la sumabilidad en trayectoria. |
| Cebras | El nodo medido mezclaba la mitad conservada y la lectura retirada. Se alinea con la parte algebraica demostrada de la afirmación 172; la lectura de deriva sigue retirada. No se ha demostrado nada nuevo. |

Los valores anteriores de Arañas y Cebras quedan en los campos `antes` del
registro. La descripción previa de Ocelotas se conserva además en el respaldo
de entrada y en Git. Las listas literales históricas del generador no cambiaron.

## Persistencia y verificación

`guardarafirmaciones.py` incorpora las tablas `mapa_*` al mismo reemplazo
atómico de SQLite. El catálogo declara la asignación mediante claves
estables; los ID 1–208 se anclan a la fuente histórica congelada. Rechaza
afirmaciones sin pieza, duplicadas, animales sin ubicación y fuentes ausentes
antes de escribir la base. Un registro histórico sin el campo del mapa sigue
siendo regenerable con el convenio anterior.

La [auditoría](auditoria_mapa.json) comprueba cobertura, correspondencia
literal JSON/SQLite, conservación de tablas, integridad, referencias y enlaces.
La [prueba de navegador](navegacion.json) abre ambos HTML desde archivo local,
sin red, a 1440 y 390 píxeles: búsqueda de once nombres, alias Focas, inventario,
frontera actual, red, filtros de estados, afirmaciones y correcciones.

No se recompiló Lean ni se relanzaron censos: se reconstruyó documentación
con evidencia existente, sin atribuir una nueva certificación matemática.
No se editaron OEIS, las implementaciones independientes recuperadas ni
`respuestas.db`. No hubo commit ni push.
