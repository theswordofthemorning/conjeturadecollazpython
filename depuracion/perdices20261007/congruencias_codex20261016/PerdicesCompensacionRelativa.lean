import PerdicesRelojRachas
import Mathlib.Algebra.Order.Archimedean.Real.Basic

/-! Obstruccion en la relajacion, no contraejemplos orbitales.
Una reserva proporcional, incluso sumada a una constante, no da reloj.
La repeticion orbital AB se trata aparte y tiene una barrera entera. -/

namespace PerdicesCompensacionRelativa

open PerdicesTransporteImpar PerdicesRelojRachas

def modelo : ℕ → List (Bloque × ℚ)
  | 0 => []
  | m + 1 => (.a, 1) :: (.b, 3) :: modelo m

def ReservaRelativa (eta k : ℚ) : ℚ → List (Bloque × ℚ) → Prop
  | _, [] => True
  | h, (p, d) :: rs =>
      0 < d ∧ d + k ≤ (1 - eta) * h ∧
        ReservaRelativa eta k (h + gamma p * d) rs

theorem coste_modelo (m : ℕ) : coste (modelo m) = 4 * (m : ℚ) := by
  induction m with
  | zero => simp [modelo, coste]
  | succ m ih => simp only [modelo, coste, ih, Nat.cast_add, Nat.cast_one]; ring

theorem longitud_modelo (m : ℕ) : (modelo m).length = 2 * m := by
  induction m with
  | zero => rfl
  | succ m ih => simp [modelo, ih]; omega

theorem reserva_modelo {eta k h : ℚ} (he : eta < 1)
    (hh : 3 + k ≤ (1 - eta) * h) (m : ℕ) :
    ReservaRelativa eta k h (modelo m) := by
  induction m generalizing h with
  | zero => trivial
  | succ m ih =>
      simp only [modelo, ReservaRelativa, gamma]
      refine ⟨by norm_num, by linarith, by norm_num, ?_, ?_⟩
      · nlinarith
      · apply ih
        nlinarith

theorem reserva_admisible {eta k h : ℚ} {rs : List (Bloque × ℚ)}
    (he : 0 ≤ eta) (hk : 0 ≤ k) (hh : 0 ≤ h)
    (hr : ReservaRelativa eta k h rs) : Admisible h rs := by
  induction rs generalizing h with
  | nil => trivial
  | cons r rs ih =>
      obtain ⟨p, d⟩ := r
      obtain ⟨hd, hc, ht⟩ := hr
      have hg : 0 ≤ gamma p := by cases p <;> norm_num [gamma]
      refine ⟨le_of_lt hd, ?_, ih (by nlinarith) ht⟩
      nlinarith [mul_nonneg he hh]

theorem sin_reloj_relativo {eta k h : ℚ}
    (he : eta < 1) (hh : 3 + k ≤ (1 - eta) * h) (c d : ℝ) :
    ∃ m : ℕ, ReservaRelativa eta k h (modelo m) ∧
      c * (h : ℝ) + d < (coste (modelo m) : ℝ) := by
  obtain ⟨m, hm⟩ := exists_nat_gt (c * (h : ℝ) + d)
  refine ⟨m + 1, reserva_modelo he hh _, ?_⟩
  rw [coste_modelo]
  push_cast
  have hn : 0 ≤ (m : ℝ) := Nat.cast_nonneg m
  linarith

theorem identidad_modelo (m : ℕ) (h : ℚ) :
    descuento h (modelo m) + 4 * (m : ℚ) =
      coeficiente ((modelo m).map Prod.fst) * h := by
  have ht := identidad_defectos (modelo m) h
  rw [coste_modelo] at ht
  linarith

theorem criterio_residual {rs : List (Bloque × ℚ)} {h c d : ℚ} :
    coste rs ≤ c * h + d ↔
      (coeficiente (rs.map Prod.fst) - c) * h - d ≤ descuento h rs := by
  have ht := identidad_defectos rs h
  constructor <;> intro ha <;> nlinarith only [ht, ha]

theorem reserva_uno_vacia {k h : ℚ} {rs : List (Bloque × ℚ)}
    (hk : 0 ≤ k) (hr : ReservaRelativa 1 k h rs) : rs = [] := by
  cases rs with
  | nil => rfl
  | cons r rs =>
      obtain ⟨p, d⟩ := r
      obtain ⟨hd, hc, ht⟩ := hr
      norm_num at hc
      linarith

def palabra : ℕ → List Bloque
  | 0 => []
  | m + 1 => .a :: .b :: palabra m

theorem balance_orbital_ab {m n x : ℕ} (h : Camino (palabra m) n x) :
    16 ^ m * (11 * x + 19) = 27 ^ m * (11 * n + 19) := by
  induction m generalizing n with
  | zero => cases h; simp
  | succ m ih =>
      cases h with
      | @cons _ _ _ y _ ha ht =>
          cases ht with
          | @cons _ _ _ z _ hb hr =>
              have hi := ih hr
              have hp : 16 * (11 * z + 19) = 27 * (11 * n + 19) := by
                simp only [Paso, N, D, E] at ha hb
                omega
              rw [pow_succ, pow_succ]
              nlinarith [congrArg (fun t => 16 * t) hi,
                congrArg (fun t => 27 ^ m * t) hp]

theorem divisibilidad_orbital_ab {m n x : ℕ} (h : Camino (palabra m) n x) :
    16 ^ m ∣ 11 * n + 19 := by
  have hb := balance_orbital_ab h
  have hc : Nat.Coprime (16 ^ m) (27 ^ m) :=
    (by decide : Nat.Coprime 16 27).pow m m
  apply hc.dvd_of_dvd_mul_left
  rw [← hb]
  exact dvd_mul_right _ _

theorem barrera_orbital_ab {m n x : ℕ} (h : Camino (palabra m) n x) :
    16 ^ m ≤ 11 * n + 19 :=
  Nat.le_of_dvd (by omega) (divisibilidad_orbital_ab h)

end PerdicesCompensacionRelativa

#print axioms PerdicesCompensacionRelativa.coste_modelo
#print axioms PerdicesCompensacionRelativa.longitud_modelo
#print axioms PerdicesCompensacionRelativa.reserva_modelo
#print axioms PerdicesCompensacionRelativa.reserva_admisible
#print axioms PerdicesCompensacionRelativa.sin_reloj_relativo
#print axioms PerdicesCompensacionRelativa.identidad_modelo
#print axioms PerdicesCompensacionRelativa.criterio_residual
#print axioms PerdicesCompensacionRelativa.reserva_uno_vacia
#print axioms PerdicesCompensacionRelativa.balance_orbital_ab
#print axioms PerdicesCompensacionRelativa.divisibilidad_orbital_ab
#print axioms PerdicesCompensacionRelativa.barrera_orbital_ab
