import PerdicesComplejidad

/-! # Perdices: ningún racional 2-ádico tiene palabra de paridades sturmiana.

Para `q` impar y positivo, `Tq q x = x/2` si `x` es par y `(3x+q)/2` si es impar.
Si `x_t = p_t/q`, el atajo de Collatz sobre racionales de denominador impar da
`p_(t+1) = Tq q p_t`, con las mismas paridades. Una palabra es sturmiana si tiene
exactamente `m+1` factores distintos de cada largo `m`. Se prueba que la palabra de
paridades de `p` bajo `Tq q` nunca lo es: si la órbita es inyectiva, por conteo de
residuos módulo `2^m`; si no, porque es eventualmente periódica.
-/

namespace PerdicesRacional

/-- Mapa `3x+q` sobre enteros. -/
def Tq (q x : ℤ) : ℤ := if x % 2 = 0 then x / 2 else (3 * x + q) / 2

/-- Bit de subida: `1` si `x` es impar. -/
def sube (x : ℤ) : ℕ := if x % 2 = 0 then 0 else 1

/-- Pasos impares entre los `t` primeros. -/
def S (q : ℤ) : ℕ → ℤ → ℕ
  | 0, _ => 0
  | t + 1, x => sube x + S q t (Tq q x)

theorem paso_par {q x : ℤ} (h : x % 2 = 0) : 2 * Tq q x = x := by
  unfold Tq
  rw [if_pos h]
  omega

theorem paso_impar {q x : ℤ} (hq : q % 2 = 1) (h : x % 2 = 1) :
    2 * Tq q x = 3 * x + q := by
  unfold Tq
  rw [if_neg (by omega)]
  omega

/-- Mismas `k` paridades: congruencia módulo `2^k`. -/
theorem congruentes {q : ℤ} (hq : q % 2 = 1) : ∀ (k : ℕ) (x y : ℤ),
    (∀ i, i < k → (Tq q)^[i] x % 2 = (Tq q)^[i] y % 2) → (2 : ℤ) ^ k ∣ x - y := by
  intro k
  induction k with
  | zero => intro x y _; simp
  | succ k ih =>
    intro x y h
    have h0 : x % 2 = y % 2 := by simpa using h 0 (by omega)
    have hT : (2 : ℤ) ^ k ∣ Tq q x - Tq q y := ih (Tq q x) (Tq q y) (fun i hi => by
      have := h (i + 1) (by omega)
      simpa only [Function.iterate_succ_apply] using this)
    obtain ⟨c, hc⟩ := hT
    rcases Int.emod_two_eq_zero_or_one x with hx | hx
    · have e1 := paso_par (q := q) hx
      have e2 := paso_par (q := q) (show y % 2 = 0 by omega)
      exact ⟨c, by rw [pow_succ]; linear_combination e2 - e1 + 2 * hc⟩
    · have e1 := paso_impar hq hx
      have e2 := paso_impar hq (show y % 2 = 1 by omega)
      have h3 : (2 : ℤ) ^ (k + 1) ∣ 3 * (x - y) :=
        ⟨c, by rw [pow_succ]; linear_combination e2 - e1 + 2 * hc⟩
      have hcop : IsCoprime ((2 : ℤ) ^ (k + 1)) 3 := by
        apply IsCoprime.pow_left
        rw [Int.isCoprime_iff_gcd_eq_one]
        rfl
      exact hcop.dvd_of_dvd_mul_left h3

