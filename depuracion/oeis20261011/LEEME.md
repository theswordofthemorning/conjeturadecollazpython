# OEIS: tres fichas nuevas en *proposed* — 11-10-2026

Enviadas por Claude desde la cuenta del usuario (Omar Said), con su
autorización explícita de esta sesión: «generar las 3 nuevas fichas,
controlar Chrome, enviarlas y dejarlas en estado proposed». El usuario
prefirió fichas nuevas a las correcciones de A398792 y A398793 que
proponía [PENDIENTE_20261010.md](../../papers/oeis/PENDIENTE_20261010.md);
esas correcciones siguen pendientes y sin enviar.

## Estado comprobado al terminar (11-10, 21:43 EDT)

Panel «My Drafts (3)», copiado de la página:

| Ficha | Estado | Revisión al proponer | Qué es |
|---|---|---|---|
| [A400983](https://oeis.org/draft/A400983) | proposed | #4 | tiempo del primer encuentro de A078417(n) y A078417(n)+1 bajo el mapa clásico |
| [A400984](https://oeis.org/draft/A400984) | proposed | #3 | k > 1 cuya trayectoria bajo T (A014682) contiene k+1 («near-cycles» de Rozier–Terracol) |
| [A400985](https://oeis.org/draft/A400985) | proposed | #3 | racha más larga de alturas iguales en [1, 2^n) (la L de la tabla de Wu) |

*Proposed* significa en revisión, no aprobada. Se reservaron exactamente
tres números (A400980–A400982 son de otro autor). Cupos: 3 de 3 ocupados.

## Por qué estas tres

Lo que OEIS viene aceptando (A400486, A400487, edición de A078441) son
objetos de la literatura sin parámetros propios, con una conjetura
publicada y enlazados con fichas existentes. El rechazo NOGI del 24-09
([acta](../oeis20260924/LEEME.md)) castigó parámetros arbitrarios y
variantes de una misma idea. Por eso se eligieron tres objetos distintos:

1. **A400983** completa A078417 (dice *cuándo* se encuentran sus pares;
   A078417 dice *quiénes*). Era la propuesta única del 24-09
   (`../../../zootheorem/drafts/PROPUESTA_ENCUENTRO_20260924.md`), nunca
   enviada; se reescribió remitiendo a A400486 y quitando el comentario
   sobre A398792. Nuevo: **a(n) nunca vale 4** (prueba por casos en
   [sin_cuatro.py](sin_cuatro.py)).
2. **A400984** viene de Rozier y Terracol, *Paradoxical behavior in
   Collatz sequences* (arXiv:2502.00948 v5, apéndice B; PDF en
   `lecturas/`). Su compañera A393502 (inicios paradójicos, Ralf
   Stephan, feb-2026) ya está aprobada, pero la lista de los 21 casi
   ciclos no estaba en OEIS. Es la ecuación T^j(k) = k+1, vecina de la de
   los ciclos (T^j(k) = k). No hay más términos bajo 2,8·10^19 (lema B.2
   y teorema 5.3 del artículo).
3. **A400985** es la columna L de la tabla de Wu (1992), cuya columna K
   es A400487. La conjetura de Wu (L → ∞) equivale a que A078441(k)
   exista para todo k. a(27)–a(31) salen de la b-file de A078441
   (Hofmann).

Ninguna cita nuestros artículos ni dice «proved» sobre resultados propios.
No se dejó nota en la discusión.

## Descartadas

- **Inicios paradójicos** de Rozier–Terracol: ya es A393502.
- **Pares con igual número de mitades** (A006666): coinciden con A078417
  hasta 200 000 (es la pregunta de Gao recogida en A400486).
- **Menor m con tiempo de encuentro n**: variante de A400983; enviarla a
  la vez repetiría el error del 24-09.

## Verificación

- [calcular.py](calcular.py) (`--limite-encuentro 1000000 --limite-casi 1000000`,
  31 s; [salida](calcular_salida.txt)):
  - A078417 recalculada coincide con la b-file oficial;
  - A400983 coincide con la b-file preparada en zootheorem (10 000);
  - a = 3 sii m ≡ 4 (mod 8); el único valor ausente entre 3 y 39 es el 4;
  - la forma de Lagarias de Gao coincide con {A078417 : a ≤ log2 m};
  - A400984 reproduce los 21 pares (j, n) del apéndice B, y todos los
    k > 3 son paradójicos;
  - A400985: cálculo directo (n ≤ 22) = b-file de A078441 (n ≤ 31) =
    tabla del artículo III (n ≤ 26); L(2^30) = 176, como Wu.
- [sin_cuatro.py](sin_cuatro.py) `--modulo 64`
  ([salida](sin_cuatro_salida.txt)): sólo las clases 4 (mod 8) cumplen
  f^4(m) = f^4(m+1), y ya se encuentran en el paso 3; no hay soluciones
  aisladas.
- [verificar_fichas.py](verificar_fichas.py) `--carpeta .`
  ([salida](verificar_fichas_salida.txt)): ejecuta tal cual cada `%o`,
  lo compara con `%S`, comprueba offsets, ejemplos y el límite de 260
  caracteres.
- Duplicados (API de OEIS, 11-10): sin resultados para los datos de las
  tres; el control Fibonacci devuelve A000045.
- Envío: el campo del formulario tenía el mismo SHA-256 que
  `A40098x_interno.txt`. Tras guardar, el texto del servidor coincide
  con él, una vez unidos `%S/%T/%U` y quitado `changed` de `%K`.

`ficha_*.txt` son los borradores con `A000000`; `A40098x_enviar.txt` y
`A40098x_interno.txt`, lo enviado (con el número y en el formato del
editor, sin número en cada línea).

## Si responden los editores

Seguir `../../../zootheorem/drafts/PROCEDIMIENTO_OEIS.md`. Hace falta
autorización del usuario para contestar o editar.
