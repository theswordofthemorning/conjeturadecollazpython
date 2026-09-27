# Revisión adversarial de los artículos y los borradores OEIS

27-09-2026. Hecha en la conversación principal, sin subagentes, antes de
escribir y después sobre los textos terminados. No sustituye la **revisión
humana** de los enunciados, que sigue pendiente, ni una revisión externa.

## 1. Lean: qué se volvió a comprobar

- Los 10 módulos finales y `lakefile.lean`, `lake-manifest.json` y
  `lean-toolchain` tienen el mismo SHA-256 (con LF) que
  [la evidencia del 26-09](../../depuracion/gao20260920/evidencia_gao_lean.json).
  Los fuentes Lean son los de `HEAD` (6a87fda).
- En los 30 módulos no hay `sorry`, `admit`, `native_decide`, `axiom`,
  `unsafe`, `extern`, `implemented_by`, `opaque` ni notaciones o macros.
  Sólo hay instancias `Decidable` por `infer_instance` y dos `set_option`
  de límites de elaboración.
- Se recompilaron hoy `GaoEnunciado`, `GaoLiteral`, `GarnerEnunciado` y
  `WuEnunciado` (Lean 4.32.2): los seis teoremas finales dependen sólo de
  `propext`, `Classical.choice` y `Quot.sound`, y todos los `#guard` pasan.
  No se relanzó `leanchecker`: los fuentes son idénticos a los del 26-09.

## 2. Enunciados contra las fuentes primarias

- **Gao (1993)**, PDF original, págs. 261–267. La coalescencia (pág. 264),
  `d(x)` y `d̄_k` (pág. 265) coinciden con `Hienas.lean`. La conjetura
  literal es «d̄_k → 1». Gao probó que `d̄_k` crece (corolario 2).
- Su glosa «almost every pair ... have the same height» exige que casi todo
  entero llegue a 1. El artículo I lo dice explícitamente: esa glosa
  equivale a la densidad 1 de los que llegan a 1, que está abierta.
- **Lagarias**, bibliografía I: entrada 68 (Gao), 72 (Garner) y 188 (Wu
  1992). Las notas del laboratorio citan «189–190» para Wu, pero Wu 1992 es
  la 188; la 189 es Wu 1993 y la 190, Wu 1995. En la bibliografía II, la
  entrada 124 es Wu–Hao 2003.
- **zbMATH** (API): Wu 1992 (Zbl 0766.11013) repite el resumen inglés, con
  «two conjectures are proposed» y sin enunciarlas. La reseña de Garner
  (Zbl 0566.10009, G. Lord) mide la altura con T y deja abierta la
  existencia de rachas largas. El teorema del artículo II cubre las dos
  alturas.
- **Elia y Tucker**: *Integers* 15 (2015), #A54. La nota
  `depuracion/oeis20260924/LEEME.md` dice «Integers 16 (2016) #A80», y es
  un error. Refutan la *caracterización* de Garner, no su conjetura (2).
- **Wu (1992)**: las dos conjeturas sólo se conocen por la lectura con la
  IA de CNKI. Queda pendiente cotejarlas con el original.

## 3. Cálculo independiente (código nuevo, sin importar el laboratorio)

| Control | Resultado | Archivo |
|---|---|---|
| Tabla 3 de Gao, `2^k d̄_k`, k = 1..24 | 21 de 21 valores | [revision_gao.py](revision_gao.py), [salida](revision_gao_salida.txt) |
| Tabla 2 de Gao, `d(10^j)`, j = 2..8 | 7 de 7 (nunca se había cotejado) | ídem y [10^8](tabla2_1e8_salida.txt) |
| Puente de Hienas, n < 2^22 | 1.567.551 encuentros, 0 fallos | ídem |
| Rachas de Garner por otra ruta, L = 1..16 | altura `t+a+m` y `σ∞ = t+m`, con tres m cada una | [revision_garner.py](revision_garner.py), [salida](revision_garner_salida.txt) |
| A078441, a(1)..a(40), y tabla 1 de Gao (8 filas, maximales) | coinciden | ídem |
| Wu: K(2^N), N ≤ 22; con la altura de T, igual | coincide con el laboratorio | [revision_wu.py](revision_wu.py), [salida](revision_wu_salida.txt) |
| Coalescencia ⟹ misma altura y `σ∞`, n < 2^20 | 0 excepciones | ídem |
| Pregunta de Gao (altura igual, `σ∞` distinta) | 0 casos para n < 2^24 | [wu_n24_salida.txt](wu_n24_salida.txt) |
| `L(2^N)` contra la b-file oficial de A078441, N ≤ 26 | 26 de 26 | este informe |

