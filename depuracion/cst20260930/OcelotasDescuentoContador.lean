import OcelotasDescuentoRachas
import OcelotasPrefijosAfinados

/-! # Cota descontada desde el contador y después de un corte par

Se conserva la criba anterior. El término R + cota(alfa, beta-1, R)
es menor o igual que cota(alfa, beta, R) cuando alfa y beta son al menos 1.
La aplicación tras un corte usa un primer cruce finito, sin LMN.
-/

namespace OcelotasDescuentoContador

open Real Ocelotas OcelotasTrayectorias OcelotasContador OcelotasDescuentoRachas
  OcelotasPrefijos

theorem domina_cota_anterior {alfa beta : ℝ} (ha : 1 ≤ alfa) (hb : 1 ≤ beta) (r : ℕ) :
    r + OcelotasAfinada.cota alfa (beta - 1) r ≤ OcelotasAfinada.cota alfa beta r := by
  induction r with
  | zero => simp [OcelotasAfinada.cota]
  | succ r ih =>
    have hprev : (r : ℝ) + OcelotasAfinada.cota alfa (beta - 1) r ≤
        OcelotasAfinada.cota alfa beta r := by exact_mod_cast ih
    have hn : (0 : ℝ) ≤ OcelotasAfinada.cota alfa (beta - 1) r := by positivity
    have hp : 0 ≤ beta - 1 + alfa * OcelotasAfinada.cota alfa (beta - 1) r := by
      nlinarith
    have hfloor := Nat.floor_le hp
    have hmul := mul_le_mul_of_nonneg_left hprev (by linarith : 0 ≤ alfa)
    have hr : (0 : ℝ) ≤ r := by positivity
    simp only [OcelotasAfinada.cota]
    apply Nat.le_floor
    push_cast
    nlinarith

theorem criba_contador {k s : ℕ} {alfa beta : ℝ}
    (hs : 0 < s) (ha : 1 ≤ alfa) (hb : 1 ≤ beta)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2) :
    ∀ n, 0 < n → n + 1 ≤ s → (k = 0 ∨ T^[k - 1] n % 2 = 0) →
    S k n ≤ rachas n k + OcelotasAfinada.cota alfa (beta - 1) (rachas n k) := by
  induction k with
  | zero => intro n hn hns hf; simp [S, rachas, OcelotasAfinada.cota]
  | succ k ih =>
    intro n hn hns hf
    have hfin : T^[k] n % 2 = 0 := by simpa using hf
    by_cases hpar : n % 2 = 0
    · have hcut := rachas_add_corte (n := n) (i := 1) (Or.inr (by simpa using hpar)) k
      have hr : rachas n (k + 1) = rachas (T n) k := by
        simpa [Nat.add_comm, rachas, hpar] using hcut
      have hvalor : T n ≤ n := by
        simp only [T, hpar, if_pos]
        exact Nat.div_le_self _ _
      have hf' : k = 0 ∨ T^[k - 1] (T n) % 2 = 0 := by
        by_cases hk : k = 0
        · exact Or.inl hk
        · right
          have he : T^[k - 1] (T n) = T^[k] n := by
            have h := iter_add 1 (k - 1) n
            simpa [show 1 + (k - 1) = k by omega] using h.symm
          rw [he]
          exact hfin
      have h := ih (T n) (paso_positivo hn) (by omega) hf'
      simpa only [S, hpar, Nat.zero_add, hr] using h
    · obtain ⟨hpos, a, b, hw, he⟩ := extraer_palabra (by omega : n % 2 = 1)
        (by omega : 0 < k + 1) (by simpa using hfin)
      have h := OcelotasDescuentoRachas.criba_palabra hn hw hs hns (le_refl _) ha hb halfa hbeta
      rwa [he] at h

theorem criba_real_despues_corte {n k i R s : ℕ} {alfa beta : ℝ}
    (hn : 0 < n) (hk : PrimerCruce n k) (hi : i < k)
    (hcorte : i = 0 ∨ T^[i - 1] n % 2 = 0) (hr : rachas n k ≤ R)
    (hs : 0 < s) (hvalor : T^[i] n + 1 ≤ s) (ha : 1 ≤ alfa) (hb : 1 ≤ beta)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2) :
    S k n ≤ S i n + (R - rachas n i) +
      OcelotasAfinada.cota alfa (beta - 1) (R - rachas n i) := by
  have ht : i + (k - i) = k := by omega
  have hsuma := S_add i (k - i) n
  rw [ht] at hsuma
  have hrpart := rachas_add_corte hcorte (k - i)
  rw [ht] at hrpart
  have hrest : rachas (T^[i] n) (k - i) ≤ R - rachas n i := by omega
  have hfin : T^[k - i - 1] (T^[i] n) % 2 = 0 := by
    rw [← iter_add, show i + (k - i - 1) = k - 1 by omega]
    exact cruce_termina_par hk
  have hc := criba_contador hs ha hb halfa hbeta (T^[i] n)
    (iterado_positivo hn i) hvalor (Or.inr hfin)
  have hmono := OcelotasAfinada.cota_monotona ha (by linarith : 0 ≤ beta - 1) hrest
  omega

theorem criba_desde_potencia {n k i R maximo B : ℕ}
    (hn : 0 < n) (hk : PrimerCruce n k) (hi : i < k)
    (hcorte : i = 0 ∨ T^[i - 1] n % 2 = 0) (hr : rachas n k ≤ R)
    (hvalor : T^[i] n ≤ maximo) (hB : 256 ≤ B)
    (hpot : (maximo + 1) ^ 256 ≤ 2 ^ B) :
    S k n ≤ S i n + (R - rachas n i) +
      OcelotasPrefijosAfinados.cota (B - 256) (R - rachas n i) := by
  have hbeta := OcelotasTreceBase.beta_de_potencia (by omega : 0 < maximo + 1) hpot
  have hBreal : (256 : ℝ) ≤ B := by exact_mod_cast hB
  have hc := criba_real_despues_corte hn hk hi hcorte hr
    (by omega : 0 < maximo + 1) (by omega : T^[i] n + 1 ≤ maximo + 1)
    (by norm_num : (1 : ℝ) ≤ 1585 / 1000)
    (by linarith : (1 : ℝ) ≤ (B : ℝ) / 256)
    OcelotasTreceBase.alfa_valida hbeta
  have he : ((B - 256 : ℕ) : ℝ) / 256 = (B : ℝ) / 256 - 1 := by
    rw [Nat.cast_sub hB]
    norm_num
    ring
  rw [OcelotasPrefijosAfinados.cota_real, he]
  exact hc

end OcelotasDescuentoContador

#print axioms OcelotasDescuentoContador.domina_cota_anterior
#print axioms OcelotasDescuentoContador.criba_contador
#print axioms OcelotasDescuentoContador.criba_real_despues_corte
#print axioms OcelotasDescuentoContador.criba_desde_potencia
