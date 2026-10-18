import WuEnunciado

/-! # La altura con el atajo T de Garner

Garner (1985, pág. 57) usa `T(n) = n/2` si n es par y `(3n+1)/2` si es impar, y define
«The height of n ∈ ℕ is the least k such that T^k(n) = 1»; su Fig. 1 lleva el 12 a 1 en 7
pasos. Wu (1992) muy probablemente usa la misma T. `GarnerEnunciado` y `WuEnunciado` usan
el mapa clásico. Este módulo enuncia las conjeturas con T y las deduce de las clásicas.

* `puente`: si n tiene altura clásica h, su altura T es `mitades n h` (σ∞ de Gao). Cada
  paso de T es una división por 2, precedida o no de un 3n+1.
* `conjetura_garner_T`: rachas arbitrariamente largas de igual altura T.
* `conjetura_wu_dos_T`: `lim L = ∞` con la altura T.
* `conjetura_wu_uno_T`: `lim d(M) = 1` con la altura T equivale al mismo problema abierto
  que la versión clásica: que los que llegan a 1 tengan densidad natural 1. -/

open Filter Topology

namespace AlturaT

open GarnerEnunciado

/-- Atajo de Garner: n/2 si n es par, (3n+1)/2 si es impar. -/
def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- Altura de Garner: h es el mínimo número de pasos con `T^(h)(n) = 1`. -/
def alturaT (n h : ℕ) : Prop := T^[h] n = 1 ∧ ∀ k, k < h → T^[k] n ≠ 1

instance (n h : ℕ) : Decidable (alturaT n h) := by unfold alturaT; infer_instance

/-! ## El puente entre las dos alturas -/

