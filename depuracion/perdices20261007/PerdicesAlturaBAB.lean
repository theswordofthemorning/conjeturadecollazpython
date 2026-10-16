import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Si falla P2 en BAB, las dos partes impares de 3^b*r+1 tienen producto
excepcionalmente pequeño. Se certifica la reducción bajo las identidades
aritméticas escritas en ALTURA_BAB.md; no se supone la conjetura abc.
También se certifica el cierre lineal para epsilon=7/17 y K=2*ell.
-/

namespace PerdicesAlturaBAB

theorem producto_de_fallo {A D U V R S K H : ℕ}
    (hd : 0 < D) (hs : 0 < S)
    (hsemilla : A*(U*R+1) ≤ D*H)
    (hdivision : K*S = V*R+1)
    (hfallo : 2*A*H^4 < U*K^2)
    (hescala : 1024*D^4 ≤ A^5) (hvr : 3 ≤ V*R) :
    1024*U^3*(R*S)^2 < V^2 := by
  have hx : A*(U*R) ≤ D*H :=
    (Nat.mul_le_mul_left A (Nat.le_succ _)).trans hsemilla
  have hp := Nat.mul_le_mul_left (2*A) (pow_le_pow_left' hx 4)
  have hf := Nat.mul_lt_mul_of_pos_left hfallo (pow_pos hd 4)
  have h1 : 2*A^5*U^4*R^4 < D^4*U*K^2 := by
    nlinarith only [hp, hf]
  have h2 := Nat.mul_lt_mul_of_pos_right h1 (pow_pos hs 2)
  have he : K^2*S^2 = (V*R+1)^2 := by rw [← mul_pow, hdivision]
  have ht := Nat.mul_le_mul_right (V*R) hvr
  have hc : (V*R+1)^2 ≤ 2*V^2*R^2 := by nlinarith only [ht, hvr]
  have h3 := Nat.mul_le_mul_left (D^4*U) hc
  have h4 : (2*U*R^2)*(A^5*U^3*(R*S)^2) <
      (2*U*R^2)*(D^4*V^2) := by
    calc
      _ < D^4*U*(K^2*S^2) := by nlinarith only [h2]
      _ = D^4*U*(V*R+1)^2 := by rw [he]
      _ ≤ _ := by nlinarith only [h3]
  have h5 := Nat.lt_of_mul_lt_mul_left h4
  have h6 := Nat.mul_le_mul_right (U^3*(R*S)^2) hescala
  have h7 : D^4*(1024*U^3*(R*S)^2) < D^4*V^2 := by
    nlinarith only [h5, h6]
  exact Nat.lt_of_mul_lt_mul_left h7

theorem escala (a : ℕ) : 1024*((9 : ℕ)^a)^4 ≤ (2^(3*a+2))^5 := by
  have h := pow_le_pow_left' (by norm_num : (9 : ℕ)^4 ≤ 2^15) a
  calc
    _ = 1024*(9^4)^a := by rw [← pow_mul, ← pow_mul]; congr 2; omega
    _ ≤ 1024*(2^15)^a := Nat.mul_le_mul_left _ h
    _ = 2^(15*a+10) := by rw [pow_add, pow_mul]; norm_num; ring
    _ = _ := by rw [← pow_mul]; congr 1; omega

theorem fallo_producto {a b ell k r s : ℕ}
    (hb : 1 ≤ b) (hr : 1 ≤ r) (hs : 1 ≤ s)
    (hsemilla : 2^(3*a+2)*(2^b*r+1) ≤ 9^a*2^ell)
    (hdivision : 2^k*s = 3^b*r+1)
    (hfallo : 3*a+3+4*ell < b+2*k) :
    1024*2^(3*b)*(r*s)^2 < 3^(2*b) := by
  have hf : (2 : ℕ)^(3*a+3+4*ell) < 2^(b+2*k) :=
    (Nat.pow_lt_pow_iff_right (by decide : 1 < 2)).mpr hfallo
  have hl : 2*2^(3*a+2)*(2^ell)^4 = (2 : ℕ)^(3*a+3+4*ell) := by
    calc
      _ = 2^(1+(3*a+2)+ell*4) := by
        rw [pow_add (2 : ℕ) (1+(3*a+2)) (ell*4), pow_mul (2 : ℕ) ell 4,
          pow_add (2 : ℕ) 1 (3*a+2), pow_one]
      _ = _ := by congr 1; omega
  have hrp : (2 : ℕ)^b*(2^k)^2 = 2^(b+2*k) := by
    rw [← pow_mul, ← pow_add]
    congr 1
    omega
  have hv : 3 ≤ (3 : ℕ)^b := by
    simpa using Nat.pow_le_pow_right (by decide : 1 ≤ 3) hb
  have hvr : 3 ≤ (3 : ℕ)^b*r := by nlinarith
  have h := producto_de_fallo (by positivity : 0 < (9 : ℕ)^a)
    (by omega : 0 < s) hsemilla hdivision (by rw [hl, hrp]; exact hf) (escala a) hvr
  simpa only [← pow_mul, Nat.mul_comm] using h

theorem altura_dieciocho {b r s : ℕ}
    (h : 1024*2^(3*b)*(r*s)^2 < 3^(2*b)) :
    (6*r*s)^18 < (3 : ℕ)^b := by
  have h1 : (6*r*s)^2 * 2^(3*b) < (3 : ℕ)^(2*b) := by
    nlinarith only [h, Nat.zero_le (2^(3*b)*(r*s)^2)]
  have h2 := Nat.pow_lt_pow_left h1 (by decide : 9 ≠ 0)
  have h3 : (3 : ℕ)^(17*b) ≤ 2^(27*b) := by
    simpa only [pow_mul] using
      pow_le_pow_left' (by norm_num : (3 : ℕ)^17 ≤ 2^27) b
  have h4 : (6*r*s)^18 * 2^(27*b) < (3 : ℕ)^b * 3^(17*b) := by
    convert h2 using 1
    · simp only [mul_pow, ← pow_mul]
      congr 2
      omega
    · rw [← pow_add, ← pow_mul]
      congr 1
      omega
  have h5 := Nat.mul_le_mul_left ((6*r*s)^18) h3
  have h6 : (6*r*s)^18 * 3^(17*b) < (3 : ℕ)^b * 3^(17*b) := h5.trans_lt h4
  exact Nat.lt_of_mul_lt_mul_right h6

theorem criterio_producto {a b ell k r s : ℕ}
    (hb : 1 ≤ b) (hr : 1 ≤ r) (hs : 1 ≤ s)
    (hsemilla : 2^(3*a+2)*(2^b*r+1) ≤ 9^a*2^ell)
    (hdivision : 2^k*s = 3^b*r+1)
    (haltura : (3 : ℕ)^b ≤ (6*r*s)^18) :
    b+2*k ≤ 3*a+3+4*ell := by
  by_contra he
  have hf := fallo_producto hb hr hs hsemilla hdivision (by omega)
  have hh := altura_dieciocho hf
  omega

theorem radical_condicional {b r s rad C : ℕ}
    (h : (6*r*s)^18 < (3 : ℕ)^b)
    (hrad : rad ≤ 6*r*s) (hc : (3 : ℕ)^b ≤ C) :
    rad^18 < C :=
  (pow_le_pow_left' hrad 18).trans_lt (h.trans_le hc)

theorem presupuesto_bab_siete {a b c ell vin vfin : ℕ}
    (hin : vin = 3*a+2)
    (hb : 17*b+34 ≤ 17*ell+3*a)
    (hv : 17*(3*c+vfin) ≤ 17*ell+3*a+10*b) :
    7*(3*a+b+3*c)+17*vfin ≤ 17*vin+34*ell := by
  omega

theorem presupuesto_aba_siete {L vin vfin ell : ℕ}
    (h : L+2*vfin ≤ 2*vin+4*ell) :
    7*L+17*vfin ≤ 17*vin+34*ell := by
  omega

end PerdicesAlturaBAB

#print axioms PerdicesAlturaBAB.producto_de_fallo
#print axioms PerdicesAlturaBAB.escala
#print axioms PerdicesAlturaBAB.fallo_producto
#print axioms PerdicesAlturaBAB.altura_dieciocho
#print axioms PerdicesAlturaBAB.criterio_producto
#print axioms PerdicesAlturaBAB.radical_condicional
#print axioms PerdicesAlturaBAB.presupuesto_bab_siete
#print axioms PerdicesAlturaBAB.presupuesto_aba_siete
