import OcelotasContador

/-! # Ocelotas aplicada a ciclos: calibración contra los m-ciclos

Si la CST vale para toda palabra con a lo sumo `R` rachas, ningún ciclo no
trivial del atajo tiene a lo sumo `R` rachas impares (contadas sobre el ciclo,
es decir, sus `m` mínimos locales en el sentido de Simons-de Weger y Hercher).

Idea: el mínimo `m` de un ciclo nunca baja de sí mismo, pero al dar la vuelta
completa el coeficiente `3^S/2^L` ya es menor que 1. Luego `m` tiene primer
cruce finito sin descenso, y su palabra hasta ese cruce es un prefijo del ciclo.
-/

namespace OcelotasCiclos

open Ocelotas OcelotasContador

/-- La CST para palabras de a lo sumo `R` rachas (forma de `descenso_contador`). -/
def CSTHasta (R : ℕ) : Prop :=
  ∀ {n k : ℕ}, 2 ≤ n → PrimerCruce n k → rachas n k ≤ R → T^[k] n < n

/-- `j` inicia una racha impar del ciclo de longitud `L` que pasa por `n`. -/
def inicio (n L j : ℕ) : ℕ :=
  if T^[j] n % 2 = 1 ∧ T^[j + L - 1] n % 2 = 0 then 1 else 0

/-- Rachas impares de un ciclo de longitud `L`, contadas cíclicamente. -/
def rachasCiclicas (n L : ℕ) : ℕ := ∑ j ∈ Finset.range L, inicio n L j

theorem periodo {n L : ℕ} (hc : T^[L] n = n) (j : ℕ) : T^[j + L] n = T^[j] n := by
  rw [Nat.add_comm, iter_add, hc]

theorem periodo_mod {n L : ℕ} (hc : T^[L] n = n) (j : ℕ) : T^[j] n = T^[j % L] n := by
  conv_lhs => rw [← Nat.mod_add_div j L]
  generalize j / L = q
  induction q with
  | zero => simp
  | succ q ih => rw [Nat.mul_succ, ← Nat.add_assoc, periodo hc, ih]

theorem suma_rotada (f : ℕ → ℕ) (L : ℕ) (hf : ∀ j, f (j + L) = f j) (i : ℕ) :
    ∑ j ∈ Finset.range L, f (i + j) = ∑ j ∈ Finset.range L, f j := by
  induction i with
  | zero => simp
  | succ i ih =>
    have h1 := Finset.sum_range_succ' (fun j => f (i + j)) L
    have h2 := Finset.sum_range_succ (fun j => f (i + j)) L
    have h3 : f (i + L) = f (i + 0) := by rw [hf, Nat.add_zero]
    have h4 : ∑ j ∈ Finset.range L, f (i + 1 + j) = ∑ j ∈ Finset.range L, f (i + (j + 1)) :=
      Finset.sum_congr rfl (fun j _ => by rw [Nat.add_assoc, Nat.add_comm 1 j])
    omega

theorem inicio_periodo {n L : ℕ} (hc : T^[L] n = n) (j : ℕ) :
    inicio n L (j + L) = inicio n L j := by
  unfold inicio
  rw [show j + L + L - 1 = (j + L - 1) + L by omega]
  simp only [periodo hc]

/-- El recuento cíclico no depende del punto del ciclo desde el que se cuenta. -/
theorem rotar {n L : ℕ} (hL : 1 ≤ L) (hc : T^[L] n = n) (i : ℕ) :
    rachasCiclicas (T^[i] n) L = rachasCiclicas n L := by
  unfold rachasCiclicas
  have h : ∀ j, inicio (T^[i] n) L j = inicio n L (i + j) := by
    intro j
    unfold inicio
    rw [← iter_add, ← iter_add, show i + (j + L - 1) = i + j + L - 1 by omega]
  simp only [h]
  exact suma_rotada (inicio n L) L (inicio_periodo hc) i

theorem rachas_mono (n : ℕ) : Monotone (rachas n) :=
  monotone_nat_of_le_succ (fun k => by simp only [rachas]; omega)

