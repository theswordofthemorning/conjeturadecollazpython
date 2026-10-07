import CasaPlaneador

/-! # La grieta: el intruso del muro A

07-10-2026. Explicación en `LEEME.md` de esta carpeta, sección «El retrato de la grieta».

Una **grieta** del muro A es un número `n ≥ 2` cuyo pronóstico baja de 1 pero que nunca
baja de sí mismo. El muro A dice exactamente que no hay grietas
(`muroA_iff_sin_grietas`). Este archivo hace con la grieta lo que `CasaRetrato` hizo con el
fugitivo: la supone y anota lo que tendría que cumplir.

* `desciende_de_cruce`, `desciende_si_grande`: el **descenso de Terras** (1976), con cota
  explícita: si el pronóstico cruza por primera vez en el paso `k` y `k·2^k ≤ 3n`, el número
  baja en ese mismo paso;
* `cuenta_sin_descenso`, `casi_todo_desciende`: **casi todo número baja de sí mismo**
  (Terras, 1976; Everett, 1977): por debajo de `2^(104m)` los que nunca bajan son a lo sumo
  `(100m + 2)·2^(100m)`, y tienen densidad cero;
* `grieta_tarde`: **rasgo G1**: una grieta cruza tarde para su tamaño, `3n < k·2^k`;
* `desciende_lmn`, `teorema_E_lmn`, `grieta_lmn`: bajo LMN, el **teorema E** de Lagarias
  (1985) con constante explícita: si el primer cruce es `k ≥ 2^16`, sólo el menor número de
  la clase módulo `2^k` podría ser grieta; con Rhin (`teorema_E_rhin`, `grieta_rhin`) basta
  `k ≥ 98`, y la grieta cumple `3n ≤ k^15`;
* `circuito_tiene_grieta`: el menor valor de todo circuito es una grieta; `circuito_exige_25`:
  bajo LMN, por el tramo de Ocelotas, ninguna vuelta de circuito tiene 24 picos o menos;
* `crias_sin_muroA`: sin el muro A, cada punto sin retorno de un fugitivo es una fuga pura o
  una grieta; `sin_retorno_raros`: esos puntos son raros, como en (2.32) de Lagarias;
* `fuga_tiende`, `fuga_sube`: toda órbita que crece sin límite, pura o no, tiende al infinito
  y termina subiendo en al menos 63 de cada 100 pasos, salvo una constante ((2.31) de
  Lagarias); vale para una grieta cuya órbita escapa;
* `retrato_grieta`: los rasgos juntos.

Hipótesis externas sólo donde se nombran: `LMN23` (corolario 2 de Laurent–Mignotte–Nesterenko,
1995, la de `CasaOcelotas`) en `desciende_lmn`, `teorema_E_lmn`, `grieta_lmn` y
`circuito_exige_25`, y `RhinEntera` (forma entera de la cota de Rhin, 1987, la de `Ocelotas`)
en `desciende_rhin`, `teorema_E_rhin` y `grieta_rhin`. Son argumentos de los teoremas, no
axiomas.

Compilación: `comprobar_casa.py`, en esta carpeta. -/

namespace CasaGrieta

open Ocelotas OcelotasContador OcelotasTrayectorias OcelotasCierre OcelotasLMN
  OcelotasLMNFuente CasaPlano CasaRetrato CasaTablero CasaPlaneador

/-- Una **grieta** del muro A: el pronóstico baja de 1, pero el número nunca baja de sí
    mismo. -/
def Grieta (n : ℕ) : Prop := 2 ≤ n ∧ Cruza n ∧ ¬ Desciende n

/-- El muro A dice exactamente que no hay grietas. -/
theorem muroA_iff_sin_grietas : MuroA ↔ ∀ n, ¬ Grieta n := by
  unfold MuroA Grieta
  constructor
  · rintro hA n ⟨h2, hc, hd⟩
    exact hd (hA n h2 hc)
  · intro h n h2 hc
    by_contra hd
    exact h n ⟨h2, hc, hd⟩

/-! ## El descenso de Terras -/

/-- **Descenso de Terras** (Terras, 1976, teorema C(b) en la reseña de Lagarias, 1985), con
    cota explícita: si el pronóstico cruza por primera vez en el paso `k` y `S·3^S < 3n`,
    donde `S` cuenta las subidas de esos `k` pasos, el número ya bajó en el paso `k`. -/
theorem desciende_de_cruce {n k : ℕ} (hk : PrimerCruce n k)
    (h : S k n * 3 ^ S k n < 3 * n) : T^[k] n < n := by
  have ht := tamano_antes_del_cruce k fun i hi => pre_cruce hk hi
  have hq := hk.2
  by_contra hc
  push Not at hc
  have h1 : 3 * (2 ^ k * n) ≤ 3 * (2 ^ k * T^[k] n) := by
    have := Nat.mul_le_mul_left (2 ^ k) hc
    omega
  have h3 : 3 * n * (3 ^ S k n + 1) ≤ 3 * n * 2 ^ k := Nat.mul_le_mul_left _ hq
  nlinarith

