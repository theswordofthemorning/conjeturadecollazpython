# Pendientes de la tanda de YAH y de su certificación

19-10-2026. Estado y pendientes de la tanda de YAH sobre la escalera del
piloto ([LEEME.txt](LEEME.txt)).

## Estado

No corre ninguna tanda. Resultados y lectura en
[INFORME_YAH.md](INFORME_YAH.md).

- Peldaño 5 y G_A2, con pasadas de 120, 900 y 3600 s: paradas a las 22:26
  del 19-10-2026, sin QED; 11 reglas en cada residuo.
- Diagnóstico de 30 minutos ([PLAN_YAH.md](PLAN_YAH.md)), de 22:43 a
  22:50: calibración 4/4 QED; G_B4 sin prueba, con 11 reglas. Se detuvo
  ahí, como prevé el plan; G_B5…G_B7 no se corrieron.
- En los tres caen sólo las reglas con L, y todas las formas de dimensión
  ≤ 3 dan UNSAT. Sin mecanismo nuevo, no ampliar la búsqueda de YAH.

## Pendientes

1. **Auditoría de Nashida sobre G_A2 y G_B4.**
   - Lista de comprobaciones en [PLAN_YAH.md](PLAN_YAH.md) («Nashida: qué
     comprobar antes de ampliar»); especificaciones en
     [ccchallenge20261019](../../../ccchallenge20261019/PLAN.md).
   - Decide si hay una barrera estructural para los residuos exactos.

2. **Pruebas a mano de las mezclas mínimas.**
   - G_B4 (11 reglas, dos dinámicas) y G_A2 son los sistemas más pequeños
     que resisten. Sus órbitas son cortas: como mucho 14 y 8 pasos en
     z < 2^12.
   - Buscar una medida demostrable en Lean sin YAH, o el motivo de que no
     haya una simple. Cada rama sola tiene la suya: v2(z) en la rama A y
     v2(z+1) en la rama B.

3. **Traductor de certificados YAH → Lean.** YAH busca, no certifica.
   - Cada quitada de YAH imprime las matrices de la interpretación. Su validez
     es una cuenta finita de desigualdades matriciales, sobre los naturales o
     en max-plus/min-plus.
   - Hay que pasar esa salida a un `.lean` que la compruebe con `decide`,
     sin `sorry`, `axiom` ni `native_decide`.
   - Primera prueba: los QED de calibración de los peldaños 1 a 4, con
     matrices pequeñas y sacados en segundos.
   - Sólo hace falta para un QED que importe; hoy sólo están los de
     calibración.
   - Usa un solo proceso Lean, así que no compite con una tanda.

4. **Equivalencia SRS ↔ función para las debilitadas.**
   - Para G ya está probada en Lean (`piloto_iff`, [JudasPiloto.lean](../../JudasPiloto.lean)).
   - Para G_Ak y G_Bk sólo está comprobada por simulación.
   - Hay que extender la prueba a la familia, con las reglas por sufijo y
     las de L para los z pequeños.

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
  mezclarlas, aunque una sea muy débil, ninguna interpretación matricial
  pequeña basta: G_A2 (rama A mínima) y G_B4 (rama B mínima) se comportan
  igual que G. Encaja con la obligación abierta de Perdices: una
  restricción aritmética conjunta para historias no periódicas. Lo difícil
  parece ser cómo se encadenan las ramas, no cada rama.
- **Lo que sí sirve como herramienta.** YAH busca medidas lineales por
  matrices para sistemas finitos de reescritura. Si una restricción de
  Perdices se puede escribir como un sistema así (por ejemplo, restringida a
  historias que respetan un patrón finito), el diagnóstico de aquí la prueba
  o descarta formas pequeñas en minutos. `lanzar.py` acepta cualquier
  sistema en `sistemas/`.
- **Lo que no prueba.** Un UNSAT descarta sólo una forma concreta (tipo,
  dimensión y ancho), no una cota. Y un QED de YAH todavía no es una prueba
  certificada mientras no exista el traductor a Lean (pendiente 3).
