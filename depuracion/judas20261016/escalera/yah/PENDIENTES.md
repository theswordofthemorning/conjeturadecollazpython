# Pendientes de la tanda de YAH y de su certificación

19-10-2026. Lo que está en marcha y lo que queda por hacer alrededor de la
tanda de YAH sobre la escalera del piloto ([LEEME.txt](LEEME.txt)).

## En marcha

- **Peldaño 5 completo** (`lanzar.sh --fondo --sin-calibracion`, lanzada a
  las 15:54). Pasadas de 120, 900 y 3600 s por forma, con 36 formas.
  - Al primer segundo cayó `L t t R -> L f f f R`; quedan 11 reglas estrictas.
  - Lo más probable es «sin prueba» con el núcleo de mahler y
    collatz-T-5or7mod8 intacto. Eso no es un contraejemplo.
  - Los resultados en curso están en `resultados/`. No se suben hasta que
    termine.

## Pendientes

1. **Escalera de G debilitadas.** Ya preparada y sin lanzar.
   - Se lanza con `lanzar.sh --fondo --debilitadas`, cuando acabe el
     peldaño 5, porque `parar.sh` no distingue dos tandas a la vez.
   - Las versiones son G_A2…G_A5 (la rama A no actúa en 0 mod 2^k) y
     G_B4…G_B7 (la rama B no actúa en −1 mod 2^k).
   - `debilitar.py` las genera y comprueba la simulación en todo z < 2^12
     (0 fallos) y la lectura con el lector de YAH ([debilitadas.json](debilitadas.json)).
   - Objetivo: el k donde la cascada deja de dar QED y qué reglas resisten
     ahí.

2. **Traductor de certificados YAH → Lean.** YAH busca, no certifica.
   - Cada quitada de YAH imprime las matrices de la interpretación. Su validez
     es una cuenta finita de desigualdades matriciales, sobre los naturales o
     en max-plus/min-plus.
   - Hay que pasar esa salida a un `.lean` que la compruebe con `decide`,
     sin `sorry`, `axiom` ni `native_decide`.
   - Primera prueba: los QED de calibración de los peldaños 1 a 4, con
     matrices pequeñas y sacados en segundos.
   - Después, todo QED que den el peldaño 5 o la escalera debilitada.
   - Usa un solo proceso Lean, así que no compite con la tanda.

3. **Equivalencia SRS ↔ función para las debilitadas.**
   - Para G ya está probada en Lean (`piloto_iff`, [JudasPiloto.lean](../../JudasPiloto.lean)).
   - Para G_Ak y G_Bk sólo está comprobada por simulación.
   - Hay que extender la prueba a la familia, con las reglas por sufijo y
     las de L para los z pequeños.

4. **Pruebas a mano de los peldaños débiles.**
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