/-- Si la CST vale hasta `R` rachas, todo ciclo no trivial tiene más de `R`. -/
theorem ciclo_exige {R : ℕ} (hC : CSTHasta R) {n L : ℕ} (hL : 1 ≤ L)
    (hc : T^[L] n = n) (hno : ∀ j, 2 ≤ T^[j] n) : R < rachasCiclicas n L := by
  -- El mínimo del ciclo.
  have hne : (Finset.image (fun j => T^[j] n) (Finset.range L)).Nonempty :=
    Finset.image_nonempty.mpr (Finset.nonempty_range_iff.mpr (by omega))
  obtain ⟨i, _, him⟩ := Finset.mem_image.mp (Finset.min'_mem _ hne)
  have hmin0 : ∀ j, T^[i] n ≤ T^[j] n := by
    intro j
    rw [periodo_mod hc j]
    calc T^[i] n = _ := him
      _ ≤ T^[j % L] n := Finset.min'_le _ _ (Finset.mem_image.mpr
            ⟨j % L, Finset.mem_range.mpr (Nat.mod_lt _ (by omega)), rfl⟩)
  have hmin : ∀ j, T^[i] n ≤ T^[j] (T^[i] n) := fun j => by rw [← iter_add]; exact hmin0 _
  have hcm : T^[L] (T^[i] n) = T^[i] n := by rw [← iter_add, periodo hc]
  have h2 := hno i
  rw [← rotar hL hc i]
  generalize T^[i] n = m at h2 hmin hcm ⊢
  have hper : ∀ j, T^[j + L] m = T^[j] m := periodo hcm
  -- Tras la vuelta completa el coeficiente ya es menor que 1.
  have hcoef : 3 ^ S L m < 2 ^ L := by
    have h := cota_inferior m L
    rw [hcm] at h
    have hle : 3 ^ S L m ≤ 2 ^ L := Nat.le_of_mul_le_mul_right h (by omega)
    have hne : 3 ^ S L m ≠ 2 ^ L := (par_ne_impar (pot2_par hL) (pot3_impar _)).symm
    omega
  -- Primer cruce del mínimo.
  have hex : ∃ k, 1 ≤ k ∧ 3 ^ S k m < 2 ^ k := ⟨L, hL, hcoef⟩
  have hkspec := Nat.find_spec hex
  have hkL : Nat.find hex ≤ L := Nat.find_min' hex ⟨hL, hcoef⟩
  have hpc : PrimerCruce m (Nat.find hex) := by
    refine ⟨fun j hj h1 => ?_, hkspec.2⟩
    have := Nat.find_min hex hj
    simp only [not_and, not_lt] at this
    exact this h1
  have hr : R < rachas m (Nat.find hex) := by
    by_contra h
    have hd := hC h2 hpc (by omega)
    have := hmin (Nat.find hex)
    omega
  -- El predecesor del mínimo en el ciclo es par.
  have hpred : m % 2 = 1 → T^[L - 1] m % 2 = 0 := by
    intro _
    by_contra hp
    have hp1 : T^[L - 1] m % 2 = 1 := by omega
    have hT : T (T^[L - 1] m) = m := by
      have : T^[L] m = T (T^[L - 1] m) := by
        obtain ⟨L', rfl⟩ : ∃ L', L = L' + 1 := ⟨L - 1, by omega⟩
        simp [Function.iterate_succ_apply']
      rw [← this, hcm]
    have h2T := T_impar hp1
    rw [hT] at h2T
    have := hmin (L - 1)
    omega
  -- Contar desde el mínimo coincide con el recuento cíclico.
  have heq : rachas m L = rachasCiclicas m L := by
    rw [rachas_eq_card, Finset.card_filter]
    unfold rachasCiclicas
    refine Finset.sum_congr rfl (fun j _ => ?_)
    unfold inicio
    rcases Nat.eq_zero_or_pos j with rfl | hjpos
    · by_cases hodd : m % 2 = 1
      · have := hpred hodd
        simp [hodd, this]
      · simp [hodd]
    · rw [show j + L - 1 = (j - 1) + L by omega, hper]
      simp [show j ≠ 0 by omega]
  have hmono := rachas_mono m hkL
  omega

end OcelotasCiclos

#print axioms OcelotasCiclos.ciclo_exige
