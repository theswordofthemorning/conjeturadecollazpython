import CasaPotencia
import CasaDomino

/-! # Bajo la forma entera de LMN, una falla de CST cruza tarde

Ruta B, 05-10-2026. Hipótesis explícita `LMNEntera`: la forma entera del corolario de
Laurent–Mignotte–Nesterenko (1995) que `OcelotasLMN.cola_lmn_entera` deduce de `LMNDebil`,
con el mismo enunciado (en `depuracion/cst20260930`; ese enlace usa logaritmos reales y no
se compila en esta instalación). Es un argumento del teorema, no un axioma.

* `cruce_justo`: en el primer cruce `k ≥ 2`, `2^k ≤ 2 · 3^(S_k(n))`;
* `falla_acotada`: si `n ≥ 2` falla en CST con primer cruce `k`, entonces
  `n 2^(k−1) < 3^k 2^(19(t+33)²)` para todo `t` con `k < 2^(t+1)`;
* `falla_tardia`: si además `n ≥ 2^125000`, entonces `2n < 2^k`: el primer cruce llega
  después de `log₂ n + 1` pasos;
* `fallasCST_lmn_potencia` y `noDescienden_lmn_potencia`: por encima de `2^125000`, las
  fallas de CST y los que nunca bajan son, bajo N, menos de `3 (2N)^0,95` y `4 (2N)^0,95`.

Así, bajo LMN, el exponente de los candidatos a menor contraejemplo baja de `31/32` al
`0,95` de los fugitivos. La cota `2^125000` es holgada.

Compilación: `comprobar_fugitivo.py`, en esta carpeta. -/

namespace CasaLMN

open Ocelotas OcelotasContador CasaPlano CasaFugitivo CasaCasiTodos CasaDomino CasaPotencia

/-- Forma entera del corolario de Laurent–Mignotte–Nesterenko, con el enunciado de
    `OcelotasLMN.cola_lmn_entera`. -/
def LMNEntera : Prop :=
  ∀ k q t : ℕ, 2 ≤ k → 2 ^ k ≤ 2 * 3 ^ q → 3 ^ q < 2 ^ k → k < 2 ^ (t + 1) →
    3 ^ q ≤ (2 ^ k - 3 ^ q) * 2 ^ (19 * (t + 33) ^ 2)

