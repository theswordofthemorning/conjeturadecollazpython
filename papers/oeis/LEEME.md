# Borradores OEIS: Gao, Wu y Garner

**04-10-2026: A400486 aprobada** por Sean A. Irvine (revisión #8, 04-10
18:29 EDT). En la #7 añadió a(29) = 216253629 y a(30) = 435078205, con su
`%E`. Los demás campos coinciden con
[borrador_1_gao.txt](borrador_1_gao.txt); OEIS sólo añadió `new` a `%K`
([ficha aprobada](../../depuracion/oeis20260917/A400486_20261004_aprobada.txt)).
No hemos recalculado esos dos términos; cumplen la cota de Gao
`a(n+1) >= 2*a(n)`. A400487 sigue en *proposed*: Jason Yuen añadió `more`
el 02-10 y la discusión está vacía. La web muestra «My Drafts (1)»: 1 de 3
cupos ocupado.

**30-09-2026: A078441 aprobada** (revisión #40, 29-09 23:52), con el
bloque firmado y los enlaces
([ficha aprobada](../../depuracion/oeis20260917/A078441_20260930_aprobada.txt)).
A400486 y A400487 siguen sin aprobar; en la vista pública figuran como
«allocated» ([captura](../../depuracion/oeis20260917/A400486_A400487_20260930_publico.txt)).
No se ha consultado el panel de cupos. Lo que sigue es el estado del 28-09.

**Estado comprobado el 28-09-2026, 15:20 EDT: las tres fichas están en
*proposed*.** Se respondió a Marcus y se agruparon las firmas de A078441
(#37, reenvío #38), con autorización del usuario. Conservados el programa
PARI de Barbera y los retoques de Marcus. Gao y Wu no tienen preguntas
pendientes. [Respuesta, cotejos y capturas](RESPUESTA_20260928.md).

Los envíos originales fueron el 27-09 (16:42–16:55 EDT), en el orden
pedido: 1 Gao, 2 Wu, 3 Garner. *Proposed* significa en revisión, no aprobado.

| Ficha | Qué es | Texto enviado el 27-09 | Estado del envío original a las 16:56 EDT |
|---|---|---|---|
| [A400486](https://oeis.org/draft/A400486) | Gao: la tabla 3 de Gao (1993) en cuentas, n = 1..28 | [borrador_1_gao.txt](borrador_1_gao.txt) | *proposed*; Michel Marcus añadió `more` |
| [A400487](https://oeis.org/draft/A400487) | Wu: la cuenta K(2^N) de Wu (1992), n = 1..26 | [borrador_2_wu.txt](borrador_2_wu.txt) | *proposed*; Marcus pasó la cita de Krasikov–Lagarias al formato arXiv |
| [A078441](https://oeis.org/draft/A078441) #31 | edición: conjetura de Garner, tabla 1 de Gao, Wu y enlaces | [borrador_3_A078441.txt](borrador_3_A078441.txt) | *proposed* |

Los tres borradores conservan los textos del 27-09, con los retoques de
Marcus de ese día. Para A078441, el contenido actualizado está en la
[captura interna del 28-09](../../depuracion/oeis20260917/A078441_20260928_interno_guardado.txt).
OEIS añade la palabra clave `changed` y reparte DATA en `%S/%T/%U`.
La cuenta sigue con 3 de 3 cupos ocupados; las correcciones de
A398792–A398795 siguen esperando.

## Cómo se envió

1. En «My Drafts» había 0 borradores. La propuesta del encuentro del 24-09
   (`../../../zootheorem/drafts/PROPUESTA_ENCUENTRO_20260924.md`) **nunca se
   envió**: no está en OEIS.
2. Se repitió la búsqueda de duplicados. `1,4,11,29,65,145,305,641,1317` y
   `4,13,32,69,147,303,620,1270,2618` dieron «No results»; el control
   Fibonacci dio A000045.
3. Se pidieron dos números con `/edit/allocate` (A400486–A400487), para poner
   la referencia cruzada entre las dos fichas antes de enviarlas.
4. El texto se cargó en el formato interno. Antes de guardar se comprobó que
   el campo tenía el mismo SHA-256 que el borrador. Después de guardar se
   releyó el texto del servidor. En A078441, el diff de la revisión #31
   muestra sólo 2 `%C` firmados, 4 `%H` y la línea `%Y` ampliada.
5. Se pulsó «These changes are ready for review». En «My Drafts» las tres
   aparecen como *proposed*.

## Cambios hechos el mismo 27-09, antes de enviar

- **Sin b-files.** Repetían DATA: los 28 y 26 términos caben en tres líneas,
  y OEIS pide b-files sólo para lo que no cabe. Siguen en esta carpeta.
- **Gao.** «positive integers» en `%N`; `3*x+1`; «In the terminology of Gao
  (1993), m and m+1 then coalesce»; aclarado el ejemplo del 14.
- **Wu.** «Jia-Bang Wu»: el DOI resuelve a CNKI con el autor 邬家邦. También
  `3*x+1`.
- **A078441.**
  - **Garner.** El comentario ya no dice «that is, a(n) exists for every n».
    Garner mide la altura con T (según la reseña de zbMATH), y la conjetura
    que implica que a(n) existe es la forma que recuerda Gao: misma altura
    con f y mismas mitades.
  - **«first seven runs».** La tabla 1 de Gao tiene ocho filas. La octava,
    349 desde 9749626154, está fuera de la b-file.
  - **Wu** va como `%H` con el DOI; Lagarias, con «entries 68, 72 and 188».
  - **Comentarios firmados**, porque la ficha es de otro autor.
- **Enlaces comprobados.** Los DOI de Gao, Garner y Wu, y los arXiv de
  Lagarias y de Krasikov–Lagarias.

## Si responden los editores

Seguir `../../../zootheorem/drafts/PROCEDIMIENTO_OEIS.md`:

1. Leer la discusión.
2. Contestar una sola vez con «Add note to discussion».
3. Si la ficha volvió a *editing*, reenviarla.
4. Comprobar la fila en «My Drafts».

Ante un NOGI, usar los argumentos de la sección siguiente. No contestar ni
editar sin autorización del usuario.

## Por qué sirven (la objeción NOGI)

El 24-09 Irvine rechazó tres fichas por «not of general interest» y preguntó
cómo ayudaban con Collatz. Estas son distintas en lo que él objetó:

- **Salen de la literatura, sin parámetros propios.** La 1 es, en cuentas
  exactas, la tabla 3 de Gao (1993); la 2 es la cuenta de Wu (1992). Los
  cortes (`n < 2^k − 1`, `[1, 2^N)`) son los de los autores.
- **Cada una lleva una conjetura publicada sobre su límite.** Gao:
  `a(n)/2^n -> 1`. Wu: la proporción de enteros en rachas tiende a 1.
- **La de Wu toca Collatz de frente, sin usar nada nuestro.** Si
  `a(n)/2^n -> 1`, los enteros que llegan a 1 tienen densidad 1 (cada k
  contado llega a 1). Eso está abierto: la mejor cota es `x^0,84`.
- **La 3 no crea variantes.** Añade a A078441 lo que ya dice la literatura:
  la conjetura de Garner y que sus primeros récords son la tabla 1 de Gao.

Ninguna dice «proved». Las líneas que enlazan nuestros artículos están aparte
(abajo) y sólo se añaden cuando el artículo tenga DOI y el usuario lo decida.
Dado que los cupos están llenos, esas líneas irán como ediciones nuevas
cuando se liberen.

## Líneas opcionales, tras publicar los artículos

Sustituir `XXXXXXX` por el DOI de Zenodo (o de la revista). El nombre es el
de los artículos, Omar Javier Said Duran; `%A` lleva el de la cuenta OEIS,
Omar Said.

A400486 (Gao):

```text
%C A400486 Said Duran (2026) gives a proof, formalized in Lean 4, that a(n)/2^n -> 1, together with the form recorded by Lagarias.
%H A400486 Omar Javier Said Duran, <a href="https://doi.org/10.5281/zenodo.XXXXXXX">Consecutive integers coalesce with density one under the Collatz map</a>, 2026.
```

A400487 (Wu):

```text
%C A400487 Conversely, a(n)/2^n -> 1 if the integers that reach 1 have natural density 1: by Said Duran (2026), consecutive integers coalesce with density 1 in the sense of Gao (see A400486), and coalescing integers that reach 1 take the same number of steps.
%H A400487 Omar Javier Said Duran, <a href="https://doi.org/10.5281/zenodo.XXXXXXX">On two conjectures of Wu on consecutive integers of the same height in the Collatz problem</a>, 2026.
```

A078441: las dos líneas del final de su archivo.

## Diferencia con A398792

A400486 no es A398792 con otro nombre.

| | A398792 | A400486 |
|---|---|---|
| Mapa | el atajo T (A014682) | el clásico (A006370) |
| Qué cuenta | residuos `r < 2^n` | enteros `m < 2^n − 1` |
| Condición al encontrarse en `<= n` pasos | los mismos impares | las mismas mitades |
| ¿Excluye el 1? | no | sí, hasta el encuentro |
| n = 4 | A398792(4) = 3 | a(4) = 1 |

Está en `%Y` como pariente.

## Verificación

- [verificar_borradores.py](verificar_borradores.py) hace cinco
  comprobaciones:
  - ejecuta tal cual el programa de cada ficha y lo compara con `%S`;
  - coteja las b-files locales con `%S`;
  - comprueba el desfase `%O` y las fórmulas `%F`;
  - recalcula los ejemplos;
  - coteja las cifras de los comentarios.

  Usa las b-files oficiales de A078417 (copia en
  `../../depuracion/oeis20260924`) y de A078441 (`b078441_oficial.txt`,
  bajada de oeis.org el 27-09, licencia CC BY-SA 4.0). Resultado: OK, también
  sobre los textos enviados.
- [terminos_oeis.py](terminos_oeis.py) calcula los términos
  ([salida](terminos_oeis_salida.txt)). Es independiente de los programas
  de las fichas y de `revision20260927/`, y coincide con ellos.
- Los términos de Gao reproducen los 21 valores de su tabla 3. Los de Wu
  reproducen `d(2^10) = 620/1023` y el crecimiento que él observó.
