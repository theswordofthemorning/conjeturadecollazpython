import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Optimo de la relajacion de tamano con ventanas solapadas.
La extraccion de ventanas orbitales y el testigo finito se contrastan
por separado. No se afirma una obstruccion al reloj universal. -/

namespace PerdicesVentanasSimultaneas

theorem ventana_iff {n x m d e q r N : ℚ}
    (hm : 0 < m) (hd : 0 < d) (hq : 0 < q)
    (hcamino : m * x = d * n + e) :
    N ≤ q * x + r ↔ (m * (N - r) - q * e) / (q * d) ≤ n := by
  rw [div_le_iff₀ (mul_pos hq hd)]
  have hi : q * (m * x) = q * (d * n + e) := congrArg (q * ·) hcamino
  constructor
  · intro h
    have hh := mul_le_mul_of_nonneg_left h (le_of_lt hm)
    nlinarith only [hi, hh]
  · intro h
    by_contra hn
    have hh := mul_lt_mul_of_pos_left (lt_of_not_ge hn) hm
    nlinarith only [hi, hh, h]

theorem todas_ventanas_iff {ι : Type*} {n : ℚ}
    (x m d e q r N : ι → ℚ)
    (hm : ∀ i, 0 < m i) (hd : ∀ i, 0 < d i) (hq : ∀ i, 0 < q i)
    (hcamino : ∀ i, m i * x i = d i * n + e i) :
    (∀ i, N i ≤ q i * x i + r i) ↔
      ∀ i, (m i * (N i - r i) - q i * e i) / (q i * d i) ≤ n := by
  exact forall_congr' fun i => ventana_iff (hm i) (hd i) (hq i) (hcamino i)

theorem maximo_exacto {ι : Type*} (a : ι → ℚ) (j : ι) (h n : ℚ)
    (hmayor : ∀ i, a i ≤ h) (hig : a j = h) :
    (∀ i, a i ≤ n) ↔ h ≤ n := by
  constructor
  · intro hn
    simpa [hig] using hn j
  · intro hn i
    exact (hmayor i).trans hn

theorem frontera_A_entera (x : ℤ) :
    (∃ y : ℤ, 2 * y = 3 * x + 1) ↔ 2 ∣ x + 1 := by
  constructor
  · rintro ⟨y, hy⟩
    exact ⟨y - x, by omega⟩
  · rintro ⟨k, hk⟩
    exact ⟨x + k, by omega⟩

theorem frontera_B_entera (x : ℤ) :
    (∃ y : ℤ, 8 * y = 9 * x + 5) ↔ 8 ∣ x + 5 := by
  constructor
  · rintro ⟨y, hy⟩
    exact ⟨y - x, by omega⟩
  · rintro ⟨k, hk⟩
    exact ⟨x + k, by omega⟩

theorem residuo_B (x : ℤ) : 8 ∣ x + 5 ↔ x % 8 = 3 := by omega

theorem barrera_sufijo_AB {b n x : ℕ}
    (ha : 2 * x = 3 * n + 1) (hb : 8 ^ b ≤ x + 5) :
    2 * 8 ^ b ≤ 3 * n + 11 := by omega

theorem reloj_AB {b n ell : ℕ}
    (hb : 2 * 8 ^ b ≤ 3 * n + 11) (hell : n + 5 ≤ 2 ^ ell) :
    3 * b + 1 ≤ ell + 1 := by
  by_contra hn
  have hexp : ell + 2 ≤ 3 * b + 1 := by omega
  have hpot : 2 ^ (ell + 2) ≤ 2 ^ (3 * b + 1) :=
    Nat.pow_le_pow_right (by decide) hexp
  have hi : (2 : ℕ) ^ (3 * b + 1) = 2 * 8 ^ b := by
    rw [pow_add, pow_mul]
    norm_num
    omega
  have hj : (2 : ℕ) ^ (ell + 2) = 4 * 2 ^ ell := by
    rw [pow_add]
    norm_num
    omega
  rw [hi, hj] at hpot
  omega

end PerdicesVentanasSimultaneas

#print axioms PerdicesVentanasSimultaneas.ventana_iff
#print axioms PerdicesVentanasSimultaneas.todas_ventanas_iff
#print axioms PerdicesVentanasSimultaneas.maximo_exacto
#print axioms PerdicesVentanasSimultaneas.frontera_A_entera
#print axioms PerdicesVentanasSimultaneas.frontera_B_entera
#print axioms PerdicesVentanasSimultaneas.residuo_B
#print axioms PerdicesVentanasSimultaneas.barrera_sufijo_AB
#print axioms PerdicesVentanasSimultaneas.reloj_AB
