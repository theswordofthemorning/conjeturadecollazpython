import OcelotasCribaPrefijos

/-! # Ocelotas: ensamblaje de bloques para la criba por prefijos

Permite evaluar subárboles por separado en el núcleo y unirlos sin
repetir su evaluación. Las condiciones de la rama también se comprueban.
-/

namespace OcelotasPrefijosBloques

open Ocelotas OcelotasRachas OcelotasResiduos OcelotasCribaPrefijos

theorem acepta_rama {limite qmin R r m a c q s combustible : ℕ} {anterior : Bool}
    (hr : r ≤ limite) (ha : m ≤ a) (hs : s ≤ R)
    (hcriba : ¬(anterior = false ∧
      q + cota (R - s) (Nat.log2 (a * ((limite - r) / m) + c + 1) + 1) < qmin))
    (h0 : OcelotasCribaPrefijos.comprobar limite qmin R r (2 * m) (numerador a c) (T c)
      (q + c % 2) (s + incremento c anterior) (decide (c % 2 = 1)) combustible = true)
    (h1 : OcelotasCribaPrefijos.comprobar limite qmin R (r + m) (2 * m)
      (numerador a (a + c)) (T (a + c)) (q + (a + c) % 2)
      (s + incremento (a + c) anterior) (decide ((a + c) % 2 = 1)) combustible = true) :
    OcelotasCribaPrefijos.comprobar limite qmin R r m a c q s anterior (combustible + 1) = true := by
  rw [OcelotasCribaPrefijos.comprobar, if_neg (by omega), if_neg (by omega),
    if_neg (by omega), if_neg hcriba, h0, h1]
  rfl

end OcelotasPrefijosBloques

#print axioms OcelotasPrefijosBloques.acepta_rama
