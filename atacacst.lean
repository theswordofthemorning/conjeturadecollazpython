/-
  atacacst.lean — LA PALANCA DEL ATAQUE A CST, demostrada.

  CST (Terras 1976): sigma(n) = sigma*(n) para todo n >= 2, donde sigma es la
  primera bajada REAL (T^k n < n) y sigma* la primera bajada del COEFICIENTE
  (2^k > 3^{S_k}).  Siempre sigma* <= sigma.

  LO QUE ESTE FICHERO DEMUESTRA, para todo k, todo r y todo m:

    1. terras_1_2   T^k(2^k*m + r) = 3^{S_k(r)}*m + T^k(r)      (la identidad)
    2. palanca      si 3^S < 2^k  y  T^k(r) < r + (2^k - 3^S)*m,
                    entonces  T^k(2^k*m + r) < 2^k*m + r         (bajada real)
    3. tramo_finito si 3^S < 2^k  y  m > T^k(r),  bajada real garantizada.

  CONSECUENCIA: en cada clase r mod 2^k donde el coeficiente cae, el fallo de
  CST solo puede vivir en el tramo finito m <= T^k(r); todo lo demas de la
  clase -infinitos numeros- baja de verdad. atacacst.py revisa esos tramos.

  La identidad y sus definiciones vienen de depuracion/lean/A20.lean (trio del
  02-08-2026); los teoremas 2 y 3 son nuevos. Sin Mathlib, solo nucleo.
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

/- ── Los dos lemas de paridad y la identidad, como en A20.lean ── -/

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
    · rw [T_par (2 ^ k * m) r h, ih m (T r)]
      have hs : S (k + 1) r = S k (T r) := by
        show r % 2 + S k (T r) = S k (T r)
        omega
      rw [hs]
    · have h1 : r % 2 = 1 := by omega
      rw [T_impar (2 ^ k * m) r h1]
      have h3 : 3 * (2 ^ k * m) + T r = 2 ^ k * (3 * m) + T r := by
        rw [Nat.mul_comm 3 (2 ^ k * m), Nat.mul_assoc, Nat.mul_comm m 3]
      rw [h3, ih (3 * m) (T r)]
      have hs : S (k + 1) r = S k (T r) + 1 := by
        show r % 2 + S k (T r) = S k (T r) + 1
        omega
      rw [hs, Nat.pow_succ, Nat.mul_assoc]

/- ── TEOREMA NUEVO 1: LA PALANCA.
     Si el coeficiente cae (3^S < 2^k) y m esta fuera del tramo exacto,
     la bajada del coeficiente ES bajada real. ── -/

theorem palanca (k m r : Nat)
    (hcoef : 3 ^ S k r < 2 ^ k)
    (htramo : Titer k r < r + (2 ^ k - 3 ^ S k r) * m) :
    Titer k (2 ^ k * m + r) < 2 ^ k * m + r := by
  rw [terras_1_2]
  have h1 : 3 ^ S k r + (2 ^ k - 3 ^ S k r) = 2 ^ k := by omega
  have hexp : 3 ^ S k r * m + (2 ^ k - 3 ^ S k r) * m = 2 ^ k * m := by
    rw [← Nat.add_mul, h1]
  omega

/- ── TEOREMA NUEVO 2: EL TRAMO ES FINITO, con cota gruesa y limpia.
     Basta m > T^k(r): fuera de ahi, TODA la clase baja de verdad. ── -/

theorem tramo_finito (k m r : Nat)
    (hcoef : 3 ^ S k r < 2 ^ k)
    (hm : Titer k r < m) :
    Titer k (2 ^ k * m + r) < 2 ^ k * m + r := by
  apply palanca k m r hcoef
  have hd : 1 ≤ 2 ^ k - 3 ^ S k r := by omega
  have hmm : 1 * m ≤ (2 ^ k - 3 ^ S k r) * m := Nat.mul_le_mul_right m hd
  omega

/- ── CASOS CONOCIDOS, por el nucleo con decide (no #eval) ── -/

-- El objeto es el atajo: T 7 = 11 (el clasico daria 22).
theorem caso_T7 : T 7 = 11 := by decide

-- La clase 1 mod 4 cae en k = 2 (S = 1, 3 < 4) y su tramo es m <= T^2(1) = 1:
theorem caso_coef_cae : 3 ^ S 2 1 < 2 ^ 2 := by decide
theorem caso_tramo : Titer 2 1 = 1 := by decide
-- ...y en cuanto m = 2 > 1, la bajada real se cumple (n = 9: 9→14→7 < 9):
theorem caso_baja : Titer 2 (2 ^ 2 * 2 + 1) < 2 ^ 2 * 2 + 1 := by decide
-- ...y de hecho la palanca la da para TODO m >= 2 de la clase, no caso a caso:
theorem clase_1_mod_4_baja (m : Nat) (hm : 2 ≤ m) :
    Titer 2 (2 ^ 2 * m + 1) < 2 ^ 2 * m + 1 := by
  apply tramo_finito 2 m 1 (by decide)
  have h : Titer 2 1 = 1 := by decide
  omega

-- Y el caso con numeros de verdad del repo: el 27 (clase 27 mod 2^5, S=4).
-- 3^4 = 81 > 32 = 2^5: el coeficiente NO ha caido en k=5 y la palanca no
-- aplica -- correcto, porque el 27 sube. El nucleo confirma que sube:
theorem caso_27_sube : 2 ^ 5 < 3 ^ S 5 27 := by decide

/- ── El control final ── -/
#print axioms terras_1_2
#print axioms palanca
#print axioms tramo_finito
#print axioms clase_1_mod_4_baja
