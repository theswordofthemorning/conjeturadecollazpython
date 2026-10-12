# El arca del laboratorio — 12-10-2026

- [Mapa básico](MapaDependenciasBasic.html): el recorrido histórico, nueve ramas y todos los animales.
- [Mapa completo](MapaDependenciasComplex.html): añade red navegable, 333 afirmaciones y 85 correcciones.
- [Reconstrucción y decisiones](RECONSTRUCCION.md): fuentes cotejadas, vínculos y límites.
- [Auditoría de datos](auditoria_mapa.json) y [prueba de navegación](navegacion.json).

Ambas páginas se abren con doble clic y funcionan **sin conexión**. Buscar
también encuentra alias como Focas. Seleccionar una pieza muestra qué aporta,
hasta dónde llega, de dónde viene y qué resultados la utilizan.

## Cobertura

**70 entradas:** 68 nombres de animales, el alias Focas → Queltehues y la
subteoría Lurrus. Hay 123 piezas, organizadas en nueve ramas. Las 333
afirmaciones tienen una asignación explícita; las piezas documentales sin
afirmación propia también están presentes, con sus fuentes.

La tanda del 12-10 añade dos afirmaciones de Perdices sobre soportes y
rectas invariantes de matrices. Las 331 afirmaciones anteriores se conservan.

El árbol indica pertenencia a la investigación. Las otras conexiones distinguen
uso de un resultado, antecedente histórico, hipótesis o puente pendiente y
contraste. Se conservan las 96 dependencias anteriores, una dentro de la
familia Conejas. No se interpretan como si cada resultado de un animal
dependiera de todos los resultados del otro.

El recorrido Nashida → Pandas → Wirsching → CST → Ocelotas se documenta
como orden de exploración. Casa continúa esa ruta; las ramas de Jinetas y
Perdices se entrelazan y tienen antecedentes propios.

## Fuente y regeneración

La fuente editorial es
[mapa_investigacion.json](../coherencia20260913/mapa_investigacion.json),
enlazada por el registro vigente. No se deducen conexiones a partir de
nombres de archivos. Desde la raíz del repositorio:

```text
python -B -X utf8 guardarafirmaciones.py
python -B -X utf8 depuracion/mapa20261011/generar_mapa.py
python -B -X utf8 depuracion/mapa20261011/verificar_mapa.py --salida depuracion/mapa20261011/auditoria_mapa.json
python -B -X utf8 depuracion/mapa20261011/verificar_navegacion.py --salida depuracion/mapa20261011/navegacion.json
```

La última comprobación requiere Playwright y Chromium instalados; visualizar
los mapas no requiere instalar nada. No ejecuta experimentos matemáticos.

SQLite incluye tablas `mapa_*`: piezas, ramas, inventario, afirmaciones
asignadas, correspondencia con nodos anteriores y relaciones documentadas.
`nodos` y `dependencias` conservan el catálogo anterior como subconjunto.
**Para consultar el arca completa, usar `mapa_piezas` y `mapa_inventario`.**
Todo se escribe mediante el mismo reemplazo atómico que el resto del catálogo.

Las claves nuevas se enlazan por nombre estable. Los ID históricos 1–208
quedan anclados a la fuente congelada que verifica el generador. Si se añade
una afirmación sin ubicación, la regeneración falla antes de reemplazar SQLite.

## Conservación

La plantilla vigente es [plantilla_flujo.html](plantilla_flujo.html) (12-10):
vuelve al diagrama de flujo de la primera versión, con flechas que se encienden
al pasar el ratón, sobre los datos del arca. Las librerías de dibujo están en
`vendor/` y el generador las incrusta en cada HTML. Se conservan la primera
plantilla, [plantilla.html](plantilla.html), y la de bloques de texto,
[plantilla_arca.html](plantilla_arca.html). No se editaron notas históricas,
implementaciones Lean, conversaciones ni fichas OEIS. Los HTML, el generador
y la base anteriores se respaldaron antes de sustituirlos; la auditoría
registra las huellas de las tablas conservadas.
