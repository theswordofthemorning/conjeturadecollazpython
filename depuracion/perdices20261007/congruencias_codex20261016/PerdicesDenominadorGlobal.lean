import Mathlib.Data.Nat.GCD.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

/-! Criterio afin reducido y obstruccion de A B^b.
La conexion con palabras arbitrarias y el corolario logaritmico se escriben
en DENOMINADOR_GLOBAL.md. No se supone ni se demuestra el reloj uniforme. -/

namespace PerdicesDenominadorGlobal

theorem divisibilidad_reducida {n y m d e g q r : ℕ}
    (hc : Nat.Coprime m g) (hd : d = m + g * q) (he : e = g * r)
    (h : m * y = d * n + e) : m ∣ q * n + r := by
  have hi : m * n + g * (q * n + r) = m * y := by
    rw [hd, he] at h
    nlinarith only [h]
  apply hc.dvd_of_dvd_mul_left
  exact (Nat.dvd_add_iff_right (dvd_mul_right m n)).mpr
    (hi ▸ dvd_mul_right m y)

theorem barrera_reducida {n y m d e g q r : ℕ}
    (hc : Nat.Coprime m g) (hd : d = m + g * q) (he : e = g * r)
    (h : m * y = d * n + e) (hn : 0 < n) (hq : 0 < q)
    (hr : r ≤ 5 * q) : m ≤ q * (n + 5) := by
  have hp : 0 < q * n + r := by positivity
  have hb := Nat.le_of_dvd hp (divisibilidad_reducida hc hd he h)
  nlinarith only [hb, hr]

theorem nueve_domina_ocho (b : ℕ) : 8 ^ b ≤ 9 ^ b :=
  Nat.pow_le_pow_left (by decide) b

theorem familia_sin_cancelacion (b q e : ℕ)
    (hq : q + 2 * 8 ^ b = 3 * 9 ^ b)
    (he : e + 10 * 8 ^ b = 11 * 9 ^ b) : Nat.Coprime q e := by
  have hq2 : Nat.Coprime q 2 := by
    have hc : Nat.Coprime (3 * 9 ^ b) 2 :=
      (by decide : Nat.Coprime 3 2).mul_left
        ((by decide : Nat.Coprime 9 2).pow_left b)
    rw [← hq] at hc
    exact (Nat.coprime_add_mul_left_left q 2 (8 ^ b)).mp hc
  have hq8 : Nat.Coprime q (8 * 8 ^ b) := by
    have hc : Nat.Coprime q 8 := by simpa using hq2.pow_right 3
    exact hc.mul_right (hc.pow_right b)
  have hi : 3 * e + 8 * 8 ^ b = 11 * q := by omega
  have hgq := Nat.gcd_dvd_left q e
  have hge := Nat.gcd_dvd_right q e
  have hgv : Nat.gcd q e ∣ 8 * 8 ^ b := by
    apply (Nat.dvd_add_iff_right (dvd_mul_of_dvd_right hge 3)).mpr
    rw [hi]
    exact dvd_mul_of_dvd_right hgq 11
  have hc := hq8.coprime_dvd_left hgq
  exact hc.eq_one_of_dvd hgv

theorem familia_denominador_grande (k q : ℕ)
    (hq : q + 2 * 8 ^ (k + 3) = 3 * 9 ^ (k + 3)) :
    2 * 8 ^ (k + 3) < q := by
  have hi : 4 * 8 ^ (k + 3) < 3 * 9 ^ (k + 3) := by
    clear q hq
    induction k with
    | zero => norm_num
    | succ k ih =>
        rw [show k + 1 + 3 = (k + 3) + 1 by omega,
          pow_succ (8 : ℕ) (k + 3), pow_succ (9 : ℕ) (k + 3)]
        nlinarith [show 0 < 9 ^ (k + 3) from Nat.pow_pos (by decide)]
  omega

end PerdicesDenominadorGlobal

#print axioms PerdicesDenominadorGlobal.divisibilidad_reducida
#print axioms PerdicesDenominadorGlobal.barrera_reducida
#print axioms PerdicesDenominadorGlobal.nueve_domina_ocho
#print axioms PerdicesDenominadorGlobal.familia_sin_cancelacion
#print axioms PerdicesDenominadorGlobal.familia_denominador_grande
