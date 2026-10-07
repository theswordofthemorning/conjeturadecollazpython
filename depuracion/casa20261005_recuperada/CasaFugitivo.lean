import CasaPlano

/-! # El retrato del fugitivo

Ruta B, paso 2 (05-10-2026). Un **fugitivo** es un número sin primer cruce: su pronóstico
`3^S k n / 2^k` nunca baja de 1 (`FugaPura n` en `CasaPlano`). El muro B dice que no hay
fugitivos `n ≥ 2`. Aquí se demuestran, sin hipótesis externas, los rasgos que tendría que
tener uno:

* `fugitivo_no_acotado`: su órbita supera cualquier cota (es una fuga);
* `fugitivo_no_repite`, `fugitivo_no_vuelve`: nunca repite un valor ni vuelve a bajar a
  su punto de partida;
* `fugitivo_no_periodico`: su patrón de subidas y bajadas nunca se vuelve periódico;
* `fugitivo_proporcion`, `fugitivo_63`: en todo prefijo sube en más de 63 de cada 100
  pasos (y, en general, en más de `q/p` si `3^q < 2^p`);
* `fugitivo_tres_mod_cuatro`: es `≡ 3 (mod 4)`;
* `proporcion_sin_cruce`: entre los residuos módulo `2^K`, la proporción cuyo pronóstico
  sigue sin bajar de 1 a los `K` pasos es a lo sumo `ρ^K`, con
  `ρ = (1 + √3) / (2√2) ≈ 0,966`;
* `fugitivos_densidad_cero`: los fugitivos tienen densidad natural 0 (Terras, 1976).

Rasgo auxiliar del radier: `iguales_de_paridades`, dos números con la misma sucesión de
paridades son iguales; `S_congr`, `S k` depende sólo del residuo módulo `2^k`; y
`suma_pesos`, la función generatriz `∑_{r < 2^K} x^(S K r) = (1 + x)^K`.

Compilación: `comprobar_casa.py`, en esta carpeta. -/

namespace CasaFugitivo

open Ocelotas OcelotasContador CasaPlano

/-! ## El cero y los ciclos -/

theorem T_cero : T 0 = 0 := by decide

theorem S_cero (k : ℕ) : S k 0 = 0 := by
  induction k with
  | zero => rfl
  | succ k ih =>
    show 0 % 2 + S k (T 0) = 0
    rw [T_cero, ih]

theorem iter_periodo {m p : ℕ} (hp : T^[p] m = m) (t : ℕ) : T^[t * p] m = m := by
  induction t with
  | zero => simp
  | succ t ih => rw [Nat.succ_mul, iter_add, ih, hp]

theorem S_periodo {m p : ℕ} (hp : T^[p] m = m) (t : ℕ) : S (t * p) m = t * S p m := by
  induction t with
  | zero => simp [S]
  | succ t ih => rw [Nat.succ_mul, S_add, ih, iter_periodo hp, Nat.succ_mul]

/-- En un ciclo, el pronóstico de una vuelta completa está por debajo de 1. -/
theorem ciclo_baja {m p : ℕ} (hp1 : 1 ≤ p) (hp : T^[p] m = m) : 3 ^ S p m < 2 ^ p := by
  rcases Nat.eq_zero_or_pos m with h0 | h0
  · subst h0
    rw [S_cero, pow_zero]
    exact Nat.one_lt_two_pow (by omega)
  · have h := cota_inferior m p
    rw [hp] at h
    exact lt_of_le_of_ne (Nat.le_of_mul_le_mul_right h h0) (tres_ne_dos hp1)

