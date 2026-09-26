# Momentos y controles finitos de la cadena de Gao

Este proyecto fija Lean 4.32.2 y Mathlib en
`905b95818eb32af7874a58b427f50c1711a5e96c` (etiqueta v4.32.2).
`lake-manifest.json` fija también las dependencias transitivas. La caché
de compilación y las descargas permanecen en `.lake/`, fuera de Git.

Desde este directorio:

```text
lake exe cache get Mathlib.Analysis.Real.Sqrt Mathlib.Tactic.Linarith Mathlib.Tactic.NormNum Mathlib.Tactic.FieldSimp Mathlib.NumberTheory.Multiplicity
lake build GaoCore GaoFormal
lake env lean Momentos.lean
```

`GaoCore` importa la transición completa de
[`cadena_completa.lean`](../cadena_completa.lean); no la reemplaza por
una cadena auxiliar. `GaoFormal` contiene:

- [Momentos.lean](Momentos.lean): magnitud de la cadena completa y C1.
- [Maximos.lean](Maximos.lean): unión finita y cruce dominado por un potencial.
- [Resto.lean](Resto.lean): identidad afín, W prolongado y V1–V2.
- [Producto.lean](Producto.lean): producto normalizado y máximo desde T.
- [Supervivencia.lean](Supervivencia.lean): supervivencia inferior `1/(t+1)`.
- [Banda.lean](Banda.lean): energía, contador y cola de mixtos en la excursión original.
- [RachasEnteras.lean](RachasEnteras.lean): conteo de rachas para offsets enteros.
- [UmbralRachas.lean](UmbralRachas.lean): valoración diádica y umbral logarítmico.
- [Reloj.lean](Reloj.lean): bloques deterministas, reloj M6 y cola física H3.
- [Palabras.lean](Palabras.lean): espacio común y promedios de prefijos.
- [SalidaPalabras.lean](SalidaPalabras.lean): primera salida y offset acotado.
- [Ventana.lean](Ventana.lean): combinación conjunta de eventos.
- [ParametrosVentana.lean](ParametrosVentana.lean): VH explícita y uniforme.
- [Hormigas.lean](Hormigas.lean): palabra universal de absorción y cota cuadrática.
- [Ensayo.lean](Ensayo.lean): relevo y absorción uniforme antes de H+D.
- [Repeticion.lean](Repeticion.lean), [Guardias.lean](Guardias.lean) y
  [ConteoEnsayos.lean](ConteoEnsayos.lean): protocolo guardado y conteo.
- [Lagartijas.lean](Lagartijas.lean): pocas entradas admisibles antes de h
  y CF_F completa (`lagartijas`, `cf_f`). [Nota](../Lagartijas.md).
- [Martas.lean](Martas.lean): el lado derecho de CF_F tiende a cero;
  `P(sigma>h)->0` (`martas`). [Nota](../Martas.md).
- [Tejonas.lean](Tejonas.lean): pares reales, transporte a clases y
  densidad uno del conjunto de Gao (`transporte`, `gao`). [Nota](../Tejonas.md).
- [GaoEnunciado.lean](GaoEnunciado.lean): el enunciado para revisión, como
  límite de densidades (`conjetura_gao`).
- [Hienas.lean](Hienas.lean): sólo importa Mathlib. Define la coalescencia
  de Gao y `d̄_k`, y prueba que un encuentro en `<= log2 n` pasos ya es
  coalescencia (`puente`). [Nota](../Hienas.md).
- [GaoLiteral.lean](GaoLiteral.lean): la conjetura tal como la escribe Gao,
  `d̄_k -> 1` y `d(x) -> 1` (`conjetura_gao_literal`), y un `#guard` que
  recalcula su tabla 3 hasta k=12.

La magnitud es `tamano=|c|/3^k` y vale cero en el cementerio. El bit
selecciona la paridad del ancla. `promedio` asigna probabilidad 1/2 a
cada rama; `hojas` conserva las multiplicidades de las palabras, aunque
varias alcancen el mismo estado. Los instantes son números de pasos
físicos del mapa atajo, empezando en cero.

Momentos desarrolla estos puentes:

- Dominación entera universal → dominación sobre reales.
- Deriva de `sqrt(tamano)` con factor `31/32` y sumando 1.
- Promedio a tiempo n, igual a una suma de `2^n` hojas dividida por `2^n`.
- Cota de momento desde `(0,1)` y Markov a tiempo determinista.
- Marca persistente de haber superado U, unión finita y máximo hasta h.

Las cotas de las dos raíces se comprueban mediante los racionales
`91/128` y `157/128`; su semisuma es `31/32`. No se usan aproximaciones
decimales como hipótesis.

Resto añade una marca persistente de primera salida del interior.
La base continúa la cadena original, mientras W se prolonga
multiplicativamente tras salir. Producto prueba para todo T,H la cota
`P(existe t en [T,T+H]: Pi_t>(31/32)^t)<=(61/62)^T`.
[Enunciados, hipótesis y evidencia](../Control_aditivo_producto.md).

La [variante armónica](../Ventana_armonica.md) usa Supervivencia y Banda
para evitar la fórmula binomial. Cambia el parámetro de la ventana a
Q=T+1. El [reloj por bloques](../Reloj_bloques.md) enlaza las rachas
con el tiempo físico. La [ventana conjunta](../Ventana_conjunta.md)
certifica VH para todo offset entero; también fija parámetros usando
una cota del offset conocida al inicio.
El [ensayo finito](../Ensayo_finito.md) conecta VH con Hormigas sobre
la cadena original y obtiene un piso uniforme de fusión antes de H+D.

El alcance es finito y universal en n, h y los estados indicados.
El protocolo global de ensayos, CF_F, su límite, el transporte a clases de
enteros y la densidad uno de Gao quedan formalizados (ConteoEnsayos,
Lagartijas, Martas, Tejonas). Lean certifica los enunciados; su lectura
humana y el cotejo del artículo primario de Gao siguen pendientes.
Tampoco se obtiene una cota a tiempo de salida condicionado sustituyendo
n por una variable aleatoria. El estado de validación se registra en
la [revisión principal](../REVISION.md).
