import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

/-! Núcleo algebraico de la estimación de la población protegida.
Las cuentas por rotaciones y el máximo binomial tienen prueba escrita;
no se introducen como teoremas orbitales en este módulo. -/

namespace PerdicesProtegidos

def peso (K s j : ℕ) : ℕ := K.choose j * s ^ j * (K - s) ^ (K - j)

theorem recurrencia_peso {K s j : ℕ} (hj : j < K) :
    (j + 1) * (K - s) * peso K s (j + 1) =
      (K - j) * s * peso K s j := by
  have hpot : K - j = K - (j + 1) + 1 := by omega
  have hc := Nat.choose_succ_right_eq K j
  unfold peso
  calc
    (j + 1) * (K - s) * (K.choose (j + 1) * s ^ (j + 1) *
        (K - s) ^ (K - (j + 1))) =
      (K.choose (j + 1) * (j + 1)) * s ^ (j + 1) * (K - s) ^ (K - j) := by
        rw [hpot, pow_succ]
        ring
    _ = (K.choose j * (K - j)) * s ^ (j + 1) * (K - s) ^ (K - j) := by rw [hc]
    _ = (K - j) * s * (K.choose j * s ^ j * (K - s) ^ (K - j)) := by
        rw [pow_succ]
        ring

theorem peso_crece {K s j : ℕ} (hs : s < K) (hj : j < s) :
    peso K s j ≤ peso K s (j + 1) := by
  have hrec := recurrencia_peso (s := s) (lt_trans hj hs)
  have hks : K - s + s = K := Nat.sub_add_cancel (le_of_lt hs)
  have hkj : K - j + j = K := Nat.sub_add_cancel (le_of_lt (lt_trans hj hs))
  have hcoef : (j + 1) * (K - s) ≤ (K - j) * s := by nlinarith
  have hmul := Nat.mul_le_mul_right (peso K s j) hcoef
  have hpos : 0 < (j + 1) * (K - s) :=
    Nat.mul_pos (by omega) (Nat.sub_pos_of_lt hs)
  nlinarith only [hrec, hmul, hpos]

theorem peso_decrece {K s j : ℕ} (hs : s < K) (hjs : s ≤ j) (hj : j < K) :
    peso K s (j + 1) ≤ peso K s j := by
  have hrec := recurrencia_peso (s := s) hj
  have hks : K - s + s = K := Nat.sub_add_cancel (le_of_lt hs)
  have hkj : K - j + j = K := Nat.sub_add_cancel (le_of_lt hj)
  have hcoef : (K - j) * s ≤ (j + 1) * (K - s) := by nlinarith
  have hmul := Nat.mul_le_mul_right (peso K s j) hcoef
  have hpos : 0 < (j + 1) * (K - s) :=
    Nat.mul_pos (by omega) (Nat.sub_pos_of_lt hs)
  nlinarith only [hrec, hmul, hpos]

theorem peso_maximo {K s : ℕ} (hs : s < K) (j : ℕ) (hj : j ≤ K) :
    peso K s j ≤ peso K s s := by
  have sube : ∀ d i, i + d ≤ s → peso K s i ≤ peso K s (i + d) := by
    intro d
    induction d with
    | zero => intro i hi; simp
    | succ d ih =>
      intro i hi
      have h1 := ih i (by omega)
      have h2 := peso_crece hs (show i + d < s by omega)
      exact h1.trans (by simpa [Nat.add_assoc] using h2)
  have baja : ∀ d i, s ≤ i → i + d ≤ K → peso K s (i + d) ≤ peso K s i := by
    intro d
    induction d with
    | zero => intro i hi hK; simp
    | succ d ih =>
      intro i hi hK
      have h1 := ih i hi (by omega)
      have h2 := peso_decrece hs (show s ≤ i + d by omega) (show i + d < K by omega)
      have h3 : peso K s (i + (d + 1)) ≤ peso K s (i + d) := by
        simpa [Nat.add_assoc] using h2
      exact h3.trans h1
  by_cases hjs : j ≤ s
  · simpa [Nat.add_sub_of_le hjs] using sube (s - j) j (by omega)
  · simpa [Nat.add_sub_of_le (show s ≤ j by omega)] using
      baja (j - s) s (le_refl s) (by omega)

theorem suma_pesos {K s : ℕ} (hs : s ≤ K) :
    ∑ j ∈ Finset.range (K + 1), peso K s j = K ^ K := by
  have h := add_pow s (K - s) K
  rw [Nat.add_sub_of_le hs] at h
  simpa [peso, mul_comm, mul_left_comm, mul_assoc] using h.symm

theorem cota_modo {K s : ℕ} (hs : s < K) :
    K ^ K ≤ (K + 1) * (K.choose s * s ^ s * (K - s) ^ (K - s)) := by
  rw [← suma_pesos (le_of_lt hs)]
  calc
    ∑ j ∈ Finset.range (K + 1), peso K s j ≤
        ∑ _j ∈ Finset.range (K + 1), peso K s s := by
      exact Finset.sum_le_sum fun j hj => peso_maximo hs j (by simpa using Nat.le_of_lt_succ (Finset.mem_range.mp hj))
    _ = (K + 1) * (K.choose s * s ^ s * (K - s) ^ (K - s)) := by simp [peso]