/-- Un factor menor que 1 repetido termina venciendo cualquier ventaja inicial. -/
theorem existe_vuelta {s i a p : ℕ} (h : 3 ^ a < 2 ^ p) :
    ∃ t : ℕ, 3 ^ s * (3 ^ a) ^ t < 2 ^ i * (2 ^ p) ^ t := by
  have hpos : (0 : ℝ) < 2 ^ p := by positivity
  have hq : (3 : ℝ) ^ a / 2 ^ p < 1 := by
    rw [div_lt_one hpos]
    exact_mod_cast h
  obtain ⟨t, ht⟩ := exists_pow_lt_of_lt_one
    (show (0 : ℝ) < 2 ^ i / 3 ^ s by positivity) hq
  refine ⟨t, ?_⟩
  rw [div_pow, div_lt_div_iff₀ (by positivity) (by positivity)] at ht
  have hr : (3 : ℝ) ^ s * (3 ^ a) ^ t < 2 ^ i * (2 ^ p) ^ t := by linarith
  exact_mod_cast hr

/-- Si la órbita de `n` entra en un ciclo, el pronóstico de `n` baja de 1. -/
theorem cruza_de_ciclo {n i p : ℕ} (hp1 : 1 ≤ p) (hp : T^[p] (T^[i] n) = T^[i] n) :
    Cruza n := by
  obtain ⟨t, ht⟩ := existe_vuelta (s := S i n) (i := i) (ciclo_baja hp1 hp)
  refine ⟨i + t * p, ?_⟩
  rw [S_add, S_periodo hp, pow_add, pow_add, pow_mul', pow_mul']
  exact ht

