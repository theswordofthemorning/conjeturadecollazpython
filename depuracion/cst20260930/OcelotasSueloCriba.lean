import OcelotasSueloRachas
import OcelotasContador

/-! # Criba que conserva la reducción de los bloques pares

C_(j+1)=floor(beta+alfa*C_j-gamma*j). Gamma acota por abajo
log_2((2N+1)/(N+1)); N es un suelo de los comienzos de los bloques.
La cota se aplica al primer cruce sin suponer que el valor final sea >=N.
-/

namespace OcelotasSueloCriba

open Real Ocelotas OcelotasTrayectorias OcelotasContador

noncomputable def cota (alfa beta gamma : ℝ) : ℕ → ℕ
  | 0 => 0
  | i + 1 => Nat.floor (beta + alfa * cota alfa beta gamma i - gamma * i)

theorem criba_congruencias (A : ℕ → ℕ) {n s r N : ℕ} {alfa beta gamma : ℝ}
    (hs : 0 < s) (hn : n + 1 ≤ s) (h0 : A 0 = 0) (ha : 0 ≤ alfa)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2)
    (hgamma : gamma * log 2 ≤ log (2 * N + 1) - log (N + 1))
    (hc : ∀ i, i < r → (2 * N + 1) ^ i * 2 ^ A (i + 1) ≤
      (n + 1) * (N + 1) ^ i * 3 ^ A i) :
    A r ≤ cota alfa beta gamma r := by
  induction r with
  | zero => simp [cota, h0]
  | succ r ih =>
    have hprev := ih (fun i hi => hc i (by omega))
    have hp := OcelotasSueloRachas.paso_real hs hn (hc r (by omega)) halfa hbeta hgamma
    have hprevR : (A r : ℝ) ≤ cota alfa beta gamma r := by exact_mod_cast hprev
    have hmul := mul_le_mul_of_nonneg_left hprevR ha
    simp only [cota]
    apply Nat.le_floor
    linarith

theorem doble_indice {alfa beta gamma : ℝ}
    (ha : 3 / 2 ≤ alfa) (hb : 2 ≤ beta) (hg : gamma ≤ 1) (r : ℕ) :
    2 * r ≤ cota alfa beta gamma r := by
  induction r with
  | zero => simp [cota]
  | succ r ih =>
    have hprev : (2 : ℝ) * r ≤ cota alfa beta gamma r := by exact_mod_cast ih
    have hr : (0 : ℝ) ≤ r := by positivity
    have hm := mul_le_mul_of_nonneg_left hprev (by linarith : 0 ≤ alfa)
    have ham := mul_le_mul_of_nonneg_right ha hr
    have hgm := mul_le_mul_of_nonneg_right hg hr
    simp only [cota]
    apply Nat.le_floor
    push_cast
    nlinarith

theorem cota_monotona {alfa beta gamma : ℝ}
    (ha : 3 / 2 ≤ alfa) (hb : 2 ≤ beta) (hg : gamma ≤ 1) :
    Monotone (cota alfa beta gamma) := by
  apply monotone_nat_of_le_succ
  intro i
  have hd := doble_indice ha hb hg i
  have hprev : (2 : ℝ) * i ≤ cota alfa beta gamma i := by exact_mod_cast hd
  have hi : (0 : ℝ) ≤ i := by positivity
  have hm := mul_le_mul_of_nonneg_left hprev (by linarith : 0 ≤ alfa - 1)
  have ham := mul_le_mul_of_nonneg_right ha hi
  have hgm := mul_le_mul_of_nonneg_right hg hi
  simp only [cota]
  apply Nat.le_floor
  nlinarith

theorem cota_le_anterior {alfa beta gamma : ℝ} (ha : 0 ≤ alfa) (hg : 0 ≤ gamma) (r : ℕ) :
    cota alfa beta gamma r ≤ OcelotasAfinada.cota alfa beta r := by
  induction r with
  | zero => rfl
  | succ r ih =>
    have hprev : (cota alfa beta gamma r : ℝ) ≤ OcelotasAfinada.cota alfa beta r := by
      exact_mod_cast ih
    have hm := mul_le_mul_of_nonneg_left hprev ha
    have hgr : 0 ≤ gamma * r := mul_nonneg hg (by positivity)
    simp only [cota, OcelotasAfinada.cota]
    apply Nat.floor_mono
    linarith

theorem criba_palabra {n s r R N : ℕ} {a b : ℕ → ℕ} {alfa beta gamma : ℝ}
    (hw : Palabra n a b r) (hmin : ∀ i, i < r → N ≤ T^[tiempo a b i] n)
    (hs : 0 < s) (hn : n + 1 ≤ s) (hr : r ≤ R)
    (ha : 3 / 2 ≤ alfa) (hb : 2 ≤ beta) (hg : gamma ≤ 1)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2)
    (hgamma : gamma * log 2 ≤ log (2 * N + 1) - log (N + 1)) :
    S (tiempo a b r) n ≤ cota alfa beta gamma R := by
  have hc := criba_congruencias (acumulados a) hs hn rfl
    (by linarith : 0 ≤ alfa) halfa hbeta hgamma
    (OcelotasSueloRachas.congruencias_suelo hw hmin)
  rw [cuenta_impares hw r le_rfl]
  exact le_trans hc (cota_monotona ha hb hg hr)

theorem criba_primer_cruce {n s r R N : ℕ} {a b : ℕ → ℕ} {alfa beta gamma : ℝ}
    (hw : Palabra n a b r) (hk : PrimerCruce n (tiempo a b r)) (hN : N ≤ n)
    (hs : 0 < s) (hn : n + 1 ≤ s) (hr : r ≤ R)
    (ha : 3 / 2 ≤ alfa) (hb : 2 ≤ beta) (hg : gamma ≤ 1)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2)
    (hgamma : gamma * log 2 ≤ log (2 * N + 1) - log (N + 1)) :
    S (tiempo a b r) n ≤ cota alfa beta gamma R := by
  apply criba_palabra hw _ hs hn hr ha hb hg halfa hbeta hgamma
  intro i hi
  exact le_trans hN (no_desciende_antes hk (tiempo_lt hw hi))

end OcelotasSueloCriba

#print axioms OcelotasSueloCriba.criba_congruencias
#print axioms OcelotasSueloCriba.doble_indice
#print axioms OcelotasSueloCriba.cota_monotona
#print axioms OcelotasSueloCriba.cota_le_anterior
#print axioms OcelotasSueloCriba.criba_palabra
#print axioms OcelotasSueloCriba.criba_primer_cruce
