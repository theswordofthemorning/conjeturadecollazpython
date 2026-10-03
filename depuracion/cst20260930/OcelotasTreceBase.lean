import OcelotasAfinadaTrayectorias
import Mathlib.Algebra.Order.Floor.Semifield

/-! # Ocelotas: interfaces de los certificados numéricos para trece rachas -/

namespace OcelotasTreceBase

open Real Ocelotas OcelotasLMN OcelotasAfinada OcelotasTrayectorias
  OcelotasAfinadaTrayectorias

theorem alfa_valida : log 3 ≤ (1585 / 1000 : ℝ) * log 2 := by
  have h2 := log_dos_cotas
  have h3 := log_tres_cotas
  linarith [h2.1, h3.2]

/-- Se comprueba una cota de log s con una comparación entera finita. -/
theorem beta_de_potencia {s B : ℕ} (hs : 0 < s) (hp : s ^ 256 ≤ 2 ^ B) :
    log s ≤ ((B : ℝ) / 256) * log 2 := by
  have hpot : (s : ℝ) ^ 256 ≤ (2 : ℝ) ^ B := by exact_mod_cast hp
  have hsR : (0 : ℝ) < s := by exact_mod_cast hs
  have hlog := Real.log_le_log (by positivity : (0 : ℝ) < (s : ℝ) ^ 256) hpot
  rw [Real.log_pow, Real.log_pow] at hlog
  norm_num at hlog
  linarith

/-- La cota positiva de una pareja se transporta al exponente real del cruce. -/
theorem lambda_de_pareja {P Q p v : ℤ} {k q : ℕ} {c : ℝ}
    (hQ : 0 < Q) (hv : 0 < v) (hdet : P * v - p * Q = 1)
    (hc : 0 < c) (hU : c ≤ P * log 2 - Q * log 3)
    (hV : p * log 2 - v * log 3 < 0) (hq : 0 < q)
    (hfin : (q : ℤ) < Q + v) (hk : 3 ^ q < 2 ^ k) :
    c ≤ (k : ℝ) * log 2 - q * log 3 := by
  have hL : 0 < (k : ℝ) * log 2 - q * log 3 := lambda_pos hk
  have h := aproximacion_superior (x := log 2) (y := log 3)
    (k := (k : ℤ)) (b := (q : ℤ)) hQ hv hdet (lt_of_lt_of_le hc hU) hV
    (by exact_mod_cast hq) hfin (by simpa using hL)
  exact le_trans hU (by simpa using h)

theorem pequeno_por_cota {n r s : ℕ} {a b : ℕ → ℕ} {c : ℝ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr13 : r ≤ 13)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hc : 0 < c) (hLambda : c ≤ (tiempo a b r : ℝ) * log 2 -
      S (tiempo a b r) n * log 3) (hs : (13 : ℝ) ≤ s * c)
    (hsmall : s ≤ 31624) : n < 31624 :=
  lt_of_lt_of_le (semilla_de_cota hw hr hr13 hk hf hc hLambda hs) hsmall

theorem imposible_por_criba {n r s B qmin : ℕ} {a b : ℕ → ℕ} {c : ℝ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr13 : r ≤ 13)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hc : 0 < c) (hLambda : c ≤ (tiempo a b r : ℝ) * log 2 -
      S (tiempo a b r) n * log 3) (hs : (13 : ℝ) ≤ s * c)
    (hpot : s ^ 256 ≤ 2 ^ B)
    (hcriba : OcelotasAfinada.cota (1585 / 1000) ((B : ℝ) / 256) 13 < qmin)
    (hq : qmin ≤ S (tiempo a b r) n) : False := by
  have hns := semilla_de_cota hw hr hr13 hk hf hc hLambda hs
  have hbeta := beta_de_potencia (by omega : 0 < s) hpot
  have hbound := criba_palabra hw (by omega : 0 < s) (by omega : n + 1 ≤ s) hr13
    (by norm_num : (1 : ℝ) ≤ 1585 / 1000) (by positivity : (0 : ℝ) ≤ (B : ℝ) / 256)
    alfa_valida hbeta
  omega

end OcelotasTreceBase

#print axioms OcelotasTreceBase.alfa_valida
#print axioms OcelotasTreceBase.beta_de_potencia
#print axioms OcelotasTreceBase.lambda_de_pareja
#print axioms OcelotasTreceBase.pequeno_por_cota
#print axioms OcelotasTreceBase.imposible_por_criba