/-- Si la órbita de `n` repite un valor, el pronóstico de `n` baja de 1. -/
theorem cruza_de_repeticion {n i j : ℕ} (hlt : i < j) (heq : T^[i] n = T^[j] n) :
    Cruza n := by
  apply cruza_de_ciclo (i := i) (p := j - i) (by omega)
  rw [← iter_add, Nat.add_sub_cancel' hlt.le, ← heq]

/-! ## Rasgo 1: la órbita del fugitivo no está acotada -/

/-- Un fugitivo nunca repite un valor de su órbita. -/
theorem fugitivo_no_repite {n : ℕ} (h : FugaPura n) {i j : ℕ} (hij : i ≠ j) :
    T^[i] n ≠ T^[j] n := by
  intro heq
  rcases lt_or_gt_of_ne hij with hlt | hlt
  · exact h (cruza_de_repeticion hlt heq)
  · exact h (cruza_de_repeticion hlt heq.symm)

/-- La órbita de un fugitivo supera cualquier cota. -/
theorem fugitivo_no_acotado {n : ℕ} (h : FugaPura n) : Fuga n := by
  classical
  by_contra hf
  simp only [Fuga, not_forall, not_exists, not_lt] at hf
  obtain ⟨M, hM⟩ := hf
  have hmaps : Set.MapsTo (fun k => T^[k] n) (↑(Finset.range (M + 2)) : Set ℕ)
      (↑(Finset.range (M + 1)) : Set ℕ) := by
    intro k _
    simp only [Finset.mem_coe, Finset.mem_range]
    exact Nat.lt_succ_of_le (hM k)
  obtain ⟨i, -, j, -, hij, heq⟩ :=
    Finset.exists_ne_map_eq_of_card_lt_of_maps_to (by simp) hmaps
  exact fugitivo_no_repite h hij heq

/-- Un fugitivo nunca vuelve a su punto de partida: queda estrictamente por encima. -/
theorem fugitivo_no_vuelve {n : ℕ} (h : FugaPura n) {k : ℕ} (hk : 1 ≤ k) :
    n < T^[k] n := by
  have h1 := fuga_pura_no_baja h k
  have h2 := fugitivo_no_repite h (i := 0) (j := k) (by omega)
  rw [Function.iterate_zero_apply] at h2
  omega

/-! ## El patrón de paridades determina el número -/

theorem T_dos (s : ℕ) : T (2 * s) = s := by
  unfold T
  rw [if_pos (by omega)]
  omega

theorem T_dos_uno (s : ℕ) : T (2 * s + 1) = 3 * s + 2 := by
  unfold T
  rw [if_neg (by omega)]
  omega

theorem coprimo_tres (K : ℕ) : Nat.gcd (2 ^ K) 3 = 1 :=
  Nat.Coprime.pow_left K (by decide)

/-- Un paso del atajo baja la congruencia módulo `2^(K+1)` a módulo `2^K`. -/
theorem T_congr {K x y : ℕ} (h : x ≡ y [MOD 2 ^ (K + 1)]) :
    T x ≡ T y [MOD 2 ^ K] ∧ x % 2 = y % 2 := by
  have h2 : x % 2 = y % 2 := Nat.ModEq.of_dvd (dvd_pow_self 2 (Nat.succ_ne_zero K)) h
  refine ⟨?_, h2⟩
  have h22 : (2 : ℕ) ^ (K + 1) = 2 * 2 ^ K := by ring
  rw [h22] at h
  apply Nat.ModEq.mul_left_cancel' (c := 2) (by norm_num)
  rcases Nat.mod_two_eq_zero_or_one x with hx | hx
  · have hy : y % 2 = 0 := by omega
    rw [T_par hx, T_par hy]
    exact h
  · have hy : y % 2 = 1 := by omega
    rw [T_impar hx, T_impar hy]
    exact (h.mul_left 3).add_right 1

/-- `S k` depende sólo del residuo módulo `2^k`. -/
theorem S_congr : ∀ K x y, x ≡ y [MOD 2 ^ K] → S K x = S K y
  | 0, _, _, _ => rfl
  | K + 1, x, y, h => by
    obtain ⟨h1, h2⟩ := T_congr h
    show x % 2 + S K (T x) = y % 2 + S K (T y)
    rw [h2, S_congr K _ _ h1]

/-- Dos números con las mismas `K` primeras paridades son congruentes módulo `2^K`. -/
theorem congr_de_paridades : ∀ K x y, (∀ j, j < K → T^[j] x % 2 = T^[j] y % 2) →
    x ≡ y [MOD 2 ^ K]
  | 0, x, y, _ => by simp [Nat.ModEq, Nat.mod_one]
  | K + 1, x, y, h => by
    have h0 : x % 2 = y % 2 := h 0 (by omega)
    have hT : T x ≡ T y [MOD 2 ^ K] := congr_de_paridades K (T x) (T y) fun j hj => by
      have := h (j + 1) (by omega)
      rwa [Function.iterate_succ_apply, Function.iterate_succ_apply] at this
    have h2 : 2 * T x ≡ 2 * T y [MOD 2 ^ (K + 1)] := by
      have := Nat.ModEq.mul_left' 2 hT
      rwa [show 2 * 2 ^ K = 2 ^ (K + 1) by ring] at this
    rcases Nat.mod_two_eq_zero_or_one x with hx | hx
    · have hy : y % 2 = 0 := by omega
      rwa [T_par hx, T_par hy] at h2
    · have hy : y % 2 = 1 := by omega
      rw [T_impar hx, T_impar hy] at h2
      exact Nat.ModEq.cancel_left_of_coprime (coprimo_tres (K + 1))
        (Nat.ModEq.add_right_cancel' 1 h2)

/-- Dos números con la misma sucesión completa de paridades son iguales. -/
theorem iguales_de_paridades {x y : ℕ} (h : ∀ j, T^[j] x % 2 = T^[j] y % 2) : x = y := by
  have hc := congr_de_paridades (x + y + 1) x y (fun j _ => h j)
  have hx : x < 2 ^ (x + y + 1) :=
    lt_of_lt_of_le Nat.lt_two_pow_self (Nat.pow_le_pow_right (by norm_num) (by omega))
  have hy : y < 2 ^ (x + y + 1) :=
    lt_of_lt_of_le Nat.lt_two_pow_self (Nat.pow_le_pow_right (by norm_num) (by omega))
  unfold Nat.ModEq at hc
  rwa [Nat.mod_eq_of_lt hx, Nat.mod_eq_of_lt hy] at hc

/-! ## Rasgo 2: el patrón del fugitivo nunca se vuelve periódico -/

/-- El patrón de subidas y bajadas de `n` es periódico, con periodo `p`, desde el paso `i`. -/
def PatronPeriodico (n : ℕ) : Prop :=
  ∃ i p, 1 ≤ p ∧ ∀ j, i ≤ j → T^[j + p] n % 2 = T^[j] n % 2

/-- Un patrón que termina siendo periódico obliga a la órbita a entrar en un ciclo. -/
theorem ciclo_de_patron {n i p : ℕ}
    (hper : ∀ j, i ≤ j → T^[j + p] n % 2 = T^[j] n % 2) : T^[i] n = T^[i + p] n := by
  apply iguales_de_paridades
  intro j
  rw [← iter_add, ← iter_add, show i + p + j = i + j + p by omega]
  exact (hper (i + j) (by omega)).symm

theorem fugitivo_no_periodico {n : ℕ} (h : FugaPura n) : ¬ PatronPeriodico n := by
  rintro ⟨i, p, hp1, hper⟩
  exact fugitivo_no_repite h (by omega : i ≠ i + p) (ciclo_de_patron hper)

/-! ## Rasgo 3: el fugitivo sube en más de 63 de cada 100 pasos -/

theorem fugitivo_sube {n : ℕ} (h : FugaPura n) (k : ℕ) : 2 ^ k ≤ 3 ^ S k n :=
  not_lt.mp fun hc => h ⟨k, hc⟩

/-- Si `3^q ≤ 2^p`, en todo prefijo de longitud `k` el fugitivo sube al menos `q k / p`
    veces. -/
theorem fugitivo_proporcion {n : ℕ} (h : FugaPura n) {q p : ℕ} (hqp : 3 ^ q ≤ 2 ^ p)
    (k : ℕ) : q * k ≤ p * S k n := by
  have h1 : 3 ^ (q * k) ≤ 3 ^ (p * S k n) :=
    calc 3 ^ (q * k) = (3 ^ q) ^ k := pow_mul 3 q k
      _ ≤ (2 ^ p) ^ k := Nat.pow_le_pow_left hqp k
      _ = (2 ^ k) ^ p := by rw [← pow_mul, ← pow_mul, mul_comm]
      _ ≤ (3 ^ S k n) ^ p := Nat.pow_le_pow_left (fugitivo_sube h k) p
      _ = 3 ^ (p * S k n) := by rw [← pow_mul, mul_comm]
  exact (Nat.pow_le_pow_iff_right (by norm_num)).1 h1

/-- Versión estricta: si `3^q < 2^p` y `k ≥ 1`, sube más de `q k / p` veces. -/
theorem fugitivo_proporcion_estricta {n : ℕ} (h : FugaPura n) {q p : ℕ}
    (hqp : 3 ^ q < 2 ^ p) {k : ℕ} (hk : 1 ≤ k) : q * k < p * S k n := by
  have h1 : 3 ^ (q * k) < 3 ^ (p * S k n) :=
    calc 3 ^ (q * k) = (3 ^ q) ^ k := pow_mul 3 q k
      _ < (2 ^ p) ^ k := Nat.pow_lt_pow_left hqp (by omega)
      _ = (2 ^ k) ^ p := by rw [← pow_mul, ← pow_mul, mul_comm]
      _ ≤ (3 ^ S k n) ^ p := Nat.pow_le_pow_left (fugitivo_sube h k) p
      _ = 3 ^ (p * S k n) := by rw [← pow_mul, mul_comm]
  exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 h1

/-- En todo prefijo de `k ≥ 1` pasos, el fugitivo sube en más de 63 de cada 100. -/
theorem fugitivo_63 {n : ℕ} (h : FugaPura n) {k : ℕ} (hk : 1 ≤ k) : 63 * k < 100 * S k n :=
  fugitivo_proporcion_estricta h (by norm_num) hk

/-- Un fugitivo es `≡ 3 (mod 4)`: sus dos primeros pasos son subidas. -/
theorem fugitivo_tres_mod_cuatro {n : ℕ} (h : FugaPura n) : n % 4 = 3 := by
  have h2 := fugitivo_sube h 2
  have hS : S 2 n = n % 2 + T n % 2 := by
    show n % 2 + (T n % 2 + S 0 (T (T n))) = n % 2 + T n % 2
    rfl
  have hS2 : S 2 n = 2 := by
    by_contra hne
    have hle : S 2 n ≤ 1 := by omega
    have := Nat.pow_le_pow_right (by norm_num : 0 < 3) hle
    omega
  unfold T at hS
  split_ifs at hS <;> omega

/-! ## Rasgo 4: casi ningún número es fugitivo (Terras) -/

theorem suma_pares_impares (f : ℕ → ℝ) (N : ℕ) :
    ∑ r ∈ Finset.range (2 * N), f r =
      ∑ s ∈ Finset.range N, f (2 * s) + ∑ s ∈ Finset.range N, f (2 * s + 1) := by
  induction N with
  | zero => simp
  | succ N ih =>
    rw [show 2 * (N + 1) = 2 * N + 1 + 1 by ring, Finset.sum_range_succ,
      Finset.sum_range_succ, ih, Finset.sum_range_succ, Finset.sum_range_succ]
    ring

/-- `s ↦ 3 s + 2` permuta los residuos módulo `2^K`. -/
theorem suma_permutada (K : ℕ) (g : ℕ → ℝ) (hg : ∀ a b, a ≡ b [MOD 2 ^ K] → g a = g b) :
    ∑ s ∈ Finset.range (2 ^ K), g (3 * s + 2) = ∑ s ∈ Finset.range (2 ^ K), g s := by
  have hN : 0 < 2 ^ K := by positivity
  have hinj : Set.InjOn (fun s => (3 * s + 2) % 2 ^ K) ↑(Finset.range (2 ^ K)) := by
    intro a ha b hb hab
    simp only [Finset.coe_range, Set.mem_Iio] at ha hb
    have h1 : 3 * a + 2 ≡ 3 * b + 2 [MOD 2 ^ K] := hab
    have h3 : a ≡ b [MOD 2 ^ K] :=
      Nat.ModEq.cancel_left_of_coprime (coprimo_tres K) (Nat.ModEq.add_right_cancel' 2 h1)
    unfold Nat.ModEq at h3
    rwa [Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hb] at h3
  have himg : (Finset.range (2 ^ K)).image (fun s => (3 * s + 2) % 2 ^ K) =
      Finset.range (2 ^ K) := by
    apply Finset.eq_of_subset_of_card_le
    · intro y hy
      simp only [Finset.mem_image] at hy
      obtain ⟨s, -, rfl⟩ := hy
      exact Finset.mem_range.2 (Nat.mod_lt _ hN)
    · rw [Finset.card_image_of_injOn hinj]
  calc ∑ s ∈ Finset.range (2 ^ K), g (3 * s + 2)
      = ∑ s ∈ Finset.range (2 ^ K), g ((3 * s + 2) % 2 ^ K) :=
        Finset.sum_congr rfl fun s _ => hg _ _ (Nat.mod_modEq _ _).symm
    _ = ∑ y ∈ (Finset.range (2 ^ K)).image (fun s => (3 * s + 2) % 2 ^ K), g y :=
        (Finset.sum_image hinj).symm
    _ = _ := by rw [himg]

/-- Función generatriz de las subidas: `∑_{r < 2^K} x^(S K r) = (1 + x)^K`. -/
theorem suma_pesos (x : ℝ) (K : ℕ) :
    ∑ r ∈ Finset.range (2 ^ K), x ^ S K r = (1 + x) ^ K := by
  induction K with
  | zero => simp [S]
  | succ K ih =>
    have hpar : ∀ s, S (K + 1) (2 * s) = S K s := by
      intro s
      show (2 * s) % 2 + S K (T (2 * s)) = S K s
      rw [T_dos]
      omega
    have himp : ∀ s, S (K + 1) (2 * s + 1) = 1 + S K (3 * s + 2) := by
      intro s
      show (2 * s + 1) % 2 + S K (T (2 * s + 1)) = 1 + S K (3 * s + 2)
      rw [T_dos_uno]
      omega
    rw [pow_succ', suma_pares_impares]
    simp only [hpar, himp, pow_add, pow_one]
    rw [← Finset.mul_sum, suma_permutada K (fun r => x ^ S K r)
      (fun a b hab => by rw [S_congr K a b hab]), ih]
    ring

/-- Residuos módulo `2^K` cuyo pronóstico a los `K` pasos sigue sin bajar de 1. -/
def sinCruce (K : ℕ) : Finset ℕ :=
  (Finset.range (2 ^ K)).filter fun r => 2 ^ K ≤ 3 ^ S K r

theorem raiz_pow {a : ℝ} (ha : 0 ≤ a) (k : ℕ) : (Real.sqrt a ^ k) ^ 2 = a ^ k := by
  rw [← pow_mul, mul_comm, pow_mul, Real.sq_sqrt ha]

/-- Cota tipo Chernoff: hay a lo sumo `((1 + √3)/√2)^K` residuos sin cruce a los `K`
    pasos, de `2^K`. -/
theorem cota_sinCruce (K : ℕ) :
    ((sinCruce K).card : ℝ) ≤ ((1 + Real.sqrt 3) / Real.sqrt 2) ^ K := by
  have h2 : (0 : ℝ) < Real.sqrt 2 ^ K := by positivity
  have hpeso : ∀ r ∈ sinCruce K, (1 : ℝ) ≤ Real.sqrt 3 ^ S K r / Real.sqrt 2 ^ K := by
    intro r hr
    have hr' : 2 ^ K ≤ 3 ^ S K r := (Finset.mem_filter.1 hr).2
    rw [one_le_div h2]
    have hc : (Real.sqrt 2 ^ K) ^ 2 ≤ (Real.sqrt 3 ^ S K r) ^ 2 := by
      rw [raiz_pow (by norm_num), raiz_pow (by norm_num)]
      exact_mod_cast hr'
    exact (pow_le_pow_iff_left₀ (by positivity) (by positivity) two_ne_zero).1 hc
  calc ((sinCruce K).card : ℝ) = (sinCruce K).card • (1 : ℝ) := by simp
    _ ≤ ∑ r ∈ sinCruce K, Real.sqrt 3 ^ S K r / Real.sqrt 2 ^ K :=
        Finset.card_nsmul_le_sum _ _ _ hpeso
    _ ≤ ∑ r ∈ Finset.range (2 ^ K), Real.sqrt 3 ^ S K r / Real.sqrt 2 ^ K :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
          fun _ _ _ => by positivity
    _ = (1 + Real.sqrt 3) ^ K / Real.sqrt 2 ^ K := by
        simp_rw [div_eq_mul_inv]
        rw [← Finset.sum_mul, suma_pesos]
    _ = _ := (div_pow _ _ _).symm

/-- La razón de la cota: `ρ = (1 + √3)/(2√2) < 1`. -/
theorem razon_menor : (1 + Real.sqrt 3) / Real.sqrt 2 / 2 < 1 := by
  have h3 := Real.sq_sqrt (show (0 : ℝ) ≤ 3 by norm_num)
  have h2 := Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)
  have h3p := Real.sqrt_nonneg 3
  have h2p := Real.sqrt_nonneg 2
  have hs3 : Real.sqrt 3 < 7 / 4 := by nlinarith
  have hs2 : 7 / 5 < Real.sqrt 2 := by nlinarith
  rw [div_div, div_lt_one (by positivity)]
  linarith

/-- Proporción de residuos sin cruce a los `K` pasos: a lo sumo `ρ^K`, con `ρ ≈ 0,966`. -/
theorem proporcion_sin_cruce (K : ℕ) :
    ((sinCruce K).card : ℝ) / 2 ^ K ≤ ((1 + Real.sqrt 3) / Real.sqrt 2 / 2) ^ K := by
  rw [div_pow, div_le_div_iff_of_pos_right (by positivity)]
  exact cota_sinCruce K

open Classical in
/-- Fugitivos menores que `N`. -/
noncomputable def fugitivos (N : ℕ) : Finset ℕ := (Finset.range N).filter FugaPura

/-- Contar con los residuos sin cruce: `#{n < N : 2^K ≤ 3^S_K(n)} ≤ (N / 2^K + 1) · c_K`. -/
theorem filtro_por_residuos (N K : ℕ) :
    ((Finset.range N).filter fun n => 2 ^ K ≤ 3 ^ S K n).card ≤
      (N / 2 ^ K + 1) * (sinCruce K).card := by
  rw [← Finset.card_range (N / 2 ^ K + 1), ← Finset.card_product]
  apply Finset.card_le_card_of_injOn (fun n => (n / 2 ^ K, n % 2 ^ K))
  · intro n hn
    have hn' : n < N ∧ 2 ^ K ≤ 3 ^ S K n := by simpa using hn
    simp only [Finset.coe_product, Set.mem_prod, Finset.mem_coe, Finset.mem_range,
      sinCruce, Finset.mem_filter]
    refine ⟨Nat.lt_succ_of_le (Nat.div_le_div_right hn'.1.le), Nat.mod_lt _ (by positivity),
      ?_⟩
    rw [S_congr K _ n (Nat.mod_modEq _ _)]
    exact hn'.2
  · intro a _ b _ hab
    simp only [Prod.mk.injEq] at hab
    rw [← Nat.div_add_mod a (2 ^ K), ← Nat.div_add_mod b (2 ^ K), hab.1, hab.2]

/-- Contar fugitivos con los residuos sin cruce: `#(fugitivos N) ≤ (N / 2^K + 1) · c_K`. -/
theorem fugitivos_por_residuos (N K : ℕ) :
    (fugitivos N).card ≤ (N / 2 ^ K + 1) * (sinCruce K).card := by
  classical
  refine le_trans (Finset.card_le_card ?_) (filtro_por_residuos N K)
  intro n hn
  have hn' : n < N ∧ FugaPura n := by simpa [fugitivos] using hn
  exact Finset.mem_filter.2 ⟨Finset.mem_range.2 hn'.1, fugitivo_sube hn'.2 K⟩

/-- Para `N ≥ 2^K`: `(N / 2^K + 1) · c_K ≤ 2 ρ^K N`. -/
theorem cota_bloques {N K : ℕ} (hN : 2 ^ K ≤ N) :
    (((N / 2 ^ K : ℕ) : ℝ) + 1) * (sinCruce K).card ≤
      2 * ((1 + Real.sqrt 3) / Real.sqrt 2 / 2) ^ K * N := by
  have hK : (0 : ℝ) < 2 ^ K := by positivity
  have hNr : (2 : ℝ) ^ K ≤ N := by exact_mod_cast hN
  have hc := cota_sinCruce K
  have hcnn : (0 : ℝ) ≤ (sinCruce K).card := by positivity
  have hdiv : ((N / 2 ^ K : ℕ) : ℝ) ≤ N / 2 ^ K := by
    have h' : ((N / 2 ^ K : ℕ) : ℝ) * 2 ^ K ≤ N := by
      exact_mod_cast Nat.div_mul_le_self N (2 ^ K)
    exact (le_div_iff₀ hK).2 h'
  have huno : (1 : ℝ) ≤ N / 2 ^ K := by rw [le_div_iff₀ hK]; linarith
  have hfac : ((N / 2 ^ K : ℕ) : ℝ) + 1 ≤ 2 * (N / 2 ^ K) := by linarith
  rw [div_pow ((1 + Real.sqrt 3) / Real.sqrt 2) (2 : ℝ) K, mul_comm (2 : ℝ), mul_assoc]
  calc (((N / 2 ^ K : ℕ) : ℝ) + 1) * (sinCruce K).card
      ≤ (2 * (N / 2 ^ K)) * ((1 + Real.sqrt 3) / Real.sqrt 2) ^ K :=
        mul_le_mul hfac hc hcnn (by positivity)
    _ = ((1 + Real.sqrt 3) / Real.sqrt 2) ^ K / 2 ^ K * (2 * N) := by
        field_simp

/-- Para `N ≥ 2^K`, la proporción de fugitivos menores que `N` es a lo sumo `2 ρ^K`. -/
theorem proporcion_fugitivos {N K : ℕ} (hN : 2 ^ K ≤ N) :
    ((fugitivos N).card : ℝ) / N ≤ 2 * ((1 + Real.sqrt 3) / Real.sqrt 2 / 2) ^ K := by
  have hK : (0 : ℝ) < 2 ^ K := by positivity
  have hNpos : (0 : ℝ) < N := lt_of_lt_of_le hK (by exact_mod_cast hN)
  have hcont : ((fugitivos N).card : ℝ) ≤ (((N / 2 ^ K : ℕ) : ℝ) + 1) * (sinCruce K).card := by
    exact_mod_cast fugitivos_por_residuos N K
  rw [div_le_iff₀ hNpos]
  exact hcont.trans (cota_bloques hN)

/-- **Terras (1976)**, en la forma del primer cruce: los fugitivos tienen densidad
    natural 0. -/
theorem fugitivos_densidad_cero :
    Filter.Tendsto (fun N : ℕ => ((fugitivos N).card : ℝ) / N) Filter.atTop (nhds 0) := by
  set ρ := (1 + Real.sqrt 3) / Real.sqrt 2 / 2
  have hρ0 : 0 ≤ ρ := by positivity
  have hρ1 : ρ < 1 := razon_menor
  rw [tendsto_order]
  refine ⟨fun a ha => Filter.Eventually.of_forall fun N => ?_, fun a ha => ?_⟩
  · exact lt_of_lt_of_le ha (by positivity)
  · obtain ⟨K, hK⟩ := exists_pow_lt_of_lt_one (show 0 < a / 2 by linarith) hρ1
    rw [Filter.eventually_atTop]
    refine ⟨2 ^ K, fun N hN => ?_⟩
    have := proporcion_fugitivos hN
    linarith

/-! ## El retrato completo -/

/-- **El retrato del fugitivo.** Un número sin primer cruce tiene órbita no acotada que
    nunca repite valores, patrón de paridades nunca periódico, más de 63 subidas de cada
    100 pasos en todo prefijo, y es `≡ 3 (mod 4)`; además, los fugitivos tienen densidad
    natural 0. -/
theorem retrato_del_fugitivo {n : ℕ} (h : FugaPura n) :
    Fuga n ∧ (∀ i j, i ≠ j → T^[i] n ≠ T^[j] n) ∧ ¬ PatronPeriodico n ∧
      (∀ k, 1 ≤ k → 63 * k < 100 * S k n) ∧ n % 4 = 3 ∧
      Filter.Tendsto (fun N : ℕ => ((fugitivos N).card : ℝ) / N) Filter.atTop (nhds 0) :=
  ⟨fugitivo_no_acotado h, fun _ _ hij => fugitivo_no_repite h hij,
    fugitivo_no_periodico h, fun _ hk => fugitivo_63 h hk, fugitivo_tres_mod_cuatro h,
    fugitivos_densidad_cero⟩

end CasaFugitivo

#print axioms CasaFugitivo.cruza_de_ciclo
#print axioms CasaFugitivo.fugitivo_no_acotado
#print axioms CasaFugitivo.fugitivo_no_vuelve
#print axioms CasaFugitivo.S_congr
#print axioms CasaFugitivo.iguales_de_paridades
#print axioms CasaFugitivo.fugitivo_no_periodico
#print axioms CasaFugitivo.fugitivo_proporcion
#print axioms CasaFugitivo.fugitivo_63
#print axioms CasaFugitivo.fugitivo_tres_mod_cuatro
#print axioms CasaFugitivo.suma_pesos
#print axioms CasaFugitivo.cota_sinCruce
#print axioms CasaFugitivo.proporcion_sin_cruce
#print axioms CasaFugitivo.filtro_por_residuos
#print axioms CasaFugitivo.proporcion_fugitivos
#print axioms CasaFugitivo.fugitivos_densidad_cero
#print axioms CasaFugitivo.retrato_del_fugitivo
