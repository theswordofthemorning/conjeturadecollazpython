import OcelotasPrefijosTestigos
import OcelotasCribaPrefijosDescuento

/-! # Hojas con exponente propuesto para la criba descontada

La cota máxima X debe ser positiva. Esa condición garantiza que el
exponente calculado es al menos 256, también para estados arbitrarios.
En los estados que representan órbitas positivas se cumple X>=1.
-/

namespace OcelotasPrefijosDescuentoTestigos

open Ocelotas OcelotasCribaPrefijosDescuento
open OcelotasResiduos (numerador)

set_option maxRecDepth 8192

theorem exponente_minimo {x : ℕ} (hx : 2 ≤ x) :
    256 ≤ OcelotasPrefijosBinarios.exponente x := by
  have hp := le_trans (Nat.pow_le_pow_left hx 256)
    (OcelotasPrefijosBinarios.potencia_exponente x)
  exact (Nat.pow_le_pow_iff_right (by decide : 1 < (2 : ℕ))).1 hp

theorem acepta_rama {limite qmin R r m a c q s combustible : ℕ} {anterior : Bool}
    (ha : m ≤ a)
    (h0 : comprobar limite qmin R r (2 * m) (numerador a c) (T c)
      (q + c % 2) (s + incremento c anterior) (decide (c % 2 = 1)) combustible = true)
    (h1 : comprobar limite qmin R (r + m) (2 * m)
      (numerador a (a + c)) (T (a + c)) (q + (a + c) % 2)
      (s + incremento (a + c) anterior) (decide ((a + c) % 2 = 1)) combustible = true) :
    comprobar limite qmin R r m a c q s anterior (combustible + 1) = true := by
  rw [comprobar]
  split
  · rfl
  · rw [if_neg (by omega)]
    split
    · rfl
    · split
      · rfl
      · rw [h0, h1]; rfl

theorem acepta_criba {limite qmin R r m a c q s combustible B : ℕ} {anterior : Bool}
    (ha : m ≤ a) (hanterior : anterior = false)
    (hX : 1 ≤ a * ((limite - r) / m) + c)
    (hpot : (a * ((limite - r) / m) + c + 1) ^ 256 ≤ 2 ^ B)
    (hcota : q + (R - s) + OcelotasPrefijosAfinados.cota (B - 256) (R - s) < qmin) :
    comprobar limite qmin R r m a c q s anterior (combustible + 1) = true := by
  have hb : OcelotasPrefijosBinarios.exponente (a * ((limite - r) / m) + c + 1) ≤ B := by
    rw [OcelotasExponenteBinarioExacto.exponente_igual]
    exact (OcelotasExponenteBinarioExacto.techo_equiv _ _).2 hpot
  have hmin : 256 ≤ OcelotasPrefijosBinarios.exponente (a * ((limite - r) / m) + c + 1) :=
    exponente_minimo (by omega)
  have hmono := OcelotasPrefijosTestigos.cota_monotona_exponente
    (Nat.sub_le_sub_right hb 256) (R - s)
  rw [comprobar]
  split
  · rfl
  · rw [if_neg (by omega)]
    split
    · rfl
    · rw [if_pos ⟨hanterior, hmin, by omega⟩]

theorem acepta_vacio {limite qmin R r m a c q s combustible : ℕ} {anterior : Bool}
    (hr : limite < r) :
    comprobar limite qmin R r m a c q s anterior (combustible + 1) = true := by
  rw [comprobar, if_pos hr]

theorem acepta_descenso {limite qmin R r m a c q s combustible : ℕ} {anterior : Bool}
    (ha : a < m) (hc : c < r) :
    comprobar limite qmin R r m a c q s anterior (combustible + 1) = true := by
  rw [comprobar]
  split
  · rfl
  · simpa only [if_pos ha] using decide_eq_true hc

theorem acepta_exceso {limite qmin R r m a c q s combustible : ℕ} {anterior : Bool}
    (ha : m ≤ a) (hs : R < s) :
    comprobar limite qmin R r m a c q s anterior (combustible + 1) = true := by
  rw [comprobar]
  split
  · rfl
  · simp only [if_neg (by omega : ¬a < m)]

end OcelotasPrefijosDescuentoTestigos

#print axioms OcelotasPrefijosDescuentoTestigos.exponente_minimo
#print axioms OcelotasPrefijosDescuentoTestigos.acepta_rama
#print axioms OcelotasPrefijosDescuentoTestigos.acepta_criba
#print axioms OcelotasPrefijosDescuentoTestigos.acepta_vacio
#print axioms OcelotasPrefijosDescuentoTestigos.acepta_descenso
#print axioms OcelotasPrefijosDescuentoTestigos.acepta_exceso
