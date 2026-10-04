import OcelotasExponenteBinarioExacto
import OcelotasCribaPrefijosBinarios

/-! # Certificados de prefijos con una cota de exponente proporcionada

En una rama basta certificar ambos hijos. En una hoja de criba basta
proporcionar B y comprobar una potencia y una desigualdad entera.
Así se puede evitar volver a calcular el exponente durante la evaluación.
-/

namespace OcelotasPrefijosTestigos

open Ocelotas OcelotasCribaPrefijosBinarios
open OcelotasResiduos (numerador)

theorem cota_monotona_exponente {B C : ℕ} (h : B ≤ C) (r : ℕ) :
    OcelotasPrefijosAfinados.cota B r ≤ OcelotasPrefijosAfinados.cota C r := by
  induction r with
  | zero => rfl
  | succ r ih =>
    simp only [OcelotasPrefijosAfinados.cota]
    exact Nat.div_le_div_right (Nat.add_le_add (Nat.mul_le_mul_left 25 h)
      (Nat.mul_le_mul_left 10144 ih))

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
    (hpot : (a * ((limite - r) / m) + c + 1) ^ 256 ≤ 2 ^ B)
    (hcota : q + OcelotasPrefijosAfinados.cota B (R - s) < qmin) :
    comprobar limite qmin R r m a c q s anterior (combustible + 1) = true := by
  have hb : OcelotasPrefijosBinarios.exponente (a * ((limite - r) / m) + c + 1) ≤ B := by
    rw [OcelotasExponenteBinarioExacto.exponente_igual]
    exact (OcelotasExponenteBinarioExacto.techo_equiv _ _).2 hpot
  have hmono := cota_monotona_exponente hb (R - s)
  rw [comprobar]
  split
  · rfl
  · rw [if_neg (by omega)]
    split
    · rfl
    · rw [if_pos ⟨hanterior, by omega⟩]

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
  · simp [show ¬a < m by omega, hs]

end OcelotasPrefijosTestigos

#print axioms OcelotasPrefijosTestigos.cota_monotona_exponente
#print axioms OcelotasPrefijosTestigos.acepta_rama
#print axioms OcelotasPrefijosTestigos.acepta_criba
#print axioms OcelotasPrefijosTestigos.acepta_vacio
#print axioms OcelotasPrefijosTestigos.acepta_descenso
#print axioms OcelotasPrefijosTestigos.acepta_exceso
