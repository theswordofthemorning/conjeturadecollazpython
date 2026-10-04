import OcelotasCribaPrefijosSuelo

/-! # Piloto acotado: semillas 4095..8191, q>=60, hasta cuatro rachas

El nucleo evalua el verificador. El JSON de preparacion no es una premisa.
Es un piloto de la criba, no una ampliacion de la frontera global de CST.
-/

namespace OcelotasSueloPiloto

open Ocelotas OcelotasContador

set_option maxRecDepth 8192
set_option maxHeartbeats 2000000

theorem acepta :
    OcelotasCribaPrefijosSuelo.comprobar 8191 60 4 4095 1 1 4095 0 0 false 64 = true := by
  decide +kernel

theorem descenso {n k : ℕ} (hn : 4095 ≤ n) (hlim : n ≤ 8191)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 4) (hq : 60 ≤ S k n) : T^[k] n < n := by
  exact OcelotasCribaPrefijosSuelo.certificado_descenso (by decide) acepta hn hlim hk hr hq

end OcelotasSueloPiloto

#print axioms OcelotasSueloPiloto.acepta
#print axioms OcelotasSueloPiloto.descenso
