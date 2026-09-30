import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Data.Nat.Log

/-! # Ocelotas: la conjetura CST de Terras para palabras de dos rachas impares

Atajo de Collatz `T(n) = n/2` (par), `(3n+1)/2` (impar). `S k n` cuenta los pasos impares
entre `n, T n, …, T^(k-1) n`. El primer cruce del coeficiente es `τ(n) = k` cuando
`3^S_j ≥ 2^j` para `1 ≤ j < k` y `3^S_k < 2^k` (`PrimerCruce n k`). La conjetura CST de
Terras (1976) dice que en ese paso ya hay descenso real: `T^k(n) < n` para todo `n ≥ 2`.

`ocelotas`: si la palabra de paridad de `n` hasta su primer cruce es `1^a 0^b 1^c 0^d`
(dos rachas de pasos impares, es decir, dos máximos locales), entonces `T^k(n) < n`.

La única hipótesis externa es `RhinEntera`, forma entera de la cota de Rhin (1987) para
formas lineales en `log 2` y `log 3`: con `2^(k-1) ≤ 3^q < 2^k`,
`Λ = k log 2 − q log 3 ≥ k^(−13.3)` da `2^k − 3^q = 3^q (e^Λ − 1) ≥ 3^q k^(−14)`.

Estructura de la prueba (ver `LEEME.md`):
* tramos: `2^a (T^a n + 1) = 3^a (n+1)` en una racha impar, `2^b T^b y = y` en una par;
* identidad: `2^k T^k(n) + 2^(a+b+c) + 3^c 2^a = 3^q n + 3^q + 3^c 2^(a+b)`, `q = a+c`;
* congruencias: `2^a ∣ n+1` y `2^c ∣ T^(a+b)(n) + 1`;
* `nucleo`: el fallo obliga a `2^q D³ < 18·27^q`, con `D = 2^k − 3^q`;
* con Rhin: `n < 2k^14`, `3^q < 36 k^84`, luego `k ≤ 1023` y `q ≤ 645`;
* `finito_q` (cálculo en el núcleo): para `q ≤ 645` sólo quedan `k ≤ 27` y `n ≤ 50`;
* `finito_n` (cálculo en el núcleo): CST para `2 ≤ n ≤ 50` con primer cruce `k ≤ 27`.

Compilación, desde `depuracion/gao20260920/formal`:
`lake env lean ../../cst20260930/Ocelotas.lean` -/

set_option maxRecDepth 100000

namespace Ocelotas

/-- Atajo de Collatz. -/
def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- `S k n`: pasos impares entre `n, T n, …, T^(k-1) n`. -/
def S : ℕ → ℕ → ℕ
  | 0, _ => 0
  | k + 1, n => n % 2 + S k (T n)

/-- `k` es el primer cruce del coeficiente de `n` (el tiempo de parada del coeficiente
    `τ(n)` de Terras): `3^S_j ≥ 2^j` para `1 ≤ j < k` y `3^S_k < 2^k`. -/
def PrimerCruce (n k : ℕ) : Prop :=
  (∀ j, j < k → 1 ≤ j → 2 ^ j ≤ 3 ^ S j n) ∧ 3 ^ S k n < 2 ^ k

instance (n k : ℕ) : Decidable (PrimerCruce n k) := by unfold PrimerCruce; infer_instance

/-- La palabra de paridad de `n` de longitud `a+b+c+d` es `1^a 0^b 1^c 0^d`. -/
def DosRachas (n a b c d : ℕ) : Prop :=
  (∀ t, t < a → T^[t] n % 2 = 1) ∧ (∀ t, t < b → T^[a + t] n % 2 = 0) ∧
    (∀ t, t < c → T^[a + b + t] n % 2 = 1) ∧ (∀ t, t < d → T^[a + b + c + t] n % 2 = 0)

/-- Forma entera de la cota de Rhin (1987): si `2^(k-1) ≤ 3^q < 2^k`, entonces
    `3^q ≤ (2^k − 3^q) k^14`. Hipótesis externa del teorema. -/
def RhinEntera : Prop :=
  ∀ k q : ℕ, 2 ^ k ≤ 2 * 3 ^ q → 3 ^ q < 2 ^ k → 3 ^ q ≤ (2 ^ k - 3 ^ q) * k ^ 14

