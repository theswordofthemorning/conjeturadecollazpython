import Mathlib.Tactic.IntervalCases
import Mathlib.Tactic.SplitIfs
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Logic.Function.Iterate

/-! # El piloto 1/110 como parada de una función parcial

Ruta de Judas, J2, 16-10-2026. Certifica la reformulación de
`J2_MECANISMOS.md` §2. Con el atajo `T`, la palabra de paridades de `n` es
prefijo de `{1,110}^ω` para todo largo si y sólo si `n = 3 mod 4` y la función
parcial `G` nunca se detiene desde `z = (n+1)/4`. Aquí
`G(z) = 3z/2` si z es par y `(9z+1)/8` si `z = 7 mod 8`.

`Admite n L` sigue la convención de SALIDAS §1: todo 0 con índice `j < L` va
precedido de dos 1. No se supone ni se demuestra que `G` se detenga. El
fantasma `-1` aparece aquí como `z = 0`, punto fijo de `G` (`fantasma_cero`).
-/

namespace JudasPiloto

def T (x : ℕ) : ℕ := if x % 2 = 0 then x / 2 else (3 * x + 1) / 2

/-- Las `L` primeras paridades de `n` forman un prefijo de `{1,110}^ω`. -/
def Admite (n L : ℕ) : Prop :=
  ∀ j, j < L → T^[j] n % 2 = 0 → 2 ≤ j ∧ T^[j - 1] n % 2 = 1 ∧ T^[j - 2] n % 2 = 1

/-- Función parcial del piloto sobre `z = (x+1)/4`; `none` es parar. -/
def G (z : ℕ) : Option ℕ :=
  if z % 2 = 0 then some (3 * z / 2)
  else if z % 8 = 7 then some ((9 * z + 1) / 8)
  else none

/-- Iterados de `G`; `none` si se detuvo antes. -/
def orbita : ℕ → ℕ → Option ℕ
  | z, 0 => some z
  | z, i + 1 => match G z with
    | none => none
    | some w => orbita w i

/-- `G` nunca se detiene desde `z`. -/
def NoPara (z : ℕ) : Prop := ∀ i, (orbita z i).isSome

theorem noPara_iff (z : ℕ) : NoPara z ↔ ∃ w, G z = some w ∧ NoPara w := by
  constructor
  · intro h
    have h1 := h 1
    cases hG : G z with
    | none => simp [orbita, hG] at h1
    | some w =>
      refine ⟨w, rfl, fun i => ?_⟩
      have h2 := h (i + 1)
      simpa [orbita, hG] using h2
  · rintro ⟨w, hG, hw⟩ i
    cases i with
    | zero => simp [orbita]
    | succ i => simpa [orbita, hG] using hw i

/-- Prueba de fuego: `z = 0`, que corresponde a `n = -1`, nunca se detiene. -/
theorem fantasma_cero : NoPara 0 := by
  intro i
  induction i with
  | zero => simp [orbita]
  | succ i ih => simpa [orbita, G] using ih

theorem admite_mono {n L L' : ℕ} (h : Admite n L) (hL : L' ≤ L) : Admite n L' :=
  fun j hj hp => h j (by omega) hp

theorem admite_cero (n : ℕ) : Admite n 0 := fun j hj => absurd hj (Nat.not_lt_zero j)

theorem iter_uno (j x : ℕ) : T^[j + 1] x = T^[j] (T x) := Function.iterate_succ_apply T j x

theorem iter_tres (j x : ℕ) : T^[j + 3] x = T^[j] (T^[3] x) :=
  Function.iterate_add_apply T j 3 x

/-! ## Bloques y salidas -/

theorem bloque_a {x : ℕ} (hx : x % 8 = 7) :
    T x % 4 = 3 ∧ (T x + 1) / 4 = 3 * ((x + 1) / 4) / 2 := by
  simp only [T]; split_ifs <;> omega

theorem bloque_b {x : ℕ} (hx : x % 32 = 27) :
    T^[3] x % 4 = 3 ∧ (T^[3] x + 1) / 4 = (9 * ((x + 1) / 4) + 1) / 8 := by
  simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, T]
  split_ifs <;> omega