/-- Recíproco: congruencia módulo `2^k` da las mismas `k` paridades. -/
theorem mismas_paridades {q : ℤ} (hq : q % 2 = 1) : ∀ (k : ℕ) (x y : ℤ),
    (2 : ℤ) ^ k ∣ x - y → ∀ i, i < k → (Tq q)^[i] x % 2 = (Tq q)^[i] y % 2 := by
  intro k
  induction k with
  | zero => intro x y _ i hi; omega
  | succ k ih =>
    intro x y h i hi
    obtain ⟨c, hc⟩ := h
    have hc' : x - y = 2 * (2 ^ k * c) := by rw [hc, pow_succ]; ring
    have h0 : x % 2 = y % 2 := by omega
    rcases i with _ | i
    · simpa using h0
    · rw [Function.iterate_succ_apply, Function.iterate_succ_apply]
      apply ih (Tq q x) (Tq q y) _ i (by omega)
      rcases Int.emod_two_eq_zero_or_one x with hx | hx
      · have e1 := paso_par (q := q) hx
        have e2 := paso_par (q := q) (show y % 2 = 0 by omega)
        have h2 : 2 * (Tq q x - Tq q y) = 2 * (2 ^ k * c) := by
          linear_combination e1 - e2 + hc'
        exact ⟨c, mul_left_cancel₀ two_ne_zero h2⟩
      · have e1 := paso_impar hq hx
        have e2 := paso_impar hq (show y % 2 = 1 by omega)
        have h2 : 2 * (Tq q x - Tq q y) = 2 * (2 ^ k * (3 * c)) := by
          linear_combination e1 - e2 + 3 * hc'
        exact ⟨3 * c, mul_left_cancel₀ two_ne_zero h2⟩

/-- Un paso: `|x|+q` se multiplica a lo sumo por `3/2` si `x` es impar y no crece si es par. -/
theorem paso_tamano {q x : ℤ} (hq : q % 2 = 1) (hq0 : 0 ≤ q) :
    2 ^ sube x * (|Tq q x| + q) ≤ 3 ^ sube x * (|x| + q) := by
  unfold sube
  rcases Int.emod_two_eq_zero_or_one x with h | h
  · rw [if_pos h, pow_zero, pow_zero, one_mul, one_mul]
    have e := paso_par (q := q) h
    have : |x| = 2 * |Tq q x| := by
      calc |x| = |2 * Tq q x| := by rw [e]
        _ = 2 * |Tq q x| := by rw [abs_mul]; norm_num
    have : 0 ≤ |Tq q x| := abs_nonneg _
    linarith
  · rw [if_neg (by omega), pow_one, pow_one]
    have e := paso_impar hq h
    have h1 : |2 * Tq q x| = 2 * |Tq q x| := by
      rw [abs_mul]
      norm_num
    have h2 : |3 * x + q| ≤ 3 * |x| + q := by
      calc |3 * x + q| ≤ |3 * x| + |q| := abs_add_le _ _
        _ = 3 * |x| + q := by rw [abs_mul, abs_of_nonneg hq0]; norm_num
    rw [e] at h1
    linarith

/-- `2^(S_t) (|x_t|+q) <= 3^(S_t) (|p|+q)`. -/
theorem cota {q : ℤ} (hq : q % 2 = 1) (hq0 : 0 ≤ q) : ∀ (t : ℕ) (x : ℤ),
    (2 : ℤ) ^ S q t x * (|(Tq q)^[t] x| + q) ≤ 3 ^ S q t x * (|x| + q) := by
  intro t
  induction t with
  | zero => intro x; simp [S]
  | succ t ih =>
    intro x
    have h1 := ih (Tq q x)
    have h2 := paso_tamano (x := x) hq hq0
    rw [S, Function.iterate_succ_apply, pow_add, pow_add]
    have h3 : (0 : ℤ) ≤ 3 ^ S q t (Tq q x) := by positivity
    have h4 : (0 : ℤ) ≤ 2 ^ sube x := by positivity
    calc (2 : ℤ) ^ sube x * 2 ^ S q t (Tq q x) * (|(Tq q)^[t] (Tq q x)| + q)
        = 2 ^ sube x * (2 ^ S q t (Tq q x) * (|(Tq q)^[t] (Tq q x)| + q)) := by ring
      _ ≤ 2 ^ sube x * (3 ^ S q t (Tq q x) * (|Tq q x| + q)) :=
          mul_le_mul_of_nonneg_left h1 h4
      _ = 3 ^ S q t (Tq q x) * (2 ^ sube x * (|Tq q x| + q)) := by ring
      _ ≤ 3 ^ S q t (Tq q x) * (3 ^ sube x * (|x| + q)) :=
          mul_le_mul_of_nonneg_left h2 h3
      _ = 3 ^ sube x * 3 ^ S q t (Tq q x) * (|x| + q) := by ring

