# INVENTARIO Y PLAN DE DEPURACIÓN — 09-08-2026

*(Análisis pedido por el usuario: catálogo esencial/necesario/prescindible,
redundancias, y qué cuesta contexto de verdad. Las ACCIONES de riesgo se
proponen, no se ejecutan — decide el usuario.)*

## La clave que ordena todo el análisis

**El contexto de una sesión NO lo gasta el número de ficheros: lo gasta lo
que se inyecta y lo que se lee.** Un `.py` que nadie abre cuesta CERO.
El costo fijo de cada arranque es:

| se carga siempre | líneas | KB | veredicto |
|---|---|---|---|
| `CLAUDE.md` (inyectado ENTERO) | **3.466** | **202** | **EL problema. Único lever grande** |
| `MEMORY.md` + memorias | ~30 | ~5 | irrelevante |
| `RutaTeoremas.md` (se lee al arrancar) | 432 | 30 | sano — el frente arriba, historia abajo |
| `bitacora.md` (se lee SOLO la entrada de arriba) | 2.493 | 148 | sano si se respeta leer sólo el tope |

**Borrar `.py` viejos no ahorra contexto. Adelgazar `CLAUDE.md` sí.**

## El catálogo (raíz: 62 .py · 15 .txt · 14 .lean · 3 .md · 3 .db · 1 .json)

### ESENCIALES (perderlos = daño real; todos en git ✓)
- Las 3 bases: `afirmaciones.db` (170/46/20/33/49), `respuestas.db`
  (1.191 mensajes — para 355 es LA ÚNICA copia), `hilos.db`.
- Los 3 `.md` + `sucesiones.txt` + las actas (`actarevision0908.txt`,
  `teoremade*.txt`, `lemadepandas.txt`, `notamoscas.txt`, `maquinaria.txt`).
- Los **14 `.lean`** (lo único DEMOSTRADO por máquina) y los `.py` del
  programa vivo de la cadena: `paseodeladeuda`, `retorno11`, `oscilacion`,
  `lamperti`, `minorizacion`, `accesibilidad`, `empalme`, `pisoremedido`,
  `pisoporvisita`, `cadenaqnr`, `diferenciales`, `nuevasfusion`,
  `identidadexacta`, `masasdeclase`, `subrenovacionc`, `matriztransferencia`,
  `retornoslambda`, `aranas`, `moscas`, `dispersionc`, `empujarb`,
  `flecosr`, `estratoscadena`, `segundocamino`, `auditoria_rigor`.
- `records.json`, `transcripciones/` (11 zips), `depuracion/` (las actas de
  los 100 veredictos — procedencia irreemplazable).

### NECESARIOS (registro y reproducibilidad; en git ✓; costo de contexto 0)
- Los 7 `verificar_*.py` + `reimpl`, `cruzarecords`, `pinzaciclos`,
  `clasesfusion`, `clasesparalelo`, `paradacoef`, `atacacst*`, etc. —
  rederivaciones y vías cerradas CON su porqué (la doctrina los exige).
- Los resultados de barridos caros: `resultado_paralelo_k32.txt`,
  `atacacst2_progreso*.txt`, `franjaeverett_salida.txt` (no re-correr).
- Los 4 que dibujan + `collatz.py`/`main.py` + `guardar*.py`.

### PRESCINDIBLES / REGENERABLES (ya fuera de git; sólo ocupan disco local)
- Los 6 `.html` (32 MB) y 7 `.png` (2,5 MB): salidas de plotly,
  regenerables corriendo los 4 scripts. Borrables cuando quieras.
- `__pycache__`: borrado hoy (regenerable, gitignorado).

### FUERA DE GIT Y **NO** PRESCINDIBLES (el punto frágil)
- `lecturas/*.pdf` (Terras 1976, Tao 2019, las 2 bibliografías de
  Lagarias, de Bruijn, el libro de 2010 —21 MB—): fuentes leídas,
  **sólo en local, y ya se perdieron una vez**. Con copyright: **NO
  pueden subirse al repo público**. → Recomendación: respaldo PRIVADO
  fuera del repo (otro disco / repo privado / nube personal).

## ⚠ EL HALLAZGO DE RIESGO INVERSO (decidir pronto)

`lecturas/latourette2007/` — **51 páginas de la tesis escaneada están
TRACKEADAS en git, y el repo ahora es PÚBLICO**: es la obra de otra
persona redistribuida sin permiso, y justo acabamos de escribir a
Moravian. → Recomendación: **sacarlas del repo público** (quitar del
índice + gitignore; conservar copia local/privada), o pedirle permiso a
Fraboni en el hilo ya abierto. No las borro yo: decisión del usuario.

## REDUNDANCIAS REALES DETECTADAS (pocas, y ninguna urgente)

1. **`CLAUDE.md` mezcla doctrina viva con archivo histórico** — es su
   diseño declarado, pero a 3.466 líneas el archivo ahoga a la doctrina.
   **LA PROPUESTA GRANDE** (para una sesión fresca, con tu ok): partirlo
   en `CLAUDE.md` (reglas + doctrina + puntero de arranque, ~700 líneas)
   y `archivohistorico.md` (todo lo demás, greppeable, NO inyectado).
   Ahorro: ~60% del costo fijo de CADA sesión futura. Riesgo: bajo si el
   corte es mover-sin-borrar y una pasada de punteros.
2. **Conteos desfasados otra vez** (el modo de fallo documentado): el
   `CLAUDE.md` dice 52 `.py` y hay **62**; dice 5 `.lean` en una sección
   vieja y hay **14**. Se corrige en la misma pasada del punto 1.
3. `empalme.py` / `pisoremedido.py` / `pisoporvisita.py` se solapan en
   parte (los tres miden pisos) — se dejan: cada uno responde una
   pregunta distinta y el solape es barato. Igual `lamperti`/`oscilacion`.
4. No hay ficheros muertos sin función detectados: la purga del 01-08 ya
   hizo ese trabajo y lo nuevo está todo vivo.

## Qué se hizo hoy y qué queda a tu decisión

- HECHO: `__pycache__` fuera; este inventario al repo.
- ⇢ APLICADO (1), misma tarde: `lecturas/latourette2007/` fuera del
  árbol público (copia local intacta; `lecturas/` entera al gitignore).
  *Nota: las páginas siguen en el HISTORIAL de git — purgarlas del
  historial exige `git filter-repo`; decisión aparte del usuario.*
- ⇢ APLICADO (2), misma tarde, con el diseño del usuario (SISTEMA DE
  DERIVADOS): `CLAUDE.md` pasó de **3.466 a ~390 líneas** (tronco:
  doctrina viva + resúmenes `[D-nn]`) y `derivados.md` guarda las 10
  ramas ÍNTEGRAS (3.172 líneas movidas, no borradas). El costo fijo de
  cada sesión futura baja ~89%.
- ⇢ APLICADO (3), misma tarde: respaldo local
  `Desktop\lecturas_respaldo_2026-08-09.zip` (26,6 MB: lecturas + los
  3 PDF de la raíz). El destino final (nube/disco) es del usuario.
