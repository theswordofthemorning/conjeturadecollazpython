import OcelotasExponenteBinarioExacto
import OcelotasCribaPrefijosAfinados
import OcelotasCribaPrefijosBinarios

/-! # La bisección conserva el veredicto para cualquier estado y combustible

La igualdad es puramente computacional: vale también para estados que
no representan una órbita. No se añade ninguna hipótesis matemática.
-/

namespace OcelotasVerificadoresEquivalentes

theorem comprobar_igual (limite qmin R combustible : ℕ) :
    ∀ r m a c q s anterior,
    OcelotasCribaPrefijosBinarios.comprobar limite qmin R r m a c q s anterior combustible =
    OcelotasCribaPrefijosAfinados.comprobar limite qmin R r m a c q s anterior combustible := by
  induction combustible with
  | zero => intros; rfl
  | succ combustible ih =>
    intros
    simp only [OcelotasCribaPrefijosBinarios.comprobar,
      OcelotasCribaPrefijosAfinados.comprobar,
      OcelotasExponenteBinarioExacto.exponente_igual,
      OcelotasCribaPrefijosBinarios.incremento,
      OcelotasCribaPrefijosAfinados.incremento, ih]

end OcelotasVerificadoresEquivalentes

#print axioms OcelotasVerificadoresEquivalentes.comprobar_igual
