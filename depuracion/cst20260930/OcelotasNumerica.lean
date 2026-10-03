import OcelotasTreceBase

/-! # Ocelotas: interfaces numéricas con cantidad de rachas variable -/

namespace OcelotasNumerica

open Real Ocelotas OcelotasTrayectorias OcelotasAfinadaTrayectorias OcelotasTreceBase

theorem pequeno_por_cota {n r R s limite : ℕ} {a b : ℕ → ℕ} {c : ℝ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ R)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hc : 0 < c) (hLambda : c ≤ (tiempo a b r : ℝ) * log 2 -
      S (tiempo a b r) n * log 3) (hs : (R : ℝ) ≤ s * c)
    (hsmall : s ≤ limite) : n < limite :=
  lt_of_lt_of_le (semilla_de_cota hw hr hrR hk hf hc hLambda hs) hsmall

theorem imposible_por_criba {n r R s B qmin : ℕ} {a b : ℕ → ℕ} {c : ℝ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ R)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hc : 0 < c) (hLambda : c ≤ (tiempo a b r : ℝ) * log 2 -
      S (tiempo a b r) n * log 3) (hs : (R : ℝ) ≤ s * c)
    (hpot : s ^ 256 ≤ 2 ^ B)
    (hcriba : OcelotasAfinada.cota (1585 / 1000) ((B : ℝ) / 256) R < qmin)
    (hq : qmin ≤ S (tiempo a b r) n) : False := by
  have hns := semilla_de_cota hw hr hrR hk hf hc hLambda hs
  have hbeta := beta_de_potencia (by omega : 0 < s) hpot
  have hbound := criba_palabra hw (by omega : 0 < s) (by omega : n + 1 ≤ s) hrR
    (by norm_num : (1 : ℝ) ≤ 1585 / 1000) (by positivity : (0 : ℝ) ≤ (B : ℝ) / 256)
    alfa_valida hbeta
  omega

end OcelotasNumerica

#print axioms OcelotasNumerica.pequeno_por_cota
#print axioms OcelotasNumerica.imposible_por_criba
