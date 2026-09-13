# Estado para continuar — 13-09-2026

**Objetivo:** `phi=lim a(n)/2^n=1`. P0, depuración local, terminó;
P1–P3 siguen abiertos. La próxima tarea es **P1: completar el reloj global**.
No hace falta releer la historia para empezar.

## Objeto y límites que deben conservarse

`T(x)=x/2` si es par, `(3x+1)/2` si es impar (A014682).
`a(n)` cuenta clases módulo `2^n` que funden hasta n con igual conteo
impar; nuevas en n: `a(n)-2a(n-1)`. OEIS usa `b(n)=a(n+1)-2a(n)`.
El CLI usa el mapa **clásico**. Los pasos mixtos OEIS empiezan en 1.

Para el conjunto F de fusiones balanceadas, `densidad inferior(F)>=phi`;
la unión creciente no prueba `phi=d(F)`. Igual altura **finita** requiere
convergencia y controlar primeras llegadas a 1. Pandas sólo da su
implicación bajo terminación y `Res<3`. El nombre histórico «Gao–Wu» no
sustituye estas hipótesis. La aprobación OEIS no demuestra la densidad.

Cadena: núcleo `{v,3^k*v+c}` y frontera de gap positivo en k=0; el bit
es paridad del **ancla**, no del menor. `(1,1)` con bit 1 absorbe clases.
En una excursión se parte de `(2,c0)` con bits justos independientes;
`tau` es la primera llegada a k=1, **no la fusión**.

## Base disponible y obstáculos

- **Mangostas:** ley exacta de rachas; reloj de n mixtos O(n log n).
- **Gacelas:** supervivencia y control del producto. Con `u0=c0/9`,
  `u_tau=Pi_tau*u0+W_tau`; falta controlar W en la salida.
- **Corolario escrito:** `P_(2,c0)(tau>t)<=C sqrt(log(t+2)/(t+1))`,
  uniforme en c0. Controla una excursión interior, no los tramos de frontera.
- **Erizas:** descarta contracción uniforme en todas las escalas y tiempos
  grandes, incluso L2 en todo un sector lineal. Escala fija no queda descartada.
- La revisión local 12 existe; su reloj O(n) usa una media medida y no se
  adopta. Los argumentos probabilísticos no están íntegramente formalizados.
- Ni `p_i→0` implica absorción incompleta ni momentos a tiempo fijo se
  trasladan automáticamente a salida condicionada. El cambio armónico
  hacia delante no es la reversión ni el condicionamiento a supervivencia futura.

## Siguiente trabajo y criterio de cierre

1. **P1:** abrir [Matematica.md, §3](depuracion/coherencia20260913/Matematica.md#3-corolario-del-reloj-de-mangostas-y-gacelas).
   Especificar tiempos de entrada, salida y reinicio; añadir los tramos
   k=0,1 al reloj interior. Contrastar las transiciones con `cadenakc.lean`.
   Cierre: cota del reloj global con dominio y dependencia del arranque explícitos.
2. **P2:** buscar M finito y p>0 uniformes tales que
   `P(|W_tau|<=M | tau>T(c0))>=p`, para un horizonte declarado de orden
   `log(2+|c0|)`. Cierre: prueba bajo la ley real o familia que refute
   uniformidad. Detalle y pago del producto: la misma nota, §4.
3. **P3:** controlar los arranques reales c_i y demostrar divergencia de
   la suma de riesgos condicionales; ensamblar Markov fuerte y
   Borel–Cantelli sin asumir la recurrencia buscada.

Para ensayos P2: ambos signos, semillas pequeñas, potencias de 2 y 3 y
vecinos, congruencias adversarias. Declarar horizonte y ventana; separar
supervivencia, salida y censura. Una mediana marginal no basta.

## Registro y entrega

Catálogo: `afirmaciones.db`, 216 filas; fuente vigente
`depuracion/coherencia20260913/registro.json` + `guardarafirmaciones.py`.
Los IDs de fichas antiguas no coinciden siempre con filas actuales:
interpretar `depuracion/veredictos.jsonl` por enunciado literal.
`respuestas.db`: 1.957 mensajes hasta 24-08; faltan fuentes de septiembre.

[Auditoría y controles](depuracion/coherencia20260913/LEEME.md): 24 controles
pasaron, nueve Lean. Hay cambios locales sin commit/push; `revision12_adv1/`
era preexistente sin seguimiento: preservarlo. Los tres drafts siguen
pendientes en la última observación; [publicación](../zootheorem/PLAN_INVESTIGACION.md).
Al cerrar una pieza, actualizar esta ficha, registro y plan público (P4).