/-- Basta `k·2^k ≤ 3n`: los números grandes de cada clase bajan justo en su primer cruce. -/
theorem desciende_si_grande {n k : ℕ} (hk : PrimerCruce n k) (h : k * 2 ^ k ≤ 3 * n) :
    T^[k] n < n := by
  apply desciende_de_cruce hk
  have hk1 := primerCruce_pos hk
  have hS := S_le_pasos k n
  have hq := hk.2
  rcases Nat.eq_zero_or_pos (S k n) with h0 | h0
  · rw [h0, zero_mul]
    have h2 : 2 ≤ 2 ^ k := by
      calc 2 = 2 ^ 1 := by norm_num
        _ ≤ 2 ^ k := Nat.pow_le_pow_right (by norm_num) hk1
    have h3 : 2 ≤ k * 2 ^ k := le_trans h2 (Nat.le_mul_of_pos_left _ (by omega))
    omega
  · calc S k n * 3 ^ S k n < S k n * 2 ^ k := Nat.mul_lt_mul_of_pos_left hq h0
      _ ≤ k * 2 ^ k := Nat.mul_le_mul_right _ hS
      _ ≤ 3 * n := h

/-- Un número que nunca baja de sí mismo es chico comparado con su primer cruce. -/
theorem chico_si_no_baja {n k : ℕ} (hk : PrimerCruce n k) (hd : ¬ Desciende n) :
    3 * n < k * 2 ^ k := by
  by_contra h
  push Not at h
  exact hd ⟨k, primerCruce_pos hk, desciende_si_grande hk h⟩

/-! ## Casi todo número baja -/

/-- Si el pronóstico está por debajo de 1 en el paso `j`, el primer cruce llega a más tardar
    en `j`. -/
theorem primer_cruce_antes {n j : ℕ} (h : 3 ^ S j n < 2 ^ j) :
    ∃ k, k ≤ j ∧ PrimerCruce n k := by
  classical
  have hc : Cruza n := ⟨j, h⟩
  refine ⟨Nat.find hc, Nat.find_min' hc h, ?_, Nat.find_spec hc⟩
  intro i hi _
  exact not_lt.mp (Nat.find_min hc hi)

open Classical in
/-- **Cuenta de los que no bajan.** Entre 0 y N−1, los números que nunca bajan de sí mismos
    son a lo sumo los que aguantan `100m` pasos sin cruzar más los menores que
    `100m·2^(100m)`. -/
theorem cuenta_sin_descenso_bloques (N m : ℕ) :
    ((Finset.range N).filter fun n => ¬ Desciende n).card ≤
      (N / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) + 100 * m * 2 ^ (100 * m) := by
  have hsub : (Finset.range N).filter (fun n => ¬ Desciende n) ⊆
      (Finset.range N).filter (fun n => 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n) ∪
        Finset.range (100 * m * 2 ^ (100 * m)) := by
    intro n hn
    rw [Finset.mem_filter] at hn
    rw [Finset.mem_union, Finset.mem_filter, Finset.mem_range, Finset.mem_range]
    by_cases h : 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n
    · exact Or.inl ⟨Finset.mem_range.1 hn.1, h⟩
    · right
      push Not at h
      obtain ⟨k, hkj, hk⟩ := primer_cruce_antes h
      have h1 := chico_si_no_baja hk hn.2
      have h2 : k * 2 ^ k ≤ 100 * m * 2 ^ (100 * m) :=
        Nat.mul_le_mul hkj (Nat.pow_le_pow_right (by norm_num) hkj)
      omega
  calc ((Finset.range N).filter fun n => ¬ Desciende n).card
      ≤ ((Finset.range N).filter (fun n => 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n) ∪
          Finset.range (100 * m * 2 ^ (100 * m))).card := Finset.card_le_card hsub
    _ ≤ ((Finset.range N).filter (fun n => 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n)).card +
          (Finset.range (100 * m * 2 ^ (100 * m))).card := Finset.card_union_le _ _
    _ ≤ (N / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) + 100 * m * 2 ^ (100 * m) := by
      rw [Finset.card_range]
      exact Nat.add_le_add_right (cuenta_sin_cruce N m) _

open Classical in
/-- **En cifras:** por debajo de `2^(104m)` hay a lo sumo `(100m + 2)·2^(100m)` números que
    nunca bajan de sí mismos; por debajo de x, unos x^0,962 por un factor logarítmico. -/
theorem cuenta_sin_descenso (m : ℕ) :
    ((Finset.range (2 ^ (104 * m))).filter fun n => ¬ Desciende n).card ≤
      (100 * m + 2) * 2 ^ (100 * m) := by
  have h := cuenta_sin_descenso_bloques (2 ^ (104 * m)) m
  have e1 : 2 ^ (104 * m) / 2 ^ (100 * m) = 2 ^ (4 * m) := by
    rw [Nat.pow_div (by omega) (by norm_num)]
    congr 1
    omega
  have e2 : (2 ^ (4 * m) + 1) * 2 ^ (96 * m) = 2 ^ (100 * m) + 2 ^ (96 * m) := by
    rw [add_mul, one_mul, ← pow_add]
    congr 2
    omega
  have e3 : 2 ^ (96 * m) ≤ 2 ^ (100 * m) := Nat.pow_le_pow_right (by norm_num) (by omega)
  rw [e1, e2] at h
  nlinarith

