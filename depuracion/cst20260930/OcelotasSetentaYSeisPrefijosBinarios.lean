import OcelotasCribaPrefijosBinarios

/-! # Ocelotas: ventana de 76 rachas que rebasa el umbral externo

El certificado se evalua en el nucleo. No presupone LMN ni Rozier-Terracol.
-/

namespace OcelotasSetentaYSeisPrefijosBinarios

open Ocelotas OcelotasContador OcelotasCribaPrefijosBinarios

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem certificado : comprobar 42380653296441592424 130441933147714940 76
    28000000000000000001 1 1 28000000000000000001 0 0 false 256 = true := by
  decide +kernel

theorem descenso {n k : ℕ} (hn : 28000000000000000001 ≤ n)
    (hmax : n ≤ 42380653296441592424) (hk : PrimerCruce n k)
    (hr : rachas n k ≤ 76) (hq : 130441933147714940 ≤ S k n) : T^[k] n < n :=
  certificado_descenso certificado hn hmax hk hr hq

end OcelotasSetentaYSeisPrefijosBinarios

#print axioms OcelotasSetentaYSeisPrefijosBinarios.certificado
#print axioms OcelotasSetentaYSeisPrefijosBinarios.descenso
