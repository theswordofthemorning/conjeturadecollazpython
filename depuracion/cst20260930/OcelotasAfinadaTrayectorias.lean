import OcelotasAfinada
import OcelotasLMN

/-! # Ocelotas: aplicación de la criba afinada a órbitas reales

Puente universal hasta la exclusión de un intervalo. Las cotas racionales
de logaritmos, la tabla de intervalos y el censo de semillas siguen fuera
de esta formalización. No se afirma aquí CST hasta 18 rachas en Lean.
-/

namespace OcelotasAfinadaTrayectorias

open Real Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN

theorem criba_palabra {n s r R : ℕ} {a b : ℕ → ℕ} {alfa beta : ℝ}
    (hw : Palabra n a b r) (hs : 0 < s) (hn : n + 1 ≤ s) (hr : r ≤ R)
    (ha : 1 ≤ alfa) (hb : 0 ≤ beta)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2) :
    S (tiempo a b r) n ≤ OcelotasAfinada.cota alfa beta R := by
  rw [cuenta_impares hw r le_rfl]
  exact le_trans
    (OcelotasAfinada.criba_congruencias (acumulados a) hs hn rfl
      (by linarith) halfa hbeta (congruencias_acumuladas hw))
    (OcelotasAfinada.cota_monotona ha hb hr)

/-- El fallo acota directamente el producto de la semilla y la forma lineal. -/
theorem fallo_lambda {n r : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r)
    (hr : 0 < r) (hk : PrimerCruce n (tiempo a b r))
    (hf : n ≤ T^[tiempo a b r] n) :
    ((tiempo a b r : ℝ) * log 2 - S (tiempo a b r) n * log 3) * n < r := by
  set k := tiempo a b r with he_k
  set q := S k n with he_q
  set lam : ℝ := (k : ℝ) * log 2 - q * log 3 with he_lam
  have hpos3 : (0 : ℝ) < (3 : ℝ) ^ q := by positivity
  have hpos2 : (0 : ℝ) < (2 : ℝ) ^ k := by positivity
  have hexp : Real.exp lam = (2 : ℝ) ^ k / (3 : ℝ) ^ q := by
    have hl : lam = log ((2 : ℝ) ^ k) - log ((3 : ℝ) ^ q) := by
      rw [Real.log_pow, Real.log_pow, he_lam]
    rw [hl, Real.exp_sub, Real.exp_log hpos2, Real.exp_log hpos3]
  have he := Real.add_one_le_exp lam
  rw [hexp, le_div_iff₀ hpos3] at he
  have hprod := fallo_producto hw hr hk hf
  have hlt : 3 ^ q < 2 ^ k := hk.2
  have hprodR : ((2 : ℝ) ^ k - (3 : ℝ) ^ q) * n < (r : ℝ) * (3 : ℝ) ^ q := by
    have hcast : (((2 ^ k - 3 ^ q) * n : ℕ) : ℝ) =
        ((2 : ℝ) ^ k - (3 : ℝ) ^ q) * n := by
      rw [Nat.cast_mul, Nat.cast_sub hlt.le]
      push_cast
      rfl
    have hreal := (Nat.cast_lt (α := ℝ)).2 hprod
    change (((2 ^ k - 3 ^ q) * n : ℕ) : ℝ) < ((r * 3 ^ q : ℕ) : ℝ) at hreal
    rw [hcast] at hreal
    push_cast at hreal
    exact hreal
  have hn : (0 : ℝ) ≤ n := by positivity
  have hm := mul_le_mul_of_nonneg_right he hn
  change lam * n < r
  nlinarith

/-- Si el producto s*c cubre R, una cota inferior c de Lambda acota n por s. -/
theorem semilla_de_cota {n r R s : ℕ} {a b : ℕ → ℕ} {c : ℝ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ R)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hc : 0 < c) (hLambda : c ≤ (tiempo a b r : ℝ) * log 2 -
      S (tiempo a b r) n * log 3) (hs : (R : ℝ) ≤ s * c) : n < s := by
  have hfallo := fallo_lambda hw hr hk hf
  have hmul := mul_le_mul_of_nonneg_right hLambda (by positivity : (0 : ℝ) ≤ n)
  have hrR' : (r : ℝ) ≤ R := by exact_mod_cast hrR
  have hns : (n : ℝ) < s := by nlinarith
  exact_mod_cast hns

/-- Exclusión universal: se unen la cota de Lambda y la criba logarítmica. -/
theorem descenso_intervalo {n k s qmin R : ℕ} {alfa beta c : ℝ}
    (hn : n % 2 = 1) (hk : PrimerCruce n k) (hr : rachas n k ≤ R)
    (hq : qmin ≤ S k n) (hc : 0 < c)
    (hLambda : c ≤ (k : ℝ) * log 2 - S k n * log 3)
    (hs : (R : ℝ) ≤ s * c) (ha : 1 ≤ alfa) (hb : 0 ≤ beta)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2)
    (hcriba : OcelotasAfinada.cota alfa beta R < qmin) : T^[k] n < n := by
  by_contra hf
  have hf' : n ≤ T^[k] n := by omega
  obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce hn hk
  have hk' : PrimerCruce n (tiempo a b (rachas n k)) := by rwa [he]
  have hf'' : n ≤ T^[tiempo a b (rachas n k)] n := by rwa [he]
  have hLambda' : c ≤ (tiempo a b (rachas n k) : ℝ) * log 2 -
      S (tiempo a b (rachas n k)) n * log 3 := by rwa [he]
  have hns := semilla_de_cota hw hpos hr hk' hf'' hc hLambda' hs
  have hq' := criba_palabra hw (by omega : 0 < s) (by omega : n + 1 ≤ s)
    hr ha hb halfa hbeta
  rw [he] at hq'
  omega

end OcelotasAfinadaTrayectorias

#print axioms OcelotasAfinadaTrayectorias.criba_palabra
#print axioms OcelotasAfinadaTrayectorias.fallo_lambda
#print axioms OcelotasAfinadaTrayectorias.semilla_de_cota
#print axioms OcelotasAfinadaTrayectorias.descenso_intervalo
