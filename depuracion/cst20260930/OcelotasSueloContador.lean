import OcelotasSueloNumerica
import OcelotasPrefijosAfinados

/-! # Cota con suelo desde el contador y después de un corte par

El suelo se hereda del primer cruce global. No se supone que el sufijo
tenga su propio primer cruce ni que el valor final permanezca sobre el suelo.
El corte es vacío o sigue a una entrada par, para no partir una racha impar.
-/

namespace OcelotasSueloContador

open Real Ocelotas OcelotasTrayectorias OcelotasContador OcelotasPrefijos

theorem criba_contador {k s N : ℕ} {alfa beta gamma : ℝ}
    (hs : 0 < s) (ha : 3 / 2 ≤ alfa) (hb : 2 ≤ beta) (hg : gamma ≤ 1)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2)
    (hgamma : gamma * log 2 ≤ log (2 * N + 1) - log (N + 1)) :
    ∀ n, n + 1 ≤ s → (∀ j, j < k → N ≤ T^[j] n) →
    (k = 0 ∨ T^[k - 1] n % 2 = 0) →
    S k n ≤ OcelotasSueloCriba.cota alfa beta gamma (rachas n k) := by
  induction k with
  | zero => intro n hns hmin hf; simp [S, rachas, OcelotasSueloCriba.cota]
  | succ k ih =>
    intro n hns hmin hf
    have hfin : T^[k] n % 2 = 0 := by simpa using hf
    by_cases hpar : n % 2 = 0
    · have hcut := rachas_add_corte (n := n) (i := 1) (Or.inr (by simpa using hpar)) k
      have hr : rachas n (k + 1) = rachas (T n) k := by
        simpa [Nat.add_comm, rachas, hpar] using hcut
      have hvalor : T n ≤ n := by
        simp only [T, hpar, if_pos]
        exact Nat.div_le_self _ _
      have hmin' : ∀ j, j < k → N ≤ T^[j] (T n) := by
        intro j hj
        have h := hmin (1 + j) (by omega)
        simpa only [iter_add, Function.iterate_one] using h
      have hf' : k = 0 ∨ T^[k - 1] (T n) % 2 = 0 := by
        by_cases hk : k = 0
        · exact Or.inl hk
        · right
          have he : T^[k - 1] (T n) = T^[k] n := by
            have h := iter_add 1 (k - 1) n
            simpa [show 1 + (k - 1) = k by omega] using h.symm
          rw [he]
          exact hfin
      have h := ih (T n) (by omega) hmin' hf'
      simpa only [S, hpar, Nat.zero_add, hr] using h
    · obtain ⟨hpos, a, b, hw, he⟩ := extraer_palabra (by omega : n % 2 = 1)
        (by omega : 0 < k + 1) (by simpa using hfin)
      have hsuelo : ∀ j, j < rachas n (k + 1) → N ≤ T^[tiempo a b j] n := by
        intro j hj
        have ht := tiempo_lt hw hj
        rw [he] at ht
        exact hmin _ ht
      have h := OcelotasSueloCriba.criba_palabra hw hsuelo hs hns (le_refl _)
        ha hb hg halfa hbeta hgamma
      rwa [he] at h

theorem criba_real_despues_corte {n k i R s N : ℕ} {alfa beta gamma : ℝ}
    (hk : PrimerCruce n k) (hi : i < k) (hN : N ≤ n)
    (hcorte : i = 0 ∨ T^[i - 1] n % 2 = 0) (hr : rachas n k ≤ R)
    (hs : 0 < s) (hvalor : T^[i] n + 1 ≤ s)
    (ha : 3 / 2 ≤ alfa) (hb : 2 ≤ beta) (hg : gamma ≤ 1)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2)
    (hgamma : gamma * log 2 ≤ log (2 * N + 1) - log (N + 1)) :
    S k n ≤ S i n + OcelotasSueloCriba.cota alfa beta gamma (R - rachas n i) := by
  have ht : i + (k - i) = k := by omega
  have hsuma := S_add i (k - i) n
  rw [ht] at hsuma
  have hrpart := rachas_add_corte hcorte (k - i)
  rw [ht] at hrpart
  have hrest : rachas (T^[i] n) (k - i) ≤ R - rachas n i := by omega
  have hfin : T^[k - i - 1] (T^[i] n) % 2 = 0 := by
    rw [← iter_add, show i + (k - i - 1) = k - 1 by omega]
    exact cruce_termina_par hk
  have hmin : ∀ j, j < k - i → N ≤ T^[j] (T^[i] n) := by
    intro j hj
    rw [← iter_add]
    exact le_trans hN (no_desciende_antes hk (by omega : i + j < k))
  have hc := criba_contador hs ha hb hg halfa hbeta hgamma (T^[i] n)
    hvalor hmin (Or.inr hfin)
  have hmono := OcelotasSueloCriba.cota_monotona ha hb hg hrest
  omega

theorem criba_desde_potencia {n k i R maximo B : ℕ}
    (hk : PrimerCruce n k) (hi : i < k) (hN : 4095 ≤ n)
    (hcorte : i = 0 ∨ T^[i - 1] n % 2 = 0) (hr : rachas n k ≤ R)
    (hvalor : T^[i] n ≤ maximo) (hB : 512 ≤ B)
    (hpot : (maximo + 1) ^ 256 ≤ 2 ^ B) :
    S k n ≤ S i n + OcelotasSueloNumerica.cota B (R - rachas n i) := by
  have hbeta := OcelotasTreceBase.beta_de_potencia (by omega : 0 < maximo + 1) hpot
  have hBR : (512 : ℝ) ≤ B := by exact_mod_cast hB
  have hc := criba_real_despues_corte (N := 4095) hk hi hN hcorte hr
    (by omega : 0 < maximo + 1) (by omega : T^[i] n + 1 ≤ maximo + 1)
    (by norm_num : (3 / 2 : ℝ) ≤ 1585 / 1000)
    (by linarith : (2 : ℝ) ≤ (B : ℝ) / 256)
    (by norm_num : (4095 / 4096 : ℝ) ≤ 1) OcelotasTreceBase.alfa_valida hbeta
    (by norm_num; exact OcelotasSueloNumerica.gamma_valida)
  rw [← OcelotasSueloNumerica.cota_real B _ hB] at hc
  exact hc

end OcelotasSueloContador

#print axioms OcelotasSueloContador.criba_contador
#print axioms OcelotasSueloContador.criba_real_despues_corte
#print axioms OcelotasSueloContador.criba_desde_potencia
