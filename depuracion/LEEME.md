# Depuración total del repo — LA REGLA DE LOS TRES sobre los 100 ítems

Encargada por el usuario el 02-08-2026: **verificar cada afirmación y cada
constante de `afirmaciones.db` antes de publicar nada**, porque los números los
hizo Opus 5 cometiendo error sobre error. Por cada ítem van tres agentes: uno lo
demuestra en **Lean 4** (o dictamina `NO_FORMALIZABLE` con su porqué), otro lo
calcula en **Python desde cero sin ver al primero**, y un **comparador
adversarial** revisa a los dos con la lista de la casa (¿enunciaron lo mismo?
¿coinciden por premisa compartida? ¿promedio o cota? ¿borde sin probar?).

## Qué hay aquí

| fichero | qué es |
|---|---|
| `plan.json` | los 100 ítems (80 afirmaciones + 20 constantes) repartidos en 25 lotes de 4, ordenados por cuánto sostiene cada pieza (primero el andamio de Terras) |
| `veredictos.jsonl` | una fila por ítem dictado: el trabajo completo de los tres agentes. **Este fichero es el registro que manda** |
| `fichas/` | la ficha literal que recibió cada agente (enunciado, cuantificador, estado, fuente, notas) — sin esto los veredictos no son reproducibles |
| `lean/` | los `.lean` que escribieron los agentes 1 (compilan con el núcleo, sin Mathlib) |
| `py/` | los scripts de los agentes 2 y de los comparadores (`*_comp.py`) |

## Historia

La primera pasada (sesión `429f4e04`, 02-08-2026 por la mañana) dictó los lotes
1, 2 y 3 y murió por límite de sesión con la mega-tanda A en vuelo (21 de 72
agentes terminados, ningún comparador). Los resultados parciales se rescataron
de los journals de los workflows y se reutilizan como caché en la relanzada —
el trabajo pagado no se paga dos veces.

## Marcador

Se actualiza en cada tanda; la cifra que vale es la de `veredictos.jsonl`
(`una fila = un ítem dictado`). Veredictos posibles del comparador:
`CONFIRMADA / EXAGERADA / CORREGIDA / REFUTADA / NO_DECIDIBLE`.

**Las correcciones dictadas NO se aplican solas**: aplicarlas a
`afirmaciones.db` y al `CLAUDE.md` es un paso aparte, que se hace leyendo la
fila entera — el veredicto del comparador manda, pero su `correccion_exacta` se
copia literal, no de memoria.
