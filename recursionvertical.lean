/- recursionvertical.lean
   EL MOTOR DE LA RECURSION VERTICAL (PANTERAS), demostrado en Lean 4.
   (04-08-2026; el noveno .lean del repo. Nucleo puro, sin Mathlib.)

   La contraccion de Gatas sube en diagonal por el triangulo de estratos:
   aqui se demuestra el DESPLAZAMIENTO exacto que lo produce -

     Titer (k+2) (4t+1) = Titer k (3t+1)      (la trayectoria se corre 2)
     S (k+2) (4t+1) = 1 + S k (3t+1)          (cada lado gana UN impar)
     (idem para el lado 4t+2 / 3t+2)

   y el COROLARIO: el par (4t+1, 4t+2) funde BALANCEADO en el paso k+2
   si y solo si el par contraido (3t+1, 3t+2) funde balanceado en el
   paso k. Con la biyectividad de t -> 3t+1 modulo 2^m (declarada; es
   el paso de conteo pendiente), esto da e_s(N)|_{r=1 mod 4} =
   e_{s-2}(N-2): la diagonal medida exacta en auditoria_rigor.py R35.
   El corrimiento de estrato (+2 mixtos) esta en mixto0/mixto1. -/

def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

def Titer : Nat → Nat → Nat
  | 0, l => l
  | n + 1, l => Titer n (T l)

def S : Nat → Nat → Nat
  | 0, _ => 0
  | n + 1, l => l % 2 + S n (T l)

-- ── los cuatro pasos de la contraccion (como en contracciondegatas) ──
theorem paso1_impar (t : Nat) : T (4 * t + 1) = 6 * t + 2 := by
  unfold T
  have h : (4 * t + 1) % 2 = 1 := by omega
  simp [h]
  omega

theorem paso1_par (t : Nat) : T (4 * t + 2) = 2 * t + 1 := by
  unfold T
  have h : (4 * t + 2) % 2 = 0 := by omega
  simp [h]
  omega

theorem paso2_par (t : Nat) : T (6 * t + 2) = 3 * t + 1 := by
  unfold T
  have h : (6 * t + 2) % 2 = 0 := by omega
  simp [h]
  omega

theorem paso2_impar (t : Nat) : T (2 * t + 1) = 3 * t + 2 := by
  unfold T
  have h : (2 * t + 1) % 2 = 1 := by omega
  simp [h]
  omega

-- ── LOS DOS PASOS DE LA CONTRACCION SON MIXTOS (el estrato sube en 2) ──
theorem mixto0 (t : Nat) : (4 * t + 1) % 2 ≠ (4 * t + 2) % 2 := by omega

theorem mixto1 (t : Nat) : (6 * t + 2) % 2 ≠ (2 * t + 1) % 2 := by omega

-- ── EL DESPLAZAMIENTO DE TRAYECTORIA: dos pasos se absorben exactos ──
theorem titer_shift1 (k t : Nat) :
    Titer (k + 2) (4 * t + 1) = Titer k (3 * t + 1) := by
  show Titer k (T (T (4 * t + 1))) = Titer k (3 * t + 1)
  rw [paso1_impar, paso2_par]

theorem titer_shift2 (k t : Nat) :
    Titer (k + 2) (4 * t + 2) = Titer k (3 * t + 2) := by
  show Titer k (T (T (4 * t + 2))) = Titer k (3 * t + 2)
  rw [paso1_par, paso2_impar]

-- ── EL DESPLAZAMIENTO DE S: cada lado gana exactamente UN impar ──
theorem s_shift1 (k t : Nat) :
    S (k + 2) (4 * t + 1) = 1 + S k (3 * t + 1) := by
  show (4 * t + 1) % 2 + ((T (4 * t + 1)) % 2 + S k (T (T (4 * t + 1))))
       = 1 + S k (3 * t + 1)
  rw [paso1_impar, paso2_par]
  omega

theorem s_shift2 (k t : Nat) :
    S (k + 2) (4 * t + 2) = 1 + S k (3 * t + 2) := by
  show (4 * t + 2) % 2 + ((T (4 * t + 2)) % 2 + S k (T (T (4 * t + 2))))
       = 1 + S k (3 * t + 2)
  rw [paso1_par, paso2_impar]
  omega

-- ── EL COROLARIO: LA FUSION BALANCEADA SE DESPLAZA, ida y vuelta ──
theorem fusion_desplaza (k t : Nat) :
    (Titer (k + 2) (4 * t + 1) = Titer (k + 2) (4 * t + 2) ∧
     S (k + 2) (4 * t + 1) = S (k + 2) (4 * t + 2))
    ↔ (Titer k (3 * t + 1) = Titer k (3 * t + 2) ∧
       S k (3 * t + 1) = S k (3 * t + 2)) := by
  rw [titer_shift1, titer_shift2, s_shift1, s_shift2]
  constructor
  · intro h
    exact ⟨h.1, by omega⟩
  · intro h
    exact ⟨h.1, by omega⟩

-- ── caso concreto por el nucleo: t = 1, el (5,6) contra el (4,5) ──
theorem caso_t1 : Titer 5 5 = Titer 5 6 ∧ Titer 3 4 = Titer 3 5 := by decide

#print axioms titer_shift1
#print axioms s_shift1
#print axioms fusion_desplaza
