/- lemasdeperras.lean
   LOS DOS LEMAS CARGADOS DE PERRAS, demostrados en Lean 4.
   (04-08-2026; el septimo .lean del repo. Nucleo puro, sin Mathlib.)

   1. EL LEMA DEL VORTICE (el atomo del programa de fusion entero):
      para un estado mixto {s, s+g} (g impar, s >= 1), la fusion en el
      paso siguiente ocurre SI Y SOLO SI g = 2s+1 (o sea D = 0) y s es
      impar. De el cuelgan Perras, los aterrizajes y las unicidades.

   2. EL ARRANQUE D1 = 1: el par (2s, 2s+1) pasa a {s, 3s+2}, cuyo gap
      es 2s+2 y cuyo D = gap - 2*menor - 1 = 1. Es el paso 1 de la
      demostracion de Perras. -/

def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

-- ── 1. EL LEMA DEL VORTICE ──
theorem vortice (s g : Nat) (hg : g % 2 = 1) (hs : 1 ≤ s) :
    T s = T (s + g) ↔ (g = 2 * s + 1 ∧ s % 2 = 1) := by
  unfold T
  by_cases h : s % 2 = 0
  · -- s par, s+g impar: s/2 = (3(s+g)+1)/2 es imposible en positivos
    have h2 : ¬ (s + g) % 2 = 0 := by omega
    simp [h, h2]
    omega
  · -- s impar, s+g par: (3s+1)/2 = (s+g)/2  <=>  g = 2s+1
    have h1 : s % 2 = 1 := by omega
    have h2 : (s + g) % 2 = 0 := by omega
    simp [h, h2]
    omega

-- ── 2. EL ARRANQUE: (2s, 2s+1) -> {s, 3s+2} con D = 1 ──
theorem arranque (s : Nat) (h : 1 ≤ s) :
    T (2 * s) = s ∧ T (2 * s + 1) = 3 * s + 2 ∧
    (3 * s + 2) - s = 2 * s + 2 ∧ (2 * s + 2) - 2 * s - 1 = 1 := by
  unfold T
  refine ⟨?_, ?_, by omega, by omega⟩
  · simp [Nat.mul_mod_right]
  · have h2 : (2 * s + 1) % 2 = 1 := by omega
    simp [h2]
    omega

-- ── El corolario que usa Perras: desde D = 1, el compartido-impar deja
--    D = 1 y el compartido-par lo baja a 0 (enunciado sobre el gap) ──
theorem tramo_D1_impar (s : Nat) (h1 : s % 2 = 1) :
    T (s + (2 * s + 2)) - T s = 2 * (T s) + 2 := by
  unfold T
  have h2 : (s + (2 * s + 2)) % 2 = 1 := by omega
  have h3 : ¬ s % 2 = 0 := by omega
  simp [h2, h3]
  omega

theorem tramo_D1_par (s : Nat) (h0 : s % 2 = 0) (h : 2 ≤ s) :
    T (s + (2 * s + 2)) - T s = 2 * (T s) + 1 := by
  unfold T
  have h2 : (s + (2 * s + 2)) % 2 = 0 := by omega
  simp [h0, h2]
  omega

-- ── Casos por el nucleo (decide, no #eval): el vortice del (4,5) en el
--    paso 3 (la familia de Garner) y el arranque del par (6,7) ──
theorem caso_garner : T 1 = T 4 := by decide
theorem caso_no_vortice : T 3 ≠ T 8 := by decide

#print axioms vortice
#print axioms arranque
#print axioms tramo_D1_impar
#print axioms tramo_D1_par
