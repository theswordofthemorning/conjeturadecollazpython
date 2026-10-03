import OcelotasContador
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-! # Ocelotas con la proposición de Rhin literal, sólo para alturas grandes

`RhinEntera` era una traducción hecha a mano. Aquí la hipótesis es la
desigualdad real publicada por Rhin (1987, proposición de la p. 160), en la
forma en que la aplican Simons y de Weger (2005, lema 12):
`|u0 + u1 log 2 + u2 log 3| ≥ H^(-13,3)`, con `H = max(|u1|, |u2|)`.
Sólo se usa el caso `u0 = 0`, y el paso a la forma entera se demuestra.

El original no se pudo consultar, así que su umbral de validez queda como
parámetro `H0`. Basta `H0 ≤ 131072`: la cadena de diez rachas sólo usa Rhin
para descartar los fallos con `k ≥ 131072`.

Los cuerpos de `fallo_rhin`, `tiempo_diez`, `diez_de_certificado`,
`descenso_contador` y `cst_contador` se repiten con la hipótesis puntual;
los módulos certificados no se tocan.
-/

namespace OcelotasRhin

open Ocelotas OcelotasRachas OcelotasTrayectorias OcelotasFinito OcelotasCertificado
  OcelotasCierre OcelotasContador

/-- Proposición de Rhin (1987, p. 160), con umbral explícito para la altura. -/
def RhinProposicion (H0 : ℕ) : Prop :=
  ∀ u0 u1 u2 : ℤ, (H0 : ℤ) ≤ max |u1| |u2| →
    ((max |u1| |u2| : ℤ) : ℝ) ^ (-(133 / 10 : ℝ)) ≤
      |(u0 : ℝ) + (u1 : ℝ) * Real.log 2 + (u2 : ℝ) * Real.log 3|

/-- Caso homogéneo `u0 = 0`, el único que se usa. -/
def RhinHomogenea (H0 : ℕ) : Prop :=
  ∀ u1 u2 : ℤ, (H0 : ℤ) ≤ max |u1| |u2| →
    ((max |u1| |u2| : ℤ) : ℝ) ^ (-(133 / 10 : ℝ)) ≤
      |(u1 : ℝ) * Real.log 2 + (u2 : ℝ) * Real.log 3|

/-- Forma entera, exigida sólo desde `K0`. -/
def RhinDesde (K0 : ℕ) : Prop :=
  ∀ k q : ℕ, K0 ≤ k → 2 ^ k ≤ 2 * 3 ^ q → 3 ^ q < 2 ^ k →
    3 ^ q ≤ (2 ^ k - 3 ^ q) * k ^ 14

theorem homogenea_de_proposicion {H0 : ℕ} (hR : RhinProposicion H0) : RhinHomogenea H0 := by
  intro u1 u2 hH
  have h := hR 0 u1 u2 hH
  simpa using h

theorem rhin_desde_mono {K0 K1 : ℕ} (h : K0 ≤ K1) (hR : RhinDesde K0) : RhinDesde K1 :=
  fun k q hk => hR k q (le_trans h hk)

/-- La hipótesis antigua es la nueva desde cero; en particular la implica. -/
theorem entera_iff_desde_cero : RhinEntera ↔ RhinDesde 0 := by
  constructor
  · intro h k q _
    exact h k q
  · intro h k q
    exact h k q (Nat.zero_le k)