/-! ## El atajo por tramos -/

theorem T_impar {n : ℕ} (h : n % 2 = 1) : 2 * T n = 3 * n + 1 := by
  unfold T; rw [if_neg (by omega)]; omega

theorem T_par {n : ℕ} (h : n % 2 = 0) : 2 * T n = n := by
  unfold T; rw [if_pos h]; omega

theorem iter_add (i j n : ℕ) : T^[i + j] n = T^[j] (T^[i] n) := by
  rw [add_comm, Function.iterate_add_apply]

/-- Racha impar: `2^m (T^m x + 1) = 3^m (x + 1)`. -/
theorem tramo_impar : ∀ m x : ℕ, (∀ t, t < m → T^[t] x % 2 = 1) →
    2 ^ m * (T^[m] x + 1) = 3 ^ m * (x + 1) := by
  intro m
  induction m with
  | zero => intro x _; simp
  | succ m ih =>
    intro x h
    have e := ih x (fun t ht => h t (by omega))
    have hm := T_impar (h m (by omega))
    have h2 : 2 * T (T^[m] x) + 2 = 3 * (T^[m] x + 1) := by omega
    rw [Function.iterate_succ_apply']
    calc 2 ^ (m + 1) * (T (T^[m] x) + 1) = 2 ^ m * (2 * T (T^[m] x) + 2) := by ring
      _ = 2 ^ m * (3 * (T^[m] x + 1)) := by rw [h2]
      _ = 3 * (2 ^ m * (T^[m] x + 1)) := by ring
      _ = 3 * (3 ^ m * (x + 1)) := by rw [e]
      _ = 3 ^ (m + 1) * (x + 1) := by ring

/-- Racha par: `2^m T^m x = x`. -/
theorem tramo_par : ∀ m x : ℕ, (∀ t, t < m → T^[t] x % 2 = 0) → 2 ^ m * T^[m] x = x := by
  intro m
  induction m with
  | zero => intro x _; simp
  | succ m ih =>
    intro x h
    have e := ih x (fun t ht => h t (by omega))
    have hm := T_par (h m (by omega))
    rw [Function.iterate_succ_apply']
    calc 2 ^ (m + 1) * T (T^[m] x) = 2 ^ m * (2 * T (T^[m] x)) := by ring
      _ = 2 ^ m * T^[m] x := by rw [hm]
      _ = x := e

theorem S_add : ∀ i j n : ℕ, S (i + j) n = S i n + S j (T^[i] n) := by
  intro i
  induction i with
  | zero => intro j n; simp [S]
  | succ i ih =>
    intro j n
    rw [show i + 1 + j = (i + j) + 1 by omega]
    simp only [S]
    rw [ih j (T n), Function.iterate_succ_apply]
    omega

theorem S_impar : ∀ m x : ℕ, (∀ t, t < m → T^[t] x % 2 = 1) → S m x = m := by
  intro m
  induction m with
  | zero => intro x _; rfl
  | succ m ih =>
    intro x h
    have h0 : x % 2 = 1 := h 0 (by omega)
    have hs := ih (T x) (fun t ht => by
      have := h (t + 1) (by omega)
      rwa [Function.iterate_succ_apply] at this)
    simp only [S]
    omega

theorem S_par : ∀ m x : ℕ, (∀ t, t < m → T^[t] x % 2 = 0) → S m x = 0 := by
  intro m
  induction m with
  | zero => intro x _; rfl
  | succ m ih =>
    intro x h
    have h0 : x % 2 = 0 := h 0 (by omega)
    have hs := ih (T x) (fun t ht => by
      have := h (t + 1) (by omega)
      rwa [Function.iterate_succ_apply] at this)
    simp only [S]
    omega

/-! ## Aritmética auxiliar -/

/-- `72 k^84 < 2^k` para `k ≥ 1024`. -/
theorem poli_exp {k : ℕ} (hk : 1024 ≤ k) : 72 * k ^ 84 < 2 ^ k := by
  have hk0 : k ≠ 0 := by omega
  have h1 : k < 2 ^ (Nat.log 2 k).succ := Nat.lt_pow_succ_log_self (by norm_num) k
  have h2 : 2 ^ Nat.log 2 k ≤ k := Nat.pow_log_le_self 2 hk0
  set m := Nat.log 2 k with hm
  have hm10 : 10 ≤ m := by
    by_contra h
    have h' : m + 1 ≤ 10 := by omega
    have : 2 ^ (m + 1) ≤ 2 ^ 10 := Nat.pow_le_pow_right (by norm_num) h'
    have : k < 2 ^ 10 := lt_of_lt_of_le h1 this
    omega
  have h3 : ∀ m, 10 ≤ m → 84 * m + 91 ≤ 2 ^ m := by
    intro m hm
    induction m, hm using Nat.le_induction with
    | base => norm_num
    | succ m hm ih =>
      have : 1024 ≤ 2 ^ m := by
        calc 1024 = 2 ^ 10 := by norm_num
          _ ≤ 2 ^ m := Nat.pow_le_pow_right (by norm_num) hm
      rw [pow_succ]
      omega
  have h4 : 84 * m + 91 ≤ k := le_trans (h3 m hm10) h2
  have h5 : k ^ 84 < (2 ^ (m + 1)) ^ 84 := Nat.pow_lt_pow_left h1 (by norm_num)
  calc 72 * k ^ 84 < 2 ^ 7 * (2 ^ (m + 1)) ^ 84 := by
        have : 72 * k ^ 84 ≤ 72 * (2 ^ (m + 1)) ^ 84 := Nat.mul_le_mul_left 72 h5.le
        have hp : 0 < (2 ^ (m + 1)) ^ 84 := by positivity
        have : 72 * (2 ^ (m + 1)) ^ 84 < 2 ^ 7 * (2 ^ (m + 1)) ^ 84 :=
          Nat.mul_lt_mul_of_pos_right (by norm_num) hp
        omega
    _ = 2 ^ (84 * m + 91) := by rw [← pow_mul, ← pow_add]; ring_nf
    _ ≤ 2 ^ k := Nat.pow_le_pow_right (by norm_num) h4

/-- El `k` del primer cruce queda fijado por `q`: `k = log2(3^q) + 1`. -/
theorem k_de_q {k q : ℕ} (h1 : 2 ^ k < 2 * 3 ^ q) (h2 : 3 ^ q < 2 ^ k) :
    k = Nat.log2 (3 ^ q) + 1 := by
  have hne : 3 ^ q ≠ 0 := by positivity
  have a1 := Nat.log2_self_le hne
  have a2 := Nat.lt_log2_self (n := 3 ^ q)
  set L := Nat.log2 (3 ^ q)
  have c1 : L < k := by
    have : 2 ^ L < 2 ^ k := lt_of_le_of_lt a1 h2
    exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 this
  have c2 : k < L + 2 := by
    have : 2 ^ k < 2 ^ (L + 2) := by
      calc 2 ^ k < 2 * 3 ^ q := h1
        _ < 2 * 2 ^ (L + 1) := by omega
        _ = 2 ^ (L + 2) := by ring
    exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 this
  omega

/-- Núcleo aritmético: con `u = 2^a`, `v = 2^c`, `w = 2^(a+b)`, `A = 3^a`, `C = 3^c`,
    `D = 2^k − 3^q` y `Bv` el término aditivo menos las correcciones, el fallo del descenso
    (`D n ≤ Bv`) y las dos congruencias obligan a `u v D³ < 18 (AC)³`. -/
theorem nucleo {u v w A C D Bv n y2 : ℕ} (hu : 2 ≤ u) (hw : 2 * u ≤ w) (hwA : w < A)
    (hA : A < u * u) (hDP : D < A * C) (hB : Bv < 2 * (A * C))
    (hf : D * n ≤ Bv) (h1 : u ≤ n + 1) (h2 : v ≤ y2 + 1) (h3 : w * y2 + u = A * (n + 1)) :
    u * v * D * (D * D) < 18 * ((A * C) * (A * C) * (A * C)) := by
  set P := A * C with hP
  have hPpos : 0 < P := by omega
  -- u D < 3 P
  have hUD : u * D < 3 * P := by
    have e1 : u * D ≤ (n + 1) * D := Nat.mul_le_mul_right D h1
    have e2 : (n + 1) * D = D * n + D := by ring
    omega
  -- D w v < 4 A P
  have hwv : w * v + u ≤ A * (n + 1) + w := by
    have : w * v ≤ w * (y2 + 1) := Nat.mul_le_mul_left w h2
    have e : w * (y2 + 1) = w * y2 + w := by ring
    omega
  have hDwv : D * (w * v) < 4 * (A * P) := by
    have e1 : D * (w * v) ≤ D * (A * (n + 1) + w) := by
      apply Nat.mul_le_mul_left; omega
    have e2 : D * (A * (n + 1) + w) = A * (D * n) + A * D + D * w := by ring
    have e3 : A * (D * n) ≤ A * Bv := Nat.mul_le_mul_left A hf
    have e4 : A * Bv < A * (2 * P) := Nat.mul_lt_mul_of_pos_left hB (by omega)
    have e5 : A * D < A * P := Nat.mul_lt_mul_of_pos_left hDP (by omega)
    have e6 : D * w ≤ D * A := Nat.mul_le_mul_left D hwA.le
    have e7 : D * A = A * D := by ring
    have e8 : A * (2 * P) = 2 * (A * P) := by ring
    omega
  have hUVD : u * v * D < 2 * (A * P) := by
    have e1 : 2 * (u * v * D) ≤ D * (w * v) := by
      have := Nat.mul_le_mul_right (v * D) hw
      calc 2 * (u * v * D) = 2 * u * (v * D) := by ring
        _ ≤ w * (v * D) := this
        _ = D * (w * v) := by ring
    omega
  rcases Nat.eq_zero_or_pos D with hD0 | hDpos
  · subst hD0
    simp only [mul_zero]
    positivity
  · have hDD : 0 < D * D := Nat.mul_pos hDpos hDpos
    calc u * v * D * (D * D) < 2 * (A * P) * (D * D) := Nat.mul_lt_mul_of_pos_right hUVD hDD
      _ = 2 * P * (A * (D * D)) := by ring
      _ ≤ 2 * P * (u * u * (D * D)) := by
          apply Nat.mul_le_mul_left
          exact Nat.mul_le_mul_right _ hA.le
      _ = 2 * P * ((u * D) * (u * D)) := by ring
      _ < 2 * P * ((3 * P) * (3 * P)) := by
          apply Nat.mul_lt_mul_of_pos_left _ (by omega)
          exact Nat.mul_lt_mul'' hUD hUD
      _ = 18 * (P * P * P) := by ring

/-! ## Los dos cálculos finitos, en el núcleo -/

/-- Para `q ≤ 645`, con `k = log2(3^q) + 1` y `D = 2^k − 3^q`: o bien `18·27^q ≤ 2^q D³`
    (lo que contradice el núcleo), o bien `k ≤ 27` y `2·3^q ≤ 51 D` (lo que deja `n ≤ 50`). -/
theorem finito_q : ∀ q, q ≤ 645 →
    18 * 27 ^ q ≤ 2 ^ q * (2 ^ (Nat.log2 (3 ^ q) + 1) - 3 ^ q) ^ 3 ∨
      (Nat.log2 (3 ^ q) + 1 ≤ 27 ∧ 2 * 3 ^ q ≤ 51 * (2 ^ (Nat.log2 (3 ^ q) + 1) - 3 ^ q)) := by
  decide +kernel

/-- CST para `2 ≤ n ≤ 50` con primer cruce `k ≤ 27`. -/
theorem finito_n : ∀ n, n ≤ 50 → ∀ k, k ≤ 27 → 2 ≤ n → PrimerCruce n k → T^[k] n < n := by
  decide +kernel

/-! ## El teorema -/

theorem par_ne_impar {x y : ℕ} (hx : x % 2 = 0) (hy : y % 2 = 1) : x ≠ y := by omega

theorem pot2_par {m : ℕ} (hm : 1 ≤ m) : 2 ^ m % 2 = 0 := by
  obtain ⟨j, rfl⟩ : ∃ j, m = j + 1 := ⟨m - 1, by omega⟩
  rw [pow_succ]; omega

theorem pot3_impar (m : ℕ) : 3 ^ m % 2 = 1 := by
  induction m with
  | zero => rfl
  | succ m ih => rw [pow_succ]; omega

set_option exponentiation.threshold 1100 in
set_option maxHeartbeats 1000000 in
/-- **Ocelotas.** Si la palabra de paridad de `n ≥ 2` hasta su primer cruce del coeficiente
    tiene dos rachas impares, `1^a 0^b 1^c 0^d`, entonces en ese paso hay descenso real. -/
theorem ocelotas (hR : RhinEntera) {n a b c d : ℕ} (hn : 2 ≤ n)
    (ha : 1 ≤ a) (hb : 1 ≤ b) (hc : 1 ≤ c) (hd : 1 ≤ d)
    (hw : DosRachas n a b c d) (hk : PrimerCruce n (a + b + c + d)) :
    T^[a + b + c + d] n < n := by
  have hkc := hk
  obtain ⟨w1, w2, w3, w4⟩ := hw
  obtain ⟨hpre, hfin⟩ := hk
  obtain ⟨k, hkdef⟩ : ∃ k, k = a + b + c + d := ⟨_, rfl⟩
  rw [← hkdef] at hkc hpre hfin ⊢
  -- los tramos
  have r2 : ∀ t, t < b → T^[t] (T^[a] n) % 2 = 0 := fun t ht => by
    rw [← iter_add]; exact w2 t ht
  have r3 : ∀ t, t < c → T^[t] (T^[a + b] n) % 2 = 1 := fun t ht => by
    rw [← iter_add]; exact w3 t ht
  have r4 : ∀ t, t < d → T^[t] (T^[a + b + c] n) % 2 = 0 := fun t ht => by
    rw [← iter_add]; exact w4 t ht
  have E1 := tramo_impar a n w1
  have E2 := tramo_par b (T^[a] n) r2
  have E3 := tramo_impar c (T^[a + b] n) r3
  have E4 := tramo_par d (T^[a + b + c] n) r4
  rw [← iter_add] at E2 E3 E4
  rw [← hkdef] at E4
  -- las cuentas de impares
  have Sab : S (a + b) n = a := by
    rw [S_add, S_impar a n w1, S_par b _ r2]; omega
  have Sabc : S (a + b + c) n = a + c := by
    rw [S_add, Sab, S_impar c _ r3]
  have Sfin : ∀ e, e ≤ d → S (a + b + c + e) n = a + c := by
    intro e he
    rw [S_add, Sabc, S_par e _ (fun t ht => r4 t (by omega))]
    omega
  -- el primer cruce
  have hab0 : 2 ^ (a + b) ≤ 3 ^ a := by
    have := hpre (a + b) (by omega) (by omega)
    rwa [Sab] at this
  have hab : 2 ^ (a + b) < 3 ^ a :=
    lt_of_le_of_ne hab0 (par_ne_impar (pot2_par (by omega)) (pot3_impar a))
  have hk1 : 2 ^ (k - 1) < 3 ^ (a + c) := by
    have h := hpre (k - 1) (by omega) (by omega)
    rw [show k - 1 = a + b + c + (d - 1) by omega, Sfin (d - 1) (by omega)] at h
    rw [show k - 1 = a + b + c + (d - 1) by omega]
    exact lt_of_le_of_ne h (par_ne_impar (pot2_par (by omega)) (pot3_impar _))
  have hkq : 3 ^ (a + c) < 2 ^ k := by
    have h := hfin
    rw [hkdef, Sfin d le_rfl] at h
    rw [hkdef]; exact h
  have hk2 : 2 ^ k < 2 * 3 ^ (a + c) := by
    have : 2 ^ k = 2 * 2 ^ (k - 1) := by
      rw [← pow_succ']; congr 1; omega
    omega
  -- supongamos que no desciende
  by_contra hcon
  have hfallo : n ≤ T^[k] n := by omega
  set y1 := T^[a] n
  set y2 := T^[a + b] n
  set y3 := T^[a + b + c] n
  set y4 := T^[k] n
  -- la identidad clave
  have KI : 2 ^ k * y4 + 2 ^ (a + b + c) + 3 ^ c * 2 ^ a =
      3 ^ a * 3 ^ c * n + 3 ^ a * 3 ^ c + 3 ^ c * 2 ^ (a + b) := by
    calc 2 ^ k * y4 + 2 ^ (a + b + c) + 3 ^ c * 2 ^ a
        = 2 ^ (a + b + c) * (2 ^ d * y4) + 2 ^ (a + b + c) + 3 ^ c * 2 ^ a := by
          rw [hkdef]; ring
      _ = 2 ^ (a + b + c) * y3 + 2 ^ (a + b + c) + 3 ^ c * 2 ^ a := by rw [E4]
      _ = 2 ^ (a + b) * (2 ^ c * (y3 + 1)) + 3 ^ c * 2 ^ a := by ring
      _ = 2 ^ (a + b) * (3 ^ c * (y2 + 1)) + 3 ^ c * 2 ^ a := by rw [E3]
      _ = 3 ^ c * 2 ^ a * (2 ^ b * y2) + 3 ^ c * 2 ^ (a + b) + 3 ^ c * 2 ^ a := by ring
      _ = 3 ^ c * 2 ^ a * y1 + 3 ^ c * 2 ^ (a + b) + 3 ^ c * 2 ^ a := by rw [E2]
      _ = 3 ^ c * (2 ^ a * (y1 + 1)) + 3 ^ c * 2 ^ (a + b) := by ring
      _ = 3 ^ c * (3 ^ a * (n + 1)) + 3 ^ c * 2 ^ (a + b) := by rw [E1]
      _ = 3 ^ a * 3 ^ c * n + 3 ^ a * 3 ^ c + 3 ^ c * 2 ^ (a + b) := by ring
  -- abreviaturas
  have hP : 3 ^ (a + c) = 3 ^ a * 3 ^ c := pow_add 3 a c
  obtain ⟨P, hPdef⟩ : ∃ P, P = 3 ^ a * 3 ^ c := ⟨_, rfl⟩
  rw [← hPdef] at KI hP
  rw [hP] at hk1 hkq hk2
  obtain ⟨D, hD⟩ : ∃ D, D = 2 ^ k - P := ⟨_, rfl⟩
  obtain ⟨Bv, hBv⟩ : ∃ Bv, Bv = P + 3 ^ c * 2 ^ (a + b) - 2 ^ (a + b + c) - 3 ^ c * 2 ^ a :=
    ⟨_, rfl⟩
  -- el fallo en forma D n ≤ Bv
  have hQ : 3 ^ c * 2 ^ (a + b) < P := by
    rw [hPdef, mul_comm (3 ^ a)]
    exact Nat.mul_lt_mul_of_pos_left hab (by positivity)
  have hf : D * n ≤ Bv := by
    have e1 : 2 ^ k * n ≤ 2 ^ k * y4 := Nat.mul_le_mul_left _ hfallo
    have e2 : D * n = 2 ^ k * n - P * n := by rw [hD, Nat.sub_mul]
    rw [e2]
    omega
  have hB : Bv < 2 * P := by
    have : Bv ≤ P + 3 ^ c * 2 ^ (a + b) := by
      rw [hBv]; exact le_trans (Nat.sub_le _ _) (Nat.sub_le _ _)
    omega
  have hDP : D < P := by rw [hD]; omega
  -- las congruencias
  have cop2a : Nat.Coprime (2 ^ a) (3 ^ a) := Nat.Coprime.pow a a (by decide)
  have cop2c : Nat.Coprime (2 ^ c) (3 ^ c) := Nat.Coprime.pow c c (by decide)
  have h1 : 2 ^ a ≤ n + 1 := by
    have hdv : 2 ^ a ∣ 3 ^ a * (n + 1) := ⟨y1 + 1, E1.symm⟩
    exact Nat.le_of_dvd (by omega) (cop2a.dvd_of_dvd_mul_left hdv)
  have h2 : 2 ^ c ≤ y2 + 1 := by
    have hdv : 2 ^ c ∣ 3 ^ c * (y2 + 1) := ⟨y3 + 1, E3.symm⟩
    exact Nat.le_of_dvd (by omega) (cop2c.dvd_of_dvd_mul_left hdv)
  have h3 : 2 ^ (a + b) * y2 + 2 ^ a = 3 ^ a * (n + 1) := by
    rw [← E1, ← E2]; ring
  have hw2 : 2 * 2 ^ a ≤ 2 ^ (a + b) := by
    rw [pow_add]
    have : 2 ≤ 2 ^ b := by
      calc 2 = 2 ^ 1 := by norm_num
        _ ≤ 2 ^ b := Nat.pow_le_pow_right (by norm_num) hb
    nlinarith [Nat.one_le_two_pow (n := a)]
  have hu2 : 2 ≤ 2 ^ a := by
    calc 2 = 2 ^ 1 := by norm_num
      _ ≤ 2 ^ a := Nat.pow_le_pow_right (by norm_num) ha
  have hA : 3 ^ a < 2 ^ a * 2 ^ a := by
    rw [← mul_pow]; exact Nat.pow_lt_pow_left (by norm_num) (by omega)
  have hC : 3 ^ c < 2 ^ c * 2 ^ c := by
    rw [← mul_pow]; exact Nat.pow_lt_pow_left (by norm_num) (by omega)
  have N := nucleo hu2 hw2 hab hA (by rw [← hPdef]; exact hDP) (by rw [← hPdef]; exact hB)
    hf h1 h2 h3
  rw [← hPdef] at N
  -- Rhin: n < 2 k^14
  have hRk := hR k (a + c) (by rw [hP]; omega) (by rw [hP]; exact hkq)
  rw [hP, ← hD] at hRk
  have hn14 : n < 2 * k ^ 14 := by
    have e1 : n * P ≤ n * (D * k ^ 14) := Nat.mul_le_mul_left n hRk
    have e2 : n * (D * k ^ 14) = (D * n) * k ^ 14 := by ring
    have e3 : (D * n) * k ^ 14 ≤ Bv * k ^ 14 := Nat.mul_le_mul_right _ hf
    have e4 : Bv * k ^ 14 < 2 * P * k ^ 14 :=
      Nat.mul_lt_mul_of_pos_right hB (pow_pos (by omega) 14)
    have e5 : n * P < (2 * k ^ 14) * P := by
      calc n * P ≤ Bv * k ^ 14 := by rw [e2] at e1; exact le_trans e1 e3
        _ < 2 * P * k ^ 14 := e4
        _ = (2 * k ^ 14) * P := by ring
    exact Nat.lt_of_mul_lt_mul_right e5
  -- k ≤ 1023
  have hk1023 : k ≤ 1023 := by
    by_contra hbig
    have hpe := poli_exp (k := k) (by omega)
    have hk14 : 1 ≤ k ^ 14 := Nat.one_le_pow _ _ (by omega)
    have hu : 2 ^ a ≤ 2 * k ^ 14 := by omega
    -- 2 u v < A (n + 2) ≤ A (2 k^14 + 1)
    have hv1 : 2 * 2 ^ a * 2 ^ c < 3 ^ a * (2 * k ^ 14 + 1) := by
      have e1 : 2 ^ (a + b) * 2 ^ c ≤ 2 ^ (a + b) * (y2 + 1) := Nat.mul_le_mul_left _ h2
      have e2 : 2 * 2 ^ a * 2 ^ c ≤ 2 ^ (a + b) * 2 ^ c := Nat.mul_le_mul_right _ hw2
      have e3 : 2 ^ (a + b) * (y2 + 1) = 3 ^ a * (n + 1) - 2 ^ a + 2 ^ (a + b) := by
        have : 2 ^ (a + b) * (y2 + 1) = 2 ^ (a + b) * y2 + 2 ^ (a + b) := by ring
        omega
      have e4 : 3 ^ a * (n + 1) ≤ 3 ^ a * (2 * k ^ 14) := Nat.mul_le_mul_left _ (by omega)
      have e5 : 3 ^ a * (2 * k ^ 14 + 1) = 3 ^ a * (2 * k ^ 14) + 3 ^ a := by ring
      omega
    -- v < 3 k^28
    have hv : 2 ^ c < 3 * k ^ 28 := by
      have e1 : 3 ^ a * (2 * k ^ 14 + 1) < 2 ^ a * 2 ^ a * (2 * k ^ 14 + 1) :=
        Nat.mul_lt_mul_of_pos_right hA (by omega)
      have e2 : 2 ^ a * 2 ^ a * (2 * k ^ 14 + 1) ≤ 2 ^ a * (2 * k ^ 14) * (2 * k ^ 14 + 1) := by
        apply Nat.mul_le_mul_right; exact Nat.mul_le_mul_left _ hu
      have e3 : 2 ^ a * (2 * 2 ^ c) < 2 ^ a * (2 * k ^ 14 * (2 * k ^ 14 + 1)) := by
        calc 2 ^ a * (2 * 2 ^ c) = 2 * 2 ^ a * 2 ^ c := by ring
          _ < 2 ^ a * (2 * k ^ 14) * (2 * k ^ 14 + 1) := by omega
          _ = 2 ^ a * (2 * k ^ 14 * (2 * k ^ 14 + 1)) := by ring
      have e4 := Nat.lt_of_mul_lt_mul_left e3
      have e5 : k ^ 14 ≤ k ^ 28 := Nat.pow_le_pow_right (by omega) (by norm_num)
      have e6 : 2 * k ^ 14 * (2 * k ^ 14 + 1) = 2 * (2 * k ^ 28 + k ^ 14) := by ring
      omega
    -- P < 36 k^84
    have hP36 : P < 36 * k ^ 84 := by
      have e1 : 3 ^ a < 4 * k ^ 28 := by
        have : 2 ^ a * 2 ^ a ≤ (2 * k ^ 14) * (2 * k ^ 14) := Nat.mul_le_mul hu hu
        have e : (2 * k ^ 14) * (2 * k ^ 14) = 4 * k ^ 28 := by ring
        omega
      have e2 : 3 ^ c < 9 * k ^ 56 := by
        have : 2 ^ c * 2 ^ c ≤ (3 * k ^ 28) * (3 * k ^ 28) := Nat.mul_le_mul hv.le hv.le
        have e : (3 * k ^ 28) * (3 * k ^ 28) = 9 * k ^ 56 := by ring
        omega
      calc P = 3 ^ a * 3 ^ c := hPdef
        _ < (4 * k ^ 28) * (9 * k ^ 56) := Nat.mul_lt_mul'' e1 e2
        _ = 36 * k ^ 84 := by ring
    omega
  -- q ≤ 645
  have hq645 : a + c ≤ 645 := by
    by_contra hbig
    have e1 : 3 ^ 646 ≤ 3 ^ (a + c) := Nat.pow_le_pow_right (by norm_num) (by omega)
    have e2 : 2 ^ k ≤ 2 ^ 1023 := Nat.pow_le_pow_right (by norm_num) hk1023
    have e3 : (2 : ℕ) ^ 1023 < 3 ^ 646 := by decide +kernel
    rw [hP] at e1
    omega
  -- k queda fijado por q
  have hkq' : k = Nat.log2 (3 ^ (a + c)) + 1 := k_de_q (by rw [hP]; exact hk2) (by rw [hP]; exact hkq)
  have hfin_q := finito_q (a + c) hq645
  rw [← hkq', hP] at hfin_q
  rcases hfin_q with hA1 | ⟨hk27, h51⟩
  · -- contradice el núcleo
    have e1 : 2 ^ a * 2 ^ c * D * (D * D) = 2 ^ (a + c) * (2 ^ k - P) ^ 3 := by
      rw [hD, pow_add]; ring
    have e2 : 18 * (P * P * P) = 18 * 27 ^ (a + c) := by
      rw [← hP, show (27 : ℕ) = 3 ^ 3 by norm_num, ← pow_mul]
      ring
    rw [e1, e2] at N
    omega
  · -- queda n ≤ 50
    rw [← hD] at h51
    have hDpos : 0 < D := by omega
    have hn50 : n ≤ 50 := by
      have e1 : D * n < 51 * D := by omega
      have e2 : D * n < D * 51 := by rw [mul_comm 51] at e1; exact e1
      have := Nat.lt_of_mul_lt_mul_left e2
      omega
    have := finito_n n hn50 k hk27 hn hkc
    omega

end Ocelotas

#print axioms Ocelotas.finito_q
#print axioms Ocelotas.finito_n
#print axioms Ocelotas.ocelotas

/- Cotejo con los cálculos: el caso más ajustado de `dos_rachas.py` es `n = 39`, palabra
   `1^3 0^1 1^2 0^2`, primer cruce en `k = 8` y `T^8(39) = 38`. -/
#guard Ocelotas.T^[8] 39 == 38
#guard decide (Ocelotas.PrimerCruce 39 8)