open Classical in
/-- **Casi todo número baja de sí mismo** (Terras, 1976; Everett, 1977): los números que
    nunca bajan tienen densidad cero. -/
theorem casi_todo_desciende {ε : ℝ} (hε : 0 < ε) :
    ∃ N₀ : ℕ, ∀ N, N₀ ≤ N →
      (((Finset.range N).filter fun n => ¬ Desciende n).card : ℝ) ≤ ε * N := by
  obtain ⟨m, hm⟩ := pow_unbounded_of_one_lt (2 / ε) (by norm_num : (1 : ℝ) < 16)
  set R : ℕ := 2 ^ (96 * m) + 100 * m * 2 ^ (100 * m) with hR
  refine ⟨⌈2 * (R : ℝ) / ε⌉₊, fun N hN => ?_⟩
  have h1 := cuenta_sin_descenso_bloques N m
  have e : 2 ^ (100 * m) = 16 ^ m * 2 ^ (96 * m) := by
    rw [show 100 * m = 4 * m + 96 * m by ring, pow_add, pow_mul]
    norm_num
  have h2 : N / 2 ^ (100 * m) * 2 ^ (96 * m) ≤ N / 16 ^ m := by
    rw [e, ← Nat.div_div_eq_div_mul]
    exact Nat.div_mul_le_self _ _
  have h3 : ((Finset.range N).filter fun n => ¬ Desciende n).card ≤ N / 16 ^ m + R := by
    have e4 : (N / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) =
        N / 2 ^ (100 * m) * 2 ^ (96 * m) + 2 ^ (96 * m) := by ring
    rw [hR]
    omega
  have h4 : (((Finset.range N).filter fun n => ¬ Desciende n).card : ℝ) ≤
      ((N / 16 ^ m : ℕ) : ℝ) + R := by
    exact_mod_cast h3
  have h16 : (0 : ℝ) < 16 ^ m := by positivity
  have h5 : ((N / 16 ^ m : ℕ) : ℝ) ≤ (N : ℝ) / 16 ^ m := by
    rw [le_div_iff₀ h16]
    exact_mod_cast Nat.div_mul_le_self N (16 ^ m)
  have h6 : (N : ℝ) / 16 ^ m ≤ ε * N / 2 := by
    rw [div_le_iff₀ h16]
    have h7 : 2 < 16 ^ m * ε := (div_lt_iff₀ hε).1 hm
    nlinarith [Nat.cast_nonneg (α := ℝ) N]
  have h8 : (R : ℝ) ≤ ε * N / 2 := by
    have h9 : 2 * (R : ℝ) / ε ≤ (N : ℝ) := (Nat.le_ceil _).trans (by exact_mod_cast hN)
    rw [div_le_iff₀ hε] at h9
    linarith
  linarith

/-! ## Con LMN y con Rhin: la grieta es la menor de su clase -/

/-- Margen numérico para LMN: `19(t + 33)^2 + t + 1 ≤ 2^t` desde `t = 16`. -/
theorem margen_lmn : ∀ t, 16 ≤ t → 19 * (t + 33) ^ 2 + t + 1 ≤ 2 ^ t := by
  intro t ht
  induction t, ht using Nat.le_induction with
  | base => norm_num
  | succ t ht ih =>
    rw [pow_succ 2 t]
    nlinarith [ih, Nat.zero_le (t * t)]

/-- **Bajo LMN, cruzar a tiempo obliga a bajar**: si el pronóstico cruza por primera vez en
    el paso `k ≥ 2` y `k·2^(19(log₂ k + 33)^2) < 3n`, el número baja en el paso `k`. -/
theorem desciende_lmn (hL : LMN23) {n k : ℕ} (hk : PrimerCruce n k) (hk2 : 2 ≤ k)
    (h : k * 2 ^ (19 * (Nat.log 2 k + 33) ^ 2) < 3 * n) : T^[k] n < n := by
  have hv := (ventana_cruce hk).2
  have hq := hk.2
  have hcola := cola_lmn_entera (debil_de_corolario hL) hk2 hv hq
    (Nat.lt_pow_succ_log_self (by norm_num) k)
  have ht := tamano_antes_del_cruce k fun i hi => pre_cruce hk hi
  have hS := S_le_pasos k n
  by_contra hc
  push Not at hc
  set A := 3 ^ S k n with hA
  set E := 2 ^ (19 * (Nat.log 2 k + 33) ^ 2) with hE
  obtain ⟨D, hD⟩ : ∃ D, 2 ^ k = A + D := ⟨2 ^ k - A, by omega⟩
  rw [hD, Nat.add_sub_cancel_left] at hcola
  rw [hD] at ht hq
  have hD1 : 1 ≤ D := by omega
  have e1 : 3 * ((A + D) * n) ≤ 3 * ((A + D) * T^[k] n) := by
    have := Nat.mul_le_mul_left (A + D) hc
    omega
  have e2 : 3 * D * n ≤ A * S k n := by nlinarith
  have e3 : A * S k n ≤ D * E * k :=
    calc A * S k n ≤ D * E * S k n := Nat.mul_le_mul_right _ hcola
      _ ≤ D * E * k := Nat.mul_le_mul_left _ hS
  have e4 : D * (k * E) < D * (3 * n) := Nat.mul_lt_mul_of_pos_left h hD1
  nlinarith

