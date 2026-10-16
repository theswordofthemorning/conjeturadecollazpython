import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasResiduosFinito

/-! Puente entre un registro externo de tiempos totales y CST.
El mapa Col cuenta un paso impar y su division por dos por separado.
Solo la cobertura del registro es externa. El intervalo pequeno y el
puente hasta CST se verifican en el nucleo; no se supone el corolario RT.
-/

namespace OcelotasRoosendaal

open Real Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN

def Col (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- Cobertura, no solo la trayectoria de la semilla record. -/
def DelayHasta (N D : ℕ) : Prop :=
  ∀ n, 2 ≤ n → n ≤ N → ∃ d, d ≤ D ∧ Col^[d] n = 1

theorem impares_le_tiempo (k n : ℕ) : S k n ≤ k := by
  induction k generalizing n with
  | zero => simp [S]
  | succ k ih =>
    simp only [S]
    have := ih (T n)
    have := Nat.mod_lt n (by decide : 0 < 2)
    omega

theorem rachas_le_tiempo (n k : ℕ) : rachas n k ≤ k := by
  induction k with
  | zero => simp [rachas]
  | succ k ih =>
    simp only [rachas]
    split <;> omega

theorem lambda_hasta_2480 {k q : ℕ} (hq : 0 < q) (hmax : q ≤ 2480)
    (hcruce : 3 ^ q < 2 ^ k) :
    (1 / 1200 : ℝ) ≤ (k : ℝ) * log 2 - q * log 3 := by
  have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
  have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
  apply OcelotasTreceBase.lambda_de_pareja (P := 3647) (Q := 2301)
    (p := 1054) (v := 665) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) _ _ hq (by omega) hcruce
  · norm_num
    linarith [h2.1, h3.2]
  · norm_num
    linarith [h2.2, h3.1]

/-- Todo primer cruce de hasta 2480 pasos es un descenso, para toda semilla. -/
theorem descenso_cruce_corto {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hcorto : k ≤ 2480) : T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · by_contra h
    have hf : n ≤ T^[k] n := by omega
    obtain ⟨hr, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hqpos := impares_pos hw hr
    have hqmax := impares_le_tiempo k n
    have hrmax := rachas_le_tiempo n k
    have hkw : PrimerCruce n (tiempo a b (rachas n k)) := by rwa [he]
    have hfw : n ≤ T^[tiempo a b (rachas n k)] n := by rwa [he]
    have hL := lambda_hasta_2480 (by simpa [he] using hqpos)
      (by omega : S k n ≤ 2480) hk.2
    have hsmall := OcelotasNumerica.pequeno_por_cota
      (R := 2480) (s := 2976000) (limite := 4912741)
      hw hr (by omega) hkw hfw (by norm_num : (0 : ℝ) < 1 / 1200)
      (by simpa [he] using hL) (by norm_num) (by norm_num)
    have hd := OcelotasResiduosFinito.descenso_finito hn (by omega) hk
    omega

/-- Llegar a 1 en d pasos clasicos implica llegar en a lo sumo d pasos T. -/
theorem llegada_atajo {d n : ℕ} (hllega : Col^[d] n = 1) :
    ∃ t, t ≤ d ∧ T^[t] n = 1 := by
  induction d using Nat.strong_induction_on generalizing n with
  | h d ih =>
    by_cases hn : n = 1
    · exact ⟨0, Nat.zero_le _, by simpa using hn⟩
    cases d with
    | zero => simp at hllega; contradiction
    | succ d =>
      by_cases hpar : n % 2 = 0
      · have hpaso : Col n = T n := by simp [Col, T, hpar]
        have hl : Col^[d] (T n) = 1 := by
          simpa only [Function.iterate_succ_apply, hpaso] using hllega
        obtain ⟨t, ht, he⟩ := ih d (by omega) hl
        exact ⟨t + 1, by omega, by simpa only [Function.iterate_succ_apply] using he⟩
      · have hodd : n % 2 = 1 := by omega
        have hpaso : Col (Col n) = T n := by
          have heven : (3 * n + 1) % 2 = 0 := by omega
          simp [Col, T, hpar, heven]
        cases d with
        | zero =>
          simp only [Nat.zero_add, Function.iterate_one, Col, if_neg hpar] at hllega
          omega
        | succ d =>
          have hl : Col^[d] (T n) = 1 := by
            simpa only [Function.iterate_succ_apply, hpaso] using hllega
          obtain ⟨t, ht, he⟩ := ih d (by omega) hl
          exact ⟨t + 1, by omega, by simpa only [Function.iterate_succ_apply] using he⟩

/-- Descarga del corolario CST a partir de la unica cobertura externa. -/
theorem cst_de_delay {N n k : ℕ} (hD : DelayHasta N 2480)
    (hn : 2 ≤ n) (hN : n ≤ N) (hk : PrimerCruce n k) : T^[k] n < n := by
  obtain ⟨d, hd, hl⟩ := hD n hn hN
  obtain ⟨t, ht, he⟩ := llegada_atajo hl
  have hkt : k ≤ t := by
    by_contra h
    have hantes := no_desciende_antes hk (by omega : t < k)
    rw [he] at hantes
    omega
  exact descenso_cruce_corto hn hk (by omega)

end OcelotasRoosendaal

#print axioms OcelotasRoosendaal.impares_le_tiempo
#print axioms OcelotasRoosendaal.rachas_le_tiempo
#print axioms OcelotasRoosendaal.lambda_hasta_2480
#print axioms OcelotasRoosendaal.descenso_cruce_corto
#print axioms OcelotasRoosendaal.llegada_atajo
#print axioms OcelotasRoosendaal.cst_de_delay
