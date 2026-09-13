# Reglas del laboratorio

## Arranque y contexto

Leer **sólo [ESTADO_INVESTIGACION.md](ESTADO_INVESTIGACION.md)** después de
estas reglas. Si ya se proporcionaron en la sesión, no releerlas.
Abrir luego únicamente el archivo o sección que requiera la tarea.
`RutaTeoremas.md` es un índice opcional; `CLAUDE.md` remite aquí.
No precargar bitácora, derivados, actas, transcripciones ni todo SQLite.
Buscar con `rg -n` y leer rangos cortos; ampliar cuando una dependencia lo exija.
El archivo histórico conserva decisiones antiguas, no instrucciones vigentes.

## Trabajo y rigor

- Antes de editar: `git fetch origin` y revisar `git status -sb` en cada
  repo afectado. Preservar cambios locales e históricos; no publicar por
  el solo hecho de actualizar documentación.
- Trabajo local sin subagentes salvo petición explícita del usuario.
- Python sencillo, cuatro espacios, nombres en español; conservar las
  implementaciones independientes. Preferir enteros o `Fraction` para
  afirmaciones exactas. Scripts con parámetros explícitos, sin depender de `input()`.
- Declarar mapa, dominio, índices, unidades, ley y condicionamiento.
  Distinguir prueba escrita, formalización, conteo exacto y medición.
  Un barrido finito no es una prueba universal; cotejar también bordes.
- Para afirmaciones matemáticas, contrastar una derivación o cálculo
  independiente y Lean cuando corresponda. Si la formalización es parcial,
  declarar el tramo pendiente. Lean certifica el enunciado, no su interpretación.
  Comprobar `lean --version` y `#print axioms`; evitar `sorryAx`.
- Los resultados propios conservan nombres de animales en femenino;
  consultar el índice histórico antes de asignar otro.
- Mirar parámetros antes de ejecutar o importar experimentos antiguos:
  algunos lanzan barridos al importar. No repetir censos caros por cambios
  documentales. En Windows usar `python -B -X utf8`; cuidar cp1252 en Sublime.

## Archivos y verificaciones

`collatz.py` y `main.py`: mapa clásico y CLI. `depuracion/`: fichas,
verificadores y actas. El compañero `../zootheorem/` publica papers,
`seqs/`, `verify/` y `lean/mirror_theorem.lean`. Consultar su plan sólo
si se trabaja en publicación. No hay build, linter ni CI centralizados.

Validar lo afectado; el conjunto acotado está en
`depuracion/coherencia20260913/ejecutar_controles.py`. Para documentación,
comprobar conservación y enlaces; no relanzar ese conjunto por rutina.

## Cierre y mantenimiento

Actualizar el estado breve **sustituyendo** lo superado: resultado, límite,
siguiente acción y evidencia. Mantenerlo en unas 600 palabras; llevar
pruebas y sesiones largas a notas temáticas enlazadas, sin duplicarlas.
Cambios de afirmaciones: registro versionado y generador, no sólo SQLite.
`respuestas.db` es captura literal; nunca reconstruir conversaciones.
Describir cambios y validación en español; conservar evidencia histórica.