/-- **Teorema E de Lagarias (1985), explícito bajo LMN**: si el primer cruce es `k ≥ 2^16`,
    todo número de la clase que sea al menos `2^k` baja en el paso `k`. Una grieta con un
    primer cruce así sería el menor número de su clase módulo `2^k`. -/
theorem teorema_E_lmn (hL : LMN23) {n k : ℕ} (hk : PrimerCruce n k) (hk16 : 2 ^ 16 ≤ k)
    (hn : 2 ^ k ≤ n) : T^[k] n < n := by
  apply desciende_lmn hL hk (le_trans (by norm_num) hk16)
  set t := Nat.log 2 k with htdef
  have ht16 : 16 ≤ t := Nat.le_log_of_pow_le (by norm_num) hk16
  have hkt : k < 2 ^ (t + 1) := Nat.lt_pow_succ_log_self (by norm_num) k
  have hm := margen_lmn t ht16
  have h2t : 2 ^ t ≤ k := Nat.pow_log_le_self 2 (by omega)
  calc k * 2 ^ (19 * (t + 33) ^ 2) < 2 ^ (t + 1) * 2 ^ (19 * (t + 33) ^ 2) :=
        Nat.mul_lt_mul_of_pos_right hkt (by positivity)
    _ = 2 ^ (19 * (t + 33) ^ 2 + t + 1) := by
        rw [← pow_add]
        congr 1
        ring
    _ ≤ 2 ^ (2 ^ t) := Nat.pow_le_pow_right (by norm_num) hm
    _ ≤ 2 ^ k := Nat.pow_le_pow_right (by norm_num) h2t
    _ ≤ n := hn
    _ < 3 * n := by
        have : 1 ≤ 2 ^ k := Nat.one_le_two_pow
        omega

/-- `k^15 < 3·2^k` desde `k = 98`. -/
theorem quince_exp : ∀ k, 98 ≤ k → k ^ 15 < 3 * 2 ^ k := by
  intro k hk
  induction k, hk using Nat.le_induction with
  | base => norm_num
  | succ k hk ih =>
    have h1 : (k + 1) * 98 ≤ 99 * k := by omega
    have h2 : ((k + 1) * 98) ^ 15 ≤ (99 * k) ^ 15 := Nat.pow_le_pow_left h1 15
    rw [mul_pow, mul_pow] at h2
    have h3 : (99 : ℕ) ^ 15 ≤ 2 * 98 ^ 15 := by norm_num
    have h4 : (k + 1) ^ 15 ≤ 2 * k ^ 15 := by
      have h5 : (k + 1) ^ 15 * 98 ^ 15 ≤ 2 * k ^ 15 * 98 ^ 15 :=
        calc (k + 1) ^ 15 * 98 ^ 15 ≤ 99 ^ 15 * k ^ 15 := h2
          _ ≤ 2 * 98 ^ 15 * k ^ 15 := Nat.mul_le_mul_right _ h3
          _ = 2 * k ^ 15 * 98 ^ 15 := by ring
      exact Nat.le_of_mul_le_mul_right h5 (by positivity)
    rw [pow_succ 2 k]
    omega

/-- **Bajo Rhin, más fino**: si el pronóstico cruza por primera vez en el paso `k` y
    `k^15 < 3n`, el número baja en el paso `k`. -/
theorem desciende_rhin (hR : RhinEntera) {n k : ℕ} (hk : PrimerCruce n k)
    (h : k ^ 15 < 3 * n) : T^[k] n < n := by
  have hv := (ventana_cruce hk).2
  have hq := hk.2
  have hrh := hR k (S k n) hv hq
  have ht := tamano_antes_del_cruce k fun i hi => pre_cruce hk hi
  have hS := S_le_pasos k n
  by_contra hc
  push Not at hc
  set A := 3 ^ S k n with hA
  obtain ⟨D, hD⟩ : ∃ D, 2 ^ k = A + D := ⟨2 ^ k - A, by omega⟩
  rw [hD, Nat.add_sub_cancel_left] at hrh
  rw [hD] at ht hq
  have hD1 : 1 ≤ D := by omega
  have e1 : 3 * ((A + D) * n) ≤ 3 * ((A + D) * T^[k] n) := by
    have := Nat.mul_le_mul_left (A + D) hc
    omega
  have e2 : 3 * D * n ≤ A * S k n := by nlinarith
  have e3 : A * S k n ≤ D * k ^ 15 :=
    calc A * S k n ≤ D * k ^ 14 * S k n := Nat.mul_le_mul_right _ hrh
      _ ≤ D * k ^ 14 * k := Nat.mul_le_mul_left _ hS
      _ = D * k ^ 15 := by ring
  have e4 : D * k ^ 15 < D * (3 * n) := Nat.mul_lt_mul_of_pos_left h hD1
  nlinarith

