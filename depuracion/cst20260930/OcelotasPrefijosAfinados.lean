import OcelotasPrefijos
import OcelotasNumerica

/-! # Ocelotas: criba afinada de las rachas posteriores a un corte

La recurrencia entera corresponde exactamente a alfa=317/200 y beta=B/256.
El corte es vacio o sigue a una entrada par: no se fusionan rachas.
Estos lemas son elementales; no suponen LMN ni un censo externo.
-/

namespace OcelotasPrefijosAfinados

open Real Ocelotas OcelotasTrayectorias OcelotasContador OcelotasPrefijos

set_option maxHeartbeats 1000000

def cota (B : ℕ) : ℕ → ℕ
  | 0 => 0
  | r + 1 => (25 * B + 10144 * cota B r) / 6400

theorem cota_real (B r : ℕ) :
    cota B r = OcelotasAfinada.cota (1585 / 1000) ((B : ℝ) / 256) r := by
  induction r with
  | zero => rfl
  | succ r ih =>
    simp only [cota, OcelotasAfinada.cota]
    rw [← ih]
    have he : (B : ℝ) / 256 + (1585 / 1000 : ℝ) * cota B r =
        ((25 * B + 10144 * cota B r : ℕ) : ℝ) / 6400 := by push_cast; ring
    rw [he]
    exact (Nat.floor_div_eq_div (25 * B + 10144 * cota B r) 6400).symm

theorem cota_monotona (B : ℕ) : Monotone (cota B) := by
  intro r R hr
  rw [cota_real, cota_real]
  exact OcelotasAfinada.cota_monotona (by norm_num) (by positivity) hr

def exponente (s : ℕ) : ℕ :=
  if s ≤ 1 then 0 else Nat.log2 (s ^ 256 - 1) + 1

theorem potencia_exponente (s : ℕ) : s ^ 256 ≤ 2 ^ exponente s := by
  by_cases hs : s ≤ 1
  · have hcases : s = 0 ∨ s = 1 := by omega
    rcases hcases with hz | hu
    · simp [hz, exponente]
    · simp [hu, exponente]
  · simp only [exponente, if_neg hs]
    have hs0 : 0 < s := by omega
    have hp : 0 < s ^ 256 := by positivity
    have h := Nat.lt_log2_self (n := s ^ 256 - 1)
    omega

theorem criba_contador {k s : ℕ} {alfa beta : ℝ}
    (hs : 0 < s) (ha : 1 ≤ alfa) (hb : 0 ≤ beta)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2) :
    ∀ n, n + 1 ≤ s → (k = 0 ∨ T^[k - 1] n % 2 = 0) →
    S k n ≤ OcelotasAfinada.cota alfa beta (rachas n k) := by
  induction k with
  | zero => intro n hn hf; simp [S, rachas, OcelotasAfinada.cota]
  | succ k ih =>
    intro n hn hf
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
      have h := ih (T n) (by omega) hf'
      simpa only [S, hpar, Nat.zero_add, hr] using h
    · obtain ⟨hpos, a, b, hw, he⟩ := extraer_palabra (by omega : n % 2 = 1)
        (by omega : 0 < k + 1) (by simpa using hfin)
      have h := OcelotasAfinadaTrayectorias.criba_palabra hw hs hn (le_refl _) ha hb halfa hbeta
      rwa [he] at h

theorem criba_real_despues_corte {n k i R s : ℕ} {alfa beta : ℝ}
    (hk : PrimerCruce n k) (hi : i < k)
    (hcorte : i = 0 ∨ T^[i - 1] n % 2 = 0) (hr : rachas n k ≤ R)
    (hs : 0 < s) (hvalor : T^[i] n + 1 ≤ s) (ha : 1 ≤ alfa) (hb : 0 ≤ beta)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2) :
    S k n ≤ S i n + OcelotasAfinada.cota alfa beta (R - rachas n i) := by
  have ht : i + (k - i) = k := by omega
  have hsuma := S_add i (k - i) n
  rw [ht] at hsuma
  have hrpart := rachas_add_corte hcorte (k - i)
  rw [ht] at hrpart
  have hrest : rachas (T^[i] n) (k - i) ≤ R - rachas n i := by omega
  have hfin : T^[k - i - 1] (T^[i] n) % 2 = 0 := by
    rw [← iter_add, show i + (k - i - 1) = k - 1 by omega]
    exact cruce_termina_par hk
  have hc := criba_contador hs ha hb halfa hbeta (T^[i] n) hvalor (Or.inr hfin)
  have hmono := OcelotasAfinada.cota_monotona ha hb hrest
  omega

theorem criba_despues_corte {n k i R maximo : ℕ}
    (hk : PrimerCruce n k) (hi : i < k)
    (hcorte : i = 0 ∨ T^[i - 1] n % 2 = 0) (hr : rachas n k ≤ R)
    (hvalor : T^[i] n ≤ maximo) :
    S k n ≤ S i n + cota (exponente (maximo + 1)) (R - rachas n i) := by
  have hbeta := OcelotasTreceBase.beta_de_potencia (by omega : 0 < maximo + 1)
    (potencia_exponente (maximo + 1))
  have hc := criba_real_despues_corte hk hi hcorte hr (by omega : 0 < maximo + 1)
    (by omega : T^[i] n + 1 ≤ maximo + 1) (by norm_num : (1 : ℝ) ≤ 1585 / 1000)
    (by positivity : (0 : ℝ) ≤ (exponente (maximo + 1) : ℝ) / 256)
    OcelotasTreceBase.alfa_valida hbeta
  simpa only [cota_real] using hc

end OcelotasPrefijosAfinados

#print axioms OcelotasPrefijosAfinados.cota_real
#print axioms OcelotasPrefijosAfinados.cota_monotona
#print axioms OcelotasPrefijosAfinados.potencia_exponente
#print axioms OcelotasPrefijosAfinados.criba_contador
#print axioms OcelotasPrefijosAfinados.criba_real_despues_corte
#print axioms OcelotasPrefijosAfinados.criba_despues_corte