theorem mitades_succ (n h : ℕ) :
    mitades n (h + 1) = (if n % 2 = 0 then 1 else 0) + mitades (C n) h := by
  unfold mitades
  rw [Finset.card_filter, Finset.card_filter, Finset.sum_range_succ']
  simp only [Function.iterate_succ_apply, Function.iterate_zero_apply]
  exact add_comm _ _

theorem altura_succ {n h : ℕ} (hn : altura n (h + 1)) : altura (C n) h := by
  refine ⟨?_, fun k hk => ?_⟩
  · rw [← Function.iterate_succ_apply]; exact hn.1
  · rw [← Function.iterate_succ_apply]; exact hn.2 (k + 1) (by omega)

theorem alturaT_succ {n s : ℕ} (hn : n ≠ 1) (hs : alturaT (T n) s) : alturaT n (s + 1) := by
  refine ⟨by rw [Function.iterate_succ_apply]; exact hs.1, fun k hk => ?_⟩
  rcases k with _ | k
  · exact hn
  · rw [Function.iterate_succ_apply]; exact hs.2 k (by omega)

/-- Altura clásica h ⇒ altura T igual a las divisiones por 2 de esos h pasos. -/
theorem puente : ∀ h n, altura n h → alturaT n (mitades n h) := by
  intro h
  induction h using Nat.strong_induction_on with
  | _ h ih =>
    intro n hn
    rcases h with _ | h
    · have h1 : n = 1 := hn.1
      subst h1
      exact ⟨rfl, fun k hk => absurd hk (Nat.not_lt_zero k)⟩
    · have hn1 : n ≠ 1 := hn.2 0 (Nat.succ_pos h)
      have hC := altura_succ hn
      by_cases hp : n % 2 = 0
      · have hT : T n = C n := by simp only [T, C, if_pos hp]
        rw [mitades_succ, if_pos hp, add_comm]
        exact alturaT_succ hn1 (hT ▸ ih h (by omega) (C n) hC)
      · rcases h with _ | h
        · exfalso
          have e := hC.1
          simp only [Function.iterate_zero_apply, C, if_neg hp] at e
          omega
        · have h3 : (3 * n + 1) % 2 = 0 := by omega
          have hT : T n = C (C n) := by simp only [T, C, if_neg hp, if_pos h3]
          have hCn : C n % 2 = 0 := by simp only [C, if_neg hp]; exact h3
          rw [mitades_succ, if_neg hp, mitades_succ, if_pos hCn, zero_add, add_comm]
          exact alturaT_succ hn1 (hT ▸ ih h (by omega) (C (C n)) (altura_succ hC))

/-- Cada iterado de T es un iterado del mapa clásico. -/
theorem iterado_T : ∀ k n, ∃ m, T^[k] n = C^[m] n := by
  intro k
  induction k with
  | zero => exact fun n => ⟨0, rfl⟩
  | succ k ih =>
    intro n
    obtain ⟨m, hm⟩ := ih (T n)
    rw [Function.iterate_succ_apply, hm]
    by_cases hp : n % 2 = 0
    · refine ⟨m + 1, ?_⟩
      rw [Function.iterate_succ_apply]
      simp only [T, C, if_pos hp]
    · refine ⟨m + 2, ?_⟩
      have h3 : (3 * n + 1) % 2 = 0 := by omega
      rw [Function.iterate_succ_apply, Function.iterate_succ_apply]
      simp only [T, C, if_neg hp, if_pos h3]

/-- n llega a 1 con T. -/
def llegaT (n : ℕ) : Prop := ∃ h, T^[h] n = 1

/-- Llegar a 1 con T es llegar a 1 con el mapa clásico. -/
theorem llegaT_iff (n : ℕ) : llegaT n ↔ CondorasWu.llega n := by
  constructor
  · rintro ⟨k, hk⟩
    obtain ⟨m, hm⟩ := iterado_T k n
    exact ⟨m, hm ▸ hk⟩
  · intro hl
    have hl' : ∃ h, C^[h] n = 1 := hl
    exact ⟨_, (puente (Nat.find hl') n
      ⟨Nat.find_spec hl', fun k hk => Nat.find_min hl' hk⟩).1⟩

/-! ## Garner con la altura T -/

/-- La conjetura (2) de Garner (1985, pág. 58) con su propia altura: para cada L hay
    L+1 consecutivos n, …, n+L, con n tan grande como se quiera, de igual altura T. -/
def FormaGarnerT : Prop := ∀ L N : ℕ, ∃ n h : ℕ, N ≤ n ∧ ∀ i, i ≤ L → alturaT (n + i) h

theorem conjetura_garner_T : FormaGarnerT := by
  intro L N
  obtain ⟨n, h, s, hN, hi⟩ := conjetura_garner L N
  refine ⟨n, s, hN, fun i hiL => ?_⟩
  obtain ⟨ha, hm⟩ := hi i hiL
  rw [← hm]
  exact puente h (n + i) ha

/-! ## Wu con la altura T -/

/-- n está en una upla de Wu con la altura T: comparte altura T con n − 1 o con n + 1. -/
def enUplaT (n : ℕ) : Prop := ∃ h, alturaT n h ∧ (alturaT (n - 1) h ∨ alturaT (n + 1) h)

open Classical in
/-- `d(M) = K/(M − 1)` con la altura T. -/
noncomputable def dT (M : ℕ) : ℝ :=
  (((Finset.Ico 1 M).filter enUplaT).card : ℝ) / ((M : ℝ) - 1)

/-- Hay k consecutivos de igual altura T dentro de [1, M). -/
def uplaEnT (M k : ℕ) : Prop := ∃ n h, 1 ≤ n ∧ n + k ≤ M ∧ ∀ i, i < k → alturaT (n + i) h

/-- `L(M)` con la altura T: la upla más larga dentro de [1, M). -/
noncomputable def LT (M : ℕ) : ℕ := sSup {k | uplaEnT M k}

open Classical in
/-- Proporción de [1, M) que llega a 1 con T, normalizada como d. -/
noncomputable def proporcionLleganT (M : ℕ) : ℝ :=
  (((Finset.Ico 1 M).filter llegaT).card : ℝ) / ((M : ℝ) - 1)

theorem acotadoT (M : ℕ) : BddAbove {k | uplaEnT M k} := by
  refine ⟨M, ?_⟩
  rintro k ⟨n, h, hn, hk, -⟩
  omega

/-- Conjetura 2 de Wu con la altura T: `lim L = ∞`. -/
theorem conjetura_wu_dos_T : Tendsto LT atTop atTop := by
  rw [Filter.tendsto_atTop_atTop]
  intro K
  rcases Nat.eq_zero_or_pos K with rfl | hK
  · exact ⟨0, fun _ _ => Nat.zero_le _⟩
  obtain ⟨n, h, hn, hi⟩ := conjetura_garner_T (K - 1) 1
  exact ⟨n + K, fun M hM => le_csSup (acotadoT M) ⟨n, h, hn, hM, fun i hik => hi i (by omega)⟩⟩

theorem mitades_add (j r : ℕ) : ∀ x, mitades x (j + r) = mitades x j + mitades (C^[j] x) r := by
  induction j with
  | zero => intro x; simp [mitades]
  | succ j ih =>
    intro x
    rw [show j + 1 + r = (j + r) + 1 by omega, mitades_succ, ih, mitades_succ,
      Function.iterate_succ_apply]
    omega

theorem mitades_hienas : ∀ j x, mitades x j = Hienas.mitades j x := by
  intro j
  induction j with
  | zero => intro x; simp [mitades, Hienas.mitades]
  | succ j ih =>
    intro x
    rw [mitades_succ, ih]
    rfl

/-- Si n llega a 1 y coalesce con n+1 en el sentido de Gao, los dos tienen la misma
    altura clásica y las mismas mitades, y por eso la misma altura T. -/
theorem uplaT_de_coalescencia {n j : ℕ} (hl : CondorasWu.llega n) (hc : Hienas.coalescen n j) :
    enUplaT n := by
  have hC : Hienas.C = C := rfl
  obtain ⟨he, hmj, hs⟩ := hc
  rw [hC] at he hs
  have hl' : ∃ h, C^[h] n = 1 := hl
  obtain ⟨h, hh, hmin⟩ : ∃ h, C^[h] n = 1 ∧ ∀ k, k < h → C^[k] n ≠ 1 :=
    ⟨Nat.find hl', Nat.find_spec hl', fun k hk => Nat.find_min hl' hk⟩
  have hjh : j < h := by
    by_contra hcon
    exact (hs h (by omega)).1 hh
  have ha1 : altura (n + 1) h := by
    refine ⟨?_, ?_⟩
    · have e : C^[h] (n + 1) = C^[h - j] (C^[j] (n + 1)) := by
        rw [← Function.iterate_add_apply, Nat.sub_add_cancel hjh.le]
      rw [e, ← he, ← Function.iterate_add_apply, Nat.sub_add_cancel hjh.le, hh]
    · intro k hk
      by_cases hkj : k ≤ j
      · exact (hs k hkj).2
      · have hjk : j ≤ k := by omega
        have e : C^[k] (n + 1) = C^[k - j] (C^[j] (n + 1)) := by
          rw [← Function.iterate_add_apply, Nat.sub_add_cancel hjk]
        rw [e, ← he, ← Function.iterate_add_apply, Nat.sub_add_cancel hjk]
        exact hmin k hk
  have hm : mitades n h = mitades (n + 1) h := by
    have e1 := mitades_add j (h - j) n
    have e2 := mitades_add j (h - j) (n + 1)
    rw [Nat.add_sub_of_le hjh.le] at e1 e2
    rw [e1, e2, mitades_hienas j n, mitades_hienas j (n + 1), hmj, he]
  refine ⟨mitades n h, puente h n ⟨hh, hmin⟩, Or.inr ?_⟩
  rw [hm]
  exact puente h (n + 1) ha1

theorem llega_de_uplaT {n : ℕ} (h : enUplaT n) : CondorasWu.llega n := by
  obtain ⟨k, hk, -⟩ := h
  exact (llegaT_iff n).1 ⟨k, hk.1⟩

open Classical in
/-- Los que llegan a 1 sin estar en una upla T no coalescen con su siguiente. -/
theorem cota_lleganT (M : ℕ) :
    (((Finset.Ico 1 M).filter CondorasWu.llega).card : ℝ) ≤
      (((Finset.Ico 1 M).filter enUplaT).card : ℝ) +
        ((M : ℝ) - (((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card : ℝ)) := by
  have hGsub : (Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j) ⊆ Finset.range M :=
    Finset.filter_subset _ _
  have hsub : (Finset.Ico 1 M).filter CondorasWu.llega ⊆ (Finset.Ico 1 M).filter enUplaT ∪
      (Finset.range M \ (Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)) := by
    intro n hn
    rw [Finset.mem_filter, Finset.mem_Ico] at hn
    rw [Finset.mem_union, Finset.mem_sdiff]
    by_cases hc : ∃ j, Hienas.coalescen n j
    · left
      obtain ⟨j, hj⟩ := hc
      exact Finset.mem_filter.2 ⟨Finset.mem_Ico.2 hn.1, uplaT_de_coalescencia hn.2 hj⟩
    · right
      exact ⟨Finset.mem_range.2 hn.1.2, fun hG => hc (Finset.mem_filter.1 hG).2⟩
  have hcard := Finset.card_le_card hsub
  have hu := Finset.card_union_le ((Finset.Ico 1 M).filter enUplaT)
    (Finset.range M \ (Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j))
  have hsd := Finset.card_sdiff_of_subset hGsub
  rw [Finset.card_range] at hsd
  have hGM : ((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card ≤ M := by
    calc _ ≤ (Finset.range M).card := Finset.card_le_card hGsub
      _ = M := Finset.card_range M
  have hnat : ((Finset.Ico 1 M).filter CondorasWu.llega).card ≤
      ((Finset.Ico 1 M).filter enUplaT).card +
      (M - ((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card) := by
    omega
  have hr : ((((Finset.Ico 1 M).filter enUplaT).card +
      (M - ((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card) : ℕ) : ℝ) =
      (((Finset.Ico 1 M).filter enUplaT).card : ℝ) +
        ((M : ℝ) - (((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card : ℝ)) := by
    rw [Nat.cast_add, Nat.cast_sub hGM]
  rw [← hr]
  exact_mod_cast hnat

open Classical in
/-- Con `d(x) → 1` de Gao, la densidad de Wu con T y la de los que llegan a 1 se acercan. -/
theorem diferenciaT (hD : Hienas.FormaGaoD) :
    Tendsto (fun M => CondorasWu.rho M - dT M) atTop (𝓝 0) := by
  unfold Hienas.FormaGaoD at hD
  rw [Metric.tendsto_atTop] at hD ⊢
  intro ε hε
  obtain ⟨N0, hN0⟩ := hD (ε / 4) (by linarith)
  refine ⟨max N0 2, fun M hM => ?_⟩
  have hM2 : (2 : ℝ) ≤ M := by exact_mod_cast le_trans (le_max_right _ _) hM
  have hdM := hN0 M (le_trans (le_max_left _ _) hM)
  rw [Real.dist_eq] at hdM
  rw [Real.dist_eq, sub_zero]
  have hAB : (((Finset.Ico 1 M).filter enUplaT).card : ℝ) ≤
      ((Finset.Ico 1 M).filter CondorasWu.llega).card := by
    exact_mod_cast Finset.card_le_card (fun n hn => by
      rw [Finset.mem_filter] at hn ⊢
      exact ⟨hn.1, llega_de_uplaT hn.2⟩)
  have e : CondorasWu.rho M - dT M = ((((Finset.Ico 1 M).filter CondorasWu.llega).card : ℝ) -
      ((Finset.Ico 1 M).filter enUplaT).card) / ((M : ℝ) - 1) := by
    unfold CondorasWu.rho dT
    rw [sub_div]
  have hd : Hienas.d M =
      (((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card : ℝ) / M := rfl
  rw [hd] at hdM
  rw [e]
  exact CondorasWu.cota_real hM2 hε hAB (cota_lleganT M) hdM

open Classical in
/-- La proporción de los que llegan a 1 es la misma con T y con el mapa clásico. -/
theorem proporciones_iguales : proporcionLleganT = WuEnunciado.proporcionLlegan := by
  funext M
  unfold proporcionLleganT WuEnunciado.proporcionLlegan
  congr 3
  exact Finset.filter_congr (fun n _ => llegaT_iff n)

/-- Conjetura 1 de Wu con la altura T, reducida como la clásica: `lim d(M) = 1` si y sólo
    si los que llegan a 1 tienen densidad natural 1 (problema abierto). -/
theorem conjetura_wu_uno_T :
    Tendsto dT atTop (𝓝 1) ↔ Tendsto proporcionLleganT atTop (𝓝 1) := by
  have hdif := diferenciaT GaoLiteral.conjetura_gao_literal.2
  have hr : proporcionLleganT = CondorasWu.rho := proporciones_iguales
  rw [hr]
  constructor
  · intro h
    simpa using h.add hdif
  · intro h
    simpa using h.sub hdif

/-- Las dos versiones de la conjetura 1 de Wu son el mismo problema abierto. -/
theorem wu_uno_T_iff_clasica :
    Tendsto dT atTop (𝓝 1) ↔ Tendsto WuEnunciado.d atTop (𝓝 1) := by
  rw [conjetura_wu_uno_T, proporciones_iguales, WuEnunciado.conjetura_wu_uno]

end AlturaT

#print axioms AlturaT.puente
#print axioms AlturaT.conjetura_garner_T
#print axioms AlturaT.conjetura_wu_dos_T
#print axioms AlturaT.conjetura_wu_uno_T
#print axioms AlturaT.wu_uno_T_iff_clasica

/- Cotejo con Garner (1985), Fig. 1: el 12 tiene altura T 7 (12, 6, 3, 5, 8, 4, 2, 1). Las
   rachas de Gao y Penning tienen altura T igual a su σ∞: 26, 40 y 54. La racha récord de
   Wu, 176 consecutivos desde 722 067 240, también lo es con T: altura T 128, y sus dos
   vecinos tienen 120. Si alguna cuenta no coincide, el archivo no compila. -/
#guard decide (AlturaT.alturaT 12 7)
#guard (List.range 7).all (fun i => decide (AlturaT.alturaT (943 + i) 26))
#guard (List.range 17).all (fun i => decide (AlturaT.alturaT (7083 + i) 40))
#guard (List.range 25).all (fun i => decide (AlturaT.alturaT (57346 + i) 54))
#guard (List.range 176).all (fun i => decide (AlturaT.alturaT (722067240 + i) 128)) &&
  !decide (AlturaT.alturaT 722067239 128) && !decide (AlturaT.alturaT 722067416 128)
