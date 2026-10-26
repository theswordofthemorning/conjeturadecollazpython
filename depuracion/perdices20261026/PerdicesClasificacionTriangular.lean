import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Núcleos algebraicos de la clasificación con F invertible y A ≠ B.
La reducción de matrices a estas coordenadas conserva prueba escrita. -/

namespace PerdicesClasificacionTriangular

theorem determinantes_iguales (a b : ℝ) (h1 : a * b = a * a)
    (h2 : a * b = b * b) : a = b := by
  nlinarith [sq_nonneg (a - b)]

theorem trazas_iguales (a b d : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (h : a * a - 2 * d = b * b - 2 * d) : a = b := by
  nlinarith

theorem resonancia (l m a b s t e f g : ℝ)
    (hm : m ≠ 0) (ht : t ≠ 0) (hab : a ≠ b)
    (hea : s * a + e * m = l * e + a * t)
    (hfa : s * a + f * m = l * e + b * t)
    (hga : s * a + g * m = l * f + a * t)
    (heb : s * b + e * m = l * f + b * t)
    (hfb : s * b + f * m = l * g + a * t)
    (hgb : s * b + g * m = l * g + b * t) :
    l = 2 * m ∧ s = 3 * t := by
  have hef : m * (e - f) = t * (a - b) := by nlinarith
  have hfg : m * (f - g) = t * (a - b) := by nlinarith
  have hefg : e - f = f - g := mul_left_cancel₀ hm (hef.trans hfg.symm)
  have hefgm := congrArg (fun x : ℝ => m * x) hefg
  have hsp : (s - 3 * t) * (a - b) = 0 := by nlinarith
  have hs : s = 3 * t := by
    have hh := (mul_eq_zero.mp hsp).resolve_right (sub_ne_zero.mpr hab)
    linarith
  have hefne : e - f ≠ 0 := by
    intro hzero
    rw [hzero, mul_zero] at hef
    exact (mul_ne_zero ht (sub_ne_zero.mpr hab)) hef.symm
  have hlp : (l - 2 * m) * (e - f) = 0 := by nlinarith
  have hl : l = 2 * m := by
    have hh := (mul_eq_zero.mp hlp).resolve_right hefne
    linarith
  exact ⟨hl, hs⟩

theorem imagen_comun (l a b s t q r e f g : ℝ)
    (hl : l ≠ 0) (hab : a ≠ b)
    (hea : s * a = l * e + a * q)
    (hfa : s * a = l * e + b * q)
    (hga : s * a = l * f + a * t)
    (heb : s * b = l * f + b * t)
    (hfb : s * b = l * g + a * r)
    (hgb : s * b = l * g + b * r) :
    t = s ∧ q = 0 ∧ r = 0 ∧ f = 0 ∧ l * e = s * a ∧ l * g = s * b := by
  have ht : (t - s) * (a - b) = 0 := by nlinarith
  have et : t = s := by
    have hh := (mul_eq_zero.mp ht).resolve_right (sub_ne_zero.mpr hab)
    linarith
  have hq : q * (a - b) = 0 := by nlinarith
  have eq : q = 0 := (mul_eq_zero.mp hq).resolve_right (sub_ne_zero.mpr hab)
  have hr : r * (a - b) = 0 := by nlinarith
  have er : r = 0 := (mul_eq_zero.mp hr).resolve_right (sub_ne_zero.mpr hab)
  have hf : l * f = 0 := by rw [et] at hga; nlinarith
  have ef : f = 0 := (mul_eq_zero.mp hf).resolve_left hl
  exact ⟨et, eq, er, ef, by simpa [eq] using hea.symm,
    by simpa [er] using hgb.symm⟩

theorem nucleo_comun (m a b s t q r e f g : ℝ)
    (hm : m ≠ 0) (hab : a ≠ b)
    (hea : q * a + e * m = a * t)
    (hfa : s * a + f * m = b * t)
    (hga : r * a + g * m = a * t)
    (heb : q * b + e * m = b * t)
    (hfb : s * b + f * m = a * t)
    (hgb : r * b + g * m = b * t) :
    s = -t ∧ q = t ∧ r = t ∧ e = 0 ∧ g = 0 ∧ m * f = t * (a + b) := by
  have hs : (s + t) * (a - b) = 0 := by nlinarith
  have es : s = -t := by
    have hh := (mul_eq_zero.mp hs).resolve_right (sub_ne_zero.mpr hab)
    linarith
  have hq : (q - t) * (a - b) = 0 := by nlinarith
  have eq : q = t := by
    have hh := (mul_eq_zero.mp hq).resolve_right (sub_ne_zero.mpr hab)
    linarith
  have hr : (r - t) * (a - b) = 0 := by nlinarith
  have er : r = t := by
    have hh := (mul_eq_zero.mp hr).resolve_right (sub_ne_zero.mpr hab)
    linarith
  have he : m * e = 0 := by rw [eq] at hea; nlinarith
  have ee : e = 0 := (mul_eq_zero.mp he).resolve_left hm
  have hg : m * g = 0 := by rw [er] at hga; nlinarith
  have eg : g = 0 := (mul_eq_zero.mp hg).resolve_left hm
  exact ⟨es, eq, er, ee, eg, by rw [es] at hfa; nlinarith⟩

theorem nilpotentes_iguales (a b u v : ℝ) (huv : 0 < u + v)
    (h1 : a * u = b * v) (h2 : b * u = a * v) : a = b := by
  have h : (a - b) * (u + v) = 0 := by nlinarith
  have hz := (mul_eq_zero.mp h).resolve_right (ne_of_gt huv)
  linarith

end PerdicesClasificacionTriangular

#print axioms PerdicesClasificacionTriangular.determinantes_iguales
#print axioms PerdicesClasificacionTriangular.trazas_iguales
#print axioms PerdicesClasificacionTriangular.resonancia
#print axioms PerdicesClasificacionTriangular.imagen_comun
#print axioms PerdicesClasificacionTriangular.nucleo_comun
#print axioms PerdicesClasificacionTriangular.nilpotentes_iguales