theorem exponente_cinco_octavos : (3 : ℕ) ^ 5 < 2 ^ 8 := by norm_num

theorem exponente_diecisiete : (3 : ℕ) ^ 17 < 2 ^ 27 := by norm_num

theorem crecimiento_estricto :
    (8 : ℕ) ^ 27 * 16 ^ 27 < 31 ^ 27 * 5 ^ 17 * 3 ^ 10 := by norm_num

theorem potencia_ocho : (3 / 4 : ℚ) ^ 8 < 1 / 8 := by norm_num

/-- Transfiere tres desigualdades de conteo ponderado; no presupone
la cota final ni construye aquí las cuentas de palabras. -/
theorem transferencia_pesos {K A N C w x z v : ℚ}
    (hK : 0 ≤ K) (hw : 0 < w) (hv : 0 ≤ v)
    (hciclo : C ≤ K * N)
    (hmodo : x ≤ (K + 1) * C * w)
    (hcola : A * w * z ≤ x * v) :
    A * z ≤ K * (K + 1) * N * v := by
  have h1 := mul_le_mul_of_nonneg_right hciclo (show 0 ≤ (K + 1) * w by positivity)
  have h2 : x ≤ K * (K + 1) * N * w := by nlinarith only [hmodo, h1]
  have h3 := mul_le_mul_of_nonneg_right h2 hv
  have h4 : (A * z) * w ≤ (K * (K + 1) * N * v) * w := by
    nlinarith only [hcola, h3]
  exact (mul_le_mul_iff_left₀ hw).mp (by simpa [mul_comm] using h4)

/-- Convierte la cota sin divisiones en una fracción de la población. -/
theorem fraccion_desde_cuenta {A N z v c u : ℚ}
    (hN : 0 < N) (hz : 0 < z) (hu : 0 ≤ u)
    (h : A * z ≤ c * N * v) :
    u * A / N ≤ c * (u * v) / z := by
  apply (div_le_div_iff₀ hN hz).2
  have hh := mul_le_mul_of_nonneg_left h hu
  nlinarith only [hh]

theorem identidad_frontera {N M B : ℚ}
    (hN : 0 < N) (h : N = 2 * M - B) :
    1 - (2 * (M - B) / N) = B / N := by
  field_simp
  linarith

theorem piso_frontera {N M B : ℚ}
    (hN : 0 < N) (h : N = 2 * M - B)
    (hcrece : 16 * N ≤ 31 * M) :
    1 / 31 ≤ B / N := by
  apply (div_le_div_iff₀ (by norm_num : (0 : ℚ) < 31) hN).2
  nlinarith only [h, hcrece]

theorem piso_certificado {G G1 q : ℚ}
    (hG : 0 ≤ G) (hsub : G ≤ G1) (hq : 0 ≤ q) :
    1 - G1 ≤ 1 - G * (1 - q) := by
  have h := mul_nonneg hG hq
  nlinarith only [h, hsub]

theorem piso_todas_longitudes {G G1 q : ℚ}
    (hG : 0 ≤ G) (hsub : G ≤ G1) (hq : 0 ≤ q)
    (hpiso : 1 / 31 ≤ 1 - G1) :
    1 / 31 ≤ 1 - G * (1 - q) :=
  hpiso.trans (piso_certificado hG hsub hq)

theorem ventana_larga_certificado {G q K : ℚ}
    (hG : 0 ≤ G) (hq : 0 ≤ q) (hreserva : G ≤ 1 / (K + 1)) :
    1 - 1 / (K + 1) ≤ 1 - G * (1 - q) :=
  piso_certificado hG hreserva hq

end PerdicesProtegidos

#print axioms PerdicesProtegidos.exponente_cinco_octavos
#print axioms PerdicesProtegidos.recurrencia_peso
#print axioms PerdicesProtegidos.peso_crece
#print axioms PerdicesProtegidos.peso_decrece
#print axioms PerdicesProtegidos.peso_maximo
#print axioms PerdicesProtegidos.suma_pesos
#print axioms PerdicesProtegidos.cota_modo
#print axioms PerdicesProtegidos.exponente_diecisiete
#print axioms PerdicesProtegidos.crecimiento_estricto
#print axioms PerdicesProtegidos.potencia_ocho
#print axioms PerdicesProtegidos.transferencia_pesos
#print axioms PerdicesProtegidos.fraccion_desde_cuenta
#print axioms PerdicesProtegidos.identidad_frontera
#print axioms PerdicesProtegidos.piso_frontera
#print axioms PerdicesProtegidos.piso_certificado
#print axioms PerdicesProtegidos.piso_todas_longitudes
#print axioms PerdicesProtegidos.ventana_larga_certificado
