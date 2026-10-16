import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Presupuesto A^a B^b A^c bajo las identidades afines exactas de las rachas.
El enlace de estas identidades con la concatenación de pasos se escribe en
DOS_CAMBIOS.md. No se afirma el presupuesto para todas las palabras A/B.
-/

namespace PerdicesDosCambios

theorem cota_tres (s : ℕ) : (3 : ℕ) ^ (17*s) ≤ 2 ^ (27*s) := by
  simpa only [pow_mul] using
    pow_le_pow_left' (by norm_num : (3 : ℕ)^17 ≤ 2^27) s

theorem cota_orden {d s X Y ell v : ℕ}
    (h : 2^d * Y ≤ 3^s * X) (hx : X ≤ 2^ell) (hy : 2^v ≤ Y) :
    17*(d+v) ≤ 27*s+17*ell := by
  have hi : (2 : ℕ)^(d+v) ≤ 3^s * 2^ell := by
    rw [pow_add]
    exact (Nat.mul_le_mul_left _ hy).trans (h.trans (Nat.mul_le_mul_left _ hx))
  have hp := pow_le_pow_left' hi 17
  have ht := Nat.mul_le_mul_right (2^(17*ell)) (cota_tres s)
  have he : (2 : ℕ)^(17*(d+v)) ≤ 2^(27*s+17*ell) := by
    calc
      _ = (2^(d+v))^17 := by rw [← pow_mul]; congr 1; omega
      _ ≤ (3^s * 2^ell)^17 := hp
      _ = 3^(17*s) * 2^(17*ell) := by
        rw [mul_pow, ← pow_mul, ← pow_mul]
        congr 2 <;> omega
      _ ≤ 2^(27*s) * 2^(17*ell) := ht
      _ = _ := (pow_add _ _ _).symm
  exact (Nat.pow_le_pow_iff_right (by norm_num : 1 < (2 : ℕ))).mp he

theorem consumo {d s X Y : ℕ} (h : 2^d * Y = 3^s * X)
    (hx : 0 < X) (hy : 0 < Y) :
    d + padicValNat 2 Y = padicValNat 2 X := by
  have he := congrArg (padicValNat 2) h
  have ht : padicValNat 2 3 = 0 := padicValNat.eq_zero_of_not_dvd (by decide)
  rw [padicValNat.mul (by positivity) (by omega),
      padicValNat.mul (by positivity) (by omega),
      padicValNat.pow, padicValNat.pow, padicValNat_self, ht] at he
  simpa using he

theorem orden_entrada_b {y : ℕ} (hy : y % 8 = 3) :
    padicValNat 2 (y+1) = 2 := by
  have hi : 2 ≤ padicValNat 2 (y+1) :=
    (padicValNat_dvd_iff_le (by omega : y+1 ≠ 0)).mp
      (by apply Nat.dvd_of_mod_eq_zero; norm_num; omega)
  have hs : ¬ 3 ≤ padicValNat 2 (y+1) := by
    intro he
    have hd := (padicValNat_dvd_iff_le (by omega : y+1 ≠ 0)).mpr he
    have hm := Nat.mod_eq_zero_of_dvd hd
    norm_num at hm
    omega
  omega

theorem cierre_lineal {a b c ell vin vfin : ℕ}
    (hin : vin = a+2) (he : a+2 ≤ ell)
    (hb : 51*b ≤ 17*ell+10*a)
    (hv : 17*(c+vfin) ≤ 17*ell+10*a+3*b) :
    a+3*b+c+2*vfin ≤ 2*vin+4*ell := by
  omega

theorem presupuesto_aba {a b c n y z w ell : ℕ}
    (hA : 2^a * (y+1) = 3^a * (n+1))
    (hB : 2^(3*b) * (z+5) = 3^(2*b) * (y+5))
    (hC : 2^c * (w+1) = 3^c * (z+1))
    (hy : y % 8 = 3) (he : n+5 ≤ 2^ell) :
    a+3*b+c+2*padicValNat 2 (w+1) ≤
      2*padicValNat 2 (n+1)+4*ell := by
  have hvin := consumo hA (by omega) (by omega)
  rw [orden_entrada_b hy] at hvin
  have hvfin := consumo hC (by omega) (by omega)
  have hu := consumo hB (by omega) (by omega)
  have hvn : (2 : ℕ)^padicValNat 2 (n+1) ≤ n+1 :=
    Nat.le_of_dvd (by omega) pow_padicValNat_dvd
  have hin : a+2 ≤ ell := by
    have hle : (2 : ℕ)^(a+2) ≤ 2^ell := by
      rw [hvin]
      exact hvn.trans ((by omega : n+1 ≤ n+5).trans he)
    exact (Nat.pow_le_pow_iff_right (by norm_num : 1 < (2 : ℕ))).mp hle
  have hAy : 2^a * (y+5) ≤ 3^a * (n+5) := by
    have ht : (2 : ℕ)^a ≤ 3^a := pow_le_pow_left' (by decide) a
    nlinarith only [hA, ht]
  have hvy : (2 : ℕ)^padicValNat 2 (y+5) ≤ y+5 :=
    Nat.le_of_dvd (by omega) pow_padicValNat_dvd
  have hby := cota_orden hAy he hvy
  have hb : 51*b ≤ 17*ell+10*a := by omega
  have hAz : 2^(a+3*b) * (z+1) ≤ 3^(a+2*b) * (n+5) := by
    calc
      _ ≤ 2^(a+3*b) * (z+5) := Nat.mul_le_mul_left _ (by omega)
      _ = 3^(2*b) * (2^a * (y+5)) := by
        rw [pow_add]
        calc
          _ = 2^a * (2^(3*b) * (z+5)) := by ring
          _ = _ := by rw [hB]; ring
      _ ≤ 3^(2*b) * (3^a * (n+5)) := Nat.mul_le_mul_left _ hAy
      _ = _ := by rw [pow_add]; ring
  have hvz : (2 : ℕ)^padicValNat 2 (z+1) ≤ z+1 :=
    Nat.le_of_dvd (by omega) pow_padicValNat_dvd
  have hz := cota_orden hAz he hvz
  apply cierre_lineal hvin.symm hin hb
  omega

theorem region_bab {a b c ell vin vfin : ℕ}
    (hin : vin = 3*a+2)
    (hv : 17*(3*c+vfin) ≤ 17*ell+3*a+10*b)
    (hr : 37*b ≤ 34*ell+45*a+51*c+68) :
    3*a+b+3*c+2*vfin ≤ 2*vin+4*ell := by
  omega

theorem reduccion_bab {a b c ell k vfin : ℕ} (hv : vfin+3*c = k+2) :
    (3*a+b+3*c+2*vfin ≤ 2*(3*a+2)+4*ell) ↔
      b+2*k ≤ 3*a+3*c+4*ell := by
  omega

end PerdicesDosCambios

#print axioms PerdicesDosCambios.cota_tres
#print axioms PerdicesDosCambios.cota_orden
#print axioms PerdicesDosCambios.consumo
#print axioms PerdicesDosCambios.orden_entrada_b
#print axioms PerdicesDosCambios.cierre_lineal
#print axioms PerdicesDosCambios.presupuesto_aba
#print axioms PerdicesDosCambios.region_bab
#print axioms PerdicesDosCambios.reduccion_bab
