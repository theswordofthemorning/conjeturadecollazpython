import Lake
open Lake DSL

package gao where

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @
  "905b95818eb32af7874a58b427f50c1711a5e96c"

lean_lib GaoCore where
  srcDir := ".."
  roots := #[`cadena_completa]

lean_lib MangostasCore where
  srcDir := "../../frente20260910"
  roots := #[`rachas]

lean_lib GaoFormal where
  roots := #[`Momentos, `Maximos, `Resto, `Producto, `Supervivencia, `Banda,
    `RachasEnteras, `UmbralRachas, `Reloj, `Palabras, `SalidaPalabras, `Ventana,
    `ParametrosVentana, `Hormigas, `Ensayo, `Repeticion, `Guardias, `ConteoEnsayos]