/-- Bloque A: una letra, y el resto de la palabra es la de `T x`. -/
theorem admite_a {x L : ℕ} (hx : x % 8 = 7) : Admite x (L + 1) ↔ Admite (T x) L := by
  have h0 : x % 2 = 1 := by omega
  have h1 : T x % 2 = 1 := by simp only [T]; split_ifs <;> omega
  have h2 : T (T x) % 2 = 1 := by simp only [T]; split_ifs <;> omega
  constructor
  · intro h j hj hp
    rcases j with _ | _ | k
    · simp only [Function.iterate_zero_apply] at hp; omega
    · simp only [Function.iterate_succ_apply', Function.iterate_zero_apply] at hp; omega
    · have hp' : T^[k + 3] x % 2 = 0 := by rw [iter_uno]; exact hp
      obtain ⟨-, a, b⟩ := h (k + 3) (by omega) hp'
      rw [show k + 3 - 1 = (k + 1) + 1 by omega, iter_uno] at a
      rw [show k + 3 - 2 = k + 1 by omega, iter_uno] at b
      refine ⟨by omega, ?_, ?_⟩
      · simpa [show k + 1 + 1 - 1 = k + 1 by omega] using a
      · simpa [show k + 1 + 1 - 2 = k by omega] using b
  · intro h j hj hp
    rcases j with _ | k
    · simp at hp; omega
    · rw [iter_uno] at hp
      obtain ⟨hk, a, b⟩ := h k (by omega) hp
      obtain ⟨m, rfl⟩ : ∃ m, k = m + 2 := ⟨k - 2, by omega⟩
      refine ⟨by omega, ?_, ?_⟩
      · rw [show m + 2 + 1 - 1 = (m + 1) + 1 by omega, iter_uno]
        simpa [show m + 2 - 1 = m + 1 by omega] using a
      · rw [show m + 2 + 1 - 2 = m + 1 by omega, iter_uno]
        simpa [show m + 2 - 2 = m by omega] using b

/-- Bloque B: tres letras, `110`, y el resto es la palabra de `T^3 x`. -/
theorem admite_b {x L : ℕ} (hx : x % 32 = 27) : Admite x (L + 3) ↔ Admite (T^[3] x) L := by
  have e1 : T x % 2 = 1 := by simp only [T]; split_ifs <;> omega
  have e2 : T^[2] x % 2 = 0 := by
    simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, T]
    split_ifs <;> omega
  have e3 : T^[3] x % 2 = 1 := by
    simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, T]
    split_ifs <;> omega
  have e4 : T (T^[3] x) % 2 = 1 := by
    simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, T]
    split_ifs <;> omega
  have e0 : x % 2 = 1 := by omega
  constructor
  · intro h j hj hp
    rcases j with _ | _ | k
    · simp only [Function.iterate_zero_apply] at hp; omega
    · simp only [Function.iterate_succ_apply' (n := 0), Function.iterate_zero_apply] at hp
      omega
    · have hp' : T^[k + 2 + 3] x % 2 = 0 := by rw [iter_tres]; exact hp
      obtain ⟨-, a, b⟩ := h (k + 2 + 3) (by omega) hp'
      rw [show k + 2 + 3 - 1 = (k + 1) + 3 by omega, iter_tres] at a
      rw [show k + 2 + 3 - 2 = k + 3 by omega, iter_tres] at b
      refine ⟨by omega, ?_, ?_⟩
      · simpa [show k + 2 - 1 = k + 1 by omega] using a
      · simpa [show k + 2 - 2 = k by omega] using b
  · intro h j hj hp
    by_cases hj3 : j < 3
    · interval_cases j
      · simp at hp; omega
      · simp only [Function.iterate_one] at hp; omega
      · refine ⟨le_refl 2, ?_, ?_⟩
        · simpa using e1
        · simpa using e0
    · obtain ⟨k, rfl⟩ : ∃ k, j = k + 3 := ⟨j - 3, by omega⟩
      rw [iter_tres] at hp
      obtain ⟨hk, a, b⟩ := h k (by omega) hp
      obtain ⟨m, rfl⟩ : ∃ m, k = m + 2 := ⟨k - 2, by omega⟩
      refine ⟨by omega, ?_, ?_⟩
      · rw [show m + 2 + 3 - 1 = (m + 1) + 3 by omega, iter_tres]
        simpa [show m + 2 - 1 = m + 1 by omega] using a
      · rw [show m + 2 + 3 - 2 = m + 3 by omega, iter_tres]
        simpa [show m + 2 - 2 = m by omega] using b

/-- Salida tras `110`: entradas con `z = 1` o `5 mod 8`. -/
theorem salida_tres {x : ℕ} (hx : x % 32 = 3 ∨ x % 32 = 19) : ¬ Admite x 4 := by
  intro h
  have e3 : T^[3] x % 2 = 0 := by
    simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, T]
    split_ifs <;> omega
  have e2 : T^[2] x % 2 = 0 := by
    simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, T]
    split_ifs <;> omega
  obtain ⟨-, a, -⟩ := h 3 (by norm_num) e3
  simp only [show 3 - 1 = 2 by rfl] at a
  omega

