import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.Data.Nat.Digits.Defs
import Mathlib.Tactic.NormNum

/-! Un retorno de observaciones en una trayectoria entera A/B creciente.
La generalizacion a listas arbitrarias de polinomios tiene prueba escrita. -/

namespace PerdicesRetornoFirma

def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

def A (n : ℕ) : ℕ := T n

def B (n : ℕ) : ℕ := T (T (T n))

def Firma (n : ℕ) : ℕ × ℕ := (padicValNat 2 (n + 1), padicValNat 2 (n + 5))

def Peso (n : ℕ) : ℕ := (Nat.digits 2 n).sum

theorem recorrido_entero :
    T 231 = 347 ∧ T 347 = 521 ∧ T 521 = 782 ∧ T 782 = 391 ∧
    A 231 = 347 ∧ B 347 = 391 := by decide

theorem valoracion_exacta {n k : ℕ} (hn : n ≠ 0)
    (hdiv : 2 ^ k ∣ n) (hno : ¬ 2 ^ (k + 1) ∣ n) : padicValNat 2 n = k := by
  have hinf := (padicValNat_dvd_iff_le_of_ne_one (p := 2) (by decide) hn).mp hdiv
  have hsup : ¬ k + 1 ≤ padicValNat 2 n := fun h =>
    hno ((padicValNat_dvd_iff_le_of_ne_one (p := 2) (by decide) hn).mpr h)
  omega

theorem firmas_iguales : Firma 231 = (3, 2) ∧ Firma 391 = (3, 2) := by
  have h232 : padicValNat 2 232 = 3 := valoracion_exacta (by decide) (by decide) (by decide)
  have h236 : padicValNat 2 236 = 2 := valoracion_exacta (by decide) (by decide) (by decide)
  have h392 : padicValNat 2 392 = 3 := valoracion_exacta (by decide) (by decide) (by decide)
  have h396 : padicValNat 2 396 = 2 := valoracion_exacta (by decide) (by decide) (by decide)
  simp [Firma, h232, h236, h392, h396]

theorem no_rango_monotono_en_firma {α : Type*} [Preorder α] (R : ℕ → α)
    (horden : ∀ n y, n ≤ y → Firma n = Firma y → R n ≤ R y)
    (hA : ∀ n, 0 < n → n % 2 = 1 → (A n) % 2 = 1 → R (A n) < R n)
    (hB : ∀ n, 0 < n → n % 8 = 3 → (B n) % 2 = 1 → R (B n) < R n) : False := by
  have ha : R 347 < R 231 := by simpa [A, T] using hA 231 (by decide) (by decide) (by decide)
  have hb : R 391 < R 347 := by simpa [B, T] using hB 347 (by decide) (by decide) (by decide)
  have he : Firma 231 = Firma 391 := firmas_iguales.1.trans firmas_iguales.2.symm
  have hm : R 231 ≤ R 391 := horden 231 391 (by decide) he
  exact (not_lt_of_ge hm) (lt_trans hb ha)

theorem no_perfil_monotono {α : Type*} [Preorder α] (F : (ℕ × ℕ) → ℕ → α)
    (hF : ∀ firma, Monotone (F firma))
    (hA : ∀ n, 0 < n → n % 2 = 1 → (A n) % 2 = 1 →
      F (Firma (A n)) (A n) < F (Firma n) n)
    (hB : ∀ n, 0 < n → n % 8 = 3 → (B n) % 2 = 1 →
      F (Firma (B n)) (B n) < F (Firma n) n) : False := by
  apply no_rango_monotono_en_firma (fun n => F (Firma n) n) ?_ hA hB
  intro n y hny he
  rw [he]
  exact hF (Firma y) hny

theorem recorrido_con_mas_unos :
    A 8423 = 12635 ∧ T 12635 = 18953 ∧ T 18953 = 28430 ∧
    T 28430 = 14215 ∧ B 12635 = 14215 := by decide

theorem firmas_y_pesos :
    Firma 8423 = (3, 2) ∧ Firma 14215 = (3, 2) ∧
    Peso 231 = 6 ∧ Peso 391 = 5 ∧ Peso 8423 = 7 ∧ Peso 14215 = 9 := by
  have h8424 : padicValNat 2 8424 = 3 := valoracion_exacta (by decide) (by decide) (by decide)
  have h8428 : padicValNat 2 8428 = 2 := valoracion_exacta (by decide) (by decide) (by decide)
  have h14216 : padicValNat 2 14216 = 3 := valoracion_exacta (by decide) (by decide) (by decide)
  have h14220 : padicValNat 2 14220 = 2 := valoracion_exacta (by decide) (by decide) (by decide)
  refine ⟨?_, ?_, by decide, by decide, by decide, by decide⟩
  · simp [Firma, h8424, h8428]
  · simp [Firma, h14216, h14220]

theorem no_monotonia_digital {α : Type*} [Preorder α] (R : ℕ → α)
    (hperfil : ∀ firma,
      (∀ n y, Firma n = firma → Firma y = firma → n ≤ y → Peso n ≤ Peso y → R n ≤ R y) ∨
      (∀ n y, Firma n = firma → Firma y = firma → n ≤ y → Peso y ≤ Peso n → R n ≤ R y))
    (hA : ∀ n, 0 < n → n % 2 = 1 → (A n) % 2 = 1 → R (A n) < R n)
    (hB : ∀ n, 0 < n → n % 8 = 3 → (B n) % 2 = 1 → R (B n) < R n) : False := by
  rcases hperfil (3, 2) with hmas | hmenos
  · have ha : R 12635 < R 8423 := by
      simpa [A, T] using hA 8423 (by decide) (by decide) (by decide)
    have hb : R 14215 < R 12635 := by
      simpa [B, T] using hB 12635 (by decide) (by decide) (by decide)
    have hp : Peso 8423 ≤ Peso 14215 := by rw [firmas_y_pesos.2.2.2.2.1, firmas_y_pesos.2.2.2.2.2]; decide
    have hm := hmas 8423 14215 firmas_y_pesos.1 firmas_y_pesos.2.1 (by decide) hp
    exact (not_lt_of_ge hm) (lt_trans hb ha)
  · have ha : R 347 < R 231 := by
      simpa [A, T] using hA 231 (by decide) (by decide) (by decide)
    have hb : R 391 < R 347 := by
      simpa [B, T] using hB 347 (by decide) (by decide) (by decide)
    have hp : Peso 391 ≤ Peso 231 := by rw [firmas_y_pesos.2.2.1, firmas_y_pesos.2.2.2.1]; decide
    have hm := hmenos 231 391 firmas_iguales.1 firmas_iguales.2 (by decide) hp
    exact (not_lt_of_ge hm) (lt_trans hb ha)

end PerdicesRetornoFirma

#print axioms PerdicesRetornoFirma.recorrido_entero
#print axioms PerdicesRetornoFirma.valoracion_exacta
#print axioms PerdicesRetornoFirma.firmas_iguales
#print axioms PerdicesRetornoFirma.no_rango_monotono_en_firma
#print axioms PerdicesRetornoFirma.no_perfil_monotono
#print axioms PerdicesRetornoFirma.recorrido_con_mas_unos
#print axioms PerdicesRetornoFirma.firmas_y_pesos
#print axioms PerdicesRetornoFirma.no_monotonia_digital