/-- **Teorema E de Lagarias, explícito bajo Rhin**: con primer cruce `k ≥ 98`, todo número de
    la clase que sea al menos `2^k` baja en el paso `k`. -/
theorem teorema_E_rhin (hR : RhinEntera) {n k : ℕ} (hk : PrimerCruce n k) (hk98 : 98 ≤ k)
    (hn : 2 ^ k ≤ n) : T^[k] n < n :=
  desciende_rhin hR hk (lt_of_lt_of_le (quince_exp k hk98) (by omega))

/-! ## El retrato de la grieta -/

/-- Una grieta nunca baja de sí misma. -/
theorem grieta_no_baja {n : ℕ} (h : Grieta n) (k : ℕ) : n ≤ T^[k] n := by
  rcases Nat.eq_zero_or_pos k with h0 | h0
  · simp [h0]
  · by_contra hc
    push Not at hc
    exact h.2.2 ⟨k, h0, hc⟩

/-- Una grieta no llega a 1. -/
theorem grieta_no_llega {n : ℕ} (h : Grieta n) : ¬ LlegaT n := by
  rintro ⟨k, hk⟩
  have h1 := grieta_no_baja h k
  have h2 := h.1
  omega

/-- **Rasgo G1: la grieta cruza tarde**, sin hipótesis externas: su primer cruce `k` es al
    menos 2 y cumple `3n ≤ S·3^S < k·2^k`. -/
theorem grieta_tarde {n : ℕ} (h : Grieta n) :
    ∃ k, PrimerCruce n k ∧ 2 ≤ k ∧ 3 * n ≤ S k n * 3 ^ S k n ∧ 3 * n < k * 2 ^ k := by
  obtain ⟨k, hk⟩ := primerCruce_de_cruza h.2.1
  have hk1 := primerCruce_pos hk
  refine ⟨k, hk, ?_, ?_, chico_si_no_baja hk h.2.2⟩
  · by_contra hk2
    have e : k = 1 := by omega
    subst e
    have h2 := hk.2
    have hpar : n % 2 = 0 := by
      rcases Nat.mod_two_eq_zero_or_one n with hp | hp
      · exact hp
      · simp [S, hp] at h2
    exact h.2.2 ⟨1, le_rfl, descenso_par h.1 hpar hk⟩
  · by_contra hc
    push Not at hc
    exact h.2.2 ⟨k, hk1, desciende_de_cruce hk hc⟩

/-- **Rasgo G2, bajo LMN**: `3n ≤ k·2^(19(log₂ k + 33)^2)`, y si `k ≥ 2^16`, la grieta es
    menor que `2^k`: la menor de su clase. -/
theorem grieta_lmn (hL : LMN23) {n : ℕ} (h : Grieta n) :
    ∃ k, PrimerCruce n k ∧ 3 * n ≤ k * 2 ^ (19 * (Nat.log 2 k + 33) ^ 2) ∧
      (2 ^ 16 ≤ k → n < 2 ^ k) := by
  obtain ⟨k, hk, hk2, -, -⟩ := grieta_tarde h
  refine ⟨k, hk, ?_, fun h16 => ?_⟩
  · by_contra hc
    push Not at hc
    exact h.2.2 ⟨k, by omega, desciende_lmn hL hk hk2 hc⟩
  · by_contra hc
    push Not at hc
    exact h.2.2 ⟨k, by omega, teorema_E_lmn hL hk h16 hc⟩

/-- **Rasgo G2, bajo Rhin**: `3n ≤ k^15`, y si `k ≥ 98`, la grieta es menor que `2^k`. -/
theorem grieta_rhin (hR : RhinEntera) {n : ℕ} (h : Grieta n) :
    ∃ k, PrimerCruce n k ∧ 3 * n ≤ k ^ 15 ∧ (98 ≤ k → n < 2 ^ k) := by
  obtain ⟨k, hk, hk2, -, -⟩ := grieta_tarde h
  refine ⟨k, hk, ?_, fun h98 => ?_⟩
  · by_contra hc
    push Not at hc
    exact h.2.2 ⟨k, by omega, desciende_rhin hR hk hc⟩
  · by_contra hc
    push Not at hc
    exact h.2.2 ⟨k, by omega, teorema_E_rhin hR hk h98 hc⟩