/-- Salida tras `1101`: entradas con `z = 3 mod 8`. -/
theorem salida_cuatro {x : ℕ} (hx : x % 32 = 11) : ¬ Admite x 5 := by
  intro h
  have e4 : T^[4] x % 2 = 0 := by
    simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, T]
    split_ifs <;> omega
  have e2 : T^[2] x % 2 = 0 := by
    simp only [Function.iterate_succ_apply', Function.iterate_zero_apply, T]
    split_ifs <;> omega
  obtain ⟨-, -, b⟩ := h 4 (by norm_num) e4
  simp only [show 4 - 2 = 2 by rfl] at b
  omega

theorem inicio_par {n : ℕ} (hn : n % 2 = 0) : ¬ Admite n 1 := by
  intro h
  obtain ⟨h2, -⟩ := h 0 (by norm_num) (by simpa using hn)
  omega

theorem inicio_uno {n : ℕ} (hn : n % 4 = 1) : ¬ Admite n 2 := by
  intro h
  have e1 : T^[1] n % 2 = 0 := by
    simp only [Function.iterate_one, T]; split_ifs <;> omega
  obtain ⟨h2, -⟩ := h 1 (by norm_num) e1
  omega

/-! ## La equivalencia -/

theorem admite_de_noPara : ∀ L x, x % 4 = 3 → NoPara ((x + 1) / 4) → Admite x L := by
  intro L
  induction L using Nat.strong_induction_on with
  | _ L ih =>
    intro x hx hn
    obtain ⟨w, hG, hw⟩ := (noPara_iff _).1 hn
    by_cases hz : (x + 1) / 4 % 2 = 0
    · have h8 : x % 8 = 7 := by omega
      obtain ⟨hT, hTz⟩ := bloque_a h8
      have hwe : w = (T x + 1) / 4 := by
        simp only [G, hz, if_true, Option.some.injEq] at hG
        omega
      rcases L with _ | L
      · exact admite_cero x
      · rw [admite_a h8]
        exact ih L (by omega) (T x) hT (hwe ▸ hw)
    · by_cases hz7 : (x + 1) / 4 % 8 = 7
      · have h32 : x % 32 = 27 := by omega
        obtain ⟨hT, hTz⟩ := bloque_b h32
        have hwe : w = (T^[3] x + 1) / 4 := by
          simp only [G, hz, hz7, if_false, if_true, Option.some.injEq] at hG
          omega
        by_cases hL : 3 ≤ L
        · obtain ⟨L', rfl⟩ : ∃ L', L = L' + 3 := ⟨L - 3, by omega⟩
          rw [admite_b h32]
          exact ih L' (by omega) (T^[3] x) hT (hwe ▸ hw)
        · exact admite_mono ((admite_b (L := 0) h32).2 (admite_cero _)) (by omega)
      · simp [G, hz, hz7] at hG

theorem noPara_de_admite :
    ∀ i x, x % 4 = 3 → (∀ L, Admite x L) → (orbita ((x + 1) / 4) i).isSome := by
  intro i
  induction i with
  | zero => intro x _ _; simp [orbita]
  | succ i ih =>
    intro x hx ha
    by_cases hz : (x + 1) / 4 % 2 = 0
    · have h8 : x % 8 = 7 := by omega
      obtain ⟨hT, hTz⟩ := bloque_a h8
      have hG : G ((x + 1) / 4) = some ((T x + 1) / 4) := by
        simp only [G, hz, if_true, Option.some.injEq]
        omega
      simp only [orbita, hG]
      exact ih (T x) hT (fun L => (admite_a h8).1 (ha (L + 1)))
    · by_cases hz7 : (x + 1) / 4 % 8 = 7
      · have h32 : x % 32 = 27 := by omega
        obtain ⟨hT, hTz⟩ := bloque_b h32
        have hG : G ((x + 1) / 4) = some ((T^[3] x + 1) / 4) := by
          simp only [G, hz, hz7, if_false, if_true, Option.some.injEq]
          omega
        simp only [orbita, hG]
        exact ih (T^[3] x) hT (fun L => (admite_b h32).1 (ha (L + 3)))
      · exfalso
        by_cases h3 : x % 32 = 11
        · exact salida_cuatro h3 (ha 5)
        · exact salida_tres (by omega) (ha 4)

/-- **El piloto como parada.** La palabra de paridades de `n` es prefijo de
`{1,110}^ω` para todo largo si y sólo si `n = 3 mod 4` y `G` nunca se detiene
desde `(n+1)/4`. -/
theorem piloto_iff (n : ℕ) :
    (∀ L, Admite n L) ↔ n % 4 = 3 ∧ NoPara ((n + 1) / 4) := by
  constructor
  · intro h
    have h4 : n % 4 = 3 := by
      by_contra hne
      rcases (show n % 2 = 0 ∨ n % 4 = 1 by omega) with he | h1
      · exact inicio_par he (h 1)
      · exact inicio_uno h1 (h 2)
    exact ⟨h4, fun i => noPara_de_admite i n h4 h⟩
  · rintro ⟨h4, hn⟩ L
    exact admite_de_noPara L n h4 hn

end JudasPiloto

#print axioms JudasPiloto.piloto_iff
#print axioms JudasPiloto.fantasma_cero
#print axioms JudasPiloto.admite_a
#print axioms JudasPiloto.admite_b
#print axioms JudasPiloto.salida_tres
#print axioms JudasPiloto.salida_cuatro
