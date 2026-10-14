import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! # Perdices: una barrera para rangos locales de dos valuaciones.

El mapa y las paridades se definen directamente. La familia 256*k+231
realiza AB=1110 y conserva (v₂(n+1),v₂(n+5))=(3,2) entre fronteras.
La extensión a cualquier lista finita de formas afines se prueba por escrito
en PERFILES.md; no forma parte de este certificado.
-/

namespace PerdicesPerfiles

def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2
def A (n : ℕ) : ℕ := T n
def B (n : ℕ) : ℕ := T (T (T n))
def admiteA (n : ℕ) : Prop := n % 2 = 1
def admiteB (n : ℕ) : Prop :=
  n % 2 = 1 ∧ T n % 2 = 1 ∧ T (T n) % 2 = 0

def perfil (n : ℕ) : ℕ × ℕ := (padicValNat 2 (n + 1), padicValNat 2 (n + 5))
def rango (H : ℕ → ℝ) (F : ℕ × ℕ → ℝ) (n : ℕ) : ℝ := H n + F (perfil n)

theorem orden_de_restos {z a : ℕ}
    (h₀ : z % 2 ^ a = 0) (h₁ : z % 2 ^ (a + 1) ≠ 0) :
    padicValNat 2 z = a := by
  have hz : z ≠ 0 := by intro he; simp [he] at h₁
  have hle : a ≤ padicValNat 2 z :=
    (padicValNat_dvd_iff_le hz).mp (Nat.dvd_of_mod_eq_zero h₀)
  have hlt : ¬ a + 1 ≤ padicValNat 2 z := by
    intro he
    exact h₁ (Nat.mod_eq_zero_of_dvd ((padicValNat_dvd_iff_le hz).mpr he))
  omega

theorem paso_impar (n : ℕ) (h : n % 2 = 1) : T n = (3*n+1)/2 := by
  simp only [T, show n % 2 ≠ 0 by omega, if_false]

theorem paso_par (n : ℕ) (h : n % 2 = 0) : T n = n/2 := by
  simp only [T, h, if_true]

theorem orbita_familia (k : ℕ) :
    T (256*k+231) = 384*k+347 ∧
    T (384*k+347) = 576*k+521 ∧
    T (576*k+521) = 864*k+782 ∧
    T (864*k+782) = 432*k+391 := by
  have h₀ : (256*k+231) % 2 = 1 := by omega
  have h₁ : (384*k+347) % 2 = 1 := by omega
  have h₂ : (576*k+521) % 2 = 1 := by omega
  have h₃ : (864*k+782) % 2 = 0 := by omega
  rw [paso_impar _ h₀, paso_impar _ h₁, paso_impar _ h₂, paso_par _ h₃]
  omega

theorem familia_admisible (k : ℕ) :
    admiteA (256*k+231) ∧ admiteB (A (256*k+231)) := by
  obtain ⟨h₀, h₁, h₂, _⟩ := orbita_familia k
  simp only [admiteA, admiteB, A, h₀, h₁, h₂]
  omega

theorem familia_salida (k : ℕ) : B (A (256*k+231)) = 432*k+391 := by
  obtain ⟨h₀, h₁, h₂, h₃⟩ := orbita_familia k
  simp only [B, A, h₀, h₁, h₂, h₃]

theorem perfil_entrada (k : ℕ) : perfil (256*k+231) = (3,2) := by
  have h₀ : padicValNat 2 (256*k+231+1) = 3 := by
    apply orden_de_restos <;> norm_num <;> omega
  have h₁ : padicValNat 2 (256*k+231+5) = 2 := by
    apply orden_de_restos <;> norm_num <;> omega
  simp only [perfil, h₀, h₁]

theorem perfil_salida (k : ℕ) : perfil (432*k+391) = (3,2) := by
  have h₀ : padicValNat 2 (432*k+391+1) = 3 := by
    apply orden_de_restos <;> norm_num <;> omega
  have h₁ : padicValNat 2 (432*k+391+5) = 2 := by
    apply orden_de_restos <;> norm_num <;> omega
  simp only [perfil, h₀, h₁]

theorem familia_crece (k : ℕ) : 256*k+231 < B (A (256*k+231)) := by
  rw [familia_salida]
  omega

theorem rango_no_baja (H : ℕ → ℝ) (F : ℕ × ℕ → ℝ)
    (hH : Monotone H) (k : ℕ) :
    rango H F (256*k+231) ≤ rango H F (B (A (256*k+231))) := by
  have h := hH (Nat.le_of_lt (familia_crece k))
  rw [familia_salida] at h
  simp only [rango, familia_salida, perfil_entrada, perfil_salida]
  linarith

theorem no_rango_estricto_AB (H : ℕ → ℝ) (F : ℕ × ℕ → ℝ)
    (hH : Monotone H) :
    ¬ (∀ n, 0 < n → admiteA n → admiteB (A n) →
      rango H F (B (A n)) < rango H F n) := by
  intro h
  obtain ⟨hA, hB⟩ := familia_admisible 0
  have he := h 231 (by norm_num) hA hB
  exact (not_lt_of_ge (rango_no_baja H F hH 0)) he

theorem no_rango_por_bloques (H : ℕ → ℝ) (F : ℕ × ℕ → ℝ)
    (hH : Monotone H) :
    ¬ ((∀ n, 0 < n → admiteA n → rango H F (A n) < rango H F n) ∧
       (∀ n, 0 < n → admiteB n → rango H F (B n) < rango H F n)) := by
  rintro ⟨hA, hB⟩
  obtain ⟨ha, hb⟩ := familia_admisible 0
  have hpaso : A 231 = 347 := (orbita_familia 0).1
  have hpos : 0 < A 231 := by rw [hpaso]; norm_num
  have h₀ := hA 231 (by norm_num) ha
  have h₁ := hB (A 231) hpos hb
  exact (not_lt_of_ge (rango_no_baja H F hH 0)) (lt_trans h₁ h₀)

end PerdicesPerfiles

#print axioms PerdicesPerfiles.orden_de_restos
#print axioms PerdicesPerfiles.paso_impar
#print axioms PerdicesPerfiles.paso_par
#print axioms PerdicesPerfiles.orbita_familia
#print axioms PerdicesPerfiles.familia_admisible
#print axioms PerdicesPerfiles.familia_salida
#print axioms PerdicesPerfiles.perfil_entrada
#print axioms PerdicesPerfiles.perfil_salida
#print axioms PerdicesPerfiles.familia_crece
#print axioms PerdicesPerfiles.rango_no_baja
#print axioms PerdicesPerfiles.no_rango_estricto_AB
#print axioms PerdicesPerfiles.no_rango_por_bloques