/-- **Todo circuito tiene una grieta**: su menor valor. -/
theorem circuito_tiene_grieta {x : ℕ} (hx : Circuito x) : ∃ i, Grieta (T^[i] x) := by
  classical
  obtain ⟨hx1, ⟨p, hp1, hpx⟩, hno1⟩ := hx
  have hex : ∃ v, ∃ j, T^[j] x = v := ⟨x, 0, rfl⟩
  obtain ⟨j0, hj0⟩ := Nat.find_spec hex
  have hmin : ∀ j, Nat.find hex ≤ T^[j] x := fun j => Nat.find_min' hex ⟨j, rfl⟩
  generalize Nat.find hex = m at hj0 hmin
  refine ⟨j0, ?_⟩
  rw [hj0]
  have hm1 : 1 ≤ m := hj0 ▸ iter_pos hx1 j0
  have hm2 : 2 ≤ m := by
    have := hno1 j0
    omega
  have horb : ∀ k, m ≤ T^[k] m := by
    intro k
    have h := hmin (k + j0)
    rwa [Function.iterate_add_apply, hj0] at h
  have hmp : T^[p] m = m := by
    rw [← hj0, ← Function.iterate_add_apply, add_comm, Function.iterate_add_apply, hpx]
  refine ⟨hm2, ⟨p, ciclo_cruza hm1 hp1 hmp⟩, ?_⟩
  rintro ⟨k, -, hk⟩
  have := horb k
  omega

/-- **Sin el muro A, el fugitivo deja crías de dos clases**: en toda órbita que crece sin
    límite hay, tan lejos como se quiera, puntos sin retorno, y cada uno es una fuga pura o
    una grieta. -/
theorem crias_sin_muroA {n : ℕ} (hf : Fuga n) (K : ℕ) :
    ∃ k, K ≤ k ∧ (∀ t, 1 ≤ t → T^[k] n < T^[t] (T^[k] n)) ∧
      (FugaPura (T^[k] n) ∨ Grieta (T^[k] n)) := by
  classical
  have hex : ∃ v, ∃ j, K ≤ j ∧ T^[j] n = v := ⟨_, K, le_rfl, rfl⟩
  obtain ⟨k, hk, hkv⟩ := Nat.find_spec hex
  have hmin : ∀ t, 1 ≤ t → T^[k] n < T^[t] (T^[k] n) := by
    intro t ht
    have h1 : Nat.find hex ≤ T^[t + k] n := Nat.find_min' hex ⟨t + k, by omega, rfl⟩
    have hne : T^[k] n ≠ T^[t + k] n := fuga_no_repite hf (by omega)
    rw [← Function.iterate_add_apply]
    omega
  refine ⟨k, hk, hmin, ?_⟩
  have hv2 : 2 ≤ T^[k] n := by
    by_contra hlt
    push Not at hlt
    have h2 := hmin 2 (by norm_num)
    generalize T^[k] n = v at h2 hlt
    rcases (by omega : v = 0 ∨ v = 1) with rfl | rfl <;> revert h2 <;> decide
  by_cases hc : Cruza (T^[k] n)
  · right
    refine ⟨hv2, hc, ?_⟩
    rintro ⟨t, ht, hlt⟩
    have := hmin t ht
    omega
  · exact Or.inl hc

open Classical in
/-- **Los puntos sin retorno son raros** ((2.32) de Lagarias, 1985, en cifras): por debajo de
    `2^(104m)`, una órbita que crece sin límite pasa por a lo sumo `(100m + 2)·2^(100m)`
    puntos sin retorno. -/
theorem sin_retorno_raros {n : ℕ} (hf : Fuga n) (m K : ℕ) :
    ((Finset.range K).filter fun k => T^[k] n < 2 ^ (104 * m) ∧
        ∀ t, 1 ≤ t → T^[k] n < T^[t] (T^[k] n)).card ≤ (100 * m + 2) * 2 ^ (100 * m) := by
  refine le_trans ?_ (cuenta_sin_descenso m)
  refine Finset.card_le_card_of_injOn (fun k => T^[k] n) ?_ ?_
  · intro k hk
    rw [Finset.mem_coe, Finset.mem_filter] at hk
    rw [Finset.mem_coe, Finset.mem_filter, Finset.mem_range]
    show T^[k] n < 2 ^ (104 * m) ∧ ¬ Desciende (T^[k] n)
    refine ⟨hk.2.1, ?_⟩
    rintro ⟨t, ht, hlt⟩
    have := hk.2.2 t ht
    omega
  · intro i _ j _ hij
    exact fuga_inyectiva hf hij

/-- Las rachas sólo crecen con los pasos. -/
theorem rachas_mono (n : ℕ) {k k' : ℕ} (h : k ≤ k') : rachas n k ≤ rachas n k' := by
  induction k', h using Nat.le_induction with
  | base => exact le_rfl
  | succ k' _ ih =>
    rw [rachas]
    exact le_trans ih (Nat.le_add_right _ _)

/-- **Bajo LMN, ningún circuito tiene 24 picos o menos**: el menor valor de un circuito es una
    grieta, y desde él una vuelta tiene al menos 25 rachas impares. -/
