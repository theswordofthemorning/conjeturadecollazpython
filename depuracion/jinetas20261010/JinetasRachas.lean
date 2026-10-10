import Mathlib.Data.Int.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! # Jinetas: el coste de reiniciar después de una racha

Las identidades de bloques se reciben como hipótesis explícitas.
RACHAS.md deriva esas identidades de la órbita y precisa el alcance.
-/

namespace JinetasRachas

theorem puente (n x y : ℤ) : y < n ↔ x - n < x - y := by omega

theorem puente_entero (n x y : ℤ) :
    y < n ↔ x - n + 1 ≤ x - y := by omega

theorem margen_cola {M A B n x y : ℤ} (hM : 0 < M)
    (h : M * y = A * x + B) :
    y < n ↔ M * (x - n) < (M - A) * x - B := by
  constructor <;> intro hn <;> nlinarith

theorem exceso_bloque {P Q R n x y : ℤ}
    (h : P * Q * y = R * (x + 1) - P) :
    P * Q * (y - n) = R * (x - n) - (P * Q - R) * n + R - P := by
  nlinarith only [h]

theorem defecto_suelo {P Q R N x y : ℤ}
    (h : P * (Q * y + 1) = R * (x + 1)) :
    (Q * N + 1) * P * (y + 1) - (N + 1) * R * (x + 1) =
      P * (Q - 1) * (N - y) := by
  calc
    _ = (Q * N + 1) * P * (y + 1) - (N + 1) * (R * (x + 1)) := by ring
    _ = (Q * N + 1) * P * (y + 1) - (N + 1) * (P * (Q * y + 1)) := by rw [h]
    _ = _ := by ring

theorem suelo_iff {P Q R N x y : ℤ} (hP : 0 < P) (hQ : 1 < Q)
    (h : P * (Q * y + 1) = R * (x + 1)) :
    (Q * N + 1) * P * (y + 1) ≤ (N + 1) * R * (x + 1) ↔ N ≤ y := by
  have he := defecto_suelo (N := N) h
  have hp : 0 < P * (Q - 1) := mul_pos hP (by omega)
  constructor <;> intro hn <;> nlinarith only [he, hp, hn]

theorem bloque_corto {x y : ℤ} (hx : 1 < x) (h : 4 * y ≤ 3 * x + 1) :
    y < x := by omega

theorem bloque_expansivo {x y : ℤ} (hx : 0 ≤ x) (h : 8 * y = 9 * x + 5) :
    x < y := by omega

def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

theorem paso_110 (u : ℕ) :
    T (8 * u + 3) = 12 * u + 5 ∧
    T (12 * u + 5) = 18 * u + 8 ∧
    T (18 * u + 8) = 9 * u + 4 := by
  have h1 : (8 * u + 3) % 2 ≠ 0 := by omega
  have h2 : (12 * u + 5) % 2 ≠ 0 := by omega
  have h3 : (18 * u + 8) % 2 = 0 := by omega
  simp only [T, h1, h2, h3, if_false, if_true]
  omega

theorem ejemplo_corte :
    T 7 = 11 ∧ T 11 = 17 ∧ T 17 = 26 ∧ T 26 = 13 ∧
    T 13 = 20 ∧ T 20 = 10 ∧ T 10 = 5 ∧
    10 < 13 ∧ ¬10 < 7 ∧ 5 < 7 ∧
    3 ^ 1 < 2 ^ 2 ∧ ¬3 ^ 4 < 2 ^ 6 ∧ 3 ^ 4 < 2 ^ 7 := by decide

end JinetasRachas

#print axioms JinetasRachas.puente
#print axioms JinetasRachas.puente_entero
#print axioms JinetasRachas.margen_cola
#print axioms JinetasRachas.exceso_bloque
#print axioms JinetasRachas.defecto_suelo
#print axioms JinetasRachas.suelo_iff
#print axioms JinetasRachas.bloque_corto
#print axioms JinetasRachas.bloque_expansivo
#print axioms JinetasRachas.paso_110
#print axioms JinetasRachas.ejemplo_corte