theorem dos_pred {k : ℕ} (hk : 1 ≤ k) : 2 ^ k = 2 * 2 ^ (k - 1) := by
  rw [← pow_succ']
  congr 1
  omega

/-- En el primer cruce `k ≥ 2`, el último paso es par: `2^k ≤ 2 · 3^(S_k(n))`. -/
theorem cruce_justo {n k : ℕ} (hk : PrimerCruce n k) (hk2 : 2 ≤ k) :
    2 ^ k ≤ 2 * 3 ^ S k n := by
  obtain ⟨hpre, hc⟩ := hk
  have h1 := hpre (k - 1) (by omega) (by omega)
  have hS : S k n = S (k - 1) n + T^[k - 1] n % 2 := by
    have h := S_add (k - 1) 1 n
    rw [show k - 1 + 1 = k by omega] at h
    rw [h]
    simp [S]
  have he := dos_pred (show 1 ≤ k by omega)
  rcases Nat.mod_two_eq_zero_or_one (T^[k - 1] n) with h | h
  · rw [hS, h, add_zero]
    omega
  · exfalso
    rw [hS, h, pow_succ] at hc
    omega

/-- Una falla de CST con `n ≥ 2` tiene primer cruce `k ≥ 2`. -/
theorem falla_dos {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hge : n ≤ T^[k] n) :
    2 ≤ k := by
  obtain ⟨-, hc⟩ := hk
  by_contra hlt
  have hk' : k = 0 ∨ k = 1 := by omega
  rcases hk' with rfl | rfl
  · simp [S] at hc
  · have hS : S 1 n = n % 2 := by simp [S]
    rw [hS] at hc
    have hpar : n % 2 = 0 := by
      rcases Nat.mod_two_eq_zero_or_one n with h0 | h1
      · exact h0
      · rw [h1] at hc
        norm_num at hc
    have he := T_par hpar
    have hT : T^[1] n = T n := rfl
    rw [hT] at hge
    omega

/-- **Una falla de CST está acotada por su primer cruce.** -/
theorem falla_acotada (hL : LMNEntera) {n k t : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k)
    (hge : n ≤ T^[k] n) (ht : k < 2 ^ (t + 1)) :
    n * 2 ^ (k - 1) < 3 ^ k * 2 ^ (19 * (t + 33) ^ 2) := by
  have hk2 := falla_dos hn hk hge
  have hc := hk.2
  have hjusto := cruce_justo hk hk2
  have hlmn := hL k (S k n) t hk2 hjusto hc ht
  have hg := grieta_desigualdad hc hge
  have he := dos_pred (show 1 ≤ k by omega)
  have h2 : 2 ^ (k - 1) ≤ 3 ^ S k n := by omega
  have hP : 0 < 2 ^ (19 * (t + 33) ^ 2) := by positivity
  have h2k : 0 < 2 ^ k := by positivity
  generalize 2 ^ (19 * (t + 33) ^ 2) = P at hlmn hP ⊢
  generalize 2 ^ k - 3 ^ S k n = D at hlmn hg
  have hnD : n * D < 3 ^ k := by
    rw [Nat.mul_comm]
    omega
  calc n * 2 ^ (k - 1) ≤ n * (D * P) := Nat.mul_le_mul_left n (le_trans h2 hlmn)
    _ = n * D * P := by ring
    _ < 3 ^ k * P := Nat.mul_lt_mul_of_pos_right hnD hP

/-! ## Desigualdades numéricas -/

theorem tres_cuatro_base : 3 ^ (2 ^ 17) * 2 ^ (19 * (17 + 33) ^ 2 + 2) < 4 ^ (2 ^ 17) := by
  decide +kernel

/-- Para `t ≥ 17`: `3^(2^t) · 2^(19(t+33)² + 2) < 4^(2^t)`. -/
theorem tres_cuatro {t : ℕ} (ht : 17 ≤ t) :
    3 ^ (2 ^ t) * 2 ^ (19 * (t + 33) ^ 2 + 2) < 4 ^ (2 ^ t) := by
  induction t, ht using Nat.le_induction with
  | base => exact tres_cuatro_base
  | succ t ht ih =>
    have hE : 19 * (t + 1 + 33) ^ 2 + 2 ≤ 2 * (19 * (t + 33) ^ 2 + 2) := by
      nlinarith [Nat.zero_le (t * t), Nat.zero_le t]
    have e3 : 3 ^ (2 ^ (t + 1)) = 3 ^ (2 ^ t) * 3 ^ (2 ^ t) := by rw [pow_succ, pow_mul, sq]
    have e4 : 4 ^ (2 ^ (t + 1)) = 4 ^ (2 ^ t) * 4 ^ (2 ^ t) := by rw [pow_succ, pow_mul, sq]
    have e2 : 2 ^ (2 * (19 * (t + 33) ^ 2 + 2)) =
        2 ^ (19 * (t + 33) ^ 2 + 2) * 2 ^ (19 * (t + 33) ^ 2 + 2) := by rw [two_mul, pow_add]
    have hx : 0 < 3 ^ (2 ^ t) * 2 ^ (19 * (t + 33) ^ 2 + 2) := by positivity
    have hy : 0 < 4 ^ (2 ^ t) := by positivity
    have h1 : 3 ^ (2 ^ (t + 1)) * 2 ^ (19 * (t + 1 + 33) ^ 2 + 2) ≤
        3 ^ (2 ^ (t + 1)) * 2 ^ (2 * (19 * (t + 33) ^ 2 + 2)) :=
      Nat.mul_le_mul_left _ (Nat.pow_le_pow_right (by norm_num) hE)
    rw [e3, e2] at h1
    rw [e3, e4]
    generalize 3 ^ (2 ^ t) = A at h1 ih hx ⊢
    generalize 2 ^ (19 * (t + 33) ^ 2 + 2) = B at h1 ih hx
    generalize 2 ^ (19 * (t + 1 + 33) ^ 2 + 2) = D at h1 ⊢
    generalize 4 ^ (2 ^ t) = C at ih hy ⊢
    calc A * A * D ≤ A * A * (B * B) := h1
      _ = (A * B) * (A * B) := by ring
      _ < C * (A * B) := Nat.mul_lt_mul_of_pos_right ih hx
      _ < C * C := Nat.mul_lt_mul_of_pos_left ih hy

/-- Para `2^t ≤ k` con `t ≥ 17`: `3^k · 2^(19(t+33)² + 2) < 4^k`. -/
theorem tres_cuatro_k {k t : ℕ} (ht : 17 ≤ t) (hk : 2 ^ t ≤ k) :
    3 ^ k * 2 ^ (19 * (t + 33) ^ 2 + 2) < 4 ^ k := by
  have h := tres_cuatro ht
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hk
  rw [pow_add 3 (2 ^ t) d, pow_add 4 (2 ^ t) d]
  generalize 2 ^ (19 * (t + 33) ^ 2 + 2) = B at h ⊢
  calc 3 ^ 2 ^ t * 3 ^ d * B = (3 ^ 2 ^ t * B) * 3 ^ d := by ring
    _ < 4 ^ 2 ^ t * 3 ^ d := Nat.mul_lt_mul_of_pos_right h (by positivity)
    _ ≤ 4 ^ 2 ^ t * 4 ^ d := Nat.mul_le_mul_left _ (Nat.pow_le_pow_left (by norm_num) d)

theorem tres_dos_base : 3 ^ (2 ^ 17) ≤ 2 ^ (79380 + 2 ^ 17) := by
  decide +kernel

/-- Para `k ≤ 2^17`: `3^k ≤ 2^(79380 + k)`. -/
theorem tres_dos_k {k : ℕ} (hk : k ≤ 2 ^ 17) : 3 ^ k ≤ 2 ^ (79380 + k) := by
  obtain ⟨d, hd⟩ := Nat.exists_eq_add_of_le hk
  have h : 3 ^ k * 3 ^ d ≤ 2 ^ (79380 + k) * 2 ^ d := by
    have h0 := tres_dos_base
    rw [hd] at h0
    rw [← pow_add, ← pow_add, show 79380 + k + d = 79380 + (k + d) by ring]
    exact h0
  have h23 : 2 ^ d ≤ 3 ^ d := Nat.pow_le_pow_left (by norm_num) d
  have hpos : 0 < 2 ^ d := by positivity
  have : 3 ^ k * 2 ^ d ≤ 2 ^ (79380 + k) * 2 ^ d :=
    le_trans (Nat.mul_le_mul_left _ h23) h
  exact Nat.le_of_mul_le_mul_right this hpos

/-! ## El primer cruce de una falla llega tarde -/

/-- **Una falla de CST cruza tarde.** Bajo `LMNEntera`, si `n ≥ 2^125000` falla en CST con
    primer cruce `k`, entonces `2n < 2^k`. -/
theorem falla_tardia (hL : LMNEntera) {n k : ℕ} (hn : 2 ^ 125000 ≤ n) (hk : PrimerCruce n k)
    (hge : n ≤ T^[k] n) : 2 * n < 2 ^ k := by
  have hn2 : 2 ≤ n := le_trans (Nat.one_lt_two_pow (by norm_num)) hn
  have hk2 := falla_dos hn2 hk hge
  set t := Nat.log 2 k with htdef
  have ht1 : k < 2 ^ (t + 1) := Nat.lt_pow_succ_log_self (by norm_num) k
  have ht0 : 2 ^ t ≤ k := Nat.pow_log_le_self 2 (by omega)
  have hacot := falla_acotada hL hn2 hk hge ht1
  by_contra hcon
  have hnk : 2 ^ (k - 1) ≤ n := by
    have := dos_pred (show 1 ≤ k by omega)
    omega
  by_cases ht17 : 17 ≤ t
  · -- primer cruce muy largo: 4^k < 3^k 2^(E+2) contradice `tres_cuatro_k`
    have h4 := tres_cuatro_k ht17 ht0
    have hsq : 2 ^ (k - 1) * 2 ^ (k - 1) ≤ n * 2 ^ (k - 1) := Nat.mul_le_mul_right _ hnk
    have h4k : 4 ^ k = 4 * (2 ^ (k - 1) * 2 ^ (k - 1)) := by
      rw [← pow_add, show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul, ← pow_add]
      congr 1
      omega
    have hE : 3 ^ k * 2 ^ (19 * (t + 33) ^ 2 + 2) = 4 * (3 ^ k * 2 ^ (19 * (t + 33) ^ 2)) := by
      rw [pow_add]
      generalize 2 ^ (19 * (t + 33) ^ 2) = P
      ring
    omega
  · -- primer cruce corto: n sería menor que 2^125000
    have ht16 : t ≤ 16 := by omega
    have hk17 : k ≤ 2 ^ 17 := by
      have : 2 ^ (t + 1) ≤ 2 ^ 17 := Nat.pow_le_pow_right (by norm_num) (by omega)
      omega
    have h49 : (t + 33) ^ 2 ≤ 49 ^ 2 := Nat.pow_le_pow_left (by omega) 2
    norm_num at h49
    have h32 := tres_dos_k hk17
    have hgrande : 3 ^ k * 2 ^ (19 * (t + 33) ^ 2) ≤ n * 2 ^ (k - 1) := by
      calc 3 ^ k * 2 ^ (19 * (t + 33) ^ 2)
          ≤ 2 ^ (79380 + k) * 2 ^ (19 * (t + 33) ^ 2) := Nat.mul_le_mul_right _ h32
        _ = 2 ^ (79380 + k + 19 * (t + 33) ^ 2) := by rw [← pow_add]
        _ ≤ 2 ^ (125000 + (k - 1)) := Nat.pow_le_pow_right (by norm_num) (by omega)
        _ = 2 ^ 125000 * 2 ^ (k - 1) := by rw [pow_add]
        _ ≤ n * 2 ^ (k - 1) := Nat.mul_le_mul_right _ hn
    omega

/-- Por encima de `2^125000`, una falla de CST menor que `2^K` es un residuo sin cruce a los
    `K` pasos. -/
theorem falla_en_sinCruce (hL : LMNEntera) {n K : ℕ} (hn : 2 ^ 125000 ≤ n) (hnK : n < 2 ^ K)
    (hnK' : 2 ^ K ≤ 2 * n) (hf : ∃ k, PrimerCruce n k ∧ n ≤ T^[k] n) : n ∈ sinCruce K := by
  obtain ⟨k, hk, hge⟩ := hf
  have hlt := falla_tardia hL hn hk hge
  have hKk : K < k := by
    by_contra h
    have : 2 ^ k ≤ 2 ^ K := Nat.pow_le_pow_right (by norm_num) (not_lt.mp h)
    omega
  have hK1 : 1 ≤ K := by
    by_contra h
    have : K = 0 := by omega
    subst this
    rw [pow_zero] at hnK
    have hpos : 0 < 2 ^ 125000 := by positivity
    generalize 2 ^ 125000 = X at hn hpos
    omega
  exact Finset.mem_filter.2 ⟨Finset.mem_range.2 hnK, hk.1 K hKk hK1⟩

/-! ## Las cuentas por encima de `2^125000` -/

open Classical in
/-- Fallas de CST desde `2^125000` y menores que `N`. -/
noncomputable def fallasAltas (N : ℕ) : Finset ℕ :=
  (fallasCST N).filter fun n => 2 ^ 125000 ≤ n

theorem mem_fallasAltas {N n : ℕ} :
    n ∈ fallasAltas N ↔ n < N ∧ (∃ k, PrimerCruce n k ∧ n ≤ T^[k] n) ∧ 2 ^ 125000 ≤ n := by
  classical
  simp only [fallasAltas, fallasCST, Finset.mem_filter, Finset.mem_range, and_assoc]

theorem razon_grande : (3 : ℝ) / 2 ≤ (1 + Real.sqrt 3) / Real.sqrt 2 := by
  have h3 := Real.sq_sqrt (show (0 : ℝ) ≤ 3 by norm_num)
  have h2 := Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)
  have h3p := Real.sqrt_nonneg 3
  have h2p := Real.sqrt_nonneg 2
  have hs3 : (17 : ℝ) / 10 < Real.sqrt 3 := by nlinarith
  have hs2 : Real.sqrt 2 < 3 / 2 := by nlinarith
  have hpos : (0 : ℝ) < Real.sqrt 2 := by positivity
  rw [le_div_iff₀ hpos]
  nlinarith

/-- `#fallasAltas(2^J) ≤ 3 ((1+√3)/√2)^J`, bajo `LMNEntera`. -/
theorem fallasAltas_dos (hL : LMNEntera) (J : ℕ) :
    ((fallasAltas (2 ^ J)).card : ℝ) ≤ 3 * ((1 + Real.sqrt 3) / Real.sqrt 2) ^ J := by
  obtain ⟨y, hy⟩ : ∃ y : ℝ, y = (1 + Real.sqrt 3) / Real.sqrt 2 := ⟨_, rfl⟩
  rw [← hy]
  have hy32 : (3 : ℝ) / 2 ≤ y := by rw [hy]; exact razon_grande
  induction J with
  | zero =>
    have h : fallasAltas (2 ^ 0) = ∅ := by
      ext n
      simp only [mem_fallasAltas, Finset.notMem_empty, iff_false, not_and]
      intro hn _ hge
      rw [pow_zero] at hn
      have hpos : 0 < 2 ^ 125000 := by positivity
      generalize 2 ^ 125000 = X at hge hpos
      omega
    rw [h, Finset.card_empty]
    simp
  | succ J ih =>
    have hsub : fallasAltas (2 ^ (J + 1)) ⊆ fallasAltas (2 ^ J) ∪ sinCruce (J + 1) := by
      intro n hn
      rw [mem_fallasAltas] at hn
      obtain ⟨hnN, hf, hbig⟩ := hn
      rw [Finset.mem_union]
      by_cases hJ : n < 2 ^ J
      · exact Or.inl (mem_fallasAltas.2 ⟨hJ, hf, hbig⟩)
      · right
        refine falla_en_sinCruce hL hbig hnN ?_ hf
        rw [pow_succ]
        omega
    have hc : ((fallasAltas (2 ^ (J + 1))).card : ℝ) ≤
        (fallasAltas (2 ^ J)).card + (sinCruce (J + 1)).card := by
      exact_mod_cast le_trans (Finset.card_le_card hsub) (Finset.card_union_le _ _)
    have hs := cota_sinCruce (J + 1)
    rw [← hy] at hs
    have hyJ : (0 : ℝ) ≤ y ^ J := pow_nonneg (by linarith) J
    calc ((fallasAltas (2 ^ (J + 1))).card : ℝ)
        ≤ 3 * y ^ J + y ^ (J + 1) := by linarith
      _ = (3 + y) * y ^ J := by ring
      _ ≤ (3 * y) * y ^ J := by nlinarith
      _ = 3 * y ^ (J + 1) := by ring

/-- **Fallas de CST bajo LMN, con exponente `0,95`.** Para `N ≥ 2`, las fallas de CST
    `n ≥ 2^125000` menores que `N` cumplen `#^20 < 3^20 (2N)^19`. -/
theorem fallasCST_lmn_potencia (hL : LMNEntera) {N : ℕ} (hN : 2 ≤ N) :
    ((fallasAltas N).card : ℝ) ^ 20 < 3 ^ 20 * (2 * N) ^ 19 := by
  obtain ⟨K, hK1, hlow, hhigh⟩ := escala (show 1 < 2 by norm_num) hN
  have hmono : fallasAltas N ⊆ fallasAltas (2 ^ K) := by
    intro n hn
    rw [mem_fallasAltas] at hn ⊢
    exact ⟨lt_of_lt_of_le hn.1 hhigh, hn.2⟩
  have hc : ((fallasAltas N).card : ℝ) ≤ 3 * ((1 + Real.sqrt 3) / Real.sqrt 2) ^ K :=
    le_trans (by exact_mod_cast Finset.card_le_card hmono) (fallasAltas_dos hL K)
  have h2K : (2 : ℝ) ^ K < 2 * N := by
    have : 2 ^ K = 2 * 2 ^ (K - 1) := dos_pred hK1
    have h' : 2 ^ K < 2 * N := by omega
    exact_mod_cast h'
  calc ((fallasAltas N).card : ℝ) ^ 20
      ≤ (3 * ((1 + Real.sqrt 3) / Real.sqrt 2) ^ K) ^ 20 :=
        pow_le_pow_left₀ (by positivity) hc 20
    _ = 3 ^ 20 * (((1 + Real.sqrt 3) / Real.sqrt 2) ^ 20) ^ K := by
        rw [mul_pow, ← pow_mul, ← pow_mul, mul_comm K]
    _ < 3 ^ 20 * ((2 : ℝ) ^ 19) ^ K := by
        have h : (((1 + Real.sqrt 3) / Real.sqrt 2) ^ 20) ^ K < ((2 : ℝ) ^ 19) ^ K :=
          pow_lt_pow_left₀ razon_fugitivos (by positivity) (by omega)
        exact mul_lt_mul_of_pos_left h (by positivity)
    _ = 3 ^ 20 * ((2 : ℝ) ^ K) ^ 19 := by rw [← pow_mul, ← pow_mul, mul_comm 19 K]
    _ ≤ 3 ^ 20 * (2 * N) ^ 19 := by
        have := pow_le_pow_left₀ (by positivity) h2K.le 19
        nlinarith

/-- **Los que nunca bajan, bajo LMN, con exponente `0,95`.** Para `N ≥ 2`, los `n ≥ 2^125000`
    menores que `N` que nunca bajan de sí mismos cumplen `#^20 < 4^20 (2N)^19`. -/
theorem noDescienden_lmn_potencia (hL : LMNEntera) {N : ℕ} (hN : 2 ≤ N) :
    (((noDescienden N).filter fun n => 2 ^ 125000 ≤ n).card : ℝ) ^ 20 <
      4 ^ 20 * (2 * N) ^ 19 := by
  classical
  obtain ⟨K, hK1, hlow, hhigh⟩ := escala (show 1 < 2 by norm_num) hN
  have hsub : ((noDescienden N).filter fun n => 2 ^ 125000 ≤ n) ⊆
      sinCruce K ∪ fallasAltas (2 ^ K) := by
    intro n hn
    rw [Finset.mem_filter] at hn
    obtain ⟨hn1, hbig⟩ := hn
    have hn2 : n < N ∧ ¬ Desciende n := by simpa [noDescienden] using hn1
    obtain ⟨hnN, hnd⟩ := hn2
    rw [Finset.mem_union]
    by_cases hc : Cruza n
    · right
      obtain ⟨k, hk⟩ := primerCruce_de_cruza hc
      have hge : n ≤ T^[k] n := by
        by_contra hlt
        exact hnd ⟨k, primerCruce_pos hk, not_le.mp hlt⟩
      exact mem_fallasAltas.2 ⟨lt_of_lt_of_le hnN hhigh, ⟨k, hk, hge⟩, hbig⟩
    · left
      exact Finset.mem_filter.2
        ⟨Finset.mem_range.2 (lt_of_lt_of_le hnN hhigh), fugitivo_sube hc K⟩
  have hc : (((noDescienden N).filter fun n => 2 ^ 125000 ≤ n).card : ℝ) ≤
      4 * ((1 + Real.sqrt 3) / Real.sqrt 2) ^ K := by
    have h1 : (((noDescienden N).filter fun n => 2 ^ 125000 ≤ n).card : ℝ) ≤
        (sinCruce K).card + (fallasAltas (2 ^ K)).card := by
      exact_mod_cast le_trans (Finset.card_le_card hsub) (Finset.card_union_le _ _)
    have h2 := cota_sinCruce K
    have h3 := fallasAltas_dos hL K
    linarith
  have h2K : (2 : ℝ) ^ K < 2 * N := by
    have : 2 ^ K = 2 * 2 ^ (K - 1) := dos_pred hK1
    have h' : 2 ^ K < 2 * N := by omega
    exact_mod_cast h'
  calc (((noDescienden N).filter fun n => 2 ^ 125000 ≤ n).card : ℝ) ^ 20
      ≤ (4 * ((1 + Real.sqrt 3) / Real.sqrt 2) ^ K) ^ 20 :=
        pow_le_pow_left₀ (by positivity) hc 20
    _ = 4 ^ 20 * (((1 + Real.sqrt 3) / Real.sqrt 2) ^ 20) ^ K := by
        rw [mul_pow, ← pow_mul, ← pow_mul, mul_comm K]
    _ < 4 ^ 20 * ((2 : ℝ) ^ 19) ^ K := by
        have h : (((1 + Real.sqrt 3) / Real.sqrt 2) ^ 20) ^ K < ((2 : ℝ) ^ 19) ^ K :=
          pow_lt_pow_left₀ razon_fugitivos (by positivity) (by omega)
        exact mul_lt_mul_of_pos_left h (by positivity)
    _ = 4 ^ 20 * ((2 : ℝ) ^ K) ^ 19 := by rw [← pow_mul, ← pow_mul, mul_comm 19 K]
    _ ≤ 4 ^ 20 * (2 * N) ^ 19 := by
        have := pow_le_pow_left₀ (by positivity) h2K.le 19
        nlinarith

end CasaLMN

#print axioms CasaLMN.cruce_justo
#print axioms CasaLMN.falla_dos
#print axioms CasaLMN.falla_acotada
#print axioms CasaLMN.tres_cuatro_base
#print axioms CasaLMN.tres_cuatro
#print axioms CasaLMN.tres_cuatro_k
#print axioms CasaLMN.tres_dos_base
#print axioms CasaLMN.tres_dos_k
#print axioms CasaLMN.falla_tardia
#print axioms CasaLMN.falla_en_sinCruce
#print axioms CasaLMN.fallasAltas_dos
#print axioms CasaLMN.fallasCST_lmn_potencia
#print axioms CasaLMN.noDescienden_lmn_potencia