## 4. Novedad

Se buscó en arXiv (API: «same height» y Collatz; coalescencia; 3x+1 y
consecutivos), en zbMATH (API, por título) y en la web. Sólo aparecen
cómputos (Frinkle et al. 2025, LaDue 2017, Burson 2020), familias (Wu–Huang)
y la refutación de Elia–Tucker. No se halló una prueba de ninguna de las
tres conjeturas. MathSciNet y Google Scholar no se consultaron.

## 5. Errores encontrados en los borradores de los textos, y corregidos

1. Artículo I: una heurística `P(σ>t) ~ t^(-1/2)` y otra `(log n)^(-1/2)`.
   Los datos no las respaldan (la supervivencia medida baja más despacio).
   Se quitaron.
2. Artículo I: «`E√u ≤ (31/32)^n √u_0 + 32 ≤ 32`» era falso en la segunda
   desigualdad. Ahora dice `32(1−(31/32)^n)`, como Lean.
3. Artículo I: en la ventana VH faltaba condicionar a `τ > T_0`.
4. Artículo I: `UmbralRachas.orden_cota` no existe; es `UmbralRachasGao`.
   También decía 28 módulos: la cadena de Gao usa 26 y el proyecto tiene 30.
5. Artículo I: la frase que ligaba la glosa de Gao con Wu decía «es» donde
   hay una equivalencia no formalizada. Se aclaró.
6. Artículo II: decía que el residuo 4 es término de A078441, y no lo es.
7. Artículo II: la prueba del valor común usaba mal el último par del
   bloque. Ahora prueba que `r+K < 2^t`, porque el par `(2^t−1, 2^t)`
   nunca se funde.
8. Artículo III: `d(2^25)` estaba escrito a mano (0,729000); es 0,728677.
   `d(2^26)` es 0,732361, no 0,732363.
9. Artículo III: la cita del resumen de Wu mezclaba dos versiones. Ahora es
   la de zbMATH, literal.

## 6. Controles automáticos de los textos

- [revisar_tex.py](revisar_tex.py): código a ≤ 72 columnas, resúmenes
  (1623, 1466 y 1529 caracteres; arXiv admite 1920), citas resueltas y
  marcas `[TO CONFIRM]`.
- [nombres_lean.py](nombres_lean.py): todos los nombres citados con
  `\lean{}` (64, 18 y 11 distintos por artículo) existen en los fuentes con
  su espacio de nombres, o son módulos y palabras reservadas de Lean.
- [codigo_lean.py](codigo_lean.py): las 26 declaraciones mostradas son
  literales, salvo saltos de línea.
- Los tres `.tex` compilan con Tectonic 0.17.0 (XeTeX) sin avisos.
- Los borradores OEIS: [../oeis/verificar_borradores.py](../oeis/verificar_borradores.py).

## 7. Lo que esta revisión no cubre

- **Lectura humana** de los enunciados Lean y de los artículos.
- **Wu (1992) en el original**: el texto de las dos conjeturas.
- **Datos del autor**: nombre completo, afiliación y correo. Hay que
  confirmar además los modelos de IA; el commit del 20-09 no lleva marca de
  modelo.
- La sección 3 del artículo I resume pruebas cuyos detalles completos están
  sólo en Lean. El texto lo declara, pero un lector sin Lean no puede
  seguir cada constante.
- **pdfLaTeX** no se probó; sólo XeTeX. arXiv compila con pdfLaTeX. Los
  `.tex` traen la rama `\ifPDFTeX`, sin probar.
- El paquete final (Zenodo, revista overlay o arXiv con `anc/`) depende del
  formato que elija el usuario.