theorem S_le (q : ℤ) : ∀ (t : ℕ) (x : ℤ), S q t x ≤ t := by
  intro t
  induction t with
  | zero => intro x; simp [S]
  | succ t ih =>
    intro x
    have := ih (Tq q x)
    unfold S sube
    split_ifs <;> omega

/-- Antes de `K` pasos, `|x_t|+q <= 2^m` si `3^K (|p|+q) <= 2^(m+K)`. -/
theorem bajo_umbral {q p : ℤ} {m K t : ℕ} (hq : q % 2 = 1) (hq0 : 0 ≤ q) (ht : t ≤ K)
    (h : (3 : ℤ) ^ K * (|p| + q) ≤ 2 ^ (m + K)) :
    |(Tq q)^[t] p| + q ≤ 2 ^ m := by
  have hc := cota hq hq0 t p
  set s := S q t p with hs
  have hsK : s ≤ K := le_trans (S_le q t p) ht
  obtain ⟨r, hr⟩ : ∃ r, K = s + r := ⟨K - s, by omega⟩
  have h23 : (2 : ℤ) ^ r ≤ 3 ^ r := pow_le_pow_left₀ (by norm_num) (by norm_num) r
  have hpos2 : (0 : ℤ) ≤ 2 ^ s * (|(Tq q)^[t] p| + q) := by positivity
  have key : (2 : ℤ) ^ K * (|(Tq q)^[t] p| + q) ≤ 2 ^ K * 2 ^ m := by
    calc (2 : ℤ) ^ K * (|(Tq q)^[t] p| + q) = 2 ^ r * (2 ^ s * (|(Tq q)^[t] p| + q)) := by
          rw [hr, pow_add]; ring
      _ ≤ 3 ^ r * (3 ^ s * (|p| + q)) :=
          mul_le_mul h23 hc hpos2 (by positivity)
      _ = 3 ^ K * (|p| + q) := by rw [hr, pow_add]; ring
      _ ≤ 2 ^ (m + K) := h
      _ = 2 ^ K * 2 ^ m := by rw [← pow_add, Nat.add_comm m K]
  exact le_of_mul_le_mul_left key (by positivity)

/-- Factor de paridades de largo `m` en el instante `t`. -/
def factor (q p : ℤ) (m t : ℕ) : Fin m → ℤ := fun k => (Tq q)^[t + k] p % 2

