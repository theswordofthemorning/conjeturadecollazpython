import OcelotasRachas

/-! # Ocelotas: cota geométrica para una cantidad arbitraria de rachas

Esta interfaz sustituye la expansión de todos los pisos por una sola
comparación de potencias enteras. No cierra por sí sola una nueva cantidad
de rachas ni presupone una cota trascendente.
-/

namespace OcelotasGeometrica

open OcelotasRachas

theorem cota_geometrica (r m : ℕ) :
    3 * 5 ^ r * cota r m + 5 ^ (r + 1) * m ≤ 5 * 8 ^ r * m := by
  induction r with
  | zero => simp [cota]
  | succ r ih =>
    have hd : 5 * cota (r + 1) m ≤ 5 * m + 8 * cota r m := by
      have h := Nat.div_mul_le_self (5 * m + 8 * cota r m - 1) 5
      simp only [cota]
      omega
    have hpaso := Nat.mul_le_mul_left (3 * 5 ^ r) hd
    have hprev := Nat.mul_le_mul_left 8 ih
    simp only [pow_succ] at *
    nlinarith

theorem cota_lineal {r A : ℕ}
    (hA : 5 * 8 ^ r ≤ (3 * A + 5) * 5 ^ r) (m : ℕ) :
    cota r m ≤ A * m := by
  have h := cota_geometrica r m
  have hcoef := Nat.mul_le_mul_right m hA
  have hpos : 0 < 5 ^ r := by positivity
  rw [pow_succ] at h
  nlinarith

example (m : ℕ) : cota 18 m ≤ 7869 * m :=
  cota_lineal (by decide +kernel) m

theorem cota_setenta_y_cinco (m : ℕ) : cota 75 m ≤ 3395059960557476 * m :=
  cota_lineal (by decide +kernel) m

end OcelotasGeometrica

#print axioms OcelotasGeometrica.cota_geometrica
#print axioms OcelotasGeometrica.cota_lineal
#print axioms OcelotasGeometrica.cota_setenta_y_cinco
