# Pendientes de la tanda de YAH y de su certificación

19-10-2026. Estado y pendientes de la tanda de YAH sobre la escalera del
piloto ([LEEME.txt](LEEME.txt)).

## Estado

Al cierre del diagnóstico no corría ninguna tanda. Resultados y lectura en
[INFORME_YAH.md](INFORME_YAH.md).

- Peldaño 5 y G_A2, con pasadas de 120, 900 y 3600 s: paradas a las 22:26
  del 19-10-2026, sin QED; 11 reglas en cada residuo.
- Diagnóstico de 30 minutos ([PLAN_YAH.md](PLAN_YAH.md)), de 22:43 a
  22:50: calibración 4/4 QED; G_B4 sin prueba, con 11 reglas. Se detuvo
  ahí, como prevé el plan; G_B5…G_B7 no se corrieron.
- En los tres caen sólo reglas dinámicas con L. Las 22 configuraciones
  ensayadas de dimensión ≤ 3 dan UNSAT sobre cada residuo, con alcance
  limitado al tipo, dimensión, ancho y orientación probados. Sin mecanismo
  nuevo, no ampliar la búsqueda de YAH.
- **Corrección de la revisión:** `piloto_iff` formaliza paridades ↔ no parada
  de G, no SRS ↔ G. Este último puente tiene prueba escrita para G y sigue
  pendiente en Lean; para las debilitadas sólo hay cotejo finito.

## Pendientes en orden de trabajo

1. **Auditoría de Nashida sobre G_A2 y G_B4.**
   - Lista de comprobaciones en [PLAN_YAH.md](PLAN_YAH.md) («Nashida: qué
     comprobar antes de ampliar»); especificaciones en
     [ccchallenge20261019](../../../ccchallenge20261019/PLAN.md).
   - Identificar el teorema y cotejar cada hipótesis con las 11 reglas de
     cada residuo, sus orientaciones y las clases de interpretaciones.
   - Resultado esperado: documentar qué barrera se aplica, o qué hipótesis
     falta. Una etiqueta del clasificador o la equivalencia de terminación
     entre sistemas no transporta por sí sola una barrera de certificados.

2. **G_B4 a mano; G_A2 como comparación.**
   - Trabajar en z entero positivo y contar aplicaciones del mapa parcial
     definido en el informe. Los máximos reportados de 14 y 8 pasos para
     z < 2^12 son observaciones finitas, no cotas universales.
   - Buscar una medida que controle también los cambios de rama. Cada rama
     sola tiene la suya: v2(z) en A y v2(z+1) en B. Falta justificar el
     comportamiento de la mezcla para toda semilla positiva.
   - Si aparece un argumento, escribirlo con cuentas exactas y después
     formalizarlo. Si falla una medida candidata, registrar el alcance
     exacto del obstáculo, sin generalizarlo a todas las medidas.

3. **Puente SRS ↔ función, también pendiente para G.**
   - [JudasPiloto.lean](../../JudasPiloto.lean), `piloto_iff`, formaliza
     el patrón de paridades del piloto y la no parada de G. No modela SRS.
   - Para G, formalizar el argumento escrito de
     [J2_MECANISMOS.md](../../J2_MECANISMOS.md), §2; distinguir la simulación
     sobre representaciones de enteros de la terminación del sistema sobre
     todas sus palabras.
   - Para G_Ak y G_Bk sólo hay cotejo por simulación. Falta la prueba general
     y su formalización, incluidas las reglas por sufijo y las de L para
     los z pequeños.
   - Este puente es necesario para trasladar un certificado SRS al mapa;
     no bloquea la auditoría ni la búsqueda de una prueba directa del mapa.

4. **Traductor de certificados YAH → Lean, con menor prioridad.**
   - Cada quitada de YAH imprime las matrices de la interpretación. Su validez
     es una cuenta finita de desigualdades matriciales, sobre los naturales o
     en max-plus/min-plus.
   - Hay que pasar esa salida a un `.lean` que la compruebe con `decide`,
     sin `sorry`, `axiom` ni `native_decide`.
   - Primera prueba: los QED de calibración de los peldaños 1 a 4, con
     matrices pequeñas y sacados en segundos.
   - Retomarlo después de 1 y 2 si aporta al resultado buscado. Hoy sólo
     están los QED de calibración: no hay un QED nuevo de las mezclas que
     justifique adelantar esta tarea.
   - Usa un solo proceso Lean, así que no compite con una tanda.

## Condición para retomar YAH

Sólo plantear una corrida larga si la auditoría o el trabajo a mano aporta
un motivo concreto para una configuración. Registrar sistema y residuo,
tipo, dimensión, ancho, orientación, presupuesto y condición de parada.
Probar esa única configuración; no relanzar automáticamente la cascada ni
subir k por los mismos UNSAT. Ningún resultado actual demuestra igualdad
de dificultad entre G, G_A2 y G_B4 ni imposibilidad de una prueba matricial.

## Contexto

- El piloto está entre Mahler (rama A) y la conjetura 4.14 de YAH (rama B);
  es consecuencia de la 4.12. Detalle en
  [J2_MECANISMOS.md](../../J2_MECANISMOS.md) («Entre Mahler y la 4.14»).
- Lean comprueba pruebas, pero no las busca. El peldaño 5 completo equivale
  a un problema abierto del tipo de Mahler, y ahí lo que falta es la idea,
  no la comprobación.
- Prioridad frente al encargo de Perdices de `CLAUDE.md` (también en Lean):
  sin decidir.

## Para Astra (ruta Perdices)

Notas de lo que podría servir allí, sin tocar nada de Perdices:

- **Dónde se atasca.** Con cada rama sola hay prueba automática. Al
  mezclarlas, aunque una sea muy débil, ninguna de las configuraciones
  pequeñas ensayadas basta: G_A2 (rama A mínima) y G_B4 (rama B mínima)
  coinciden con G en esos resultados, sin que eso pruebe igualdad de
  dificultad. Encaja con la obligación abierta de Perdices: una
  restricción aritmética conjunta para historias no periódicas. Lo difícil
  parece ser cómo se encadenan las ramas, no cada rama.
- **Lo que sí sirve como herramienta.** YAH busca medidas lineales por
  matrices para sistemas finitos de reescritura. Si una restricción de
  Perdices se puede escribir como un sistema así (por ejemplo, restringida a
  historias que respetan un patrón finito), el diagnóstico de aquí la prueba
  o descarta formas pequeñas en minutos. `lanzar.py` acepta cualquier
  sistema en `sistemas/`.
- **Lo que no prueba.** Un UNSAT descarta sólo una configuración concreta
  (tipo, dimensión, ancho y orientación), no una cota. Los QED de YAH
  todavía están pendientes de certificación en Lean (pendiente 4) y el
  traslado de esa certificación al mapa necesita el puente del pendiente 3.