/-- En una órbita inyectiva, dos instantes con `|x|+q <= 2^m` y el mismo factor de
largo `m+1` coinciden. -/
theorem factores_distintos {q p : ℤ} {m t t' : ℕ} (hq : q % 2 = 1) (hq1 : 1 ≤ q)
    (hi : Function.Injective (fun j => (Tq q)^[j] p))
    (ht : |(Tq q)^[t] p| + q ≤ 2 ^ m) (ht' : |(Tq q)^[t'] p| + q ≤ 2 ^ m)
    (hf : factor q p (m + 1) t = factor q p (m + 1) t') : t = t' := by
  have hp : ∀ k, k < m + 1 →
      (Tq q)^[k] ((Tq q)^[t] p) % 2 = (Tq q)^[k] ((Tq q)^[t'] p) % 2 := by
    intro k hk
    have h := congrFun hf ⟨k, hk⟩
    simp only [factor] at h
    rwa [show t + k = k + t by omega, show t' + k = k + t' by omega,
      Function.iterate_add_apply, Function.iterate_add_apply] at h
  obtain ⟨c, hc⟩ := congruentes hq (m + 1) _ _ hp
  apply hi
  simp only
  by_contra hne
  have hc0 : c ≠ 0 := by
    rintro rfl
    apply hne
    linarith [hc]
  have h1 : (1 : ℤ) ≤ |c| := Int.one_le_abs hc0
  have hd : |(Tq q)^[t] p - (Tq q)^[t'] p| = 2 ^ (m + 1) * |c| := by
    rw [hc, abs_mul, abs_of_pos (by positivity)]
  have hs : |(Tq q)^[t] p - (Tq q)^[t'] p| ≤ |(Tq q)^[t] p| + |(Tq q)^[t'] p| := by
    rw [sub_eq_add_neg]
    exact (abs_add_le _ _).trans (by rw [abs_neg])
  have hpow : (2 : ℤ) ^ (m + 1) = 2 * 2 ^ m := by ring
  have h2 : (0 : ℤ) < 2 ^ m := by positivity
  nlinarith

/-- Identidad exacta: dos instantes tienen el mismo factor de largo `m` si y sólo si sus
valores son congruentes módulo `2^m`. La complejidad cuenta las clases visitadas. -/
theorem factor_iff {q p : ℤ} (hq : q % 2 = 1) (m t t' : ℕ) :
    factor q p m t = factor q p m t' ↔ (2 : ℤ) ^ m ∣ (Tq q)^[t] p - (Tq q)^[t'] p := by
  constructor
  · intro hf
    apply congruentes hq m
    intro k hk
    have h := congrFun hf ⟨k, hk⟩
    simp only [factor] at h
    rwa [show t + k = k + t by omega, show t' + k = k + t' by omega,
      Function.iterate_add_apply, Function.iterate_add_apply] at h
  · intro hd
    funext k
    have h := mismas_paridades hq m _ _ hd k k.isLt
    simp only [factor]
    rwa [show t + (k : ℕ) = k + t by omega, show t' + (k : ℕ) = k + t' by omega,
      Function.iterate_add_apply, Function.iterate_add_apply]

/-- Bernoulli entero en `ℤ`: `3^L (3+L) <= 3·4^L`. -/
theorem bernoulli (L : ℕ) : (3 : ℤ) ^ L * (3 + L) ≤ 3 * 4 ^ L := by
  have h := PerdicesComplejidad.bernoulli_cuatro_tercios L
  exact_mod_cast h

/-- Umbral explícito: si `L >= 9a`, entonces `3^(L+1) a <= 4^L`. -/
theorem umbral {a : ℤ} {L : ℕ} (hL : 9 * a ≤ L) :
    (3 : ℤ) ^ (L + 1) * a ≤ 2 ^ (L + L) := by
  have hb := bernoulli L
  have h4 : (2 : ℤ) ^ (L + L) = 4 ^ L := by rw [← two_mul, pow_mul]; norm_num
  rw [h4, pow_succ]
  have h3 : (0 : ℤ) < 3 ^ L := by positivity
  nlinarith

/-- Palabra de paridades de `p` bajo `Tq q`. -/
def palabra (q p : ℤ) : ℕ → ℤ := fun t => (Tq q)^[t] p % 2

/-- Una palabra es sturmiana si tiene exactamente `m+1` factores distintos de cada largo `m`. -/
def Sturmiana (w : ℕ → ℤ) : Prop :=
  ∀ m : ℕ, (Set.range (fun t : ℕ => fun k : Fin m => w (t + k))).ncard = m + 1

/-- Una órbita inyectiva tiene, con `m = 9(|p|+q)`, al menos `m+3` factores distintos de
largo `m+1`: su palabra no es sturmiana. -/
theorem inyectiva_no_sturmiana {q p : ℤ} (hq : q % 2 = 1) (hq1 : 1 ≤ q)
    (hi : Function.Injective (fun j => (Tq q)^[j] p)) : ¬ Sturmiana (palabra q p) := by
  intro hS
  have ha0 : 0 ≤ |p| + q := by positivity
  set m : ℕ := 9 * (|p| + q).toNat with hm
  have hLa : 9 * (|p| + q) ≤ ((m + 1 : ℕ) : ℤ) := by
    have := Int.toNat_of_nonneg ha0
    push_cast [hm]
    omega
  have hu : (3 : ℤ) ^ (m + 2) * (|p| + q) ≤ 2 ^ (m + (m + 2)) := by
    have h := umbral hLa
    rw [show m + 1 + 1 = m + 2 by omega, show m + 1 + (m + 1) = m + (m + 2) by omega] at h
    exact h
  have hbajo : ∀ t, t ≤ m + 2 → |(Tq q)^[t] p| + q ≤ 2 ^ m := fun t ht =>
    bajo_umbral hq (by omega) ht hu
  have hcard := hS (m + 1)
  have hfin : (Set.range (fun t : ℕ => fun k : Fin (m + 1) => palabra q p (t + k))).Finite :=
    Set.finite_of_ncard_ne_zero (by rw [hcard]; omega)
  have hFcard : ((Finset.range (m + 3)).image (factor q p (m + 1))).card = m + 3 := by
    rw [Finset.card_image_of_injOn]
    · simp
    · intro t ht t' ht' h
      simp only [Finset.coe_range, Set.mem_Iio] at ht ht'
      exact factores_distintos hq hq1 hi (hbajo t (by omega)) (hbajo t' (by omega)) h
  have hsub : (((Finset.range (m + 3)).image (factor q p (m + 1))) :
      Set (Fin (m + 1) → ℤ)) ⊆
      Set.range (fun t : ℕ => fun k : Fin (m + 1) => palabra q p (t + k)) := by
    intro f hf
    simp only [Finset.coe_image, Set.mem_image, Finset.mem_coe] at hf
    obtain ⟨t, -, rfl⟩ := hf
    exact ⟨t, rfl⟩
  have hle := Set.ncard_le_ncard hsub hfin
  rw [Set.ncard_coe_finset, hFcard, hcard] at hle
  omega

/-- Si la órbita repite un valor, es eventualmente periódica y su palabra no es sturmiana. -/
theorem repetida_no_sturmiana {q p : ℤ}
    (hrep : ¬ Function.Injective (fun j => (Tq q)^[j] p)) : ¬ Sturmiana (palabra q p) := by
  intro hS
  have hex : ∃ i d, 0 < d ∧ (Tq q)^[i + d] p = (Tq q)^[i] p := by
    obtain ⟨a, b, hab, hne⟩ := Function.not_injective_iff.mp hrep
    rcases lt_or_gt_of_ne hne with h | h
    · exact ⟨a, b - a, by omega, by rw [show a + (b - a) = b by omega]; exact hab.symm⟩
    · exact ⟨b, a - b, by omega, by rw [show b + (a - b) = a by omega]; exact hab⟩
  obtain ⟨i, d, hd, hper⟩ := hex
  have hstep : ∀ s, (Tq q)^[i + s + d] p = (Tq q)^[i + s] p := by
    intro s
    rw [show i + s + d = s + (i + d) by omega, Function.iterate_add_apply, hper,
      ← Function.iterate_add_apply, show s + i = i + s by omega]
  have hvuelta : ∀ s r, (Tq q)^[i + s + d * r] p = (Tq q)^[i + s] p := by
    intro s r
    induction r with
    | zero => simp
    | succ r ih =>
      rw [show i + s + d * (r + 1) = i + (s + d * r) + d by ring, hstep,
        show i + (s + d * r) = i + s + d * r by ring, ih]
  have hcard := hS (i + d)
  have hsub : Set.range (fun t : ℕ => fun k : Fin (i + d) => palabra q p (t + k)) ⊆
      (((Finset.range (i + d)).image
        (fun t : ℕ => fun k : Fin (i + d) => palabra q p (t + k))) : Set _) := by
    rintro f ⟨t, rfl⟩
    simp only [Finset.coe_image, Finset.coe_range, Set.mem_image, Set.mem_Iio]
    by_cases ht : t < i + d
    · exact ⟨t, ht, rfl⟩
    · have hmod := Nat.mod_lt (t - i) hd
      have hdiv := Nat.mod_add_div (t - i) d
      refine ⟨i + (t - i) % d, by omega, ?_⟩
      funext k
      simp only [palabra]
      rw [show t + (k : ℕ) = i + ((t - i) % d + k) + d * ((t - i) / d) by omega, hvuelta,
        show i + ((t - i) % d + k) = i + (t - i) % d + k by omega]
  have hle := Set.ncard_le_ncard hsub (Finset.finite_toSet _)
  rw [hcard, Set.ncard_coe_finset] at hle
  have himg := Finset.card_image_le (s := Finset.range (i + d))
    (f := fun t : ℕ => fun k : Fin (i + d) => palabra q p (t + k))
  rw [Finset.card_range] at himg
  omega

/-- **Ningún racional de denominador impar tiene palabra de paridades sturmiana.**
Con `x = p/q`, `q` impar y positivo, la órbita del atajo es `p_t/q` con `p_t = Tq q`-iterados. -/
theorem sin_palabra_sturmiana {q : ℤ} (hq : q % 2 = 1) (hq1 : 1 ≤ q) (p : ℤ) :
    ¬ Sturmiana (palabra q p) := by
  by_cases hi : Function.Injective (fun j => (Tq q)^[j] p)
  · exact inyectiva_no_sturmiana hq hq1 hi
  · exact repetida_no_sturmiana hi

/-- Con `q = 1`, `Tq 1` extiende a los enteros el atajo `T` de los naturales. -/
theorem Tq_uno (n : ℕ) : ((Ocelotas.T n : ℕ) : ℤ) = Tq 1 (n : ℤ) := by
  unfold Ocelotas.T Tq
  split_ifs with h1 h2 h2 <;> omega

theorem iter_uno : ∀ (k n : ℕ), ((Ocelotas.T^[k] n : ℕ) : ℤ) = (Tq 1)^[k] (n : ℤ) := by
  intro k
  induction k with
  | zero => intro n; simp
  | succ k ih =>
    intro n
    rw [Function.iterate_succ_apply, Function.iterate_succ_apply, ih, Tq_uno]

/-- **Ningún natural tiene palabra de paridades sturmiana** bajo el atajo `T`. -/
theorem natural_sin_palabra_sturmiana (n : ℕ) :
    ¬ Sturmiana (fun t => ((Ocelotas.T^[t] n % 2 : ℕ) : ℤ)) := by
  have h : (fun t => ((Ocelotas.T^[t] n % 2 : ℕ) : ℤ)) = palabra 1 (n : ℤ) := by
    funext t
    simp only [palabra]
    rw [← iter_uno]
    push_cast
    rfl
  rw [h]
  exact sin_palabra_sturmiana (by norm_num) le_rfl n

/-! ## El atajo sobre racionales de denominador impar -/

/-- Atajo de Collatz sobre `ℚ`. Con denominador impar, la paridad 2-ádica de `x` es la de
su numerador. -/
def TQ (x : ℚ) : ℚ := if x.num % 2 = 0 then x / 2 else (3 * x + 1) / 2

/-- Con `q` impar, el numerador de `a/q` tiene la paridad de `a`. -/
theorem num_div_impar {a q : ℤ} (hq : q % 2 = 1) :
    ((a : ℚ) / q).num % 2 = a % 2 := by
  have hq0 : (q : ℚ) ≠ 0 := by exact_mod_cast (show q ≠ 0 by omega)
  have hden : ((((a : ℚ) / q).den : ℕ) : ℤ) ∣ q := by
    rw [Rat.intCast_div_eq_divInt]
    exact Rat.den_dvd a q
  have hcross : ((a : ℚ) / q).num * q = a * ((((a : ℚ) / q).den : ℕ) : ℤ) := by
    have h := Rat.num_div_den ((a : ℚ) / q)
    have hd0 : ((((a : ℚ) / q).den : ℕ) : ℚ) ≠ 0 := by exact_mod_cast (Rat.den_pos _).ne'
    rw [div_eq_div_iff hd0 hq0] at h
    exact_mod_cast h
  generalize ((a : ℚ) / q).num = n at hcross ⊢
  generalize ((((a : ℚ) / q).den : ℕ) : ℤ) = d at hden hcross
  obtain ⟨c, hc⟩ := hden
  have hd : d % 2 = 1 := by
    rcases Int.emod_two_eq_zero_or_one d with h | h
    · exfalso
      have : q % 2 = 0 := by rw [hc, Int.mul_emod, h]; simp
      omega
    · exact h
  have h2 := congrArg (· % 2) hcross
  simp only [Int.mul_emod n q, Int.mul_emod a d, hq, hd, mul_one] at h2
  omega

/-- Un paso del atajo sobre `a/q` es un paso de `3x+q` sobre `a`. -/
theorem TQ_div {a q : ℤ} (hq : q % 2 = 1) :
    TQ ((a : ℚ) / q) = (Tq q a : ℚ) / q := by
  have hq0 : (q : ℚ) ≠ 0 := by exact_mod_cast (show q ≠ 0 by omega)
  unfold TQ Tq
  rw [num_div_impar hq]
  rcases Int.emod_two_eq_zero_or_one a with h | h
  · rw [if_pos h, if_pos h]
    obtain ⟨b, rfl⟩ : ∃ b, a = 2 * b := ⟨a / 2, by omega⟩
    rw [show 2 * b / 2 = b by omega]
    push_cast
    field_simp
  · rw [if_neg (by omega), if_neg (by omega)]
    obtain ⟨b, hb⟩ : ∃ b, 3 * a + q = 2 * b := ⟨(3 * a + q) / 2, by omega⟩
    rw [hb, show 2 * b / 2 = b by omega]
    have hb' : (b : ℚ) = (3 * a + q) / 2 := by
      have := congrArg (fun z : ℤ => (z : ℚ)) hb
      push_cast at this
      linarith
    rw [hb']
    field_simp

theorem iter_TQ {q : ℤ} (hq : q % 2 = 1) : ∀ (t : ℕ) (a : ℤ),
    TQ^[t] ((a : ℚ) / q) = ((Tq q)^[t] a : ℚ) / q := by
  intro t
  induction t with
  | zero => intro a; simp
  | succ t ih =>
    intro a
    rw [Function.iterate_succ_apply, Function.iterate_succ_apply, TQ_div hq, ih]

/-- **Ningún racional de denominador impar tiene palabra de paridades sturmiana** bajo el
atajo de Collatz sobre `ℚ`. -/
theorem racional_sin_palabra_sturmiana (x : ℚ) (hx : x.den % 2 = 1) :
    ¬ Sturmiana (fun t => (TQ^[t] x).num % 2) := by
  have hq : ((x.den : ℕ) : ℤ) % 2 = 1 := by omega
  have hq1 : (1 : ℤ) ≤ ((x.den : ℕ) : ℤ) := by exact_mod_cast x.den_pos
  have hx' : x = (x.num : ℚ) / ((((x.den : ℕ) : ℤ)) : ℚ) := by
    rw [Int.cast_natCast]
    exact (Rat.num_div_den x).symm
  have h : (fun t => (TQ^[t] x).num % 2) = palabra ((x.den : ℕ) : ℤ) x.num := by
    funext t
    conv_lhs => rw [hx']
    rw [iter_TQ hq, num_div_impar hq]
    rfl
  rw [h]
  exact sin_palabra_sturmiana hq hq1 x.num

end PerdicesRacional

#print axioms PerdicesRacional.paso_par
#print axioms PerdicesRacional.paso_impar
#print axioms PerdicesRacional.congruentes
#print axioms PerdicesRacional.mismas_paridades
#print axioms PerdicesRacional.paso_tamano
#print axioms PerdicesRacional.cota
#print axioms PerdicesRacional.S_le
#print axioms PerdicesRacional.bajo_umbral
#print axioms PerdicesRacional.factores_distintos
#print axioms PerdicesRacional.factor_iff
#print axioms PerdicesRacional.bernoulli
#print axioms PerdicesRacional.umbral
#print axioms PerdicesRacional.inyectiva_no_sturmiana
#print axioms PerdicesRacional.repetida_no_sturmiana
#print axioms PerdicesRacional.sin_palabra_sturmiana
#print axioms PerdicesRacional.Tq_uno
#print axioms PerdicesRacional.iter_uno
#print axioms PerdicesRacional.natural_sin_palabra_sturmiana
#print axioms PerdicesRacional.num_div_impar
#print axioms PerdicesRacional.TQ_div
#print axioms PerdicesRacional.iter_TQ
#print axioms PerdicesRacional.racional_sin_palabra_sturmiana
