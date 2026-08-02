/-
  A20 — Terras 1976, Teorema 1.2, sobre el mapa del ATAJO:
      T(n) = n/2 si n par,  (3n+1)/2 si n impar.

  ENUNCIADO:  T^k(2^k*m + r) = 3^(S_k(r)) * m + T^k(r)
  con S_k(r) = numero de impares entre los k primeros iterados r, T r, ..., T^{k-1} r.

  Las definiciones estan escritas AQUI, desde cero, sin mirar ningun fichero
  del repo. Los casos concretos de abajo (decide) protegen contra la trampa
  de demostrar un teorema sobre otro objeto.
-/

set_option maxRecDepth 40000

/-- El mapa del ATAJO. (El clasico seria 3n+1 sin dividir; NO es este.) -/
def T (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- T^k. Convenio: Titer (k+1) n = Titer k (T n). -/
def Titer : Nat → Nat → Nat
  | 0, n => n
  | k + 1, n => Titer k (T n)

/-- S k n = cuantos impares hay entre n, T n, ..., T^{k-1} n. -/
def S : Nat → Nat → Nat
  | 0, _ => 0
  | k + 1, n => n % 2 + S k (T n)

/- ── Dos lemas aritmeticos: como pasa T por 2*q + r segun la paridad de r ── -/

theorem T_par (q r : Nat) (h : r % 2 = 0) : T (2 * q + r) = q + T r := by
  unfold T
  have h2 : (2 * q + r) % 2 = 0 := by omega
  rw [if_pos h2, if_pos h]
  omega

theorem T_impar (q r : Nat) (h : r % 2 = 1) : T (2 * q + r) = 3 * q + T r := by
  unfold T
  have h2 : ¬ ((2 * q + r) % 2 = 0) := by omega
  have h0 : ¬ (r % 2 = 0) := by omega
  rw [if_neg h2, if_neg h0]
  omega

/- ── EL TEOREMA (A20): valido para TODO k, TODO m (incluido 0) y TODO r
     (ni siquiera hace falta r < 2^k: la identidad vale para r arbitrario). ── -/

theorem terras_1_2 : ∀ (k m r : Nat),
    Titer k (2 ^ k * m + r) = 3 ^ (S k r) * m + Titer k r := by
  intro k
  induction k with
  | zero =>
    intro m r
    show 2 ^ 0 * m + r = 3 ^ (S 0 r) * m + r
    simp [S]
  | succ k ih =>
    intro m r
    have hpm : 2 ^ (k + 1) * m + r = 2 * (2 ^ k * m) + r := by
      rw [Nat.pow_succ, Nat.mul_comm (2 ^ k) 2, Nat.mul_assoc]
    show Titer k (T (2 ^ (k + 1) * m + r)) = 3 ^ (S (k + 1) r) * m + Titer k (T r)
    rw [hpm]
    by_cases h : r % 2 = 0
    · -- paso PAR: el impar no se gasta, la pendiente no cambia
      rw [T_par (2 ^ k * m) r h, ih m (T r)]
      have hs : S (k + 1) r = S k (T r) := by
        show r % 2 + S k (T r) = S k (T r)
        omega
      rw [hs]
    · -- paso IMPAR: m pasa a 3m, la pendiente gana un factor 3
      have h1 : r % 2 = 1 := by omega
      rw [T_impar (2 ^ k * m) r h1]
      have h3 : 3 * (2 ^ k * m) + T r = 2 ^ k * (3 * m) + T r := by
        rw [Nat.mul_comm 3 (2 ^ k * m), Nat.mul_assoc, Nat.mul_comm m 3]
      rw [h3, ih (3 * m) (T r)]
      have hs : S (k + 1) r = S k (T r) + 1 := by
        show r % 2 + S k (T r) = S k (T r) + 1
        omega
      rw [hs, Nat.pow_succ, Nat.mul_assoc]

/- ── CASOS CONOCIDOS, comprobados por el NUCLEO con decide (no #eval) ── -/

-- La definicion es el atajo y no el clasico: T 7 = 11 (el clasico daria 22).
theorem caso_T7 : T 7 = 11 := by decide

-- Trayectoria corta completa del 7 con el atajo:
-- 7→11→17→26→13→20→10→5→8→4→2→1: llega al 1 en 11 pasos, con 5 impares.
theorem caso_trayectoria_7 : Titer 11 7 = 1 := by decide
theorem caso_impares_7 : S 11 7 = 5 := by decide

-- Instancia concreta del teorema, con numeros de verdad (k=6, r=27, m=5):
theorem caso_identidad : Titer 6 (2 ^ 6 * 5 + 27) = 3 ^ (S 6 27) * 5 + Titer 6 27 := by
  decide

-- Bordes: m = 0, k = 0, r = 0, r par, r = 2^k - 1 (todo impares).
theorem borde_m0 : Titer 8 (2 ^ 8 * 0 + 27) = 3 ^ (S 8 27) * 0 + Titer 8 27 := by decide
theorem borde_k0 : Titer 0 (2 ^ 0 * 9 + 3) = 3 ^ (S 0 3) * 9 + Titer 0 3 := by decide
theorem borde_r0 : Titer 5 (2 ^ 5 * 6 + 0) = 3 ^ (S 5 0) * 6 + Titer 5 0 := by decide
theorem borde_r_par : Titer 4 (2 ^ 4 * 3 + 12) = 3 ^ (S 4 12) * 3 + Titer 4 12 := by decide
theorem borde_r_tope : Titer 5 (2 ^ 5 * 2 + 31) = 3 ^ (S 5 31) * 2 + Titer 5 31 := by decide
-- Y en el borde r = 2^k - 1 la pendiente es 3^k (k impares seguidos):
theorem borde_todo_impar : S 5 31 = 5 := by decide

/- ── El control final ── -/
#print axioms terras_1_2
#print axioms caso_trayectoria_7
#print axioms caso_identidad
#print axioms borde_m0
