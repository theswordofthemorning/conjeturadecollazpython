# Pendientes de la tanda de YAH y de su certificación

19-10-2026. Lo que está en marcha y lo que queda por hacer alrededor de la
tanda de YAH sobre la escalera del piloto ([LEEME.txt](LEEME.txt)).

## En marcha

Estado a las 21:00 del 19-10-2026. Las dos tandas corren a la vez, con
6 solucionadores cada una y nice 10. Usan unos 2 GB de RAM y el procesador
está entre 90 y 97 °C. Ninguna se ha caído. Los resultados parciales están
en `resultados/` y `resultados_debilitadas/`, sin la carpeta `trabajo/`.

- **Peldaño 5 completo** (`lanzar.sh --fondo --sin-calibracion`, lanzada a
  las 15:54). Pasadas de 120, 900 y 3600 s por forma, con 36 formas.
  - Al primer segundo cayó `L t t R -> L f f f R`. Desde entonces quedan
    11 reglas estrictas, sin más avances.
  - Las formas pequeñas dan UNSAT. natural d4 dio UNSAT en las dos
    orientaciones con 900 s.
  - Las naturales d5 y d6 y las árticas d4 y d5 llegan al tope de 900 s.
    Ya corre la pasada de 3600 s; acabaría hacia las 6:00 del 20-10.
  - Lo más probable es «sin prueba», con el núcleo de mahler y
    collatz-T-5or7mod8 intacto. Eso no es un contraejemplo.

- **Escalera de G debilitadas** (`lanzar.sh --fondo --debilitadas`,
  lanzada a las 16:53). Corre a la vez que el peldaño 5, con su propia
  carpeta de trabajo, y se para con `parar.sh --debilitadas`.
  - Las versiones son G_A2…G_A5 (la rama A no actúa en 0 mod 2^k) y
    G_B4…G_B7 (la rama B no actúa en −1 mod 2^k).
  - `debilitar.py` las genera. Comprueba la simulación en todo z < 2^12
    (0 fallos) y la lectura con el lector de YAH ([debilitadas.json](debilitadas.json)).
  - Objetivo: el k donde la cascada deja de dar QED, y qué reglas resisten
    ahí.
  - **Primer resultado parcial:** ya se resiste G_A2, la versión más débil.
    - Caen al momento las dos reglas con L. Quedan 11 reglas: las 9 X,
      `t f R -> a1 t R` (z = 4m+2 → 6m+3) y `t t t R -> a2 a2 R` (la
      rama B entera).
    - La pasada de 900 s acabó sin avance. La de 3600 s está en curso.
    - El peldaño 4 (sólo la rama B) dio QED en segundos. Basta añadirle la
      rama A en la clase más estrecha para frenar la cascada. Apunta a que
      lo difícil para estas formas es la mezcla de las dos ramas.
  - Si G_A2 acaba «sin prueba», conviene revisar el plan antes de que siga
    con G_B4 y el resto (con pasadas más cortas, u otra escalera que
    debilite la rama B en vez de la A).

## Pendientes

1. **Traductor de certificados YAH → Lean.** YAH busca, no certifica.
   - Cada quitada de YAH imprime las matrices de la interpretación. Su validez
     es una cuenta finita de desigualdades matriciales, sobre los naturales o
     en max-plus/min-plus.
   - Hay que pasar esa salida a un `.lean` que la compruebe con `decide`,
     sin `sorry`, `axiom` ni `native_decide`.
   - Primera prueba: los QED de calibración de los peldaños 1 a 4, con
     matrices pequeñas y sacados en segundos.
   - Después, todo QED que den el peldaño 5 o la escalera debilitada.
   - Usa un solo proceso Lean, así que no compite con la tanda.

2. **Equivalencia SRS ↔ función para las debilitadas.**
   - Para G ya está probada en Lean (`piloto_iff`, [JudasPiloto.lean](../../JudasPiloto.lean)).
   - Para G_Ak y G_Bk sólo está comprobada por simulación.
   - Hay que extender la prueba a la familia, con las reglas por sufijo y
     las de L para los z pequeños.

3. **Pruebas a mano de los peldaños débiles.**
   - G_A2 y las primeras de cada familia tienen órbitas muy cortas: como
     mucho 8 pasos en la muestra de G_A2.
   - Puede que admitan una medida sencilla, demostrable en Lean sin YAH.
   - Servirían para contrastar los QED automáticos.

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
  pequeña basta. Encaja con la obligación abierta de Perdices: una
  restricción aritmética conjunta para historias no periódicas. Lo difícil
  parece ser cómo se encadenan las ramas, no cada rama.
- **Lo que sí sirve como herramienta.** YAH busca medidas lineales por
  matrices para sistemas finitos de reescritura. Si una restricción de
  Perdices se puede escribir como un sistema así (por ejemplo, restringida a
  historias que respetan un patrón finito), la tanda de aquí puede probarla
  o descartar formas pequeñas en horas. `lanzar.py` acepta cualquier
  sistema en `sistemas/`.
- **Lo que no prueba.** Un UNSAT descarta sólo una forma concreta (tipo,
  dimensión y ancho), no una cota. Y un QED de YAH todavía no es una prueba
  certificada mientras no exista el traductor a Lean (pendiente 1).
