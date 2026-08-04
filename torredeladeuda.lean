/- torredeladeuda.lean
   EL PASEO DE LA DEUDA (alias RATAS): el esqueleto en Lean 4.
   (04-08-2026; el decimo .lean del repo. Nucleo puro, sin Mathlib.)

   Las leyes de compensacion de la torre, pisos k = 2 y 3 (parametrizadas
   v = 2j+1, lineales, el nucleo las verifica; el k general exige la
   induccion de 3^k impar mas reescrituras de producto - declarado).

   LA LEY: en la forma mixta {v, 3^k v + 1} con v IMPAR, el paso
   compensa (el chico gana el impar: deuda -1) y DESCIENDE a la torre
   negativa {s', 3^(k-1) s' - (3^(k-1)-1)/2} con s' = (3v+1)/2. -/

def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

-- ── 3^k es impar (la base de todas las paridades de la torre) ──
theorem pow3_impar : ∀ k, 3 ^ k % 2 = 1 := by
  intro k
  induction k with
  | zero => rfl
  | succ n ih => rw [Nat.pow_succ]; omega

-- ── PISO k = 2: {v, 9v+1}, v = 2j+1 impar ──
theorem gap_impar_k2 (j : Nat) :
    (9 * (2 * j + 1) + 1) % 2 ≠ (2 * j + 1) % 2 := by omega

theorem compensa_k2 (j : Nat) :
    T (2 * j + 1) = 3 * j + 2 ∧
    T (9 * (2 * j + 1) + 1) = 3 * (3 * j + 2) - 1 := by
  unfold T
  constructor
  · have h : (2 * j + 1) % 2 = 1 := by omega
    simp [h]; omega
  · have h : (9 * (2 * j + 1) + 1) % 2 = 0 := by omega
    simp [h]; omega

-- ── PISO k = 3: {v, 27v+1}, v = 2j+1: desciende a {s', 9s' - 4} ──
theorem compensa_k3 (j : Nat) :
    T (27 * (2 * j + 1) + 1) = 9 * (3 * j + 2) - 4 := by
  unfold T
  have h : (27 * (2 * j + 1) + 1) % 2 = 0 := by omega
  simp [h]; omega

-- ── EL SALDO: el paso da el impar al lado CHICO (deuda -1) ──
theorem chico_impar (j : Nat) : (2 * j + 1) % 2 = 1 := by omega
theorem grande_par_k2 (j : Nat) : (9 * (2 * j + 1) + 1) % 2 = 0 := by omega

#print axioms pow3_impar
#print axioms compensa_k2
#print axioms compensa_k3