/-- Paso demostrado de la desigualdad real a la forma entera:
`Δ = 3^q (e^Λ - 1) ≥ 3^q Λ ≥ 3^q k^(-13,3) ≥ 3^q k^(-14)`. -/
theorem desde_homogenea {H0 : ℕ} (hR : RhinHomogenea H0) : RhinDesde H0 := by
  intro k q hk _hv hlt
  have hqk : q < k := by
    by_contra h
    have h1 : 2 ^ k ≤ 2 ^ q := Nat.pow_le_pow_right (by norm_num) (not_lt.mp h)
    have h2 : 2 ^ q ≤ 3 ^ q := Nat.pow_le_pow_left (by norm_num) q
    omega
  have hk1 : 1 ≤ k := by omega
  have hH : max |(k : ℤ)| |(-(q : ℤ))| = (k : ℤ) := by
    rw [abs_neg, abs_of_nonneg (by positivity), abs_of_nonneg (by positivity)]
    exact max_eq_left (by exact_mod_cast hqk.le)
  have hr := hR (k : ℤ) (-(q : ℤ)) (by rw [hH]; exact_mod_cast hk)
  rw [hH] at hr
  set L : ℝ := (k : ℝ) * Real.log 2 - (q : ℝ) * Real.log 3 with hL
  have hexpr : ((k : ℤ) : ℝ) * Real.log 2 + ((-(q : ℤ) : ℤ) : ℝ) * Real.log 3 = L := by
    push_cast
    rw [hL]
    ring
  have hpos3 : (0 : ℝ) < (3 : ℝ) ^ q := by positivity
  have hpos2 : (0 : ℝ) < (2 : ℝ) ^ k := by positivity
  have hltR : (3 : ℝ) ^ q < (2 : ℝ) ^ k := by exact_mod_cast hlt
  have hlog : Real.log ((3 : ℝ) ^ q) < Real.log ((2 : ℝ) ^ k) := Real.log_lt_log hpos3 hltR
  rw [Real.log_pow, Real.log_pow] at hlog
  have hLpos : 0 < L := by
    rw [hL]
    linarith
  rw [hexpr, abs_of_pos hLpos] at hr
  have hkR : ((k : ℤ) : ℝ) = (k : ℝ) := by push_cast; rfl
  rw [hkR] at hr
  -- hr : k^(-13,3) ≤ L
  have hexp : Real.exp L = (2 : ℝ) ^ k / (3 : ℝ) ^ q := by
    have hL' : L = Real.log ((2 : ℝ) ^ k) - Real.log ((3 : ℝ) ^ q) := by
      rw [Real.log_pow, Real.log_pow, hL]
    rw [hL', Real.exp_sub, Real.exp_log hpos2, Real.exp_log hpos3]
  have h1 : L + 1 ≤ Real.exp L := Real.add_one_le_exp L
  have hk1R : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk1
  have h14 : (k : ℝ) ^ (-(14 : ℝ)) ≤ (k : ℝ) ^ (-(133 / 10 : ℝ)) :=
    Real.rpow_le_rpow_of_exponent_le hk1R (by norm_num)
  have h14' : (k : ℝ) ^ (-(14 : ℝ)) = ((k : ℝ) ^ (14 : ℕ))⁻¹ := by
    rw [Real.rpow_neg (by positivity)]
    norm_cast
  have hk14pos : (0 : ℝ) < (k : ℝ) ^ (14 : ℕ) := by positivity
  have hclave : ((k : ℝ) ^ (14 : ℕ))⁻¹ ≤ (2 : ℝ) ^ k / (3 : ℝ) ^ q - 1 := by
    rw [← h14', ← hexp]
    linarith
  rw [div_sub_one (ne_of_gt hpos3), le_div_iff₀ hpos3] at hclave
  have h3 := mul_le_mul_of_nonneg_right hclave hk14pos.le
  have hsimp : ((k : ℝ) ^ (14 : ℕ))⁻¹ * (3 : ℝ) ^ q * (k : ℝ) ^ (14 : ℕ) = (3 : ℝ) ^ q := by
    field_simp
  rw [hsimp] at h3
  have hcast : (((2 ^ k - 3 ^ q) * k ^ 14 : ℕ) : ℝ) =
      ((2 : ℝ) ^ k - (3 : ℝ) ^ q) * (k : ℝ) ^ (14 : ℕ) := by
    rw [Nat.cast_mul, Nat.cast_sub hlt.le]
    push_cast
    ring
  have hfin : ((3 ^ q : ℕ) : ℝ) ≤ (((2 ^ k - 3 ^ q) * k ^ 14 : ℕ) : ℝ) := by
    rw [hcast]
    push_cast
    exact h3
  exact_mod_cast hfin

theorem desde_proposicion {H0 : ℕ} (hR : RhinProposicion H0) : RhinDesde H0 :=
  desde_homogenea (homogenea_de_proposicion hR)

/-! ## La cadena de diez rachas con la hipótesis puntual -/

/-- `fallo_rhin` con la desigualdad sólo en el `k` y el `q` de la órbita. -/
theorem fallo_rhin_punto {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hk : PrimerCruce n (tiempo a b r))
    (hf : n ≤ T^[tiempo a b r] n)
    (he : 3 ^ S (tiempo a b r) n ≤
      (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * tiempo a b r ^ 14) :
    n < r * tiempo a b r ^ 14 := by
  have hp := fallo_producto hw hr hk hf
  have hm := Nat.mul_le_mul_left r he
  have hc : (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * n <
      (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * (r * tiempo a b r ^ 14) := by
    nlinarith
  exact Nat.lt_of_mul_lt_mul_left hc

/-- `tiempo_diez` con la hipótesis puntual; el cuerpo es el original. -/
theorem tiempo_diez_punto {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hR : 3 ^ S (tiempo a b r) n ≤
      (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * tiempo a b r ^ 14) :
    tiempo a b r < 131072 := by
  let k := tiempo a b r
  let t := Nat.log 2 k
  let m := 4 + 14 * (t + 1)
  have hk0 : 0 < k := (ventana_cruce hk).1
  have hlo : 2 ^ t ≤ k := Nat.pow_log_le_self 2 (by omega)
  have hhi : k < 2 ^ (t + 1) := Nat.lt_pow_succ_log_self (by decide) k
  have hn : n + 1 < 2 ^ m := by
    have hfR := fallo_rhin_punto hw hr hk hf hR
    have hrk := Nat.mul_le_mul_right (k ^ 14) hr10
    have hp := Nat.pow_lt_pow_left hhi (by decide : 14 ≠ 0)
    have he : 16 * (2 ^ (t + 1)) ^ 14 = 2 ^ m := by
      dsimp [m]
      rw [pow_add 2 4, show 14 * (t + 1) = (t + 1) * 14 by omega, pow_mul]
      norm_num
    have hpos : 0 < k ^ 14 := by positivity
    change n < r * k ^ 14 at hfR
    nlinarith
  have hc := criba_desde_trayectoria hw hn
  have hcm := cota_monotona (by dsimp [m]; omega : 1 ≤ m) hr10
  have hd := cota_diez_lineal m
  have hq : 0 < S k n := by
    rw [show k = tiempo a b r from rfl, cuenta_impares hw r le_rfl]
    have ha := (hw 0 hr).1
    have hs := cuenta_impares hw 1 (by omega)
    have ht := tiempo_mono a b (show 1 ≤ r by omega)
    have hsum := S_add (tiempo a b 1) (tiempo a b r - tiempo a b 1) n
    rw [Nat.add_sub_of_le ht] at hsum
    rw [cuenta_impares hw r le_rfl, hs] at hsum
    simp only [acumulados] at hsum
    omega
  have hki := tiempo_por_impares hq (ventana_cruce hk).2
  have hlin : k ≤ 364 * (4 + 14 * (t + 1)) := by
    change S k n ≤ cota r m at hc
    dsimp [m] at hc hcm hd
    omega
  by_contra hlarge
  have ht : 17 ≤ t := Nat.le_log_of_pow_le (by decide) (by norm_num; omega)
  have hcola := cola_diez t ht
  omega

/-- Rhin sólo hace falta para descartar `k ≥ 131072`. -/
theorem tiempo_diez_desde (hR : RhinDesde 131072) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n) :
    tiempo a b r < 131072 := by
  by_contra hgrande
  have he := hR _ _ (by omega) (ventana_cruce hk).2 hk.2
  have hmenor := tiempo_diez_punto hw hr hr10 hk hf he
  omega

/-- `ocelotas_diez` con `RhinDesde 131072`; el cuerpo es el de `diez_de_certificado`. -/
theorem ocelotas_diez_desde (hR : RhinDesde 131072) {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra hdesc
  have hf : n ≤ T^[tiempo a b r] n := by omega
  let k := tiempo a b r
  let q := S k n
  have hkt : k < 131072 := tiempo_diez_desde hR hw hr hr10 hk hf
  have hk2 : 2 ≤ k := by
    have ha := (hw 0 hr).1
    have hb := (hw 0 hr).2.1
    have ht := tiempo_mono a b (show 1 ≤ r by omega)
    simp only [tiempo] at ht
    dsimp [k]
    omega
  have hkd : k = Nat.log2 (3 ^ q) + 1 := k_de_q (ventana_estricta hk hk2) hk.2
  have hq1 : 1 ≤ q := by
    by_contra h
    have hq0 : q = 0 := by omega
    simp only [hq0, pow_zero, show Nat.log2 1 = 0 from rfl] at hkd
    omega
  have hqmax : q ≤ 82696 := exponente_acotado hkt hk.2
  have hc := criba_certificada q hq1 hqmax
  simp only [CertificadoAritmetico] at hc
  rw [← hkd] at hc
  rcases hc with hsemilla | hfuera
  · have hp := fallo_producto hw hr hk hf
    have hrP := Nat.mul_le_mul_right (3 ^ q) hr10
    change (2 ^ k - 3 ^ q) * n < r * 3 ^ q at hp
    have hnsmall : n < 11215 := Nat.lt_of_mul_lt_mul_left
      (show (2 ^ k - 3 ^ q) * n < (2 ^ k - 3 ^ q) * 11215 by nlinarith)
    exact hdesc (descenso_finito hn (by omega) hk)
  · have hcribado : q ≤ cota 10 ((q - 1) / 182) :=
      criba_fallo hw hr hr10 hk hf hfuera
    have hlineal := cota_diez_lineal ((q - 1) / 182)
    omega

theorem descenso_contador_desde (hR : RhinDesde 131072) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) : T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hh := ocelotas_diez_desde hR hn hw hpos hr
    rw [he] at hh
    exact hh hk

theorem cst_contador_desde (hR : RhinDesde 131072) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj, descenso_contador_desde hR hn hk hr⟩

/-- **CST hasta diez rachas, bajo el caso homogéneo de Rhin para `H ≥ H0`, `H0 ≤ 131072`.**
Primer descenso = primer cruce del coeficiente. -/
theorem cst_rhin {H0 : ℕ} (hH0 : H0 ≤ 131072) (hR : RhinHomogenea H0) {n k : ℕ}
    (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  cst_contador_desde (rhin_desde_mono hH0 (desde_homogenea hR)) hn hk hr

/-- La misma conclusión con la proposición general, con `u0` arbitrario. -/
theorem cst_rhin_proposicion {H0 : ℕ} (hH0 : H0 ≤ 131072) (hR : RhinProposicion H0)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  cst_rhin hH0 (homogenea_de_proposicion hR) hn hk hr

/-- Con un umbral `H0` cualquiera, el tramo `131072 ≤ k < H0` queda como hipótesis
finita aparte; `verificar_rhin_convergentes.py` la comprueba hasta 3010 cifras. -/
theorem desde_tramo {H0 : ℕ} (hR : RhinHomogenea H0)
    (htramo : ∀ k q : ℕ, 131072 ≤ k → k < H0 → 2 ^ k ≤ 2 * 3 ^ q → 3 ^ q < 2 ^ k →
      3 ^ q ≤ (2 ^ k - 3 ^ q) * k ^ 14) : RhinDesde 131072 := by
  intro k q hk hv hlt
  by_cases hH : H0 ≤ k
  · exact desde_homogenea hR k q hH hv hlt
  · exact htramo k q hk (by omega) hv hlt

theorem cst_rhin_tramo {H0 : ℕ} (hR : RhinHomogenea H0)
    (htramo : ∀ k q : ℕ, 131072 ≤ k → k < H0 → 2 ^ k ≤ 2 * 3 ^ q → 3 ^ q < 2 ^ k →
      3 ^ q ≤ (2 ^ k - 3 ^ q) * k ^ 14)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  cst_contador_desde (desde_tramo hR htramo) hn hk hr

/-- Un fallo de CST, si existe, tiene al menos once rachas impares. -/
theorem fallo_exige_once_rhin {H0 : ℕ} (hH0 : H0 ≤ 131072) (hR : RhinHomogenea H0)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) :
    11 ≤ rachas n k := by
  by_contra h
  have := (cst_rhin hH0 hR hn hk (by omega : rachas n k ≤ 10)).2
  omega

/-- La hipótesis nueva es más débil que la antigua. -/
theorem desde_de_entera (hR : RhinEntera) : RhinDesde 131072 :=
  rhin_desde_mono (Nat.zero_le _) (entera_iff_desde_cero.1 hR)

end OcelotasRhin

#print axioms OcelotasRhin.homogenea_de_proposicion
#print axioms OcelotasRhin.desde_homogenea
#print axioms OcelotasRhin.desde_proposicion
#print axioms OcelotasRhin.tiempo_diez_punto
#print axioms OcelotasRhin.tiempo_diez_desde
#print axioms OcelotasRhin.ocelotas_diez_desde
#print axioms OcelotasRhin.cst_contador_desde
#print axioms OcelotasRhin.cst_rhin
#print axioms OcelotasRhin.cst_rhin_proposicion
#print axioms OcelotasRhin.desde_tramo
#print axioms OcelotasRhin.cst_rhin_tramo
#print axioms OcelotasRhin.fallo_exige_once_rhin
#print axioms OcelotasRhin.desde_de_entera