theorem circuito_exige_25 (hL : LMN23) {x : ℕ} (hx : Circuito x) :
    ∃ i p, Grieta (T^[i] x) ∧ 1 ≤ p ∧ T^[p] (T^[i] x) = T^[i] x ∧
      25 ≤ rachas (T^[i] x) p := by
  obtain ⟨i, hg⟩ := circuito_tiene_grieta hx
  obtain ⟨-, ⟨p, hp1, hpx⟩, -⟩ := hx
  have hmp : T^[p] (T^[i] x) = T^[i] x := by
    rw [← Function.iterate_add_apply, add_comm, Function.iterate_add_apply, hpx]
  obtain ⟨k, hk, hr⟩ := CasaOcelotas.grieta_exige_25 hL hg.1 hg.2.1 hg.2.2
  have hkp : k ≤ p := by
    by_contra hlt
    push Not at hlt
    have h1 := hk.1 p hlt hp1
    have h2 := ciclo_cruza (le_trans (by norm_num) hg.1) hp1 hmp
    omega
  exact ⟨i, p, hg, hp1, hmp, le_trans hr (rachas_mono _ hkp)⟩

/-! ## Toda fuga, pura o no -/

/-- Toda órbita que crece sin límite tiende al infinito: pasado cierto paso, nunca vuelve a
    quedar por debajo de una cota dada. -/
