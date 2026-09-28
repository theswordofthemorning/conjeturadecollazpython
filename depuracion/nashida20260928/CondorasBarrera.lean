import Condoras

/-!
# Condoras: puente condicional desde una barrera finita

Mapa clásico `GarnerEnunciado.C`, enteros positivos y tiempos naturales desde cero.
Conteos exactos sobre `[1, X]`; `rho` y `dWu` conservan `[1, M)` y divisor `M - 1`.
No hay ley aleatoria ni condicionamiento probabilístico.

Se demuestra una implicación. `CotaBarrera error` y `Cubierta B` son hipótesis
explícitas; no se importa ni se demuestra el teorema externo de Nashida.
La barrera es estricta en `SobreBarrera` e inclusiva en `Cubierta`.
El perfil `error` es arbitrario: Nashida correspondería a `error B = K B^(-c)`.
-/

open Filter Topology Classical
open GarnerEnunciado CondorasWu

namespace CondorasBarrera

def Cubierta (B : ℕ) : Prop := ∀ n, 1 ≤ n → n ≤ B → llega n

def SobreBarrera (B n : ℕ) : Prop := ∀ j, B < C^[j] n

open Classical in
noncomputable def excepciones (B X : ℕ) : ℕ :=
  ((Finset.Icc 1 X).filter (SobreBarrera B)).card

def CotaBarrera (error : ℕ → ℝ) : Prop :=
  ∀ B : ℕ, 1 ≤ B → ∀ X : ℕ,
    (excepciones B X : ℝ) ≤ error B * X

theorem no_llega_iff_sobre {B n : ℕ} (hB : 1 ≤ B) (hc : Cubierta B)
    (hn : 1 ≤ n) : ¬ llega n ↔ SobreBarrera B n := by
  constructor
  · intro hno j
    by_contra! hmenor
    have hpos : 1 ≤ C^[j] n := by
      have h := Hienas.cota_inferior j n
      change n ≤ 2 ^ j * C^[j] n at h
      by_contra! hzero
      have hz : C^[j] n = 0 := by omega
      rw [hz, Nat.mul_zero] at h
      omega
    obtain ⟨k, hk⟩ := hc (C^[j] n) hpos hmenor
    apply hno
    refine ⟨k + j, ?_⟩
    rw [Function.iterate_add_apply]
    exact hk
  · intro hs hl
    obtain ⟨j, hj⟩ := hl
    have h := hs j
    rw [hj] at h
    omega

theorem cuenta_complementaria {B : ℕ} (hB : 1 ≤ B) (hc : Cubierta B) (M : ℕ) :
    ((Finset.Ico 1 M).filter llega).card + excepciones B (M - 1) = M - 1 := by
  classical
  have hs : Finset.Icc 1 (M - 1) = Finset.Ico 1 M := by
    ext n
    simp only [Finset.mem_Icc, Finset.mem_Ico]
    omega
  have he : (Finset.Ico 1 M).filter (SobreBarrera B) =
      (Finset.Ico 1 M).filter (fun n => ¬ llega n) := by
    apply Finset.filter_congr
    intro n hn
    exact (no_llega_iff_sobre hB hc (Finset.mem_Ico.mp hn).1).symm
  unfold excepciones
  rw [hs, he, Finset.card_filter_add_card_filter_not]
  simp

theorem cota_rho {B M : ℕ} {error : ℕ → ℝ} (hB : 1 ≤ B) (hc : Cubierta B)
    (hN : CotaBarrera error) (hM : 2 ≤ M) :
    1 - error B ≤ rho M := by
  classical
  have hm : (0 : ℝ) < (M : ℝ) - 1 := by
    have h : (1 : ℝ) < M := by exact_mod_cast (by omega : 1 < M)
    linarith
  have hcast : ((M - 1 : ℕ) : ℝ) = (M : ℝ) - 1 := by
    rw [Nat.cast_sub (by omega), Nat.cast_one]
  have hcuenta : (((Finset.Ico 1 M).filter llega).card : ℝ) +
      (excepciones B (M - 1) : ℝ) = ((M - 1 : ℕ) : ℝ) := by
    exact_mod_cast cuenta_complementaria hB hc M
  have hbound := hN B hB (M - 1)
  rw [hcast] at hcuenta hbound
  unfold rho
  rw [le_div_iff₀ hm]
  nlinarith

theorem cota_finita_dWu {B M : ℕ} {error : ℕ → ℝ} (hB : 1 ≤ B) (hc : Cubierta B)
    (hN : CotaBarrera error) (hM : 2 ≤ M) :
    1 - error B -
      ((M : ℝ) - (((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card : ℝ)) /
        ((M : ℝ) - 1) ≤ dWu M := by
  classical
  have hm : (0 : ℝ) < (M : ℝ) - 1 := by
    have h : (1 : ℝ) < M := by exact_mod_cast (by omega : 1 < M)
    linarith
  have hpaso : rho M ≤ dWu M +
      ((M : ℝ) - (((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card : ℝ)) /
        ((M : ℝ) - 1) := by
    unfold rho dWu
    simpa only [add_div] using
      div_le_div_of_nonneg_right (CondorasWu.cota_llegan M) hm.le
  have h := cota_rho hB hc hN hM
  linarith

/-- Forma eventual de `liminf dWu ≥ 1 - error B`; la cota externa sigue siendo hipótesis. -/
theorem cota_eventual_dWu {B : ℕ} {error : ℕ → ℝ} (hB : 1 ≤ B) (hc : Cubierta B)
    (hN : CotaBarrera error) (ε : ℝ) (hε : 0 < ε) :
    ∀ᶠ M in atTop, 1 - error B - ε ≤ dWu M := by
  have hdif := CondorasWu.diferencia GaoLiteral.conjetura_gao_literal.2
  rw [Metric.tendsto_atTop] at hdif
  obtain ⟨N, hN0⟩ := hdif ε hε
  filter_upwards [eventually_ge_atTop (max N 2)] with M hM
  have hM2 : 2 ≤ M := le_trans (le_max_right _ _) hM
  have habs := hN0 M (le_trans (le_max_left _ _) hM)
  simp only [Real.dist_eq, sub_zero] at habs
  have hr := cota_rho hB hc hN hM2
  linarith [(abs_lt.mp habs).2]

end CondorasBarrera

set_option pp.fullNames true

#print axioms CondorasBarrera.no_llega_iff_sobre
#print axioms CondorasBarrera.cuenta_complementaria
#print axioms CondorasBarrera.cota_rho
#print axioms CondorasBarrera.cota_finita_dWu
#print axioms CondorasBarrera.cota_eventual_dWu
#check @CondorasBarrera.cota_eventual_dWu