theorem fuga_tiende {n : ℕ} (hf : Fuga n) (M : ℕ) : ∃ K, ∀ k, K ≤ k → M < T^[k] n := by
  have hfin : ((fun k => T^[k] n) ⁻¹' Set.Iic M).Finite :=
    (Set.finite_Iic M).preimage (fuga_inyectiva hf).injOn
  obtain ⟨K, hK⟩ := hfin.bddAbove
  refine ⟨K + 1, fun k hk => ?_⟩
  by_contra hc
  have hmem : k ∈ (fun k => T^[k] n) ⁻¹' Set.Iic M := by
    simp only [Set.mem_preimage, Set.mem_Iic]
    omega
  have := hK hmem
  omega

/-- Mientras el valor no baje de 1000, cada subida multiplica a lo sumo por 3001/2000 y cada
    bajada divide por 2: `1000^S · 2^t · T^t(x) ≤ 3001^S · x`. -/
theorem crecimiento_alto {x : ℕ} :
    ∀ t, (∀ i, i < t → 1000 ≤ T^[i] x) →
      1000 ^ S t x * 2 ^ t * T^[t] x ≤ 3001 ^ S t x * x := by
  intro t
  induction t with
  | zero => intro _; simp [S]
  | succ t ih =>
    intro halto
    have ih' := ih fun i hi => halto i (by omega)
    have hy := halto t (by omega)
    have hS : S (t + 1) x = S t x + T^[t] x % 2 := by
      rw [S_add]
      simp [S]
    rw [Function.iterate_succ_apply', hS]
    rcases Nat.mod_two_eq_zero_or_one (T^[t] x) with hp | hp
    · rw [hp, Nat.add_zero]
      have he := T_par hp
      calc 1000 ^ S t x * 2 ^ (t + 1) * T (T^[t] x)
          = 1000 ^ S t x * 2 ^ t * (2 * T (T^[t] x)) := by ring
        _ = 1000 ^ S t x * 2 ^ t * T^[t] x := by rw [he]
        _ ≤ 3001 ^ S t x * x := ih'
    · rw [hp]
      have he := T_impar hp
      have h1 : 1000 * (2 * T (T^[t] x)) ≤ 3001 * T^[t] x := by omega
      calc 1000 ^ (S t x + 1) * 2 ^ (t + 1) * T (T^[t] x)
          = 1000 ^ S t x * 2 ^ t * (1000 * (2 * T (T^[t] x))) := by ring
        _ ≤ 1000 ^ S t x * 2 ^ t * (3001 * T^[t] x) := Nat.mul_le_mul_left _ h1
        _ = 3001 * (1000 ^ S t x * 2 ^ t * T^[t] x) := by ring
        _ ≤ 3001 * (3001 ^ S t x * x) := Nat.mul_le_mul_left _ ih'
        _ = 3001 ^ (S t x + 1) * x := by ring

/-- **Rasgo 1 para toda fuga, pura o no** ((2.31) de Lagarias, 1985, en cifras): una órbita
    que crece sin límite termina subiendo en al menos 63 de cada 100 pasos, salvo una
    constante. Vale, en particular, para una grieta cuya órbita escapa. -/
theorem fuga_sube {n : ℕ} (hf : Fuga n) :
    ∃ K C, ∀ k, K ≤ k → 63 * (k - K) ≤ 100 * (S k n - S K n) + C := by
  obtain ⟨K, hK⟩ := fuga_tiende hf 999
  set x := T^[K] n with hx
  refine ⟨K, 63 * x, fun k hk => ?_⟩
  obtain ⟨t, rfl⟩ : ∃ t, k = K + t := ⟨k - K, by omega⟩
  have hS : S (K + t) n - S K n = S t x := by
    rw [S_add, ← hx]
    omega
  rw [hS, show K + t - K = t by omega]
  have halto : ∀ i, i < t → 1000 ≤ T^[i] x := by
    intro i _
    have := hK (K + i) (by omega)
    rw [hx, ← Function.iterate_add_apply, add_comm]
    omega
  have h1 := crecimiento_alto t halto
  have hpos : 1 ≤ T^[t] x := by
    have := hK (K + t) (by omega)
    rw [hx, ← Function.iterate_add_apply, add_comm]
    omega
  set a := S t x
  have h2 : 1000 ^ a * 2 ^ t ≤ 3001 ^ a * x :=
    le_trans (Nat.le_mul_of_pos_right _ hpos) h1
  have h3 : (1000 ^ a * 2 ^ t) ^ 63 ≤ (3001 ^ a * x) ^ 63 := Nat.pow_le_pow_left h2 63
  have h3' : 1000 ^ (63 * a) * 2 ^ (63 * t) ≤ 3001 ^ (63 * a) * x ^ 63 := by
    rw [mul_pow, mul_pow, ← pow_mul, ← pow_mul, ← pow_mul] at h3
    rw [mul_comm 63 a, mul_comm 63 t]
    exact h3
  have h4 : (3001 : ℕ) ^ 63 ≤ 2 ^ 100 * 1000 ^ 63 := by norm_num
  have h5 : 3001 ^ (63 * a) ≤ 2 ^ (100 * a) * 1000 ^ (63 * a) := by
    rw [pow_mul, pow_mul, pow_mul, ← mul_pow]
    exact Nat.pow_le_pow_left h4 a
  have h6 : x ^ 63 < 2 ^ (63 * x) := by
    rw [mul_comm, pow_mul]
    exact Nat.pow_lt_pow_left Nat.lt_two_pow_self (by norm_num)
  have h7 : 1000 ^ (63 * a) * 2 ^ (63 * t) < 1000 ^ (63 * a) * 2 ^ (100 * a + 63 * x) := by
    calc 1000 ^ (63 * a) * 2 ^ (63 * t) ≤ 3001 ^ (63 * a) * x ^ 63 := h3'
      _ ≤ 2 ^ (100 * a) * 1000 ^ (63 * a) * x ^ 63 := Nat.mul_le_mul_right _ h5
      _ < 2 ^ (100 * a) * 1000 ^ (63 * a) * 2 ^ (63 * x) :=
          Nat.mul_lt_mul_of_pos_left h6 (by positivity)
      _ = 1000 ^ (63 * a) * 2 ^ (100 * a + 63 * x) := by rw [pow_add]; ring
  have h8 : 2 ^ (63 * t) < 2 ^ (100 * a + 63 * x) :=
    Nat.lt_of_mul_lt_mul_left h7
  have h9 := (Nat.pow_lt_pow_iff_right (by norm_num)).1 h8
  omega

/-- **El retrato de la grieta**: nunca baja de sí misma, no llega a 1, su órbita cae en un
    circuito o crece sin límite, y cruza tarde. Además, casi ningún número baja nunca
    (`casi_todo_desciende`). -/
theorem retrato_grieta {n : ℕ} (h : Grieta n) :
    (∀ k, n ≤ T^[k] n) ∧ ¬ LlegaT n ∧ ((∃ i, Circuito (T^[i] n)) ∨ Fuga n) ∧
      ∃ k, PrimerCruce n k ∧ 2 ≤ k ∧ 3 * n ≤ S k n * 3 ^ S k n ∧ 3 * n < k * 2 ^ k :=
  ⟨grieta_no_baja h, grieta_no_llega h,
    dos_fallas (le_trans (by norm_num) h.1) (grieta_no_llega h), grieta_tarde h⟩

end CasaGrieta

#print axioms CasaGrieta.muroA_iff_sin_grietas
#print axioms CasaGrieta.desciende_de_cruce
#print axioms CasaGrieta.desciende_si_grande
#print axioms CasaGrieta.chico_si_no_baja
#print axioms CasaGrieta.primer_cruce_antes
#print axioms CasaGrieta.cuenta_sin_descenso_bloques
#print axioms CasaGrieta.cuenta_sin_descenso
#print axioms CasaGrieta.casi_todo_desciende
#print axioms CasaGrieta.margen_lmn
#print axioms CasaGrieta.desciende_lmn
#print axioms CasaGrieta.teorema_E_lmn
#print axioms CasaGrieta.quince_exp
#print axioms CasaGrieta.desciende_rhin
#print axioms CasaGrieta.teorema_E_rhin
#print axioms CasaGrieta.grieta_no_baja
#print axioms CasaGrieta.grieta_no_llega
#print axioms CasaGrieta.grieta_tarde
#print axioms CasaGrieta.grieta_lmn
#print axioms CasaGrieta.grieta_rhin
#print axioms CasaGrieta.circuito_tiene_grieta
#print axioms CasaGrieta.crias_sin_muroA
#print axioms CasaGrieta.sin_retorno_raros
#print axioms CasaGrieta.rachas_mono
#print axioms CasaGrieta.circuito_exige_25
#print axioms CasaGrieta.fuga_tiende
#print axioms CasaGrieta.crecimiento_alto
#print axioms CasaGrieta.fuga_sube
#print axioms CasaGrieta.retrato_grieta
